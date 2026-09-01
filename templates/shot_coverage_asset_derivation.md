# Shot Coverage & Asset Derivation Engine（镜头覆盖与资产衍生引擎）

> **适用范围：Stage 02 → Stage 03，V4.5.2同时处理Entity-driven、Event-node-driven、Character-route-driven、Relation-driven与Predictive Environment / Prop资产需求。**
>
> **Character Asset Pipeline保持现状，不使用本模板重做人物多视图、人物母图或人物衣柜逻辑。Transformation Master Set / WP等仍按原有Transformation Authority建立；本引擎只在其作为已存在正式对象、且真实Shot确需额外可见面时提供Coverage判断，不改其设计流程。**

## 1｜核心原则

**Spatial Canon First → Clean Master → Event/Relation/Shot Coverage Driven。**

正式资产不再按“场景应该有几张、道具应该有正背侧几张”机械平铺。先建立一个能定义对象身份/空间的高质量Canonical Master，再读取Stage 02真实Shot需求，倒推出下游实际会拍到的视角、状态与空间方向，只补最小充分Coverage。**“最小充分”按下游Video风险判断，不按“理论上文字能解释”判断。** 当前项目静态图成本很低；若一张高清Coverage能显著降低昂贵Video对关键结构/空间的猜测，应生成，而不是为了少一张图片把风险留到Stage 05。

任何新增Environment / Prop衍生图都必须回答：

1. **Parent Master是谁？**
2. **被哪些Shot真正需要？**
3. **镜头会看到哪一面 / 哪个空间方向 / 哪个状态？**
4. **现有结构Authority还留下什么会增加Video风险的静态歧义？**
5. **这张衍生图具体降低什么下游失败风险？**

无法回答以上问题的衍生图，默认不生成。

## 2｜Authority层级

### 2.1 Canon Master（正式主资产）
负责“它到底是什么 / 这个地方到底是什么空间”。

- `PROP_CANON_MASTER`：一道具原则上先建立**一张正式高清Hero Master**，锁轮廓、比例、材质、功能结构、非对称特征与关键识别点。
- `ENV_CANON_MASTER`：一场景原则上先建立**一张正式高清Hero Environment Master**，锁空间身份、主要地标、材质、尺度、出入口关系与基础主光。Hero View选择最能说明空间的正向/3/4/Establishing视角，不为了“正面”而牺牲空间可读性。

Canon Master是父Authority。后续Coverage View不得修改其设计，只能从它推导。

### 2.2 Structure / Geography Spec（结构/空间文字规格）
主图之外先补**文字或简化结构记录**，而不是立刻生成更多图片。

Prop至少记录：
- 正面/背面定义；
- 非对称点；
- 开合/折叠/机关关系；
- 尺寸与Human Scale；
- 可持握/接触区域；
- 不能变化的Design Locks。

Environment至少记录：
- Entrances / Exits；
- 门窗与固定地标；
- 可行走/表演/战斗区；
- 关键家具/舞台/柜台/楼梯等位置关系；
- 基础Camera Axis / 常用拍摄半球；
- L2/L3时按需要建立简化Blocking Map / Zone Map。

**先Geometry/Structure，后Coverage。** 一张Hero图看不到的内容，先用结构规格定义Canon；但若当前真实Shot属于高价值/高风险、会清楚看到该结构，或Video需要据此完成接触/空间关系，且纯文字仍留下明显视觉猜测，则生成Coverage View。不要把“文字存在”误判为“图像级歧义已消失”。

### 2.3 Derived Coverage View（衍生覆盖视图）
由Stage 02的Shot Coverage Matrix触发，属于Parent Master的子资产。

命名建议：
- `PROP_<ID>_CV_<VIEW_OR_USE>`
- `ENV_<ID>_CV_<CAMERA_SIDE_OR_ZONE>`

登记字段：
```text
Parent Master：
Coverage Asset ID：
Triggered By Shot(s)：SH__ / SH__
Coverage Need：WHOLE / CLOSE-UP / REVERSE / SIDE / TOP / ENTRY / EXIT / INTERACTION / OPEN_STATE / OTHER
Camera / Visible Side：
Required State：
Why Master Is Insufficient：
Downstream Risk Reduced：
Authority Boundary：继承Parent Master；只增加该视角/状态可见信息，不得重设计
Status：WIP / CURRENT / APPROVED / DEPRECATED
```

Coverage View可以成为Stage 04/05的高清对象/空间参考，但**不是新的独立Canon设计**。

