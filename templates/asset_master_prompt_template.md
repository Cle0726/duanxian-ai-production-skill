# 图片资产母图生成提示词模板

> **Current Reference Binding Gate：** 本任务只要实际向图像模型绑定任何视觉Reference（UI槽位、Attachment、Native Token或其他Handle），在生成前必须读取`reference_binding_semantic_verification.md`建立当前`REFERENCE BINDING CONTENT MAP`；正文不写Token也不能跳过。

> **Current Model-Facing Surface Gate：** 任何图片资产Prompt在交付前必须运行`model_facing_prompt_surface_sanitizer.md`，并在需要风格连续性时额外运行`style_authority_projection_gate.md`。Existing Authority Reuse Scan、MUST_BIND列表、Asset ID/Version、文件名与Executor Binding List只给操作者/流水线看；模型正文只接收当前Generation Profile要求的真实`@资产`Mention + 直接的身份/结构/综合色/构图执行句 + 经过投影的风格执行句群。强绑定Approved Asset不得省略Mention。


本模板用于 **Stage 03（第03阶段：视觉/规划资产）**。V4.5.2的Spatial Planning Diagram优先由结构化Spatial Canon + `tools/spatial_diagram_renderer.py`确定性渲染；若平台/工作流需要图像模型辅助绘制，也必须以结构数据为Source of Truth，不得让图片模型改写Topology/Floor Plan。生成前读取`image_candidate_strategy.md`确定当前Job的`Planned Image Candidate Count`；候选数属于生产元数据/生成参数，不写进模型Prompt正文，也不要求模型“在一张图里给多个方案”。任何会反复使用的正式资产，在进入分镜/视频之前，都应先有一份已经确认的“母图生成提示词”。输出前读取`execution_reference_semantics.md` + `prompt_semantic_deduplication_engine.md`：同一身份/结构/画风/限制只保留在最合适区块一次，不用“主体描述一次、材质段再说一次、末尾限制又反写一次”的方式堆Prompt。 若当前任务不是新建Master而是QC失败候选返修，先读取`task_bound_reference_binding.md` + `inpaint_local_patch_authority_engine.md`：失败候选本身必须作为`REVISION_SOURCE_IMAGE / EDIT_TARGET`，不得只绑定Parent Master然后声称是在修改候选。**任何Reference的Asset ID / Version / 文件名只留在Executor Input Map，不进入母图Prompt正文。写Prompt前必须先读取 `asset_aspect_ratio_authority.md`，由资产类型决定画布比例；不得从Style Board / Color Card / Storyboard / Final Video继承画布比例。**

人物资产必须先做“服装与环境分析”，主要/反复角色同时读取`personal_adornment_identity_system.md`决定个人装饰策略，并读取 `character_identity_differentiation_engine.md` + `face_identity_matrix.md` + `hair_identity_architecture.md` + `source_wardrobe_adaptation_authority.md` + `character_costume_dramaturgy.md` + `wardrobe_style_design_engine.md` + `wardrobe_diversity_design_matrix.md` + `character_appeal_silhouette_system.md` + `body_identity_presentation_authority.md`；主要/反复人物额外读取 `character_closet_registry.md`。把当前剧情阶段应该穿的**完整Look**直接生成进人物母图。默认不要拆成“身份图 + 独立服装图”让下游再拼，也不得把换季简化成“旧造型+大衣”。

**如果该人物是首次建档的新角色、尚无APPROVED Character Master：必须同时读取 `new_character_generation_recipe.md`。** 先用已验证的新人物统一抽卡配方锁住《断弦之歌》的二维插画生成方向，再根据角色自身剧情功能设计独立身份，不复制现有主角长相。



**如果当前任务是 `AD-01 Signature Adornment Detail`：必须读取 `character_asset_requirement_set.md` + `personal_adornment_identity_system.md` + `character_closet_registry.md`。** AD-01只锁已批准角色个人装饰的形状、Placement、Scale、Material、Wear与佩戴方式，不重设计Face/Hair/Wardrobe；若该物件承担剧情因果则停止AD-01并升级Prop / PR-01。


**如果当前任务是 `EMPTY_ENVIRONMENT_MASTER / ENVIRONMENT_CLEAN_CANON / ENV_CANON_MASTER`：必须读取 `environment_asset_standard.md` + `base_visual_authority_manifest.md`。Base Master必须是**空场景**：禁止可读人物、群众、临时表演、一次性剧情动作和临时持物状态；只锁固定空间、固定家具/结构、材质、综合色与基础主光。登记`population_policy=EMPTY_ENVIRONMENT_ONLY`、`readable_human_count=0`、`transient_content_policy=CLEAN_CANON`。人物以后由Character/FMH资产与Shot Assembly/Execution Frame加入。

