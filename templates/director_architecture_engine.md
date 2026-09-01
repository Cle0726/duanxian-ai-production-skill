# Director Architecture Engine（导演架构引擎） Current Authority

> **Story Input Gate：** Stage 02 Director Architecture只接受当前`EPISODE SCREENPLAY LOCK`派生的Scene Intent；不得从小说原段/旧Story Lock临时补一个未经改编的剧情Beat。
> **用途：** 承接`director_intelligence_core.md`已经由Director Judge选定的导演解释，把Sequence Arc转成可执行空间、Blocking、Camera与Detailed Shot Contract。它不再负责“第一时间想出怎么拍”。
>
> **核心原则：** `Selected Directorial Thesis → Sequence Arc → Staging → Camera → Shot Progression → Cut → Segment → Asset Need`。资产服务导演，AI执行限制不得反向偷改Selected Thesis。

## 1｜Stage 02正式内部顺序

Stage 02分三层：

### A. Director Intelligence Pass（必须先完成）
读取`director_intelligence_core.md`：
1. Story / World State；
2. Audience Knowledge / Emotion IN→OUT + Dramatic Question + Felt Intent；
3. Directorial Importance Tier；
4. 1/2/3个真正不同的Directorial Interpretation；
5. D1/D2执行Actor / Cinematographer / Editor Critique；
6. Director Judge锁Selected Option + Non-Negotiable Directorial Invariants；
7. 读取`sequence_arc_engine.md`锁Sequence Arc；
8. 读取`editorial_grammar_engine.md`建立`Editorial Intent Draft`（Viewpoint Arc / Hold-Transfer-Reveal / Cut Strategy），暂不要求完整Shot ID。

没有Director Judge、Sequence Arc与Editorial Intent Draft，不得进入下面的Director Architecture Pass。

### B. Director Architecture Pass
9. `Scene Spatial Requirement Draft`；
10. `Dramatic Geometry / Blocking`；
11. `Axis / Screen Direction / Eyeline Plan`；
12. `Distance Arc / Depth Plan + Cinematography Grammar`；
13. `Scene Coverage Strategy / Shot Progression`；
14. 将Editorial Intent Draft映射到正式Shot ID，**同步锁定 `EDITORIAL_PLAN + Detailed Shot Contract`**。

完成9–14并通过Director Hard Gates后，Scene Core=LOCKED；整集所有Scene Core锁定后Episode级=`DIRECTOR CORE LOCKED`。

### C. Production Translation Pass
15. 读取`director_to_ai_execution_boundary.md`建立Director Invariants / Execution Variables；
16. `Segment Plan`；
17. `Shot Storyboard Coverage Plan + Supplemental Previs`；
18. `Raw Asset Analysis`；
19. `Asset Consolidation & Sufficiency Audit`；
20. `Final Episode Asset Requirement Manifest`。

Production Translation只能改变执行方法，不能静默改变Audience Alignment、Reveal顺序、核心Blocking、关键Reaction Give/Deny、POV或Sequence关键Hold/Cut。若执行限制确实冲突，输出`AI_EXECUTION_CONSTRAINT_CONFLICT`返回Director Judge裁决。

Stage 03批准Environment Canon Master + Geography后仍执行`director_spatial_reconciliation_gate.md` Pass A/Pass B；这属于真实空间验证，不是重新导演。

## 2｜Selected Directorial Thesis / Visual Thesis

本区只接收Director Judge已选定的Thesis，不重新生成候选。每个重要Scene至少明确：

```text
Scene Narrative Function：
Primary Emotional Pressure：
Power Relationship：谁在压迫/回避/保护/观察谁
Visual Thesis：一句话说明这场戏的核心视觉关系
Visual Reveal Priority：观众先知道空间/人物/道具/威胁中的什么
Spatial Change Across Scene：空间关系从什么变成什么
Shot Progression Intent：距离/景别/视角总体怎样变化
End Visual State：离场时观众应记住的构图/关系
```

