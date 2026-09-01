# Task-Bound Reference Binding & Negative Relevance Engine（任务绑定式参考选择与负面相关性引擎）

> **用途：** 在Stage 03图片生成、Stage 04 Storyboard、Stage 05 Final Video、任何QC失败后的Revision / Local Patch之前，先回答“当前到底在生成/修改什么”，再决定真正应该绑定哪些图片输入，以及哪些具体禁止项值得进入模型Prompt。
>
> **核心原则：Task First → Target First → Key Visible Asset Coverage → Most Direct Authority → Minimum Sufficient References。**

---

## 1｜为什么需要本引擎

“同一个项目里存在这个资产”不等于“当前任务应该@它”。

常见错误：
- 当前Shot根本没有角色A/B/C，当前Storyboard、Ending Frame、Reference Pack也没有他们，却在Prompt里写“不要出现角色A/B/C”；这不会提供有效控制，反而把无关人物名称重新送入模型上下文。
- 当前打斗镜头拍舞台侧后方/台口反打，但因为“场景是剧院”，仍机械@舞台正面Hero Master；如果已有更贴近当前机位的Approved Coverage，这张正面母图只会争夺空间控制权。
- QC说“这张候选只需稍微改一下”，后续Prompt却重新@Parent Master，而没有把**真正要修改的失败候选**作为Revision Source / Edit Target；这实际上变成了“重新生成”，不是“修改当前图”。

本引擎把这些统一视为**Reference Binding错误**。

---

## 2｜Generation Task Contract（生成任务契约）

每次准备生成前必须先内部建立：

```text
TASK TYPE：NEW_CANON_MASTER / PERSONAL_ADORNMENT_DETAIL / DERIVED_COVERAGE / FUNCTIONAL_MINOR_HUMAN_ASSET / PERFORMANCE_SUPPORT_ASSET / NARRATIVE_FX_ASSET / PRODUCTION_SUPPORT_REF / SHOT_ASSEMBLY_ASSET /
           STORYBOARD / VIDEO_CONDITIONING_KEYFRAME / FINAL_VIDEO /
           REVISION_IMAGE / LOCAL_PATCH / VIDEO_RETRY / OTHER
OUTPUT TARGET：<Asset / Storyboard / Segment / Shot ID>
SHOT BINDING：<当前真实Shot(s)>
EDIT / REVISION SOURCE：<若是在改现有结果，必须指向那张真实候选>
VISIBLE / ACTIVE ENTITIES：<当前画面真正入镜或影响生成的角色/群体/道具/场景>
KEY VISIBLE ASSET REGISTER：<当前会被清楚看见、操作、特写或承担因果的关键人物/场景/道具/武器/实体/状态；含匿名但功能明确的小人物>
REQUIRED AUTHORITY FIELDS：<身份/服装/结构/当前视角/空间/动作/连续性/综合色/STYLE_CONTINUITY/局部设计...>
REFERENCE FIELD COVERAGE：<读取`reference_field_coverage_map.md`，逐字段标Critical/Covered>
REFERENCE CANDIDATE POOL：<可用APPROVED资产 + 当前Revision Candidate + Control References>
```

没有建立Task Contract，不得开始Reference Resolver。

---

## 2.1｜Reference Completeness Before Pruning（先保证完整，再删冗余）

Reference Resolver开始删图之前，必须先读取`reference_field_coverage_map.md`并完成Key Visible Asset Register。

**不能把“Most Direct / Minimum Sufficient”误读成“尽可能少上传图片”。**

- 当前镜头清楚出现的关键人物 → 必须有Identity/Current Look Authority；
- 当前镜头清楚可读且身份相关的Personal Adornment → 必须由Current Look或AD-01覆盖；Current Look不足且无AD-01时为`ADORNMENT_ASSET_GAP`；
- 当前镜头清楚出现/使用的关键道具、武器、载具、怪物 → 必须有对应结构/状态Authority；
- 当前Camera Side需要的Environment → 必须有当前最直接Master/Coverage；
- 当前Shot若`PERFORMANCE_ASSET_REQUIREMENT_SET`标记Required → 必须有Approved Performance Support；
- 当前剧情FX若`NARRATIVE_FX_ASSET_MANIFEST.authority_mode=NARRATIVE_FX_REFERENCE` → 必须有Approved Narrative FX视觉Authority；
- 复杂多人关系如果Assembly最直接 → Assembly加入；
- 具体Shot若Additional Video Conditioning Keyframe最直接 → Anchor加入；
- 只有“当前不关键、不可辨认、没有因果职责”的深背景对象才允许不建立人物母图；承担构图/氛围/见证/因果职责且清楚可见的人物，必须先由`Functional Minor Human Asset / Minor Human Master`覆盖。Assembly/Previs只补当前关系和动作。