## 3｜Stage 02：Shot Coverage Matrix

导演锁定Detailed Shot Contract与Segment后、形成Raw Asset Demand之前，必须对**本集实际出现的场景与重要道具**做Coverage分析；Coverage结果随后进入`asset_consolidation_sufficiency_audit.md`，不能因Shot ID不同机械变成多张最终资产。

### 3.1 Prop Shot Coverage

只对关键/易漂移/近景/交互道具记录：

| Shot | Prop | 景别/用途 | 可见面 | 交互/Holder | 必须状态 | 当前结构Authority的Static Ambiguity可接受? | 需要衍生图 |
|---|---|---|---|---|---|---|---|
| SH__ | PROP__ | MCU / Insert / Action | front/side/back/top | RH hold / table / open | CLOSED/OPEN/... | YES/NO | NONE / CV__ |

触发衍生图的典型情况：
- Insert / Close-up会清楚看到Master未覆盖的一面；
- 非对称道具发生反打/翻转；
- 开合/折叠/机关状态是剧情信息；
- 手持/操作方式对结构稳定性重要；
- 关键道具将以桌面俯拍、地面掉落、内侧/背面等明确方向出现；
- 后续视频模型若只看Hero Master，很可能猜错关键结构。

**不触发：** 只是换一个普通角度、短暂反光、轻微湿水、简单手握，且现有Master+文字已经把当前Shot的静态歧义降到LOW。若同一“简单手握”实际上是昂贵T3/T4镜头的关键接触且模型高概率猜错，则转`production_support_reference_engine.md`判断Interaction Support，不机械仍判NONE。

### 3.2 Environment Shot Coverage

对每个Location记录本集真实摄影需求：

| Shot | Environment | Shot Purpose | Camera Side / Zone | 可见地标/出入口 | Blocking需求 | 当前结构Authority的Static Ambiguity可接受? | 需要衍生图 |
|---|---|---|---|---|---|---|---|
| SH__ | ENV__ | Establishing / OTS / Reverse / Action | door side / window side / reverse | ... | low/medium/high | YES/NO | NONE / CV__ |

触发衍生图的典型情况：
- 对话有明确Reverse / OTS，Hero Master无法解释反方向空间；
- 人物要从门/楼梯/走廊进入并走到目标位置；
- 追逐/战斗跨多个Zone；
- 镜头从柜台/舞台/窗边等固定锚点反拍；
- 同一空间跨多个Segment反复使用，且Camera Side变化大；
- 镜头会近距离拍摄Hero Master中不可读的固定空间结构。

**不触发：** 纯Establishing、Montage或单一拍摄方向且Hero Master对当前可见空间已经足够唯一。短Insert若会看清此前不可读的固定结构，不因“镜头短”自动豁免，仍按Video Risk判断。


## 3.25｜Event Node + Relation Driven Coverage（V4.5.2）

Coverage Matrix不能只问“这一镜看对象哪一面”，还必须读取`SPATIAL_CANON + SCENE_EVENT_NODE_GRAPH + SHOT_RELATION_GRAPH`：

- Event Node要求人物到达/经过/观察的Zone或Anchor，必须有对应可拍视角；
- `CLUE_REVEAL / LOOK_POV`若依赖从A看到B，必须派生`ENVIRONMENT_COVERAGE`，并写`coverage_reason_codes=[CLUE_REVEAL]`或`[LOCATION_VISIBILITY]`；
- 外景识别物切入同一建筑内部时，必须派生`ENVIRONMENT_COVERAGE`并写`coverage_reason_codes=[LOCATION_IDENTITY]`，或提供等价真实视觉证据；
- Relation-driven Coverage必须写入Final Episode Asset Requirement Manifest，不得只存在于Relation Graph而不进入资产队列。

`SCENE_VIEW_GRID`只是同一Set的多个独立Clean View集合，UI可以排成宫格；它不是时序Storyboard，也不得以拼板图片直接冒充单镜头空间锚。

## 3.26｜Event Route / Reciprocal / Predictive Coverage（V4.5.2）

### Event Node → Spatial Node
每个需要空间资产支撑的剧情Event Node应绑定Location / Zone / Anchor；跨节点人物移动优先读取`CHARACTER_EVENT_ROUTE`。如果事件写“从餐厅冲向楼梯”，但Floor Plan没有合法门/路径，先修Spatial Canon，不生成假Coverage。

