---
name: ai-manga-production-workflow
description: "《断弦之歌》专属AI漫剧六阶段生产Controller。V4.5.11-M1以V4.5.11全部导演、视频、Temporal与Editorial能力为领域基线，融合V4.5.7 Thin Kernel、Route-scoped Lazy Loading、Runtime Freshness与Anti-Shortcut控制闭环。"
---

# 《断弦之歌》AI漫剧生产工作流 V4.5.11-M1｜Proxy-First + Seedance 2.5 30s + Editorial Cut Bridge

> **Current Skill Version：`V4.5.11`**

> **Current Revision：`V4.5.11-M1_V4511_BASE_WITH_V457_THIN_CONTROL`**
> **Merge Authority：`V4.5.11_DOMAIN_BASE + V4.5.7_CONTROL_PLANE_ADDITIONS`**

## V4.5.11-M1｜V4.5.7 控制架构融合层

本修订以V4.5.11为领域与创作规则基线：Seedance 2.5、30秒长叙事、Proxy-First、Temporal Reference Hygiene、Storyboard Approximate Editorial Cut Bridge及其既有规则全部保留。融合仅增强控制平面；除本节明确声明的Context / Runtime / Anti-Shortcut规则外，不覆盖或删改V4.5.11原有导演、资产、分镜、视频、声音、连续性与后期规则。

### M1.1｜Thin Runtime Loading

- 单次任务先从结构化State解析当前Stage / Route / Capability，不默认把整套Skill全文加载到创作上下文。
- 必须调用`tools/context_load_planner.py`生成`CONTEXT_LOAD_PLAN`；Route Registry等大型控制面由脚本读取，不作为默认创作上下文。
- Context分为：T0 Kernel、T1 Route Runtime、T2 Conditional Authority、T3 Repair / Exception。只加载当前任务真正需要的最小完整集合。
- Context预算只能缩小到更精准Route，不能删除当前任务Hard Authority，也不能把Deprecated或历史文件提升为Authority。

### M1.2｜Verified Runtime Freshness

- 调用方不得自行声明Runtime为FRESH。只有`tools/runtime_freshness_resolver.py`验证Type、Status、Skill Version、Scope、Source Fingerprint与Runtime Fingerprint后，才允许走FRESH Fast Path。
- Runtime为`MISSING / STALE / INCOMPLETE`时，必须按Context Plan加载当前Route声明的Fallback Source；证据不足不能按“看起来没变”跳过回源。
- Skill、Source、Scope或关键Fingerprint变化后，只重编受影响Runtime，不从Stage 01无条件重做。

### M1.3｜Route-scoped Capability Loading

- Combat、Threat/Horror、Creature、Voice、Temporal、Complex Camera、Crowd、Transformation等专项规则只在对应Capability真实命中时加载。
- Genre Pressure命中时加载`screen_experience_genre_pressure_engine.md`；ACTIVE Creature Threat再加载`creature_performance_engine.md`。
- Validator与Schema属于Machine Validation Context；只有生成、修复或验证对应Structured Artifact时才进入当前工作集。

### M1.4｜Controller顺序

`Resolve State → Resolve Route → Build CONTEXT_LOAD_PLAN → Validate Plan → Load T0/T1/T2 only → Execute → Run Local Gates → Task Readiness → Stage Transition → System Integrity → Write State/Fingerprint`

用户说“继续”时从Current State继续；不得重启全项目，也不得跳过当前Route前置证据。

### M1.5｜Anti-Shortcut Invariant

- `QUALITY_FIRST`下，Protected Experience Beat属于内容完整性，不属于成本预算。
- Delete / Merge / Shorten必须通过Experience Completeness Gate；Cost、Quota、Token、减少生成段数不能作为删除Pressure / Reveal / Reaction / Consequence的理由。
- 字段齐全但体验Beat没有真实Landing，仍视为未完成。
- Approval必须来自真实Approval Record；QC PASS、User Approval、Promotion与Stage Transition保持分离。

### M1.6｜融合优先级

1. V4.5.11既有Canon / Director / Asset / Storyboard / Video / Temporal / Editorial领域规则；
2. 本M1节新增的Context Loading、Runtime Freshness、Capability Routing与Anti-Shortcut控制规则；
3. Derived Runtime与Prompt，不得反向覆盖以上Authority。

若M1控制规则与V4.5.11领域规则发生冲突，只回滚最小受影响Route并生成Conflict Evidence；不得静默删除任一侧规则。


## 2026-08-28｜Storyboard Approximate Editorial Cut Bridge

- 真实Approved Video仍必须提取Ending Frame并写Continuity Snapshot，用于事实核验、Stage 06剪辑和真正同镜续接；但“存在真实尾帧”不再等于“下一次生成必须直接上传尾帧”。
- `SEAMLESS_EXTEND / GUIDED_CONTINUATION`仍由Verified Ending Anchor拥有模型`t=0`；只有确实要求像素级同镜延续时才走这两条路线。
- 只要Locked Editorial Plan允许真实切镜，默认走`CUT_REPROJECT + STORYBOARD_BLOCKING_APPROXIMATE`：下一镜以Approved Storyboard Exit/Entry、World Spatial State、高清人物/环境Authority和新Shot Execution Frame重建，不直接上传上一视频尾帧。
- 切镜只硬继承剧情必要的空间人物占位：人物在场集合、世界Zone/Anchor、Screen Side或动作方向、深度、朝向、动作Phase、道具Holder与精确数量。微姿态、衣褶、像素纹理、压缩噪声、综合色误差和尾帧局部缺陷不得被提升为下一镜视觉Authority。
- 过渡主要由Locked Editorial Language完成：按当前剪辑方案选择`MATCH_ON_ACTION / CUT_REFRAME / REACTION_CUT / SPATIAL_REORIENTATION / J-CUT / L-CUT / SOUND_BRIDGE / SHAPE_OR_DIRECTION_MATCH`。Storyboard结尾与下一镜入口只需在上述P0占位字段上大致合理，不要求逐像素复制。
- 该路线的目的不是放松连续性，而是把“世界事实连续”与“尾帧像素污染”分离；若剧情必须无缝延长同一动作、同一摄影机或同一Take，禁止借切镜规则规避Ending Anchor。

## 2026-08-27｜Temporal Reference Hygiene Logic-Closed Hotfix

- 从`V4.5.7 temporal-reference-hygiene logic-closed release`前向合并到当前`V4.5.10`主线；这是逻辑热修，不回退Seedance 2.5、30秒Envelope、Proxy-First或全能参考字段分权。
- 时间入口固定为`SEAMLESS_EXTEND / GUIDED_CONTINUATION / CUT_REPROJECT / SCENE_REBASE`；同镜续接由已验证Ending Anchor拥有模型`t=0`，普通人物/道具/环境/综合色/执行帧不得静默成为竞争Primary。
- Ending Anchor必须具备来源、源视频Fingerprint、实际帧Hash、Continuity Snapshot独立验证、递归像素血缘与degradation debt；证据不足必须`TEMPORAL_RESET_REQUIRED`。
- 同镜续接时遵循“Pixels own present, Prompt owns future, Canon owns reset”；需要高清人物母图但会与`t=0`竞争时，先做`TEMPORAL_T0_SUFFICIENCY_ASSESSMENT`，不足则切镜重投影或Scene Rebase。
- 新增Temporal Planner / T0 Sufficiency / Continuity Snapshot机械校验及对抗测试；所有后续Prompt编译必须依据本热修选择时间入口，不得把低质量尾帧当综合色或人物画质Authority。

## V4.5.10｜Asset Library Completeness / Performance / Narrative FX

