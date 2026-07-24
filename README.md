# AI Agent 学习记录

这个仓库用于记录我学习 AI Agent 开发的过程。

我会从 Python 工程基础、HTTP 与 API、LLM 应用开始，逐步学习 Agent 架构、工具调用、记忆、RAG 和多 Agent 系统，并通过持续实践建立完整的 Agent 开发能力。

---

## 学习目标

- 掌握 Python 工程基础
- 熟悉 Git 与 GitHub 工作流
- 理解 HTTP、REST API 和 JSON
- 理解 LLM API 与上下文管理
- 独立构建 AI Agent 应用
- 学习 LangGraph 与 OpenAI Agents SDK
- 学习 RAG、MCP 和多 Agent 系统
- 完成两个可部署、可测试、可讲解的 Agent 项目
- 从 2026 年 8 月底开始投递杭州的 AI 应用开发相关实习岗位

---

## 当前进度

### 第 1 周：基础能力（已完成）

- ✅ 配置开发环境
- ✅ 使用 `uv` 管理 Python 项目
- ✅ 学习 Git 工作流与版本控制基础
- ✅ 学习 HTTP 请求与 JSON 数据处理
- ✅ 调用 DeepSeek API
- ✅ 实现带对话上下文的命令行 Chatbot
- ✅ 使用 `Agent` 类封装 LLM 调用
- ✅ 理解并实现基于 `messages` 的短期记忆
- ✅ 学习 Agent Loop 与 Tool Calling

### 第 2 周：多工具 Agent 工程化（进行中）

- ✅ 将工具拆分为独立模块
- ✅ 实现动态工具注册表
- ✅ 实现多工具和连续工具调用
- ✅ 增加决策轮次与工具调用次数保护
- ✅ 实现 Schema 与注册表一致性检查
- ✅ 使用 Pydantic 验证工具参数与返回值
- ✅ 将成功和失败结果结构化
- ✅ 根据函数注解和 Docstring 自动生成 Tool Schema
- ✅ 拆分工具执行器并增加自动化测试

---

## 学习路线概览

- [x] Python 基础复习
- [x] Git 基础
- [x] HTTP 与 API 基础
- [x] LLM API 基础
- [x] 基础 Chat Agent 与短期记忆
- [x] Tool Calling
- [x] Agent Loop
- [x] 多工具注册与参数验证
- [x] Tool Schema 自动生成
- [ ] 工具执行器与自动化测试
- [ ] LangGraph
- [ ] RAG
- [ ] MCP
- [ ] 电商售后客服 Agent
- [ ] AgentTrace 追踪与自动评测平台

详细路线请查看 [ROADMAP.md](ROADMAP.md)，暑假倒排计划请查看 [SUMMER_PLAN.md](SUMMER_PLAN.md)。

---

## 项目结构

```text
agent-learning/
├── week01/
│   ├── day01/
│   ├── day02/
│   ├── day03/
│   ├── day04/
│   └── day05/
├── week02/
│   ├── day01/
│   ├── day02/
│   ├── day03/
│   ├── day04/
│   └── day05/
├── notes/
│   ├── week01/
│   └── week02/
├── README.md
├── ROADMAP.md
├── SUMMER_PLAN.md
├── pyproject.toml
└── uv.lock
```

---

## 已完成的实践

### 第 1 周

#### 命令行 AI Chatbot

- 使用 Python 与 `requests`
- 调用 DeepSeek API
- 解析 API 返回的 JSON 数据
- 保存并传递对话上下文

#### 基础 Agent

- 使用 `Agent` 类封装调用流程
- 使用 `messages` 保存用户和助手消息
- 实现连续对话与短期记忆
- 增加基本的请求异常处理

### 第 2 周

#### 多工具 Agent

- 使用注册表动态选择并执行工具
- 支持一次任务中的连续工具调用
- 使用最大决策轮次和工具调用次数限制防止死循环
- 使用 Pydantic 严格验证工具参数和返回值
- 将工具错误作为结构化消息交回 LLM

#### Tool Schema 自动生成

- 从函数名生成工具名称
- 从 Docstring 生成工具描述
- 从类型注解生成参数 JSON Schema
- 从 `Literal` 生成 `enum`
- 从默认值判断 `required`
- 从注册表批量生成 LLM 可用的 `TOOLS`

---

## 学习笔记

每日学习笔记保存在：

```text
notes/
```

笔记主要记录概念理解、代码实践、调试过程和学习反思，方便后续复习。
