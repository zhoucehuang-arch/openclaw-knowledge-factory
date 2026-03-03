# Cron + Heartbeat Orchestration

## 目标

把定时任务（cron）和会话轮询（heartbeat）变成协同系统，而不是重复触发器。

## 分工

- Cron：精确定时、独立执行、固定输出（如 AM/PM 简报）
- Heartbeat：状态巡检、异常发现、闭环提醒

## 联动协议

1. cron 产出后写入统一状态文件（`memory/heartbeat-state.json`）
2. heartbeat 读取状态：
   - 若新产出未发送 -> 触达提醒
   - 若任务 running/pending 超阈值 -> 告警
   - 若系统稳定且无新事项 -> HEARTBEAT_OK
3. heartbeat 不重复生成已有 cron 报告，只做监督和补偿

## 反重复策略

- 同主题任务设置 cooldown（建议 2-4h）
- heartbeat 遇到最近 30 分钟已检查任务不重复检查
- cron 报告先做 24h dedup 再发布

## 故障降级

- 搜索源失效：SearXNG -> agent-reach -> web_fetch
- 模型失效：主模型 -> 备用模型 -> 最小报告模式
- 通知失败：重试 1 次，仍失败则记录并在 heartbeat 报警

## 关键 SLO

- 定时任务准点率 >= 95%
- 漏发率 < 2%
- 重复提醒率 < 10%
