# PB03 定时与心跳闭环剧本

## Goal
保证“定时产出 -> 状态回写 -> 心跳监督 -> 异常补偿”全链路闭环。

## Trigger
有多个 cron 任务并行，且需要避免漏发/重复发。

## Steps
1. 统一定义每个 cron 的 output_path 和 status_key。
2. cron 成功后回写 `heartbeat-state.json`（时间、版本、发送状态）。
3. heartbeat 每轮巡检状态并执行补偿逻辑。
4. 每日汇总一次闭环率与异常原因。

## Metrics
- 主指标：任务闭环率 >= 95%
- 护栏：重复通知率 < 10%

## Failure Modes
- cron 执行成功但消息未发送
- heartbeat 只回复 OK，未发现待补偿项

## Rollback
临时关闭自动补偿，仅保留告警并人工确认。