任一Critical Field缺Authority → `REFERENCE_COVERAGE_GAP`，先回上游补资产，不得直接进入Prompt Compiler。

复合Reference的Authority字段不能无理由消失。对Final Video综合色卡，若Primary Visual已继承同一Scene Color Authority，则`LINEAGE_ONLY`是默认合法路由，不属于OMIT；其它Reference若改变Direct路线，仍必须逐字段`PRESERVE → REMAP`到Panel / Crop / Applied / Text / Approved Assembly / Functional Minor Human Asset等合法Owner。

---

## 2.2｜Scene Color Authority Preservation

场景绑定型图片/Storyboard/Video/Revision在Reference Pruning前必须读取`color_authority_preservation_gate.md`。如果当前Scene已有Approved Scene Color Card，或没有Scene Card但存在当前Scene明确继承的Scene-matched综合色基准：
- 独立建立`SCENE COLOR AUTHORITY SCAN`；
- Scene-bound Image / Shot Execution把最直接Scene Color视觉证据加入`MUST_BIND_COLOR_AUTHORITY`；Final Video先记录Authority与Primary Visual综合色血缘，默认不把色卡加入Direct Pack；
- Scene-bound Image / Shot Execution的复合色卡不得因担心污染就直接降TEXT-only；Final Video则先走`LINEAGE_ONLY`，只有综合色风险Trigger成立才Direct，或在Direct不合适/槽位压力时用`TEXT_CONTROL`。`UNKNOWN`既不强制Direct，也不触发Applied；
- Parent/Revision Source负责内容结构，不能被当成Scene Color Card的等价替代。

未解决`COLOR_AUTHORITY_BINDING_GAP`不得进入Prompt Compiler；但Final Video的`LINEAGE_ONLY`是合法已解决状态，不得误报成“色卡未绑定”。


## 2.3｜Style Continuity Field Coverage
正式视觉输出必须判断`STYLE_CONTINUITY = CRITICAL / SUPPORT / N/A`：
- 新Canon Master仍需继承Project Style DNA，因此通常至少SUPPORT；
- 补图、重建、Revision、Coverage、FMH/Support/Assembly延续默认CRITICAL；
- Final Video默认CRITICAL；
- 纯技术Map/Path可N/A。

CRITICAL时，Reference Candidate Pool必须优先寻找同对象Parent / Revision Source、同Scene Approved图、Approved Render Style Evidence，并由`style_authority_projection_gate.md`生成模型侧风格投影。`“保持同画风”`不算Field Coverage。

## 3｜Reference Eligibility Test（参考图资格测试）

每一张准备上传的图必须同时回答：

1. **Why Now：为什么当前任务现在需要它？**
2. **What Field：它具体控制哪个当前可见/可执行字段？**
3. **Most Direct：它是不是当前可用的最直接Authority？**

任一无法回答 → 先执行Information Retention Test：若该Reference不含当前任务仍必需字段才`OMIT REFERENCE`；若仍含必需字段，先证明Route Change依据，再逐字段`PRESERVE → REMAP`，禁止信息随图片一起蒸发。

### Reference Audit最小记录

```text
Reference：<ID / Version>
Role：<EDIT_TARGET / VIEW_AUTHORITY / IDENTITY / STRUCTURE / CONTINUITY / CONTROL / STYLE...>
Triggered By：<Shot / Revision Issue / Current Visible Field>
Why Now：<一句话>
Authority Fields：<只列真实字段>
Directness：PRIMARY / SUPPORT / TEXT-ONLY / OMIT
```

**“同场景”“同人物”“以后可能用到”“母图更正式”都不是Why Now。**

---

## 4｜Most Direct Authority优先级

同一字段存在多个Reference时，优先选择对当前任务**最直接**的那个，而不是最上游的那个。

### 4.1 修改已有图片

若用户/QC意图是“修改这张图、在这张基础上修、稍微改一下”：