**如果当前任务是 `FUNCTIONAL_MINOR_HUMAN_ASSET`：必须读取 `functional_minor_human_asset_protocol.md`。** 只根据Stage 02 `SCOPED_CAST_BRIEF`建立当前Scene/Shot Group所需的最小匿名人物外观Authority：年龄/性别感、身形、服装轮廓、必要外貌差异、匿名边界。不要把它升级成完整主角Character Master，也不要在人物资产页里烘焙最终场景站位。即使核心风险是人景物关系，也必须先完成这张人物母图；随后再用Shot Assembly补关系。

**如果当前任务是 `PERFORMANCE_EXPRESSION_SUPPORT / PERFORMANCE_ACTION_POSE_SUPPORT / PERFORMANCE_CONTACT_POSE_SUPPORT`：必须读取 `performance_asset_requirement_engine.md`。** 先绑定Approved Character/FMH Base Authority，只生成Requirement授权的表情、姿态或Contact静态形态；不得重新设计人物脸、发型、服装，不得把动作Timing或Camera Motion写成静态资产职责。多格Support若用于内部库，默认不得直接作为Final Video Reference。

**如果当前任务是 `NARRATIVE_FX_REFERENCE / NARRATIVE_FX_STATE_SHEET`：必须读取 `narrative_fx_asset_standard.md`。** 只建立剧情型FX的视觉形态、状态节点和静态环境交互；不得发明新的Environment Geography或人物Identity，也不得生成/要求Reference Video。

**如果当前任务是 `SHOT_ASSEMBLY_ASSET`：必须读取 `shot_assembly_asset_layer.md`。** 该任务的目标不是重新设计已有角色/场景/道具，也不是从Storyboard宫格清稿，而是把已批准的Character/FMH Authority、已批准场景/关键道具/状态和当前Scene光色组装成一张高清静态生产图，稳定多人关系、空间占位或人景物同框关系。一次性`SCOPED_CAST / NON_RECURRING`也必须先继承Approved FMH/Minor Human Master；Assembly不得首次建立其基础Appearance。

**如果该人物是剧情明确可变身的圣谱者，并且当前任务是建立TF / TE / TH / TC / WP / TS / TM / FX资产：必须读取 `transformation_asset_standard.md` + `transformation_splendor_architecture.md` + `music_identity_mapping.md` + `transformation_beauty_core_five.md` + `musical_eye_motif_system.md` + `musical_eye_motif_registry.md`。** 日常Character Master负责身份；Transformation Asset负责变身结构。先由人格/情绪/人物弧建立Music Identity，再把同一音乐身份转译到礼服、眼影/眼周、头发、瞳孔/虹膜和音乐武器，最后再处理FX与时序。

> **Color Binding Gate（Current Rule）：** 场景绑定型Asset（Coverage / Support / Assembly / FMH / Rebuild / Scene-bound Revision）在编译Prompt前必须执行`color_authority_preservation_gate.md`。当前Scope已有Approved Scene Color Card时，将其或Color-Only Crop加入`MUST_BIND_COLOR_AUTHORITY`；已有母图不能代替综合色视觉Authority。纯Character Identity Master不强制绑定Scene Card。

> **Current Runtime-Clean：** `SCENE_COLOR_APPLIED_REFERENCE`不是普通Stage 03规划资产。已有Approved Color Card时直接绑定/保留综合色Authority；没有有效`APPLIED_REFERENCE_TRIGGER`不得创建“综合色应用参考图”Job。


**如果当前任务是 `SPATIAL_PLANNING_DIAGRAM`：** 这不是电影美术图。必须读取`state/spatial_canon.schema.yaml`对应Topology/Floor Plan/Route数据；优先使用`tools/spatial_diagram_renderer.py`生成可审核SVG。Planning Diagram允许ID、文字、距离、方向、箭头和路径，但禁止获得Storyboard/First Frame/Video Primary Visual权限。若结构数据未锁，不得让图像模型自行猜地图。

**V4.5.2 Justification Gate：** 正式TO BUILD资产在生成Prompt前必须已有`WHY_REQUIRED / REQUIRED_BY / DOWNSTREAM_USE`。Environment Coverage还必须有`Spatial Parent + Visual Parent`；缺少这些元数据时停止生成，不用“先出图再解释用途”。