### Reciprocal Coverage
当剧情会使用正打/反打、前看/回看、入口/出口、地点A看地点B等关系时，可把关系本身派生成Coverage Obligation。Reciprocal并不等于必须两张：只有下游确实需要双方视角时才成对生成。

### Predictive Coverage
对Tier S/A高复用Set，在已知后续剧本/Director Coverage中提前合并重复机位需求，形成`ENVIRONMENT_COVERAGE`并写`coverage_reason_codes=[PREDICTIVE]`。目的不是“九宫格凑齐”，而是减少未来同一Set重复生成。每项必须记录`predicted_shot_ids / downstream_use / why_required`。

### 双Parent Contract
环境Coverage必须登记：
- `spatial_parent_refs`：锁Topology/Floor Plan/Zone/Anchor；
- `visual_parent_refs`：锁当前Set已批准的材质、家具、光色与设计。

如果只绑定Visual Parent而违背Floor Plan，或只绑定Floor Plan而重新设计房间美术，均为`COVERAGE_PARENTAGE_FAIL`。

## 3.3｜与Production Support Reference的分工

Coverage只解决**对象/空间本身的可见结构或正式摄影方向**。如果Canon已经定义，当前高风险Shot缺的是复杂交互、多人Contact、一次性Transient State或Storyboard精确组合，不要把每一种临时动作都升级成Coverage。

路由：
- 新结构面/空间方向不可读 → Derived Coverage；
- 跨多个Shot/Segment持续的明显状态 → Persistent State Variant；
- Canon已定但复杂交互/Contact/一次性Action State仍需高清证据 → Stage 03 Production Support Reference；
- 必须等Approved Storyboard才能确定最终单画面构图 → Stage 04 Video Conditioning Frame（First / Target / Last / Contact / Exit / Entry），不再把“HD Anchor是否需要”作为能否拥有镜头执行图的开关。

具体读取`production_support_reference_engine.md`与`video_conditioning_asset_architecture.md`。同一风险只允许一个Owner，禁止Coverage + Support + Conditioning Frame重复建图。

## 4｜Stage 03：生产顺序

### 4.1 Prop
1. Reuse Existing Approved Master；
2. 若无正式Master → 先生成一张`PROP_CANON_MASTER`；
3. QC + 用户APPROVE；
4. 建立/更新Structure Spec；
5. 读取Prop Shot Coverage；
6. 只生成`当前结构Authority仍留下正式可见面/空间方向静态歧义`且确实由Shot触发的Derived Coverage View；
7. 每张Coverage View都必须从Approved Parent Master倒推，QC确认same object；
8. 必要Coverage全部APPROVED后进入Episode Asset Freeze。

**禁止默认“正/背/侧/细节一套全做”。** 正背侧只有当实际镜头/结构风险要求时才生成。

### 4.2 Environment
1. Reuse Existing Approved Master；
2. 若无正式Master → 先生成一张`ENV_CANON_MASTER`；
3. QC + 用户APPROVE；
4. 建立Geography Spec；L2/L3必要时建立Blocking / Zone Map；
5. 读取Environment Shot Coverage；
6. 只生成被真实机位需要的Reverse / Side / Door-side / Window-side / Zone Coverage等；
7. 所有Coverage必须由同一Parent Master + Geography推导，门窗、地标、尺度与轴线不可漂移；
8. 必要Coverage全部APPROVED后进入Episode Asset Freeze。

**禁止从每个新视角重新设计一个“看起来像同地点”的独立场景。**

## 5｜Shot-Bound ≠ 临时Storyboard图

本模板的`Derived Coverage View`仍是Stage 03正式高清资产，只是它的**生成理由来自Shot**。它不是：
- Storyboard Grid；
- Storyboard Panel；
- 临时Pose图；
- Ending Frame；
- 为单次动作随手生成的低清草图。

Stage 02先锁Shot Contract与构图意图，Stage 04负责把它落实为Panel级构图和表演执行。Stage 03 Coverage只负责让Stage 04/05在某个真实需要的方向上，能够看清同一个正式道具/同一个正式空间。

## 6｜Coverage Gap规则

Stage 04实际做Storyboard时若发现：
- Detailed Shot Contract / Stage 02 Coverage Analysis此前遗漏了一个**必须看清的道具结构面**；或
- 一个**新的正式摄影方向**无法由现有Environment Master / Coverage唯一确定；

则标记：

`ASSET_COVERAGE_GAP`

同时：`EPISODE ASSET FREEZE BROKEN(reason=coverage)`。

