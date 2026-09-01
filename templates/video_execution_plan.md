# Video Execution Plan（视频执行计划）｜Stage 05 Pre-Compile Authority

> **目的：** Final Video Prompt不是把20个栏目拼起来。Stage 05必须先读取当前`GENERATION_ENVELOPE`，再把已批准的Director / Storyboard / Shot Execution / Spatial / Performance / Camera / Audio / Reference事实求解成一个**按时间可执行、空间可达、身体可行、镜头可读、切点可执行**的`VIDEO EXECUTION PLAN`，通过后才允许编译至少2500个非空白字符、且Master上限为NONE的Seedance Prompt。
>
> **核心原则：** `SOLVE FIRST → WRITE SECOND.` 先解决“这一镜到底怎么发生”，再写自然语言。Execution Plan是结构化执行结论，不是隐藏思维过程；用户可看到摘要，内部可保留结构化记录。

## 1｜输入

至少读取：
- `GENERATION_ENVELOPE`（FORMAT_MODE / shot_ids / CUT_CONTRACT[] / Storyboard Grid Gate）；
- Director Invariants / Shot Contract / Sequence Arc；
- Approved Mandatory Storyboard / Supplemental Previs（若有）；
- `VIDEO_CONDITIONING_READY`与Primary Shot Execution Frame；
- `SPATIAL_EXECUTION_STATE`；
- Current World / Character / Prop / Continuity State；
- Reference Binding Map + Current Scene Color Authority + Video Color Reference Mode；
- 适用时的Performance / Natural Motion / Combat / Voice / Camera Authority。

任何上游事实仍未锁定时不得用Execution Plan自行发明第二套Canon。

## 2｜固定求解顺序

### Pass A｜Reference / Authority Integrity
先确认：
- 当前真正参与生成的`@资产`是谁；
- Primary Shot Execution Frame是否继承当前Scene/Look Domain的Scene Color Authority；
- `scene_color_reference_mode`是否为`LINEAGE_ONLY / TEXT_CONTROL / DIRECT_REFERENCE`之一；默认优先`LINEAGE_ONLY`，只有明确综合色风险Trigger时才让Scene Color Card占Direct Reference槽；
- Character / Prop / Continuity Reference是否职责重叠或互相矛盾；
- Reference只提供稳定Authority，不得覆盖Director已锁动态事实。

有Reference冲突：`REFERENCE_EXECUTION_CONFLICT` → BLOCK。

### Pass B｜Spatial Blocking
对每个关键人物/道具明确：
- Entry Position / Depth / Orientation；
- 与目标人物、道具、门窗、家具、车辆等Anchor的关系；
- Movement Corridor；
- Motion Target；
- End Landing；
- Visibility / Occlusion变化；
- 180 Axis / Screen Direction / Eyeline（适用时）。

必须回答：**从起点能不能真实走到终点？路径有没有穿墙、穿人、跨越不可达Anchor或突然左右翻转？**

失败：`EXECUTION_SPATIAL_PATH_CONFLICT`。

### Pass C｜Body / Prop Occupancy
对当前可见关键人物检查：
- 左手、右手、左脚、右脚分别正在做什么；
- 哪只脚/哪个身体部位承重；
- Holder / Support / Contact关系；
- 换手、抓取、释放、推拉、扶持是否有中间过程；
- 一个肢体不得在同一时间执行两个互斥任务。

失败：`EXECUTION_LIMB_OCCUPANCY_CONFLICT`。

### Pass D｜Action + Performance Causality
人物动作必须沿因果链组织，不直接从情绪标签跳到结果：

`Trigger → Perception → Processing Delay → Micro-expression Leak → Decision/Tactic → Preparation → Primary Action → Settle/Recovery`

适用时明确：
- Objective / Tactic / Subtext；
- Active Listening / Reaction Give-Deny；
- 微表情顺序（眼、眉、唇、下颌/喉部、呼吸、小动作）；
- 视线Trigger与Landing；
- 重心准备、动作启动、加减速与动作完成后的余势。