1. 当前失败/待修改候选 = `EDIT_TARGET / REVISION_SOURCE_IMAGE` = **MUST / PRIMARY**；
2. 正确局部参考 = `PATCH_DESIGN_AUTHORITY`（需要时MUST）；
3. Parent Master = 仅当需要锁身份/结构/空间Canon时作为SUPPORT；
4. 与Revision Issue无关的母图/旧候选 = OMIT。

**禁止：文字说修改候选，实际不上传候选而只@母图。**

若平台不支持Mask/Inpaint但支持Image-to-Image Revision，也仍必须把待修改候选作为`REVISION_SOURCE_IMAGE`。只有明确选择“放弃当前候选，从Master重新生成新候选”时，才允许不以失败候选为Primary，并把任务改名为`FRESH_REGEN`而不是Revision。

### 4.2 Environment / Prop Shot View

已有当前Shot匹配的Approved Derived Coverage时：
- 当前Coverage = `VIEW / SPATIAL AUTHORITY` = PRIMARY；
- Parent Canon Master只在Coverage无法独立承载的固定身份/结构字段上作为SUPPORT；
- 若Coverage已足够唯一，Parent Master降为TEXT-ONLY或OMIT。

例：舞台侧后方战斗镜头已有`ENV_STAGE_CV_STAGE_LEFT_REVERSE`，则它优先于舞台正面Hero Master。不能因为Hero Master是“母图”就机械@进去。

### 4.3 正在生成新的Derived Coverage

这是例外：当前任务本身是在“从Master倒推新视角”，因此Parent Master必须作为Primary Canon Source；Geography / Structure Spec同时参与。尚不存在的目标Coverage当然不能作为Reference。

### 4.4 Prop Interaction / Close-up

若当前镜头清楚拍到道具某一面/开合态且已有对应Coverage：优先该Coverage。Parent Master只保留它仍独有的结构/材质Authority；不把所有方向一起上传。

### 4.5 Production Support / Shot Assembly / Additional Video Conditioning Keyframe

如果Canon/Coverage已经定义对象，但当前复杂Interaction / Contact / Transient State仍需要一张高清生产证据：使用Approved `PRODUCTION SUPPORT REFERENCE`作为该字段最直接Support，不把它升级成Identity/Structure Canon。若是低复用、无需正式Prop Canon但当前Shot必须清楚拿/递/操作的小物件，可使用限定Scope的`LIGHTWEIGHT_INTERACTION_PROP_REF`；一次性关键Insert可用`SHOT_DETAIL_REF`。

如果当前主要风险是**多人关系 / 人物进入场景 / 人景物整体组合**，并已有Approved `SHOT_ASSEMBLY_ASSET`：它作为`HD_SHOT_ASSEMBLY_IMAGE`承担关系/同框/空间占位字段。反复/命名人物仍需要正式角色Identity Authority；一次性`SCOPED_CAST / NON_RECURRING`也必须先有Approved FMH/Minor Human Master，Assembly只能继承其Appearance并补当前关系。它不能替代仍然必要的道具Canon或Environment Geometry Authority。

Approved Storyboard之后的`VIDEO_FIRST_FRAME / VIDEO_TARGET_FRAME / VIDEO_LAST_FRAME / VIDEO_CONDITIONING_KEYFRAME / VIDEO_CUT_EXIT_FRAME / VIDEO_CUT_ENTRY_FRAME`按各自Time Scope承担Primary Visual Conditioning；Approved Storyboard继续负责跨时间的Temporal Beat / Action Sequence / Cut关系。Character/Prop/Environment Canon与SPATIAL_CANON仍负责身份、结构和世界空间事实。

---

## 5｜Stage-Specific Binding