- Stage 03采用`RICH CANON LIBRARY`：不设置固定图片资产数量上限，由真实Requirement决定资产规模。
- Stage 05采用`MINIMUM_SUFFICIENT_REFERENCE_SET`：只精简当前Job的Direct References，不得反向删掉Stage 03应建立的Authority。
- `PERFORMANCE_ASSET_REQUIREMENT_SET`按Shot判定特殊表情、姿态与Contact静态Support。
- `NARRATIVE_FX_ASSET_MANIFEST`管理剧情型FX的Text-only或Visual Reference模式及状态覆盖。
- Freeze新增`ASSET_LIBRARY_COMPLETENESS_PASS`。
- Reference Video继续禁止；Performance/FX只用静态图片Authority、Storyboard、Prompt与Execution Frame执行。
- Backport只吸收旧资产规则的有效生产哲学；不恢复巨型重复Prompt，也不把“资产库做足”误写成机械生成固定数量的无用视图。

> **项目定位：** 本Skill只服务《断弦之歌》的长期AI短剧生产。它不是通用短剧模板，也不是单纯Prompt集合，而是项目级Production Controller + Canon/Director Authority + Runtime Compiler + QC Gate。

> **V4.5控制面基础：** 同一个执行事实只允许一个Owner。`SKILL.md`不再重复具体领域规则；Workflow、Route、Authority、Runtime、Validation分权。正常生产优先读取结构化State与Runtime；只有首次设计、版本变化、冲突、缺字段或QC失败时回读完整Source Authority。

## 1｜固定六阶段

一级生产流程始终只有六个Stage，不新增Stage 07：

1. **Stage 01｜Source Narrative → Screenplay Lock**
2. **Stage 02｜Director Intelligence → Director Architecture → Production Translation**
3. **Stage 03｜Episode Asset Build → Director Reconciliation → Asset Freeze**
4. **Stage 04｜Mandatory Shot Storyboard → Supplemental Previs → Storyboard Approval**
5. **Stage 05｜Typed Video State → Prompt Compile → Video QC → Ending Frame**
6. **Stage 06｜Editing / Voice / Music / SFX / Color / Subtitle / Master QC**

Workflow状态和合法Transition的唯一Owner：`controller/workflow_state_machine.yaml`。

## 2｜V4.5五类权限

任何规则必须属于以下一种，不得在多个总控文件重复拥有。

### FLOW
回答“当前在哪个状态、下一状态是什么”。

- 唯一Owner：`controller/workflow_state_machine.yaml`

### ROUTE
回答“当前任务应加载哪些Runtime；Runtime失效时回读哪些Source Authority”。

- 唯一Owner：`controller/route_registry.yaml`

### AUTHORITY
回答“某个创作/生产领域具体怎么判断、怎么设计”。

- Source Authority主要保存在`templates/`。
- 事实Owner索引：`controller/authority_registry.yaml`。

### RUNTIME
回答“已经批准的Source Authority如何压缩成当前执行卡”。

- Runtime规则：`templates/runtime_efficiency_system.md`
- Schema：`runtime/*.schema.yaml`

### VALIDATION
回答“当前结果是否满足局部Gate、Task Readiness、Stage Transition或System Integrity”。

- Cross-module不变量：`templates/system_integrity_authority.md`
- 确定性检查优先使用`validators/`。

## 3｜Controller Contract

每次正式生产按以下顺序执行：

1. **Resolve Project State**：优先读取项目当前结构化`episode_state`与`shot_state`；旧项目只有Markdown Workspace时先执行Migration。
   - **Novel Source Re-anchor：** 每个Episode在首次继续生产、Novel Source版本变化、当前镜头语义与改编层发生冲突，或用户要求“读小说/按原著”时，必须读取当前Episode Novel Source并记录绝对路径与SHA-256。篇幅可控时完整读取一次；否则读取当前Sequence及必要前后文。相同Fingerprint已完成Re-anchor后不得每个Shot重复全文加载，但后续导演、资产、Storyboard、Prompt和QC必须回指该Source事实，禁止只根据镜头摘要猜原著。
2. **Resolve Controller Capability**：记录当前执行模型是`MULTIMODAL_ACTIVE`还是`TEXT_ONLY_CONTINUATION`。Text-only模式只能消费Current Visual Evidence，禁止凭文件名/Prompt猜图片内容。
3. **Resolve Next Action**：只用`controller/workflow_state_machine.yaml`计算当前合法Next Action。
4. **Resolve Route**：用`controller/route_registry.yaml`选择当前任务Route。
5. **Prefer Runtime**：若所需Runtime存在、版本/指纹有效且字段覆盖完整，直接使用Runtime；不要为了“更严谨”重复全文读取Source Authority。
6. **Fallback to Source**：Runtime缺失、STALE、规则版本变化、Source版本变化、字段不足、冲突或QC失败时，只回读该Route声明的最小Source Set。
7. **Execute Task**：创作判断由LLM完成；命名、哈希、文件归档、Schema/约束检查等确定性工作优先交给脚本。图片/视频任务必须建立`GENERATION_JOB`并经Host Adapter调用真实生成能力；宿主能力可用时不得只输出Prompt后停住。
   - 任何图片视觉审核先执行`tools/media_review_proxy_builder.py`：Metadata Inventory必须先于Pixel Review；只审最长边不超过1600px的代理图和审核Contact Sheet。Contact Sheet只做Triage，最终APPROVED资产必须单独打开其代理图验收。原始大图仅以绝对路径与SHA-256引用，不得重复通过`view_image`读取。
8. **Run Local Gates**：先跑领域Gate/Validator。
9. **Run Task Readiness**：例如`VIDEO_GENERATION_READY`。
10. **Run Stage Transition**：只有State Machine的Transition prerequisites满足才改变Stage状态。
11. **Run System Integrity**：检查无越权、无假批准、无假Evidence、无静默Director Drift。
12. **Write State**：写回结构化State、Approval Record、Runtime Fingerprint；历史细节进入Ledger，不污染Hot State。

用户说“继续”时，不从Stage 01重读；优先从Current State得到Next Action。

## 4｜Production Modes

### Production Mode
正式制作默认模式。所有Lock、Freeze、Storyboard Approval、Video Approval与Continuity Evidence必须真实成立。

### Demo Mode
允许快速演示方向，但必须明确标识`DEMO / NOT APPROVED / NOT PRODUCTION AUTHORITY`，不得写回正式Canon或Approval State。

### Existing Project Migration
若已有V4.2.x Workspace/Approved成果，继承真实APPROVED成果，不从头重做。先读取`templates/existing_project_migration.md`，把旧Workspace投影到V4.5结构化State；迁移规则不能把未知状态自动升级为APPROVED。

## 5｜Stage最小职责

### Stage 01｜Screenplay Authority
固定执行：

`01A Source Narrative Parse → 01B Screenplay Adaptation → 01C Screenplay QC/User Approval → EPISODE SCREENPLAY LOCKED`

`Story Lock`只保存Canon边界，不能代替Screenplay Lock。Stage 01允许Scene Split/Merge、心理外化、对白改编、戏剧压缩；禁止Shot/Lens/Camera/Storyboard/Reference/Asset越权。

### Stage 02｜Director Authority
只有`EPISODE SCREENPLAY LOCKED`后才开始。

导演选择必须先于生产便利性：

`World State → Audience State/Felt Intent → Directorial Interpretation → Department Critique（D1/D2）→ Director Judge → Sequence Arc → Blocking/Spatial → Cinematography → Detailed Shot Contract → DIRECTOR CORE LOCKED → SHOT_RELATION_GRAPH`

Director Judge之前不得用成本、Reference槽位、已有资产便利度、平台时长能力来选择导演方案。`DIRECTOR CORE LOCKED`后才进入Director→AI Production Translation。

**Editorial Authority：** Sequence Arc之后必须读取`templates/editorial_grammar_engine.md`先建立Editorial Intent Draft；Shot Progression与Formal Shot ID形成后，再与Detailed Shot Contract同步锁定`EDITORIAL_PLAN`。它独立拥有`Viewpoint Arc / Edit Function / Cut Trigger / Cut Timing / Transition / Continuity Strategy`。摄影语言决定单个Shot怎么看，剪辑语言决定为什么此刻切以及注意权交给谁；禁止用“多换几个景别”冒充剪辑设计。`editing_mode`只表达是否允许模型内Multi-shot，实际一次生成包含几个Formal Shot与具体`FORMAT_MODE`由`GENERATION_ENVELOPE`决定；失败可降级为单镜头组接，不改写Editorial Plan。

