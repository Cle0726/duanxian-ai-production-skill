# Prompt Compiler（提示词自动编译器）｜Current Authority

> **用途：** Skill内部把规则与分析分层管理；用户最后收到一整份可直接复制的最终Prompt。当前版本统一执行Semantic Dedup：内部多引擎完整分析，模型侧把Performance / Action Feasibility / Natural Motion / Physics / Crowd / Environment的同一时间事实归并成一个Integrated Shot Timeline。

## Current｜Director Invariant Compile Gate

Stage 05任何FINAL VIDEO PROMPT在模块拼装前必须读取当前`DIRECTOR_INTELLIGENCE_DECISION_CARD + Sequence Arc + Approved Previs Set`，并通过`director_to_ai_execution_boundary.md`提取本Segment适用Invariant。Compiler可以压缩表达，但不能改变Audience Alignment、Reveal顺序、核心Blocking/Distance、POV、Reaction Give-Deny、关键Hold/Cut或Opening/Closing Function。

- 仅Prompt措辞/Reference/Slot变化 → 不重开导演；
- 必须改变Invariant → `DIRECTOR_INVARIANT_EXECUTION_FAIL`，返回Director Judge；
- Judge已妥协但Decision Card/Sequence未更新 → `DIRECTOR_COMPROMISE_PROPAGATION_GAP`，禁止继续编译。



## Current｜Style Authority Projection Compile Gate

Stage 03/04/05正式视觉任务读取`style_authority_projection_gate.md`。已绑定Approved视觉风格证据时，Reference继续作为主要Style Owner，但Stage 05 Final Video仍必须保留当前镜头真正影响生成结果的绘制语言、人物/环境融合、材质与防照片/3D漂移描述；不再限制为“一句防漂移”。没有可用视觉风格证据时使用FULL文字渲染核心。`STYLE_TAG_ONLY_FAIL`只在文字是唯一Style Control且只剩抽象Tag时成立。

## Current｜Final Prompt Egress Hard Gate

Compiler不得把第一次写出的候选Prompt直接交付。最终必须调用`prompt_egress_gate.md`形成`FINAL_COPY_SURFACE`。Generation Prompt中的任务壳、输入清单、文件元数据、内部资产ID、流水线方法名、QC说明或meta-prompt说明都属于出站失败。Style Projection只保留其求解出的直接绘画语言。


## Current｜Constraint-First Compile Gate

Final Video不再采用“多模块各写一段 → 最后去重”的主架构。所有模块先写入`VIDEO_EXECUTION_STATE`；固定顺序：
`Narrative Normalize → Reference Binding Semantic Verify → Typed State Finalize（含Spatial Execution State）→ Prompt Constraint Solver → Shot Proof/Motion Budget → Video Generation Readiness → Generation/QC Separation → Natural-language Compile → Semantic Dedup → Surface Sanitizer → Egress Rewrite → Post-Compile Constraint Closure → Mechanical Surface Lint → FINAL_COPY_SURFACE`。

- Conflict Solver解决互斥；Semantic Dedup只解决重复；二者不可互代。
- `Hard Conflict Count > 0`或`VIDEO_GENERATION_READY != YES`时，不产生正式Final Prompt。
- QC Contract不进入Generation Prompt；不存在模型侧`【成片必须满足】`复读块。
- Existing visual references已承担身份/静态空间/构图时，模型Prompt不重复资产行政说明；但当前Shot需要Seedance理解的人物/服装、Scene空间、Prop状态、构图、Start→Relation→Motion Target→End Landing必须以**足够详细的可执行文字**穿透到模型侧。
- **所有模块只写State，只有Prompt Compiler拥有Final自然语言写权限。** Camera/Style/Audio/Action模块不得在Compiler后“补一句”。
- Final Candidate经过任何自然语言改写后必须由`post_compile_constraint_closure.md`反查；Pre-compile PASS不能替代Final语义闭环。

## 1｜Internal Rules ≠ Model Prompt

