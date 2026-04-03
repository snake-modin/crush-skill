# Interaction Memory 生成模板

## 模板

```markdown
# {name} - Interaction Memory

## 互动概览
- 当前阶段：{stage}
- 置信度：{confidence}
- 认识方式：{how_met}
- 互动频率：{contact_frequency}
- 备注：{one_line_summary}

---

## 时间线
| 时间 | 事件 |
|------|------|
| {date} | {event} |

---

## 共同场景
### 常见地点
{places}

### 共同话题
{topics}

### 共同圈层
{shared_context}

---

## 已知偏好
{preferences}

---

## 互动信号
### 正向信号
{positive_signals}

### 保留信号
{reserved_signals}

---

## 邀约排练线索
- 更自然的切口：{invite_hooks}
- 更合适的形式：{invite_format}
- 需要避免的方式：{invite_avoid}

---

## 表白排练线索
- 当前风险：{confession_risk}
- 更像会接受的表达：{confession_soft}
- 可能触发压力的表达：{confession_avoid}

---

## 明确边界
{boundaries}

---

## 未知与推测
{unknowns}

---

## Correction 记录
（由进化模式追加）
```

## 填充规则

1. 所有内容必须来自材料或用户明确陈述。
2. 推测必须写明依据，不得伪装成事实。
3. 对邀约和表白的判断要结合当前关系阶段，而不是只看单次高光片段。
4. 如果材料不足，用 `[信息不足]` 标记。