**Director Perception Hard Gate：** D1/D2 Scene在锁Formal Shot前必须建立`UNRESOLVED_STATE + RELATIONAL_PRESSURE`；每个Formal Shot再锁`CAMERA_ETHICS + ATTENTION_FLOW + SHOT_SCALE_JUSTIFICATION + CAMERA_PLACEMENT_JUSTIFICATION + VISUAL_FORCE_STACK + VISUAL_SALIENCE_BUDGET`。CU/ECU/Detail若只能用“更有情绪/更电影”解释，直接失败；Camera必须同时有物理可达理由与叙事观看理由。`DIRECTOR_PERCEPTION_PASS`是`DIRECTOR CORE LOCKED`前置。跨镜头重复由`SHOT_GRAMMAR_HISTORY + CREATIVE_DRIFT_TELEMETRY`发Warning，不能为了降低重复率自动乱换角度。

### Stage 03｜World & Visual Asset Construction Authority
Production Mode进入图片生成前先完成`SPATIAL_CANON`：按场景复用等级建立最小充分的Location Topology / Building Floor Plan / Room-Zone / Door-Window / Entry-Exit / Sightline / Access / Elevation关系，并把剧情Event Node绑定到真实Location/Zone。

空间事实LOCK后，才生成Environment Clean Canon、Derived Coverage、Required Production Support、Required Shot Assembly、角色/道具等Entity-driven资产，以及由SHOT_RELATION_GRAPH派生的Clue/Sightline/Location Identity等Relation-driven `VISUAL_ASSET_OBLIGATION`。Stage 03内部由`EPISODE_ASSET_BUILD`按Generation Queue自动派发到Character / Environment / Prop / Transformation / Scene Color / Support / Assembly子Route；Queue未清空不得完成Stage 03。 **V4.5.7新生产的所有环境派生视角只创建`ENVIRONMENT_COVERAGE`这一种物理资产类型；Event Node / Reciprocal / Predictive / Clue Reveal / Location Visibility / Location Identity / Required View只写入`coverage_reason_codes`，旧`*_VIEW`类型仅供迁移读取。**

Stage 02C先产出Provisional Manifest；`SPATIAL_CANON_LOCKED`后必须二次收敛Relation-driven需求并形成Final Manifest，之后才允许正式图片Asset Build。只有`SPATIAL_CANON_LOCKED + 关系义务到期项有真实Evidence + Director Spatial Reconciliation`全部成立才允许`EPISODE ASSET FROZEN`。

### Stage 04｜Storyboard + Video Conditioning Authority
**所有正式Shot一律先跑白描分镜，不得例外。** 每一个正式Shot在进入Stage 05前，至少必须有一张**实际生成、视觉QC通过且经用户批准的纯净白描 Clean Storyboard Panel**覆盖，且资产必须声明`STORYBOARD_RENDER_MODE = WHITE_LINE_STORYBOARD_ONLY`；存在关键动作阶段、位移、Camera变化、Focus变化或状态变化时，必须增加足够白描Panel证明关键节点。`Hero Frame / Keyframe Pair / Spatial Map / Camera Path / Shot Execution Frame / Rendered Keyframe`全部只能作为Supplemental Previs或后续Conditioning，**不能替代白描Storyboard Baseline**。

所有白描Panel必须是纯画面：**像素内不得出现任何文字、数字、Shot/Panel ID、时间码、CUT、Camera术语、箭头、运动轨迹线、说明框、气泡、字幕或Logo**。多镜头或多Beat场景默认先以一次真实Image Generation Job生成完整`STORYBOARD_CONTACT_SHEET`，完成Master QC后由`tools/storyboard_contact_sheet_splitter.py`确定性切出`STORYBOARD_CLEAN_PANEL`；只有真正单Panel镜头、局部修复或Provider无法可靠生成Contact Sheet时才允许走单Panel生成Fallback。图像模型不得自行生成带注释的Storyboard Page。切格后如需Review Board，再由`tools/storyboard_grid_assembler.py`对已QC Panels确定性拼版。**只要正式Sequence包含2个及以上Formal Shot，就必须在离开Stage 04前形成并批准整段Storyboard Proof。**

Mandatory白描Panel保留Scene Color Authority的**血缘**但不把彩色色卡作为图像模型直接Reference：Generation Job使用`projection_mode = VALUE_LIGHTING_LINEAGE_ONLY`，只继承光源方向、明暗层级和主体分离；`required_bindings`不得绑定`COLOR_AUTHORITY`。综合色相在后续Shot Execution恢复为Direct Color Reference；进入Final Video后只保留Scene Color Authority为必需血缘，是否额外直绑色卡由Reference Budget按`LINEAGE_ONLY / TEXT_COLOR_CONTROL / DIRECT_COLOR_REFERENCE`动态裁决。

Storyboard的镜头运动、时间、CUT/No-Cut、动作、表演、视线、Shot Relation、Landing等说明只能存在于离图Metadata，并且**必须继续传递到Stage 05 `VIDEO EXECUTION ANALYSIS`与Final Video Prompt**；Metadata不得成为这些执行描述的最终落点。Stage 05必须把它们正规化为`VIDEO_EXECUTION_PLAN.storyboard_handoff`八字段合同，并由`storyboard_to_video_prompt_handoff_lint.py`逐字段检查对应`prompt_anchor`真实出现在Final Video Prompt；只出现同类关键词不算继承。缺项统一标记`STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP`并阻断Video Generation。

Storyboard审批严格分两段：T19先要求Contact Sheet Master真实生成并达到`QC_PASS_WAITING_APPROVAL`，随后确定性Split，所有Mandatory白描Panel完成Panel QC、Entity Binding与Fingerprint登记；此时不得先Promotion。多Shot Sequence可再由这些Panel按Formal Shot顺序确定性拼出Review Board。用户批准时写**一份同时覆盖Contact Sheet Master、Derived Panel IDs与各自Fingerprint**的`APPROVAL_RECORD`，Parent Job与Derived Assets共享同一`approval_ref`后再Promotion。Derived Panel不得伪造独立Image Generation Job。只有`storyboard_contact_sheet_lint.py --phase approved + storyboard_coverage_lint.py --phase approved + storyboard_sequence_grid_lint.py --phase approved（适用时）`共同闭环，才成立`APPROVED PREVIS SET`。

Storyboard QC同时检查Shot Relation：Attention Target、Reveal、POV、Match或其它Cut Motivation必须在相邻Panel中成立。随后必须进入Video Conditioning：每个正式Video Unit至少建立/Promotion一个Approved Shot-specific Primary Visual；涉及镜头关系时再检查A_EXIT ↔ B_ENTRY Pairwise Alignment。**白描Storyboard只能作为Director/Blocking/Temporal Control Reference，不具备Primary Visual Eligibility，不得Promotion成最终Primary Video Conditioning。** Shot Execution Frame必须保留`Master/Coverage → Shot Execution`血缘，并继续绑定当前Scene Color Authority。

`CONTINUITY_ENTRY`若需要上一段真实Ending Frame，必须等待真实`APPROVED VIDEO`产生的Continuity Evidence；计划Exit或Storyboard尾格不得冒充。

### Stage 05｜Video Execution Authority
所有Final Video任务采用Constraint-First：

`Approved Previs + STORYBOARD_SEQUENCE_PROOF（2+ Shot时） → GENERATION_ENVELOPE → Multi-shot Envelope Grid Gate（非ONER时） → VIDEO_CONDITIONING_READY + Runtime → VIDEO_EXECUTION_STATE → Spatial State → VIDEO EXECUTION PLAN → Constraint/Timing/Camera/Body Resolve → Execution Plan Freeze → 镜头执行分析 → Detailed Natural-language Compile → Semantic Dedup → Surface Sanitizer → Egress → Post-Compile Closure → VIDEO_GENERATION_READY`