以下属于Skill内部生产控制，**不得写进真正复制给视频模型的FINAL VIDEO PROMPT正文**：
- Generation Task Contract、Key Visible Asset Register / Reference Field Coverage Map、Reference Eligibility Audit、Why Now / Most Direct评分；
- “本Scene以后还有谁/下一Beat有什么”这类仅用于Scope防越界、但当前无真实污染路径的信息；
- Adaptive Take Budget / Shot Investment Tier / 生成几次；
- WEB_QC_DEFAULT / LOCAL_SELF_CHECK；
- Approval Gate / WAITING APPROVAL；
- Reference Budget算法与MUST / CONDITIONAL / TEXT-ONLY裁剪过程；
- Executor Input Map、动态QC图号、文件名 / Asset ID / Version / Path等Reference生产元数据；
- Workspace、归档、Candidate Triage、Retry状态；
- “读取某模板/执行某Gate”等给Skill自己的指令。

这些信息默认留在Workspace / Internal Runtime，不打印到普通生成交付；但**Generation Asset Mention不是内部元数据**。读取`adapters/generation/platform_profile.yaml`：Current Project Default Capability=`MULTIMODAL_ALL_ROUND_REFERENCE`，但Project Reference Policy=`NO_REFERENCE_VIDEO + MANAGED_AUDIO_REFERENCE`；若当前Host Prompt Surface=`NAMED_ASSET_MENTION_REQUIRED`，则当前任务真正MUST_BIND / DIRECT_BIND / CONTINUITY_ENTRY等强绑定Approved Asset必须以真实平台原生`@资产`Mention投射到Prompt正文。不得输出本地路径、内部Asset ID或版本链。生成侧Reference表达继续读取`execution_reference_semantics.md`并在交付前运行`model_facing_prompt_surface_sanitizer.md`。正文不得出现Reference职责表、Authority/MUST_BIND/Resolver等流水线说明；但不得把真实@资产Mention当成行政文本删掉。若Native Mention尚未建立，WITHHOLD Prompt并要求先完成Binding。WEB_QC_COPY_PROMPT的动态`@图N`是QC证据编号，与Generation Asset Mention分离。

## 2｜Prompt Modules

