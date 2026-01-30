"""
FutureReady-KB 核心数据模型
定义文档、实体、关系等核心数据结构
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class DocumentType(str, Enum):
    """文档类型"""
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    TXT = "txt"
    HTML = "html"
    MARKDOWN = "md"
    WEB_ARCHIVE = "web_archive"


class EntityType(str, Enum):
    """实体类型"""
    PERSON = "person"
    ORGANIZATION = "organization"
    POLICY = "policy"
    DATE = "date"
    MONEY = "money"
    LOCATION = "location"
    LEGAL_TERM = "legal_term"
    CUSTOM = "custom"


class RelationType(str, Enum):
    """文档关系类型"""
    REFERENCES = "references"          # 引用
    SUPERSEDES = "supersedes"          # 取代/更新
    CONTRADICTS = "contradicts"        # 矛盾
    SUPPLEMENTS = "supplements"        # 补充
    RELATES_TO = "relates_to"          # 相关


class AlertSeverity(str, Enum):
    """预警严重程度"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Entity:
    """提取的实体"""
    type: EntityType
    value: str
    confidence: float
    source_doc_id: str
    context: Optional[str] = None  # 实体出现的上下文
    
    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")


@dataclass
class DocumentMetadata:
    """文档元数据 - 这是系统的核心"""
    
    # === 强制字段 (Mandatory) ===
    uploader_id: str                    # 上传者ID/邮箱
    upload_time: datetime               # 上传时间
    department: str                     # 所属部门
    business_context: str               # 业务上下文 (为什么上传这个文档?)
    
    # === 推荐字段 (Recommended) ===
    tags: List[str] = field(default_factory=list)
    related_doc_ids: List[str] = field(default_factory=list)
    expiry_date: Optional[datetime] = None  # 文档过期时间
    
    # === 可选字段 (Optional) ===
    version: Optional[str] = None
    source_url: Optional[str] = None    # 如果是网页存档
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> None:
        """验证元数据完整性"""
        if not self.business_context or len(self.business_context.strip()) < 10:
            raise ValueError(
                "business_context 必须至少10个字符! "
                "请说明为什么上传这个文档，例如: "
                "'新政策要求保存3年' 或 '关键客户合同，涉及连带责任'"
            )
        
        if not self.uploader_id or "@" not in self.uploader_id:
            raise ValueError("uploader_id 必须是有效的邮箱地址")


@dataclass
class Document:
    """文档主体"""
    id: str
    file_path: str
    content_type: DocumentType
    
    # 元数据
    metadata: DocumentMetadata
    
    # 文档内容
    raw_content: Optional[bytes] = None
    parsed_text: Optional[str] = None
    
    # AI 增强数据
    embeddings: Optional[List[float]] = None
    ai_summary: Optional[str] = None
    extracted_entities: List[Entity] = field(default_factory=list)
    ai_risk_score: Optional[float] = None
    
    # 系统字段
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1
    
    def __post_init__(self):
        self.metadata.validate()


@dataclass
class DocumentRelation:
    """文档之间的关系"""
    source_doc_id: str
    target_doc_id: str
    relation_type: RelationType
    confidence: float
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentResponse:
    """Agent 响应结构"""
    answer: str
    sources: List[str]  # 引用的文档ID列表
    confidence: float
    reasoning_trace: Optional[List[str]] = None  # 推理过程
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Alert:
    """系统预警"""
    type: str
    severity: AlertSeverity
    message: str
    affected_doc_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False


@dataclass
class SearchQuery:
    """搜索查询"""
    query: str
    department: Optional[str] = None
    tags: Optional[List[str]] = None
    date_range: Optional[tuple[datetime, datetime]] = None
    doc_types: Optional[List[DocumentType]] = None
    limit: int = 10
    
    # 时间旅行查询
    as_of_date: Optional[datetime] = None  # 查询"某个时间点的知识"


@dataclass
class SearchResult:
    """搜索结果"""
    document: Document
    score: float  # 相关性得分
    highlights: List[str] = field(default_factory=list)  # 匹配片段