## A｜资产登记
- 资产ID：
- 版本：V__
- 状态：WIP（制作中） / CURRENT（当前在用） / APPROVED（已批准Canon） / APPROVED SCOPED FIGURE（已批准范围人物） / APPROVED ASSEMBLY（已批准镜头组装资产） / APPROVED SUPPORT（已批准生产辅助） / DEPRECATED（已废弃）
- 资产类型：Spatial Planning Diagram / 人物 / Voice Identity Asset / Functional Minor Human Asset / Performance Support / Narrative FX Reference / Personal Adornment Detail (AD-01) / 变身资产 / 场景 / Event View / Reciprocal Coverage / Predictive Coverage / 道具 / Shot Assembly Asset / Render Style / Cinematic Shot Style / Global Color Card / Scene Color Extension / Lighting Reference
- Base Master（基础母图：标准版本）：
- State Variant（状态变体：同一资产发生持久变化后的版本，如有）：
- 所属Master Set（母图组：多张图共同锁定同一复杂资产，如有）：
- Owner / Parent Location（所属角色 / 所属大地点，如有）：
- 使用集 / Scene（场次） / Shot（镜头）：
- WHY_REQUIRED / 为什么现在必须生成：
- REQUIRED_BY / 上游Event、Shot、Relation、Reuse Requirement：
- Spatial Parent / Visual Parent（Coverage适用）：
- 下游职责 / DOWNSTREAM_USE：
- 不负责：

> **通俗解释：** 已经存在的项目编号不要乱改。只有原来没有编号的新场景/道具，才建议使用 `ENV-*` / `PROP-*`。

## B｜人物资产前置：服装与环境分析
人物资产填写；其他资产跳过。

- 季节 / 气候：
- 天气 / 温度感：
- 室内 / 室外 / 交通工具：
- 时间：
- 场合 / 社交正式度：
- 活动：
- 身份 / 审美 / 职业 / 行动需求：
- Character Identity Distinction Card：Face ID / Hair ID / Eye ID / Wardrobe ID / Adornment ID
- Adornment Strategy / Current Active Adornment / Current LOOK Binding：
- AD-01 Requirement：REQUIRED / NOT REQUIRED / REUSE｜Reason：
- Character Fashion DNA：
- Character Closet / 可复用LOOK或Item：
- Primary / Secondary Appeal Hook：
- Boldness Dial：RESTRAINED / ASSERTIVE / BOLD / EDITORIAL（成年角色）
- Body-Line Emphasis / Silhouette Hook / Motion Appeal：
- 年代 / 世界观限制：

### 当前剧情阶段完整人物造型
先执行 `Closet-First Outfit Assembly`：能用角色已拥有单品重组就优先重组；现有衣柜无法同时满足功能+人格+审美+魅力+剧情时才新增单品。

说明内层、中间层（如有）、外层、裤/裙/连衣裙、鞋靴、围巾/帽子/手套、固定饰品、材质与厚度、整体比例与综合色；同时说明Primary/Secondary Appeal与Body-Line Emphasis在当前季节如何继续成立。

**把这套完整造型直接写进人物母图Prompt（提示词）。不要默认再建立独立Wardrobe Master（服装母图）让下游拼接。**

## C｜母图必须稳定的信息

### 人物母图
身份、年龄感、骨相/脸、发型结构、体型比例、当前剧情阶段完整服装、固定饰品、必要资产格式/视图。


### Personal Adornment Detail / AD-01
必须继承Approved Character / Current LOOK中的既定装饰，不从零另设计。只锁：Category / Placement / Scale / Shape-Motif / Material / Finish-Wear / Fastening / Left-Right / 与耳朵、头发、领口、手指等实际接触关系。输出应足以供MCU/CU稳定继承；不承担剧情Prop机制、不改服装、不改脸发眼。若Current Look已经足够清楚则不生成AD-01。

### 变身资产
必须继承Approved Normal Character Master的身份。先建立 `Music Identity Card`，再根据 `transformation_asset_standard.md`、`transformation_splendor_architecture.md` 与 `transformation_beauty_core_five.md` 分别锁定礼服、眼影/眼周、头发、瞳孔/虹膜、音乐武器五核心，以及圣约指挥棒机制与变身时序；不把所有职责压进单张图，也不允许“变身=换色服装”。首次/核心变身同时建立`Transformation Splendor Profile`，先锁Costume Thesis / Style Family / Boldness Dial / Primary+Secondary Costume Signature / Graphic Block / Negative Space，再锁Large-Medium-Small / Material Contrast / Hair Splendor / Weapon-Body Silhouette / Visual Level Gap；同时读取`body_identity_presentation_authority.md`建立`Transformation Body Presentation Mode + Preserved Appeal Hook + Body-Costume Interaction`。礼服设计不变成日常穿搭，但人物身材美与Body Identity必须同步成立。Dark Gothic只是可选Style Family，不是默认模板。

