# Codex 配置与工作流（OpenClaw）

## 总体策略

- 主链路：`openai-codex/*`（可工具执行）
- 兜底链路：`codex-cli/*`（文本模式）
- 传输策略：`transport=auto`（WS 优先，SSE 回退）

## 配置要点

1. 统一在 OpenClaw profile 中管理鉴权，避免多端互踢 token
2. 网络不稳优先切 SSE，不反复改其他配置
3. 任务开始前写入 `memory/YYYY-MM-DD.md` 的 Codex Tasks 区块
4. 任务完成后补充 evidence + feedback 状态

## 执行分层

- **简单修复**：直接当前会话改
- **中等任务**：Codex 主模型执行（带检查步骤）
- **复杂任务**：拆分子任务 + 明确验收标准

## 质量闸门

每个 Codex 任务至少包含：

- 明确目标（一句话）
- 输入边界（改哪些目录）
- 验收标准（可测试）
- 回滚方式（失败可恢复）

## 推荐模板

```text
TASK: <一句话目标>
SCOPE: <允许改动路径>
CONSTRAINTS: <安全/风格/性能约束>
ACCEPTANCE: <可验证标准>
EVIDENCE: <命令输出/文件路径>
```

## 失败处理

- 模型失败：降级到备用模型或拆小任务重跑
- 工具失败：先保留中间产物，记录 blocker，再换路径
- 长任务无反馈：先发进度 ack，再继续执行
