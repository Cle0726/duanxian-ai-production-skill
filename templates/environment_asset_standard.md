# 03.2｜场景资产标准模板

> **V4.5.2 Current Rule：场景采用 Script-Grounded Virtual Set → Spatial Canon → Clean Canon → Event/Relation/Predictive Coverage。** 重要/复用地点在生成Hero图之前先把剧情Event Node落到Topology / Floor Plan / Zone / Door-Window / Sightline / Access与Character Event Route；空间确认后每张派生图仍必须回指Spatial Parent，不允许“先做一张平面图，后面又各画各的”。角色资产规则不受影响。

## 1. 资产定位
Environment Master用于锁定“这个地方到底长什么样、门窗在哪里、人物怎么走”，不是只追求气氛漂亮的单张背景。

Stage 03必须同时读取 `shot_coverage_asset_derivation.md` 与 `color_script_derivation_engine.md`。正式顺序为：**Scene Inventory / Event Nodes → Reuse Tier → Spatial Canon（室外Topology；室内Floor Plan/Zone/Anchor；跨地点Sightline/Access）→ Spatial QC/Approval → Scene Color Extension → 一张正式高清Clean Hero Environment Master → 根据真实Event/Shot Coverage倒推必要视角。** Color Card负责综合色，不依赖先有场景母图；Environment Master再按已锁综合色生成，避免“先随便出场景、再用色卡追着改”的循环。


## 1.1｜Empty Environment Master Hard Rule（V4.5.7）

任何被Formal Scene / Event Node / Formal Shot实际使用的真实Location或Sub-location，**Tier S/A/B/C一律必须先有一张Approved空场景Clean Master**。Tier C只减少Spatial Planning与Derived Coverage，不豁免Base Master。

空场景母图要求：
- 无可读人物、无群众、无一次性表演；
- 无临时剧情动作或临时持物状态污染；
- `transient_content_policy=CLEAN_CANON`；
- `population_policy=EMPTY_ENVIRONMENT_ONLY`；
- 锁空间身份、固定结构、固定家具、材质、综合色与基础主光；
- 同一`location_entity_id`按`reuse_key`复用，不因换Shot重复生成新的Master。

白描Storyboard、Shot Assembly、人物在景中的Execution Frame都不能替代这张空场景母图。

## 2. Environment登记（场景资产台账）
- ID（保留已有ID；无ID时才建议ENV-*）
- 名称 / Parent Location（所属大地点） / Sub-location（子空间）
- Version（版本） / Status（状态）
- Era（时代） / Region（地区）
- Geometry / Geography Spec Ref（空间结构）
- Entrances / Exits（入口 / 出口）
- Walkable / Action Space（人物可以走动/打斗的区域）
- Key Landmarks（稳定地标）
- Materials（材质）
- Base Lighting（基础主光方向）
- Global Color DNA Ref（全局综合色DNA）
- Scene Color Extension Spec / Card Ref（场景综合色扩展；如适用）
- Camera Axis / Primary Shooting Hemisphere（适用时）
- Blocking / Zone Map Ref（L2/L3需要时）
- State Variants（持续状态变体）
- Master Prompt（母图提示词） / Approved Canon Master（已批准正式场景主图）
- Derived Coverage Views（由哪些Shot触发、Parent Master、版本/状态）

- Production Support Reference不属于Environment Canon视角集；若空间Canon已定但当前多人接触/精确Shot组合仍高风险，路由到`production_support_reference_engine.md`，不要继续堆Environment Coverage。

## 3. 大型地点拆分
按生产需要拆外部、室内、舞台、后台、走廊、车辆内部等真实子空间，不允许一个模糊地点名承担所有空间关系。


## 3.5｜Spatial Canon Preflight（先搭Set，再画场景）

Environment不是“一张背景图”，而是可反复取景的Set。正式生成Environment视觉资产前，先按Reuse Tier建立最小充分空间Canon：

- `Tier S`核心长期Set：Topology/Floor Plan、Zone、Door/Window、Entry/Exit、Sightline、Access、Elevation、Recurring Camera-safe Views；
- `Tier A`多集复用：Layout + Major Relations + Required Sightline/Entry/Exit；
- `Tier B`单集多镜：Minimal Layout + Event Nodes真正使用的Zone/Anchor；
- `Tier C`一次性过场：只锁当前Shot不可省略的空间关系，不机械建全屋；**但仍必须生成一张空场景Clean Master**。

结构化Owner为`state/spatial_canon.schema.yaml`，运行时投影为`SPATIAL_CANON_RUNTIME`。规划图可有房间ID、门窗ID、北向、路线和箭头，因为它是Planning Diagram；它不得自动成为Storyboard/First Frame/Video Primary Visual。

