# 强制Shot分镜 / Supplemental Previs提示词模板｜Current Authority

> **当前最高用途规则：** Stage 04对多镜头/多Beat Segment默认先用**一次真实Image Generation Job直接生成完整纯净白描Contact Sheet**，完成Master QC后再由`tools/storyboard_contact_sheet_splitter.py`确定性切出每个正式Shot/Beat对应的Clean Panels；真正单Panel镜头、局部修复或已验证Provider无法可靠输出Contact Sheet时才允许单Panel Image Job Fallback。图片像素内不生成任何文字、箭头、时间码、CUT或Shot/Panel编号。所有动态/导演说明只存在于离图Metadata，并必须在Stage 05继续编译进对应Final Video Prompt。


## 0.2｜Clean Storyboard Pixel Contract（不可覆盖）

图像模型只生成`CLEAN_STORYBOARD_PANEL`：单幅16:9视觉证据，表达构图、Blocking、姿态、视线、前中后景、空间结构、剧情状态。Mandatory Baseline固定为`STORYBOARD_RENDER_MODE = WHITE_LINE_STORYBOARD_ONLY`：清晰黑白白描/线稿，低装饰、低材质渲染；只允许极少量中性灰用于前中后景结构分离，不得形成灰阶精修画；**不得用彩色精修、最终成片渲染、Hero/Keyframe/Shot Execution图替代白描Baseline。**

**图片像素中禁止出现：**任何中文/英文/数字、Shot ID、Panel ID、时间码、景别名称、镜头术语、CUT/DISSOLVE、箭头、运动轨迹线、指示线、说明框、气泡、字幕、Logo、Watermark（平台不可避免水印按QC例外处理）。

Panel顺序、时间、Camera Motion、Cut Type、Attention Target、Shot Relation、动作节点、表演与视线说明全部写在外部Metadata。对于多镜头或多Beat场景，优先生成一张完整白描Contact Sheet，再由`tools/storyboard_contact_sheet_splitter.py`确定性切出Clean Panels；如需统一复核顺序，也可再由`tools/storyboard_grid_assembler.py`把切出的Panels重组成Sequence Board。图像模型不得自行设计带字Storyboard Page。上述离图执行说明在Stage 05必须进入`VIDEO EXECUTION ANALYSIS → Final Video Prompt`，不得只停留在Storyboard Metadata。

**Visual Proof原则：** 隐藏Metadata后，只看画面仍必须能读出构图、Blocking、Attention Target与关系证据；不能靠箭头或文字替画面完成导演任务。



## 0.2A｜Director Contact Sheet Mode（新增）

当一个Scene / Sequence需要连续规划多个镜头或多个动作Beat时，Storyboard默认优先采用**一次生成完整白描宫格 Contact Sheet**，而不是先独立生成每个Panel。

支持的常用宫格密度：`4 / 6 / 9 / 12 / 16 / 25`（也可自定义）。选择由`Duration + Beat Count + Action Complexity + Camera Change + Editorial Density`决定。

- `SHOT_GRID`：每格主要对应一个正式Shot；
- `BEAT_GRID`：多个格可以属于同一个Shot，用于打斗、长镜头、舞蹈、复杂Blocking等动作节点分析；
- 生成出的Contact Sheet必须仍然遵守匿名几何人形规则；
- Contact Sheet通过QC/Approval后，必须使用`tools/storyboard_contact_sheet_splitter.py`确定性切格，得到后续Stage 05可追踪的独立`STORYBOARD_CLEAN_PANEL`。

注意：Contact Sheet是**Storyboard生成任务**，不是最终视频直接Reference。它优先承担整段镜头设计、Blocking、动作推进和剪辑关系证明；真正的视频输入仍以切格后的单Panel、Execution Frame和按风险挑选的视觉资产为主。

## 0.3｜Anonymous Geometric Human Rule（新增，不可覆盖）

白描分镜**不得出现具体人物身份**。所有人物只允许使用匿名几何人形 / 简化姿态占位：
- 允许：头部椭圆、躯干/四肢体块、基本站姿/坐姿/动作姿态、清楚的空间占位与朝向；
- 禁止：可识别脸、具体五官、发型轮廓、服装细节、饰品、纹章、制服图案、角色独有身体特征、可识别年龄化妆信息、任何足以让模型把Storyboard误认成“角色视觉Authority”的细节；
- 禁止在白描中把主角、路人、群众画成可辨认的“谁”；人物身份、服装、发型、表演细节只在后续生成图片/视频提示词与相应Canon Asset中描述；
- 白描承担的是`构图 / Blocking / 空间 / 姿态 / 观看关系 / 动作节点`证明，不承担角色长相与服装Authority。