### Stage 03｜图片资产
- `NEW_CANON_MASTER`：使用项目风格/文字Canon/必要Identity，不引用与新资产无关的Shot图。
- `PERSONAL_ADORNMENT_DETAIL`：Approved Character / Current LOOK + Adornment Identity Card / AC record作为Source，只生成已批准装饰的高清局部；不重新设计人物或把剧情Prop降级成Adornment。
- `DERIVED_COVERAGE`：Parent Master + Structure/Geography = Primary；由Triggered Shot决定目标视角。
- `FUNCTIONAL_MINOR_HUMAN_ASSET`：Stage 02 `SCOPED_CAST_BRIEF` = TEXT PRIMARY；必要Project Style / Scene Color只控制画法与综合色；不得借用主角脸模做“反向参考”。输出只承担当前Scope的匿名人物Appearance。
- `PRODUCTION_SUPPORT_REF`：最直接Approved Parent Authorities + Video Risk Contract = Source；只锁授权Interaction/Contact/Transient State/Entity Action字段。
- `PERFORMANCE_SUPPORT_ASSET`：Approved Character/FMH Base Authority + `PERFORMANCE_ASSET_REQUIREMENT_SET` = Source；只锁授权Expression / Action Pose / Contact Pose静态形态，不建立新Identity，不控制动作Timing。
- `NARRATIVE_FX_ASSET`：`NARRATIVE_FX_ASSET_MANIFEST` + 对应Environment/Prop/Style Parent = Source；只锁FX视觉形态、状态节点与环境静态交互；禁止Reference Video。
- `SHOT_ASSEMBLY_ASSET`：反复/命名人物使用Approved Character Authority；一次性`SCOPED_CAST / NON_RECURRING`使用Approved FMH/Minor Human Master；Environment / 关键Prop / State使用Approved Authority + Assembly Brief = Source。只锁多人关系/人景物组装/空间占位/Contact，不从Storyboard宫格直接生成，也不首次建立人物Appearance。
- `REVISION_IMAGE / LOCAL_PATCH`：失败候选/待修改图 = Primary Edit Target；Parent Master不得冒充Edit Target。

### Stage 04｜Storyboard
- **先做Key Visible Asset Register，再决定图片输入。** 当前Segment会被清楚看见/操作/承担因果的关键人物、Environment方向、Prop / Weapon / Vehicle / Entity / Persistent State必须逐字段覆盖；
- Shot-matched Coverage优先于泛化Hero View；当前镜头若需要Approved `SHOT_ASSEMBLY_ASSET`稳定多人关系/人景物组合，则加入；
- CONTINUITY_ENTRY按需加入真实Previous Ending Frame；CUT_ENTRY / SCENE_OPENING不机械加入；
- 若关键可见资产没有视觉Authority，输出`REFERENCE_COVERAGE_GAP`回Stage 03，不得为了减少图片输入而省掉；
- 不入镜或不可辨认且无因果职责的角色/背景对象不因为“本Scene里存在”就加入。

### Stage 05｜Final Video
- **当前视频镜头里真正会出现并可读的关键资产必须全部被Reference Field Coverage Map覆盖。** 这优先于“图片越少越好”；
- Approved Storyboard继续控制跨时间Composition/Temporal/Action Sequence字段；Approved Video Conditioning Frame在其Time Scope内承担Primary Visual。是否额外保留Storyboard视觉输入按**字段覆盖 + Capability**裁决，不做整资产TEXT化；
- 当前Camera Direction最匹配的高清Environment Coverage优先；当前清楚入镜的反复/命名人物必须有正式Identity/Look Authority；一次性`SCOPED_CAST`只要清楚可见，必须由Approved FMH/Minor Human Master覆盖Appearance；Assembly/Previs不得承担、共享或替代人物Appearance Authority；当前清楚出现/操作的关键Prop / Weapon / Vehicle / Entity / Persistent State必须有对应Authority；
- 当前镜头若需要匿名/功能性小人物（路人、孩子剪影、护士、乘客、见证者等）来维持构图、氛围或因果，只要该匿名/功能性小人物清楚可见，必须有Approved FMH/Minor Human Master作为Base Appearance Owner；Assembly / Approved Previs Human Anchor只能作为Supplemental Relation/Pose/Contact Proof。缺FMH则`FUNCTIONAL_MINOR_HUMAN_GAP`，不得继续；
- 已有Approved `SHOT_ASSEMBLY_ASSET`时，可用`HD_SHOT_ASSEMBLY_IMAGE`承载多人关系/人景物组装，但不能因此遗漏它没有覆盖的关键身份/结构字段；
- CONTINUITY_ENTRY按真实Ending Frame职责加入；
- 没有明确当前职责的真正冗余Reference删除；**关键资产绝不能因为“精简Reference Pack”被删除。**

---

## 6｜Negative Relevance Gate（负面相关性闸门）

具体人物名、具体场景名、具体怪物/道具名、未来Beat元素进入`Task-Specific Restrictions`之前，必须证明存在**真实污染路径**。

### 6.1 合法污染路径

