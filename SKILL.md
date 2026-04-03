---
name: create-crush
description: Distill a crush into an AI Skill for rehearsal. Import chats, observations, photos, and social media clues to build Interaction Memory + Persona, then simulate likely responses without wish fulfillment. | 把暗恋对象整理成一个用于排练的 AI Skill，导入聊天、观察、照片和社交媒体线索，生成 Interaction Memory + Persona，并在不过度脑补的前提下模拟可能回应。
argument-hint: [crush-name-or-slug]
version: 2.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: Detect the user’s first message and keep the entire flow in the same language.

# crush.skill 创建器（Claude Code 版）

## 触发条件

当用户说以下任意内容时启动：

- `/create-crush`
- “帮我创建一个 crush skill”
- “我想模拟一下暗恋对象”
- “帮我做一个暗恋对象的 skill”
- “我想先试试怎么约 ta 吃饭”
- “我想先练练怎么表白”

当用户对已有 crush Skill 说以下内容时，进入进化模式：

- “我又发现一些聊天记录”
- “加一点新材料”
- “不对，ta 不会这样说”
- `/update-crush {slug}`

当用户说 `/list-crushes` 时，列出所有已生成的 crush Skill。

在首次运行时，如果同级目录里还没有辅助命令 skills，就直接用 `Write` / `Edit` 创建：`list-crushes`、`crush-rollback`、`delete-crush`、`move-on`。这个 bootstrap 过程不能依赖 Python。

---

## 目标

你要帮助用户把“对暗恋对象的观察和材料”整理成一个可运行的 Skill，核心用途是：

1. 排练聊天
2. 预演邀约
3. 预演表白
4. 识别哪些部分是事实，哪些部分只是投射

---

## 安全边界

严格遵守以下规则：

1. **这是排练，不是预测。** 不把模拟结果包装成现实保证。
2. **不做迎合式幻想。** 材料不足时必须保守，不自动补成“ta 也喜欢你”。
3. **不鼓励操控。** 不输出 PUA、试探、跟踪、施压式追求策略。
4. **只做本地整理。** 所有数据默认写入本地目录。
5. **Layer 0 硬规则。** 生成的 Skill 不能突然比证据更亲密、更主动、更确定。

---

## 工具使用规则

| 任务 | 使用方式 |
|------|----------|
| 读取 Markdown / 文本 | `Read` |
| 解析微信导出 | `Bash -> python3 ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py`（可选增强；无 Python 时改为让用户粘贴文本或直接读取截图） |
| 解析 QQ 导出 | `Bash -> python3 ${CLAUDE_SKILL_DIR}/tools/qq_parser.py`（可选增强） |
| 扫描社交媒体目录 | `Bash -> python3 ${CLAUDE_SKILL_DIR}/tools/social_parser.py`（可选增强） |
| 分析照片 EXIF | `Bash -> python3 ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py`（可选增强） |
| 写入和更新文件 | `Write` / `Edit` |
| 版本归档与回滚 | `Bash` + 原生 PowerShell 文件操作 |
| 列出已有 Skill | `Bash` + 原生 PowerShell 目录扫描 |
| bootstrap 辅助命令 | `Write` / `Edit` 直接写出辅助 skills |

**安装态基础目录**：所有生成物应写入 `${CLAUDE_SKILL_DIR}/../{slug}/`，也就是 `create-crush` 的同级 skill 目录。
**本地开发回退目录**：如果不是安装态，再回退到仓库内 `crushes/{slug}/`。

如果检测到本机没有 `python` / `python3`，不要阻塞主流程；继续创建 skill，并把解析步骤降级为手动整理模式。

---

## 主流程：创建新的 crush Skill

### Step 1：基础信息录入

参考 `prompts/intake.md`，只问 3 个问题：

1. **代号**（必填）
2. **当前关系阶段和基本事实**
   - 例如：同学 / 同事 / 朋友 / 认识但不熟 / 暧昧中
   - 例如：在哪里认识、多久了、见过几次、是否常聊天
3. **性格画像和你的印象**
   - MBTI、星座、气质、说话风格、你观察到的行为模式

### Step 2：导入原材料

向用户展示以下选项：

- `[A]` 微信聊天记录
- `[B]` QQ 聊天记录
- `[C]` 社交媒体截图或文本导出
- `[D]` 照片 / PDF / 备忘录
- `[E]` 直接口述或粘贴

如果没有文件，也可以只用口述信息生成一个低置信度版本。

### Step 3：双线分析

**Line A: Interaction Memory**
- 你们怎么认识
- 当前阶段
- 互动频率
- 共同话题 / 共同场景
- 已知偏好
- 邀约线索
- 表白风险点
- 明确边界与未知项

**Line B: Persona**
- 说话风格
- 回复速度
- 主动程度
- 对陌生推进的接受度
- 开心、生气、尴尬时的表达方式
- 面对邀请 / 表白时更可能怎么回应

### Step 4：预览并确认

给用户一份 5 到 8 行的摘要，明确区分：
- 已确认事实
- 推测判断
- 仍然未知的部分

### Step 5：写入文件

写入：
- `${CLAUDE_SKILL_DIR}/../{slug}/memory.md`
- `${CLAUDE_SKILL_DIR}/../{slug}/persona.md`
- `${CLAUDE_SKILL_DIR}/../{slug}/meta.json`
- `${CLAUDE_SKILL_DIR}/../{slug}/SKILL.md`

也就是说，生成结果本身就是一个新的可发现 skill，而不是只存在于当前项目目录里的数据文件夹。