视频Prompt**内部编译源**模块（不等于最终模型侧独立章节）：
- `TYPED EXECUTION STATE`｜所有模块先写结构化事实，不直接写Final Prompt；
- `CONSTRAINT SOLVER`｜检查Camera/Audio/Action/Reference/State/Symbolic Negative互斥；
- `RENDER STYLE`｜正向绘制画风；
- `STYLE AUTHORITY PROJECTION`｜把Project Style DNA / Approved Style Evidence压缩成模型仍可执行的风格句群；
- `CINEMATIC SHOT STYLE`｜项目级摄影语法（适用时，不覆盖具体Storyboard）；
- `COLOR`｜Global / Scene / Shot当前最直接综合色与光色；综合色Authority优先视觉绑定，Color Card是否整图直绑由Capability/Risk路由；
- `REFERENCE`｜先经Key Visible Asset Field Coverage + Task-Bound Binding筛选真实图片输入，内部保留Input Mode与精确绑定；模型侧不输出Reference Role表。Current Generation Profile下，凡强绑定Approved Asset都必须输出真实`@资产`Mention + 最短执行句，并把Environment/Identity/Assembly/Color/Continuity控制继续消解进真实执行区块；关键可见资产必须全部有Authority与有效Mention，之后才删除真正冗余图；
- `CONTINUITY`｜实际起始连续性；
- `SPATIAL EXECUTION`｜来自`SPATIAL_EXECUTION_STATE`的动态位置/朝向/相对关系/路径/目标/落点；Reference锁静态，文字锁动态；
- `TIMELINE / CAMERA`｜时间轴与摄影机；
- `PERFORMANCE`｜表演：内部由Actor Objective / Tactic / Listening驱动，模型侧编译为具体Trigger / Visible Behavior / Listener / Subtext；
- `VOICE DIRECTION / PROSODY`｜有重要Dialogue/VO时读取`VOICE_DIRECTION_PLAN`并运行`tools/voice_direction_prompt_compiler.py`得到`VOICE_PROMPT_HANDOFF`；只保留改变表演意义的Performance Loudness / Pace / Pause / Stress / Pitch-Energy / Terminal Intonation及必要Interaction；不把Mix Gain当表演；
- `VISUAL REFERENCE ROUTING`｜读取综合色卡/Style Board/Storyboard的视觉路由结果；Approved视觉控制默认优先Direct/Panel使用；只有当前Capability/Role、已观察失败、已证明槽位或用户要求等Route Evidence才允许改变路线，生成式Applied不得由主观风险触发；
- `ACTION FEASIBILITY`｜内部动作求解层：Limb Occupancy / Support Graph / Preconditions / Minimal Bridge / Exit State；不把分析表原样塞给模型；
- `NATURAL MOTION`｜内部根据Motion Corridor / Kinetic Chain / Overlap / Joint Arc / Velocity / Locomotion / Settle把合法动作自然化；
- `ACTION / PHYSICS`｜只编译已经通过Action Feasibility + Natural Motion求解的接触、受力、惯性与环境反馈；
- `CROWD / AMBIENT LIFE`｜仅镜头存在明显背景群体时启用；内部按Cluster / Motion Field / Attention / Reaction Propagation求解，模型侧只保留2–4条低强度、不同步的背景生命指令；
- `COMBAT CHOREOGRAPHY`｜战斗编排：仅战斗/追逐/高强度行动Segment启用，编译Victory Condition、有效距离、Initiative、Combat Exchange与Counterplay；
- `MUSICAL COMBAT / CINEMATIC IMPACT-VFX`｜Music Identity/共鸣技能/重要接触适用时，把音乐时间语法翻译成Footwork / Weapon Kinetics / Tactical Timing，并编译Contact Point、Force Propagation、Environment Proof、VFX Causality与Aftermath；
- `ENVIRONMENT`｜环境反馈；
- `MOTION GRAMMAR`｜Music Identity转译后的可见动作（适用时）；
- `SOUND CONTENT`｜本段实际需要的对白/环境/拟音/剧情内音乐；
- `GLOBAL LOCKS`｜全局短锁，按规则只注入一次；
- `TASK-SPECIFIC RESTRICTIONS`｜当前Segment独有高风险限制。

最终视频模型侧按`video_prompt_template.md`输出详细执行稿：@资产绑定 / 镜头目标与时长 / 起始状态与必要视觉确认 / 场景空间、构图、景别与摄影机 / 完整分段时间轴 / 动作、表演、视线、肢体占用与物理反馈 / 环境动态 / 光影综合色 / 对白、声音与必要呼吸 / 结尾状态 / 必要限制。各事实仍遵守One Fact → One Owner，可融合进Timeline避免同义复读，但不得把完整控制项压成几百字。Reference Binding List、Reference Responsibilities、Asset ID/Version等始终留在模型正文之外。

## 3｜禁止项三层结构

### Layer A｜Authority Source（内部规则源，不直接整段复制）
- 全局视觉与Negative Style → `project_style_dna.md`；
- Reference Fidelity / Render Quality → `reference_role_fidelity_isolation.md` + `render_quality_authority.md`；
- Stage 05声音边界 → `video_audio_generation_boundary.md`。

### Layer B｜Compiled Direct Execution Clauses（最终模型Prompt，只保留可执行语言）
Compiler只提取当前任务真正需要的**直接可执行版本**，而且**模块名/Lock名不进入Copy Surface**。Stage 05不再以“短版”为目标：
- Visual / Negative执行句：必要时最多1组；
- Render Fidelity执行句：必要时最多1组；
- Audio执行句：需要声音边界时最多1组。

禁止同一Global Lock以“中文解释 + 英文长列表 + 末尾再追加”的方式重复出现。