`Visual Thesis`不能只写“紧张 / 悲伤 / 激烈”。必须能转译成空间或摄影，例如：
- “两人始终被门框隔开，直到角色A主动跨入B的个人距离”；
- “怪物逐步从背景威胁压到前景，最终遮住出口”；
- “变身前人物被环境吞没，变身完成后人物剪影主导画面”。

---

## 3｜Scene Spatial Requirement Draft（Stage 03前的功能空间草案）

新Environment尚未批准时，不假装知道完整建筑几何。Stage 02只锁剧情必须满足的**功能关系**：

```text
Required Functional Zones：舞台 / 门区 / 病床 / 驾驶位 / 台阶等
Must-See Relationships：哪些Zone/地标必须能在同一视线或同一Shot建立关系
Required Movement Lanes：人物/怪物/车辆必须能通过的路径
Required Combat Clearance：战斗或追逐至少需要怎样的活动区
Required Sightlines：谁必须看得到谁/哪个出口/哪个关键Prop
Required Barriers：桌、门框、钢琴、柱子等是否承担关系/阻挡功能
Unknown Geometry：尚未批准、不能在此时写死的空间事实
```

这是给Stage 03 Environment设计的导演需求，不是Environment Canon本身。

---

## 4｜Dramatic Geometry / Blocking（戏剧几何与场面调度）

人物位置必须从Objective / Relationship / Threat / Physical Task推出，而不是“为了让每个人都完整出现”。

### 4.1 Blocking Tactic
可按需使用：
- `APPROACH`｜主动缩短距离；
- `WITHDRAW`｜拉开距离；
- `CROSS`｜横穿对方视线/轴线；
- `OCCUPY`｜占据关键空间；
- `BLOCK_EXIT`｜封住出口；
- `KEEP_BARRIER`｜刻意保留桌/门/座位等屏障；
- `TURN_AWAY`｜拒绝视线/关系；
- `SHARE_SPACE`｜进入共同动作区；
- `PROTECT / INTERPOSE`｜身体进入另一人与威胁之间；
- `ENCIRCLE / FLANK`｜战斗/多人场面包围或侧击。

不要求每句对白都有走位；只有关系、战术或物理任务发生变化时才改变Blocking。

### 4.2 Inter-character Distance
使用相对距离，不机械要求厘米：
- `INTIMATE / TOUCHING`
- `PERSONAL`
- `ARM_REACH`
- `WEAPON_REACH`
- `ONE_STEP_THREAT`
- `MID_SEPARATION`
- `LONG_SEPARATION`

Combat可在内部补大致米数/武器有效距离用于可行性检查，但不强迫模型看到数字。

### 4.3 Distance Arc
重要Scene/Beat记录距离变化：

`Entry Distance → Pressure Distance → Contact/Reveal Distance → Exit Distance`

距离本身必须能解释剧情变化。禁止整场重要冲突一直保持同一“安全展示距离”。

---

## 5｜Depth Composition（纵深构图）

重要多人Shot必须考虑：
- `FG / MG / BG`：谁在前景、中景、背景；
- `Subject Screen Occupancy`：主要主体相对画面占比；
- `Overlap / Occlusion`：NONE / LIGHT / INTENTIONAL；
- `Crop Permission`：FULL / PARTIAL / AGGRESSIVE；
- `Negative Space Purpose`：留白服务威胁、视线、运动还是信息；
- `Depth Change`：人物是否在Shot内跨越景深。

**P0：** 除非剧情明确需要仪式性/对峙式正面陈列，重要多人Shot不得默认“所有人同深度、同尺寸、均匀间距、全身完整可见”。

失败：`STAGING_DISTANCE_FLAT_FAIL`。

---

## 6｜Axis / Screen Direction / Eyeline（轴线、屏幕方向、视线）

每个多人/运动Scene在Shot前先建立：

