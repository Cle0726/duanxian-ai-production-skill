# Reference Resolver（参考图自动选择器）｜Current Authority

> **用途：** 每次图片、Storyboard、视频生成或Revision前，先读取`task_bound_reference_binding.md`建立Task Contract，再选择当前任务真正需要的最小充分参考集合。内部建立真实Executor Input Map；生成Prompt的参考表达由`execution_reference_semantics.md`消解为直接可执行的主体/空间/综合色/构图/Entry/Timeline语言。**Current Generation Profile下，所有强绑定Approved Asset必须显式输出真实平台`@资产`Mention**；不输出Semantic Role职责表、内部Asset ID或伪造`@图N`。若平台只支持顺序图号，必须由本次真实Binding Map解析。

**Color Authority Preservation（Current）：** Scene Color Authority必须保留，但Final Video不再把“保留Authority”等同于“占用Direct Reference槽”。Scene-bound Image / Shot Execution仍Visual-First；Final Video默认由已继承综合色的Primary Visual承担直接视觉状态，Scene Color Card先`LINEAGE_ONLY`，只有明确综合色风险/Provider/用户Trigger才升级`DIRECT_COLOR_REFERENCE`；必要时可`TEXT_COLOR_CONTROL`。`SCENE_COLOR_APPLIED_REFERENCE`仍只允许证据触发。

## 1｜核心原则

**Task First → Target First → Key Visible Asset Coverage → Most Direct Authority → Minimum Sufficient Reference Set。** 当前项目默认Reference能力类为`MULTIMODAL_ALL_ROUND_REFERENCE`，因此Resolver可以跨图片与音频选择最直接Authority；**参考视频在项目层硬禁用**，不得进入候选集。

“这个资产属于当前Scene”不是加入理由。每张Reference必须回答：
- `Why Now`：当前任务为什么需要它；
- `What Field`：它控制哪个当前字段；
- `Most Direct`：它是不是当前最直接可用Authority。

答不出来 → 先判断它是否仍含当前镜头必需信息。若没有才`OMIT REFERENCE`；若有，先尝试最直接视觉路由（Direct Bind / Panel / Crop / Assembly / Previs Anchor）；只有目标模型实测不适合原Reference时才执行`ROUTE CHANGE → PRESERVE REQUIRED FIELDS → REMAP`。

## 1.1｜Key Visible Asset Coverage Gate（关键可见资产覆盖闸门）

Resolve前必须读取`reference_field_coverage_map.md`：
- 先列当前Stage 04/05真正会被清楚看到或参与动作的关键人物、Environment方向、Prop / Weapon / Vehicle / Entity / Persistent State；
- 再决定各字段由哪个最直接Approved Reference承担；
- **不是为了Reference Pack短就删关键资产。** 多张有独立职责的Reference完全合法；
- 任一Critical Field没有视觉Authority → `REFERENCE_COVERAGE_GAP`，返回上游补资产；
- 槽位不足且无法通过Assembly/Anchor/TEXT_CONTROL重组 → `REFERENCE_SLOT_OVERFLOW`，不得静默删除关键图。

---


## Current｜Style Continuity Authority Resolve

当Task属于补图、重建、Revision、Derived Coverage、Support、Assembly、FMH延续、Storyboard/Video风格承接时，`REQUIRED AUTHORITY FIELDS`必须显式包含`STYLE_CONTINUITY`。

Style Continuity视觉证据优先：
1. 同一对象的Approved Parent / Revision Source；
2. 同一Scene / 同一视觉家族的Approved正式图；
3. Approved Render Style Evidence / Style Applied Clean Reference；
4. Current `VERIFIED_VISUAL_STYLE_FINGERPRINT`（文字Sidecar，特别供Blind/低视觉执行端复用）；
5. `project_style_dna.md`文字Authority。

目标平台支持视觉Reference且1–3存在时，不得把STYLE_CONTINUITY自动降为TEXT_ONLY。Style Board可以按Capability/Role直接绑定；只有**已观察到**样例内容串入/版式直译、`ROLE_SEPARATION=VERIFIED_FAIL`且已造成越权、已证明槽位冲突或用户明确要求时才改Clean Crop或Style Applied Reference。Resolve完成后运行`style_authority_projection_gate.md`决定MINIMAL或FULL文字量。

失败：`STYLE_EVIDENCE_BINDING_GAP / STYLE_CONTINUITY_RISK_IGNORED`。

## 2｜Current Authority术语

### Approved HD Object Authority
进入模型的高清对象Authority统一标记：

`HD_OBJECT_AUTHORITY_IMAGE`

它可以是：
- Character / Transformation / Detail Master（包括Approved AD-01 Signature Adornment Detail）；
- Environment / Prop / Weapon Canon Master；
- **Approved Environment / Prop Derived Coverage**；
- 当前任务需要的其他高清对象Detail Authority。

**Parent Master不天然高于Derived Coverage。** 同一字段优先当前Task最直接的Approved高清Authority。


### Approved Shot Assembly Authority
进入模型标记：`HD_SHOT_ASSEMBLY_IMAGE`。它只控制多人关系、人景物组装、空间占位与Montage情境；它不是对象Canon，也不是Storyboard。

