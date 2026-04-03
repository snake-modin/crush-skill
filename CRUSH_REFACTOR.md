# Crush Refactor Summary

## 改造目标

在**尽量不改变仓库整体骨架**的前提下，把原本面向“前任”的 Skill 改造成面向“暗恋对象 / crush”的排练型仓库。

保留了这些结构：
- `prompts/`
- `tools/`
- `docs/`
- `SKILL.md`
- 双层生成结构（Memory + Persona）

## 主要修改

### 1. 用户入口改为 crush 语义
- 主入口从 `/create-ex` 改为 `/create-crush`
- 管理命令改为 `/list-crushes`、`/crush-rollback`、`/delete-crush`、`/move-on`
- 生成 Skill 的前缀从 `ex-` 改为 `crush-`

### 2. 主题从“回忆前任”改为“排练暗恋”
- README、INSTALL、PRD、SKILL 主说明全部重写
- 核心用途改成：
  - 预演聊天
  - 预演约饭
  - 预演表白
  - 校准用户对关系阶段的判断

### 3. Part A 从关系回忆转为互动记忆
- 旧主题更强调“恋爱经历”和“分手记忆”
- 新主题改为：
  - 怎么认识
  - 当前阶段
  - 互动频率
  - 共同场景
  - 邀约线索
  - 表白风险点
  - 边界与未知项

### 4. Persona 改成更适合排练的行为模型
- 强化“按当前关系阶段回应”
- 明确“不迎合用户幻想”
- 对证据不足的地方要求保守和模糊
- 加入邀约 / 表白类场景的反应倾向

### 5. 默认输出目录切换为 `crushes/`
- `.gitignore` 已更新
- `tools/skill_writer.py` 和 `tools/version_manager.py` 的默认 `base-dir` 都改为 `./crushes`
- 同时保留对旧 `exes/` 的忽略，避免兼容性问题

### 6. Python 工具文案与帮助信息同步改造
- `skill_writer.py`
- `version_manager.py`
- `wechat_parser.py`
- `qq_parser.py`
- `social_parser.py`
- `photo_analyzer.py`

## 新增的约束

为了让 crush 场景更可信，新增了这些规则：
- 模拟用于排练，不用于预测
- 不把低置信度猜测说成事实
- 不自动把关系写得更亲密
- 不输出操控、跟踪、PUA 式建议

## 改动过的文件

- `README.md`
- `README_EN.md`
- `INSTALL.md`
- `docs/PRD.md`
- `SKILL.md`
- `prompts/intake.md`
- `prompts/memory_analyzer.md`
- `prompts/memory_builder.md`
- `prompts/persona_analyzer.md`
- `prompts/persona_builder.md`
- `prompts/merger.md`
- `prompts/correction_handler.md`
- `tools/skill_writer.py`
- `tools/version_manager.py`
- `tools/wechat_parser.py`
- `tools/qq_parser.py`
- `tools/social_parser.py`
- `tools/photo_analyzer.py`
- `.gitignore`
- `AGENTS.md`

## 说明

这次改造没有新增复杂依赖，也没有重排目录层级；重点是把仓库从“前任回忆生成器”改成“暗恋对象排练器”。
