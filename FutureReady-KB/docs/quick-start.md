# 快速开始指南

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/FutureReady-KB.git
cd FutureReady-KB

# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 或安装为包
pip install -e .
```

## 5 分钟快速上手

### 1. 运行示例程序

```bash
python examples/demo.py
```

这将创建一个演示知识库，上传示例文档，并展示基本功能。

### 2. 手动使用

```python
import asyncio
from futureready import KnowledgeBase, LegalAgent

async def main():
    # 创建知识库
    kb = KnowledgeBase(base_path="./my_kb", department="legal")
    
    # 上传文档
    doc = await kb.ingest(
        file_path="contract.pdf",
        metadata={
            "uploader": "your.email@company.com",
            "department": "legal",
            "business_context": "重要客户合同，涉及知识产权条款",
            "tags": ["contract", "ip", "client_a"]
        }
    )
    
    # 创建 Agent
    agent = LegalAgent(kb)
    
    # 查询
    result = await agent.query("我们的合同中有哪些知识产权条款？")
    print(result.answer)
    
    # 主动监控
    alerts = await agent.monitor()
    for alert in alerts:
        print(f"预警: {alert.message}")

asyncio.run(main())
```

## 核心概念

### 1. 强制元数据

FutureReady-KB 的核心理念是"为未来准备"。每个文档必须包含业务上下文:

```python
metadata = {
    "uploader": "zhang.san@company.com",      # 谁上传的
    "department": "legal",                     # 哪个部门
    "business_context": "为什么上传这个文档？",  # 核心！
    "tags": ["contract", "important"]          # 标签
}
```

**为什么 business_context 是必填的？**

因为这是帮助未来 AI 理解"为什么这个文档重要"的关键。当 AI 能力足够强时，它需要知道文档的业务含义，而不只是内容。

### 2. Agent-Ready 设计

系统设计就是为 AI Agent 优化的:

```python
class MyCustomAgent(BaseAgent):
    async def query(self, question: str):
        # 1. 检索相关文档
        docs = await self.kb.search(SearchQuery(
            query=question,
            department=self.department
        ))
        
        # 2. 使用 LLM 分析
        response = await self.llm.generate(prompt)
        
        # 3. 返回结构化结果
        return AgentResponse(
            answer=response.text,
            sources=[d.id for d in docs],
            confidence=0.85
        )
```

### 3. 时间旅行查询

查询"某个时间点我们知道什么":

```python
result = await kb.search(SearchQuery(
    query="数据隐私政策",
    as_of_date=datetime(2023, 3, 1)  # 2023年3月1日时的知识
))
```

## 下一步

- 📖 阅读 [API 文档](api.md)
- 🎭 创建[自定义 Agent](agent-development.md)
- 🚀 查看[部署指南](deployment.md)
- 💡 浏览[最佳实践](best-practices.md)

## 常见问题

### Q: 为什么不直接用现有的知识库系统？

A: 现有系统是为"当下可用"设计的。FutureReady-KB 是为"未来 AI"设计的，核心区别在于:

1. **强制业务上下文** - 不只是存储，而是构建"为什么"
2. **时间维度** - 支持历史查询和知识演化追踪
3. **Agent-First** - API 设计就是为 AI 调用优化的

### Q: 现在 AI 能力还不够，用这个有意义吗？

A: 非常有意义！

1. **防止知识流失** - 即使没有 AI，也是一个很好的知识库
2. **数据积累** - 等 AI 成熟时，你已经有了 18 个月的数据优势
3. **渐进增强** - 随着 AI 能力提升，系统会自动变得更强大

### Q: 支持哪些 LLM？

A: 设计上是 LLM 无关的，可以集成:

- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- 本地模型 (Llama, Mistral)
- 任何支持文本生成的 API

### Q: 数据安全吗？

A: 完全本地部署，数据存在你的服务器上。如果需要云端 LLM，可以:

1. 使用脱敏处理
2. 选择支持本地部署的模型
3. 使用企业版 LLM API (带数据隔离保证)

## 获取帮助

- 💬 [GitHub Discussions](https://github.com/yourusername/FutureReady-KB/discussions)
- 🐛 [报告 Bug](https://github.com/yourusername/FutureReady-KB/issues)
- 📧 contact@futureready-kb.dev
