# Generation Envelope Engine（生成包络与模型内多镜头执行层）｜Current Authority

> **用途：** 把“电影剪辑里的Formal Shot”与“AI视频模型的一次Generation Call”彻底解耦。`EDITORIAL_PLAN`决定为什么切；本文件决定哪些已锁Shot可以被装进同一次生成，以及它们以什么`FORMAT_MODE`执行。
>
> **核心关系：** `EDITORIAL_PLAN → Formal Shots → GENERATION_ENVELOPE → CUT_CONTRACT[] → VIDEO_EXECUTION_PLAN → VIDEO_PROMPT_ARTIFACT → Generation Job`。
>
> **不可覆盖硬门：** 任何不是`ONER`的Envelope，必须先有每个CUT对应的Approved白描Clean Panel，并由`tools/storyboard_grid_assembler.py`按CUT顺序确定性拼出一张`STORYBOARD_CLEAN_SEQUENCE_BOARD`。宫格缺失、顺序不符、混入别的Shot、仍未QC或像素内有文字/编号/箭头时，`NO VIDEO GENERATION`。

## 1｜Authority Boundary

### 本文件唯一拥有
- `Generation Envelope`的分组边界：哪些Formal Shots属于同一次模型调用；
- 实际`FORMAT_MODE`：`ONER / SEQUENTIAL_MULTISHOT / TIMED_MULTISHOT / FREESTYLE_BROLL`；
- `CUT_CONTRACT[]`执行封装；
- Multi-shot是否需要Storyboard Grid以及Grid与CUT顺序的一一对应；
- Multi-shot失败后的`ASSEMBLY_FIRST / SPLIT_TO_SINGLE_SHOT_ENVELOPES`降级策略；
- Provider Adapter进入前的模型无关Envelope结构。

### 本文件不拥有
- 为什么切、何时切、Reaction Give/Deny、Reveal逻辑：归`editorial_grammar_engine.md / EDITORIAL_PLAN`；
- Shot的Camera事实：归Cinematography / Camera Motion Authority；
- 人物Blocking、表演、物理、空间Canon；
- Provider具体FOV、时长字段、参数、Reference Slot写法：归Provider Adapter。

因此：**Envelope只能包装已锁导演事实，不能为了方便一次生成而重新发明镜头。**

## 2｜Formal Shot ≠ Generation Call

默认不再假设`1 Formal Shot = 1 Video Generation`。

合法关系：

```text
1 Formal Shot → 1 ONER Envelope
2–N相邻Formal Shots → 1 Controlled Multi-shot Envelope
1失败Multi-shot Envelope → N个Single-shot Envelope（导演意图不变）
```

合并只改变执行打包，不改变Shot ID、Cut Motivation、Camera Contract或Continuity事实。

## 3｜FORMAT MODE

### ONER
- Exactly 1 Formal Shot；
- 模型内`NO CUT`；
- 保留一个主Camera Idea；
- Envelope自身不要求额外子宫格，但该Shot自身Mandatory Clean Panel仍是Stage 04硬要求；若它属于一个2+ Formal Shot的Sequence，Stage 04仍必须存在整段`STORYBOARD_SEQUENCE_PROOF`白描宫格。

### SEQUENTIAL_MULTISHOT
- Exact 2–N CUT；
- CUT顺序锁定，但不强迫用秒数切；
- 每个CUT有独立Camera/Action/Performance/Information Contract；
- 只允许在已指定CUT边界切换。

### TIMED_MULTISHOT
- Exact 2–N CUT；
- 每个CUT有`start_sec / end_sec`；
- 累积时长必须闭合到Envelope总时长；
- 用于模型对时间段和硬切执行较可靠的场景。

### FREESTYLE_BROLL
- 只用于非关键连续性B-roll / Montage探索；
- 仍必须预先定义至少2个计划视角与白描宫格；
- 允许模型在这些已批准视角范围内探索节奏，不允许新增人物、地点、叙事事实或未批准镜头概念；
- 正式对白、线索Reveal、复杂动作接触、关键Transformation默认不得用此模式。

## 4｜什么时候允许合并成Multi-shot Envelope

优先同时满足：
- 同一Scene / 可连续推断的时间；
- 主要人物集合与当前状态稳定；
- 属于同一个Narrative Beat或不可分割的剪辑句子；
- Editorial Plan已锁定相邻Cut关系；
- 每个Shot已经有独立Storyboard Evidence；
- Reference / Conditioning没有无法解决的Slot竞争；
- 总时长在当前Provider能力范围内；
- 模型已知支持受控Multi-shot，或当前目标明确允许测试。

