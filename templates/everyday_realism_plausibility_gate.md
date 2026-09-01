# Everyday Realism & Plausibility Gate｜日常现实性与合理性全局闸门

> **用途：** 除剧本明确声明的变身、战斗、超自然、梦境、幻觉或象征化镜头外，《断弦之歌》所有普通剧情视觉资产默认必须符合现实世界的空间功能、建筑/车辆结构、人体工学、物件用途、社会空间、日常物理与连续性。漂亮、综合色正确、角色身份正确都不能抵消明显不合理。

> **总原则：** `REALISM_REQUIRED BY DEFAULT`。奇幻世界只豁免被Canon明确改变的局部规则；没有“因为作品有超自然元素，所以普通车厢/餐馆/人物坐姿也可以不现实”的全局豁免。

## 1｜Realism Baseline

普通剧情默认启用八个现实维度：

1. `ENVIRONMENT_FUNCTIONAL_REALISM`：空间首先要能完成其现实功能；
2. `ARCHITECTURAL_REALISM`：房间、门窗、楼梯、通道、尺度、连通关系基本成立；
3. `VEHICLE_REALISM`：车辆内部结构、驾驶控制区、乘员区、出入口、视野、通道与容量符合具体车辆类型；
4. `HUMAN_ERGONOMICS`：站、坐、走、转身、Reach、支撑、身体与家具关系可成立；
5. `OBJECT_AFFORDANCE`：物件真的能被其现实用途使用，开合/抓握/放置/通行空间成立；
6. `SOCIAL_SPATIAL_PLAUSIBILITY`：普通人在当前关系与任务下的位置、距离、朝向、交流条件不反常；若反常必须有剧情原因；
7. `MUNDANE_PHYSICS`：重力、支撑、湿度、破损、光源、惯性、因果等普通物理不无因违背；
8. `MUNDANE_CONTINUITY`：人物/座位/物件/湿度/门窗/车辆状态等不因CUT或新图无因重置、瞬移或变位。

## 2｜检查顺序：先现实，再美术

任何人物进入Environment的正式资产，按以下顺序判断：

`SOURCE FACT → FUNCTIONAL/SPATIAL REALITY → HUMAN OCCUPANCY → AFFORDANCE/PHYSICS → SOCIAL/BEHAVIORAL PLAUSIBILITY → CONTINUITY → VISUAL QUALITY`

前六层存在P0/P1失败时，禁止因为“构图好看、氛围漂亮、人物脸对”而APPROVE。

**Hard Rule：** A visually attractive asset that is physically, functionally, ergonomically, architecturally, socially, or causally implausible MUST FAIL unless a scoped Canon exception explicitly authorizes that exact dimension.

## 3｜Source Logic 与现实解释

先区分三种事实：

- `EXPLICIT_SOURCE_FACT`：小说/锁定剧本明确规定；不能为生成便利静默修改；
- `DERIVED_REALISTIC_RESOLUTION`：Source没有写死，可按现实常识选择最自然、最少新信息的解，并登记；
- `OPEN_STORY_SIGNIFICANT`：不同现实解会改变剧情意义、人物关系或关键信息，必须返回Director/User裁决。

现实性Gate不能用“现实里通常怎样”覆盖明确Canon；但若Canon本身包含超现实机制，只放宽该机制真正影响的维度。

## 4｜Environment Functional Realism

Environment不是漂亮盒子。生成前必须回答：

- 这个地点/设施到底是什么类型，核心现实用途是什么；
- 人如何进入、离开、工作、坐下、通行；
- 固定家具/设备是否留出必要操作空间；
- 出入口是否被无因堵死；
- 关键功能Zone之间是否可以真实到达；
- 空间容量与人物数量是否基本相容。

若Visual Asset为了构图重新发明一个功能完全不同的空间，判`ENVIRONMENT_FUNCTIONAL_REALISM_FAIL`。

## 5｜Architectural Realism

室内/建筑至少检查：

- 门位于可连接的墙/边界并确实通向相邻空间；
- 窗位于合理外墙/采光面，不无因通向室内别处；
- 楼梯/坡道有真实去向和足够通行空间；
- 房间尺度、层高、家具尺寸与成年人体比例基本可信；
- 门开启、床边、桌椅、柜门、走道等保留基本使用净空；
- Floor Plan / Room Layout与派生画面不互相否定。

不要求建筑法规毫米级合规，但明显“现实中无法使用/无法建成/尺度荒谬”的设计不能进入Canon。

## 6｜Vehicle Realism Profile

`VEHICLE`必须作为独立Location Kind处理，不再默认当普通`ROOM_LAYOUT`。

先明确`vehicle_type`，再建立`VEHICLE_LAYOUT`，至少锁：