**不要求每个2秒窗口都塞满微表情。** 只有当前Beat存在人物表演信息时才写，但一旦存在，必须是有Trigger的变化过程，不能只写“悲伤/紧张/自然”。

失败：`EXECUTION_PERFORMANCE_CAUSALITY_GAP`。

#### Pass D.5｜Asymmetric Multi-Human Performance Gate

同镜存在2名及以上可见人物时，除非剧本明确要求同步动作，Execution Plan必须为每人分别锁定：
`Objective / Trigger / Perception / Reaction Latency / Gesture Vocabulary / Action Arc / Listener Response / Settle`。

硬规则：
- 不同人物不得共享同一动作起点、手势、节拍、视线转移、身体路径与停稳时刻；
- “两人同时抬手、同时转头、同频后退、镜像式比划”不得作为默认群众化动作；
- 主说话者的表演与Listener Reaction分轨，听者按人物关系采用不同延迟与不同反应幅度；
- 若剧情要求同步，必须记录可验证的共同Trigger与同步目的；
- 每个Performance Track只保留符合该人物Objective的少量动作，不用抽象手舞足蹈填满对白。

未证明差异化或出现无剧情依据的同频动作：`MULTI_HUMAN_SYNCHRONY_ANTIPATTERN` → BLOCK。

### Pass E｜Camera Grammar
每个时间窗优先只保留**一个Dominant Camera Idea**：
- Start Geometry；
- Shot Size / Height / Angle / Lens Family / Focus；
- Move Trigger；
- Path；
- Speed / Motion Curve；
- Subject Relationship；
- Landing Geometry / Composition。

同一窗口禁止无证明地堆叠“推进 + 环绕 + 升降 + 摇摄 + 手持”等互相竞争的Camera Move。复杂Camera必须有Storyboard/Camera Path Previs证明。

失败：`EXECUTION_CAMERA_COMPETITION_CONFLICT`。

#### Pass E.2｜Camera Landing Reachability Gate

Camera的Start / Path / Landing必须做几何闭合。Execution Plan必须回答：最终Attention Target在世界空间和画面投影上如何从起始位置到达目标构图。

- 固定中轴、无摇摄、主体不移动时，偏轴人物不能被要求在结尾自动居中；
- 需要转移构图主权时，只能选择物理可达的主体位移、受控Pan/Tilt、Dolly/Truck/Arc或可证明的组合运动；
- 复合运镜必须写清唯一Trigger、先后顺序、角度/距离范围和停稳点，不能同时声明“锁死机位”和“最终居中”；
- Landing必须留出可读Hold，不能在最后一帧才仓促甩到目标。

无法证明：`CAMERA_LANDING_GEOMETRY_CONFLICT` → BLOCK。

### Pass E.5｜Generation Envelope / Editorial Boundary Protection
先读取`GENERATION_ENVELOPE.format_mode`，不得再从Prompt作者临时决定是否切镜。

**ONER**：本Plan只执行一个Formal Shot，模型内`NO CUT`；仍继承`Viewpoint Role / Edit Entry Function / Protected Editorial Moment / Edit Exit Function / Incoming-Outgoing Cut Strategy`，给Stage 06留下真实可用的Entry/Exit State与必要Handle。

**Multi-shot**：
- `MULTISHOT_STORYBOARD_GRID_GATE_PASS`必须先为真；
- Execution Plan逐个复制`CUT_CONTRACT[]`成为`cut_handoffs`；
- 每个Block对应一个Formal Shot、一个Approved白描Panel、自己的Camera Character与Entry/Exit Trigger；
- `TIMED_MULTISHOT`必须闭合全部start/end时间；
- 不允许在CUT之间插入Envelope中不存在的新机位；
- Sequence Board只做结构辅助证据，不能成为Primary Visual。

