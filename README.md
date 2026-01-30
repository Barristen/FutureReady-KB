# 🚀 FutureReady-KB

> **为下一代 AI 准备的企业知识基础设施**  
> Enterprise Knowledge Infrastructure for Future AI Agents

[English](#english) | [中文](#chinese)

---

## 🎯 核心理念 <a name="chinese"></a>

**现状**: 企业的关键知识正在流失
- 📄 政策文件2年后官网就删除  
- 👤 员工离职带走业务 know-how  
- 📊 历史决策无据可查

**未来**: AI Agent 需要高质量的企业数据
- ⚖️ 法务 AI: 自动识别合同风险  
- 📢 公关 AI: 危机预警和舆情分析  
- 💼 财务 AI: 合规自动检查

**矛盾**: 等 AI 成熟了再整理数据已经晚了

**解决方案**: 现在就开始积累，为 12-18 个月后的 AI 爆发做准备

---

## ⚡ 快速开始

```bash
# 克隆项目
git clone https://github.com/yourusername/FutureReady-KB.git
cd FutureReady-KB

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python -m futureready init --department legal

# 启动服务
python -m futureready serve
```

访问 `http://localhost:8000` 开始使用

---

## 📦 核心特性

### 1. 🗂️ 智能文档摄入
- ✅ 支持 PDF/Word/Excel/网页快照
- ✅ 自动提取元数据和实体
- ✅ **强制业务上下文标注** (这是关键!)

### 2. 🔍 多维检索引擎
- 🎯 语义搜索 (向量检索)
- ⏰ 时间线追溯 (历史查询)
- 🕸️ 知识图谱关联 (实体关系)

### 3. 🤖 Agent-Ready 设计
- 📡 标准化 API (REST + GraphQL)
- 🎭 部门专用 Agent 模板
- 🔬 推理过程可追溯

### 4. 📈 渐进式 AI 增强
- **当前** (已实现): 基础 OCR + 语义搜索
- **6个月**: 文档深度理解 + 智能问答
- **12个月**: 复杂推理 + 主动预警

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Legal AI │  │  PR AI   │  │ Custom   │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
└───────┼─────────────┼─────────────┼───────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼───────────────────┐
│              Knowledge Base API                        │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Semantic   │  │  Temporal    │  │   Graph      │ │
│  │  Retrieval  │  │  Retrieval   │  │   Query      │ │
│  └─────────────┘  └──────────────┘  └──────────────┘ │
└───────┬─────────────┬─────────────┬───────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼───────────────────┐
│                Storage Layer                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Docs   │  │ Vectors │  │  Graph  │  │Metadata │ │
│  │  (S3)   │  │(Qdrant) │  │ (Neo4j) │  │ (PG)    │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
└────────────────────────────────────────────────────────┘
```

---

## 📚 使用案例

### 案例 1: 法务部门自动化

```python
from futureready import LegalAgent, KnowledgeBase

# 初始化知识库
kb = KnowledgeBase(path="./legal_kb")

# 上传文档 (强制元数据)
kb.ingest(
    file_path="contract_v2.pdf",
    metadata={
        "uploader": "zhang.san@company.com",
        "department": "legal",
        "business_context": "重要客户续约合同，涉及连带责任条款",
        "tags": ["contract", "liability", "client_a"]
    }
)

# 创建法务 Agent
agent = LegalAgent(kb)

# 查询历史合同
result = await agent.query(
    "过去3年我们签的合同中，有多少包含连带责任条款？"
)

print(result.answer)
# "共发现 23 份合同包含连带责任条款..."

print(result.sources)
# [Document(id="doc_123", title="客户A合同"), ...]

# 主动监控
alerts = await agent.monitor()
for alert in alerts:
    print(f"⚠️  {alert.severity}: {alert.message}")
# ⚠️  HIGH: 新政策可能影响 5 份现有合同
```

### 案例 2: 自动网页存档

```python
from futureready import WebArchiver

# 监控关键网站
archiver = WebArchiver(kb_path="./pr_kb")

archiver.watch([
    "https://www.gov.cn/zhengce/",      # 政府政策
    "https://competitor.com/news/",     # 竞争对手
    "https://industry-news.com/"        # 行业动态
])

# 每天自动存档 + 变化检测
archiver.run(
    interval="daily",
    on_change=lambda diff: send_alert(diff)
)
```

### 案例 3: 时间旅行查询

```python
# 查询"某个时间点我们知道什么"
result = kb.query(
    "2023年3月我们对数据隐私的理解是什么？",
    as_of_date="2023-03-01"
)

# 对比不同时间点的知识差异
diff = kb.compare_timeline(
    query="GDPR合规要求",
    dates=["2022-01-01", "2023-01-01", "2024-01-01"]
)
```

---

## 🛠️ 自定义 Agent

```python
from futureready import BaseAgent, AgentResponse

class HRAgent(BaseAgent):
    """人力资源专用 Agent"""
    
    async def query(self, question: str) -> AgentResponse:
        # 1. 检索相关文档
        docs = await self.kb.retrieve(
            query=question,
            filters={"department": "hr"}
        )
        
        # 2. 构建提示词
        prompt = f"""
        基于以下HR文档回答问题:
        {self._format_docs(docs)}
        
        问题: {question}
        """
        
        # 3. LLM 推理
        response = await self.llm.generate(prompt)
        
        return AgentResponse(
            answer=response.text,
            sources=[d.id for d in docs],
            confidence=response.confidence
        )
    
    async def monitor(self):
        """监控劳动法变化"""
        recent_policies = await self.kb.get_documents(
            filters={
                "tags": ["labor_law", "policy"],
                "upload_time": "last_30_days"
            }
        )
        
        # 检查是否影响现有员工手册
        alerts = []
        for policy in recent_policies:
            conflicts = await self._check_handbook_conflicts(policy)
            if conflicts:
                alerts.append(Alert(
                    type="policy_update",
                    severity="medium",
                    message=f"新劳动法规可能要求更新员工手册"
                ))
        
        return alerts
```

---

## 📖 完整文档

- [安装指南](docs/installation.md)
- [API 文档](docs/api.md)
- [Agent 开发指南](docs/agent-development.md)
- [部署指南](docs/deployment.md)

---

## 🗺️ Roadmap

### Phase 1: MVP (已完成 ✅)
- [x] 核心框架
- [x] 文档摄入引擎
- [x] 基础检索
- [x] Legal Agent 示例
- [x] Docker 部署

### Phase 2: 增强功能 (进行中 🚧)
- [ ] 网页自动存档
- [ ] 知识图谱可视化
- [ ] PR Agent
- [ ] HR Agent
- [ ] Slack/飞书集成

### Phase 3: 企业级特性 (规划中 📋)
- [ ] 权限管理
- [ ] 审计日志
- [ ] 多租户支持
- [ ] 高级 Agent (复杂推理)

---

## 🤝 贡献指南

我们欢迎以下贡献:

1. 🎭 **新的部门 Agent 模板** (Finance/Marketing/R&D...)
2. 🔧 **更好的文档解析器** (特殊格式/OCR优化)
3. 📊 **真实使用案例** (成功故事/最佳实践)
4. 🐛 **Bug 报告和修复**

查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情

---

## 💡 为什么选择 FutureReady-KB?

与现有知识库系统对比:

| 特性 | 传统知识库 | FutureReady-KB |
|------|-----------|----------------|
| 目标 | 当下可用 | **为未来AI准备** |
| 元数据 | 可选 | **强制 + 业务上下文** |
| 检索 | 关键词 | 语义 + 时间 + 图谱 |
| AI集成 | 事后考虑 | **Agent-First 设计** |
| 专业化 | 通用工具 | **部门垂直方案** |

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/FutureReady-KB&type=Date)](https://star-history.com/#yourusername/FutureReady-KB&Date)

---

## 📬 联系我们

- 💬 讨论: [GitHub Discussions](https://github.com/yourusername/FutureReady-KB/discussions)
- 🐛 问题: [GitHub Issues](https://github.com/yourusername/FutureReady-KB/issues)
- 📧 邮件: contact@futureready-kb.dev

---

<div align="center">

**如果这个项目对你有帮助，请给我们一个 ⭐️**

Made with ❤️ by the FutureReady-KB Team

</div>

---

## 🌐 English Version <a name="english"></a>

### 🎯 Core Concept

**Current Reality**: Critical enterprise knowledge is vanishing
- 📄 Policy documents disappear from official sites after 2 years
- 👤 Employees leave, taking business know-how with them
- 📊 Historical decisions lack documentation

**Future Need**: AI Agents require high-quality enterprise data
- ⚖️ Legal AI: Automatic contract risk identification
- 📢 PR AI: Crisis early warning and sentiment analysis
- 💼 Finance AI: Automated compliance checking

**The Paradox**: Waiting for AI maturity before organizing data is too late

**Solution**: Start accumulating now, prepare for AI explosion in 12-18 months

### ⚡ Quick Start

```bash
git clone https://github.com/yourusername/FutureReady-KB.git
cd FutureReady-KB
pip install -r requirements.txt
python -m futureready init --department legal
python -m futureready serve
```

Visit `http://localhost:8000` to get started

### 📦 Key Features

1. **Smart Document Ingestion**: PDF/Word/Excel/Web snapshots with mandatory metadata
2. **Multi-dimensional Retrieval**: Semantic + Temporal + Graph queries
3. **Agent-Ready Design**: Standardized API with department-specific templates
4. **Progressive AI Enhancement**: From basic OCR (now) to complex reasoning (12 months)

[See full documentation above]