```text
Primary 180 Axis：
Character Screen Side Baseline：A=L / B=R / ...
Primary Eyeline Pair：
Movement Direction：L→R / R→L / Depth In/Out
Axis Crossing Allowed：NO / YES + 为什么
Re-establish Method（若越轴）：中性镜头 / 可见跨轴 / 新Establishing
```

规则：
- CUT后屏幕方向要能追溯到轴线计划；
- 战斗攻击线、追逐运动方向和Eyeline不能无因翻转；
- 允许有意越轴，但必须让观众重新理解空间；
- Environment镜像或Reference镜像不能偷偷改变Screen Direction Authority。

失败：`SCREEN_DIRECTION_FAIL / EYELINE_CONTINUITY_FAIL / AXIS_CROSS_UNMOTIVATED`。

---

## 7｜Visual Hierarchy（画面主次）

每个重要Shot至少锁：

```text
Focus Owner：第一眼主体
Secondary Read：第二信息
Background Information：只需存在，不抢第一读
Read Order：1 → 2 → 3（适用时）
Critical Visual Read：当前Shot必须让观众真正看清的字段
```

`Critical Visual Read`可包括：
- FACE / EYE / MUSICAL_EYE_MOTIF
- WEAPON_GEOMETRY / CONTACT_POINT
- PROP_STATE / PERSONAL_ADORNMENT
- EXIT / SPATIAL_RELATION
- INJURY / DAMAGE
- TRANSFORMATION_SILHOUETTE

如果剧情要求观众看清某字段，而Shot Size / Occupancy根本不足，导演阶段就必须改镜头，不允许等Stage 04/05再发现。

失败：`CRITICAL_VISUAL_READ_FAIL / VISUAL_HIERARCHY_FLAT_FAIL`。

---

## 8｜Scene Coverage Strategy / Shot Progression

Shot不能只逐条“各自合理”，整场还必须有摄影推进。

每个重要Scene记录：

```text
Opening Coverage Function：
Distance Progression：例如 WIDE → MEDIUM → TIGHT → RELEASE WIDE
Perspective Progression：观察 / 进入 / 压迫 / 主观 / 释放等
Optical / Focus Progression：只有Lens Family / Focus Access的变化具有叙事因果时填写
Information Progression：每次靠近/拉远增加什么
Shot Repetition Rule：哪些景别/构图可以重复，为什么
Closing Coverage Function：
```

没有固定公式；允许从Close碎片开始、后揭全景，也允许稳定长镜。但必须能解释**为什么这一场的摄影距离这样变化**。

失败：`SHOT_PROGRESSION_FLAT_FAIL`。

---

## 8.5｜Dramatic Sound / Silence & Narrative Lighting Intent（条件性导演感官意图）

这不是Stage 06混音/配乐设计，也不要求每个Shot填声音灯光表。只有声音缺失、画内音乐、关键SFX、光线变化或剪影揭示会改变叙事/剪辑时才锁。

### Dramatic Sound / Silence
```text
Diegetic Sound Focus：当前Scene最重要的画内声音
Silence / Absence Rule：什么声音应该“缺失”或突然中断
Sound Perspective：SOURCE NEAR / FAR / OFFSCREEN / DIRECTIONAL（适用时）
Sync-Critical SFX：必须与画面Contact/Mechanism/Reveal同步的声音
Sound Bridge：NONE / J-CUT / L-CUT / MATCH / CARRY
Audio-led Cut：声音是否触发CUT / Reveal / Reaction
Dialogue Priority：声音是否必须让位于对白
```

Stage 02只锁剧情/导演需要的声音事件；Stage 05仍服从`video_audio_generation_boundary.md`，正式BGM留Stage 06。

### Narrative Lighting Intent
```text
Motivated Source：主要实际光源/来源
Narrative Function：SEPARATE SUBJECT / HIDE / REVEAL / SILHOUETTE / PRESSURE / WARMTH / OTHER
Critical Visibility：哪个Face / Eye / Weapon / Material必须被光线读出
Lighting Change Trigger：灯灭/门开/雷光/Transformation/FX等
Shot Lighting Variant Need：NONE / TEXT / REUSABLE REFERENCE REVIEW
```