若某个任务模板本身已经包含该Global Lock的**Compiled输出块**（例如Render Style Board模板里的Negative Style Lock），Compiler视为已经注入，不再从Authority Source追加第二份。

### Layer C｜Task-Specific Restrictions（当前任务专属）
先执行`task_bound_reference_binding.md`的Negative Relevance Gate。具体人物名、地点名、怪物/道具名、未来Beat元素只有存在当前Reference / Control / Continuity / 已证实Failure的真实污染路径时才允许进入；**当前输入里根本不存在的实体不得为了“保险”重新点名排除。**

优先用正向Shot Scope说明“当前画面实际包含什么”。只补本段特有且真实存在污染风险的问题，例如镜像、特定武器结构、攻击路线、指定CUT、Storyboard/Ending Frame中仍残留但当前Shot必须移除的元素。

如果某限制已经被前文正向动作/Reference职责完整解决，不再为了保险重复写。

**禁止示例：** 当前分镜、Reference、Continuity都没有凯登/西莉亚/诺拉，却写“不出现凯登/西莉亚/诺拉”。这属于`NEGATIVE_RELEVANCE_FAIL`，应从模型Prompt删除，只保留内部Shot Scope。

### QC Rule（验收层）
QC可以检查Global Lock有没有执行，但**QC文字不反向复制进模型Prompt**。
“生成规则出现一次 + QC检查一次”属于正常分层，不算重复。

## 4｜Minimum Necessary Change

Failure Diagnosis判断某模块失败时：
1. 锁住其他已正确模块；
2. 只修改故障模块；
3. 重新运行去重检查；
4. Compiler重新拼成一份完整Prompt；
5. 面向用户只交最终可复制版本，不要求用户自己在长Prompt中找位置替换。

例如动作方向错误：STYLE / REFERENCE / CAMERA / SOUND保持不变，只修改ACTION FEASIBILITY（如需要）/ ACTION / PHYSICS和必要的Task-Specific Restriction。若问题是“持伞手又去摸喉咙”，先修肢体占用与Support Bridge，不用整条Prompt重写。

## 5｜Preflight Dedup Check（编译前去重检查）

## 5.0｜Video Duration Compatibility Gate（视频时长兼容闸门）

FINAL VIDEO PROMPT编译前必须确认：
- `Director Target Duration > 0`；
- Director Target与Approved Sequence / Previs一致；
- `SKILL_DURATION_CEILING = NONE`，不得调用旧10s Hard Ceiling；
- 若`Platform Duration Profile = UNDECLARED`，不得虚构Slot / Hard Max；
- 若当前平台能力已可靠提供，Execution Duration Mapping与真实平台能力兼容；
- 不存在Duration Padding / Forced Compression。

不满足时按类型输出`INVALID_DIRECTOR_DURATION / PLATFORM_DURATION_PROFILE_FABRICATION / PLATFORM_DURATION_CONFLICT / PLATFORM_DURATION_SPLIT_REQUIRED / AI_EXECUTION_CONSTRAINT_CONFLICT`，返回Stage 02C/04/Director Judge做最小修正。**不得因为Director Target超过历史10秒范围就自动阻止编译。**

## 5.1｜Runtime Completeness Gate（运行时完整度闸门）

如果当前Prompt由Runtime Capsule / Runtime Core编译，Compiler必须额外确认：
- Capsule Skill Version与当前Skill一致；
- 所需Authority Source没有被修改/失效；
- Target / Reference / Entry / Integrated Timeline / Performance / **Action Feasibility / Limb-Prop Support / Preconditions** / **Natural Motion / Motion Corridor / Kinetic Chain / Overlap** / Action Physics / **Crowd Runtime / Ambient Motion / Attention / Reaction Propagation（适用时）** / Exit均没有因压缩读取而丢失；
- 需要时的Render Fidelity与No-BGM/Audio执行句各最多一次，且只使用直接模型语言；
- 当前任务需要的Music Identity / Voice / Transformation因果已注入；战斗涉及Music Identity/VFX时，Musical Combat Translation与Cinematic Impact/VFX因果没有因Runtime压缩丢失；
- Task-Specific Restrictions来自当前Segment真实污染风险，不是旧段残留；无污染路径的具体实体排除已删除；
- Reference Pack仍满足Key Visible Asset Coverage + Task-Bound Most Direct Authority；当前高清对象输入使用`HD_OBJECT_AUTHORITY_IMAGE`，Assembly使用`HD_SHOT_ASSEMBLY_IMAGE`；Revision任务仍绑定真实Revision Source；
- Final Prompt长度由任务复杂度决定，不由Runtime节省目标决定。

