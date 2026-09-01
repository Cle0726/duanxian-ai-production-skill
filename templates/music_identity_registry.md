# Music Identity Registry & Scene Overlay（音乐身份登记与场景叠加层）

> **用途：** 让Music Identity不只停留在Stage 03静态资产，而是稳定跨Stage 03 → 04 → 05 → 06使用，同时避免“角色今天悲伤就把核心音乐人格改掉”。

## 1｜三层模型

### A. `Character Leitmotif`｜角色核心音乐身份（稳定层）
这是角色长期身份，来自已批准Music Identity Card。

包含：
- Music Family / Style；
- Instrument / Voice（已确认时）；
- Rhythm Profile；
- Dynamics Profile；
- Timbre Metaphor；
- Phrase Shape；
- Visual Grammar；
- Base Motion Grammar；
- Forbidden Mismatch。

一旦APPROVED，不因单场戏“悲伤/愤怒/回忆”而直接改写。需要改变时走版本修订与批准。

### B. `Scene Emotion Layer`｜当前Scene情绪层（临时层）
例如：悲伤、回忆、戒备、释然、恐惧、克制、狂喜。

它只能调制Character Leitmotif：
- 速度感；
- 动作幅度；
- 停顿；
- 动态强弱；
- Stage 06配乐方向。

不能把Rock角色直接改写成“另一个角色的室内乐身份”。

### C. `Action Intensity Layer`｜动作强度层（临时层）
例如：REST / LOW / MEDIUM / HIGH / FINISHER。

它控制：
- Acceleration；
- Attack Cadence；
- Rest / Hold / Sustain；
- Syncopation / Counterpoint（适用时）；
- Recovery / Closure；
- Breath Pattern；
- FX强度；
- Stage 06音乐动态建议。

它改变强度，不改变角色核心音乐语法。

## 2｜Effective Music / Motion Profile

Stage 04/05实际执行的是：

**Character Leitmotif + Scene Emotion Layer + Action Intensity Layer → Effective Motion Grammar**

例如：
- 角色核心 = Rock；
- Scene Emotion = 悲伤；
- Action Intensity = LOW；

结果可以是“压低、受控、带强拍残留的悲伤摇滚动作语言”，而不是把角色改成另一个音乐家族。

## 3｜登记状态

每个Music Identity Card至少记录：
- Character ID；
- Music Identity Version；
- Source Status：CANON / APPROVED_DERIVED；
- Approval Status：WIP / CURRENT / APPROVED / DEPRECATED；
- Character Leitmotif字段；
- 使用中的Transformation Asset版本；
- Last Updated。

DERIVED方向只有用户批准后才能升级为`APPROVED_DERIVED`并作为长期Leitmotif使用。

## 4｜跨Stage职责

### Stage 03
使用Character Leitmotif建立Beauty Core Five与Transformation Assets。

### Stage 04
读取Character Leitmotif + 当前Scene Emotion + Action Intensity，决定镜头里的动作节奏、停顿、身体线条和表演能量；战斗Scene继续交给`Musical Combat Translation Layer`决定Footwork / Commitment / Weapon Kinetics / Tactical Timing与Impact空间。

### Stage 05
把Effective Motion Grammar翻译成可见动作；战斗时继续编译Impact/VFX因果，不把音乐术语或随机音符直接丢给模型，不自动生成对应BGM。

### Stage 06
读取：
- Character Leitmotif；
- Scene Emotion Layer；
- Action Intensity Layer；
- Music Cue Direction；
作为正式BGM选曲/制作/剪辑方向之一。

## 5｜Workspace最小记录

每个相关Scene / Segment至少保存：
- `Music Identity Ref = Character ID / Version`；
- `Scene Emotion Layer`；
- `Action Intensity Layer`；
- `Effective Motion Grammar`；
- `Musical Combat Translation Ref / Delta`（战斗适用时）；
- `Stage 06 Music Cue Direction Handoff`。

不涉及音乐身份的普通Segment可以写`N/A`，不要机械填充。