若需要证明脸部/特定Look，必须继承已Approved Character/FMH Base Authority后再做Rendered Human Anchor或Video Conditioning；若需要证明道具接触、复杂人景物组合，可补Shot Assembly。以上均不得污染白描Baseline，也不得替代Base Master。


## 0.35｜Storyboard Entity Binding Map（离图身份映射硬门）

**Storyboard pixels are anonymous; storyboard entities are not anonymous.**

白描中的每一个可追踪人物/道具/环境占位都必须在离图`STORYBOARD_ENTITY_BINDING_MAP`中拥有稳定Slot：
- 人物：`H_A / H_B / H_C ...`；
- 道具：`P_A / P_B ...`；
- 场景/关键空间：`E_A ...`；
- 群众原型：`C_A ...`；
- 车辆：`V_A ...`。

**这些Slot ID绝对不得画进白描像素，也不得进入最终模型Prompt。** 它们只用于内部绑定：
`H_A → Entity ID → Approved Canon Assets → Stage05 Reference Resolution`。

每个Panel还必须为所有Human Slot记录`world_zone / frame_region / depth_region / body_orientation / pose_state / action_state / action_phase`；有交互时记录`gaze_target_slot / contact_target_slot / held_prop_slots / motion_vector`。因此白描可以极度抽象，但站位、朝向、动作与交互语义不能模糊。

Stage 04通过`storyboard_entity_binding_lint.py`后才允许Storyboard QC通过。Stage 05必须把Slot解析成真实人物/道具/场景及当前最小充分Reference；不得根据“左边那个火柴人”继承身份。

## 0.5｜Reference Binding Gate
只要本次Previs / Storyboard实际绑定任何人物、环境、道具、综合色、Style或Parent Reference，在生成前必须读取`reference_binding_semantic_verification.md`建立当前`REFERENCE BINDING CONTENT MAP`。UI已选图但正文不写Token，同样属于真实Binding，不能跳过Content-Role核验。

## 1｜前置Gate

正式Stage 04 Previs / Storyboard必须满足：
- `EPISODE ASSET FROZEN`；
- `DIRECTOR SPATIAL RECONCILED`；Stage 02 Detailed Shot Contract已经与Stage 03真实Environment Geography / Coverage对齐；
- Stage 02 Director Target Duration已锁定且`>0`；
- 当前Segment已有Stage 02 `Shot Storyboard Coverage Contract`并通过`previsualization_strategy_router.md`；每个Shot都在`SHOT_STORYBOARD_COVERAGE_PLAN`中有Panel Coverage计划；
- 当前Sequence已有Locked `EDITORIAL_PLAN`；每个Shot的Viewpoint Role、Edit Entry/Exit Function与相邻Cut Trigger/Timing/Continuity Strategy已锁定；
- Stage 02当前Scene的`DIRECTOR_INTELLIGENCE_DECISION_CARD + Sequence Arc`有效，且本Segment的Director Invariants已提取；
- Stage 02 `Focus Owner / Critical Visual Read / Blocking / Distance / Depth / Entry/Landing Camera Geometry / Lens Family / Focus Plan / Stabilization / Axis-Screen Direction / Camera Intent / Cut Motivation / Shot Relation`已按当前Shot复杂度锁定；Stage 02C适用时已有`SPATIAL_EXECUTION_STATE`，当前Previs要证明其Start/Relation/Path/Landing而不是重新设计；剧情关键的Audio/Silence/Lighting Cue（若有）也已保留；
- 当前Segment Entry Mode已确定；
- CONTINUITY_ENTRY若需要真实Previous Ending Frame，则等待真实APPROVED Ending Frame；
- Reference已通过`reference_field_coverage_map.md`的Key Visible Asset Coverage + Task-Bound Resolve；当前关键入镜人物、场景方向、道具/武器/实体/状态没有遗漏；
- Environment / Prop若当前Shot需要新结构面但冻结资产没有对应Authority，标`ASSET_COVERAGE_GAP → EPISODE ASSET FREEZE BROKEN`，回Stage 03只补必要Coverage并重新Freeze；
- 高风险动作通过Action Feasibility与Natural Motion Preflight；
- 存在Crowd时已建立最小Crowd Motion Intent；
- 交付前通过Semantic Dedup，并最后运行`model_facing_prompt_surface_sanitizer.md`。