### Control Reference
- Storyboard → Shot / Composition / Action Anchor；
- Ending Frame → 起始Continuity；
- Render Style Anchor → 绘画语言；
- Cinematic Shot Style Anchor → 项目级摄影语法，不覆盖具体Storyboard；
- Global / Scene Color Reference → 当前综合色；Shot Lighting Variant通常TEXT_CONTROL。

输入模式：
`HD_OBJECT_AUTHORITY_IMAGE / HD_PRODUCTION_SUPPORT_IMAGE / HD_SHOT_ASSEMBLY_IMAGE / CONTROL_IMAGE / CONTROL_CROP / TEXT_CONTROL`

`HD_PRODUCTION_SUPPORT_IMAGE`只用于已批准的Production Support Reference / Additional Video Conditioning Keyframe：可成为当前Interaction / Contact / Transient State / Scoped Minor Prop Appearance / Shot Detail字段的PRIMARY；除明确限定Scope的轻量小道具外，不能覆盖Character Identity、Object Canon Structure或Environment Geography。

`HD_SHOT_ASSEMBLY_IMAGE`只用于已批准的`SHOT_ASSEMBLY_ASSET`：可成为当前多人物关系、人物-场景-道具组合、Montage情境同框、空间占位关系的PRIMARY或SUPPORT；任何清楚可见的一次性`SCOPED_CAST / NON_RECURRING`都必须先有Approved FMH/Minor Human Master，Assembly只继承其Appearance并控制当前组合关系。它不是Storyboard，不控制剪辑节奏，也不能反向改写已有Canon。

## 3｜Stage 03 Binding

### NEW_CANON_MASTER
只加入建立新Master真正需要的Canon / Identity / Project Style信息。不因Scene里还有其他角色/道具就全部上传。


### PERSONAL_ADORNMENT_DETAIL / AD-01
- Approved Character / Current LOOK = Identity + placement context source；
- Approved Adornment Identity Card / Closet AC record = Shape / Material / Wear / left-right source；
- 输出AD-01后进入`HD_OBJECT_AUTHORITY_IMAGE / DETAIL_AUTHORITY / PERSONAL_ADORNMENT_AUTHORITY`；
- 不重设计人物、服装或装饰；若物件已变成剧情Prop则停止AD-01并改走Prop Authority。

### FUNCTIONAL_MINOR_HUMAN_ASSET
- Stage 02 `SCOPED_CAST_BRIEF` = PRIMARY TEXT AUTHORITY；
- Project Style / 当前Scene Color = STYLE/COLOR only；
- 不引用主角Character Master来“告诉模型不要长成主角”；匿名边界用正向Scoped Appearance + 必要最短Identity Exclusion表达；
- 输出为`APPROVED SCOPED FIGURE / HD_OBJECT_AUTHORITY_IMAGE / SCOPED_CHARACTER_APPEARANCE_AUTHORITY`，只在登记Scope内有效；
- 如果当前真正需要的人物-场景-道具位置关系仍高风险，保留Standalone FMH作为Appearance Authority，并额外走`SHOT_ASSEMBLY_ASSET`锁组合关系。

### DERIVED_COVERAGE
- Parent Canon Master = PRIMARY CANON SOURCE；
- Structure / Geography Spec = TEXT Authority；
- Triggered Shot = Camera / Visible Side / State目标；
- 任务完成后新Coverage成为该视角的Approved HD Object Authority。

### REVISION_IMAGE / LOCAL_PATCH
- 当前QC失败Candidate / 待修改图 = `EDIT_TARGET / REVISION_SOURCE` = PRIMARY；
- Patch Design Authority按需加入；
- Parent Master只在需要锁Canon字段时SUPPORT；
- 不得只@Parent Master却声称是在修改失败图。

### PRODUCTION_SUPPORT_REF
- 当前Support Target本身不存在，不能把别的Support冒充目标；
- 使用最直接Approved Canon/Coverage/State Authorities作为Parent Source；
- Triggered Shot / Video Risk Contract定义Interaction / Contact / Transient State / Entity Action / Scoped Minor Prop / Shot Detail目标；
- 只生成已授权风险字段，不重设计Canon。

### SHOT_ASSEMBLY_ASSET
- 反复/命名人物使用已批准Character Authority；一次性`SCOPED_CAST / NON_RECURRING`可使用Stage 02 Scoped Cast Brief；Environment / 关键Prop / State仍使用已批准Authority；
- Assembly Brief说明需要稳定的人景物关系，而不是具体剪辑；
- 输出为`HD_SHOT_ASSEMBLY_IMAGE`；
- 不得把Storyboard宫格直接上传并声明是在做Assembly。

### FRESH_REGEN
只有明确放弃失败Candidate、从Approved Authority重新出新候选时使用。不得包装成Revision。

## 4｜Stage 04 Storyboard Binding

**先做Reference Field Coverage Map，再做裁剪。** 当前Segment如果清楚出现3个主要人物、1个关键道具和当前场景反拍，就必须分别确认这些字段由什么Authority承担；不能因为Assembly存在就默认它自动代替所有人物身份，也不能因为想少传图就删掉关键道具。

