# Video Temporal Salvage QC（视频时间片段抢救质检）｜Current Authority

> **用途：** 当一个Video Take整体不能PASS时，不再默认把整条视频视为废片。QC必须额外判断其中是否存在能够保留、剪辑、替换音频后使用、或仅作为剪辑Handle使用的真实时间段，并把这些时间段登记为可追溯素材。
>
> **核心原则：Whole-Take Failure ≠ Whole-Take Waste。** 但“画面有几秒不错”也不等于可直接进成片；每个可保留片段必须同时通过视觉有效性、时间完整性、叙事用途、剪点可用性、连续性兼容与导演Invariant检查。

---

## 1｜触发条件

以下任一成立时必须执行Temporal Salvage QC：
- `Verdict = REVISE`；
- `Verdict = OPTIONAL_SAME_PROMPT_RETRY`；
- `Recommended Action = POST_FIX_ONLY / MINIMUM_PROMPT_REVISION`且存在局部时间问题；
- PASS Take存在明确Trim区、可删尾部或需要保留剪辑Handle；
- 用户明确询问“废片里有没有能用的片段”。

`INSUFFICIENT_EVIDENCE`时不得猜时间窗；只能输出`TEMPORAL_SALVAGE_STATUS = INSUFFICIENT_EVIDENCE`并说明缺失证据。

---

## 2｜Whole-Take Verdict与Temporal Salvage必须分离

原Video QC Verdict继续使用：
- `PASS`
- `REVISE`
- `OPTIONAL_SAME_PROMPT_RETRY`
- `INSUFFICIENT_EVIDENCE`

另外独立增加：

`TEMPORAL_SALVAGE_STATUS = FULL_TAKE_USABLE / SALVAGE_AVAILABLE / NO_SALVAGE / INSUFFICIENT_EVIDENCE`

禁止因为存在Salvage Window就把整体REVISE Take改判PASS。

---

## 3｜Salvage Window四种状态

每个时间段只能标为以下之一：

### `CLEAN_KEEP`
可以直接进入剪辑候选：
- 本时间段无P0/P1视觉硬伤；
- 起点与终点都是合法剪点；
- 片段内部动作/表演/Camera是完整的；
- 不依赖被拒绝区间才能理解；
- 不改变Director Invariants。

### `CONDITIONAL_KEEP`
画面或声音有真实用途，但必须满足明确条件，例如：
- 画面可用但原音频需替换；
- 只能从独立CUT进入/离开；
- 只能作为Insert / Reaction / Establishing；
- 需要J-cut / L-cut / Cover Cut掩盖边界；
- 需要与另一Take的已批准片段匹配后才可用。

没有明确使用条件不得标Conditional。

### `HANDLE_ONLY`
不能承担独立叙事Beat，但可保留为剪辑余量，例如：
- 入点前稳定0.3–1s；
- 出点后短暂稳定余韵；
- 转场、遮挡、镜头落稳、环境空镜尾部。

Skill不设置固定最短秒数；是否有价值由真实剪辑功能决定。

### `REJECT`
存在硬错误、动作中断、错误身份/道具/空间、严重Reference泄漏、无法合法剪出、或继续使用会破坏Director/Continuity。

---

## 4｜每个Window必须检查六项

### 4.1 Visual Validity
检查身份、环境、道具、动作、解剖、综合色、画风、Reference污染、VFX与Camera本身是否可用。

### 4.2 Temporal Integrity
片段内部必须有可理解的开始与结束；不得从半个接触、半个转身、半个音节、穿模发生中间或Camera whip最坏位置硬切。

### 4.3 Narrative / Editorial Utility
必须说明它实际能承担什么：
`ESTABLISHING / PERFORMANCE_BEAT / ACTION_BEAT / REACTION / INSERT / TRANSITION / ATMOSPHERE / HANDLE / AUDIO_ONLY / OTHER`

“画面挺好看”不是合法用途。

### 4.4 Entry / Exit Cutability
分别判断：
- `ENTRY_CUT = CLEAN / CONDITIONAL / NOT_CUTTABLE`
- `EXIT_CUT = CLEAN / CONDITIONAL / NOT_CUTTABLE`

并写清条件。

### 4.5 Continuity Compatibility
检查人物位置、朝向、动作阶段、道具状态、视线、轴线、光色、环境状态与前后镜是否可接。

### 4.6 Director Invariant Compatibility
Salvage不能为了省Video成本破坏：
- Audience Alignment；
- Reveal / Withhold顺序；
- Reaction Give-Deny；
- 核心Blocking / Distance；
- Key Hold / Cut；
- Opening / Closing Function；
- 明确要求不中断的长镜头。