## 2｜内部分析层（不得整段复制给模型）

Skill内部先读取Stage 02 Detailed Shot Contract + Shot Storyboard Coverage Contract；Stage 04第一职责是**把每个Shot变成可验证Panel Coverage**，第二职责才是用Supplemental Previs证明额外风险；不得重新发明导演意图。按需运行：
- World State Transition / Continuity；
- Actor Objective / Tactic / Active Listening / Performance Causality；
- Limb Occupancy / Support / Transfer / Contact / Weight Shift / Ongoing Task；
- Motion Corridor / Kinetic Chain / Overlap / Joint Arc / Locomotion / Settle；
- Crowd Cluster / Motion Field / Attention / Reaction Propagation；
- Combat Exchange / Contact / Force / VFX；
- Director Spatial Staging / Axis / Screen Direction / Eyeline；
- Cinematography Grammar + Camera Motion Contract；
- Key Visible Asset Register / Reference Field Coverage；
- Reference Eligibility / Most Direct Authority。

这些结果只在最终Evidence / Anchor / Panel真正发生的位置出现一次。

## 3｜Shot Storyboard Coverage + Binding Preflight（内部，不复制到模型）

- Mandatory Board Type / Shot Coverage Plan属于必需生产控制；Primary Risk Driver / Proof Question只决定Supplemental Previs，不直接给图像模型。
- 它们先被翻译成最终`Output Format / Panel Count / Layout / Camera-Blocking Requirements`。
- Reference Binding / Asset ID / Version / Role / MUST_BIND只留Executor Packet；Mandatory白描模型只得到直接主体、空间、构图、冻结动作、光源方向与明暗结构，不得到综合色相；Supplemental Rendered Previs才按自身Authority接收色彩。


## 3.5｜Mandatory Board First（内部，不复制到模型）

1. Mandatory Baseline固定为`CONTACT_SHEET_FIRST → deterministic split → CLEAN_STRUCTURAL_STORYBOARD Panel Set`；Contact Sheet是多镜头/多Beat默认生成Master，Split Panels才是逐Shot/逐Beat后续追踪单位。真正单Panel镜头或修复任务才允许直接生成单Panel；
2. 按`SHOT_STORYBOARD_COVERAGE_PLAN`保证每个Shot至少有一个可定位Panel；
3. 有动作/位移/Camera/Focus/状态变化的Shot增加必要节点；
4. Long Take多个Panel必须明确仍是同一Shot，不产生假CUT；
5. Multi-shot / Montage每个真实Shot都必须覆盖，CUT / Match Cut不能漏；
6. Baseline完成后，才按Risk Driver生成可选Hero / Pair / Map / Camera Path / Contact Chain等Supplemental Component。

`CLEAN_STRUCTURAL_STORYBOARD`：清楚黑白线稿/极少中性灰、简化材质，不渲染综合色相；强调构图/Blocking/冻结Camera几何/空间/动作节点。它不是最终Render Style/Color/Face Identity Authority。

`CLEAN_STORYBOARD_BOARD`只能由已生成的白描Clean Panels确定性排列；Board不得增加新的角色细节、综合色相、文字、编号、箭头或导演标记，也不得改变任一Panel的画风与内容。它只改善阅读顺序和整体导演审阅。

### 3.6｜Multi-shot Sequence / Generation Envelope宫格硬门（新增，不复制给图像模型）

只要当前正式Sequence包含`2+ Formal Shot`，白描宫格就从“方便Review”升级为**Stage 04硬前置证据**，即使后续采用ASSEMBLY_FIRST、每个Shot分别生成也不能跳过。除此之外，当某个`GENERATION_ENVELOPE`满足`FORMAT_MODE != ONER`、包含多个Formal Shot、或包含多个CUT Contract时，该Envelope还必须拥有与自身CUT子集严格对应的宫格证据：
- 每个CUT必须有Approved `STORYBOARD_CLEAN_PANEL`，默认由同一Approved Contact Sheet确定性Split得到；
- 如需要Sequence Review Board，Panel再按CUT order交给`tools/storyboard_grid_assembler.py`确定性拼版；
- 输出登记为`STORYBOARD_CLEAN_SEQUENCE_BOARD`，`layout_type=MULTI_PANEL`；
- Board的`source_panel_asset_ids_ordered`必须与Envelope `CUT_CONTRACT[].storyboard_panel_asset_id`完全一致；
- Board仍然零文字、零编号、零箭头、零CUT/时间码；
- Board只可作为结构/顺序辅助Reference，`primary_visual_eligible=false`；
- Sequence级宫格未形成/未通过：`STORYBOARD_SEQUENCE_GRID_QC_PASS/APPROVED_PASS=false`，不得离开Stage 04；
- Envelope级宫格未形成/未通过：`MULTISHOT_STORYBOARD_GRID_GATE_PASS=false → NO VIDEO GENERATION`。

