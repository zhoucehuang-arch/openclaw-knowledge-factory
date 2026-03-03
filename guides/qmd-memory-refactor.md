# QMD Memory Refactor Guide

## 目标

把高频情报从“堆日志”升级为“可检索、可升级、可执行”的长期记忆系统。

## 分层模型

- L0 Raw: 原始抓取与报告（只归档，不直接决策）
- L1 Facts: 去重后的事实条目（带来源）
- L2 Principles: 跨多条事实提炼出的稳定规律
- L3 Actions: 可执行动作与实验记录

## 建议目录

- `memory/raw/`
- `memory/facts/`
- `memory/principles/`
- `memory/actions/`
- `memory/index.json`

## 重构规则

1. 每条事实必须包含 source_url + timestamp + topic
2. 同主题 24h 内去重（link + semantic topic）
3. 只有通过验证的事实才能提升为 principle
4. principle 必须绑定至少一个 action
5. action 必须回写 outcome（win/neutral/fail）

## QMD 查询策略

- 检索前先查近 24h 主题索引，避免重复搜索
- 检索后先写 facts，再决定是否升级为 principles
- 每次输出时优先引用 principles，不重复复述 raw

## 健康检查指标

- 重复率（目标 < 20%）
- 无来源条目占比（目标 = 0）
- principle->action 转化率（目标 > 60%）
- action 闭环率（目标 > 70%）
