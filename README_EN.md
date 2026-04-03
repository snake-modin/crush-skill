# crush.skill

> *Do they really like me?*  

*People say a confession is meant to be a song of triumph, never the trumpet before the charge. But not everyone is blessed with the certainty of being loved. So maybe, before anything is said that cannot be taken back, the kindest thing we can give our hearts is a **rehearsal***

**Turn your crush into a conversational AI Skill for practice, reflection, and calibration.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

Feed it your observations, chat logs, photos, screenshots, and personal notes. The result is a **crush Skill** that helps you rehearse invitations, test confession wording, and sanity-check your assumptions.

This is **not** a prediction engine. It can only simulate responses from the evidence you provide, so treat it as rehearsal, not truth.

[Installation](#installation) · [Usage](#usage) · [Scenarios](#scenarios) · [中文](README.md)

---

## Installation

### Claude Code

```bash
mkdir -p .claude/skills
git clone <your-repo-url> .claude/skills/create-crush
```

### Optional dependencies

```bash
pip3 install -r requirements.txt
```

`Pillow` is only needed for photo EXIF analysis.

---

## Usage

Type this in Claude Code:

```text
/create-crush
```

Then provide:
- a codename for your crush
- your current relationship stage
- source material and personal observations

On the first `/create-crush` run, the skill should write generated crush skills as **siblings under `.claude/skills/`**, not into the current project working directory.

Generated commands:
- `/{slug}`: full conversation mode
- `/{slug}-memory`: interaction memory only
- `/{slug}-persona`: persona only

### Management commands

These helper commands are expected to be bootstrapped by `/create-crush` on first run:

| Command | Description |
|---------|-------------|
| `/list-crushes` | List all generated crush Skills |
| `/crush-rollback {slug} {version}` | Roll back to a previous version |
| `/delete-crush {slug}` | Delete |
| `/move-on {slug}` | Gentle alias for delete |

---

## Scenarios

1. Rehearse asking them out to lunch.
2. Dry-run a confession before saying it for real.
3. Practice opening messages so you stop sending awkward dead-end texts.
4. Feed in new evidence and keep refining the simulation.

---

## Architecture

Each crush Skill keeps the original two-part structure:

| Part | Purpose |
|------|---------|
| **Part A - Interaction Memory** | How you met, current stage, shared context, invitation signals, boundaries, unknowns |
| **Part B - Persona** | Speech style, emotional patterns, initiative level, likely reaction to invites/confessions |

### Supported Tags

These tags are not applied mechanically. They are translated into concrete interaction rules.

- **Attachment styles**: Secure, Anxious, Avoidant, Disorganized
- **Love languages**: Words of Affirmation, Quality Time, Receiving Gifts, Acts of Service, Physical Touch
- **Personality tags**: Talkative, Reserved, Tough-love, Silent treatment, Clingy, Independent, Romantic, Pragmatic, Perfectionist, Procrastinator, Workaholic, Controlling, Insecure, Revenge bedtime procrastination, Leaves on read, Instant replier, Three-day social feed visibility, Sends voice messages at night ...
- **Crush-specific tags**: Slow warm-up, Strong boundaries, Responds to jokes but rarely initiates, Active in group chats but restrained in private, Warm only with familiar people, Easily awkward, Good at flirty ambiguity, Dislikes pressure to define the relationship
- **Zodiac signs**: All 12 supported as soft modifiers for trait translation
- **MBTI**: All 16 supported as soft modifiers for communication style, initiative, and decision patterns

### Evolution

- **Append memory** -> add new chat logs, photos, screenshots, or observations -> analyze the delta -> merge into the right section
- **Conversation correction** -> say “they wouldn’t say that” / “they wouldn’t agree that fast” / “this doesn’t feel like them” -> write into the Correction layer -> take effect immediately
- **Version management** -> every update is archived automatically -> rollback stays available

The repository structure stays lightweight:

```text
crush-skill/
├── SKILL.md
├── prompts/
├── tools/
├── docs/PRD.md
└── requirements.txt
```

Runtime output:

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

## Safety Notes

- Use this project for rehearsal and reflection, not manipulation.
- Low-evidence areas should stay uncertain instead of turning into wish fulfillment.
- Do not treat simulated responses as permission, consent, or a reliable forecast.

---
### Endnotes

> *We were almost a sentence*  
> *the world forgot to finish*  
> *One breath more, one word less*  
> *and maybe love would have stayed*  
>
> *But the dawn kept moving*  
> *and all we held*  
> *became the shape of almost*  

MIT License © repository contributors