若原计划是不可切开的Long Take，前后好片段即使视觉正确，也不得自动拼接成新CUT。可登记为`HANDLE_ONLY / CONDITIONAL_KEEP`或留存备用，但是否使用必须返回Director/Editor判断。

---

## 5｜Audio与Video必须分开判

每个Salvage Window同时记录：

`VIDEO_USE = KEEP / CONDITIONAL / REJECT`

`AUDIO_USE = KEEP / REPLACE / AUDIO_ONLY / REJECT`

典型合法组合：
- `VIDEO KEEP + AUDIO KEEP`
- `VIDEO KEEP + AUDIO REPLACE`
- `VIDEO REJECT + AUDIO_ONLY`
- `VIDEO CONDITIONAL + AUDIO REPLACE`

**Audio-only保留规则：** 若画面本身必须Reject，但实际对白/环境声/拟音仍有明确剪辑价值，Window不得标成彻底`REJECT`；应标`CONDITIONAL_KEEP` + `EDITORIAL_FUNCTION = AUDIO_ONLY` + `VIDEO_USE = REJECT` + `AUDIO_USE = AUDIO_ONLY`。`REJECT`保留给“该时间窗没有任何可复用Video或Audio价值”的情况。

禁止因为画面可用就默认原声音也可用；也禁止因为画面坏掉就丢弃可用对白/环境声。

---

## 6｜Temporal Salvage Map标准格式

```text
TEMPORAL_SALVAGE_MAP
Source Take: <TAKE_ID>
Source Duration: <actual duration>
Take Verdict: <PASS / REVISE / OPTIONAL_SAME_PROMPT_RETRY / INSUFFICIENT_EVIDENCE>
Temporal Salvage Status: <FULL_TAKE_USABLE / SALVAGE_AVAILABLE / NO_SALVAGE / INSUFFICIENT_EVIDENCE>

WINDOW 01
IN: 00:00.00
OUT: 00:03.86
STATUS: CLEAN_KEEP
EDITORIAL_FUNCTION: ESTABLISHING
VIDEO_USE: KEEP
AUDIO_USE: KEEP
ENTRY_CUT: CLEAN
EXIT_CUT: CLEAN
CONTINUITY: COMPATIBLE
DIRECTOR_INVARIANTS: PRESERVED
CONDITIONS: NONE
WHY_KEEP: <可观察理由>

WINDOW 02
IN: 00:03.86
OUT: 00:07.42
STATUS: REJECT
...
```

时间窗必须按时间升序；不得互相重叠。若Verifier无法判断精确边界，应保守缩短KEEP区间，不得用猜测扩张。

**Full Timeline Coverage：** 对非PASS / 局部失败Take，Temporal Salvage Map必须覆盖`00:00.00 → Source Duration`整个真实时间轴；不允许留下未分类Gap。所有不可用区间也必须显式标`REJECT`。相邻Window允许边界相接，但不得重叠或留洞。若某段因证据不足无法分类，则整个Salvage Status应降为`INSUFFICIENT_EVIDENCE`，不得用缺口假装已经完成完整观看。

---

## 7｜Salvage Clip Registry

QC发现可用时间段后，不直接把整个Take升级为APPROVED。内部建立：

```text
SALVAGE_CLIP_REGISTRY
Source Take: <TAKE_ID>
Source Take Verdict: <...>
Preserve Source File: TRUE

Clip ID: <...>
IN / OUT: <...>
Status: SALVAGE_CANDIDATE / APPROVED_SALVAGE_CLIP / STALE / REJECTED
Window Class: CLEAN_KEEP / CONDITIONAL_KEEP / HANDLE_ONLY
Editorial Function: <...>
Video Use: <...>
Audio Use: <...>
Conditions: <...>
Continuity Notes: <...>
Director Invariant Notes: <...>
Approval Source: <user / final edit approval; candidate阶段为空>
```

规则：
- QC发现可用片段 → `SALVAGE_CANDIDATE`；
- 源Take即使整体REVISE，也必须`Preserve Source File = TRUE`，不得因“废片”自动删除；
- 只有用户/最终剪辑明确采用该片段后，才升级`APPROVED_SALVAGE_CLIP`；
- `SALVAGE_CANDIDATE`不是Canon，也不能自动成为下一Segment的Ending Frame Authority。

---

## 8｜Ending Frame / Continuity边界

整体REVISE Take中的Salvage Window不能自动提供正式Previous Ending Frame。