**空间事实优先：** “钟楼在哪边、哪扇窗能看见、门通向哪里、楼梯往哪层”先在Spatial Canon解决，禁止用后续漂亮图片反向猜这些事实。


## 3.6｜Planning Diagram Standard（室外拓扑 / 室内平面）

Spatial Canon需要人类可快速审核的Planning Diagram。它是工程图，不是成片Reference：

### Outdoor Topology Diagram
至少按当前剧情所需显示：
- Location / Event Node；
- 北向或稳定方向基准；
- 节点连接与Character Event Route；
- 距离或Distance Class；
- 上坡/下坡/高差；
- 关键遮挡、河流/林线/道路等边界；
- Sightline / Landmark Relation（剧情需要时）。

### Building Floor Plan / Room Layout
至少按当前剧情所需显示：
- Room / Zone；
- Door / Window / Stair / Entry / Exit；
- 房间连接；
- 角色跨Event Node的进入/离开路径；
- 关键Sightline与Camera-safe区域（需要时）。

Planning Diagram允许ID、文字、距离、箭头和路线，因为这些是结构证据；它必须登记`layout_type=PLANNING_DIAGRAM`、`direct_input_allowed=false`、`primary_visual_eligible=false`。

**Cascade Lock：** Required Planning Diagram未QC/批准，禁止批量生成依赖它的Environment Clean Canon / Event View / Coverage。

## 3.7｜Character Event Route（人物完整动线）

对追逐、逃亡、跨房间移动、重复进出等剧情，不能只登记`A ADJACENT B`。必须建立`CHARACTER_EVENT_ROUTE`：Actor Group、Event Node顺序、Location/Zone/Anchor、移动方式、距离/坡向（已知时）与所依赖Spatial Relation。

`Event Node`必须能够回答“人物此刻在哪里、从哪个门/路径来、下一事件去哪里”。导演Blocking可以改变表演节奏，但不得凭空改变Locked World Route。

## 4. Canon Master + Geography Spec

### 4.1 Scene Color Preflight → Hero Environment Master
先读取Stage 02已经派生的`Scene Color Extension Spec`。若`Scene Color Extension Card Need=YES`且尚无Approved Card，先由Global Color DNA + Scene Spec生成/批准该Card；若Need=NO，直接使用文字Spec。然后每个真实子空间原则上做**一张正式高清Hero Master**。视角选择最能解释空间的正向/3/4/Establishing方向；不要求机械“正面”，但必须清楚锁定空间身份、尺度、主地标、出入口关系、材质与基础主光。

### 4.2 Geography / Blocking
Hero Master不再承担“首次发明空间”的职责。门窗、固定家具/舞台/柜台/楼梯、可行走区、关键距离、人物进出路径和Sightline首先来自已批准Spatial Canon；Hero Master只把这些事实视觉化并用于材质/设计复核。

Hero Master批准后用真实材质/空间信息对Stage 02的`Scene Color Extension Spec`做一致性复核：默认只补充已被正式资产证明的Material Family，不反向用母图随机综合色改写既有Color Authority。若发现Spec与Approved Canon/剧情事实有P0冲突，回到综合色派生做最小修正并按Change Impact复查；不存在冲突时保持原Spec/Card。

- `L1 Single-View / Low Continuity`：通常Hero Master + 简短Geography Spec即可覆盖固定空间结构；但若该短Shot本身存在高价值静态歧义，仍按Video Risk Matrix判断是否需要局部Coverage或Production Support，不因L1自动豁免；
- `L2 Blocking-Critical`：根据真实Shot需要建立最小Blocking/Zone Map与少数Coverage View；
- `L3 Hero / Recurrent Set`：核心反复场景才建立更完整Blocking Map与更广Coverage，但仍必须由真实镜头/长期复用需求证明。

**Spatial Canon before image, Geography before coverage。** 一张图看不到的空间先用结构化Geometry锁，不直接靠AI从新角度自由猜。

## 5. Derived Coverage View（场景衍生覆盖视图）
仅由Stage 02 Environment Shot Coverage触发：
- 对话明确Reverse / OTS；
- 门口/窗边/柜台/舞台等固定锚点反拍；
- 人物从入口走到目标位置；
- 追逐/战斗跨Zone；
- 同一空间跨Segment使用且机位半球明显变化；
- 镜头近距离拍到Hero Master不可读的固定结构。

Coverage示例：`REVERSE / SIDE / DOOR_SIDE / WINDOW_SIDE / COUNTER_TO_ROOM / STAGE_TO_AUDIENCE / STAIR_TOP / STAIR_BOTTOM`。

每张Coverage必须：
- 回指Approved Parent Master；
- 回指Triggered By Shot(s)；
- 保持同一门窗、地标、尺度、轴线与材质；
- 只扩展当前拍摄方向，不重设计空间。