光色实现继续服从`color_script_derivation_engine.md`的Global → Scene → Shot层级。导演只锁叙事功能，不重写Color Authority。

---

## 9｜Detailed Shot Contract（详细镜头契约）

T1/T2简单Shot使用Minimum Necessary Fields；T3/T4、Combat、Transformation、多人复杂Blocking必须完整填写。

```text
Shot ID / Beat：
Shot Purpose：
Focus Owner / Secondary Read：
Critical Visual Read：
Shot Size / Camera Distance：
Subject Screen Occupancy：
Inter-character Distance：
Depth Layers：FG / MG / BG
Overlap / Crop：
Camera Side / Axis：
Screen Direction / Eyeline：
Entry Camera Height / Vertical Angle / Subject View：按`cinematography_grammar.md`，仅填写会改变镜头含义的字段
Lens Family：WIDE_PERSPECTIVE / NORMAL / PORTRAIT_COMPRESSION / LONG_LENS_OBSERVATION / MACRO_DETAIL（按需）
Focus Plan：Focus Plane / DOF / Focus Behavior / Trigger-Landing（按需）
Stabilization / Support：LOCKED_OFF / TRIPOD_HEAD / GIMBAL_STABILIZED / SHOULDER / HANDHELD / DOLLY_RAIL / CRANE / VEHICLE_MOUNT / OTHER（按需）
Dramatic Sensory Cue：仅当Audio / Silence / Lighting对当前Shot因果重要时填写
Blocking Start：
Blocking Change：
Blocking End：
Camera Intent：STATIC PRESSURE / SLOW APPROACH / SUBJECT FOLLOW / REVEAL TRAVEL / COMBAT PURSUIT / OTHER
Motion Priority：SUBJECT / OPPONENT / CAMERA / ENVIRONMENT / VFX
Viewpoint Role：按`editorial_grammar_engine.md`，定义观众此刻站在哪里
Edit Entry Function：当前Shot为什么从上一个Cut进入
Protected Editorial Moment：本Shot不可被剪掉/遮掉的动作、反应或信息节点
Edit Exit Function：当前Shot为什么在这里结束并把注意权交给下一Shot
Cut Motivation：
Cut Trigger / Cut Timing：由`EDITORIAL_PLAN`拥有；当前Shot只继承相关边界
Shot Relation：CONTINUOUS_HOLD或真实CUT的相邻镜头关系；不得为丰富术语虚构
Information Gain：
Exit Visual State：
Director Target Duration：
Asset / Reference Implication：
```

### Minimum Necessary Fields
简单单人静态Shot可省略无关字段，但至少保留：
`Purpose + Focus Owner + Critical Read + Shot Size + Blocking/State + Camera Intent + Cut Motivation/No Cut + Duration`。Entry Camera Geometry / Lens / Focus / Stabilization / Shot Relation只在它们会改变叙事、空间可读性或执行稳定性时加入；运镜改变Geometry时由Camera Motion Contract补Landing Geometry。

---

## 10｜Cinematography Grammar + Camera Motion Contract

Stage 02先读取`cinematography_grammar.md`锁真正有因的Camera Position/View、Lens Family、Focus与Stabilization；随后再决定是否需要Camera Motion。它负责**导演意图**，不必把所有运动写成工程路径：
- `STATIC PRESSURE`
- `SLOW APPROACH`
- `SLOW WITHDRAWAL`
- `SUBJECT FOLLOW`
- `LATERAL REVEAL`
- `REVEAL TRAVEL`
- `COMBAT PURSUIT`
- `IMPACT WITNESS`
- `SUBJECTIVE INSTABILITY`（仅有叙事因果）

T3/T4或运动歧义明显时，Stage 02就建立初版`Camera Motion Contract`；Stage 04只精确到实际Panel路径，不重新发明导演意图。

---