处理：
1. 不重做Parent Master；
2. 回Stage 03只补最小Derived Coverage View；
3. QC + 用户批准；
4. 更新Coverage Matrix / Episode Asset Pack；
5. 重新Freeze；
6. Change Impact只复查依赖该Coverage的Storyboard/Video。

若只是普通角度/姿势，现有Approved HD Object Authority + Storyboard足以解决，则**不打破Freeze**。

## 7｜Freeze Gate补充

Environment / Prop在冻结前不仅检查“有没有Master”，还检查：
- 每个TO BUILD对象已有Approved Canon Master；
- Shot Coverage Matrix已经跑过；
- 所有`Master Is Insufficient = NO`的镜头不无意义加图；
- 所有真正需要的Coverage View已APPROVED；
- 每张Coverage View都有Parent Master和Triggered By Shot(s)；
- Environment各视图保持同一Geography；
- Prop各视图保持同一Object Geometry / Scale / Function；
- Character资产没有被本引擎误改、误扩展或重新拆分。

## 8｜成本原则

**Coverage是为了减少下游失败，不是为了收集设定图。**

默认优先级：

`Approved Master + Text Spec` → 评估当前Shot Static Ambiguity / Video Risk → `Required Derived Coverage`（结构/空间问题）或交给`Production Support Reference Engine`（交互/Contact/Shot组合问题）→ 风险降到可接受后停止。

禁止：
- “以后可能用到”式360°环境全套；
- 道具默认正背侧顶底全套；
- 为每个Shot都做一张Stage 03资产；
- 让Coverage View承担Storyboard构图职责；
- 因为一个衍生角度不好看就重设计Parent Master。

## 11｜Downstream Reference Binding

Coverage一旦APPROVED，Stage 04/05如果当前Shot正好由该Coverage触发，Resolver应把它作为该摄影方向的`PRIMARY VIEW / SPATIAL AUTHORITY`。Parent Hero Master只在Coverage仍缺失Canon字段时补充；不得因为“母图更正式”机械同时@，造成正面视角与当前反打/侧拍争权。具体执行见`task_bound_reference_binding.md`。

## V4.5｜Relation-Driven Asset Obligation（关系驱动资产义务）

> **关键升级：** Asset Requirement不再只由“镜头里有什么人物/场景/道具”派生，还必须由`SHOT_RELATION_GRAPH`派生“为了证明相邻镜头关系，必须看见什么”。结构化载体：`state/visual_asset_obligation.schema.yaml`。

### 两类需求必须同时跑
1. `ENTITY-DRIVEN`：Character / Environment / Prop / Transformation / Coverage；
2. `RELATION-DRIVEN`：Clue / Reveal / Sightline / Exterior↔Interior Identity / Exit↔Entry / POV Target / Match Motif等。

### 典型关系资产
- `ENVIRONMENT_COVERAGE + coverage_reason_codes=[CLUE_REVEAL]`：某地点内能准确看见剧情线索的特定视角；
- `ENVIRONMENT_COVERAGE + coverage_reason_codes=[LOCATION_VISIBILITY]`：证明“A地点从指定视线能看到B地点/地标”；
- `ENVIRONMENT_COVERAGE + coverage_reason_codes=[LOCATION_IDENTITY]`：证明“远景建筑、钟面、内部机械室属于同一Location Entity”；
- `VIDEO_CUT_EXIT_FRAME / VIDEO_CUT_ENTRY_FRAME`：Storyboard批准后在Video Conditioning层完成；
- 其它First/Target/Contact按现有Video Conditioning规则派生。

### Asset Obligation状态
每条义务必须记录`obligation_id / relation_id / reason / fulfill_by / required_visual_fact / fulfillment_asset_ids / status`。

- `STAGE_03_FREEZE`前：关系所需的Canon/Coverage/Clue/Location Identity证明必须FULFILLED或有真实可审计Waiver；
- `STAGE_04_STORYBOARD_QC`前：Storyboard必须真实表现Attention Target与Cut Motivation；
- `STAGE_04_VIDEO_CONDITIONING_QC`前：Exit/Entry/First/Target等执行图片必须完成Pairwise Alignment。

### 禁止
- 两个Location各有漂亮Master，就假定它们的关系已被证明；
- 只有文字写“同一个钟楼”，但没有任何Location Identity / Sightline资产；
- Scene Master里存在一个窗口，就假定镜头“推向窗”能唯一确定目标窗；
- 因为Video模型可能理解关系，就Waive本可在图片阶段消除的静态歧义。