**禁止为了“保险”机械制作360°。**


## 5.1｜Reciprocal / Predictive Set Coverage

Coverage不只是“换角度”。当剧情或空间关系需要时，必须从Event/Relation派生：
- `FORWARD_VIEW`：A看向B；
- `REVERSE_VIEW`：B方向反打A或同一空间反向；
- `LOOK_BACK_VIEW`：人物经过节点后回望来路；
- `ENTRY / EXIT_VIEW`：明确门/路径与下一个Zone；
- `LANDMARK / CLUE_VIEW`：建立叙事地标；
- `PREDICTIVE_COVERAGE`：根据后续已知Scene/Shot需求一次性准备高复用机位。

不要求机械成对或固定九宫格；只有`WHY_REQUIRED`能够由Event、Shot、Relation或长期复用证明时才生成。

### 双Parent派生
所有正式Coverage建议同时登记：
- `Spatial Parent`：SPATIAL_CANON / Floor Plan / Topology，锁Geometry；
- `Visual Parent`：已批准Clean Canon或Key Event View，锁材质、美术、综合色。

缺任一Parent而需要模型从新角度重新发明空间或美术时，不能批准为同一Set Coverage。

## 6. State Variant（场景持续状态变体）
NORMAL → ATTACK / AFTERMATH等仅改变授权的持续状态，不重建设计空间。

天气/时间通常只是Condition，不自动变成新的Environment identity；但若它们导致当前地点长期/多镜出现显著综合色差异，则在同一Environment identity下派生`Scene Color Extension`或`Shot Lighting Variant`，不新建地点。

**Color Variant ≠ Environment Identity Variant。**

**Environment Master ≠ Runtime Environment State。** 门开、灯灭、玻璃破碎、烟雾/水/散落物/群众流向等先由World State Ledger持续记录；只有持续跨大量镜头且结构复杂、仅靠Prompt难稳定时才升级正式State Variant。

## 6.1 Clean Set / Transient Entity Separation（长期场景与临时剧情状态分离）
Canon Master优先建立`ENVIRONMENT_CLEAN_CANON`：锁Geometry / Landmark / Permanent Fixture / Material / Base Lighting，不把当前剧情临时状态烤进地点身份。

默认不得进入Clean Canon的内容：
- 临时顾客、路人、剧情人物、一次性群众；
- 当前镜头打碎的杯子、临时散落物、血迹、尸体、烟、火、爆炸VFX；
- 当前剧情造成的门窗破坏、家具倒塌、临时水渍/污渍；
- 仅当前Scene成立的天气/特殊灯光（除非它被明确锁为地点长期Canonical状态）。

固定招牌、建筑结构、永久家具、长期装饰属于地点Canon。剧情临时内容进入`World State / Scene State Variant`，在Storyboard之后由`video_conditioning_asset_architecture.md`合成进Shot Execution Frame。

**UNSCRIPTED TRANSIENT ENTITY = HARD FAIL：** 若Shot/Scene要求空场，Environment Clean Canon却出现非结构性顾客/路人/剧情人物，不能因为“氛围不错”批准。

## 7. Prompt结构
### Canon Master
- 资产目标
- 世界/时代位置
- 空间身份与核心几何
- 尺度
- 材质
- 基础综合色/主光（由Global Color DNA + 当前Scene Color Extension派生，不机械套用其他Scene色卡）
- 稳定地标与出入口
- Hero View要求
- 高风险限制

### Derived Coverage View
- Parent Master
- Triggered By Shot(s)
- Camera Side / Zone
- 必须看见的固定地标/出入口
- 与Parent Master一致的空间几何
- 当前Condition（如有，但不得污染identity）
- `DO NOT REDESIGN`锁

## 8. QC（场景质检）
- Hero Master是否先清楚定义空间，而不是一开始就堆多视图？
- Spatial Canon是否已先锁定Topology/Floor Plan/Zone/Anchor/Sightline/Access？
- 室外/跨区域剧情的人物完整Character Event Route是否成立，距离/坡向/节点顺序是否一致？
- Required Planning Diagram是否真实存在并已批准，而不是只有文字声称Topology完成？
- Geography / Entrances / Exits / Action Space是否与Spatial Canon一致？
- 是否先跑过Environment Shot Coverage？
- 每张新增Coverage是否能回指真实Event/Shot/Relation与具体摄影方向？
- Coverage是否同时继承正确Spatial Parent与Visual Parent？
- 需要反打/回望/地标关系时，Reciprocal Coverage是否已按真实需求派生？
- Predictive Coverage是否由未来已知镜头/高复用需求证明，而不是为了凑固定宫格？
- 多视图是否严格同一Geometry，而不是“风格类似的另一个房间”？
- 是否存在无镜头依据的360°补图？
- World（世界观是否对）
- Style（画风是否对）
- Continuity（前后连续性是否对）
- Coverage View是否错误承担Storyboard构图职责？
- Clean Canon是否混入临时人物/群众/剧情道具/破坏状态？
- 可见临时实体是否有World State/Scene State来源，而不是被烤进Parent Environment？