典型适合：
- `LOOK → OBJECT/POV → REACTION`；
- `ACTION START → CONTACT/INSERT → CONSEQUENCE`；
- `QUESTION → WITHHOLD → REVEAL`；
- 连续对话中的有动机关系视角转移。

默认不要合并：
- 跨地点/跨时间大跳跃；
- 角色身份或服装/伤势状态在镜间发生大版本变化；
- 每个镜头都需要完全不同复杂Reference Set；
- 复杂战斗多个高风险Contact同时挤在一个Envelope且模型稳定性不足；
- 只是为了“看起来会切镜”。

## 5｜CUT CONTRACT

每个CUT是一个Mini Shot Execution Contract，而不是一句“切到特写”。至少包含：

```text
CUT_ID / ORDER / SHOT_ID
NARRATIVE_FUNCTION
VIEWPOINT_ROLE
CAMERA_CHARACTER
CORE_LENS_INTENT
CAMERA_START / CAMERA_PATH / CAMERA_END
ACTION_BEAT
PERFORMANCE_BEAT
INFORMATION_REVEALED
CUT_IN_TRIGGER / CUT_OUT_TRIGGER
CONTINUITY_HANDOFF
STORYBOARD_PANEL_ASSET_ID
PRIMARY_VISUAL_ASSET_IDS（适用时）
POSITIVE_LOCKS
TIMING（Timed模式时）
```

### Camera Character
切镜不能只改变景别。至少判断观看方式是否发生变化：
- `LOCKED_OBSERVATIONAL`
- `STABLE_RELATIONAL`
- `SUBJECTIVE_HANDHELD`
- `TRACKING_PARTICIPANT`
- `REVEALING_MOVE`
- `COMPRESSED_WATCHING`
- `WIDE_SPATIAL`
- `DETAIL_INSPECTION`
- `DISORIENTED_SUBJECTIVE`
- `OTHER`

连续CUT若只做`MS正面 → MCU正面 → CU正面`而Camera Character、Information Relationship与Performance Access都没变化，视为伪多镜头风险。

## 6｜Multi-shot Mandatory White-line Grid Gate

> **两层门禁不要混淆：** Stage 04已有Sequence级硬门——任何`EDITORIAL_PLAN.shot_order`为2+的正式Sequence都必须先形成整段白描宫格`STORYBOARD_SEQUENCE_PROOF`。本节再处理Envelope级硬门：只有一个Generation Call内部含2+CUT时，还必须有与该Envelope CUT子集一一对应的宫格。

### 6.1 触发条件
满足任一条件即`MULTISHOT = TRUE`：
- `format_mode != ONER`；
- `shot_ids`数量 > 1；
- `cut_contracts`数量 > 1。

任何一项触发后都不能通过“实际只是一个镜头”绕开宫格。

### 6.2 必须先有独立Panel
每个CUT必须绑定自己的`STORYBOARD_CLEAN_PANEL`：
- `WHITE_LINE_STORYBOARD_ONLY`；
- Pixel Cleanliness全部false；
- 已通过Storyboard QC并Approved；
- `shot_id`与CUT一致；
- 不得用Hero Frame / Shot Execution Frame / Keyframe顶替。

### 6.3 宫格只能确定性拼版
按CUT `order`顺序，把上面的Clean Panels交给：

```bash
python3 tools/storyboard_grid_assembler.py <panel1> <panel2> ... \
  --output <sequence_board.png> \
  --manifest-output <sequence_board.manifest.json>
```

生成的Asset必须是：
- `asset_type = STORYBOARD_CLEAN_SEQUENCE_BOARD`；
- `layout_type = MULTI_PANEL`；
- `storyboard_render_mode = WHITE_LINE_STORYBOARD_ONLY`；
- `video_usage.primary_visual_eligible = false`；
- `storyboard_grid_assembly.source_panel_asset_ids_ordered`与CUT顺序完全一致；
- `storyboard_grid_assembly.assembler_tool = tools/storyboard_grid_assembler.py`；
- `fingerprint`与Envelope记录一致；
- QC=`PASS`。

**宫格不是让图像模型自己生成的Storyboard Page。** 它只是已批准独立Panel的无字确定性排序证据。