`Semantic Dedup`不能替代Conflict Solver；`Surface Sanitizer`不能替代Readiness；自然语言编译完成后仍必须做Post-Compile Closure。Scene-bound Video必须保留Primary Shot Execution的Approved血缘，但是否把该合成图直接送入模型由Target Adapter裁决。**《断弦之歌》采用`FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING`：当前Location的Approved Empty Environment Master和画面中每一名清楚可见人物各自的Approved Character/FMH Master始终是身份/几何Authority；Storyboard只负责Blocking/Timeline/CUT；Primary只负责它仍然独占且未被更高清Authority覆盖的构图或连续性字段。** 同一字段不得同时由白描、低清合成Primary和高清母图争夺。对于即梦 Seedance 2.0 全能参考，若Approved白描Storyboard + Final Prompt已经完整覆盖动作、站位与CUT，且Shot-specific Primary只是把同一人物/场景再次低清合成，则Primary默认`OMIT_REDUNDANT_BAKED_COMPOSITE`，不得为了“完整包”强制上传；这不影响Primary作为内部QC与血缘Evidence保存。Storyboard直绑时必须明确“只参考动作/Blocking/镜头顺序，不参考白描画风、人物身份、纹理与最终画质”。平台槽位不足或字段冲突时必须BLOCK或重路由，不能让低保真参考压过高清人物/场景母图。


**Generation Envelope Authority：** Formal Shot与Video Generation Call不再强制1:1。Stage 04B读取`templates/generation_envelope_engine.md`建立`GENERATION_ENVELOPE`：`ONER / SEQUENTIAL_MULTISHOT / TIMED_MULTISHOT / FREESTYLE_BROLL`。非ONER必须为每个CUT绑定独立Approved白描Panel，再按CUT顺序真实运行`storyboard_grid_assembler.py`生成Envelope级`STORYBOARD_CLEAN_SEQUENCE_BOARD`；Panel数量、顺序、Board Fingerprint、QC任一不闭合都报`MULTISHOT_STORYBOARD_GRID_*`并禁止视频生成。Seedance目标可读取`adapters/generation/seedance_multishot_profile.yaml`编译FOV Anchor、受控CUT格式与Positive Locks；Provider能力不足时拆回Single-shot Envelopes。

**Execution Plan Hard Gate：** Stage 05必须先执行`templates/video_execution_plan.md`，用结构化计划解决Reference、空间站位、肢体/道具占用、动作与微表情因果、Camera竞争、时长负载、物理/环境/声音同步；只有`VIDEO_EXECUTION_PLAN_PASS=YES`才允许写Final Prompt和建立Video Generation Job。20项Coverage是完整性检查，不是20段说明书，最终正文必须按时间因果融合。

**Prompt Control Restoration：** `@图`是稳定锚点，不是详细视频导演文字的替代品。每个Stage 05 Video Unit在Final Prompt前必须形成用户可核对的`镜头执行分析`，至少覆盖：镜头目标、起始状态、人物外观/服装必要确认、场景空间、道具状态、构图、景别、摄影机、时间轴、逐段动作、表演、视线、肢体占用、物理反馈、环境动态、光影综合色、声音、对白/呼吸、结尾状态、必要负面限制。`PROMPT_LENGTH_CEILING = NONE`；正常Seedance Final Video Master Prompt的**模型可执行正文至少2500个非空白字符，Master上限为NONE**。不得因Reference已绑定、Runtime Fast Path、Semantic Dedup或Surface Sanitizer自动压成短Prompt，也不得仅因正文较长而裁剪仍具因果控制价值的内容。

**Stage 05 Prompt Authority Order：** `video_prompt_template.md → prompt_compiler.md → prompt_egress_gate.md → video_prompt_detail_lint.py`拥有最终Video正文结构与详细度；`execution_reference_semantics.md / visual_reference_routing.md / prompt_semantic_deduplication_engine.md / model_facing_prompt_surface_sanitizer.md`只能处理绑定、路由、去重与行政净化，**不得删除上述20项中当前Shot适用的执行信息**。发生冲突时必须报`REFERENCE_TEXT_SUPPRESSION_CONFLICT`或`PROMPT_DENSITY_POLICY_CONFLICT`并返回Compiler。

**Combat Conditional Prompt Lock：** 当前Video Unit被判定为真实战斗/追逐近身冲突时，上述20项仍全部保留，并额外强制覆盖`Combat Objective / Engagement Distance / Read→Decision / Attack-Defense Exchange / Attack-Escape Lane / Contact or Near Miss / Force Direction / Recoil-Recovery / Initiative Shift / Combat Camera Read / Exit Combat State`。缺任一适用项不得进入Video Generation；普通非战斗镜头不得被该条件规则误加战斗字段。

实际Video Take出现后才进入Video QC。`QC PASS`不等于`APPROVED`；只有用户明确批准后才登记`APPROVED VIDEO`。Ending Frame只能从真实Approved Video建立。

### Stage 06｜Post
Locked `EDITORIAL_PLAN`是Picture Assembly的导演剪辑意图Authority，`GENERATION_ENVELOPE`记录实际生成打包与CUT Contracts。Stage 06按真实Approved Takes确定精确IN/OUT并执行J/L Cut、Match、Action Cut、Reaction Cut、Reveal、Ellipsis、Parallel/Contrast等已锁策略；Multi-shot Take允许按CUT做Sub-cut Salvage，好的CUT保留、失败CUT拆成Single-shot Envelope重生替换，但不得改变Viewpoint Arc或关键Reveal/Reaction/Cut Motivation。
只对已批准或明确登记为可用Salvage的素材做剪辑、配音、环境声/Foley/SFX、BGM、调色、字幕与Master QC。

## 6｜全局不变量

完整定义见`templates/system_integrity_authority.md`。以下必须常驻：

1. **One Fact → One Owner**：执行Authority不能重复拥有同一个事实。
2. **No Stage Bypass**：不得绕过State Machine prerequisites。
3. **QC PASS ≠ APPROVED**：用户批准是独立事件。
4. **No False Evidence**：不存在真实文件/视频/图像Evidence时不得声称已检查、归档或生成。
5. **Ending Frame Authenticity**：Continuity Ending Frame必须来自真实Approved Video。
6. **No Silent Director Drift**：执行层不得为模型便利静默改变Director Invariants。
7. **Runtime Cannot Create Authority**：Runtime只能投影Source Authority，不能创造新Canon/规则。
8. **Authority Change Propagates**：Source版本变化必须使相关Runtime/下游State失效或触发Change Impact。
9. **Revision Scope Is Minimal**：返工只重新打开真正受影响的QC维度和下游依赖。
10. **Fresh Compile After Stale/Conflict**：旧Prompt只能恢复Intent，不能作为不断追加补丁的文字母版。
11. **Prompt Surface Is Executable Only**：Stage/Gate/文件路径/内部Asset Metadata不得泄漏到模型执行Prompt。
12. **Hard Capability Boundary**：平台能力未知时保持UNKNOWN，不得编造时长、槽位、文件能力或QC能力。
13. **Mandatory Asset Mention**：Current Generation Profile下，当前任务真正MUST_BIND / DIRECT_BIND / CONTINUITY_ENTRY等强绑定Approved Asset必须以真实平台原生`@资产`Mention进入Generation Prompt；不得因为资产已在UI/Runtime中存在而静默省略，也不得伪造不存在的Token。
14. **No Blind Visual Guessing**：当前Controller没有视觉能力时，不得根据文件名、Asset ID、原生成Prompt或历史意图推断图片实际内容；任何`@资产`视觉选择必须来自Fingerprint匹配的Current Visual Evidence。
15. **Generation Must Close**：正式图片/视频任务必须从`GENERATION_JOB`走到真实Result Handle/Candidate；宿主能力可用时，“只给Prompt”不算完成。
16. **Scene Color Follows Scene, Reference Slots Stay Lean**：Approved Base Color Card在新Scene/Look Domain自动派生Scene Color Card；Scene-bound图片与Shot Execution直接继承/绑定它。Final Video必须保留同一Scene Color Authority血缘，但色卡默认`LINEAGE_ONLY`，只有明确风险Trigger才占用Direct Reference槽。
17. **Asset Lineage Is Preserved**：Coverage、Shot Execution与Video必须能回查Parent Master/Source Generation Job；不得产生无父来源的孤立最终@图。
18. **White-line Storyboard Universal Gate**：每一个正式Shot必须先有Approved纯净白描Clean Panel Coverage；任何彩色/精修/视频执行静帧或Supplemental Previs均不得替代。2+ Formal Shot的正式Sequence必须额外拥有整段Approved白描宫格；非ONER Generation Envelope还必须拥有与CUT子集严格对应的Envelope宫格。
19. **Storyboard Text Off-Pixel, Video-Prompt On**：Storyboard像素零文字零箭头；离图的Camera/Timing/Cut/Action/Performance/Eyeline/Relation说明必须编译进对应Stage 05 Final Video Prompt，缺失即阻断Video。
20. **Editorial Before Coverage**：正式Sequence先锁Viewpoint Arc与Cut Logic，再落Formal Shots；不得先做机械Coverage再随机加切镜。默认跨视角通过多Shot生成+Stage 06组接，不把多机位随机切换压给单个Video Unit。
21. **Perception Before Optics**：D1/D2先解决不可解决状态、关系压力与观看伦理，再锁景别/Lens；特写必须证明不可替代的信息收益与空间代价。
22. **Anti-Pattern Memory Is Advisory**：Shot Grammar History只识别无意识偏置；重复可以是有意风格，Telemetry Warning不得自动改导演方案。
23. **Causal Sequence Resists Shuffle**：声明为CAUSAL的Sequence必须有Information/Action/Eyeline/Audio依赖；Associative/Montage按自身组织逻辑验收。
24. **Execution Density ≠ Visual Salience Density**：Stage 05可以详细，但每镜仍保持有限视觉主次，不能把所有Prompt事实变成同等显眼。