至少命中一项才允许写具体排除：
- 当前上传的Storyboard / Ending Frame / Control Image里实际包含该元素，但当前输出需要移除/不延续；
- 当前Reference Pack中的某张图实际包含该元素，且模型可能把它误带入输出；
- 当前连续性源Scene中存在该元素，但当前CUT/Shot明确要求它离开画面，而输入仍可能诱发残留；
- 当前文字动作/空间描述存在高概率歧义，可能把下一Beat/邻近区域元素提前生成；
- Failure Diagnosis已经证明模型反复错误生成该特定元素。

### 6.2 不合法的“保险禁止”

以下情况默认删除具体名字：
- 该人物/道具/地点根本没有出现在当前视觉Reference；
- 当前Shot / Segment没有它；
- 当前Continuity Source没有它；
- Prompt正文没有诱发它的相邻概念；
- 只是因为剧本后面S04–S06会出现，所以提前写“不出现”。

这类信息留在**内部Shot Scope / Future Beat Guard**即可，不进入模型正文。

### 6.3 核心原则

**Absent-from-input ≠ needs-negative.**

模型侧优先使用正向Shot Scope：
```text
画面仅包含：<当前真实人物/群体/场景/道具>
```

只有存在真实污染路径时，才补最短具体限制。禁止长串“不要出现A/B/C/D/E”把不存在的概念重新注入上下文。

如果确有真实污染路径，且又必须保留一个更窄的合法替代（例如“禁止额外行人，但保留已定义的1名远景匿名见证者”），则使用`Forbid + Replacement`：先写排除范围，再写唯一合法替代，不允许只有禁止没有替代Owner。

通用质量Negative（例如额外肢体、穿模、错误字幕等）不受“具体实体污染路径”限制，但仍按Prompt Lock Dedup只出现一次。

---

## 7｜Revision Binding硬规则

### `REVISION_TARGET_BINDING_FAIL`
出现以下任一项：
- 用户/QC明确要修改候选A，但Reference Pack没有候选A；
- 把Parent Master错误标成“待修改图”；
- 修改Derived Coverage时只@Parent Master、不@失败Coverage Candidate；
- Storyboard局部修改却只@角色/场景Master、不@待修改Storyboard；
- Image-to-Image Revision没有把Revision Source设为Primary。

→ 禁止输出修改Prompt。

### `REFERENCE_COVERAGE_GAP`
- 当前镜头存在关键可见人物/场景方向/道具/武器/实体/状态/Personal Adornment，但没有Approved视觉Authority覆盖；
- Personal Adornment已是Critical，Current Look不足且缺Approved AD-01；
- 为了减少Reference数量删掉了一个Critical Field；
- Assembly/Anchor被误认为能覆盖它实际没有锁定的身份/结构字段。

→ 回Stage 03/04补最小必要Authority或Assembly/Anchor；不得继续Storyboard/Final Video。

### `REFERENCE_SLOT_OVERFLOW`
- 所有Critical Field都确实需要视觉Reference，但平台槽位不足；
- 无法通过删除真正重复项、TEXT_CONTROL或Approved Assembly/Anchor安全重组。

→ 不得静默删关键图；先重组资产/Anchor或必要时调整Segment。

### `REFERENCE_FIELD_PRESERVATION_MISS`
- 复合参考被OMIT后，其中仍然必要的综合色、构图、空间占位、群体或匿名功能人物字段没有被替代Owner接管；
- 文字里声称“用TEXT_CONTROL吸收”，但没有实际提炼结果；

→ 回Reference Resolver完成当前Route Change的Required Field Preserve/Remap，不得继续。

### `FUNCTIONAL_MINOR_HUMAN_GAP`
- 当前Shot / Segment明确需要匿名或功能性小人物，但没有合法Visual Owner；
- Readable Scoped Cast对应Approved FMH/Minor Human Master缺失；
- 试图用Shot Assembly、Mandatory Storyboard或Rendered Human Anchor替代其Base Appearance Master；
- 试图用“禁止其他人”替代功能性小人物定义；

→ Readable Scoped Cast一律按Stage 02 Owner回Stage 03补Approved FMH/Minor Human Master；若FMH已存在但仅缺关系/姿态证据，再补Assembly或Stage 04 Previs Human Anchor。不得用后两者替代Base Appearance Master，也不得继续Video。

