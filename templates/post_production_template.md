# 后期成片模板


本模板用于 **Stage 06（第06阶段：后期成片）**。


## Stage 05 → Stage 06 Audio Handoff（声音职责交接）

Stage 05原则上只交接必要 Dialogue/VO、Ambience、Foley/SFX，以及剧情明确的 Diegetic/Source Music。
**正式BGM不由视频模型生成，统一在本Stage 06选择、制作、编辑与混音。**
若某个视频Take带有模型随机生成的非剧情内BGM，应优先移除/分离，不得把它默认升级为正式配乐。

### Voice Status Handoff
读取 `voice_identity_audio_status.md` 与Workspace：`TEMP_SYNC_AUDIO`必须在本Stage替换为正式声音；`FINAL_VOICE`保持角色声音身份并做清理/混音；`NO_DIALOGUE_AUDIO`按后期配音计划处理。

## Planned Editorial Assembly（导演剪辑计划交接）

Stage 06首先读取Locked `EDITORIAL_PLAN + GENERATION_ENVELOPE`。Editorial Plan拥有Viewpoint Arc、Cut Trigger、Cut Timing、Transition与Continuity Strategy；Generation Envelope记录哪些Formal Shots曾被同一次模型调用打包、实际FORMAT_MODE与CUT_CONTRACT。Approved Video Takes是真实素材Evidence；后期可以根据真实帧选择精确IN/OUT，但不得静默改变关键Reveal、POV、Reaction Give-Deny、Action-on-Cut或Sound Bridge。

```text
PLANNED EDITORIAL EDL
Edit ID｜From Shot/Take｜OUT｜To Shot/Take｜IN｜Cut Trigger｜Cut Timing｜Transition｜Continuity Strategy｜Audio Bridge｜Audience Change
```

`ONER / ASSEMBLY_FIRST`：一个Formal Shot对应一个主要Approved Clip，再按EDL切换视角。Multi-shot Envelope产物必须逐CUT检查内部切点是否与Editorial Plan及白描宫格一致；若只有部分CUT合格，允许做**Sub-cut Salvage**：保留合格CUT区间，把失败CUT拆成Single-shot Envelope重生后替换，不必废掉整条Take，也不得改写原Editorial Plan。


### Multi-shot Sub-cut Salvage Registry

```text
ENVELOPE SUB-CUT SALVAGE
Envelope ID｜Take ID｜CUT ID｜Source IN｜Source OUT｜Status CLEAN_KEEP / REPLACE / HANDLE_ONLY｜Replacement Envelope｜Continuity Condition
```

规则：
- Salvage边界以实际视频帧为证据，不以计划秒数冒充；
- `CLEAN_KEEP`必须保持对应CUT的身份、空间、动作、Camera Character、信息功能和Exit State；
- `REPLACE`只重生受影响CUT，优先保持原Storyboard Panel与Cut Contract；
- 新旧片段拼接仍受Editorial Cut Trigger / Continuity Strategy约束。

## Current｜Salvage Clip Ingest（废片可用片段导入）

进入Stage 06时先读取`video_temporal_salvage_qc.md`与当前`SALVAGE_CLIP_REGISTRY`：
- `CLEAN_KEEP`可以进入正式Edit候选；
- `CONDITIONAL_KEEP`必须满足其Audio / Cut / Continuity条件后才能使用；
- `HANDLE_ONLY`只作入出点余量或转场；
- `REJECT`不得进入正片；
- 多Take拼接前检查Identity / Axis / Action State / Lighting / Style / Audio Continuity与Director允许的Cut结构。

若采用Salvage Candidate，建立：

```text
SALVAGE ASSEMBLY EDL
Clip ID｜Source Take｜IN｜OUT｜Editorial Function｜Video Use｜Audio Use｜Transition / Condition
```

真正进入最终剪辑并经用户确认后才把对应Clip从`SALVAGE_CANDIDATE`升级为`APPROVED_SALVAGE_CLIP`。源Take继续保留，至少到最终成片锁定后。

