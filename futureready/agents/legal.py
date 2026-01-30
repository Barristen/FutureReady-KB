"""
LegalAgent - 法务部门专用 Agent
专注于合同分析、合规检查、法规监控
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from futureready.agents.base import BaseAgent
from futureready.core.models import AgentResponse, Alert, AlertSeverity, SearchQuery


class LegalAgent(BaseAgent):
    """
    法务专用 Agent
    
    核心能力:
    1. 合同风险识别
    2. 合规性检查
    3. 法规变化监控
    4. 历史案例检索
    """
    
    async def query(
        self, 
        question: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """回答法务相关问题"""
        
        # 1. 构建搜索查询
        search_query = SearchQuery(
            query=question,
            department="legal",
            limit=10
        )
        
        # 添加时间范围 (如果提供)
        if context and "date_range" in context:
            search_query.date_range = context["date_range"]
        
        # 2. 检索相关文档
        results = await self.kb.search(search_query)
        documents = [r.document for r in results]
        
        if not documents:
            return AgentResponse(
                answer="抱歉，在法务知识库中没有找到相关文档。",
                sources=[],
                confidence=0.0
            )
        
        # 3. 如果没有 LLM，返回基础检索结果
        if not self.llm:
            answer = self._build_basic_answer(question, results)
            return AgentResponse(
                answer=answer,
                sources=[d.id for d in documents],
                confidence=0.6
            )
        
        # 4. 使用 LLM 生成答案
        prompt = self._build_legal_prompt(question, documents)
        llm_response = await self.llm.generate(prompt)
        
        return AgentResponse(
            answer=llm_response["text"],
            sources=[d.id for d in documents],
            confidence=llm_response.get("confidence", 0.8),
            reasoning_trace=[
                f"检索到 {len(documents)} 份相关法务文档",
                f"使用 {self.llm.model} 模型进行分析"
            ]
        )
    
    async def monitor(self) -> List[Alert]:
        """
        主动监控法律风险
        
        监控内容:
        1. 新政策/法规变化
        2. 合同到期预警
        3. 潜在合规冲突
        """
        alerts = []
        
        # 监控1: 检查最近30天的新政策
        alerts.extend(await self._monitor_policy_changes())
        
        # 监控2: 检查即将到期的合同
        alerts.extend(await self._monitor_contract_expiry())
        
        # 监控3: 检查潜在的合规冲突
        alerts.extend(await self._monitor_compliance_conflicts())
        
        return alerts
    
    def _build_legal_prompt(self, question: str, documents: List[Any]) -> str:
        """构建法务专用提示词"""
        return f"""你是一位专业的企业法务顾问。基于以下法务文档回答问题。

{self._format_docs(documents)}

用户问题: {question}

请提供专业的法务建议，注意:
1. 明确指出法律依据和相关文档
2. 如果涉及风险，请明确说明风险等级
3. 如果需要进一步法律审查，请明确建议
4. 使用专业但易懂的语言

答案:
"""
    
    def _build_basic_answer(self, question: str, results: List[Any]) -> str:
        """构建基础答案 (不使用 LLM)"""
        answer_parts = [
            f"在法务知识库中找到 {len(results)} 份相关文档:\n"
        ]
        
        for i, result in enumerate(results[:5], 1):
            doc = result.document
            answer_parts.append(
                f"{i}. {doc.metadata.business_context} "
                f"(上传时间: {doc.metadata.upload_time.strftime('%Y-%m-%d')})"
            )
        
        if len(results) > 5:
            answer_parts.append(f"\n... 以及其他 {len(results) - 5} 份文档")
        
        return "\n".join(answer_parts)
    
    async def _monitor_policy_changes(self) -> List[Alert]:
        """监控政策变化"""
        alerts = []
        
        # 获取最近30天上传的政策文件
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        search_query = SearchQuery(
            query="",
            department="legal",
            tags=["policy", "regulation", "law"],
            date_range=(thirty_days_ago, datetime.now()),
            limit=50
        )
        
        recent_policies = await self.kb.search(search_query)
        
        if len(recent_policies) > 0:
            # TODO: 实现更智能的冲突检测
            # 这里简化为: 如果有新政策就发预警
            alerts.append(Alert(
                type="policy_update",
                severity=AlertSeverity.MEDIUM,
                message=f"最近30天内上传了 {len(recent_policies)} 份新的政策文件，建议审查是否影响现有合同和流程。",
                affected_doc_ids=[r.document.id for r in recent_policies],
                metadata={
                    "policy_count": len(recent_policies),
                    "period": "last_30_days"
                }
            ))
        
        return alerts
    
    async def _monitor_contract_expiry(self) -> List[Alert]:
        """监控合同到期"""
        alerts = []
        
        # 获取所有有到期时间的合同
        search_query = SearchQuery(
            query="",
            department="legal",
            tags=["contract"],
            limit=1000
        )
        
        contracts = await self.kb.search(search_query)
        
        # 检查即将到期的合同 (未来60天内)
        sixty_days_later = datetime.now() + timedelta(days=60)
        expiring_soon = []
        
        for result in contracts:
            doc = result.document
            if doc.metadata.expiry_date:
                if datetime.now() <= doc.metadata.expiry_date <= sixty_days_later:
                    expiring_soon.append(doc)
        
        if expiring_soon:
            alerts.append(Alert(
                type="contract_expiry",
                severity=AlertSeverity.HIGH,
                message=f"有 {len(expiring_soon)} 份合同将在未来60天内到期，请及时处理续约或终止事宜。",
                affected_doc_ids=[d.id for d in expiring_soon],
                metadata={
                    "expiring_count": len(expiring_soon),
                    "period_days": 60
                }
            ))
        
        return alerts
    
    async def _monitor_compliance_conflicts(self) -> List[Alert]:
        """监控合规冲突"""
        alerts = []
        
        # TODO: 实现更复杂的冲突检测逻辑
        # 例如: 新政策要求 vs 现有合同条款
        # 这需要更强的 AI 能力来分析文档内容
        
        # 当前实现: 占位符
        # 在未来的版本中，这里会使用 LLM 进行深度分析
        
        return alerts
    
    async def analyze_contract_risk(self, contract_doc_id: str) -> Dict[str, Any]:
        """
        分析特定合同的风险
        
        Returns:
            {
                "risk_score": 0.7,  # 0-1
                "risk_factors": ["连带责任", "无限期合同"],
                "recommendations": ["建议添加终止条款"]
            }
        """
        # TODO: 实现合同风险分析
        # 需要 LLM 能力来理解合同内容
        
        return {
            "risk_score": 0.0,
            "risk_factors": [],
            "recommendations": ["功能开发中，敬请期待"]
        }
