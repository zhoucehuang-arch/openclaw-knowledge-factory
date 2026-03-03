# OpenClaw 联网技能配置指南

## 目标

让不同 OpenClaw 节点稳定联网搜索，并统一证据质量与回退策略。

## 推荐技能栈（按优先级）

1. `searxng`（主搜索，隐私友好，可自建）
2. `agent-reach`（跨平台内容读取：X/Reddit/YouTube/GitHub 等）
3. `web_fetch`（轻量网页正文抓取）
4. `web_search`（Brave API，作为补充而非唯一依赖）

## 统一配置原则

- 主链路固定为：`searxng -> agent-reach -> web_fetch`
- `web_search` 缺 key 时自动降级，不阻断任务
- 每条关键结论至少 1 个可访问链接
- 每轮报告覆盖 >= 6 个独立域名，避免单源偏差

## SearXNG 配置检查

- 服务可用
- 时区和语言符合使用场景
- 引擎集合包含：general + github + news + reddit（按需）

## Agent Reach 配置建议

- 优先启用：X、Reddit、YouTube、GitHub
- 遇到网页 403 时，自动换源到同主题可访问来源
- 对关键账号（如 `@heynavtoor`）建立固定追踪查询模板

## 证据标准

每条知识卡至少包含：

- 结论一句话
- 原始来源链接
- 适用边界
- 可执行动作

## 常见问题

- **403/反爬**：切换同主题来源，不做硬重试死循环
- **API key 缺失**：降级到 SearXNG + Agent Reach
- **结果重复**：启用 24h 去重清单（links + topics）