只选择当前Segment真正可见且对Panel执行有职责的Reference：
- 当前入镜反复/命名人物需要身份锁定时加入对应Character Authority；一次性`SCOPED_CAST / NON_RECURRING`只要清楚可见，必须由Approved FMH/Minor Human Master承担Appearance Authority；Approved Assembly或Previs只能补Placement/Pose/Contact，不得替代人物母图；
- 若稳定Personal Adornment在Panel中清楚可读且承担身份识别：先检查Current Look是否足够；足够则用Current Look，不足且有Approved AD-01则AD-01=MUST；不足且无AD-01则`ADORNMENT_ASSET_GAP`回Stage 03，不能让Storyboard重猜；
- 若变身人物眼妆/瞳孔在Panel中可读或本Beat强调眼部，`TE-03 = PRIMARY TRANSFORMATION_EYE_SIGNATURE / MUSICAL_EYE_MOTIF AUTHORITY`；TF-01只负责整体变身身份，不能代替TE-03细节；
- Environment先找当前Camera Direction最匹配的Approved Coverage；没有Coverage或Coverage缺必要Canon字段时才加入Parent Canon Master；
- Prop同理，优先当前Visible Side / Interaction / State对应Coverage；
- CONTINUITY_ENTRY按需使用真实Previous Ending Frame；
- CUT_ENTRY / SCENE_OPENING不机械加入Ending Frame；
- Style DNA文字规则常驻；Render Style图像只在绘画方法确实需要时CONDITIONAL；Cinematic Shot Style只在当前镜头语法需要、且不与Storyboard具体Camera冲突时CONDITIONAL；
- 当前Scene若已有Approved Scene Color Extension，优先它承担综合色控制；Global Color Card通常转TEXT Authority，不机械一起上传。

Storyboard Revision必须把待修改Storyboard作为EDIT_TARGET。

若当前Segment已有Approved `SHOT_ASSEMBLY_ASSET`，并且Storyboard主要难点在多人同框/空间占位/人景物组合关系，可将其作为高质量关系参考；但具体机位关系继承`DIRECTOR SPATIAL RECONCILED`的Detailed Shot Contract；Storyboard只负责Panel级执行/精化。

所有正式Shot在Approved Clean Storyboard后建立最小Primary Video Conditioning。若复杂度要求额外Keyframe，则该Frame继承Approved Storyboard构图/Blocking、SPATIAL_CANON与最直接对象Authority；通过后登记`APPROVED_VIDEO_CONDITIONING`并按其Frame Role成为对应时间点Primary Visual，不得反向改Storyboard或Canon。


## V4.4｜Stage 05 Two-Layer Reference Resolve

Final Video Resolve必须先建立：

`Layer A = PRIMARY_VISUAL_CONDITIONING`
`Layer B = AUXILIARY_FIELD_AUTHORITIES`

Layer A每个Video Unit至少一个Approved/Promoted Shot-specific Primary Visual。Layer B继续允许Character/Environment/Design/Color/Style/Storyboard/Continuity直接视觉绑定。

**禁止逻辑：** 不能因为Layer B字段覆盖率达到100%，就把Layer A判为可省略。`Environment Master + Color Board + Design Board + Whole Storyboard`仍然可能完整覆盖“字段”，但没有定义最终第一帧；这种情况必须`PRIMARY_VISUAL_CONDITIONING_GAP`。

Primary Visual只接管它已经静态证明的Composition / Blocking / Current State / Exact Composite字段；Storyboard独有的Temporal/Cut/Action Sequence继续保留，Character/Environment/Color/Style的Canon字段也继续按需保留。

## 5｜Stage 05 Final Video Binding

**Final Video优先保证关键可见资产完整。** 当前镜头实际会出现且可读的主要人物、关键Prop / Weapon / Vehicle / Entity、Persistent State、当前Environment方向必须全部在Field Coverage Map中为YES，之后才做Reference去重。

### Character
只加入当前真正入镜、且模型需要身份/造型视觉Authority的人物。专项脸/眼/变身/武器Detail不机械全套上传，但**一旦眼妆/瞳孔达到可辨识程度或属于剧情重点，TE-03不是“可省细节”，而是Critical Eye Authority。**

Personal Adornment Visibility：
- 装饰太小不可辨识 → 不机械追加AD-01；
- 装饰清楚可读且属于Identity，但Current Look已足够锁定 → Current Look承担`PERSONAL_ADORNMENT`，AD-01可OMIT；
- 装饰清楚可读、Current Look不足、Approved AD-01存在 → `AD-01 = MUST / PRIMARY PERSONAL_ADORNMENT_AUTHORITY`；
- 装饰清楚可读、Current Look不足且无AD-01 → `ADORNMENT_ASSET_GAP`，禁止继续Final Video Prompt。

Transformation Eye Visibility：
- Wide / Full Body且眼部不可辨识 → TF-01通常足够；
- Medium且Primary Eye Signature可读 → TE-03加入；
- MCU / CU / ECU / 变身完成 / 眼部启动 / 战斗眼神 / 关键情绪Close-up → TE-03 MUST；
- TE-03负责`TRANSFORMATION_EYE_SIGNATURE / MUSICAL_EYE_MOTIF`，不得由低清Storyboard、泛化TF-01或文字重新猜。

### Environment
1. 读取当前Shot Camera Side / Zone；