## 11｜Editorial Grammar + Cut Motivation + Shot Relation

Sequence Arc锁定后，必须读取`editorial_grammar_engine.md`建立`EDITORIAL_PLAN`。先设计`Viewpoint Arc → Edit Function → Cut Trigger → Cut Timing → Continuity Strategy`，再确认Formal Shot数量；禁止先机械拆Coverage，再给每个镜头补一个理由。

每个明确CUT至少属于一种：
- `INFORMATION_CHANGE`
- `POWER_SHIFT`
- `EYELINE_REVEAL`
- `ACTION_LANDING`
- `REACTION_THRESHOLD`
- `SPATIAL_REORIENTATION`
- `RHYTHM_CONTRAST`
- `MATCH_ACTION`
- `TEMPORAL_ELLIPSIS`
- `TRANSFORMATION_REVEAL`

如果当前Shot的信息、权力、动作或视角没有发生值得切换的变化，默认优先保持原Shot。

`Cut Motivation`回答“为什么切”；`Cut Trigger / Cut Timing / Transition / Continuity Strategy`由Editorial Plan回答“具体何时、如何切”；真正CUT存在时再按`cinematography_grammar.md`记录`Shot Relation`（如ACTION→CONSEQUENCE / EYELINE MATCH / MATCH ON ACTION / WITHHOLD→REVEAL）。没有CUT写`CONTINUOUS_HOLD`。

**默认生产策略：** 视角切换优先通过多个Formal Shots分别生成，再在Stage 06组接，而不是要求一个Video Unit内部随机切换机位。只有`EDITORIAL_PLAN.editing_mode=IN_MODEL_MULTISHOT`且证据完整时，才允许Stage 05把多个子Shot编译进同一生成任务。

失败：`CUT_MOTIVATION_WEAK / MECHANICAL_SHOT_REVERSE_LOOP / SHOT_RELATION_CONFLICT / EDITORIAL_PLAN_GAP / CUT_TRIGGER_MISSING / EDIT_CONTINUITY_CONFLICT`。

---

## 12｜Dialogue Blocking（对白空间表演）

Actor Performance Brief确定Objective / Tactic后，重要关系Beat再回答：
- 角色是否靠近、退开、横切、背对、隔着障碍物；
- Listener是否在意义变化后改变身体朝向/距离；
- 是否通过占位而非微表情表达权力变化；
- Ongoing Physical Task如何自然限制走位。

禁止把所有对白关系只交给“表情变化 + 正反打”。

---

## 13｜Combat Spatial Directing（战斗空间导演）

Combat Design Brief必须追加：

```text
Engagement Distance Ladder：Entry → Threat → Weapon Reach → Contact/Near Miss → Exit
Spatial Dominance：谁占据中心/高位/出口/障碍区
Attack Lane：攻击线从哪里进入哪里
Defensive Escape Lane：防守者可退向哪里
Depth Strategy：敌我是否前后景错层
Contact Read Shot：哪一Shot必须看清接触点/险些命中
Initiative Shift Visual：主动权改变时构图/距离怎样改变
Combat Coverage Rhythm：Spatial Read → Compression → Commitment → Contact → Consequence（按需，不机械五镜）
```

战斗重要Shot若所有参战者始终同深度完整全身陈列，且没有策略原因，判`COMBAT_LINEUP_FAIL`。

---

## 14｜Montage Design Brief

Montage不能只是资产逐张展示。重要Montage记录：

```text
Montage Thesis：
Ordering Logic：升级 / 对照 / 扩散 / 收缩 / 因果链 / 空间扩张
Connection Device：动作匹配 / 形状匹配 / 声音桥 / 综合色 / 方向 / 意义对照
Information Gain Per Shot：每个Shot新增什么，而不是重复同一事实
Duration Rhythm：镜头长度是否加速/减速/保持
Scale Progression：个人 → 群体 → 城市 / 反向 / 其他
Return-to-Mainline Trigger：用什么镜头结束Montage并回主线
```