失败：`EDITORIAL_BOUNDARY_EXECUTION_GAP / IN_MODEL_MULTISHOT_EVIDENCE_GAP / MULTISHOT_STORYBOARD_GRID_* / MULTISHOT_TIMING_BUDGET_FAIL`。

### Pass F｜Timing / Instruction Budget
把当前Video Unit拆成连续时间窗，优先使用剧情Beat而不是平均切秒：

`W01 start–end → Trigger / Human Response / Action / Camera / Physics / Sound / Landing`

检查：
- 所有MUST动作在目标时长内是否可完成；
- 动作是否留出Preparation / Processing Delay / Contact / Recovery；
- 同一窗口的独立动作、Prop事件、Camera Move是否超过Proof Capacity；
- 关键视觉Read是否有足够Hold；
- 超载时优先拆Shot / Segment，不用把七八件事压缩成一句。

失败：`EXECUTION_TIMING_BUDGET_OVERFLOW`。

### Pass G｜Physics / Environment / Audio Synchronization
按时间窗绑定：
- Weight / Momentum / Contact / Recoil；
- Hair / Cloth / Liquid / Rain / Smoke / Debris余动；
- Door / Vehicle / Furniture等环境响应；
- Foley / Ambience / Dialogue / Breath / Music事件；
- 声音必须和对应可见事件或剧情内来源对齐。

失败：`EXECUTION_CAUSAL_SYNC_CONFLICT`。

### Pass H｜Conflict Audit + Freeze
运行`prompt_constraint_solver.md`与适用机械Validator，确认：
- Hard Conflict Count = 0；
- Motion Load / Camera Load可执行；
- Reference / Spatial / Body / Timing / Audio没有未解冲突；
- Ending State与下一镜Continuity不矛盾。

通过后写：`VIDEO_EXECUTION_PLAN_PASS = true`，Plan状态=`FROZEN_FOR_COMPILE`。

## 3｜结构化Execution Plan

```text
VIDEO EXECUTION PLAN
Generation Envelope：
Format Mode：ONER / SEQUENTIAL_MULTISHOT / TIMED_MULTISHOT / FREESTYLE_BROLL
Formal Shot IDs：
Video Unit：
Duration：
Status：DRAFT / BLOCKED / FROZEN_FOR_COMPILE

REFERENCE INTEGRITY
- Primary Visual：
- Scene Color Authority：
- Scene Color Reference Mode：LINEAGE_ONLY / TEXT_CONTROL / DIRECT_REFERENCE
- Color Direct-Reference Trigger：<none / explicit reason>
- Additional Direct Binds：
- Conflict Count：0

SPATIAL BLOCKING
- Subject：Start → Corridor → Target → End Landing
- Axis / Screen Direction / Eyeline：
- Spatial Conflict Count：0

BODY / PROP OCCUPANCY
- Subject：LH / RH / LF / RF / Support / Prop Holder
- Occupancy Conflict Count：0

EXECUTION WINDOWS
- W01 [start–end]
  - Trigger / Perception / Processing：
  - Micro-expression / Eyeline：
  - Preparation / Primary Action / Recovery：
  - Limb / Prop State：
  - Physics / Environment Response：
  - Camera：Start → Trigger → Path/Speed → Landing
  - Audio / Dialogue / Breath：
  - Critical Read / Hold：
- W02 ...

TIMING
- Target Duration：
- Planned Duration：
- Fits：YES / NO

EDITORIAL / ENVELOPE BOUNDARY
- Editorial Permission：ASSEMBLY_FIRST / IN_MODEL_MULTISHOT
- Actual Format Mode：ONER / SEQUENTIAL_MULTISHOT / TIMED_MULTISHOT / FREESTYLE_BROLL
- Storyboard Grid：N/A / APPROVED ASSET + FINGERPRINT
- Cut Handoffs：CUT_ID / SHOT_ID / Panel / Camera Character / In Trigger / Out Trigger / Timing
- Viewpoint Role：
- Edit Entry Function：
- Protected Editorial Moment：
- Edit Exit Function：
- Incoming / Outgoing Edit：
- Required Head / Tail Handle：

ENDING STATE
- Character / Prop / Camera / Environment Landing：
- Continuity Handoff：

CONFLICT AUDIT
- Hard Conflict Count：0
- Unresolved Issues：[]

VIDEO_EXECUTION_PLAN_PASS：YES / NO
```