任何一项无法确认：`RUNTIME FALLBACK = FULL AUTHORITY`，回读完整模板后再编译。

## 5.2｜User-Facing Delivery Contract（用户真正拿去生成的表面）

普通Stage 03/04/05生成交付默认格式：

```text
<这里只有最终可复制Prompt正文>
```

代码块外不再重复任务壳、输入映射、输出管理信息、文件路径或资产名。如果用户必须先完成实际Reference Binding，只在代码块外写一句人类操作提示；绑定完成并通过Content/Role核验后重新编译Copy Surface。

**禁止**把“上传清单 + 本地路径 + Prompt”合并成一段让用户再自行删减。

## 6｜目标

让Prompt更像一张真正的导演执行单：内部多引擎推导，模型侧只保留一次最清楚的执行结果。
**规则源可以完整；Final Video Prompt以可控性与执行完整度优先，不以“短”为目标。Semantic Dedup只消除重复和行政噪声，不得把Seedance所需的时间轴、动作、表演、摄影机、物理、声音、光影综合色与Ending State压缩掉。**


## Performance Compilation Rule（表演编译规则）

先读取`actor_performance_engine.md`完成Objective / Obstacle / Tactic / Listening / Adjustment推导，再由Performance Causality生成可见行为。模型侧不得只出现“她害怕 / 他很关心 / 她震惊地看着”等抽象词。Compiler必须把内部演员逻辑编译为当前景别可见的具体表演。

当Performance信息很多时，不通过删除心理信号缩短Prompt：
**合并同因果 → 排序 → 分时 → 景别转译 → 必要时拆Shot/Segment。**

每Beat的1–3项规则指主要Emotional Carrier，不是全部身体动作的硬上限。心理上的`Involuntary Leak + Controlled Response`可以共存。

有对白时，优先保留会改变潜台词理解的回答速度、停顿、视线、原任务动作变化与Listener Reaction。`Sentence End ≠ Recovery`：同一Objective / Tactic / Thought Intention内不逐句编译Recovery。

若`Breath = IMPLICIT`，FINAL VIDEO PROMPT不需要反复点名“呼吸/胸口/肩线稳定”；直接用连续姿态、原任务、语流和动作桥表现自然状态。只有`Breath = VISIBLE_WITH_CAUSE`才具体编译换气。

战斗时Performance与Combat同时编译，不能为了动作清晰把主要人物做成扑克脸。

## Combat Compilation Rule（战斗编译规则）

遇到战斗Segment时，内部读取 `combat_choreography_engine.md` 与本场Combat Design Brief；存在Music Identity/共鸣技能/重要VFX时同时读取 `cinematic_combat_vfx_engine.md`。模型侧只输出当前Segment可观察、可执行的战斗因果。不要把Runtime Combat Profile、Conflict Audit矩阵、Combat Archetype或音乐术语解释整段复制进FINAL VIDEO PROMPT。

Music Identity必须先翻译为可见Timing / Footwork / Weapon Kinetics / Recovery / Tactical Timing；不能仅输出“华彩/对位/切分/渐强”等抽象术语，也不能靠随机音符和换色Glow代替。重要接触优先保留Contact Point / Force Direction / Compression / Force Propagation / Recoil / Environment Proof / Aftermath；VFX优先保留Cause / Source / Spatial Geometry / Environment Interaction / Decay。