若当前Video主要风险是多人关系或人景物组合容易被猜错，并且已存在Approved `SHOT_ASSEMBLY_ASSET`，可将其作为`HD_SHOT_ASSEMBLY_IMAGE`加入；若已有Approved `VIDEO_FIRST_FRAME / VIDEO_SHOT_EXECUTION_FRAME / VIDEO_TARGET_FRAME`，它作为Primary Visual；Assembly/Anchor按仍独占字段继续Support。

2. 查Approved Derived Coverage；
3. 有匹配Coverage → Coverage = PRIMARY `SHOT_VIEW_AUTHORITY`；
4. Parent Canon Master只有Coverage仍缺固定结构字段时SUPPORT；
5. Coverage足够唯一 → Parent OMIT / TEXT-ONLY。

### Prop / Weapon
1. 读取当前Visible Side / Interaction / State；
2. 有匹配Coverage → Coverage PRIMARY；
3. Parent Master只补仍独有Canon字段；
4. 不上传正/背/侧全套“求保险”。

### Shot Assembly / Production Support / Additional Video Conditioning Keyframe
- 当前Shot存在Approved Stage 03 Production Support时，只在它直接解决当前Interaction / Contact / Transient State / Entity Action / Scoped Minor Prop / Shot Detail字段时加入；
- 当前Shot存在Approved `VIDEO_CONDITIONING_KEYFRAME`时，它可作为`HD_PRODUCTION_SUPPORT_IMAGE`承担Exact Shot Composite / Contact / Composition Execution；
- Support图不能取代Identity / Object Structure / Geography Authority；Assembly对反复/命名人物不能取代Character Identity，对Readable `SCOPED_CAST`同样不能取代Approved FMH/Minor Human Master的Base Appearance Authority；冲突时回到对应Approved Canon/Coverage；
- Video Conditioning Frame已经把当前Storyboard某个时间点的构图/接触字段高保真落实时，只对这些**已覆盖字段**去重；Storyboard仍独占Temporal Beat / Action Sequence /多Panel状态递进，避免“单帧替代时间序列”。

### Mandatory Storyboard / Approved Previs
必须先验证`APPROVED MANDATORY SHOT STORYBOARD`覆盖当前Segment全部Shot；若缺任何Shot，禁止Stage 05 Resolve并返回Stage 04。随后执行`APPROVED PREVIS SET`，Mandatory Board与每个Required Supplemental Component均先视为**视觉控制候选**，不能默认降成TEXT_CONTROL。Stage 05按`MODEL REFERENCE CAPABILITY PROFILE + REFERENCE ROUTING MANIFEST`选择：`DIRECT_STORYBOARD_BOARD / PANEL_MULTI_REFERENCE / KEY_PANEL_SELECTION / FIRST_LAST_FRAME / CLEAN_PANEL_CROP`。只有某个Storyboard字段已被更直接视觉Authority完整接管，或目标平台客观不支持该字段所需视觉Reference时，才可对**该字段**降为TEXT_CONTROL；若Storyboard仍独占Temporal/Action Sequence，必须保留相应Board/Panel/Keyframe视觉控制。整Board / Map / Sheet是否直用只由当前Capability、Role和真实Literalization证据裁决。

### Previous Ending Frame
先读取Entry Mode：
- `CONTINUITY_ENTRY`且要求同一Camera/同一Take无缝延续：Continuity Authority = MUST，Verified Ending Anchor按Temporal Hygiene成为唯一model`t=0`视觉Owner；
- `CUT_ENTRY / CUT_REPROJECT`：默认不直接上传Ending Frame。使用`STORYBOARD_BLOCKING_APPROXIMATE`桥接Approved Storyboard Exit/Entry与World Spatial State；下一镜的高清人物、环境和Shot Execution Frame接管最终像素。只有Locked Editorial Plan明确要求像素级Match且污染评估通过时才允许例外Direct；
- `SCENE_OPENING`：不加入上一Scene尾帧。

`STORYBOARD_BLOCKING_APPROXIMATE`最低保留：人物在场集合、世界Zone/Anchor、画面侧或动作方向、深度、朝向、动作Phase、关键接触、道具Holder与数量。Cut后的微姿态、衣褶、粒子相位、纹理、压缩噪声和非剧情性综合色允许变化。过渡由Locked Editorial Plan中的`MATCH_ON_ACTION / CUT_REFRAME / REACTION_CUT / SPATIAL_REORIENTATION / J-CUT / L-CUT / SOUND_BRIDGE / SHAPE_OR_DIRECTION_MATCH`承担，不能为了追逐逐像素一致把低清尾帧带入新镜头。

### Style / Color
- Project Style DNA = TEXT Authority；
- Render Style Anchor图片 = CONDITIONAL，只控制绘画语言；
- Cinematic Shot Style Anchor图片 = CONDITIONAL，只控制项目级摄影语法；Approved Storyboard的具体Camera/Blocking优先；
- 当前Scene已有Approved Scene Color Extension → 它始终是综合色Authority；**Stage 03 Scene-bound Image与Shot Execution继续Visual-First，Stage 05 Final Video默认不重复占色卡槽。** 若Primary Visual的`scene_color_authority_id`匹配且没有综合色风险Trigger，`scene_color_reference_mode = LINEAGE_ONLY`；
- 若综合色是剧情识别信息、已观察Video综合色漂移、Multi-shot换机位时已知漂色、Primary Visual本身综合色不可靠、Provider明确要求或用户明确要求 → `DIRECT_REFERENCE`；若Direct不受支持/槽位压力但文字可以稳定控制 → `TEXT_CONTROL`；
- Global Card通常不与Scene Card平权叠加；没有Scene Color Authority本身仍是Hard Gap，不能用“少占槽”作为丢Authority的理由；
- Shot Lighting Variant默认TEXT_CONTROL；只有重复、高风险且已批准的Lighting Reference才上传；
- Style / Color图都不承担对象Canon清晰度/结构Authority。Reference Resolver优化的是**Direct Input数量**，不是删除上游Authority。

