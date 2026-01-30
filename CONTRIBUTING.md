# 贡献指南

感谢你对 FutureReady-KB 的关注！我们欢迎各种形式的贡献。

## 🎯 我们需要什么帮助

### 高优先级

1. **新的部门 Agent** 
   - HR Agent (人力资源)
   - Finance Agent (财务)
   - Marketing Agent (市场)
   - R&D Agent (研发)

2. **文档解析器**
   - PDF 深度解析 (表格、图表)
   - 扫描件 OCR
   - 特殊格式支持

3. **真实使用案例**
   - 你在公司如何使用
   - 遇到的问题和解决方案
   - 最佳实践分享

### 中优先级

4. **LLM 集成**
   - 更多 LLM Provider 实现
   - 本地模型支持
   - 提示词优化

5. **检索优化**
   - 向量数据库集成 (Qdrant/Weaviate)
   - 混合检索策略
   - 重排序算法

6. **UI/UX**
   - Web 管理界面
   - 知识图谱可视化
   - 搜索界面优化

### 低优先级

7. **文档和教程**
   - 翻译 (英文/其他语言)
   - 视频教程
   - 博客文章

8. **测试和 CI/CD**
   - 单元测试覆盖
   - 集成测试
   - GitHub Actions 配置

## 🚀 如何开始

### 1. Fork 和克隆

```bash
# Fork 这个仓库 (点击 GitHub 页面上的 Fork 按钮)

# 克隆你的 fork
git clone https://github.com/YOUR_USERNAME/FutureReady-KB.git
cd FutureReady-KB

# 添加上游仓库
git remote add upstream https://github.com/ORIGINAL_OWNER/FutureReady-KB.git
```

### 2. 创建开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试确保环境正常
pytest
```

### 3. 创建分支

```bash
# 更新主分支
git checkout main
git pull upstream main

# 创建功能分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/bug-description
```

### 4. 开发

遵循项目代码规范:

```bash
# 格式化代码
black futureready/

# 类型检查
mypy futureready/

# 运行测试
pytest tests/
```

### 5. 提交和推送

```bash
# 提交更改
git add .
git commit -m "feat: add HR agent implementation"

# 推送到你的 fork
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request

1. 访问你的 fork 页面
2. 点击 "Pull Request"
3. 填写 PR 描述 (参考下面的模板)
4. 提交 PR

## 📝 PR 模板

```markdown
## 描述
简要说明这个 PR 做了什么

## 类型
- [ ] 新功能 (feature)
- [ ] Bug 修复 (fix)
- [ ] 文档更新 (docs)
- [ ] 性能优化 (perf)
- [ ] 重构 (refactor)
- [ ] 测试 (test)

## 变更内容
- 添加了 XXX 功能
- 修复了 YYY bug
- 优化了 ZZZ 性能

## 测试
描述如何测试这些更改:
```bash
pytest tests/test_new_feature.py
```

## 截图 (如果适用)
[添加截图]

## Checklist
- [ ] 代码已格式化 (black)
- [ ] 通过类型检查 (mypy)
- [ ] 添加了测试
- [ ] 更新了文档
- [ ] 通过所有测试
```

## 💡 开发指南

### 添加新 Agent

1. 在 `futureready/agents/` 创建新文件
2. 继承 `BaseAgent` 类
3. 实现 `query()` 和 `monitor()` 方法
4. 添加到 `futureready/agents/__init__.py`
5. 创建示例程序在 `examples/`
6. 添加文档到 `docs/agents/`

示例:

```python
# futureready/agents/hr.py
from futureready.agents.base import BaseAgent
from futureready.core.models import AgentResponse

class HRAgent(BaseAgent):
    """人力资源专用 Agent"""
    
    async def query(self, question: str, context=None):
        # 实现查询逻辑
        pass
    
    async def monitor(self):
        # 实现监控逻辑
        return []
```

### 添加新的文档解析器

1. 在 `futureready/core/parsers/` 创建解析器
2. 实现 `parse()` 方法
3. 在 `KnowledgeBase._parse_document()` 中集成
4. 添加测试

### 代码规范

- 使用 Black 格式化 (line-length=88)
- 添加类型注解 (使用 mypy 检查)
- 编写文档字符串 (Google 风格)
- 保持函数简短 (<50 行)
- 优先使用异步 (async/await)

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: 添加新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式 (不影响功能)
refactor: 重构
perf: 性能优化
test: 测试
chore: 构建/工具链更新
```

示例:
```
feat(agent): add HR agent with employee handbook monitoring
fix(kb): resolve encoding issue in document ingestion
docs: update quick-start guide with LLM integration
```

## 🐛 报告 Bug

使用 [GitHub Issues](https://github.com/yourusername/FutureReady-KB/issues) 报告 bug:

**包含以下信息:**

1. 问题描述
2. 重现步骤
3. 预期行为 vs 实际行为
4. 环境信息 (Python 版本, OS 等)
5. 错误日志/截图

## 💬 讨论和提问

使用 [GitHub Discussions](https://github.com/yourusername/FutureReady-KB/discussions):

- 💡 功能建议
- 🤔 使用问题
- 📢 展示你的作品
- 💬 一般讨论

## 📜 行为准则

请遵循我们的 [行为准则](CODE_OF_CONDUCT.md):

- 尊重他人
- 包容不同观点
- 建设性反馈
- 专注于对项目最有利的事

## 🎉 贡献者

感谢所有贡献者！

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- 这里会自动生成贡献者列表 -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## 📄 License

贡献代码即表示同意代码以 [MIT License](LICENSE) 发布。

---

**还有问题？** 随时在 Discussions 中提问或发邮件到 contact@futureready-kb.dev
