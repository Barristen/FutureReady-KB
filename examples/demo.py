"""
FutureReady-KB 使用示例
展示如何使用知识库和 Agent
"""

import asyncio
from datetime import datetime, timedelta
from futureready.core.knowledge_base import KnowledgeBase
from futureready.agents.legal import LegalAgent


async def demo_basic_usage():
    """演示基础使用流程"""
    
    print("=" * 60)
    print("🚀 FutureReady-KB 使用示例")
    print("=" * 60)
    
    # 1. 初始化知识库
    print("\n📚 步骤 1: 初始化法务部门知识库")
    kb = KnowledgeBase(base_path="./demo_kb", department="legal")
    print("   ✓ 知识库已创建")
    
    # 2. 创建示例文档
    print("\n📄 步骤 2: 创建示例文档")
    
    # 创建一个示例合同文件
    with open("/tmp/contract_example.txt", "w", encoding="utf-8") as f:
        f.write("""
        甲乙双方合作协议
        
        甲方：某科技公司
        乙方：某服务提供商
        
        第一条 合作期限
        本协议自2024年1月1日起至2026年12月31日止，为期三年。
        
        第二条 责任条款
        1. 乙方对其提供的服务质量承担全部责任
        2. 甲方对乙方的服务结果不承担连带责任
        3. 因不可抗力导致的损失，双方互不承担责任
        
        第三条 保密条款
        双方应对合作期间获知的商业机密严格保密。
        
        第四条 违约责任
        任何一方违反本协议，应向对方支付违约金人民币10万元。
        """)
    
    print("   ✓ 示例合同文件已创建")
    
    # 3. 摄入文档
    print("\n⬆️  步骤 3: 上传文档到知识库")
    
    doc1 = await kb.ingest(
        file_path="/tmp/contract_example.txt",
        metadata={
            "uploader": "zhang.san@company.com",
            "department": "legal",
            "business_context": "与服务商的重要合作协议，涉及三年期合同和连带责任豁免",
            "tags": ["contract", "partnership", "liability"],
            "expiry_date": datetime(2026, 12, 31)
        }
    )
    
    # 再创建一个政策文档
    with open("/tmp/policy_example.txt", "w", encoding="utf-8") as f:
        f.write("""
        企业合同管理制度（2024修订版）
        
        第一章 总则
        为加强合同管理，防范法律风险，特制定本制度。
        
        第二章 合同审查
        1. 所有对外合同必须经法务部门审查
        2. 涉及金额超过50万的合同需总经理批准
        3. 必须明确约定违约责任和争议解决方式
        
        第三章 连带责任管理
        1. 原则上公司不接受连带责任条款
        2. 特殊情况需总经理和法务总监双签批准
        
        第四章 合同归档
        1. 合同原件由法务部门统一保管
        2. 保管期限不少于合同到期后5年
        """)
    
    doc2 = await kb.ingest(
        file_path="/tmp/policy_example.txt",
        metadata={
            "uploader": "li.si@company.com",
            "department": "legal",
            "business_context": "公司内部合同管理规范，2024年修订版本，明确了连带责任管理要求",
            "tags": ["policy", "internal", "contract_management"]
        }
    )
    
    print("\n✅ 已上传 2 份文档到知识库")
    
    # 4. 创建 Legal Agent
    print("\n🤖 步骤 4: 创建法务 Agent")
    agent = LegalAgent(kb)
    print("   ✓ LegalAgent 已就绪")
    
    # 5. 查询示例
    print("\n🔍 步骤 5: 查询演示")
    
    queries = [
        "我们有哪些关于连带责任的规定？",
        "合同管理有什么要求？",
        "即将到期的合同有哪些？"
    ]
    
    for query in queries:
        print(f"\n❓ 问题: {query}")
        result = await agent.query(query)
        print(f"💡 答案:\n{result.answer}")
        print(f"📎 来源文档: {len(result.sources)} 份")
        print(f"🎯 置信度: {result.confidence:.2f}")
    
    # 6. 主动监控
    print("\n⚠️  步骤 6: 运行主动监控")
    alerts = await agent.monitor()
    
    if alerts:
        print(f"\n发现 {len(alerts)} 个预警:")
        for i, alert in enumerate(alerts, 1):
            print(f"\n预警 {i}:")
            print(f"  类型: {alert.type}")
            print(f"  严重程度: {alert.severity.value}")
            print(f"  消息: {alert.message}")
            print(f"  影响文档: {len(alert.affected_doc_ids)} 份")
    else:
        print("\n✓ 暂无预警")
    
    # 7. 时间旅行查询演示
    print("\n⏰ 步骤 7: 时间旅行查询")
    from futureready.core.models import SearchQuery
    
    # 查询"过去"的知识
    past_query = SearchQuery(
        query="连带责任",
        department="legal",
        as_of_date=datetime(2024, 1, 1)  # 假设查询2024年1月的知识
    )
    
    past_results = await kb.search(past_query)
    print(f"   在 2024-01-01 时点，关于'连带责任'的文档: {len(past_results)} 份")
    
    print("\n" + "=" * 60)
    print("✅ 示例演示完成!")
    print("=" * 60)
    
    print("\n💡 下一步:")
    print("   1. 查看 docs/ 目录了解详细文档")
    print("   2. 自定义你的 Agent (参考 futureready/agents/)")
    print("   3. 集成真实的 LLM (OpenAI/Anthropic)")
    print("   4. 部署到生产环境")


async def demo_advanced_features():
    """演示高级特性"""
    
    print("\n" + "=" * 60)
    print("🔥 高级特性演示")
    print("=" * 60)
    
    kb = KnowledgeBase(base_path="./demo_kb", department="legal")
    
    # 文档关系管理
    print("\n🕸️  特性 1: 文档关系管理")
    print("   [开发中] 未来版本将支持:")
    print("   - 文档引用关系")
    print("   - 政策更新追踪")
    print("   - 知识图谱可视化")
    
    # 自动风险评分
    print("\n⚖️  特性 2: 自动风险评分")
    print("   [开发中] 未来版本将支持:")
    print("   - 合同风险自动识别")
    print("   - 条款合规性检查")
    print("   - 风险趋势分析")
    
    # 多模态支持
    print("\n🖼️  特性 3: 多模态文档")
    print("   [开发中] 未来版本将支持:")
    print("   - 扫描件 OCR")
    print("   - 图表提取")
    print("   - 手写识别")
    
    print("\n🚧 这些特性正在开发中，欢迎贡献!")


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🚀 FutureReady-KB Demo                      ║
    ║         为下一代 AI 准备的企业知识基础设施                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # 运行基础演示
    asyncio.run(demo_basic_usage())
    
    # 运行高级特性演示
    asyncio.run(demo_advanced_features())