- `DRIVER_CONTROL_ZONE` / 驾驶视野与控制件；
- Passenger Seating / 乘员座位朝向与容量；
- Entry / Exit；
- Aisle / Circulation；
- Front / Rear / Left / Right；
- 外部大致尺寸与内部容量是否相容；
- 当前年代/车型的基本结构常识。

若剧本规定“驾驶位 + 前乘客位 + 后排”，生成图不得无因改成“司机 + 两侧纵向公共交通长椅”。这属于`VEHICLE_FUNCTIONAL_LAYOUT_DRIFT`，不是艺术自由。

## 7｜Human Occupancy & Ergonomics

每个普通人物进入空间后至少检查：

### Cast Cardinality
- Expected人物数与Observed人物数一致；
- 非群众镜头默认禁止额外陌生人；
- 同一角色没有无因重复。

### Zone / Functional Position
- 每个角色位于其剧情/Spatial Canon要求的Zone或座位；
- 驾驶员在驾驶位，前乘客不被无因挪到后舱；
- 若人物换位，World State必须存在Move/Transition来源。

### Support / Contact
- 坐姿：骨盆/身体有真实座椅支撑，腿脚有合理空间；
- 站姿：脚与地面/支撑面关系成立；
- 靠、扶、抓、拿、开门等接触不悬空、不穿模；
- 身体不穿越扶手、墙、座椅、桌面或车体。

### Clearance / Reach
- 人能从当前位置到达门、通道、设备或目标物；
- 狭窄空间内转身、通过、坐起等动作有基本净空；
- 人体尺度与空间尺度基本一致。

明显失败分别登记`CAST_COUNT_MISMATCH / CHARACTER_ZONE_ASSIGNMENT_FAIL / HUMAN_ENVIRONMENT_INTERSECTION_FAIL / ERGONOMIC_SUPPORT_FAIL / HUMAN_SCALE_IMPLAUSIBLE / GEOMETRY_REACH_CONFLICT`。

## 8｜Object Affordance

道具与环境物件不只“看起来像”。必须能完成其用途：

- 门/窗/抽屉有可操作方向与开启空间；
- 椅子能坐、桌面能放物、吧台后能工作；
- 驾驶控制件在驾驶员可达范围；
- 杯、伞、工具、武器等尺寸/握持/支撑符合当前用途；
- 若物件因剧情异常使用，必须由Action/Canon明确授权。

明显无法使用判`OBJECT_AFFORDANCE_FAIL`。

## 9｜Social-Spatial Plausibility

普通剧情先问“正常人在这个情境下会不会这么站/坐”，再讨论电影化Blocking。

至少检查：

- 正在低声交流的人是否拥有合理交流距离/视线/听觉条件；
- 一起行动的人是否无因分散到极远位置；
- 陌生/敌对/亲密关系造成的距离变化是否有剧情依据；
- 角色任务是否允许当前朝向与位置；
- 若选择明显反常位置，必须存在`behavior_reason_ref`或导演意图。

这不是要求所有人靠很近；“疏远、戒备、躲避、监视、权力距离”都可成立，但必须是剧情可解释的选择。无理由反常判`SOCIAL_SPATIAL_IMPLAUSIBILITY`。

## 10｜Mundane Physics & Causal State

普通物理遵守`CAUSE → VISIBLE EFFECT`与`NO CAUSE → NO RANDOM EFFECT`：

- 雨水、湿衣、泥、血、破损、烟雾、碎玻璃等必须有来源；
- 已有来源的湿度/污渍/破损不能下一张无因消失；
- 普通重力、支撑、惯性、摩擦、承重不随图片重置；
- 灯光变化若来自灯灭/火焰/雷光，应同步World State；
- 普通场景不得无因出现“更有氛围”的异常污染。

## 11｜Mundane Continuity

普通连续动作/相邻Shot中：

- Character Zone / Seat / Left-Right不无因改变；
- Holder / Prop Location不无因改变；
- Door / Window / Vehicle Motion不无因Reset；
- Wetness / Dirt / Damage不无因Reset；
- Ongoing Task不因CUT消失。

如果改变发生在省略时间段，必须有合法`INTENTIONAL ELLIPSIS`且新状态不与已知事实冲突。

## 12｜Scoped Realism Exception

只允许以下显式例外类型：

`TRANSFORMATION / COMBAT / SUPERNATURAL / DREAM / HALLUCINATION / SURREAL / SYMBOLIC`

每个Exception必须写：

- `exception_id`；
- `exception_type`；
- 精确`scope`（Scene/Event/Shot/Asset）；
- `allowed_categories`；
- `reason`；
- 必要时`canon_mechanic_ref / approval_ref`。

**Exception只豁免列出的维度。**

例如战斗可以暂时放宽普通人体速度，但：门仍应在真实墙上、地面仍有支撑、未被魔法影响的椅子仍应能坐。变身可以改变身体/服装形态，但旁边普通车辆不能因此无因换内部布局。