### `SHOT_ASSEMBLY_AUTHORITY_FAIL`
- Assembly改写已有反复/命名人物Identity、Environment Geography或Prop Canon；
- Scoped Cast超出授权Scene/Shot Group被继续复用；
- Storyboard宫格被直接放大/清稿后冒充Assembly。

→ 回Stage 03重建正确Assembly，不得继续Storyboard/Video。

### `REFERENCE_RELEVANCE_FAIL`
- Reference没有Why Now；
- 当前Shot已有更直接Coverage，却无理由选择泛化Hero Master；
- 上传与当前可见字段无关的资产“求保险”；
- Reference职责与Task Target不匹配。

→ 重新Resolve。

### `NEGATIVE_RELEVANCE_FAIL`
- Task-Specific Restrictions出现具体人物/道具/地点排除，但找不到真实污染路径；
- 列出整段未来Scene元素作为“禁止出现”；

→ 删除无效具体负面项后重新编译。

---

## 8｜与Reference Fidelity Firewall的关系

- `Reference Role & Fidelity Isolation`解决“这张图能控制什么、不能把低清当最终画质”；
- 本引擎解决“**这张图当前到底该不该上传，以及是不是最直接的那一张**”。

先Task Binding，再Role/Fidelity，再Budget。

推荐顺序：

`Task Contract → Key Visible Asset Register / Reference Field Coverage → Reference Eligibility / Most Direct Authority → Reference Role & Fidelity → Slot/Budget Check → Executor Input Map → Execution Reference Semantics → Prompt Compiler`

---

## 9｜三个标准案例

### Case A｜无效负面人物注入
当前Storyboard与实际图片输入只有诺伊和当前街景；凯登 / 西莉亚 / 诺拉没有入镜、没有被输入、Ending Frame也没有他们。

错误：`不出现凯登 / 西莉亚 / 诺拉、剧院、怪物或任何S04–S06元素。`

正确处理：这些内容保留在内部Shot Scope / Future Beat Guard；模型Prompt只正向写当前画面真正包含的人物与环境。除非某个Control / Ending Frame仍残留上述元素，否则不点名。

### Case B｜舞台打斗机位
当前Shot是舞台左后方朝台口拍摄，已有Approved `ENV_STAGE_CV_LEFT_REVERSE`。

PRIMARY：`ENV_STAGE_CV_LEFT_REVERSE`。
Parent舞台正面Hero Master：若Coverage已足够锁几何则OMIT/TEXT-ONLY；只有当前Coverage仍缺失固定舞台结构字段时才SUPPORT。

### Case C｜QC失败图片轻微返修
Candidate C02整体正确，只需修手部/局部道具。

PRIMARY：C02 = `REVISION_SOURCE_IMAGE / EDIT_TARGET`。
必要时再@正确手部/道具局部Authority。Parent Master只负责身份/结构Support。

若不上传C02、只@Parent Master重新生成，那不是“修改C02”，必须改名`FRESH_REGEN`。

---

## 10｜Stop Rule

Reference Resolver既不是“尽量装满槽位”，也不是“尽量少传图”。

只有当当前Task的**所有Critical / Required Authority Fields都已经被充分覆盖**，并且继续加入的图片不再增加必要控制字段时，才停止添加。

**最好的Reference Pack = 关键资产全覆盖 + 每张图都有职责 + 没有同字段无意义重复；生成Prompt只投影职责，不投影资产名。**


## Current｜Prompt Surface Handoff

本文件产生的Task Contract、Reference Audit、MUST/CONDITIONAL/TEXT-ONLY、Asset ID、Why Now / What Field / Most Direct全部属于内部控制层。生成Prompt交付前必须经`model_facing_prompt_surface_sanitizer.md`的**Allowlist Extraction + Mechanical Surface Lint**；不得把这些表格、标题、版本号、资产名、文件路径或`TASK_SHELL / INPUT_LABEL / OUTPUT_ADMIN_SHELL`等操作者壳当作模型提示词。真实原生Token是唯一可能进入模型正文的绑定接口，但仍不得附内部名称/版本/职责长说明。


## V4.5.3｜Visual Evidence Binding Contract

Text-only Controller建立Task Binding时，每个Image Binding必须同时记录`visual_evidence_ref / visual_evidence_status / visual_fact_codes / visual_issue_codes`。强绑定`@资产`不是“相关就传”，而是由当前Task所需Visual Facts证明。