复杂战斗优先拆成1个Micro-objective或1–2个Combat Exchange；若MUST动作超过模型可稳定执行范围，应拆Segment，不通过缩写把七八个攻防动作塞进同一Take。


## Current｜Seedance Detailed Prompt Restoration

Stage 05 Final Video在正式编译前必须先按`video_execution_plan.md`生成并冻结结构化`VIDEO EXECUTION PLAN`，通过Reference / Spatial / Body-Prop / Performance Causality / Camera / Timing / Physics-Audio求解后，再生成用户可核对的`VIDEO EXECUTION ANALYSIS`，最后按`video_prompt_template.md`编译详细控制。`SOLVE FIRST → WRITE SECOND`；Plan未PASS不得靠自然语言润色掩盖冲突。

### A. User-visible analysis contract
对用户展示的是可核对的执行结论，不是内部隐藏推理。至少覆盖：镜头目标、起始状态、人物外观/服装必要确认、场景空间、道具状态、构图、景别、摄影机、时间轴、逐段动作、表演、视线、肢体占用、物理反馈、环境动态、光影综合色、声音、对白/呼吸、结尾状态、必要负面限制。

### B. Prompt density contract
- `PROMPT_LENGTH_CEILING = NONE`：正常Seedance Source Master Prompt不设置固定字数区间或最大字符数，长度由执行完整性决定；复杂镜头可以超过历史3000中文字级；
- @图/Storyboard/综合色卡是视觉Authority和稳定锚点，**不能成为删除详细文字控制的理由**；
- 已绑定Reference允许避免无意义的外貌逐毫米复读，但当前Shot执行需要的人物/服装/空间/道具/构图事实必须在正文自然确认；
- 综合色卡已绑定时仍要写当前镜头的光源、明暗、冷暖、主体分离和Shot Lighting变化；
- 任何`Concise Compile / Minimal Style / Reference already shows it`规则都不得覆盖本节；
- 如果平台存在可靠字符上限，先保留完整Master Prompt，再做Target Adapter版本，不允许把适配后的短版反写成Source。

### C. Completeness before dedup
在Semantic Dedup前建立20项Coverage Map。缺少适用项时不得进入Surface Sanitizer。20项是Coverage检查，不是20个独立正文栏目：Compiler必须以Frozen `VIDEO EXECUTION PLAN`的时间因果为主线，把表演、视线、肢体、物理、环境、Camera与声音融合进对应时间窗。Dedup只能合并同义表达，不能以“视觉Reference已承担”为理由删除视频走向控制。

## Local Inpaint Compilation Rule（局部重绘编译规则）

当输出的是图片Local Patch / Inpaint Prompt，而非Final Video Prompt时，Compiler必须读取 `inpaint_local_patch_authority_engine.md`：

- REFERENCE块必须显式区分`EDIT_TARGET`与`PATCH_DESIGN_AUTHORITY`；
- 有明确Patch图时，Executor Input Map必须把真实输入绑定为`EDIT_TARGET / PATCH_DESIGN_REFERENCE`；模型正文写直接修改动作；Current Generation Profile下，EDIT_TARGET / PATCH_DESIGN_REFERENCE等强绑定输入必须保留真实`@资产`Mention + 最短执行句，不写内部文件名/Asset ID/Role表；
- Base Master只负责底图与Frozen Region，不写成“参考它重新设计局部”；
- Patch Authority只负责Mask内新结构，不允许越权控制背景/构图/综合色；
- 输出必须包含`MASK REGION / AUTHORIZED CHANGE / FROZEN REGION / PATCH INTEGRATION`；
- 若没有图片Patch Authority且文字足以唯一执行，明确标记`PATCH_DESIGN_AUTHORITY = TEXT-ONLY`；
- 先按Edit Target Type确定回Stage 03还是Stage 04；`APPROVED_ENDING_FRAME`不得编译成“修完继续当真实尾帧”的Inpaint任务。

