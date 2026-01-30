"""
KnowledgeBase - 核心知识库类
处理文档摄入、存储、检索
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from futureready.core.models import (
    Document, DocumentMetadata, DocumentType, 
    SearchQuery, SearchResult, Entity
)


class KnowledgeBase:
    """
    企业知识库核心类
    
    主要功能:
    1. 文档摄入 (ingest)
    2. 文档检索 (search)
    3. 文档管理 (get/update/delete)
    4. 时间旅行查询 (temporal queries)
    """
    
    def __init__(self, base_path: str, department: Optional[str] = None):
        """
        初始化知识库
        
        Args:
            base_path: 知识库存储路径
            department: 部门名称 (可选，用于多部门隔离)
        """
        self.base_path = Path(base_path)
        self.department = department
        
        # 创建目录结构
        self.docs_path = self.base_path / "documents"
        self.metadata_path = self.base_path / "metadata"
        self.index_path = self.base_path / "index"
        
        for path in [self.docs_path, self.metadata_path, self.index_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # 加载索引
        self.index = self._load_index()
    
    async def ingest(
        self, 
        file_path: str,
        metadata: Dict[str, Any],
        parse_content: bool = True
    ) -> Document:
        """
        摄入新文档
        
        Args:
            file_path: 文档文件路径
            metadata: 元数据字典
            parse_content: 是否解析文档内容
            
        Returns:
            Document: 创建的文档对象
        """
        # 1. 验证文件存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 2. 创建元数据对象
        doc_metadata = DocumentMetadata(
            uploader_id=metadata["uploader"],
            upload_time=datetime.now(),
            department=metadata.get("department", self.department),
            business_context=metadata["business_context"],
            tags=metadata.get("tags", []),
            related_doc_ids=metadata.get("related_docs", []),
            expiry_date=metadata.get("expiry_date"),
            source_url=metadata.get("source_url")
        )
        
        # 验证元数据
        doc_metadata.validate()
        
        # 3. 生成文档ID
        doc_id = self._generate_doc_id(file_path)
        
        # 4. 确定文档类型
        ext = Path(file_path).suffix.lower()
        content_type = self._get_content_type(ext)
        
        # 5. 读取文件内容
        with open(file_path, 'rb') as f:
            raw_content = f.read()
        
        # 6. 解析内容 (可选)
        parsed_text = None
        if parse_content:
            parsed_text = await self._parse_document(raw_content, content_type)
        
        # 7. 创建文档对象
        document = Document(
            id=doc_id,
            file_path=str(Path(file_path).name),
            content_type=content_type,
            metadata=doc_metadata,
            raw_content=raw_content,
            parsed_text=parsed_text
        )
        
        # 8. 保存文档
        self._save_document(document)
        
        # 9. 更新索引
        self._update_index(document)
        
        print(f"✅ 文档已摄入: {doc_id}")
        print(f"   部门: {doc_metadata.department}")
        print(f"   上下文: {doc_metadata.business_context}")
        
        return document
    
    async def search(self, query: SearchQuery) -> List[SearchResult]:
        """
        搜索文档
        
        Args:
            query: 搜索查询对象
            
        Returns:
            List[SearchResult]: 搜索结果列表
        """
        results = []
        
        # 遍历所有文档
        for doc_id, doc_info in self.index.items():
            # 过滤部门
            if query.department and doc_info.get("department") != query.department:
                continue
            
            # 过滤标签
            if query.tags:
                doc_tags = set(doc_info.get("tags", []))
                if not any(tag in doc_tags for tag in query.tags):
                    continue
            
            # 过滤时间范围
            if query.date_range:
                upload_time = datetime.fromisoformat(doc_info["upload_time"])
                if not (query.date_range[0] <= upload_time <= query.date_range[1]):
                    continue
            
            # 时间旅行查询
            if query.as_of_date:
                upload_time = datetime.fromisoformat(doc_info["upload_time"])
                if upload_time > query.as_of_date:
                    continue  # 跳过在指定时间后上传的文档
            
            # 加载完整文档
            doc = self._load_document(doc_id)
            
            # 基础文本匹配 (简单实现)
            score = self._calculate_relevance_score(query.query, doc)
            
            if score > 0 or not query.query:  # 如果没有查询词，返回所有匹配的文档
                results.append(SearchResult(
                    document=doc,
                    score=score,
                    highlights=self._get_highlights(query.query, doc.parsed_text)
                ))
        
        # 按得分排序
        results.sort(key=lambda x: x.score, reverse=True)
        
        # 限制结果数量
        return results[:query.limit]
    
    async def get_document(self, doc_id: str) -> Optional[Document]:
        """获取指定文档"""
        return self._load_document(doc_id)
    
    async def update_metadata(
        self, 
        doc_id: str, 
        metadata_updates: Dict[str, Any]
    ) -> Document:
        """更新文档元数据"""
        doc = self._load_document(doc_id)
        if not doc:
            raise ValueError(f"文档不存在: {doc_id}")
        
        # 更新允许的字段
        if "tags" in metadata_updates:
            doc.metadata.tags = metadata_updates["tags"]
        if "business_context" in metadata_updates:
            doc.metadata.business_context = metadata_updates["business_context"]
        if "related_doc_ids" in metadata_updates:
            doc.metadata.related_doc_ids = metadata_updates["related_doc_ids"]
        
        doc.updated_at = datetime.now()
        doc.version += 1
        
        self._save_document(doc)
        self._update_index(doc)
        
        return doc
    
    def _generate_doc_id(self, file_path: str) -> str:
        """生成文档唯一ID"""
        timestamp = datetime.now().isoformat()
        content = f"{file_path}{timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _get_content_type(self, ext: str) -> DocumentType:
        """根据扩展名确定文档类型"""
        mapping = {
            ".pdf": DocumentType.PDF,
            ".docx": DocumentType.DOCX,
            ".doc": DocumentType.DOCX,
            ".xlsx": DocumentType.XLSX,
            ".xls": DocumentType.XLSX,
            ".txt": DocumentType.TXT,
            ".html": DocumentType.HTML,
            ".htm": DocumentType.HTML,
            ".md": DocumentType.MARKDOWN
        }
        return mapping.get(ext, DocumentType.TXT)
    
    async def _parse_document(
        self, 
        content: bytes, 
        content_type: DocumentType
    ) -> str:
        """
        解析文档内容
        TODO: 实现真实的文档解析 (PDF/Word等)
        """
        if content_type == DocumentType.TXT:
            return content.decode('utf-8', errors='ignore')
        else:
            # 其他格式暂时返回占位符
            # 实际使用需要集成 PyPDF2, python-docx 等库
            return f"[{content_type} 文档解析功能开发中]"
    
    def _save_document(self, document: Document) -> None:
        """保存文档到磁盘"""
        # 保存原始文件
        doc_file_path = self.docs_path / f"{document.id}.bin"
        with open(doc_file_path, 'wb') as f:
            f.write(document.raw_content)
        
        # 保存元数据
        metadata_file_path = self.metadata_path / f"{document.id}.json"
        metadata_dict = {
            "id": document.id,
            "file_path": document.file_path,
            "content_type": document.content_type.value,
            "metadata": {
                "uploader_id": document.metadata.uploader_id,
                "upload_time": document.metadata.upload_time.isoformat(),
                "department": document.metadata.department,
                "business_context": document.metadata.business_context,
                "tags": document.metadata.tags,
                "related_doc_ids": document.metadata.related_doc_ids,
                "expiry_date": document.metadata.expiry_date.isoformat() if document.metadata.expiry_date else None,
                "source_url": document.metadata.source_url
            },
            "parsed_text": document.parsed_text,
            "created_at": document.created_at.isoformat(),
            "updated_at": document.updated_at.isoformat(),
            "version": document.version
        }
        
        with open(metadata_file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_dict, f, ensure_ascii=False, indent=2)
    
    def _load_document(self, doc_id: str) -> Optional[Document]:
        """从磁盘加载文档"""
        metadata_file_path = self.metadata_path / f"{doc_id}.json"
        
        if not metadata_file_path.exists():
            return None
        
        with open(metadata_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 加载原始内容
        doc_file_path = self.docs_path / f"{doc_id}.bin"
        with open(doc_file_path, 'rb') as f:
            raw_content = f.read()
        
        # 重建文档对象
        metadata = DocumentMetadata(
            uploader_id=data["metadata"]["uploader_id"],
            upload_time=datetime.fromisoformat(data["metadata"]["upload_time"]),
            department=data["metadata"]["department"],
            business_context=data["metadata"]["business_context"],
            tags=data["metadata"]["tags"],
            related_doc_ids=data["metadata"]["related_doc_ids"],
            expiry_date=datetime.fromisoformat(data["metadata"]["expiry_date"]) if data["metadata"]["expiry_date"] else None,
            source_url=data["metadata"]["source_url"]
        )
        
        return Document(
            id=data["id"],
            file_path=data["file_path"],
            content_type=DocumentType(data["content_type"]),
            metadata=metadata,
            raw_content=raw_content,
            parsed_text=data.get("parsed_text"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            version=data["version"]
        )
    
    def _load_index(self) -> Dict[str, Any]:
        """加载索引"""
        index_file = self.index_path / "index.json"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _update_index(self, document: Document) -> None:
        """更新索引"""
        self.index[document.id] = {
            "file_path": document.file_path,
            "department": document.metadata.department,
            "tags": document.metadata.tags,
            "upload_time": document.metadata.upload_time.isoformat(),
            "business_context": document.metadata.business_context
        }
        
        # 保存索引
        index_file = self.index_path / "index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _calculate_relevance_score(self, query: str, document: Document) -> float:
        """
        计算相关性得分 (简单实现)
        TODO: 实现向量相似度计算
        """
        if not query:
            return 1.0
        
        query_lower = query.lower()
        score = 0.0
        
        # 检查业务上下文
        if document.metadata.business_context and query_lower in document.metadata.business_context.lower():
            score += 0.5
        
        # 检查标签
        if any(query_lower in tag.lower() for tag in document.metadata.tags):
            score += 0.3
        
        # 检查解析的文本
        if document.parsed_text and query_lower in document.parsed_text.lower():
            score += 0.2
        
        return min(score, 1.0)
    
    def _get_highlights(self, query: str, text: Optional[str]) -> List[str]:
        """提取匹配片段"""
        if not query or not text:
            return []
        
        # 简单实现: 找到包含查询词的句子
        highlights = []
        sentences = text.split('。')
        
        for sentence in sentences[:10]:  # 最多10个
            if query.lower() in sentence.lower():
                highlights.append(sentence.strip() + '。')
        
        return highlights