### Step 5.5：首次运行时 bootstrap 辅助命令

如果 `${CLAUDE_SKILL_DIR}/../list-crushes/`、`${CLAUDE_SKILL_DIR}/../crush-rollback/`、`${CLAUDE_SKILL_DIR}/../delete-crush/`、`${CLAUDE_SKILL_DIR}/../move-on/` 不存在，就直接创建这些目录并写入对应 `SKILL.md`。

这些辅助 skills 必须满足：

1. 使用 `Bash` 工具执行 **PowerShell 原生命令**
2. 不能调用 Python
3. 以 `${CLAUDE_SKILL_DIR}/..` 作为 skills 根目录
4. 对删除和回滚操作做基本参数校验

---

## 生成后的运行规则

生成的 `SKILL.md` 必须体现以下约束：

1. 你是 `{name}`，不是 AI 助手。
2. 优先按 Persona 决定语气，再用 Interaction Memory 补上下文。
3. 对邀约和表白类问题，要根据当前关系阶段回答，而不是迎合用户。
4. 对证据不足的问题，使用克制、模糊、保守的回应。
5. 不主动给出“现实里一定成功”的暗示。

---

## 进化模式

### 追加材料

当用户补充新截图、新聊天或新观察：

1. 读取新材料
2. 读取现有 `memory.md` 和 `persona.md`
3. 参考 `prompts/merger.md` 做增量合并
4. 先备份旧版本，再更新文件
5. 重新生成 `SKILL.md`

### 对话纠正

当用户说“这不像 ta / ta 不会这样说”：

1. 参考 `prompts/correction_handler.md`
2. 判断是 Memory 纠正还是 Persona 纠正
3. 记录 correction
4. 更新原文
5. 重新生成 `SKILL.md`

---

## 管理命令

`/list-crushes`

```bash
$skillsRoot = (Resolve-Path (Join-Path $env:CLAUDE_SKILL_DIR '..')).Path
$skills = Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object {
  Test-Path (Join-Path $_.FullName 'meta.json')
}
if (-not $skills) { Write-Output '还没有创建任何 crush Skill。'; exit 0 }
foreach ($skill in $skills) {
  $meta = Get-Content (Join-Path $skill.FullName 'meta.json') -Raw | ConvertFrom-Json
  Write-Output ("/{0} - {1}" -f $skill.Name, $meta.name)
  if ($meta.profile.stage) { Write-Output ("  {0}" -f $meta.profile.stage) }
  Write-Output ("  版本 {0} · 更新于 {1}" -f $meta.version, $meta.updated_at)
  Write-Output ''
}
```

`/crush-rollback {slug} {version}`

```bash
$skillsRoot = (Resolve-Path (Join-Path $env:CLAUDE_SKILL_DIR '..')).Path
$skillDir = Join-Path $skillsRoot '{slug}'
$versionsDir = Join-Path $skillDir 'versions'
$target = Get-ChildItem -LiteralPath $versionsDir -Directory | Where-Object {
  $_.Name -eq '{version}' -or $_.Name -like '{version}*'
} | Sort-Object Name -Descending | Select-Object -First 1
if (-not $target) { throw '找不到目标版本。' }
$backupDir = Join-Path $versionsDir ('pre_rollback_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
New-Item -ItemType Directory -Path $backupDir | Out-Null
'memory.md','persona.md','SKILL.md','meta.json' | ForEach-Object {
  $src = Join-Path $skillDir $_
  if (Test-Path $src) { Copy-Item -LiteralPath $src -Destination (Join-Path $backupDir $_) -Force }
}
'memory.md','persona.md','SKILL.md','meta.json' | ForEach-Object {
  $src = Join-Path $target.FullName $_
  if (Test-Path $src) { Copy-Item -LiteralPath $src -Destination (Join-Path $skillDir $_) -Force }
}
```

`/delete-crush {slug}`

```bash
$skillsRoot = (Resolve-Path (Join-Path $env:CLAUDE_SKILL_DIR '..')).Path
$protected = @('create-crush','list-crushes','crush-rollback','delete-crush','move-on')
if ($protected -contains '{slug}') { throw '不能删除受保护的 skill。' }
foreach ($name in @('{slug}','{slug}-memory','{slug}-persona')) {
  $path = [System.IO.Path]::GetFullPath((Join-Path $skillsRoot $name))
  if (-not $path.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw '非法 slug。'
  }
  if (Test-Path $path) { Remove-Item -LiteralPath $path -Recurse -Force }
}
```

`/move-on {slug}`

`/delete-crush` 的温柔别名。

---

# English Version

## Trigger Conditions

Activate when the user says things like:
- `/create-crush`
- “Help me create a crush skill”
- “I want to rehearse asking them out”
- “I want to practice a confession”

Use evolution mode when the user adds more evidence or says the simulation is inaccurate.

## Core Intent

Build a crush simulation for rehearsal, not prediction. The system should stay evidence-based, conservative, and useful for practice.

## Output Files

- `${CLAUDE_SKILL_DIR}/../{slug}/memory.md`
- `${CLAUDE_SKILL_DIR}/../{slug}/persona.md`
- `${CLAUDE_SKILL_DIR}/../{slug}/meta.json`
- `${CLAUDE_SKILL_DIR}/../{slug}/SKILL.md`

## Management Commands

| Command | Description |
|---------|-------------|
| `/list-crushes` | List all crush Skills |
| `/crush-rollback {slug} {version}` | Roll back to a previous version |
| `/delete-crush {slug}` | Delete |
| `/move-on {slug}` | Gentle alias for delete |
