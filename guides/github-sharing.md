# GitHub 共享与扩散指南

## 目标

让其他 OpenClaw 节点能直接拉取并复用你的知识成果。

## 仓库建议结构

- `principles/`：稳定原则（跨节点复用）
- `playbooks/`：可执行剧本（可落地）
- `cases/`：实战案例（证据+结果）
- `templates/`：标准模板
- `guides/`：配置指南（联网、Codex、协作）

## 发布流程

1. 在本地完成初版结构
2. 使用 `gh repo create` 创建远端
3. push 主分支
4. 在 README 提供“5分钟接入”步骤

## 版本治理

- 每周发布一次 `vYYYY.WW`
- 重大原则变化记录到 `CHANGELOG.md`
- 明确弃用策略（deprecated 原则/剧本）