## 5.0.5｜Video Reference Budget Priority

Final Video按`MINIMUM_SUFFICIENT_REFERENCE_SET`选择Direct Inputs，不按“已有多少Authority就上传多少图”执行。默认优先级：

- `P0 CONTINUITY STATE`：只有Entry连续性真正需要时进入，如Previous Approved Ending Frame；
- `P1 PRIMARY SHOT VISUAL`：Approved Shot Execution / First Frame，默认必须；
- `P1 HIGH-RISK IDENTITY / GEOMETRY`：当前镜头确有漂移风险时加入Character / Critical Prop / Nearest Environment Authority；
- `P2 COLOR / STYLE`：只有当前字段无法被Primary Visual稳定承载、风险Trigger成立或Provider要求时才占Direct槽；
- `P3 AUXILIARY COMPOSITION / MOOD`：槽位压力时最先移除或转TEXT。

**Scene Color Card默认不预占P2槽。** Authority仍存在于Lineage；如果Direct槽可以更有效地用于Prop Reverse、Environment Reverse、Character Identity或Continuity Entry，优先给这些当前独占字段。

## 5.1｜Reference Field Preservation on Route Change

只有当前`visual_reference_routing.md`已经基于**明确平台不兼容、VERIFIED_FAIL、已观察Literalization/Sample Bleed、已证明槽位冲突或用户明确要求**选择非Direct路线时，才对复合Reference做Route Change。Route Change不能把该Reference仍独占的必要字段一起删掉；必须逐字段Preserve并Remap到Panel / Crop / Applied / Text / 其他更直接Visual Owner。

综合色卡、多宫格Storyboard / Montage整板、人群档案、Style/Color Board都遵守此规则。单纯“担心污染 / UNKNOWN / 为保险”不构成Route Change依据。

**综合色卡特殊规则：** Required Scene Color Authority不能丢失。Scene-bound Image / Shot Execution按Visual-First直接绑定；Final Video默认`LINEAGE_ONLY`，综合色风险Trigger成立才Direct，Direct不适合或槽位压力时可`TEXT_CONTROL`。`UNKNOWN`不触发Applied，也不强制Final Video占色卡槽；Role Separation失败优先Color-Only Crop / Dedicated Channel。

## 5.2｜Functional Minor Human Handling（匿名/功能性小人物处理）

只要画面中存在**非主角、但承担构图/氛围/因果/视线引导/情绪见证职责**的人物，就必须读取`functional_minor_human_asset_protocol.md`。

规则：
- “不是主角”不等于“可以让模型随便长”；
- 反复/命名人物仍走正式Character Authority；
- 一次性功能人物只要清楚可见，必须由最小`Functional Minor Human Asset / Minor Human Master`承担Appearance Authority；Approved Shot Assembly、Mandatory Storyboard和Rendered Human Pose Anchor只能补组合、站位、姿态和动作证据；
- 若当前Shot明确需要这类人物且其清楚可见，但Reference Pack里没有与Stage 02 Visual Owner一致的Approved FMH/Minor Human Master覆盖Base Appearance → `FUNCTIONAL_MINOR_HUMAN_GAP`；Assembly / Approved Previs Human Anchor只能在FMH已存在后补关系、姿态、Blocking或Contact；
- Final Video Prompt里不得只写“禁止其他人”，却又希望画面拥有街道生命感或既定匿名见证者。

## 6｜Scene Runtime Pack不是最终Reference Pack

Scene Pack只是一组**候选调用索引**，不代表每个Segment都要上传里面所有图。

具体Segment必须重新做Task-Bound过滤：

`Scene Runtime Pack + World State Delta + Segment Delta → Key Visible Asset Register → Field Coverage → Eligibility Test → Entry Mode → Storyboard Control → Minimum Sufficient Reference Pack`

规则：
- Scene Pack里的Character / Environment / Prop如果当前不入镜或没有当前字段职责 → OMIT；
- Approved Storyboard只在Stage 05存在且对当前Segment有效时作为Control Source；
- Previous Ending Frame只由Entry Mode决定，不在Scene Pack Delta中默认加入；
- 任何缓存项发生Version/子空间/Persistent State变化则重新Resolve。

## 7｜Negative Relevance Gate

具体人物、地点、怪物、道具或未来Beat元素进入模型负面Prompt前，必须存在真实污染路径：
- 当前上传Reference里实际包含；
- 当前Continuity Source里实际包含且本Shot必须移除；
- 当前文字描述存在明确诱发歧义；
- Failure Diagnosis已证明模型反复错误生成。

否则留在内部Shot Scope，不进入模型正文。

**Absent-from-input ≠ needs-negative。**

## 8｜Reference Budget

