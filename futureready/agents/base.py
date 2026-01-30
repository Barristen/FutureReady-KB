"""
BaseAgent - 所有 Agent 的抽象基类
定义了 Agent 的标准接口和行为
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from futureready.core.models import AgentResponse, Alert, SearchQuery
from futureready.core.knowledge_base import KnowledgeBase


class LLMProvider(ABC):
    """LLM 提供者抽象接口"""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成响应"""
        pass
    
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """生成文本向量"""
        pass


class BaseAgent(ABC):
    """
    Agent 基类 - 所有专业 Agent 继承此类
    
    核心职责:
    1. 查询 (query): 回答用户问题
    2. 监控 (monitor): 主动发现问题/预警
    """
    
    def __init__(
        self, 
        knowledge_base: KnowledgeBase,
        llm_provider: Optional[LLMProvider] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.kb = knowledge_base
        self.llm = llm_provider
        self.config = config or {}
        
    @abstractmethod
    async def query(
        self, 
        question: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        回答用户问题
        
        Args:
            question: 用户的问题
            context: 额外上下文 (时间范围、部门等)
            
        Returns:
            AgentResponse: 包含答案、来源、置信度等
        """
        pass
    
    async def monitor(self) -> List[Alert]:
        """
        主动监控 - 可选实现
        
        Returns:
            List[Alert]: 发现的预警列表
        """
        return []
    
    def _format_docs(self, documents: List[Any]) -> str:
        """格式化文档用于提示词"""
        formatted = []
        for i, doc in enumerate(documents, 1):
            formatted.append(f"[文档 {i}]")
            formatted.append(f"标题: {doc.metadata.business_context}")
            formatted.append(f"部门: {doc.metadata.department}")
            formatted.append(f"上传时间: {doc.metadata.upload_time}")
            if doc.parsed_text:
                # 截取前500字符
                text = doc.parsed_text[:500] + "..." if len(doc.parsed_text) > 500 else doc.parsed_text
                formatted.append(f"内容摘要: {text}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def _build_prompt(self, question: str, documents: List[Any]) -> str:
        """构建标准提示词"""
        return f"""你是一个专业的企业知识助手。基于以下文档回答用户问题。

{self._format_docs(documents)}

用户问题: {question}

请提供准确、专业的答案，并说明你的依据来自哪些文档。
如果文档中没有足够信息回答，请明确说明。
"""


class OpenAILLMProvider(LLMProvider):
    """OpenAI LLM 实现 (示例)"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        调用 OpenAI API
        实际使用时需要实现真实的 API 调用
        """
        # TODO: 实现真实的 OpenAI API 调用
        return {
            "text": "这是一个示例响应",
            "confidence": 0.85
        }
    
    async def embed(self, text: str) -> List[float]:
        """
        生成文本嵌入
        实际使用时需要实现真实的 API 调用
        """
        # TODO: 实现真实的 embedding API 调用
        return [0.1] * 1536  # OpenAI embedding 维度


class AnthropicLLMProvider(LLMProvider):
    """Anthropic Claude LLM 实现"""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.model = model
    
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """调用 Anthropic API"""
        # TODO: 实现真实的 Anthropic API 调用
        return {
            "text": "Claude 响应示例",
            "confidence": 0.9
        }
    
    async def embed(self, text: str) -> List[float]:
        """Anthropic 暂无官方 embedding API，可以使用其他服务"""
        # TODO: 使用 Voyage AI 或其他 embedding 服务
        return [0.1] * 1024