在生成TF-01或TE-03前，必须先建立`Eye Signature Spec` + `Musical Eye Motif Spec`并读取Registry。锁`Primary Eye Signature + Secondary Graphic Signature（MAIN/CORE）+ optional Periocular Emblem + Musical Origin Trace`；Eye Makeup只能MINIMAL / STANDARD / EXPRESSIVE，不能NONE。允许LITERAL_NOTATION / DERIVED_MUSICAL_GLYPH / MUSICAL_GEOMETRY，不强迫每人贴标准Notation。已有APPROVED TE-03时，它是Eye + Musical Eye Canon Authority，TF修订必须精确继承。

### 场景母图 / Environment Canon Master
Stage 03场景必须同时读取 `shot_coverage_asset_derivation.md`。先用**一张正式高清Hero Environment Master**锁空间身份、核心几何、出入口、地标、尺度、材质与基础主光；再建立Geography / Blocking Spec。只有Stage 02真实Shot Coverage证明某个Reverse / Side / Door-side / Zone方向需要图像级锚定时，才从Approved Parent Master倒推Derived Coverage View。禁止默认360°或无镜头依据的多角度平铺。

### 道具母图 / Prop Canon Master
Stage 03道具必须同时读取 `shot_coverage_asset_derivation.md`。先用**一张正式高清Hero Prop Master**锁轮廓、尺寸、人物比例、材质、功能结构、非对称识别点与开合逻辑；主图批准后先补Structure Spec。只有Stage 02真实Shot Coverage证明会清楚拍到主图未覆盖的背/侧/顶/内侧、关键开合态或操作面时，才倒推Derived Coverage View。禁止默认正/背/侧/细节全套。

### Render Style Board / Evidence
只锁定二维绘画语言、线稿、轮廓概括、皮肤渲染、头发绘制与材质**表现方法**；不重新定义身份/空间/道具结构，也不承担清晰度、锐度或最终细节密度。严格读取 `project_style_dna.md` + `visual_style_authority_engine.md`：
- anime-influenced 2D illustrated character art；
- clean hand-drawn linework；
- cel-inspired controlled color blocking + soft painterly shading；
- matte painted skin；
- rich but restrained palette + controlled chroma concentration + selective saturation + controlled contrast + preserved value hierarchy；
- 已有成熟Approved资产时优先组织`APPROVED_STYLE_EVIDENCE_BOARD`，不为了标准版式无意义重生成匿名画风板。

### Cinematic Shot Style Board
只锁项目级摄影语法：景别倾向、人物/环境面积关系、前中后景、负空间、OTS/Profile/Wide等组织方式、实际光源作为构图层次的方法。**不得覆盖Director/Storyboard具体Camera / Blocking，也不承担对象清晰度。**

### Global / Scene Color Card / Lighting Reference
统一读取`color_script_derivation_engine.md`：
- Global Color DNA固定项目级综合色语法与Functional Color Map；
- Scene Color Extension只派生当前地点/气候/材质需要改变的综合色变量；
- Shot Lighting Variant通常使用TEXT_CONTROL，只有重复、高风险且文字不稳定时才生成正式Lighting Reference；
- 不负责身份、几何、镜头构图或清晰度；
- 综合色语言使用`rich but restrained + controlled chroma concentration + selective saturation + controlled contrast + preserved value hierarchy`；不得机械加入全局`low saturation / desaturated / low contrast`，实际综合色强度由Global → Scene → Shot当前层级决定。

## D｜Base Master → State Variant规则（基础母图 → 持久状态变体）
State Variant（状态变体）必须继承已批准的Base Master（基础母图），只改变剧情明确要求的**持久状态**。通俗说：还是同一个人/场景/道具，只是它“后来变成了另一个长期状态”。

例如：
- Character story-phase master → INJURED_PERSISTENT（确有必要时；若后续`TRANSFORMATION_RECOVERY=RECOVERED`，该伤势Variant在恢复点终止，不得继续作为当前身体Authority）
- PROP_KEY_A_CLOSED → OPEN / DAMAGED
- ENV_SCENE_A_NORMAL → ATTACK / AFTERMATH