只有整个正式Sequence本身就只有1个Formal Shot时，Sequence Board才是`NOT_REQUIRED`。某个ONER Envelope若属于一个多Shot Sequence，仍受该Sequence级白描宫格约束；只是这个ONER Envelope本身不另做子宫格。

Model-facing正文不得出现`Mandatory Gate / Coverage Contract / Stage 02 / Stage 04 / Director Contract`等内部管理词。

## 4｜MODEL-FACING SINGLE-PANEL FALLBACK / REPAIR PROMPT｜仅Fallback使用

> **Current Copy Surface Rule：** 本段只用于**真正单Panel镜头、局部Panel重生/修复，或Provider已验证无法稳定生成Contact Sheet**的Fallback。多镜头/多Beat默认使用上面的Director Contact Sheet Mode，不得把本段误当成全局Baseline。使用本段时才执行`ONE GENERATION JOB = ONE CLEAN 16:9 PANEL`；每次只生成一个冻结瞬间。

### 【单幅输出】
生成一张单幅16:9黑白白描/线稿Storyboard Panel。画面只承担当前Shot当前关键瞬间的构图、Blocking、姿态、视线、空间层次和剧情状态证据。Fallback单Panel任务中不要生成Storyboard Page、宫格、Contact Sheet或第二幅画面。

### 【当前冻结状态】
<只写这一瞬间已经成立的人物、位置、朝向、姿态、道具接触、伤势/衣物状态与环境状态。不得写“随后/接下来/几秒后/移动到”等动态过程。>

### 【构图与冻结机位】
<写景别、主体面积、人物距离、FG/MG/BG、透视、遮挡、视线关系，以及这一瞬间的机位高度/朝向、Lens Family、Focus状态。只描述静止几何，不写Camera Path、速度、轨迹或运动曲线。>

### 【人物 / 道具冻结状态】
<写这一刻可见的姿态、承重、手脚占用、持物/接触与空间落点。人物仅作为匿名几何人形/姿态占位，不描绘可识别脸、发型、服装细节或身份特征。只写当前状态，不描述动作路径或下一步动作。>

### 【视觉重点】
<写观众这一幅必须读到的脸部/眼部、伤势、关键道具、接触或空间信息；无法在静态画面中直接看见的时间、CUT、运动、表演过程不要写进图片Prompt。>

### 【白描与一致性】
保持已批准场景几何、道具结构、光源方向、明暗层级和主体分离。人物只保持空间占位、体型层级和姿态逻辑，不继承任何可识别脸、发型、服装细节或角色身份特征。只允许黑白线稿与极少量中性灰结构分层；不得渲染综合色相、最终材质或成片级精修。

### 【像素禁区】
画面中不得出现任何文字、字母、数字、Shot/Panel编号、时间码、CUT/DISSOLVE、Camera术语、箭头、运动轨迹线、指示线、说明框、气泡、字幕、Logo或Watermark（平台不可避免水印仅由QC按既有例外处理，不作为主动生成元素）。

### 【必要限制】
<只保留当前冻结画面仍有真实风险的身份、空间、肢体、道具、镜像或结构限制；不得加入动态导演说明。>

## 4.5｜Director Inheritance Hard Gate

Previs / Storyboard候选必须检查：
- 本Segment仍执行Selected Directorial Thesis与对应Director Invariants：Audience Alignment / Reveal- Withhold顺序 / Reaction Give-Deny / 核心Blocking-Distance / POV-Perspective / Key Hold-Cut / Opening-Closing Function（仅当前Segment适用项）；
- Mandatory Board覆盖Stage 02全部Shot且Panel/CUT语义一致；不得以Hero/Pair/Map/Path替代任何Shot Coverage；Supplemental Component才按Proof Question检查；
- 相邻Formal Shot必须同时证明`EDITORIAL_PLAN`的Viewpoint Transfer与Edit Boundary：动作向量、Eyeline、Screen Direction、Reveal顺序和Reaction Give-Deny不冲突；不能只靠景别变化制造“看起来有切镜”；
- HYBRID各Component证明不同风险，不重复堆同一信息；
- 不得把Stage 02已锁的前后景重新压成同一平面；
- 不得无因交换人物Screen Side / Eyeline；
- 不得为了“看清所有角色”取消有意遮挡/裁切；
- Combat必须保留Engagement Distance Ladder与Contact Read；
- Transformation关键展示必须保留Presentation Contract和Visual Level Gap；
- Montage必须保留Ordering / Connection / Information Gain，不得退化成若干资产展示格。