## 6.1｜V4.4 Visual Asset Hard Boundary

- Color Board、Style Board、Environment/Mechanism Design Board、Whole Storyboard**允许**按平台能力直接进入Video Reference Pack；
- 它们默认是字段级Auxiliary Authority，不因Direct Bind自动取得Primary Visual权限；
- 每个正式Video Unit必须有Approved `VIDEO_FIRST_FRAME / VIDEO_SHOT_EXECUTION_FRAME`等Primary Visual Conditioning；
- 已有Storyboard Panel / Coverage / Assembly若完全满足当前镜头，可通过Promotion复用，不强制重生成；
- 没有Primary Visual时禁止`APPROVED_PREVIS_SET → VIDEO_GENERATION_READY`直通。

详细Owner：`templates/visual_asset_usage_authority.md`、`templates/video_conditioning_asset_architecture.md`、`templates/video_conditioning_readiness_gate.md`。


## 6.2｜V4.5 Relation-Driven Asset Hard Boundary

- `DIRECTOR BREAKDOWN READY`前必须建立Locked `SHOT_RELATION_GRAPH`：相邻Shot不仅要各自合理，还要记录“为什么是这个下一个Shot”。
- Stage 02C必须从Shot Relation派生`VISUAL_ASSET_OBLIGATION`；资产需求同时包含Entity-driven与Relation-driven。
- `CLUE_REVEAL / LOOK_POV / MATCH / ACTION_CONSEQUENCE`等关系若需要特定Sightline、Location Identity或线索视角，必须在Stage 03产生对应静态资产，不得只靠文字声明。
- Episode Asset Freeze前必须完成所有`fulfill_by=STAGE_03_FREEZE`的关系资产义务。
- Storyboard QC必须验证Attention Target / Reveal / Cut Motivation已经在相邻Panel中可读。
- Video Conditioning QC必须验证A_EXIT ↔ B_ENTRY的Pairwise Alignment；两张各自正确的图不等于关系正确。
- “两个地点各有Master”不能证明地点之间的可见性、外内同一性或叙事指向。

结构化Owner：`state/shot_relation_graph.schema.yaml`、`state/visual_asset_obligation.schema.yaml`；语义Owner分别为`templates/director_architecture_engine.md`与`templates/shot_coverage_asset_derivation.md`。


## 6.3｜V4.5.2 Spatial-First + Clean Storyboard Hard Boundary

- **Cheapest Solvable Layer First：** 方位、门窗、可见性、进入路径、高差等问题必须在Spatial Canon解决；能在结构层解决的问题禁止拖给图片或Video。
- 重要/复用地点先成为可验证的Location Entity，再成为图片：室外优先Topology，室内优先Floor Plan/Zone/Anchor；图给人审核，结构化`SPATIAL_CANON`给机器执行。
- Planning Diagram允许ID、文字、箭头、路径，因为它不作为成片视觉Reference；Storyboard/Shot Execution等Visual Production Image默认必须Clean。
- **所有正式Shot的Mandatory Storyboard视觉层只能使用纯净白描Clean Panel作为Baseline**；彩色精修Storyboard、Hero Frame、Shot Execution Frame、Keyframe、Spatial Map或Camera Path都不能替代。
- Storyboard图片只表达构图、Blocking、姿态、视线、空间、剧情状态；**不得烤入任何文字、数字、Shot/Panel ID、时间码、CUT、Camera术语、箭头、运动轨迹线、说明框、字幕或Logo。**
- 宫格由独立白描Clean Panel通过确定性排版合成；图像模型不负责设计带字Storyboard Page。时间、CUT、Camera Motion、Shot Relation、动作与表演说明先写入离图Metadata/Prompt，并在Stage 05**强制编译进Final Video Prompt**；不得只留在Storyboard Metadata。
- `SHOT_RELATION_GRAPH`在Stage 02C先做Planning Validation；Spatial Canon建立后再做Spatial Proof Validation。文字声明`DESTINATION_IDENTITY_PROVEN`不算Evidence，必须能回指真实Spatial Relation和到期Visual Asset Obligation。


## 6.4｜V4.5.2 Script-Grounded Virtual Set Hard Boundary

- Spatial Canon不是建筑设定收藏，而是剧情事件的物理落点：`SCENE_EVENT_NODE → LOCATION/ZONE/ANCHOR → CHARACTER_EVENT_ROUTE`必须可追溯。
- 室外重要Set的Topology必须能回答节点、方向、距离/距离等级、坡向/高差、角色完整动线；室内重要Set的Floor Plan必须回答Room/Zone、Door/Window、Entry/Exit与跨房间路径。
- Planning Diagram允许文字、ID、箭头和路线，但它只是Spatial Evidence；所有后续场景图片必须回指已批准Spatial Parent，不能“拓扑图画完以后各画各的”。
- Event/Relation Coverage支持`FORWARD / REVERSE / LOOK_BACK / LANDMARK / ENTRY / EXIT`等关系视角；需要双向空间证明时可派生Reciprocal Coverage。
- 多角度Set Coverage采用双Parent：`Spatial Parent`锁Geometry，`Visual Parent`锁材质/美术/综合色；不得从每个新角度重新设计同一个房间。
- Coverage数量由后续剧情和镜头需求预测，不为了凑九宫格机械生成；`PREDICTIVE_COVERAGE`只生产能够被Event/Shot/Relation/高复用机位证明的视角。
- Stage 03采用Cascade Approval：Spatial Diagram/Canon未批准不得批量生成依赖它的Event View；Base Visual未批准不得批量派生Coverage；上游失败立即停止下游生成。
- `INTERIOR_LOOK`与`EXTERIOR_LOOK`默认分Domain冻结并一路投射到Video；主要/反复角色若项目要求固定声音身份，`VOICE_IDENTITY`也属于Episode Asset Freeze的一部分。
- 每个正式资产必须有`WHY_REQUIRED / REQUIRED_BY / DOWNSTREAM_USE`；没有故事、空间、镜头、关系、复用或连续性理由的“可能以后有用”资产不得进入正式生成队列。

## 6.5｜V4.5.3 Visual Evidence Handoff Hard Boundary

