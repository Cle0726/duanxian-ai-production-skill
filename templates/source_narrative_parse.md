# Source Narrative Parse｜Stage 01A 原著/源文本解析

> **用途：** Stage 01A只回答“源文本实际写了什么”。先把小说、剧本、提纲或混合输入拆成可追踪的Canon事实与叙事材料，再允许进入影视改编。**本阶段不导演、不拆Shot、不做Storyboard、不规划资产。**

## 0｜Source Mode
先登记唯一Source Mode：
- `NOVEL_SOURCE`：小说/文学叙事为主；
- `USER_PROVIDED_FINAL_SCREENPLAY`：用户明确提供并指定为当前最终剧本；
- `SCREENPLAY_DRAFT_SOURCE`：已有剧本草稿，但仍允许结构/对白改编；
- `HYBRID_SOURCE`：小说 + 旧剧本/提纲/补充Canon并存；
- `OUTLINE_SOURCE`：只有梗概/分集提纲，需要在不越过Canon边界的前提下形成剧本。

不同Source不得悄悄互相覆盖。出现冲突时记录`SOURCE_AUTHORITY_CONFLICT`并按当前Canon Authority裁决；无法安全裁决的P0冲突才询问用户。

## 1｜SOURCE NARRATIVE FACT MAP
至少提取：
- Episode / Chapter / Source Range；
- 时间、地点与明确时空切换；
- 出场人物与当前关系；
- 核心事件及其先后；
- Cause → Choice/Action → Consequence因果链；
- 人物Objective / Motivation / Knowledge / Misbelief（源文本能证明时）；
- 世界规则、状态变化、关键道具/持有关系；
- Setup / Foreshadowing / Reveal / Payoff；
- 必须保留的原文对白或关键信息；
- `VISIBLE_ACTION`：已经可直接表演/可见的行为；
- `DIALOGUE`：人物实际说出的内容；
- `INTERNAL_THOUGHT`：心理、回忆、判断、意识流；
- `NARRATION`：叙述者说明；
- `DESCRIPTIVE_PROSE`：气氛、外貌、环境、文学修辞；
- `SOUND_EVENT`：剧情真实存在的声音/声音缺失；
- `SOURCE_AMBIGUITY`：文本自身含糊、互相矛盾或缺失的事实。

## 2｜Scene Candidate不是正式Scene Lock
Stage 01A可以标记`SCENE_BOUNDARY_CANDIDATE`，依据：
- 明确地点变化；
- 明确时间跳变；
- 连续戏剧行动中断；
- 新的因果单元开始。

但不要因为小说换段、换句或换视角就机械切Scene。正式Scene Split / Merge由Stage 01B裁决。

## 3｜禁止的提前导演化
Stage 01A不得产生：
- Shot / 景别 / Lens / Camera Move / Focus；
- 4格/6格/9格或任何Storyboard Panel；
- FG/MG/BG构图；
- Reference Pack / Asset Requirement / Platform能力；
- “这里用特写更好”“这里慢推”等导演建议。

若解析结果混入上述内容，标`SOURCE_PARSE_DIRECTOR_BLEED`并清除后重做。

## 4｜Stage 01A输出
```text
SOURCE_NARRATIVE_PARSE
Source Mode:
Source Range:
Canon Facts:
Causal Chain:
Character Intent/Knowledge:
World/State Rules:
Setup-Reveal-Payoff:
Must-Preserve Dialogue/Information:
Visible Action:
Dialogue:
Internal Thought:
Narration:
Descriptive Prose:
Sound Events:
Scene Boundary Candidates:
Source Ambiguities:
```

## 5｜Hard Gate
以下任一未解决，不得进入Stage 01B：
- `SOURCE_AUTHORITY_CONFLICT`
- `SOURCE_CANON_AMBIGUITY_P0`
- `SOURCE_CAUSAL_CHAIN_GAP`
- `SOURCE_PARSE_DIRECTOR_BLEED`

通过后记录：`SOURCE_NARRATIVE_PARSED = PASS`。