### 6.4 Stage 05硬阻断
Multi-shot若出现下列任一情况：
- Board缺失；
- Panel数量与CUT数量不同；
- Board父Panel顺序不一致；
- 某CUT没有独立白描Panel；
- Board或Panel未Approved / QC Fail；
- Board含文字、数字、箭头、CUT标签、时间码；
- Board Fingerprint不一致；

则：`MULTISHOT_STORYBOARD_GRID_GATE_PASS = false → NO VIDEO GENERATION`。

## 7｜Provider Adapter Boundary

Core只输出`core_lens_intent / camera_character / cut timing semantics`。
Provider Adapter才可把它编译为：
- FOV Anchor；
- Provider的多镜头格式关键词；
- Reference Slot / @资产写法；
- Positive Lock表达；
- Provider允许的时长字段。

平台能力不足时，不删Shot、不删Cut，只把同一Envelope降级为若干Single-shot Envelope并由Stage 06组接。

## 8｜Positive Lock而非否定词堆砌

Core的风险约束保留结构化记录，但Provider Adapter优先转译成可观察的正向锁：

```text
BAD: 人物不要哭，不要转头，不要多出人
GOOD: dry face, eyes controlled forward; head remains in the established three-quarter orientation; exactly two approved characters remain in frame
```

这不意味着删除Failure Risk；只是避免模型正文把“不想要的内容”反复强化。

## 9｜Stage Handoff

### Stage 02
`EDITORIAL_PLAN`锁定Why/When/Where Cut。此时只表达“允许Multi-shot还是默认Assembly”的意图，不拥有最终Provider格式。

### Stage 04 Storyboard
每个Formal Shot真实生成独立Mandatory White-line Panel并批准。

### Stage 04B Video Conditioning Build
- 依据Editorial Plan + Provider Capability建立`GENERATION_ENVELOPE`；
- ONER直接进入后续Conditioning；
- Multi-shot必须运行Storyboard Grid Assembler并登记Sequence Board；
- `generation_envelope_lint.py`通过后才可进入后续Video Conditioning。

### Stage 05
`VIDEO_EXECUTION_PLAN`必须引用当前Envelope及Fingerprint。Multi-shot按照CUT_CONTRACT编译为单条Prompt的多个Shot Block；ONER维持单镜头Prompt。

### Stage 06
- ASSEMBLY_FIRST按Editorial Plan组接Approved Clips；
- Multi-shot Take允许`sub-cut salvage`：好CUT可保留、坏CUT可单独重生替换；
- Salvage不能改变锁定的Reveal、POV、Reaction Give/Deny与关键Continuity。

## 10｜Hard Fail

- `GENERATION_ENVELOPE_FORMAT_CONFLICT`
- `GENERATION_ENVELOPE_SHOT_SET_CONFLICT`
- `CUT_CONTRACT_GAP`
- `CUT_ORDER_CONFLICT`
- `MULTISHOT_STORYBOARD_PANEL_GAP`
- `MULTISHOT_STORYBOARD_GRID_MISSING`
- `MULTISHOT_STORYBOARD_GRID_ORDER_MISMATCH`
- `MULTISHOT_STORYBOARD_GRID_QC_FAIL`
- `MULTISHOT_FORMAT_CAPABILITY_UNSUPPORTED`
- `MULTISHOT_TIMING_BUDGET_FAIL`
- `MULTISHOT_REFERENCE_SCOPE_CONFLICT`

这些Failure只回滚最小Owner；不得因一个Envelope失败而重做整集。

## 8｜CUT Boundary Spatial Continuity（新增）

每个`CUT_CONTRACT`的`continuity_handoff`不再只是自由文字；推荐同时维护结构化`SHOT_BOUNDARY_CONTINUITY_CONTRACT`并记录：
- `inheritance_mode`：`DIRECT_CONTINUITY / MATCH_ON_ACTION / CUT_REFRAME / REACTION_CUT / ELLIPSIS / SPATIAL_REORIENTATION / SCENE_CHANGE`；
- `world_state_in → world_state_out`；
- `required_invariants`：哪些人物/道具/环境状态必须继承；
- `allowed_changes`：哪些字段允许因为机位变化、表演推进或省略而改变；
- `continuity_distance`：`LOW / MEDIUM / HIGH / SCENE_BOUNDARY`。

若相邻CUT的空间/动作变化超过当前模型一次可稳定承接的范围，应拆成更短Envelope或插入中间State；不得把HIGH距离跳变硬塞给一次生成。