- 多模态模型/人工真正看过并保留的正式图片，应把Observed Facts、Issue Codes、Role Assessment与Source Fingerprint写入`VISUAL_EVIDENCE`；一次视觉检查不能只存在于当前对话。
- `TEXT_ONLY_CONTINUATION`可以继续剧本、导演、Spatial Canon、Relation、资产需求、Prompt编译和State维护，但**禁止创建新的视觉PASS、禁止修改Observed Visual Facts、禁止从Prompt/文件名猜图片结果**。
- Text-only模式使用现有Image Asset作为Generation Reference前必须通过`REFERENCE_VISUAL_EVIDENCE_GATE`：Evidence存在、Fingerprint匹配、Required Visual Facts被覆盖、Forbidden Facts无冲突、Reference Role未越权。
- Evidence缺失只阻断依赖该图片的视觉决策；将该Asset加入`VISUAL_REVIEW_QUEUE`，不默认让整个Episode从头重做。
- 资产文件变化后旧Evidence自动`STALE`；旧Evidence不得继续驱动`@资产`选择。
- Visual Evidence回答“图片实际上画了什么”；Canon回答“项目事实应该是什么”。二者冲突时不得让旧图反向篡改Canon。

Owner：`templates/visual_evidence_handoff.md`；结构化状态：`state/visual_evidence.schema.yaml`；Runtime：`VISUAL_EVIDENCE_RUNTIME`。

## 6.6｜V4.5.4 Required View Realization Hard Boundary

- **Declared Coverage ≠ Realized Coverage：** Event Node / Shot / Relation声明`FORWARD / REVERSE / ENTRY / EXIT / LOOK_BACK / LANDMARK / CLUE / DETAIL`后，必须物化为`view_requirements`；不能只写“需要正视角”然后靠生成模型自行理解。
- 每条Required View必须至少明确：`Camera Origin`（Zone/Anchor）→ `Optical Axis`（Target/Direction）→ `Must See`（Required Visible Anchors）→ 必要`Must Not See`。例如车厢前向视角应写“后排中轴→前挡风玻璃，必须见方向盘/仪表台/驾驶位/副驾位/挡风玻璃”，而不是模糊“车内正视角”。
- Stage 03先建立`VIEW_ROLE_COVERAGE_MATRIX`，跨所有Scene合并真实镜头需求；只生成MISSING的Required View，不固定九宫格，也不以“已经生成很多图”替代Coverage完整性。
- Coverage Asset必须回指具体`view_requirement_id`。若某方向已经生成超过候选预算，而仍有P0/P1 Required View为MISSING，触发`COVERAGE_BUDGET_STARVES_REQUIRED_VIEW`并停止继续堆同方向候选。
- Freeze前不仅检查Asset Metadata，还必须由Current Visual Evidence证明实际图片的`Observed View Role / Camera Origin / Optical Axis / Visible Anchors`与Requirement一致。Prompt、文件名、Asset ID声称“FORWARD”不算视觉证明。
- 任一Required View缺资产、选中的Fulfillment未APPROVED、Evidence过期、实际方向错误或Must See Anchor缺失，均禁止`EPISODE_ASSET_FREEZE`。
- 多场景按同一规则逐Scene建立Required View Set；Tier S/A可做Predictive Coverage，但预测视角仍必须有真实`shot_ids / event_node_ids / relation_ids`或复用理由，不为凑视角数量生成。

Owner：`templates/shot_coverage_asset_derivation.md`；结构化Source：`state/spatial_canon.schema.yaml:view_requirements`；机械Gate：`validators/required_view_realization_lint.py`；确定性缺口矩阵：`tools/view_coverage_planner.py`。


## 6.7｜V4.5.5 Everyday Realism & Plausibility Hard Boundary

- **Reality by Default：** 除变身、战斗、超自然、梦境/幻觉、象征化等被Canon明确标记的局部范围，所有普通剧情按现实世界运行。
- 普通视觉资产在“好不好看”之前先检查：`Environment Functional Reality → Architecture/Vehicle → Human Occupancy/Ergonomics → Object Affordance → Social-Spatial Plausibility → Mundane Physics → Mundane Continuity`。
- `VEHICLE`是独立Location Kind；重要车辆先建立具体`vehicle_type + VEHICLE_LAYOUT`，锁驾驶控制区、乘员座位、出入口、通道、前后方向与容量，不能把车辆当普通房间自由重排。
- 人物进入Environment后必须满足Expected Cast Count、身份唯一性、Zone/Seat/Functional Position、支撑面、人体尺度、可达性和必要互动距离。人数对了但座位/功能位置错，仍然FAIL。
- 一张图若物理、功能、人体工学、建筑/车辆、社会空间或因果明显不合理，即使构图/综合色/人物脸很好也不得APPROVE。 **漂亮不能抵消不合理。**
- 超现实Exception必须精确写`scope + allowed_categories + reason`；只豁免被Canon真正改变的维度，禁止`THIS_IS_FANTASY_SO_REALISM_OFF`。
- 发现P0/P1现实性失败时先运行`Asset Logic Reconciliation`：判断Owner属于Source / Realism Contract / Spatial Canon / World State / Generated Asset / Visual Evidence，再做最小Patch。Canon正确时不得为了迁就错误图片改Canon。
- `TEXT_ONLY_CONTINUATION`只能读取Current Visual Evidence中的Observed Realism；Evidence缺失/UNKNOWN时只把当前阻塞资产加入Visual Review Queue，禁止根据Prompt猜“现实合理”。

Owner：`templates/everyday_realism_plausibility_gate.md`；结构化Source：`state/realism_contract.schema.yaml`；Runtime：`REALISM_RUNTIME`；机械Gate：`validators/everyday_realism_lint.py`。

## 6.8｜V4.5.6 Logic Integrity Hard Boundary

- **Contract Lifecycle不是自锁：** `DRAFT → QC_PASS_WAITING_APPROVAL → LOCKED`。Stage 03 Spatial QC允许验证DRAFT；只有用户批准后才LOCK，Build/Freeze/Storyboard/Conditioning/Video下游才要求LOCKED。
- **Reality Coverage不可漏绑：** V4.5.6普通`IMAGE`资产必须显式声明`realism_applicability`。`REQUIRED/SCOPED_EXCEPTION`必须绑定真实`REALISM_CONTRACT`；`NOT_APPLICABLE`必须给理由，不能靠省略字段绕过Reality-by-Default。
- **Exception ID不是权限：** 资产写了`realism_exception_ids`只是在选择候选豁免；只有该Exception真实存在、允许该Category、且当前Asset/Shot/Event/Scene命中其Scope时才生效。
- **Fine-grained Evidence > Summary：** 驾驶员前向视野、Vehicle前后方向、人体Zone/Seat、Access Path、支撑/可达等具体Observed事实一旦FAIL，粗粒度`VEHICLE_REALISM: PASS`或`overall: PASS`不得覆盖。
- **Reality Basis：** 常识可标`COMMON_KNOWLEDGE_OK`；历史车型、专业机械、医疗/工业等时代或技术特定事实若标`REFERENCE_REQUIRED`，必须有已验证Reference Provenance，禁止把LLM猜测锁成Reality Canon。
- **Stage Reality Closure：** Storyboard、Video Conditioning、Pre-Video Reference Pack和实际Video Take都必须各自产生可追溯Reality PASS。实际Video的PASS必须来自Fingerprint匹配的多模态/人工QC Evidence，Text-only Controller不得自行创建。
- **Failure Code Closure：** Hard Validator发出的错误码必须能直接或经`failure_router.code_aliases`解析到确定Rollback Route；未知P0/P1错误码视为Release-blocking Integrity Failure。

机械Owner：`validators/everyday_realism_lint.py`、`validators/video_realism_qc_lint.py`、`validators/v456_architecture_lint.py`。

## 7｜State Plane

V4.5正式状态以结构化记录为主：

- `state/episode_state.schema.yaml`
- `state/shot_state.schema.yaml`
- `state/editorial_plan.schema.yaml`
- `state/asset_registry.schema.yaml`
- `state/approval_record.schema.yaml`
- `state/continuity_snapshot.schema.yaml`
- `state/shot_relation_graph.schema.yaml`
- `state/visual_asset_obligation.schema.yaml`
- `state/spatial_canon.schema.yaml`
- `state/visual_evidence.schema.yaml`
- `state/realism_contract.schema.yaml`