禁止：`THIS_IS_FANTASY_SO_REALISM_OFF`。

## 13｜Asset Logic Reconciliation Loop

发现明显不合理时，禁止继续下游，也禁止先随机重抽。按Owner回查：

1. `SOURCE`：小说/Screenplay是否明确要求该事实；
2. `REALISM_CONTRACT`：当前普通现实解是否已锁；
3. `SPATIAL_CANON`：Location/Zone/Seat/Access/Vehicle Layout是否本身合理；
4. `WORLD_STATE`：人物/物件是否有合法进入、换位、状态来源；
5. `ASSET EXECUTION`：生成图是否违反正确的上游事实；
6. `VISUAL_EVIDENCE`：Observed事实是否真实，是否只是Prompt/文件名声称。

### 自动处理

- Source未写死、只是Derived且明显不现实 → 自动Patch最小`REALISM_CONTRACT / SPATIAL_CANON`，重算受影响资产；
- Source与Spatial/Realism Contract正确、图片错误 → Reject该Candidate，生成最小修正版；**禁止修改Canon迁就图片**；
- 只有局部手/接触错误且整体空间成立 → Local Patch；
- 不同合理解会改变剧情意义/人物关系 → `ASK_REQUIRED / STORY_SIGNIFICANT`；
- 任一P0/P1未解决 → 不得进入Storyboard/Video Conditioning/Video。

## 14｜Text-only Controller

纯文本模型不能自己观察现实性，但可以消费Current `VISUAL_EVIDENCE.observed.realism`：

- Evidence为PASS且Fingerprint Current → 可继续；
- Evidence为FAIL → 必须执行Reconciliation；
- Evidence为UNKNOWN/MISSING而当前资产承担P0/P1现实性证明 → 加入`VISUAL_REVIEW_QUEUE`，禁止猜；
- 原Prompt写“真实、合理、前乘客位”不等于实际图片做到。

## 15｜Freeze Gate

普通剧情资产在`EPISODE ASSET FROZEN`前必须满足：

- 适用的`REALISM_CONTRACT`已LOCKED；
- Current Visual Evidence已覆盖P0/P1现实维度；
- Cast数量/身份/Zone/功能位置无冲突；
- Environment/Architecture/Vehicle/Human/Object/Social/Physics/Continuity没有未豁免FAIL；
- 所有Exception是局部、有原因、可追溯；
- 根因未解决的P0/P1不允许被“用户还没发现”或“先做视频看看”绕过。

## 16｜一句话

> **除剧情明确要求不现实的那一小块之外，其余一切按现实世界运行；先证明“现实中成立”，再讨论“电影里好看”。**


## V4.5.6｜Logic Integrity Closure

### 1. Contract lifecycle
`REALISM_CONTRACT`正常生命周期固定为：
`DRAFT → QC_PASS_WAITING_APPROVAL → LOCKED`。
Planning QC只检查内容正确性，不要求提前LOCK；用户批准后才LOCK。`REVISE_REQUIRED`不得进入Build。

### 2. Reality Coverage by default
任何普通`IMAGE`正式资产必须显式记录：
- `realism_applicability: REQUIRED | SCOPED_EXCEPTION | NOT_APPLICABLE`；
- REQUIRED/SCOPED_EXCEPTION必须有`realism_contract_ids`；
- NOT_APPLICABLE必须有可审计理由；
- 缺字段/UNKNOWN在V4.5.6正式生产中是Fail，不是“默认跳过”。

### 3. Scoped Exception不可借用
`realism_exception_ids`只是Asset声明“我要使用哪个已存在Exception”，不是授予权限。真正豁免必须同时满足：Exception存在、Category被允许、当前Asset/Shot/Event/Scene命中Scope。任何一项缺失都按普通Reality Baseline执行。

### 4. Fine-grained observed facts override summary
具体视觉事实优先于大类结论。例如：
- `driver_forward_visibility: FAIL`时，即使`VEHICLE_REALISM: PASS`也必须Fail；
- `functional_layout_plausibility: FAIL`时，`overall_verdict: PASS`不能覆盖；
- 人物Zone/Seat/Support/Access Path等具体冲突同理。

### 5. Reality Basis / Provenance
Reality Contract必须声明事实依据。普通常识可用`COMMON_KNOWLEDGE_OK`；历史车型、时代建筑、专业机械、医疗/工业等若需要专业事实，标记`REFERENCE_REQUIRED`并保存已验证Reference。模型“觉得像这样”不能直接LOCK成Reality Canon。

### 6. Stage closure
现实性不是Stage 03一次性检查。新的Storyboard Panel、Video Conditioning Frame、Video Reference Pack和实际Video Take都可能重新引入座位漂移、穿插、车辆重构、物理错误，因此各阶段必须重新产生自己的Reality PASS。