失败：`MONTAGE_PPT_FAIL`。

---

## 15｜Transformation Presentation Contract / Requirement Draft

首次/关键变身必须读取`transformation_splendor_architecture.md`。

- **已有Approved Transformation Splendor Profile**：Stage 02直接建立正式`Transformation Presentation Contract`；
- **首次设计尚未完成**：Stage 02只建立`Transformation Presentation Requirement Draft`，锁“观众必须看到什么”，不得预先虚构具体裙尾、材质、发饰或Weapon-Body Silhouette。

Draft / Contract至少记录：
- `Reveal Priority`：眼妆 / 发型 / 大轮廓 / 武器 / 身体线条 / 其他；
- `Pre-Transformation Visual Baseline`；
- `Pre-Transformation Injury Snapshot / Recovery Eligibility`；
- `Transformation Completion Recovery Result / Post-Recovery Injury State`；
- `Required Visual Level Gap`；
- `Required Silhouette Read`；
- `Musical Eye Motif Read`：是否需要MCU/CU；
- `Material Read Requirement`；
- `Weapon-Body Icon Requirement`；
- `Hero Angle / Hero Distance Intent`。

Stage 03实际TF / TH / TC / TE / WP Approved并形成Splendor Profile后，由`director_spatial_reconciliation_gate.md`执行`TRANSFORMATION PRESENTATION RECONCILED`，再把Draft收敛为真实Presentation Contract。

失败：`TRANSFORMATION_PRESENTATION_FLAT_FAIL`。

---

## 16｜Motion Priority

AI视频复杂Shot必须明确一个主要驱动力：
- SUBJECT
- OPPONENT
- CAMERA
- ENVIRONMENT
- VFX

其他层可以运动，但不能全部同等抢主运动。Motion Priority用于Stage 04/05降低动作与Camera同时失控。

---

## 17｜Stage 02 Hard Gates

以下任一未解决，不得宣布`DIRECTOR CORE LOCKED`：
- `STAGING_DISTANCE_FLAT_FAIL`
- `SCREEN_DIRECTION_FAIL`
- `EYELINE_CONTINUITY_FAIL`
- `AXIS_CROSS_UNMOTIVATED`
- `CRITICAL_VISUAL_READ_FAIL`
- `VISUAL_HIERARCHY_FLAT_FAIL`
- `SHOT_PROGRESSION_FLAT_FAIL`
- `CUT_MOTIVATION_WEAK`
- `MECHANICAL_SHOT_REVERSE_LOOP`
- `COMBAT_LINEUP_FAIL`
- `SPATIAL_DOMINANCE_UNREADABLE`
- `CRITICAL_OCCLUSION_FAIL`
- `MONTAGE_PPT_FAIL`
- `TRANSFORMATION_PRESENTATION_FLAT_FAIL`

Director Core正确的产物不是“Shot很多”，而是：**每个Shot为什么这样站、这样看、这样近、这样切，都有戏剧与空间理由。**

随后必须完成`previsualization_strategy_router.md`与`asset_consolidation_sufficiency_audit.md`。只有每个有效Segment已有完整Shot Storyboard Coverage Contract，且无`MANDATORY_SHOT_STORYBOARD_NOT_PLANNED / SHOT_STORYBOARD_COVERAGE_GAP / STORYBOARD_FALSE_CUT_FAIL / STORYBOARD_EVIDENCE_INSUFFICIENT / PREVIS_REDUNDANCY_FAIL / PREVIS_DIRECTOR_AUTHORITY_BLEED`，再加上无`ASSET_CONSOLIDATION_NOT_RUN / ASSET_SUFFICIENCY_GAP / ASSET_REQUIREMENT_DUPLICATION_CONFLICT`，Stage 02才可标记`DIRECTOR BREAKDOWN READY`。

## V4.5｜Shot Relation Graph（相邻镜头关系必须先于资产派生）