旧`templates/episode_workspace.md`与`templates/continuity_snapshot.md`保留为人类可读说明/迁移兼容层，不再作为唯一机器状态源。

任何Lock/Freeze/Approval建议同时保存：

- `artifact_id`
- `version`
- `sha256`或等价稳定Fingerprint（有真实文件/结构化内容时）
- `status`
- `approved_at`（可用时）
- `source_refs`

“LOCKED”必须能回答“锁的是哪一版”。

## 8｜Runtime Plane

正常重复生产优先使用：

- `STORY_RUNTIME`
- `DIRECTOR_RUNTIME`
- `ASSET_RUNTIME`
- `SCENE_RUNTIME`
- `SPATIAL_CANON_RUNTIME`
- `REFERENCE_RUNTIME`
- `VISUAL_EVIDENCE_RUNTIME`
- `REALISM_RUNTIME`
- `VIDEO_CONDITIONING_RUNTIME`
- `VIDEO_RUNTIME`
- `QC_RUNTIME`

Runtime必须记录`source_versions / source_fingerprints / skill_version / scope / invalidation_triggers`。任何关键Source变化都使相关Runtime变为`STALE`并触发最小重编译。

详细规则：`templates/runtime_efficiency_system.md`。

## 9｜Route与Context Isolation

所有按需加载集合只由`controller/route_registry.yaml`维护。旧`templates/load_on_demand_controller.md`只作为兼容说明，不再维护第二份Route表。

特别规则：Stage 02A Director Intelligence执行时，Route必须隔离以下生产便利上下文：

- Cost Optimization
- Existing Asset Convenience
- Reference Slot Limit
- Platform Duration Mapping

Hard physical/story impossibility可以作为Feasibility Boundary提供，但不能替导演选择审美方案。

## 10｜Prompt Egress

Stage 03/04/05及Revision的可执行Generation Prompt必须经过Route声明的Surface/Egress/Validator链。

用户交付Stage 05时可以先显示结构化`镜头执行分析`供审核；真正可复制的Prompt代码块仍只包含模型执行所需内容。内部任务壳、路径、Registry、Stage、Authority、QC Checklist、Runtime字段名不进入Copy Surface。**但真实Generation Asset Mention属于模型执行内容：Current Project Default下，每个强绑定Approved Asset必须显式`@资产`调用。** 具体语法与例外读取`adapters/generation/platform_profile.yaml`和`templates/execution_reference_semantics.md`。

若脚本能力可用，优先运行现有：

- `validators/prompt_surface_lint.py`
- `validators/prompt_constraint_lint.py`
- `validators/post_compile_constraint_lint.py`
- 以及Route声明的其他Validator。

## 11｜失败与最小回退

失败不默认从头重做。使用`controller/failure_router.yaml`确定Owner Stage与最小Rollback：

- Canon/Asset缺口 → Stage 03最小补资产，必要时Break/Re-Freeze；
- Storyboard/Blocking/Shot Contract问题 → Stage 02/04对应最小Patch；
- 纯视频执行失败 → Stage 05；
- 可保留时间窗 → Temporal Salvage，不自动升级为Approved；
- Source Authority变化 → Change Impact后只重开受影响依赖。

## 12｜平台Adapter

平台限制不再散落到总控规则。网页版多模态QC当前Profile：`adapters/web_qc/platform_profile.yaml`。

生成平台时长/Reference槽位等能力若没有可靠Profile，一律保持`UNKNOWN`，由执行Route在获得真实平台信息后映射。

## 13｜用户交互

一人制片默认由Skill自动维护状态与依赖；用户主要负责：

- 提供/确认剧情或Canon级不可裁决信息；
- 上传真实生成结果；
- 对需要User Approval的Screenplay、资产、Storyboard、Video等明确批准/要求修改；
- 在审美选择存在真正不可自动裁决分歧时做最终决定。

能根据当前Approved Authority自动裁决的问题不要反复询问用户。

## 14｜语言与回答

中文为主，必要时保留专业English Terms并首次解释。回复优先输出当前结论、Next Action、需要用户做的最小动作；内部Authority/Runtime细节只有在排错、审计或用户要求时展开。

## V4.5.7 Logic Closure Patch｜Storyboard → Prompt → Video → Next Unit

- Storyboard必须真实生图并进入Generation Spine；只产出Storyboard Prompt不算完成。
- `VIDEO EXECUTION PLAN`必须绑定Director / Approved Storyboard / Shot Execution / Scene Color / World State五类Source Fingerprint；任一改变立即STALE。
- 满足“至少2500字符、Master上限NONE”的Seedance Master Prompt必须持久化成`VIDEO_PROMPT_ARTIFACT`；Video Job没有真实`prompt_ref + prompt_fingerprint + execution_plan_ref + execution_plan_fingerprint`时禁止READY。
- Approved Video必须提取真实Ending Frame并写Continuity Snapshot；有下一Video Unit时必须回Stage 04继续，不能提前进入Post。
- Stage 04/05所有State Machine Gate必须在`controller/gate_producer_registry.yaml`登记明确Producer；禁止出现“状态机要求字段、但没有任何模块负责产生”的悬空Gate。


## V4.5.7 Generation Envelope + Multishot Grid Patch

- Formal Shot与AI Generation Call解耦；新增`state/generation_envelope.schema.yaml`与`templates/generation_envelope_engine.md`。
- 新增`FORMAT_MODE = ONER / SEQUENTIAL_MULTISHOT / TIMED_MULTISHOT / FREESTYLE_BROLL`。
- 2+ Formal Shot Sequence强制`STORYBOARD_SEQUENCE_PROOF`白描宫格；非ONER Envelope再强制CUT级白描宫格。
- `tools/storyboard_grid_assembler.py`支持Manifest与SHA-256顺序证据。
- Stage 05新增`generation_envelope_lint.py + multishot_prompt_lint.py`硬检查；多镜Prompt不得塌成单镜头或擅自新增CUT。
- Seedance Adapter提供FOV Anchor与Positive Lock编译，不把Provider参数反写成Core Director Authority。
- Stage 06允许Sub-cut Salvage，失败CUT最小重生。


## V4.5.7 Spatial Continuity + Multiview Canon

当前版本新增：白描分镜匿名几何人形硬门、`MINOR_HUMAN_CANON_VIEW_SET`、`CROWD_ARCHETYPE_SET`、`PROP_CANON_VIEW_SET`、`ENV_VISUAL_ANCHOR_SET`、`SPATIAL_CONTINUITY_STATE` 与 `SHOT_BOUNDARY_CONTINUITY_CONTRACT`。目标是把“会换机位”与“资产/站位真的撑得住换机位”闭合起来。详情见 `docs/V4.5.7_SPATIAL_CONTINUITY_MULTIVIEW_UPGRADE.md`。


## V4.5.7 Storyboard Entity Binding → Video Closure

匿名白描中的`H_A/H_B/P_A/E_A`只存在于离图`STORYBOARD_ENTITY_BINDING_MAP`，稳定映射真实Entity与Approved资产候选；Stage 05通过`entity_binding_reference_resolver.py`按`FULL_AUTHORITY_DIRECT_BINDING`把Environment Slot和每个清楚可见Human Slot解析成独立Direct Reference，并由`video_entity_binding_handoff_lint.py + full_authority_direct_binding_lint.py`保证空场景、人物母图、白描分镜与真实`@资产`全部进入Final Prompt及Generation Job。详见`docs/V4.5.7_STORYBOARD_ENTITY_BINDING_VIDEO_CLOSURE.md`。


## V4.5.7 Contact Sheet First Storyboard

