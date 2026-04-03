# 安装说明

## Claude Code 安装

### 项目级安装

在你的 Git 仓库根目录执行：

```bash
mkdir -p .claude/skills
git clone <your-repo-url> .claude/skills/create-crush
```

### 全局安装

```bash
git clone <your-repo-url> ~/.claude/skills/create-crush
```

### OpenClaw 安装

```bash
git clone <your-repo-url> ~/.openclaw/workspace/skills/create-crush
```

---

## 依赖安装

```bash
cd .claude/skills/create-crush
pip3 install -r requirements.txt
```

当前唯一可选依赖是 `Pillow`，用于分析照片的 EXIF 信息。

---

## 推荐输入材料

你不需要已经和对方谈过恋爱。这个仓库面向的是**暗恋对象 / 好感对象 / 想进一步了解的人**，推荐材料包括：

- 你们已有的微信、QQ、短信聊天记录
- ta 的朋友圈、微博、小红书、Instagram 截图
- 你们共同出现过的照片
- 你对 ta 的观察笔记
- 你们见面的场景、共同朋友、共同话题

如果没有导出文件，也可以直接把你记得的内容复制进来。

---

## 微信聊天记录导出

推荐外部工具：

- **WeChatMsg**: txt / html / csv
- **PyWxDump**: sqlite
- **留痕**: json

手动方式：
1. 打开与暗恋对象的聊天窗口
2. 复制关键对话
3. 粘贴到 `.txt` 文件
4. 在 `/create-crush` 流程中上传或直接贴出

---

## QQ 聊天记录导出

1. 打开 QQ 设置
2. 进入聊天记录导出
3. 导出为 `txt` 或 `mht`
4. 在 `/create-crush` 中上传

---

## 常见问题

### Q: 这个 Skill 能预测 ta 真实会怎么回应吗？
A: 不能。它只能基于你提供的材料做保守模拟，适合排练，不适合替代现实判断。

### Q: 可以同时创建多个 crush Skill 吗？
A: 可以。安装态下，每个对象会生成独立的 `.claude/skills/{slug}/` 目录；只有在本地直接运行脚本开发时，才会退回到仓库内的 `crushes/` 目录。

### Q: 没有聊天记录还能用吗？
A: 可以，但结果会更依赖你的主观描述。材料越少，模拟越保守。

### Q: `/list-crushes` 这些命令为什么一开始不能用？
A: 它们不是仓库自带的顶层静态 skills，而是应由 `/create-crush` 首次运行时 bootstrap 出来的辅助 skills。若尚未生成，可先运行一次 `/create-crush`，或手动执行：

```bash
python tools/skill_writer.py --action bootstrap --source-skill-dir <create-crush路径>
```

### Q: 如何删除一个 crush Skill？
A: 使用 `/delete-crush {slug}` 或 `/move-on {slug}`。如果辅助命令尚未 bootstrap，也可以直接让 `/create-crush` 帮你删除。