> **新增硬原则：** 不能只证明“每个Shot各自合理”；每一对相邻Shot还必须证明“为什么是这个下一个Shot”。关系事实的结构化载体为`state/shot_relation_graph.schema.yaml`。

在`DIRECTOR CORE LOCKED → DIRECTOR BREAKDOWN READY`之间，对Episode真实Shot顺序建立`SHOT_RELATION_GRAPH`。每个相邻Shot至少记录：

- `from_shot_id / to_shot_id`；
- `relation_type`：例如CONTINUITY_CUT / ACTION_CONSEQUENCE / EYELINE_MATCH / LOOK_POV_REVEAL / **CLUE_REVEAL_CUT** / MATCH_CUT / SOUND_BRIDGE / PARALLEL / CONTRAST / ELLIPTICAL / HARD_LOCATION_CUT；
- `cut_motivation`：为什么此刻必须切到这个对象/空间；
- `narrative_attention_target`：前镜头离开前观众注意力必须落在哪里；
- `source_visual_fact / destination_visual_fact`：A端必须被看见什么，B端必须立即证明什么；
- `shared_entity_ids / world_relations`：若是同一地点、同一建筑由外到内、A地点可看见B地点等，必须显式记录；
- `bridge_requirements`：SOURCE_CLUE_VISIBLE / DESTINATION_IDENTITY_PROVEN / LOCATION_RELATION_PROVEN / EXIT_ENTRY_PAIR_ALIGNED等；
- `forbidden_interpretations`：禁止模型误读成什么，例如“右侧近窗直接变成机械结构”。

### CLUE_REVEAL_CUT
若A镜头通过一个线索把观众引向B镜头，必须满足：

`A中线索可读 → Attention Target锁定 → B为该线索真实对象/内部/后果 → 关系能由静态资产证明`

只写“推向窗”“切到钟楼”不够；必须明确**哪扇窗、窗外/远处什么对象、B与该对象是什么关系**。若关系需要当前不存在的特定视角，Stage 02必须派生Visual Asset Obligation，而不是让Stage 05自行猜。

### Hard Gates
- `SHOT_RELATION_GRAPH_GAP`
- `CUT_MOTIVATION_UNBOUND`
- `NARRATIVE_ATTENTION_TARGET_AMBIGUOUS`
- `LOCATION_RELATION_UNPROVEN`
- `ARBITRARY_VISUAL_CHANGE_FAIL`

没有Locked Shot Relation Graph，不得宣布`DIRECTOR BREAKDOWN READY`。

## Current｜Perception-First Detailed Shot Contract Extension

在`Sequence Arc + Editorial Intent Draft`之后，Formal Shot锁定前增加以下顺序，**不得反过来先选Lens/Shot Size**：

`UNRESOLVED_STATE → RELATIONAL_PRESSURE → VIEWPOINT_ROLE → CAMERA_ETHICS → ATTENTION_FLOW → SHOT_SCALE_JUSTIFICATION → CAMERA_GEOMETRY/LENS → VISUAL_FORCE_STACK → VISUAL_SALIENCE_BUDGET → INFORMATION_DELTA → CUT`。

每个Detailed Shot Contract新增最小字段：

```text
Camera Ethics：
Attention Flow：Entry / Resistance / Decisive Landing / Residual / Exit
Shot Scale Justification：Required Information / Why Wider Fails / Why Closer Fails / Spatial Cost / Narrative Gain
Camera Placement Justification：Physical / Narrative
Composition Mechanism：Primary / Optional Secondary
Visual Force Stack：1 Primary + <=2 Supporting
Visual Salience Budget：Primary / Secondary / Ambient / Suppressed / Mundane Area
```

其中Close-up理由、Camera双重合法性、Visual Force上限属于Hard Gate；跨镜头重复只由Telemetry发Warning。

`DIRECTOR CORE LOCKED`新增前置：`DIRECTOR_PERCEPTION_PASS=YES`。失败只重开受影响Shot/Sequence，不返回Stage 01。