人物的COAT_OPEN、轻微淋湿、灰尘、少量血迹等短期状态默认通过连续性状态 + Stage 04/05控制；CONTINUITY_ENTRY可读取上一段尾帧，CUT_ENTRY / SCENE_OPENING通过剧情状态与Storyboard继承，不要过度资产化。

## D.5｜Asset Prompt Compilation Rules（内部，不复制到模型正文）

- 所有正式可见图片资产先运行`style_authority_projection_gate.md`生成`STYLE PROJECTION CARD`并继承`Canonical Project Render Core`（纯技术图可显式N/A）；最终正文至少保留一段可执行风格句群，不能缩水成“二维电影插画 / 欧陆复古 / 忧郁克制 / 保持统一风格”。
- 画布比例由`asset_aspect_ratio_authority.md`与当前真实资产类型决定；最终正文只写实际比例/画幅，不写内部资产类型代码、Registry字段或规则来源。
- Master / Coverage / Support / Assembly等内部路由先在流水线决定；最终正文只写本次真正要生成的可见对象、视角、状态和空间关系，不把路由名/Asset ID复制给模型。
- 画风、材质与综合色先由对应Authority求解，再改写成直接视觉语言；不写`project_style_dna.md`、Global→Scene→Shot、Authority或Reference Role。
- 持久状态变化先内部确定“什么改变/什么继承”；模型侧只写直接变化和必须保持的可见特征。
- Reference绑定继续在Executor/Runtime层完成；Current Generation Profile下，强绑定Approved Asset必须投影真实`@资产`Mention + 最短执行句。
- V4.5.7综合色绑定：Scene-bound图片必须先解析当前`SCENE_COLOR_CARD`并作为`COLOR_AUTHORITY`强绑定；Scene-independent Master绑定Approved Base/Global Color Card。Named Asset平台必须把真实`@对应色卡`投影到最终Prompt。
- 最终正文只保留当前真实高风险限制；候选数、版本、审批、QC、Stage、下游用途全部留内部。


## E｜MODEL-FACING ASSET PROMPT｜COPY THIS ONLY

> **Current Egress Rule：** E节只定义内部生成配方，最终用户可见文本必须再交给`prompt_egress_gate.md`。最终图片Prompt不得带任何栏目标题，也不得出现任何任务壳、输入映射、本地文件元数据、内部资产元数据、流水线方法名、QC说明或meta-prompt说明。最终只输出一个无标题代码块：直接视觉内容 + 直接风格/综合色 + 必要排除项。


> **交付格式硬规则：** E节不是让模型输出“任务文档”。最终只生成**一个Prompt代码块**。代码块内不得出现`TASK_SHELL / INPUT_MAPPING / LOCAL_FILE_METADATA / INTERNAL_ASSET_METADATA / OUTPUT_ADMIN_SHELL / REFERENCE_ADMIN_TEXT`。不输出Reference行政清单；但Current Generation Profile要求强绑定Approved Asset显式Mention时，即使UI已经绑定也必须保留真实`@资产` + 最短执行句。只有平台Profile明确允许UI-only时才可省略。

最终Copy Surface按当前任务从下列执行内容中取必要项，**不机械保留栏目标题**：
- 实际画幅/比例与必要输出形式；
- 本次要生成的可见主体、环境、结构、状态；
- 构图、视角、前中后景、遮挡与空间关系；
- 身份/结构/尺度/接触等需要保持的可见连续性；
- 线稿、材质、画风、综合色与光源；
- 真实残余高风险限制。

推荐直接写成连续模型语言，例如：

```text
<直接描述当前资产主体/环境、构图与状态。>
<直接描述当前已裁决的风格、材质、综合色与光线。>
<只保留当前任务必要的排除项。>
```

如果平台已经分配真实Native Token，才可以在正文最前面增加极短绑定句；不得补文件名/版本/职责解释。

交付前必须产生内部`SURFACE_LINT_REPORT`并全部为0；否则不输出Prompt。

