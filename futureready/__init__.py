"""
FutureReady-KB - 为下一代 AI 准备的企业知识基础设施
"""

__version__ = "0.1.0"

from futureready.core.knowledge_base import KnowledgeBase
from futureready.core.models import (
    Document,
    DocumentMetadata,
    AgentResponse,
    Alert,
    SearchQuery,
)
from futureready.agents.base import BaseAgent, LLMProvider
from futureready.agents.legal import LegalAgent

__all__ = [
    "KnowledgeBase",
    "Document",
    "DocumentMetadata",
    "AgentResponse",
    "Alert",
    "SearchQuery",
    "BaseAgent",
    "LLMProvider",
    "LegalAgent",
]