## Episode Master（整集最终母版信息）
- 集数：
- 目标时长：15:00–18:00
- 当前粗剪时长：
- Picture Lock（画面剪辑正式锁定）时长：

## Scene Post Map（每场戏后期处理表）
| Scene（场次） | 画面节奏 | Dialogue/VO（对白/旁白） | Ambience Bed（环境底声） | Foley/SFX（拟音/音效） | BGM Cue（配乐节点） | Sound Bridge（声音桥接） | Color/VFX（调色/特效）备注 |
|---|---|---|---|---|---|---|---|
| S01 | | | | | | | |

## Ambience Bed（环境底声：整场持续存在的空间声音）
- 场景：
- 持续环境声：
- 空间/混响特征：
- 哪些Segment必须连续保持：
- 有意变化点：

## Music Identity Handoff（音乐身份交接）
如Scene涉及已有Music Identity角色，读取 `music_identity_registry.md`：
- Character Leitmotif（稳定角色音乐身份）；
- Scene Emotion Layer；
- Action Intensity Layer；
- Stage 06 Music Cue Direction Handoff。

这些作为正式BGM选择/制作的方向，不要求机械照搬某一种音乐类型；不得因为当前Scene悲伤就改写角色长期Leitmotif。

## Visual Beat Map Handoff（视觉拍点交接｜适用时）
音乐化战斗、变身、合奏、关键Hero Hit等读取 `visual_beat_music_sync_handoff.md`。优先使用**实际APPROVED Video**的Timestamp Map，不用计划时间冒充真实落点。

- Visual Beat Map ID / Version：
- Approved Take：
- Phrase Start：
- Protected Sync Points：
- Rest / Hold：
- Major Contact / Stinger：
- Cadence / Recovery：
- Music Sync Strategy：Align / Duck / Drop / Silence / Re-edit / Light Time-Stretch

`PROTECTED_SYNC_POINT`默认优先调整音乐，不为了现成BGM随意破坏已批准动作因果、Contact或Hit Stop。

## BGM Cue Map（配乐时间节点表）
- Cue ID：
- Scene / Beat：
- Cue In：
- Build：
- Duck under dialogue：
- Hit / Stinger：
- Drop / Silence：
- Transition：
- Cue Out：

## Sound Bridge（声音桥接：用声音提前或延后跨过画面切点）
- 切点：
- 类型：J-cut（下一场声音提前进来） / L-cut（上一场声音延后留下）
- 承接的声音：
- 目的：空间连续 / 情绪连续 / 提前引导 / 隐藏Segment拼接感

## Final continuity check（最终连续性质检）
- 画面曝光/色温/饱和度/清晰度：
- 对白响度：
- Ambience连续：
- BGM连续：
- Visual Beat Map / Protected Sync Point对齐：
- SFX/Foley接触点：
- 字幕与安全区：
- 最终返修来源：Stage 01 / 02 / 03 / 04 / 05 / 06


## Current｜Voice Direction / Prosody Conform

Picture Lock后读取`VOICE_DIRECTION_PLAN`，并建立`VOICE_TTS_HANDOFF`（见`voice_tts_handoff.md`）：
- 按真实剪辑重新锁Speech Phrase / Pause Duration；
- 检查Performance Loudness、Pace Curve、Stress / De-emphasis、Terminal Intonation是否符合Objective/Tactic/Subtext；
- TEMP_SYNC_AUDIO替换时继承表演意图，不继承随机临时Voice Identity；
- TTS支持SSML/prosody参数时再映射；未知平台不编造参数；
- 最终Mix Loudness与Performance Loudness分开处理。
- `validators/voice_tts_handoff_lint.py`通过后才成立`VOICE_TTS_HANDOFF_PASS`；重要台词的Voice Identity、Terminal、Pitch/Energy或Required Pause/Stress发生未授权漂移时，不得进入Master QC。