Local Patch任务的最终Prompt同样经过Minimum Necessary Change：正确区域不重复描述为“重新生成”，只写冻结。


## Current｜Visual Reference Routing Compile Gate
Final Video Compiler读取`REFERENCE ROUTING MANIFEST`。Color Card、Style Board、Storyboard Sheet不是按类别禁止的输入；它们可以Direct Bind、Dedicated Channel、Panel Split、Key Panel、Clean Crop或Applied Reference。Compiler只要求：当前路线与目标模型能力/项目实测相符，授权字段明确，已知Literalization失败路线没有被重复使用。视觉Reference已经承担的身份/空间/综合色/风格/构图不需要复制资产规格表，但Stage 05仍必须把当前Shot执行所需的人物/服装、空间关系、构图、光色与动作边界自然确认进正文；Reference Routing不得拥有正文裁剪权。


## Current｜Voice Direction Compile Gate
重要Dialogue/VO必须先通过`validators/voice_direction_plan_lint.py`。Final Prompt必须通过`validators/voice_prompt_handoff_lint.py`：每条当前Video Unit所需台词、说话者和编译后的Pace / Pause / Stress / Pitch-Energy / Terminal等自然语言锚点都必须真实出现。只有“悲伤/紧张/低沉”等抽象词仍标`VOICE_PROSODY_UNDERDIRECTED`。Voice Identity来自Approved Voice Master；当前Prosody只能做状态偏移。


## Current｜Model-Facing Surface Sanitization Gate

Semantic Dedup结束后、向用户交付可复制Prompt之前，必须运行`model_facing_prompt_surface_sanitizer.md`。

硬要求：
- Compiler先执行**正向Allowlist Extraction**，不是只靠Negative删除；
- Copy Surface中`Reference Responsibilities / Reuse Scan / MUST_BIND / Executor Input Map`等行政块计数 = 0；
- Copy Surface中内部Asset ID / 文件名 / Version / Path / 文件后缀计数 = 0；
- Copy Surface中`TASK_SHELL / INPUT_MAPPING / OUTPUT_ADMIN_SHELL`等操作者任务壳计数 = 0；
- `Authority / Resolver / Registry / Stage / Gate / Capsule / Method`等仅有流水线意义的词计数 = 0；
- Current Generation Profile要求强绑定资产显式@Mention：所有`emit_on_prompt=true`的Reference Binding都必须有可验证`native_token`并出现在Copy Surface；Token后不得出现内部Asset ID、版本、Path或职责长解释；
- Stage 05任何原生Video Token在发出前都已通过Reference Capability/Role Routing；Color Card/Style Board/Storyboard可在Route=Direct时合法Token化；
- 必须产生`SURFACE_LINT_REPORT`，所有Forbidden Counter = 0；没有Lint报告视为未净化；
- 普通用户交付默认只给**一个Prompt代码块**。Internal/Executor Packet不打印；若绑定尚未完成而必须人工操作，只在代码块外给最短绑定提示。

失败：`LOCAL_PATH_LEAK / FILE_NAME_LEAK / TASK_SHELL_LEAK / MODEL_FACING_METADATA_LEAK / REFERENCE_ADMIN_TEXT_LEAK / PIPELINE_JARGON_LEAK / NATIVE_TOKEN_OVERANNOTATION / PSEUDO_NATIVE_REFERENCE_TOKEN / UNROUTED_CONTROL_REFERENCE_TOKEN / MODEL_FACING_ALLOWLIST_VIOLATION / SURFACE_LINT_NOT_RUN / PROMPT_SURFACE_SANITIZATION_FAIL`。


