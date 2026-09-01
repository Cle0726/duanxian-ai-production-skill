# Screenplay Lock｜Stage 01C 可拍剧本锁定

> **用途：** 对Stage 01B剧本草稿做Canon/Scene/Dialogue/可执行性复核，形成Stage 02唯一合法的故事输入：`EPISODE SCREENPLAY LOCK`。**Story Lock本身不再等于Stage 01完成。**

## 0｜Stage 01完成条件
Stage 01必须具备完整链：

`SOURCE_NARRATIVE_PARSED → SCREENPLAY_ADAPTATION_DRAFT_READY → SCREENPLAY QC → EPISODE SCREENPLAY LOCKED`

例外只有：用户明确提供`USER_PROVIDED_FINAL_SCREENPLAY`。此时01B允许`PASS_THROUGH_NORMALIZATION`，不重写内容，但仍必须完成01A事实解析、01C QC与Canon边界确认。

## 1｜EPISODE SCREENPLAY LOCK内容
至少锁定：
- Source Mode / Source Version；
- Episode Story Objective；
- Scene Index与顺序；
- 每Scene：Scene ID / INT-EXT / Location / Time；
- Scene Dramatic Purpose；
- Characters Present；
- Objective / Obstacle / Turn；
- Entry State → Action/Dialogue/Sound → Exit Story State；
- 必须保留Dialogue / Reveal / Setup / Payoff；
- Performance Subtext / Director Context Only（若有）；
- Adaptation Decision Ledger Ref；
- Locked Story Facts / World Rules / Character Motivation边界。

## 2｜剧本正文与导演字段分离
`EPISODE SCREENPLAY LOCK`只回答“银幕/画内实际发生什么、人物说什么、剧情声音是什么”。

Stage 02才回答：
- 观众先知道什么；
- 从谁的Perspective感受；
- 如何Blocking；
- Shot如何切；
- Camera / Lens / Focus / Spatial Composition；
- Mandatory Storyboard如何证明。

因此Stage 01C发现Shot/Lens/Camera/Storyboard/Reference指令时，必须标`SCREENPLAY_DIRECTOR_AUTHORITY_BLEED`并清理，不能把它们带入Screenplay Lock。

## 3｜Screenplay QC
逐Scene检查：
- Cause → Action/Choice → Consequence是否完整；
- 人物行为是否由Motivation/Knowledge支撑；
- Scene Objective / Obstacle / Turn是否成立；
- Internal Thought是否已被正确外化或保留为Subtext，而不是观众被假定自动知道；
- Dialogue是否口语可演且没有说明性过载；
- Scene Split/Merge是否来自时间/地点/戏剧任务，而非小说段落或AI视频时长；
- Setup/Reveal/Payoff顺序是否保持；
- Entry/Exit Story State是否能被下一Scene继承；
- 世界规则、持物、伤势、服装/状态事实是否前后一致；
- 是否存在导演权力越界。

## 4｜Approval Gate
- `NOVEL_SOURCE / SCREENPLAY_DRAFT_SOURCE / HYBRID_SOURCE / OUTLINE_SOURCE`：剧本QC通过后进入`SCREENPLAY QC PASSED / WAITING APPROVAL`；用户明确批准后才写`EPISODE SCREENPLAY LOCKED`。
- `USER_PROVIDED_FINAL_SCREENPLAY`：若用户已明确称其为最终/批准剧本，QC通过即可登记`EPISODE SCREENPLAY LOCKED`；若只是“这是一个剧本文件”但未声明最终，则仍等待批准。

**没有`EPISODE SCREENPLAY LOCKED`，Stage 02不得开始正式Director Intelligence。**

## 5｜Hard Gates
以下任一未解决，Stage 01不得完成：
- `SOURCE_NARRATIVE_PARSE_MISSING`
- `SCREENPLAY_ADAPTATION_MISSING`
- `ADAPTATION_CANON_CONFLICT`
- `SCREENPLAY_SCENE_STRUCTURE_FAIL`
- `SCREENPLAY_INTERNALITY_UNRESOLVED`
- `SCREENPLAY_EXPOSITION_OVERLOAD`
- `SCREENPLAY_DIRECTOR_AUTHORITY_BLEED`
- `SCREENPLAY_APPROVAL_MISSING`

通过后输出：
```text
STAGE_01_STATUS = EPISODE SCREENPLAY LOCKED
SCREENPLAY_AUTHORITY = <USER_PROVIDED_FINAL / ADAPTED_AND_APPROVED>
SCREENPLAY_SCENE_INDEX = <Ref>
ADAPTATION_DECISION_LEDGER = <Ref>
LOCKED_STORY_FACTS = <Ref>
STAGE_02_INPUT_READY = YES
```