## F｜审核标准
- 模型Prompt是否已通过Surface Sanitizer：无Asset ID/文件名/Version/Reference职责表/Authority/MUST_BIND行政解释；Current Generation Profile要求的强绑定资产是否均保留真实`@资产`Mention + 最短执行句？
- `Canvas / Aspect Ratio`是否已经显式声明，且没有错误继承其他资产/Storyboard/Video的比例？
- 人物身份/造型类资产是否严格9:16竖版（除非用户明确覆盖）？
- 是否能稳定复现同一资产？
- 人物是否使用项目标准资产语言且服装已整合进当前人物母图？
- FRONT FACE / SIDE FACE是否真实锁住Face ID / Base Eye ID，BACK是否真实锁住Hair ID后发结构？
- 主要/反复人物的`Face / Hair / Eye / Wardrobe / Adornment`五层Identity是否完整登记？
- 若AD-01=REQUIRED，是否只继承既有装饰而未重新设计？Placement / Scale / Shape / Material / Wear是否足够近景稳定？
- ROTATING角色是否记录Rotation Pool / Current Active Adornment / Current LOOK Binding，没有每次随机换件？
- 与最接近现有角色比较后，Face / Hair / Eye是否不存在模板碰撞？
- 日常服装是否符合“欧洲时代世界语言 × 角色Fashion DNA × Wardrobe Diversity Matrix”，而不是全员同一法式模板或通用漂亮衣服？
- 是否先检查Character Closet并避免无理由新增单品？
- 是否通过No Lazy Styling：允许Closet旧单品+大衣/围巾等现实复用，但必须有新的比例/开合/层次/材质/综合色/Body Presentation逻辑，不能只换色或机械加功能件？
- 成年角色既有Appeal Hook / Body-Line Emphasis / Silhouette Hook是否被合理保留或季节性转译？
- 场景是否先有一张清楚的Canon Master + Geography，再由真实Shot Coverage决定是否补视角？
- 场景Derived Coverage多视图是否同一几何且都能回指Triggered Shot？
- 道具是否先有一张正式Canon Master，结构/尺寸/人物比例清楚？
- 道具Derived Coverage是否只在真实镜头需要时生成，而非默认正背侧全套？
- State Variant是否确有必要且正确继承？
- 是否承担了不属于自己的职责？
- 是否存在镜像、尺度、结构、身份或风格漂移歧义？
- 版本/状态是否登记清楚？

审核通过后登记正式资产ID、版本、状态、职责与关系；Stage 04/05按镜头职责引用，不重新设计，也不盲目附加所有资产。


### Body Identity / Presentation Prompt Rule
IDENTITY高权重段锁人物真实Body Identity；当前LOOK只输出已选中的`Body Presentation Mode + Preserved Appeal Hook + 2–4个Body Beauty Evidence`。禁止为“显身材”堆满收腰/贴身/高腰/开衩等互相争抢的关键词。

## V4.5.4｜COVERAGE CAMERA PROOF BLOCK

当本次任务是Environment/Event/Reciprocal/Predictive/Derived Coverage时，内部编译前必须先存在以下结构，随后再翻译成自然语言Prompt；不得只写“正视角/反打/侧面”：

```text
VIEW_REQUIREMENT_ID: <...>
Camera Origin: <Zone / Anchor>
Optical Axis: <Origin → Target Anchor/Entity>
View Direction Code: <normalized code>
Must See: <required fixed anchors / spatial facts>
Must Not See: <forbidden anchors / wrong orientation / conflicting state>
Spatial Parent: <approved planning/canon>
Visual Parent: <approved set appearance>
```

模型侧正文只保留可执行视觉句，例如“摄影机位于后排中轴，沿车辆纵轴朝前挡风玻璃拍摄；画面必须同时看清挡风玻璃、仪表台、方向盘、驾驶位和副驾位；不要朝向后排拍摄人物正面。”内部字段名不进入Copy Surface。

## V4.5.5｜EVERYDAY REALISM EXECUTION BLOCK

普通人物-场景/Vehicle/Assembly/Coverage任务在自然语言Prompt编译前先建立内部Reality Block：

```text
REALISM_CONTRACT_ID: <...>
Functional Environment Type: <restaurant / residence / specific vehicle ...>
Fixed Functional Layout: <zones / seats / driver controls / doors / aisle>
Expected Cast: <exact people/count>
Character Occupancy: <character → zone / seat / function / support>
Required Affordances: <doors/chairs/controls/props must actually work>
Mundane State: <wetness / door state / held props / vehicle motion ...>
Social-Spatial Need: <only if relevant>
Scoped Exception: <only the exact canon-authorized category; otherwise NONE>
```

随后翻译成正向、可执行的自然语言，不把内部字段名泄漏到Copy Surface。不得只追加一串“不要穿模/不要多人物”负面词；优先明确现实结构和人物功能位置。