失败：`DIRECTOR_INVARIANT_EXECUTION_FAIL / DIRECTOR_INHERITANCE_FAIL / SHOT_STORYBOARD_COVERAGE_GAP / STORYBOARD_EVIDENCE_INSUFFICIENT / PREVIS_REDUNDANCY_FAIL / STAGING_DISTANCE_FLAT_FAIL / SCREEN_DIRECTION_FAIL / COMBAT_LINEUP_FAIL / TRANSFORMATION_PRESENTATION_FLAT_FAIL / MONTAGE_PPT_FAIL`。

## 5｜Stage 04 Semantic Dedup Hard Gate

正式Storyboard Prompt输出前必须确认：
- [ ] Key Visible Asset Register中的所有Critical字段均有Approved视觉Authority，不存在`REFERENCE_COVERAGE_GAP / REFERENCE_SLOT_OVERFLOW`；
- [ ] 当前Director Decision Card / Sequence Arc有效；Segment-scope Director Invariants已被Panel执行，没有因Previs格式或Reference便利改变Audience Alignment / Reveal / Reaction Give-Deny / Key Hold-Cut；
- [ ] Detailed Shot Contract的Focus Owner / Critical Read / Distance / Depth / Entry/Landing Camera Geometry / Lens Family / Focus Plan / Stabilization / Axis / Blocking / Camera Intent / Cut Motivation / Shot Relation已被当前Panel执行，没有Stage 04自行重设计；
- [ ] 模型Prompt不存在Reference职责行政区块、文件名、Raw Asset ID、Version、Path或内部Role表；不存在`TASK_SHELL / INPUT_LABEL / OUTPUT_ADMIN_SHELL`等操作者任务壳；真实Reference控制结果已归并进主体/空间/构图/Panel执行句；Mandatory白描只允许Value/Lighting结构，不写综合色相；平台需要其它真实Reference原生Token时仅使用真实Token + 最短执行语句；
- [ ] Entry只写t=0状态；
- [ ] 表演、Action Feasibility结果、Natural Motion、Crowd、环境反馈、Combat均已并入对应Panel，不存在独立长篇复述区；
- [ ] 正向动作已经解决的问题没有再写同义Negative；
- [ ] 内部Pre-Pass术语、Gate解释、分析表没有进入模型正文；
- [ ] 每个动态事实只有一个Panel Owner；
- [ ] Revision没有在旧Prompt后继续追加补丁说明。
- [ ] `SURFACE_LINT_REPORT`全部Forbidden Counter = 0。

失败：`PROMPT_REDUNDANCY_FAIL`，重新编译，不交付。

## 6｜Storyboard Action / Crowd Hard Gates

### Action
高风险动作必须先内部求解：
`State → Requirement → Resource/Support Audit → Conflict → Minimal Bridge → Execution → Exit`

未解决肢体互斥、Prop支撑丢失、Transfer缺口、Contact前置、Weight Shift、Ongoing Task或Exit：`ACTION_FEASIBILITY_FAIL`。

动作虽合法但只能靠Pose最短插值、脚底滑转、机械串行、同帧启停：`NATURAL_MOTION_FAIL`。

### Crowd
明显群体必须有最小：
`Cluster / Ambient Motion / Attention Baseline / Flow / Reaction Propagation（适用时）`

静态Panel只定义空间Anchor，不定义Video期间冻结。背景生活强度低于主表演；合法静止不强迫持续乱动。未解决：`CROWD_PRESENCE_FAIL`。

## 7｜输出原则

**Stage 04所有Segment都必须先有White-line Clean Shot Storyboard Baseline：每个正式Shot至少有一张可定位、实际生成并批准的白描Clean Panel视觉证据；再用Supplemental Previs证明额外风险。Panel数不固定，但任何Shot都不能没有白描视觉分镜。**

**Storyboard-to-Video Text Handoff Gate：** 每个Shot对应的Camera Motion、Timing、Cut/No-Cut、Action Beat、Performance、Eyeline、Relation与Landing说明必须在Stage 05 Final Video Prompt中出现为可执行自然语言；只存在Storyboard Metadata而未进入Video Prompt时，失败码=`STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP`。