多镜头或高动作密度场景默认采用 **4/6/9/12/16/25... 白描Contact Sheet一次生成**。规范顺序为：`Contact Sheet Generation → Master QC → deterministic Split → Panel QC + Entity Binding → Review Board（可选）→ 一次User Approval覆盖Master+Derived Fingerprints → Promotion`。Contact Sheet Master永远`direct_input_allowed=false / primary_visual_eligible=false`，不得直接喂给视频模型；Stage 05只使用经批准的切格Panel、Shot Execution Frame及Resolver挑出的最小充分Reference。


## V4.5.7 Base Visual Authority Hardening

- 每个正式Environment/Sub-location（Tier S/A/B/C）必须有一张无人物的Empty Environment Clean Master。
- 每个清楚可见的配角/一次性功能人物必须有一张独立FMH/Minor Human Master，即使只出现一次。
- Storyboard / Shot Assembly / Previs不能替代上述Base Master。
- 图片多不视为问题；通过`BASE_VISUAL_AUTHORITY_MANIFEST + ASSET_REGISTRY + reuse_key + version/lineage`统一管理和复用。


## V4.5.9｜即梦 Seedance 2.0 全能参考 + 长时多镜修正

- 目标平台为即梦 `Seedance 2.0 / 全能参考`时，必须加载`adapters/generation/jimeng_seedance_2_0_omni_profile.yaml`，不得继续套用旧的“所有Authority图片全部直绑”规则。
- `Approved / retained in lineage`不等于`must upload`。Shot-specific Primary可以保留为内部构图、现实性和连续性Evidence；当它只是重复合成人物母图、空场景母图与白描动作时，Direct Route必须为`OMIT_REDUNDANT_BAKED_COMPOSITE`。
- 即梦包优先级：`高清人物/FMH母图 + 高清Empty Environment Master + 必要Critical Prop Master`高于低清/重复合成Primary；白描只承担动作、Blocking、镜头顺序和CUT，不得承担身份、纹理、综合色或最终画质。
- 白描与Prompt已经共同闭合动作/时间轴时，禁止再上传一张重复同构图的合成图“加强控制”；这会触发`REDUNDANT_COMPOSITE_REFERENCE_COMPETITION`。
- 每个`@图片N`必须在Prompt中声明唯一字段职责；同一字段出现多个视觉Owner时先解冲突再生成。没有权重控制的UI尤其要避免同时输入内容近似但保真度不同的图片。
- Seedance 2.0公开能力支持最长15秒高质量多镜头输出。当前Sequence可在15秒内闭合多个因果Shot时，优先`TIMED_MULTISHOT / SEQUENTIAL_MULTISHOT`，不要机械拆成2–4秒的独立调用。只有连续性、复杂动作负载、身份数量或Ending Frame真实性确实要求时才拆。
- 多镜Envelope仍必须使用Approved白描Sequence Proof，并逐CUT声明时间窗、画面主体、动作、镜头、声音与转场；“长视频”不等于让模型自由补镜头。
- 当前Provider Profile和用户明确要求属于Target Adapter Authority，可以重编`GENERATION_ENVELOPE`与Reference Pack，但不得改写Novel、Screenplay、Director Intent或已锁的因果顺序。


## V4.5.10｜即梦 Seedance 2.5 30秒长叙事 + 单次完整因果段落

- 目标平台为即梦 `Seedance 2.5`且用户界面真实提供30秒额度时，必须加载`adapters/generation/jimeng_seedance_2_5_30s_profile.yaml`；不得继续套用2.0的15秒上限，也不得因为额度存在就机械填满无意义动作。
- Seedance 2.5官方能力为单次最长30秒长叙事，并强化多镜头衔接、音画一致性、时间戳控制与多模态参考；当前UI能力仍以用户实际可见选项为最终证据。
- 30秒额度优先承载一个具有`Setup → Evidence → Withholding → Exception → Reaction → Threat Landing`完整因果弧的`TIMED_MULTISHOT` Envelope。若现有相邻正式Shot总时长接近30秒，允许只通过有叙事价值的等待、余音、反应阈值和结尾HOLD补足；禁止新增剧情事实、重复动作、随机运镜或模型自由补镜头来凑时长。
- `30秒长视频`不等于`30秒无切镜ONER`。是否切镜仍由Locked Editorial Plan拥有；当前段需要对象证据、人物近景和环境威胁时，应保留受控CUT。只有导演方案本身锁定一镜到底时才使用ONER。
- 30秒Envelope必须逐CUT封闭累计时间窗，总和精确等于30秒；每个CUT明确主体、景别、动作、表演、肢体占用、物理反馈、声音桥、进入与落点，并在Prompt中声明精确CUT数量、顺序及“不得新增CUT”。
- 30秒只上传最小充分字段集合：高清Empty Environment、每名清楚可见人物母图、Approved整段白描Sequence Board、必要Critical Prop Detail、Scene Color与Global Style。即使2.5允许更多素材，也禁止用冗余低清合成人物/场景Primary填槽位。
- 白描Sequence Board继续只拥有`ACTION / BLOCKING / SHOT_ORDER / CUT_TIMING`；Prompt必须明确排除白描画风、无脸人体、灰度、纹理与最终画质继承。角色、场景、道具、颜色与风格分别由高保真单项图拥有。
- 当一个30秒Envelope能够保持同一Location、同一综合色、同一因果顺序且无需中间真实Ending Frame时，优先单次生成，避免把同一高潮拆成多个短调用而浪费额度；若人物交互、精确次数、对白或物理负载超过Execution Plan预算，则拆分，不因额度强行合并。
- 30秒结果仍必须作为一个真实Video Take进入逐CUT QC；允许Stage 06按CUT做Sub-cut Salvage，不能因为前半段可用就自动批准整条视频。

## V4.5.10｜Identity Readability / Multimodal / Managed Audio Closure

- 命名或身份关键人物必须在平台有效缩放后可辨。`CRITICAL / SUPPORT`人物的Primary Visual若不可辨或UNKNOWN，触发`IDENTITY_READABILITY_FAIL`：Primary仍可控制构图，但必须Direct Bind精确匹配`subject_entity_id`的人物母图/Current Look，或重生身份可辨的执行帧。原图分辨率与文件MB不能替代平台尺度身份核验。
- 默认视频Reference能力类为`MULTIMODAL_ALL_ROUND_REFERENCE`，但项目执行层只允许文字、图片、音频参考；`REFERENCE_VIDEO_POLICY = FORBIDDEN_QUOTA_COST`。动作与运镜由白描Panel、Action Key Pose、Camera Path Metadata、Previous Ending Frame静帧和详细文字承担。
- `AUDIO_REFERENCE_POLICY = AUDIO_ASSET_MANIFEST_ONLY`：生成阶段使用的音频必须登记到`AUDIO_ASSET_MANIFEST`，拥有稳定Asset ID、Native Token/Binding、Scope、Version、Fingerprint与Approval；每个Video Job仍只绑定当前镜头需要的最小充分音频集合。
- 全能参考不取消Reference Resolver、Identity Readability或Authority边界，也不代表所有资产全部上传。Stage 03资产库可以丰富，Stage 05 Direct Pack仍按当前Provider槽位、字段独占性与风险裁决。

Video Generation Job 的Reference媒体策略现在机械闭环：所有Direct Binding必须来自ASSET_REGISTRY；参考视频硬禁；Audio只能通过AUDIO_ASSET_MANIFEST并满足媒体类型、Authority Role、Scope、Subject、Approval与Native @Token一致性后进入Job。Video Ready还必须通过`VIDEO_REFERENCE_MEDIA_POLICY_PASS + AUDIO_REFERENCE_BINDING_PASS`。


## V4.5.7 Voice Direction Logic Closure

重要Dialogue/VO现在使用结构化`VOICE_DIRECTION_PLAN`控制Trigger / Meaning / Objective / Tactic / Subtext与Performance Loudness / Pace / Pause / Stress / Pitch-Energy / Terminal Intonation；Stage 05生成`VOICE_PROMPT_HANDOFF`并机械验证Prosody确实进入Final Video Prompt，Stage 06基于Picture Lock生成`VOICE_TTS_HANDOFF`，只允许调整真实Timing，不允许静默改变Approved Voice Identity或表演意图。
