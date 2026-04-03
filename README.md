# crush.skill

> *ta，真的喜欢我吗？*  

*表白是胜利的凯歌，而非冲锋的号角，但并非人人都能对彼此的关系心知肚明，我们或许可以在一切无法挽回之前进行一次**彩排***

**把你的暗恋对象整理成一个可对话的 AI Skill。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

提供你对暗恋对象的观察、聊天记录、社交媒体截图、照片和主观印象，生成一个**更贴近现实的 crush Skill**。
它可以帮你预演聊天、试探邀约、排练表白，也可以帮你识别哪些地方只是你的想象。

提示：**这不是现实预测器**。它只能基于你提供的材料做有限模拟，适合排练，不适合替代真实沟通。

[安装](#安装) · [使用](#使用) · [场景示例](#场景示例) · [English](README_EN.md)

---

## 安装

### Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/snake-modin/crush-skill.git .claude/skills/create-crush
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

Python 依赖只用于增强解析能力，例如读取照片 EXIF、批量解析聊天导出。
核心流程和这些管理命令：
- `/create-crush`
- `/list-crushes`
- `/crush-rollback`
- `/delete-crush`
- `/move-on`

都应该可以在**没有 Python**的情况下工作。

---

## 使用

在 Claude Code 中输入：

```text
/create-crush
```

然后按提示输入：
- 暗恋对象的代号
- 你们当前的关系阶段（同学、同事、朋友、几乎没说过话、暧昧中等）
- 你掌握的材料和主观印象

首次运行 `/create-crush` 时，skill 应把生成物写到 **`.claude/skills/` 的同级目录**，也就是和 `create-crush` 并列的真实 skills，而不是当前项目目录下的 `./crushes/`。

生成后可直接使用：
- `/{slug}`：完整对话模式
- `/{slug}-memory`：只看互动记忆
- `/{slug}-persona`：只看性格与说话方式

### 管理命令

下面这些命令不是仓库里天然存在的静态文件，而是由 `/create-crush` 首次运行时 bootstrap 出来的辅助 skills。这个 bootstrap 过程应直接写出对应的 `SKILL.md`，不依赖 Python：

| 命令 | 说明 |
|------|------|
| `/list-crushes` | 列出所有已生成的 crush Skill |
| `/crush-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-crush {slug}` | 删除 |
| `/move-on {slug}` | `delete` 的温柔别名 |

---

## 场景示例

**1. 约饭预演**

```text
你：周五下班一起吃饭吗？
crush.skill：这周五可能可以，不过你得先说去哪家。
```

**2. 表白排练**

```text
你：我好像有点喜欢你。
crush.skill：你突然这么认真，我有点慌……你先让我消化一下。
```

**3. 尴尬聊天止损**

```text
你：在吗
crush.skill：在，怎么了
你：没事
crush.skill：……那你刚刚叫我干嘛
```

重点不是得到你想听的答案，而是提前感受：
- ta 可能会不会接话
- 哪种表达太直球
- 哪些邀请方式更自然
- 你是不是把好感投射得过满了

---

## 核心设计

### 数据来源

| 来源 | 形式 | 用途 |
|------|------|------|
| 微信 / QQ 聊天记录 | txt / html / json / mht | 提取说话风格、回复节奏、互动线索 |
| 社交媒体截图 | 图片 / 文本导出 | 提取公开人设、兴趣偏好、常见表达 |
| 照片 | JPEG / PNG / EXIF | 提取时间线、地点、共同场景 |
| 手动描述 | 纯文本 | 补充你知道但材料里没有的信息 |

### 生成结构

每个 crush Skill 仍然保留两层结构：

| 部分 | 内容 |
|------|------|
| **Part A - Interaction Memory** | 你们怎么认识、聊过什么、见过几次、共同场景、邀约线索、边界与不确定点 |
| **Part B - Persona** | 说话风格、情绪表达、主动程度、接受邀约的条件、面对表白的可能反应 |

### 支持的标签

这些标签不会被机械套用，而是会被翻译成更具体的互动规则：

- **依恋类型**：安全型 · 焦虑型 · 回避型 · 混乱型
- **爱的语言**：肯定的言辞 · 精心的时刻 · 接受礼物 · 服务的行动 · 身体的接触
- **性格标签**：话痨 · 闷骚 · 嘴硬心软 · 冷暴力 · 粘人 · 独立 · 大男/女子主义 · 浪漫主义 · 实用主义 · 完美主义 · 拖延症 · 工作狂 · 控制欲 · 没有安全感 · 报复性熬夜 · 已读不回 · 秒回选手 · 朋友圈三天可见 · 半夜发语音 …
- **crush 场景标签**：慢热 · 边界感强 · 会接梗但不主动 · 群里活跃私聊克制 · 只对熟人热情 · 容易尴尬 · 擅长暧昧拉扯 · 不喜欢被逼表态
- **星座**：十二星座全支持，用于微调性格标签的翻译规则
- **MBTI**：16 型全支持，用于微调沟通风格、主动程度和决策模式

### 进化机制

- **追加记忆** → 找到更多聊天记录 / 照片 / 截图 / 新观察 → 自动分析增量 → merge 进对应部分
- **对话纠正** → 说“ta 不会这样说” / “ta 不会这么快答应” / “这不像 ta” → 写入 Correction 层，立即生效
- **版本管理** → 每次更新自动存档，支持回滚

### 适用场景

- 约暗恋对象吃饭前先试几版说法
- 想表白前先看哪些表达太冒进
- 想开始聊天但怕尬住，先热身
- 想补充新材料，让角色越来越像

---

## 项目结构

```text
crush-skill/
├── SKILL.md
├── prompts/
├── tools/
├── docs/PRD.md
├── README.md
├── README_EN.md
└── requirements.txt
```

运行时输出：

```text
.claude/
└── skills/
    ├── create-crush/
    ├── list-crushes/
    ├── crush-rollback/
    ├── delete-crush/
    ├── move-on/
    └── {slug}/
```

---

## 注意事项

- 这个项目用于**排练与自我校准**，不是用来操控、跟踪或替代真实沟通。
- 当材料不足时，Skill 应该保守，不要自动脑补“ta 一定也喜欢你”。
- 如果你已经明显把全部情绪压在一个人身上，这个工具不能替代现实支持系统。

---
### 尾注

> *倘若那天*  
> *把该说的话好好说，把该体谅的不执着*  
> *如果那天我不受情绪挑拨*  
> *你会怎么做*  
>
> *那么多如果，可能如果我*   
> *可惜没如果，只剩下结果*

MIT License © repository contributors