排序按**字段职责**而不是“图的级别”机械排：
1. EDIT_TARGET / REVISION_SOURCE（Revision时绝对优先）；
2. 当前字段最直接的Approved Authority：Identity/Structure/Geography优先`HD_OBJECT_AUTHORITY_IMAGE`；Interaction/Contact/Transient State/Scoped Minor Prop/Shot Detail/Exact Shot Composite可优先`HD_PRODUCTION_SUPPORT_IMAGE`；Multi-character Relation / Scene-Character-Prop Assembly可优先`HD_SHOT_ASSEMBLY_IMAGE`；
3. 必要Continuity Control；
4. 必要Storyboard Control（已有Additional Video Conditioning Keyframe时按字段去重；Storyboard独有Temporal/Action Sequence仍保留视觉控制）；
5. 必要Render Style / Cinematic Shot Style / 当前最直接Color Control。

只有当所有Critical / Required Authority Fields都已被充分、互不冲突地覆盖，且新增Reference不再增加必要字段时，**才Stop Adding**。关键资产多时允许Reference Pack自然变大；不要为了短而漏。

## 9｜Executor Input Map + Prompt Projection

Resolver内部必须建立真实输入映射：

```text
INPUT SLOT / PLATFORM HANDLE：<真实绑定>
ASSET ID / VERSION：<内部追踪>
INPUT MODE：<HD_OBJECT_AUTHORITY_IMAGE / CONTROL_IMAGE / ...>
SEMANTIC ROLE：<Character identity / Environment / Composition / Color / Continuity / ...>
RESPONSIBILITY：<唯一当前字段>
```

随后读取`execution_reference_semantics.md`：
- **Generation Prompt**：不输出Semantic Role / Responsibility行政表；把其有效字段消解进主体、空间、综合色、构图、Entry或Timeline。Current Generation Profile下，强绑定Approved Asset必须保留真实`@资产`Mention + 最短执行句；
- **Web QC Copy Prompt**：因网页版需要指向本批真实上传证据，允许按本批实际上传顺序动态生成`@图1 / @图2 / ...`；TEXT_CONTROL不占图片编号；
- **Workspace / Snapshot / Upload List**：继续保存精确Asset ID / Version /真实文件映射。

任何Generation模板若把Native Token位置固定绑定为某一Semantic Role，或把内部资产名复制给模型，均视为Reference Mapping错误。

## 10｜Hard Gates

### REFERENCE_RELEVANCE_FAIL
- 没有Why Now；
- 有更直接Coverage却无理由用泛化Parent Master；
- 上传与当前可见字段无关的资产；
- Scene Pack候选未经Task过滤直接全塞。

### REVISION_TARGET_BINDING_FAIL
- 声称修改某Candidate，却没有把该Candidate作为EDIT_TARGET / REVISION_SOURCE；
- Parent Master冒充待修改图；
- Storyboard局部修改不上传待修改Storyboard。

### NEGATIVE_RELEVANCE_FAIL
- 负面Prompt点名当前输入不存在且无污染路径的实体；
- 把未来Beat整段元素列为“禁止出现”；
- 只写禁止、不写合法替代：若真实需求是“不要额外路人，但保留1名马路对面模糊孩子剪影”，则必须编译为`Forbid + Replacement`而不是单纯删空。

### SUPPORT_REFERENCE_AUTHORITY_FAIL
- Production Support / Shot Anchor重设计Canon；
- Support承担未授权Identity / Object Structure / Geography；
- Shot Anchor改变Approved Storyboard；
- 同一字段风险由Coverage / Support / Anchor平权重复承担并互相冲突。

### SHOT_ASSEMBLY_AUTHORITY_FAIL
- Shot Assembly改写已有反复/命名人物Identity、Object Structure或Environment Geography；
- `SCOPED_CAST`外观被带出授权Scene/Shot Group继续使用；
- Storyboard宫格被直接放大/清稿冒充Assembly；
- Assembly与其他Authority在同一字段平权冲突。


### REFERENCE_COVERAGE_GAP
- Key Visible Asset Register存在Critical资产，但Reference Pack没有覆盖；
- Assembly/Anchor没有覆盖某字段，却把对象自己的Authority删掉；
- 为了压缩@数量而遗漏主要角色、关键道具/武器/怪物、当前空间方向或持久状态。

### REFERENCE_SLOT_OVERFLOW
- 所有关键资产都需要，但输入槽位不足；
- 先删真实冗余、用TEXT_CONTROL、Approved Assembly/Anchor重组；仍不足则回上游处理，禁止静默删关键图。

### REFERENCE_FIDELITY_FAIL
- 控制图承担对象高清细节；
- Parent Master仅凭“母图身份”抢走更直接Shot Coverage；
- Render/Cinematic Style或Color Reference承担清晰度/锐度/完成质量；
- Cinematic Shot Style覆盖具体Storyboard Camera；
- Global / Scene / Shot综合色参考无必要同时堆叠；
- 低清图被放大后冒充高清对象Authority。

## 11｜标准案例

### 舞台左后方打斗
已有`ENV_STAGE_CV_LEFT_REVERSE`：
- PRIMARY = Left-Reverse Coverage；
- 正面Canon Master只有Coverage缺固定结构字段时SUPPORT；
- 否则不@正面母图。