## 3.5｜Storyboard → Prompt Handoff Contract

在Plan Freeze前，把Approved白描Storyboard的离图Metadata正规化为`storyboard_handoff`。固定字段为：
`CAMERA_MOTION / TIMING / CUT_NOCUT / ACTION_BEAT / PERFORMANCE / EYELINE / SHOT_RELATION / LANDING`。

规则：
- `CAMERA_MOTION / TIMING / CUT_NOCUT / ACTION_BEAT / LANDING`永远=`REQUIRED`，静止机位也必须明确写成“摄影机锁定/无位移”，无CUT也必须明确`NO CUT`；
- `PERFORMANCE / EYELINE / SHOT_RELATION`若确实不适用，可=`NOT_APPLICABLE`，但必须写`reason`；
- 每个`REQUIRED`项保存Storyboard来源的`source_text`，并生成一句最终视频正文必须真实包含的`prompt_anchor`；
- `prompt_anchor`不是行政标签，而是可直接给视频模型执行的自然语言；
- Final Prompt生成后运行`storyboard_to_video_prompt_handoff_lint.py`。它逐项核对Anchor，不接受“只有摄影机/时间轴等泛关键词”冒充继承。

任一必需项未进入Final Prompt：`STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP → 返回Compiler`。

## 4｜Prompt Assembly Rule

Execution Plan通过后，Compiler**按时间因果重新编排为自然语言**，而不是照20个字段逐栏复制。

推荐模型正文结构只有5个大块：
1. `@资产 + 镜头目标 / 时长 / 起始状态`；
2. `空间 / 构图 / 景别 / Camera起始几何`；
3. `Integrated Timeline`：把动作、表演、视线、肢体占用、物理、环境、Camera、声音按发生时间融合；
4. `Ending State / Continuity Landing`；
5. `Necessary Restrictions`。

20项Coverage Map仍必须全部满足，但**不等于20个独立标题**。同一事实只在最有执行价值的位置出现一次。

## 5｜Combat Extension
真实Combat Segment在本Plan中额外求解：
`Combat Objective → Engagement Distance → Read/Decision → Attack/Defense Exchange → Attack/Escape Lane → Contact/Near Miss → Force Direction → Recoil/Recovery → Initiative Shift → Combat Camera Read → Exit Combat State`。

Combat规则只增加战斗因果，不取消普通Performance、Spatial、Camera、Physics和Ending State。

## 6｜Hard Gate
以下任一成立：`NO FINAL VIDEO PROMPT / NO VIDEO GENERATION JOB`：
- `VIDEO_EXECUTION_PLAN_PASS != YES`；
- Hard Conflict Count > 0；
- Timing Fits = NO；
- Primary Camera Window竞争未解决；
- Spatial Path / Limb Occupancy / Reference Authority存在P0/P1冲突；
- Ending State无法与Continuity对齐。

## Current｜Fingerprint / Stale Hard Gate

Frozen Execution Plan必须写入：
`director / storyboard / shot_execution / scene_color / world_state`五个Source Fingerprint；存在`GENERATION_ENVELOPE`时还必须写`generation_envelope` fingerprint，并写入自身`execution_plan_fingerprint`。

任一Source Fingerprint变化：`EXECUTION_PLAN_STALE`。此时：
- `VIDEO_EXECUTION_PLAN_PASS`失效；
- 已编译`VIDEO_PROMPT_ARTIFACT`失效；
- 已创建但尚未执行的Video Generation Job不得进入READY；
- 只回退到最小受影响的Execution Plan/Prompt编译层，不无理由重开已批准上游。

## V4.5.7｜Shot Boundary Continuity Contract（新增）