模型侧只收到一次最短、最完整、可执行的结果。



## Current｜Storyboard → Video Visual Routing

`APPROVED MANDATORY SHOT STORYBOARD`由Approved**白描**Clean Panels + 外部Metadata构成。Whole Board若需要，只由这些白描Clean Panels确定性拼版；按目标模型Capability选择Clean Board、Panel Multi-reference或Key Panel。任何带文字/箭头的Review Sheet、彩色精修Board或其它Rendered Previs都不是本项目Mandatory Storyboard Baseline。

Hero/Pair/Map/Path等Supplemental Component只按其独占字段参与路由，不得冒充Mandatory Shot Coverage。

## Current｜Storyboard Real Generation Spine Hard Gate

Storyboard不是“只写Prompt”的文本交付。每个Mandatory Clean Panel与被选中的**生成式**Supplemental Previs都必须创建真实`IMAGE Generation Job`。Mandatory Sequence Board本身不是图像生成任务，只能由`tools/storyboard_grid_assembler.py`从Clean Panels确定性拼版。

审批顺序固定为：
1. 每个Mandatory Panel：`Dispatch → Host Generate → Candidate Capture → Select Candidate → Image/Visual QC → QC_PASS_WAITING_APPROVAL`；
2. 运行`storyboard_coverage_lint.py --phase qc`，必须覆盖全部正式Shot且所有计划Panel都有真实结果；此时才允许进入`STORYBOARD_QC_PASSED_WAITING_APPROVAL`；
3. 用这些QC通过Panel确定性拼Review Board，由用户一次批准当前Storyboard Set；
4. `APPROVAL_RECORD`必须记录全部Mandatory Panel IDs及其Selected Candidate Fingerprints；
5. 将同一`approval_ref`写回各Panel Job，执行`APPROVED_PROMOTED → ASSET_REGISTRY`；
6. 运行`storyboard_coverage_lint.py --phase approved`。只有该Gate通过才可成立`APPROVED PREVIS SET`。

因此禁止“先逐Panel假批准/Promotion，再让用户批准Storyboard Set”的双审批顺序。

### Off-image Storyboard Handoff Metadata（不进入白描图片像素）
每个Shot都维护固定八类交接项：`Camera Motion / Timing / Cut-NoCut / Action Beat / Performance / Eyeline / Shot Relation / Landing`。Stage 05必须将其正规化进`VIDEO_EXECUTION_PLAN.storyboard_handoff.items`；每个`REQUIRED`项保存`source_text + prompt_anchor`，不适用项必须显式`NOT_APPLICABLE + reason`。其中Camera Motion、Timing、Cut-NoCut、Action Beat、Landing永远不可豁免。

### Clean Storyboard Color Authority
Mandatory白描Panel仍记录当前Scene Color Authority血缘，但**禁止把彩色色卡作为图像模型直接Reference**。Generation Job必须使用`color_binding.required=false + authority_level=SCENE_COLOR_CARD + projection_mode=VALUE_LIGHTING_LINEAGE_ONLY + binding_status=NOT_REQUIRED`，并记录对应`color_asset_id`；`required_bindings`不得出现该综合色卡的`COLOR_AUTHORITY`绑定。白描只从该血缘继承光源方向、明暗层级和主体分离，不继承色相。综合色Direct Binding在Shot Execution阶段恢复；Final Video阶段是否继续直绑综合色卡由Reference Budget动态决定。

## Current｜Perception Proof Gate（离图Metadata + Visual QC）

Mandatory白描Panel除了证明Blocking/Camera几何，还必须能让人工/多模态QC核对Stage 02已锁的：
- `Camera Ethics`是否仍然成立（观众没有被偷偷移到另一观看立场）；
- `Attention Flow`的Entry → Resistance → Decisive Landing → Residual → Exit是否可读；
- `Shot Scale Justification`是否成立，尤其CU/ECU是否真的需要靠近；
- `Primary Composition Mechanism`是否清楚，没有多个机制互抢；
- `Visual Salience Budget`是否保持一主一辅，其余信息没有全部变成同等清晰的“AI展示”；
- 相邻Formal Shot的`Information State OUT → IN`与Editorial顺序没有提前泄露或丢失。

这些字段**不得烤进白描像素**。它们只存在于Storyboard Handoff Metadata/QC Record；白描仍保持零文字、零箭头、零编号。若视觉结果违背它们，返回对应Stage 02 Owner做最小Patch，不允许Stage 04自行换机位补救。