## Current｜Post-Compile Semantic Closure
`Surface Sanitizer / Egress Rewrite`结束后，Compiler必须把真正准备交付的Candidate反向解析为Canonical Claim Map，并运行`post_compile_constraint_closure.md`；有脚本能力时再运行`validators/post_compile_constraint_lint.py`。任何`NEW_CONSTRAINT / MISSING_REQUIRED_MODEL_TEXT / STATE_CONTRADICTION / AMBIGUOUS_EXCLUSIVE / MULTI_OWNER`非0：丢弃Candidate，回Resolved State Fresh Compile。**禁止在冲突Prompt末尾追加“修正：……”**。

## Current｜Combat Final Prompt Conditional Closure

当`conditional_source.combat`被加载、Director将当前Video Unit判定为真实战斗/追逐近身冲突，或Resolved Execution State标记`SEGMENT_TYPE=COMBAT`时，Final Video Prompt在20项通用Coverage Map之外，必须额外通过Combat Coverage Map：

`Combat Objective → Engagement Distance → Read/Decision → Attack/Defense Exchange → Attack/Escape Lane → Contact/Near Miss → Force Direction → Recoil/Recovery → Initiative Shift → Combat Camera Read → Exit Combat State`

- Combat Engine仍是战斗语法Authority；Prompt Compiler只把**当前Segment真正看得见、必须执行**的部分投影进Seedance正文；
- Semantic Dedup不得删除距离变化、攻防因果、接触点、受力方向、Recovery、主动权变化或Combat Camera Read；
- 若Combat Coverage无法在当前时长/镜头Proof Budget中清晰表达，返回Segment Planner拆分Combat Exchange，禁止用抽象短句替代；
- `video_prompt_detail_lint.py`对Combat Segment启用附加机械检查；普通对白/环境镜头不触发Combat字段要求。

## Current｜Visual Salience & Style Escalation Policy

### Visual Salience Compile Rule
Stage 05可以保留完整执行信息，但必须把`VISUAL_SALIENCE_BUDGET`编译成注意力层级：Primary必须最清楚；Secondary只提供必要支持；Ambient保持可读但不竞争；Suppressed允许退入遮挡、暗部、失焦或普通区域。

不得因为Prompt长、Reference多、Runtime字段完整，就要求“所有东西都清楚、漂亮、重要”。**Execution Density ≠ Visual Salience Density**：详细执行约束与视觉显著性是两条不同维度。

### Style Escalation Policy
当用户反馈“不够电影 / 不够《断弦之歌》 / 导演感弱”时，禁止默认做`adjective amplification`：不要只增加“cinematic / melancholic / dramatic / auteur / 高级 / 诗意”等形容词。

先定位真正缺失的Owner，并只加强一个可执行机制：
- Camera Ethics / Viewer Position；
- Blocking / Distance / Spatial Pressure；
- Attention Flow；
- Performance Access；
- Information Withhold / Reveal；
- Editorial Hold / Cut；
- Color Authority或Music Identity（确有缺失时）。

若只是增加风格形容词而没有任何Authority机制改变，视为`STYLE_ESCALATION_ADJECTIVE_ONLY`，重新编译，不覆盖已锁Director Invariants。

## V4.5.7｜Anonymous Slot Decompile（新增）

Final Video Prompt编译前必须执行：
`Storyboard Slot → Entity Binding → Spatial/Action State → Reference Resolution → Natural-language Prompt`。

禁止把`H_A / H_B / P_A / E_A`复制给模型。编译结果必须使用真实实体标签；若该实体被解析为Direct Reference，则使用真实Native `@资产`Token，并紧邻其站位/朝向/动作描述。若实体已被Primary Visual烘焙，不强行重复@，但仍必须在Prompt中明确它的Blocking/Action，防止模型把匿名白描姿态理解错。



## Current｜Prompt Length / Long Video Quota Separation
- `PROMPT_LENGTH_CEILING = NONE`：Source Master Prompt没有Skill级字符上限；
- `duration_sec > 15`不限制Prompt编译长度，但在真实Video Generation Job之前必须通过`LONG_VIDEO_QUOTA_CONFIRMATION_PASS`；
- 未经用户明确确认，不得把>15s计划标记为可生成；不得用自动拆短绕过用户额度确认。