### 打开怀表特写
已有`PROP_WATCH_CV_OPEN_INSERT`：
- PRIMARY = Open-Insert Coverage；
- 闭合正面Master不是默认输入。

### QC失败图轻微修手
- PRIMARY = 当前失败Candidate；
- 必要手部/道具Authority = SUPPORT；
- Parent Character/Prop Master只按具体Canon需求加入。

## 12｜Stop Rule

**最好的Reference Pack不是图最少，而是关键可见资产全部有Authority、且每一张都回答一个当前必须回答的问题。**


### ADORNMENT_ASSET_GAP
当前镜头Personal Adornment为Critical，Current Look不足以承担且缺Approved AD-01。返回Stage 03补最小Detail Authority并Re-Freeze。


## Current｜Model-Facing Surface Handoff

Resolver输出的是**内部Reference决策**，不是最终生成Prompt文本。`MUST_BIND / Authority / Input Mode / Asset ID / Version / Why Now / Most Direct`不得原样复制给模型。Resolver完成后交给`execution_reference_semantics.md`与`model_facing_prompt_surface_sanitizer.md`：先完成真实绑定，再把控制字段消解进主体/空间/综合色/构图/Entry/Timeline。Stage 05还必须先完成Reference Capability/Role Routing，再允许原生Token投影。

## Current｜Reference Binding Content-Role Verification

Resolver完成内部Asset Authority后还不等于**实际生成器绑定内容**已经确认。Stage 03 / 04 / 05及Revision只要实际绑定视觉Reference（UI Slot / Attachment Order / Native Token / API Handle等），编译前必须继续读取`reference_binding_semantic_verification.md`建立`REFERENCE BINDING CONTENT MAP`。文件名、Registry、历史上传顺序或“正文里没有@Token”都不能替代当前Binding内容证据。`REFERENCE_CONTENT_ROLE_CONFLICT / REFERENCE_BINDING_UNVERIFIED`未解决不得进入生成。


## V4.5.3｜Text-only Visual Evidence Resolve

当`controller_mode=TEXT_ONLY_CONTINUATION`时，任何Image Reference在Resolve前必须存在Fingerprint匹配的Current `VISUAL_EVIDENCE`。不得根据Asset名、生成Prompt或“以前用过”推断图片内容。先把Shot需求转换成`required_visual_facts / forbidden_visual_facts`，再用Evidence Fact Codes筛选资产；Evidence缺失或冲突则停止该Binding并进入`VISUAL_REVIEW_QUEUE`。

## V4.5.7｜Storyboard Entity Binding Resolve（新增）

Stage 05读取`STORYBOARD_ENTITY_BINDING_MAP`，先把匿名Slot还原为真实实体，再执行项目策略：

`reference_policy = FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING`。

对于Scene-bound Video，Authority Set固定包含：`Shot-specific Primary Visual血缘 + 当前Empty Environment Master + 每个清楚可见Human的独立Character/FMH Master + 当前Approved白描Storyboard Control`；但Authority Set不等于全部上传。Target Adapter按字段唯一Owner决定Direct Pack。即梦 Seedance 2.0全能参考中，高清人物/场景母图保留Direct；Storyboard可Direct但只锁动作/Blocking/CUT；若Primary只是重复合成同一字段，则保留Evidence而不上传。

硬规则：
1. Slot与Entity是一对一稳定绑定；反打后不得因为Screen Left/Right变化交换身份；
2. `world_zone / anchor relation`是世界事实，`frame_region`只是Camera Projection；
3. Scene-bound Video中，Environment Slot与所有清楚可见Human Slot禁止`PRIMARY_VISUAL_BAKED / TEXT_CONTROL / OMITTED`，必须=`DIRECT_REFERENCE`；Primary不得替代基础Authority，并允许按Provider Route=`OMIT_REDUNDANT_BAKED_COMPOSITE`；
4. Environment Slot选择与当前Location一致的Approved `EMPTY_ENVIRONMENT_MASTER`；Human Slot选择该Entity自己的Approved `CHARACTER_MASTER / FUNCTIONAL_MINOR_HUMAN_ASSET / MINOR_HUMAN_MASTER`，禁止选择当前Primary Visual冒充人物母图；
5. 当前Approved白描Storyboard Panel/Board必须进入Stage 05 Handoff；当Provider支持且其Temporal/Blocking字段仍有独占价值时Direct，并在Prompt明确不继承白描画风、人物身份、纹理或最终画质；若这些字段已被更直接视觉Authority完整接管，可按字段转为Prompt Control，但必须保留可审计闭合；
6. Direct Reference必须落到真实Approved Asset + Native `@Token`，并进入`Generation Job.required_bindings`；每个Token在Final Prompt中准确出现一次；
7. 平台Direct槽不足或Reference字段竞争时，先删冗余合成Primary，再压缩非独占辅助Reference；空场景和清楚可见人物母图不得删除。无法闭合时报`PROVIDER_ROUTED_BINDING_BUDGET_OR_FIELD_CONFLICT`并BLOCK；
8. 最终Prompt只出现真实实体名称/动作和真实`@资产`，绝不出现`H_A / P_A / E_A`等内部Slot。

确定性解析工具：`tools/entity_binding_reference_resolver.py`；当当前Camera/Visible Side需要从多视角Canon选择父级时，先运行`tools/nearest_spatial_visual_parent_router.py`。