只有满足全部条件时，Salvage Clip的真实末帧才可进入Ending Frame候选：
1. 该Salvage Clip已升级为`APPROVED_SALVAGE_CLIP`；
2. 它确实是最终剪辑中该Segment的视觉结束；
3. Trim-out来自原始真实Video Take的实际时间点；
4. 未对该帧做生成式重绘/Inpaint冒充真实帧；
5. 通过Ending Frame QC；
6. 用户批准最终使用关系。

之后才可登记`SALVAGE_ENDING_FRAME_CANDIDATE → APPROVED ENDING FRAME`。

---

## 9｜Failure Diagnosis与Retry联动

任何新增Video Take前必须先读取Temporal Salvage Map：

### 若`SALVAGE_AVAILABLE`
先判断失败区间能否在**不伤Director Invariants**的前提下独立补生成：
- 可以 → 保留成功片段，只为缺失Beat / Failure Window生成最小剩余内容；
- 不可以 → 仍可保留旧片作备用/Handle，但允许整Take重生；
- 若错误仅在可Trim尾部 → Stage 06 Trim，禁止重生；
- 若画面可用仅Audio坏 → 优先Stage 06换音频，不重生画面。

禁止为了利用Salvage而强行新增不该存在的CUT。

---

## 10｜多个Take的片段组合

若合法存在TAKE01 / TAKE02 / TAKE03，可从不同Take保留不同时间段，但必须通过：
- Identity / Wardrobe / Prop / Environment一致；
- Axis / Eyeline / Screen Direction兼容；
- 动作Entry/Exit State可接；
- Camera/Lighting/Style可接受；
- Audio continuity可处理；
- Director允许这些CUT存在。

通过后Stage 06可生成`SALVAGE ASSEMBLY EDL`；不通过则不得为了“省素材”拼成Frankenstein Sequence。

---


## 10.5｜Multi-Pass Salvage Merge

同一Take若因Web QC Evidence拆成多个Required Pass，不能把各Pass的KEEP时间窗直接做并集。最终Salvage Map必须：
1. 收集所有Required Pass的真实时间边界并切成Atomic Intervals；
2. 每个Interval读取所有相关Pass在其QC Scope内的结论；
3. 任一Required Pass有会使该Interval不可用的P0/P1 → 最终不得标`CLEAN_KEEP`；
4. 条件可以兼容时合并为更保守的`CONDITIONAL_KEEP / HANDLE_ONLY`并保留全部条件；
5. 结论互相矛盾且不能从Evidence消解 → `SALVAGE_MULTIPASS_CONFLICT`，补充验证同一Take，不得猜。

只有Merged Map拥有Stage 06剪辑决策权；单一Pass的Salvage Map只是Scoped Evidence。

---

## 11｜与QC Scope Freeze的区别

`QC Scope Freeze`冻结的是**检查维度**；`Temporal Salvage Map`冻结/保留的是**某个实际Take的时间素材**。

- 旧Take的CLEAN_KEEP窗口继续存在，不因为生成新Take而消失；
- 新Take仍是新的随机输出，不能拿旧Take的FROZEN_PASS代替新Take必要P0 Sanity Check；
- Temporal Window不能代替Dimension QC，Dimension Freeze也不能代替Temporal Salvage判断。

---

## 12｜Hard Fail

- `TEMPORAL_SALVAGE_NOT_ASSESSED`：非PASS/局部失败Take没有做Salvage判断；
- `SALVAGE_WINDOW_UNCUTTABLE`：标KEEP但Entry/Exit并不可合法剪；
- `SALVAGE_TIMELINE_COVERAGE_GAP`：非PASS/局部失败Take的Salvage Map没有覆盖完整Source Duration，存在未分类时间洞；
- `SALVAGE_DIRECTOR_INVARIANT_BREAK`：为了保留片段制造不允许的CUT/重排；
- `SALVAGE_CONTINUITY_MISMATCH`：片段与前后状态不可接却标CLEAN_KEEP；
- `SALVAGE_MULTIPASS_CONFLICT`：同一Take多个Required QC Pass的时间窗结论互相冲突，却未经补证据就直接合并；
- `SALVAGE_AUDIO_ASSUMPTION`：未听音频却擅自标AUDIO KEEP；
- `SALVAGE_TIMESTAMP_FABRICATION`：没有真实视频证据却编造IN/OUT；
- `SALVAGE_AUTO_APPROVAL`：QC Candidate未经用户/最终剪辑批准就升级APPROVED；
- `SALVAGE_ENDING_FRAME_AUTHORITY_BLEED`：整体失败Take的候选片段未正式采用就拿来做Ending Frame Authority；
- `SALVAGE_SOURCE_DELETION_RISK`：已有SALVAGE_CANDIDATE却允许删除唯一Source Take。

任一未解决：对应Salvage Window不得进入正式剪辑。