## V4.5｜Location Relation / Sightline Asset（地点之间也有Canon关系）

Environment Canon除了“地点自身是什么”，对反复出现或叙事关键的地点关系还必须维护：
- `VISIBLE_FROM`：A的哪个Zone/窗口/门口能看到B的哪个识别面；
- `EXTERIOR_INTERIOR_SAME_ENTITY`：外部建筑/钟面/内部房间属于同一Location Entity；
- `SAME_LOCATION_DIFFERENT_LAYER / CONTAINS / ADJACENT`等。

只有当真实Shot Relation需要时才生成关系型Coverage，不为所有地点做全量世界地图。

若Director要求“从餐馆深处看见某建筑线索，然后切入该建筑内部”，普通餐馆Hero Master + 建筑内部Design Board不能自动证明关系；必须存在最小充分的`ENVIRONMENT_COVERAGE`，并用`coverage_reason_codes=CLUE_REVEAL / LOCATION_VISIBILITY / LOCATION_IDENTITY`声明它证明的关系。

关系资产仍从Approved Parent Environment与Geography推导，不允许为了配合Cut重新设计一个“像是同地点”的假视图。

## V4.5.4｜Required View Set不是“多生成几张”

重要场景完成Topology/Floor Plan后，按本集所有Event/Shot/Relation建立`view_requirements`。每个方向必须有明确Camera Origin、Optical Axis和Must See Anchors。Environment Master只锁Set身份；它不能自动满足未被实际拍到的Reverse/Forward/Entry/Window-side方向。

跨多个Scene时逐Location汇总Required View，再用`view_coverage_planner.py`形成最小缺口队列。已有Asset只有在绑定Requirement且视觉Evidence证明实际方向/Anchor成立时才算Coverage；文件名叫“正视角”或Prompt写“正视角”均不计。

## V4.5.5｜Functional Reality Before Visual Beauty

Environment进入视觉生成前必须读取`REALISM_CONTRACT`。普通地点先回答“现实中能不能用”，再回答“画面好不好看”。

- `location_kind=VEHICLE`时不得继续用普通Room逻辑代替车辆结构；必须有具体Vehicle Type与`VEHICLE_LAYOUT`，锁Driver Control Zone、Passenger Zones、Entry/Exit、Aisle/Circulation、Front/Rear与容量。
- Restaurant / Residence / Workplace等功能空间必须保留其现实使用净空、出入口与操作区；视觉构图不得为了对称/人物展示堵死门、抹掉前乘客位或扩大内部到与外部尺度明显不相容。
- 派生Coverage继承的不只是Spatial Parent / Visual Parent，还继承适用`realism_contract_ids`。新的角度不得把同一Set改造成另一种功能布局。
- 多人物Environment Candidate只有在人物数量、Zone/Seat/功能位置、支撑与空间容量符合Contract时才可作为Approved Coverage/Assembly。

失败优先级：先判断Spatial Canon / Vehicle Layout是否本身错误；若上游正确而图片错误，Reject Candidate并只重生当前视角，不为迁就图片改Canon。

## V4.5.7｜ENV_VISUAL_ANCHOR_SET / Nearest Visual Parent（新增）

场景不采用机械正/背/侧多视图，而采用**Spatial Canon + Visual Anchor Set**：
- `ENV_VISUAL_ANCHOR_SET`只收真实会成为摄影方向的Anchor View；
- 每个Anchor必须绑定`camera_zone / optical_axis / must_see_anchors / covered_surfaces / lighting_orientation`；
- Tier A / S长期场景至少形成一个最小Anchor Pair或Anchor Set，用来锁定Hero看不到的常用方向；
- `REVERSE / ENTRY / WINDOW_SIDE / REAR_CORNER`等只有被真实镜头或未来高复用需求证明时才纳入。

新增原则：
1. `SPATIAL_CANON`锁几何事实；
2. `ENV_VISUAL_ANCHOR_SET`锁各方向的视觉事实；
3. Shot或Video需要新方向时，优先选择`Nearest Visual Parent(s)`（最接近当前Camera Axis的已批准Anchor），而不是总回到Hero重新猜整面墙。

新增硬门：`ENV_VIEW_CLOSURE_GAP`。当反打/回望/Entry-Exit方向已成为正式摄影需求，但当前没有足够Visual Anchor证明该方向时，返回Stage 03补最小Anchor View，不得由Storyboard或Video Prompt代替。