## V4.5.7｜Rich Library ≠ Large Direct Pack

Stage 03允许建立完整的空场景母图、配角人物母图、Coverage/View Set；资产库丰富不等于Stage 05全部直接@。Resolver必须从完整Asset Registry中按当前Camera / Action / Visible Surface / Identity Risk挑选Minimum Sufficient Reference Pack。Base Authority保证“有正确答案可选”，Reference Budget决定“这一镜实际发送哪几张”。

## V4.5.7｜Identity Readability Override（不可被Reference Budget覆盖）

在决定`PRIMARY_VISUAL_BAKED`前，Resolver必须读取当前Shot的`IDENTITY_READABILITY_ASSESSMENT`：

- 对Required Human为PASS：允许继续用Primary Visual承载该人物Identity；
- 为FAIL/UNKNOWN：禁止`PRIMARY_VISUAL_BAKED`作为唯一Identity路线，强制升级`DIRECT_REFERENCE`到该人物Approved Character/FMH Identity Authority，或返回Stage 04B重生Primary Visual；
- 该Direct Identity Authority属于P1，不得为了Reference Budget省槽被Storyboard、Environment Master或纯文字替代；
- 白描只提供Blocking/Timing，空场景只提供Spatial Authority，均不能消除`IDENTITY_READABILITY_FAIL`。

## 1.2｜All-Round Multimodal Role Routing

默认视频模型能力类：`MULTIMODAL_ALL_ROUND_REFERENCE`。Resolver先按**事实Owner与风险**决定Reference Role，再按Provider能力映射成真实输入。

`CHARACTER_IDENTITY → Character/FMH Image`
`ENVIRONMENT_GEOMETRY → Empty Environment Master / Visual Anchor Image`
`PROP_STRUCTURE → Prop Canon/View Image`
`BLOCKING_TIMING → Approved Storyboard Panel/Metadata`
`CURRENT_COMPOSITE → Shot Execution Frame`
`CONTINUITY_ENTRY → Previous Approved Ending Frame`
`MOTION_CAMERA_DYNAMICS → Storyboard / Action Key Pose / Camera Path Metadata / Text Control（NO REFERENCE VIDEO）`
`AUDIO_TIMING / VOICE / RHYTHM / AMBIENCE → AUDIO_ASSET_MANIFEST中的Approved Audio Reference`

硬边界：Storyboard不能补Character Identity；空场景不能补Character Identity；Primary Visual发生`IDENTITY_READABILITY_FAIL`时必须补对应人物Identity Authority或重生可辨执行帧。即使Provider为全能参考，这些Authority边界也不合并。


## V4.5.7｜Reference Video Hard Ban

`REFERENCE_VIDEO_POLICY = FORBIDDEN_QUOTA_COST`。任何`media_kind=VIDEO`资产都不得进入Video Generation Job的Reference Binding，包括动作参考视频、运镜参考视频、表演参考视频和此前生成的视频片段。动作/运镜控制必须改用Storyboard、Action Key Pose、Camera Path Metadata、Previous Ending Frame静帧与文字约束。

音频Reference是允许的，但必须来自`AUDIO_ASSET_MANIFEST`中的Approved记录；Resolver不得直接从文件系统临时抓一个音频就`@`。

## V4.5.7｜Performance / Narrative FX Resolve

Stage 03的资产库完整性与Stage 05的Direct Reference Budget必须严格分层：

`RICH CANON LIBRARY → current shot risk → MINIMUM_SUFFICIENT_REFERENCE_SET`。

新增两类可选但正式的静态Authority：

- `PERFORMANCE_SUPPORT_AUTHORITY`：只在当前Shot的特殊表情、姿态、持握或Contact仍有静态歧义时参与；不拥有人物Identity、Wardrobe、Timing或Camera Motion。
- `NARRATIVE_FX_AUTHORITY`：只在当前Shot存在已批准的剧情型FX视觉语法且Primary Visual不足以稳定其形态/状态时参与；不拥有Environment Geography、人物Identity或完整时间曲线。

Resolver规则：
1. 若Shot Execution Frame已经清楚吸收Performance Support或Narrative FX状态，则对应资产可`LINEAGE_ONLY / OMIT DIRECT`；
2. 若当前Primary Visual在关键表情/姿态/FX形态上仍有高风险，则选择最直接**单帧**Approved Support；
3. `MULTI_PANEL` Performance Sheet / Narrative FX State Sheet默认不直接送Video，先派生单帧或让Execution Frame吸收；
4. 不因为这些资产已在Stage 03生成就机械全部@；
5. 也不得反过来因为“单镜Reference Pack要小”而跳过Stage 03已经被Requirement标记为Required的资产生产；
6. 项目策略继续`REFERENCE_VIDEO_POLICY=FORBIDDEN_QUOTA_COST`，Performance与FX都不得借Reference Video实现。


## Current｜Provider-routed Field Authority Pack

《断弦之歌》不允许用“Primary已烘焙”省略空场景或人物母图，也不允许为了形式完整把所有Authority图都塞给模型。Reference Budget与Target Adapter共同裁决唯一字段Owner：高清基础母图优先，白描只锁动作/时序，重复合成Primary可不上传。即梦全能参考UI没有可靠权重控制时，`Reference越多越好`视为错误策略。