Stage 05在编译多镜头或跨段连续视频时，必须把`Previous Approved Ending Frame + Continuity Snapshot`转译成结构化`SHOT_BOUNDARY_CONTINUITY_CONTRACT`，至少明确：
- 哪些人物/关键道具必须严格继承世界位置；
- 哪些只是画面重投影；
- 当前动作处于什么Phase，下一CUT从哪一Phase进入；
- 是否存在`continuity_distance=HIGH`，若存在则优先拆Envelope或要求额外中间State。

Reference Resolver也应优先选择**最近的空间-视觉父级**：`Previous Ending Frame / Shot Execution Frame / Nearest Environment Anchor / Critical Prop View`，而不是默认堆满所有Reference。

### V4.5.11｜Editorial Cut Bridge精度分层

每个Boundary Contract必须先区分：

- `PIXEL_EXACT_T0`：只用于`SEAMLESS_EXTEND / GUIDED_CONTINUATION`；Ending Anchor是唯一model`t=0`视觉Owner。
- `WORLD_STATE_STRICT`：切镜后世界位置、接触、Holder与动作Phase严格继承，但画面由新机位重投影。
- `STORYBOARD_BLOCKING_APPROXIMATE`：默认切镜路线。Approved Storyboard Exit/Entry只需在人物集合、Zone/Anchor、Screen Side或动作方向、深度、朝向、动作Phase、道具Holder/数量上大致合理；新Shot Execution Frame与高清Authority负责最终像素。
- `SCENE_RESET`：合法场景重置，不继承上一帧构图。

采用`STORYBOARD_BLOCKING_APPROXIMATE`时必须记录：

`ending_frame_provider_route = LINEAGE_ONLY | STAGE06_EDIT_REFERENCE_ONLY`、`storyboard_exit_panel_ref`、`storyboard_entry_panel_ref`、`transition_language`和`required_invariants`。不得设置`DIRECT_T0_ANCHOR`，不得要求微姿态或像素纹理复制。若无Approved Storyboard Bridge或P0 Holder/数量/动作Phase未闭合，不能用“剪辑会遮住”放行。

## V4.5.7｜Entity Binding Handoff（新增硬门）

读取`STORYBOARD_ENTITY_BINDING_MAP`并建立`VIDEO_EXECUTION_PLAN.entity_binding_handoff`。Scene-bound Video固定`reference_integrity.direct_binding_policy = FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING`，并记录`target_provider_profile + field_owner_map + omitted_redundant_reference_ids`。每个当前Panel使用过的Slot必须保存：
- `slot_id / entity_id / entity_type / prompt_entity_label`；
- `resolution_mode`：清楚可见Human与Environment固定=`DIRECT_REFERENCE`；Prop/Nonhuman按风险可使用`PRIMARY_VISUAL_BAKED / DIRECT_REFERENCE / TEXT_CONTROL / OMITTED`；
- Direct时的`resolved_asset_id + native_token`；
- `prompt_identity_anchor / blocking_anchor / action_anchor`。

Human Slot的三类Anchor必须被最终Prompt逐字/稳定短语继承：**谁、站在哪里/朝哪里、正在做什么**。如果白描能看出姿态但无法把站位与动作反编译成明确自然语言，`VIDEO_HUMAN_PROMPT_RECOVERABILITY_GAP`，不得Freeze Execution Plan。

Freeze前必须登记`mandatory_direct_reference_ids`，至少覆盖当前Empty Environment Master与所有清楚可见Human Masters；Storyboard按Target Adapter声明的Temporal/Blocking Route进入Direct或Prompt Closure。Primary若Direct必须证明仍独占字段；若省略必须记录`OMIT_REDUNDANT_BAKED_COMPOSITE`及由Storyboard+Prompt+高清母图覆盖的字段。缺失或字段双Owner：`PROVIDER_ROUTED_FIELD_AUTHORITY_GAP / REDUNDANT_COMPOSITE_REFERENCE_COMPETITION`。