失败：`RELATION_ASSET_OBLIGATION_GAP / CLUE_VIEW_MISSING / LOCATION_IDENTITY_BRIDGE_MISSING / SIGHTLINE_ASSET_MISSING`。

## V4.5.4｜REQUIRED_VIEW_REALIZATION_GATE（多场景按需多视角闭环）

**核心：** `required_view_roles`只是导演/事件层的简写，不是完成状态。Stage 03必须把它们物化为`SPATIAL_CANON.view_requirements`，并生成确定性的`VIEW_ROLE_COVERAGE_MATRIX`。

每个Required View至少记录：
- `view_requirement_id / scene_id / location_entity_id`；
- `event_node_ids / shot_ids / relation_ids`中的真实触发来源；
- `view_role`；
- `Camera Origin`：`camera_origin_zone_id`和/或`camera_origin_anchor_id`；
- `Optical Axis`：`view_target_entity_id / view_target_anchor_id / view_direction_code`；
- `Must See`：`required_visible_anchor_ids`；
- `Must Not See`：必要时`forbidden_visible_anchor_ids / forbidden_visual_fact_codes`；
- `candidate_budget`与最终`selected_fulfillment_asset_id`。

**禁止模糊词直接进入生成：** “正视角 / 反打 / 车内前方”必须先转成可验证轴线。例如：`后排中轴(CAM_REAR_CENTER) → 前挡风玻璃(WINDSHIELD)`，Must See=`WINDSHIELD + DASHBOARD + DRIVER_SEAT + PASSENGER_SEAT`。

### VIEW_ROLE_COVERAGE_MATRIX
对Episode所有Scene统一合并并去重Required View。Matrix回答：`需要什么方向 / 为什么需要 / 现有哪张图覆盖 / 还缺什么`。`tools/view_coverage_planner.py`只把MISSING项放入Generation Queue；P0/P1缺口优先于已覆盖方向的新候选。

### Coverage Asset Binding
V4.5.7新生产的物理Coverage统一使用`ENVIRONMENT_COVERAGE`。它必须在`Asset Registry.derivation.view_requirement_ids`回指至少一个具体Requirement，并用`coverage_reason_codes`记录`EVENT_NODE / RECIPROCAL / PREDICTIVE / CLUE_REVEAL / LOCATION_VISIBILITY / LOCATION_IDENTITY / REQUIRED_VIEW`等触发原因，同时写入同一组Camera Origin / Target / View Direction / Must See。旧Coverage类型仅允许迁移读取，不得用于新建资产。

### Visual Realization Proof
Asset Prompt写对不等于图片真的对。Freeze时`REQUIRED_VIEW_REALIZATION_GATE`读取Current Visual Evidence：
- `Observed View Role`必须匹配；
- Observed Camera Origin / Optical Axis必须匹配Required View；
- Must See Anchors必须实际可见；
- Must Not See / Forbidden Visual Facts不得出现；
- 选中的Fulfillment Asset必须APPROVED且Fingerprint与Evidence一致。

失败码：`REQUIRED_VIEW_ASSET_MISSING / REQUIRED_VIEW_ROLE_VISUALLY_UNPROVEN / REQUIRED_VIEW_AXIS_VISUALLY_UNPROVEN / REQUIRED_VIEW_VISIBLE_ANCHOR_GAP / REQUIRED_VIEW_VISUAL_FACT_CONFLICT`。

### Coverage Debt First
如果仍有Required View为MISSING，同时某一已覆盖方向的Active Candidate数量超过该Requirement的`candidate_budget`，硬失败`COVERAGE_BUDGET_STARVES_REQUIRED_VIEW`。不要生成第5张相似反打，却还没有一张真正的前向视角。

## V4.5.5｜Required View × Realism Contract

`view_requirement_id`只证明“拍哪个方向”，不证明“这个方向里的世界合理”。每个包含人物或功能空间的Required View同时绑定`realism_contract_ids`：

- Camera Origin / Optical Axis仍由Required View负责；
- Vehicle/Architecture/Seat/Zone/Capacity由Realism + Spatial Canon负责；
- Expected Cast / Functional Position / Human Support由Realism Contract负责；
- 最终Current Visual Evidence必须同时证明View与Reality。

因此`FORWARD PASS`但人物被放错Seat、车辆布局漂移，仍不能Fulfill该生产资产。
