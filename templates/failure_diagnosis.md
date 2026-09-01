# Failure Diagnosis（失败诊断与最小修改）

> **用途：** 分镜或视频生成失败后，不要条件反射地整条Prompt重写。先判断“真正错在哪里”，保留已经正确的部分，只修故障源。

## 核心原则：Minimum Necessary Change（最小必要修改）

先回答三个问题：

1. 哪些部分已经正确？
2. 真正失败的类别是什么？
3. 最小需要修改的是上游哪一层？

没有证据说明有问题的内容，不要顺手重写。

## Failure Type（失败类型）

### Shot Assembly Gap｜镜头组装资产缺口
症状：人物/场景/道具各自都正确，但Storyboard或Video里多人站位、人景关系、道具所属、功能空间位置反复错误。

优先检查`shot_assembly_asset_layer.md` + `reference_field_coverage_map.md`：
- 如果问题是Stage 03本应有的人景物组装关系缺失 → `SHOT_ASSEMBLY_GAP`，Break Freeze回Stage 03补Assembly；
- 如果Assembly改变了已有角色身份/场景地理/道具Canon、把Scoped Cast带出授权范围，或实际上是从Storyboard宫格清稿 → `SHOT_ASSEMBLY_AUTHORITY_FAIL`，回Stage 03重建正确Assembly；
- 如果问题只有Approved Storyboard后才能唯一确定 → Stage 04 `VIDEO_CONDITIONING_KEYFRAME`；
- 不把这类问题误判为“再多@几个泛化Master”或直接多Video Take。


### `ASSET LIBRARY UNDERBUILD`｜资产库欠建 / 把执行精简误当资产精简
症状：Stage 03仍有本集真实Requirement未建立、未批准或未冻结，却因为Stage 05要`MINIMUM_SUFFICIENT_REFERENCE_SET`而提前删掉人物、空场景、Performance Support或Narrative FX Authority；或者把“单镜少@图”错误理解成“资产库也少做图”。

优先检查：`asset_library_completeness_policy.md` → `visual_asset_obligation` → `PERFORMANCE_ASSET_REQUIREMENT_SET` → `NARRATIVE_FX_ASSET_MANIFEST` → Episode Asset Freeze。

路由：`ASSET_LIBRARY_UNDERBUILD / ASSET_LIBRARY_STAGE03_OBLIGATIONS_UNRESOLVED`回`EPISODE_ASSET_BUILD`补齐真实Stage 03 Authority，再Refreeze。**不要通过给Stage 05增加临时文字或让视频模型现场发明来绕过。**

核心区分：`RICH CANON LIBRARY ≠ LARGE VIDEO REFERENCE PACK`。Stage 03按真实需求做足；Stage 05才按当前Shot风险选最小充分Direct Pack。

### `PERFORMANCE SUPPORT GAP`｜表演静态支持资产缺口
症状：人物身份母图正确、白描Blocking也正确，但镜头中的特殊微表情、复杂姿态、接触姿势或身体重心是当前Video高风险点，Stage 02已判定需要静态Support，却没有对应Approved Performance Support；或者Multi-panel动作页被直接当作Video唯一视觉Reference。

优先检查：`performance_asset_requirement_engine.md` → `PERFORMANCE_ASSET_REQUIREMENT_SET` → `production_support_reference_engine.md` → `reference_resolver.md`。

路由：`PERFORMANCE_SUPPORT_GAP / PERFORMANCE_SUPPORT_REQUIRED_MISSING`回`PERFORMANCE_SUPPORT_ASSET`。只补当前Required的`EXPRESSION / ACTION_POSE / CONTACT_POSE`；不机械给每个配角生成固定六表情/六动作。Multi-panel Support只用于Canon/选择，进入Video时应选单帧或烘焙进Shot Execution Frame。

Authority边界：Performance Support不拥有人物Identity、服装Canon、场景Geography、Camera或Timing；白描仍拥有Blocking/动作阶段，人物母图仍拥有Identity。

### `NARRATIVE FX ASSET GAP`｜剧情型视觉现象资产缺口
症状：失声、异常灯光、悬停血滴、共鸣异常等具有Signature、重复出现或跨镜连续性的视觉现象只剩一句Prompt文字，导致每镜形态、综合色、阶段或与环境的交互随机变化；或者FX State Sheet被整张直接@进Video导致宫格/多状态Literalization。

优先检查：`narrative_fx_asset_standard.md` → `NARRATIVE_FX_ASSET_MANIFEST` → `reference_resolver.md`。

路由：`NARRATIVE_FX_ASSET_GAP / NARRATIVE_FX_REFERENCE_REQUIRED / NARRATIVE_FX_STATE_COVERAGE_GAP`回`NARRATIVE_FX_ASSET`补静态Canon和必要状态覆盖。简单一次性低风险FX允许`TEXT_GRAMMAR_ONLY`；Signature / Continuity / High-risk FX必须建立`NARRATIVE_FX_REFERENCE`。State Sheet默认不直接进入Video，使用当前单状态图或Shot Execution Frame。

Reference Video仍禁止；Narrative FX的动态Timing、Camera和运动路径由Storyboard / Execution Plan / Prompt控制。

### `DIRECTOR / STAGING`｜导演空间 / 摄影推进失败
症状：人物站位像展示图；多人同深度、相似大小、均匀间距；对话只靠正反打；角色关系变化但距离/Blocking不变；轴线/视线翻转；整场景别没有推进；CUT没有信息或动作动机；Montage像PPT；Transformation设计很强但导演仍用普通安全全身景别展示。

优先检查：
`director_architecture_engine.md` → `cinematic_spatial_staging_engine.md` → Stage 02 Detailed Shot Contract → `director_spatial_reconciliation_gate.md` → Approved Storyboard。

路由：
- Stage 02本来就没锁Distance / Depth / Axis / Focus / Cut → 回Stage 02最小Director Patch；
- Stage 02锁了但Stage 04擅自压平 → `DIRECTOR_INHERITANCE_FAIL`，只重做受影响Storyboard；
- 真实Environment使原Camera/Blocking不可能 → `DIRECTOR SPATIAL PATCH REQUIRED`，回Reconciliation；
- 缺Coverage/Assembly才是资产问题，不要用多Video Take解决。

常见状态：`STAGING_DISTANCE_FLAT_FAIL / VISUAL_HIERARCHY_FLAT_FAIL / SCREEN_DIRECTION_FAIL / EYELINE_CONTINUITY_FAIL / SHOT_PROGRESSION_FLAT_FAIL / CUT_MOTIVATION_WEAK / MECHANICAL_SHOT_REVERSE_LOOP / MONTAGE_PPT_FAIL / DIRECTOR SHOT CONTRACT CONFLICT`。

### `COMBAT FRAMING / DISTANCE`｜战斗摄影 / 距离失败
症状：所有参战者完整全身排开；敌我长期停在安全中远距离；Weapon Reach与画面距离不匹配；主动权变化但构图不变；关键Contact看不清。

优先检查：Stage 02 `Engagement Distance Ladder / Spatial Dominance / Attack Lane / Depth Strategy / Contact Read / Initiative Shift Visual` → `combat_choreography_engine.md` → `cinematic_combat_vfx_engine.md`。

常见状态：`COMBAT_LINEUP_FAIL / COMBAT_DISTANCE_FLAT / INITIATIVE_VISUAL_FLAT / CAMERA_OBSCURES_ACTION`。

### `TRANSFORMATION INJURY RECOVERY`｜变身伤口修复失败
症状：完整变身完成后仍机械继承变身前可恢复开放伤口/活动性出血/旧伤限制；或解除变身后把已修复伤口重新刷回；或反过来把永久疤痕、不可逆损伤、死亡、独立Fatigue/Lore Cost也一起无条件清空。

优先检查：`world_state_continuity_engine.md` → `transformation_asset_standard.md` → 当前Pre-Transformation Injury Snapshot / Recovery Eligibility / Post-Recovery Injury State → Storyboard / Video Prompt。

路由：
- ELIGIBLE伤口仍被继承 → `TRANSFORMATION_INJURY_RECOVERY_FAIL`；回Stage 02更新World State Delta，并重编Stage 04/05伤势锁；
- 解除变身后旧伤复现 → `POST_TRANSFORMATION_INJURY_ROLLBACK_FAIL`；禁止引用Pre-Recovery Injury Ref；
- 把不可修复/永久状态一并抹掉 → `TRANSFORMATION_RECOVERY_OVERREACH_FAIL`；恢复最新Canon限制，不允许“万能治疗”。

### `TRANSFORMATION SPLENDOR / PRESENTATION`｜变身华丽度 / 展示失败
症状：变身只是普通服装更复杂；默认收敛为暗黑哥特/黑酒红旧金；没有一句Costume Thesis；Hero Decisions不清楚；Flat Color后设计崩塌；身体线条/综合色/材质因“高级克制”被无理由压平；或Stage 03设计合格但导演没有给Silhouette / Eye / Material / Weapon真正展示机会。

优先检查：`transformation_splendor_architecture.md` → `transformation_beauty_core_five.md` → `transformation_asset_standard.md` → Stage 02 Transformation Presentation Contract → Storyboard。

常见状态：`TRANSFORMATION_COSTUME_GENERIC_FAIL / STYLE_FAMILY_DEFAULT_COLLAPSE / TRANSFORMATION_SPLENDOR_FLAT_FAIL / SPLENDOR_LARGE_SCALE_MISSING / COSTUME_GRAPHIC_STRUCTURE_FAIL / SPLENDOR_MATERIAL_FLAT / SPLENDOR_DETAIL_NO_HIERARCHY / TRANSFORMATION_BOLDNESS_SUPPRESSED_FAIL / TRANSFORMATION_PRESENTATION_FLAT_FAIL`。

### `CHARACTER DESIGN TEMPLATE COLLISION`｜人物脸 / 眼 / 发 / 服装模板碰撞
症状：不同角色生成出来像同一个人；女性/男性分别共享同一标准脸；刘海、长发轮廓和后发结构高度重复；可变身角色只是在同款瞳孔/眼影上换颜色；服装只换综合色但廓形、领口、腰线、层次和鞋靴仍像同一品牌Lookbook。

优先检查：
`character_identity_differentiation_engine.md` → `face_identity_matrix.md` → `hair_identity_architecture.md` → `eye_signature_ledger.md` → `wardrobe_diversity_design_matrix.md`。

路由：
- Face结构撞型 → Stage 03重做Face Identity Card / 最小Character Master修订；
- Hair撞型 → 重做Hair ID / HA-01，不要只换发色或发饰；
- Eye撞型 → 先区分Base Eye Identity，再重做Transformation Eye Signature；
- Wardrobe撞型 → 保留时代/世界，比较整体Styling Signature；优先调整真正重合的比例/层次/材质/穿法，不按固定字段数量凑差异，也不要只换颜色；
- Wardrobe Styling Lazy → 允许复用Closet旧单品；重新建立比例/开合/内外层关系/材质/综合色/Body Presentation逻辑，不要因为“加了大衣”本身返工；
- 已有APPROVED旧角色不因新版规则自动改脸；优先让新角色避开，除非用户批准正式修订。

常见状态：`CHARACTER_TEMPLATE_COLLISION_FAIL / FACE TEMPLATE COLLISION / HAIR TEMPLATE COLLISION / EYE SIGNATURE COLLISION / WARDROBE TEMPLATE COLLISION / WARDROBE STYLING LAZY / EYE IDENTITY READABILITY FAIL`。



### `PERSONAL ADORNMENT FAILURE`｜个人装饰层失败
症状：主要角色全员什么也不戴；或者反过来所有人都戴相似细耳环/项链/手表；装饰与人物身份无关；Signature Adornment在四视图/分镜/视频中无因消失、换边或变形。

优先检查：`personal_adornment_identity_system.md` → `wardrobe_style_design_engine.md` → `wardrobe_diversity_design_matrix.md` → `character_closet_registry.md`。

路由：
- 全员空白 → 重做Adornment Opportunity Review，不机械给每人加同类首饰；
- 模板化 → 改类别 / Placement / Scale / Material / Wear Habit，而不是只换颜色；
- 过度装饰 → 回到1 Primary + 0–1 Secondary的主次关系；
- 连续性漂移 → 锁当前Character Master / AD-01并检查Reference Coverage。

常见状态：`ADORNMENT IDENTITY WEAK / ADORNMENT TEMPLATE COLLISION / ADORNMENT OVERDESIGN FAIL / ADORNMENT CONTINUITY FAIL / ADORNMENT BLANK CAST FAIL`。

### `MUSICAL EYE MOTIF FAILURE`｜音乐图形化眼部失败
症状：变身眼部只是普通彩妆；音乐性只能靠颜色/外部饰品理解；所有人都是“眼尾一个音符”；或相反，字段太多导致虹膜、眼线、眼影、眼下纹样全部抢焦点，无法说出一个Primary Eye Signature。

优先检查：
`musical_eye_motif_system.md` → `musical_eye_motif_registry.md` → `eye_signature_ledger.md` → `transformation_beauty_core_five.md` → `transformation_asset_standard.md`。

路由：
- 先找回`Primary Eye Signature`，删掉互相抢权重的小细节；
- MAIN/CORE再建立`Secondary Graphic`，Periocular只保留0–1个Accent；
- 再检查Musical Origin Trace是否与礼服、头发、武器共享同一Music Identity；
- 标准Notation太幼稚时，优先转成DERIVED_MUSICAL_GLYPH或MUSICAL_GEOMETRY，而不是继续贴符号；
- 若只是换颜色 / 贴音符，则重做Graphic Architecture，而不是继续调色。

常见状态：`MUSICAL EYE SOURCE LOST / EYE SIGNATURE COLLISION / MUSICAL EYE REGISTRY COLLISION / MUSICAL EYE READABILITY FAIL / MUSICAL EYE STICKER FAIL / EYE_SIGNATURE_OVERDESIGN_FAIL / MUSICAL EYE ABSENCE FAIL / MUSICAL EYE CANON DRIFT`。


### `ADORNMENT / CHARACTER LOCK FAILURE`｜个人装饰或人物身份锁缺口
症状：近景耳饰/戒指/胸针反复换边换形；ROTATING配饰随机变化；人物有DV-01但3/4脸/后发仍漂；Storyboard/Video要求清楚看装饰却没有直接Detail Authority。

优先检查：`character_asset_requirement_set.md` → `personal_adornment_identity_system.md` → `character_asset_standard.md` → `reference_field_coverage_map.md`。

路由：
- 缺DV-01 / DF-02 / HA-01等Required身份锁 → `CHARACTER_IDENTITY_LOCK_GAP`，Break Freeze只补缺口；
- Personal Adornment=Critical、Current Look不足且缺AD-01 → `ADORNMENT_ASSET_GAP`；
- ROTATING跨Scene随机换件 → `ADORNMENT_ROTATION_STATE_FAIL`，修Current Active / LOOK Binding；
- 变身时无因消失/恢复错误 → `ADORNMENT_TRANSFORMATION_STATE_FAIL`，回World State / Transformation Rule，不靠Video重抽。

### `IDENTITY DRIFT`｜人物身份漂移
症状：换脸、年龄变化、发型身份变化、人物不像正式母图。
优先检查：Reference Pack、人物母图职责、参考图冲突。

### `STYLE DRIFT`｜画风漂移
症状：真人化、3D化、AAA游戏感、线稿消失、皮肤出现毛孔/摄影感、头发变成塑料或照片级毛发、场景变成写实概念图、人物与背景不同绘画体系。
优先检查：`project_style_dna.md` → `visual_style_authority_engine.md` → Render Style Reference → Reference Pack中是否混入错误风格图 → Threat Layer是否反向污染主画风。

### `VISUAL STYLE AUTHORITY`｜视觉风格职责冲突
症状：Cinematic Shot Style把当前Storyboard机位改掉；Render Style Board中的人物身份/服装被复制到别的角色；Style Board比例污染Character Master；成熟Approved Evidence明明足够却重新抽匿名Style Board导致画风漂移。
优先检查：`visual_style_authority_engine.md` + `reference_resolver.md`。先区分Render Style Grammar / Cinematic Shot Grammar / Shot-Specific Composition，再执行最小Reference Pack。

### `COLOR DERIVATION / VALUE MUD`｜综合色派生 / 明度灰糊失败
症状：所有新地点都被强行套成夜雨蓝灰；雪原/白昼/医院/暖室内没有自己的环境综合色；人物肤色被环境色吞掉；把“low contrast”执行成全画面灰雾；Global / Scene / Shot三层色卡同时上传互相打架；临时雷光/火光被误当永久场景综合色。
优先检查：`color_script_derivation_engine.md` → 当前Global Color DNA → Scene Color Extension → Shot Lighting Variant → Reference Resolver。综合色应是`rich but restrained + controlled chroma concentration + selective saturation + controlled contrast + preserved value hierarchy`；若画面被统一压灰、暖灯/皮革/肤色失去综合色存在感，优先检查是否残留全局`low-saturation / desaturated`硬锁。

### `SPACE DRIFT`｜空间漂移
症状：门窗/座位/舞台方向变化、车内镜像、人物空间关系不成立。
优先检查：Environment Master、轴线、上一段尾帧、分镜空间设计。

### `PROP DRIFT`｜道具漂移
症状：道具消失、变形、尺寸变化、左右结构反转、武器换形。
优先检查：Prop Master、Human Scale、当前状态、接触动作。

### `WORLD STATE / TRANSITION GAP`｜世界状态 / 过渡断裂
症状：上一段仍在行驶/奔跑，下一段已无因抵达；人物凭空进入/离开；关键道具无来源换手/出现/消失；Ongoing Task换镜清零；伤势/湿度/环境破坏/Knowledge/关系状态因换Scene重置。**注意：Transformation Completion触发的合法伤口修复不是World Reset；反过来，Recovery后旧伤重新出现才是连续性错误。**
优先检查：`world_state_continuity_engine.md`中的Exit State → Required Entry State → State Diff → Transition Classification。若是Stage 02遗漏，回Stage 02补Minimum Necessary Transition Beat并更新Asset Manifest / Segment Plan；不要只在Stage 05加一句“保持连续”硬补。

### `PERFORMANCE`｜表演失败
症状：人物木、反应过大/过小、心理过程没出来、眼睛/眨眼/眉眼不自然、情绪直接顶格、听者冻结、第三人像站岗、多人同时同级反应。
优先检查：`actor_performance_engine.md` → `performance_causality_emotional_acting.md` → Stage 04表演设计 → Stage 05 Performance Path。先判断是否Objective/Tactic/Listening就不清楚，再判断微动作执行。

### `CROWD PRESENCE / AMBIENT LIFE`｜群体存在感 / 环境生命失败
症状：两个前景人物对白时背景整片冻结成截图；多人同步转头/同步喝杯/同步起步；所有群众无因盯住主角；人群Density/Flow在CUT后重置；巨响后全体零延迟同步反应；背景人物明显同脸同Pose复制；或为了“活着”让背景持续大动作抢戏。
优先检查：`crowd_presence_ambient_life_engine.md` → World State Crowd Runtime → Stage 04 Crowd Motion Intent → Stage 05 Ambient Motion Contract / Attention / Reaction Propagation。第三个明确个体仍按Actor Performance处理，不把单人问题误诊成Crowd。

常见子类：`CROWD_FREEZE / CROWD_SYNC / CROWD_ATTENTION_HIJACK / CROWD_FLOW_RESET / CROWD_REACTION_PREMATURE / CROWD_REACTION_BROADCAST / CROWD_CLONE_ARTIFACT / CROWD_OVERDIRECTED`。

### `DIRECTOR INTELLIGENCE / GENERIC COVERAGE`｜导演智能 / 泛化覆盖失败
症状：场景虽然轴线/资产/镜头都“正确”，但拍法像模板；每句一切、自动正反打、情绪自动慢推、Reaction过量；或现有资产/模型限制提前决定了POV和构图；多个导演Option只是换景别。

优先检查：`director_intelligence_core.md` → `directorial_department_critique.md` → `sequence_arc_engine.md` → `director_to_ai_execution_boundary.md`。

- Thesis抽象 / Audience State没解 → 回Stage 02 Director Intelligence；
- Option Collapse / Judge未完成 → 重新做候选与Director Judge；
- Option理由被资产/模型/Slot/成本提前污染 → `DIRECTOR_PREMATURE_PRODUCTION_CONTEXT_FAIL`，清除生产上下文后重跑候选；
- 实质SYNTHESIS未经过受影响部门Targeted Re-Critique → `DIRECTOR_SYNTHESIS_UNREVIEWED`，补复核后再锁Judge；
- Sequence平 / Reaction冗余 / Cut机械 → 重建Sequence Arc，不先改Prompt；
- AI/平台/资产约束反向改导演 → 标`AI_CONSTRAINT_BACKDRIVE_FAIL`，恢复Director Invariants；确实无法执行则返回Director Judge做显式妥协；
- Stage 03真实Geography迫使Invariant改变 → `DIRECTOR_INVARIANT_SPATIAL_CONFLICT`，不能由Spatial Reconciliation直接Patch；
- Stage 04/05参数看似正确但Audience Alignment / Reveal / Reaction / Key Hold-Cut漂移 → `DIRECTOR_INVARIANT_EXECUTION_FAIL`；
- Judge已妥协却未同步Decision Card / Sequence / Architecture → `DIRECTOR_COMPROMISE_PROPAGATION_GAP`。

### `ACTION FEASIBILITY / PROP-LIMB CONTINUITY`｜动作可行性 / 肢体-道具连续性失败
症状：持伞/持杯/持武器的手突然去做别的动作导致道具悬空；同一只手同时承担互斥任务；道具无过程换手；双手新动作让原持物凭空消失；接触无Approach/Reach；承重脚直接抬起而无重心转移；扶人/抱持负载无因中断；Ongoing Task因新表演动作自动清零；动作结束后手/Prop/姿态状态不明确。
优先检查：`action_feasibility_prop_limb_continuity_engine.md` → Stage 02 Director Contract → Stage 04 Micro-Blocking / Action State Table → Stage 05正向动作链。若缺合法Body Resource / Support Graph / Preconditions解：局部动作桥能解决则回Stage 04；需要改变核心Distance / Axis / Blocking则回Stage 02最小Patch。若合法解已明确但模型偶发违反，再按随机/执行失败处理。

常见子类：`LIMB_OCCUPANCY_CONFLICT / PROP_SUPPORT_LOSS / PROP_TRANSFER_GAP / CONTACT_PRECONDITION_MISSING / SUPPORT_BALANCE_CONFLICT / SIMULTANEOUS_ACTION_CONFLICT / ONGOING_TASK_DROP / ACTION_EXIT_STATE_GAP / INTER_CHARACTER_LOAD_CONFLICT / GEOMETRY_REACH_CONFLICT`。

### `NATURAL MOTION / KINEMATIC PERFORMANCE`｜自然动作 / 身体运动表演失败
症状：动作逻辑合法但像机器人；Pose A直接插值到Pose B；转头只转脖子、大转身脚底滑转；走路突然全身停死再抬手；动作全部串行“做完一个再做一个”；手臂沿不自然直线滑动；起坐/停步缺少准备与重心过程；动作幅度过大；主体停止时所有衣物/道具同帧冻结。
优先检查：`natural_motion_kinematic_performance_engine.md` → Stage 04 Motion Corridor → Stage 05 Integrated Timeline。先看Functional Preparation / Kinetic Chain / Overlap / Motion Arc / Velocity / Locomotion / Minimum Sufficient Motion / Residual Motion，而不是继续追加“动作自然流畅”这类空词。

常见子类：`POSE_INTERPOLATION / ROBOTIC_SEQUENCING / KINETIC_CHAIN_BREAK / JOINT_PATH_SLIDE / FOOT_PIVOT_SLIDE / PREPARATION_MISSING / VELOCITY_GENERIC / MOTION_OVERAMPLIFIED / RESIDUAL_MOTION_MISSING`。

### `PROMPT REDUNDANCY`｜提示词语义重复
症状：同一动作/状态/限制在Entry、Timeline、Performance、Action、Restrictions多次出现；正向已经写清又追加同义Negative；Reference职责反复解释；Revision把旧Prompt+补丁层层叠加。
优先检查：`prompt_semantic_deduplication_engine.md` + `prompt_compiler.md`。重新执行Fact Ownership与Semantic Canonicalization，把时间变化统一归Integrated Timeline，不通过继续删关键词或追加“再次强调”解决。

常见子类：`EXACT_DUPLICATE / SEMANTIC_DUPLICATE / CROSS_MODULE_DUPLICATE / NEGATION_MIRROR_DUPLICATE / TIMELINE_SHADOW_DUPLICATE / REFERENCE_ROLE_ECHO / LOCK_ECHO`。

### `ACTION / PHYSICS`｜动作/物理失败
症状：在动作可行性已经成立后，仍出现倒向错误、重心不合理、接触顺序错、惯性/受力不自然；战斗中还包括距离跳跃、轮流出招、主动权无因果、武器接触漂浮、打击无重量、技能只会对波、多人排队攻击、相机遮挡关键接触。
优先检查：动作路径、启动部位、重心、速度、接触点；战斗Segment同时读取 `combat_choreography_engine.md`；涉及重要Impact/VFX时加`cinematic_combat_vfx_engine.md`，检查Measure / Initiative / Combat Exchange / Contact Point / Force Direction / Impact / Counterplay / Exit。

战斗子类：`RANGE_JUMP / INITIATIVE_BREAK / TURN_BASED_LOOP / CONTACT_FLOAT / IMPACT_WEAK / TENSION_FLAT / SKILL_CLASH_GENERIC / COST_INVISIBLE / MULTI_FIGHT_QUEUE / CAMERA_OBSCURES_ACTION / DISSOLUTION_MISMATCH`。

### `CAMERA`｜摄影机失败
症状：错误推拉、乱转、越轴、构图没按Storyboard走；把Dolly误成Zoom、Pan误成Truck、Tilt误成Crane。
优先检查顺序：Stage 02 Camera Intent / Axis → Approved Storyboard → Stage 05 Camera指令。若导演Camera Intent本身未锁或与真实空间冲突，回Stage 02/Reconciliation；若Storyboard正确但物理运动歧义，读取 `camera_motion_contract.md`补Path、Axis、Perspective/Parallax与Landing。

### `CUT / TIMING / DURATION`｜切镜 / 时间 / 生成时长失败
症状：CUT没执行、切错时间、把连续Shot自动切开、节奏拖沓；或已知平台Duration Profile与实际映射冲突、凭空编造Slot/Hard Max、为了凑满平台时长出现Dead Hold、为了适配平台上限导致对白/表演/动作异常加速。
优先检查：`video_generation_duration_authority.md`、Segment Plan、Director Target Duration、Platform Duration Profile、时间轴、CUT / Match Cut指令。Skill不按固定秒数拆分；只有当前真实平台Hard Max要求时才在自然边界拆Segment，不在Stage 05硬压。

### `VIDEO RISK STATIC REFERENCE GAP`｜昂贵Video前仍有可静态消除的歧义
症状：当前Shot/Segment的Canon本身并没有错，但昂贵Video仍被要求从多个分散Master、低清Storyboard或文字自行猜复杂接触、操作关系、一次性攻击形态、关键局部或最终Shot组合；或者Stage 02已经识别Static-Solvable高风险，却没有建立任何直接高清证据。
优先检查：`production_support_reference_engine.md` → Stage 02 Video Risk-Driven Static Reference Matrix → Owner路由。对象/空间结构未定义回Canon/Coverage；跨镜持续状态回Persistent State Variant；Canon已定但复杂Interaction / Contact / Transient State需要高清证据则Stage 03补Production Support Reference；只有依赖Approved Storyboard精确构图/Blocking时才Stage 04补Additional Video Conditioning Keyframe。

**禁止误诊：** 速度、步态、动作叠接、Crowd时序、Camera Motion、对白/微表情Timing等`Static-Solvable = NO`的问题不能靠继续出静态图解决。

常见状态：`VIDEO_RISK_REFERENCE_GAP / SUPPORT_REFERENCE_AUTHORITY_FAIL`。

### `REFERENCE OVERLOAD`｜参考图过载
症状：模型同时混合多套脸/服装/场景/风格，结果不稳定。
优先检查：Reference Resolver，删掉无职责参考图。

### `FOREGROUND FIGURE / ASSET ANATOMY`｜前景人物/资产解剖失败
症状：前景主脸/情绪脸五官错位或融化；前景手多指/少指/粘连/腕部断裂；摸喉、持伞、抓握、扶持等关键接触悬空/穿模/融合；整体氛围正确但局部一眼错误。
优先检查：`foreground_figure_integrity_gate.md` → `asset_anatomy_integrity_gate.md` → 当前Candidate / Backup。`HERO_FACE / HERO_HAND / FUNCTION_HAND / 关键叙事Contact`明显错误按Asset QC P0，不得因整体好看放行。
处理：若Backup已规避同类问题先切Backup；否则当前图大部分正确时`LOCAL_PATCH`，失败Candidate必须作为EDIT_TARGET；只有局部无法稳定修复或多处结构同时崩坏才Fresh Regen。
失败码：`FACE_INTEGRITY_FAIL / ANATOMY_HAND_FAIL / HAND_CONTACT_FAIL / WRIST_CONNECTION_FAIL / CONTACT_INTEGRITY_FAIL / FOREGROUND_LIMB_READ_FAIL / FOREGROUND_FIGURE_COHERENCE_FAIL`。

### `RANDOM GENERATION FAILURE`｜随机生成失败
症状：Prompt结构正确、参考职责正确、同Prompt此前可正常生成，但这次出现偶发手崩、局部畸形、一次性异常。
处理：先确认是否已经接近合格。只有Prompt/Reference/Shot结构均正确、剩余问题高度疑似单次随机波动时，才可**可选建议同一Prompt再试1次**；否则先做最小Prompt修正，不默认抽第二Take。

## 回退层级

- 剧情因果错 → Stage 01
- World State / Scene Transition / 人物进出 / Prop去向等导演连接逻辑遗漏 → Stage 02
- 时长/Shot结构错、平台Duration Profile与映射冲突、凭空编造Slot/Hard Max、为凑平台时长Dead Hold或为适配平台上限导致表演/动作过快 → Stage 02C/05（必要时`PLATFORM_DURATION_SPLIT_REQUIRED`；若伤害Director Invariants则回Director Judge）
- 场面调度、人物距离、Depth、Axis/Screen Direction、Shot Progression、Cut Motivation、Transformation Presentation错 → Stage 02 Director Patch；若冲突只在Stage 03真实Geography出现 → Director Spatial Reconciliation
- 正式资产本身错 → Stage 03
- 前景脸/手/关键接触硬伤 → Stage 03 Candidate Switch或Local Patch；不得带着明显静态错误进入Stage 04/05
- Canon已正确但Stage 02 Required Production Support缺失 → Stage 03补最小Support Reference；若风险只在Approved Storyboard具体构图确定后成立 → Stage 04补Additional Video Conditioning Keyframe
- 构图/Panel/表演设计错 → Stage 04
- Render/Cinematic Style Authority职责错 → Stage 03 Style Authority / Reference Resolve最小修正；若仅Stage 05引用错则只重编Reference Pack
- 新场景综合色派生错 → Stage 02/03 Color Derivation；单个Shot临时光色错 → Stage 05 Shot Lighting Variant最小修正
- Crowd Blocking / Motion Intent / Attention / Reaction Propagation设计错 → Stage 04；若只是模型偶发未执行已正确Crowd Contract，再判执行随机性
- 肢体占用/道具支撑/换手/接触前置条件/重心Bridge设计错 → Stage 04；若Storyboard已有合法解但Final Prompt漏写，则Stage 05最小重编
- 动作逻辑合法但Motion Corridor / Kinetic Chain / Overlap / 步态 / 余韵不自然 → Stage 04；若Storyboard已锁自然过渡但Prompt漏编，则Stage 05只重编Integrated Timeline
- Prompt出现跨模块语义重复 → Stage 05 Prompt Compiler重新归并，不回上游重做内容
- 动作执行/模型镜头/CUT执行错 → Stage 05
- 剪辑/声音/综合色统一错 → Stage 06
- 纯随机失败 → 不回退；若当前结果已接近合格，可选建议同Prompt再试1次

## 诊断输出格式

```text
【Failure Diagnosis｜失败诊断】
失败类型：ACTION / PHYSICS

已经正确：
- 人物身份正确
- 场景正确
- CUT正确
- 综合色正确

真正问题：
- Character B倒向远离Character A
- 膝盖没有先失去支撑

问题来源：Stage 05 动作路径

最小修改：
- 保留原Reference Pack
- 保留原镜头时间轴
- 保留原CUT
- 只修改重心、膝盖、肩线和Character A的接应动作

处理方式：局部修Prompt后重生
```

## 不要做的事

- 一个手指错误就把整个Storyboard推翻；
- 一个随机畸形就改人物母图；
- 动作方向错却去修改画风Prompt；
- 场景镜像却靠加更多人物参考图解决；
- 一失败就无限增加负面词。

失败诊断的目标是：**返工范围最小，已经正确的东西尽量不动。**


## Current｜Temporal Salvage Before Retry

任何Video Take QC不通过后，在决定新增Take前必须先读取`video_temporal_salvage_qc.md`与当前`TEMPORAL_SALVAGE_MAP`：

1. `SALVAGE_AVAILABLE` → 先冻结/保留可用Source Windows；
2. 失败内容能在不伤Director Invariants的前提下独立补生成 → 只补缺失Beat/失败区间所需内容；
3. 原镜头明确要求不可切Long Take → 不得为了利用前后好片段强行新增CUT；必要时仍整Take重生，但旧片段可保留为备用/Handle；
4. `VIDEO_KEEP + AUDIO_REPLACE` → 优先Stage 06处理声音，不重生画面；
5. 可Trim尾部/局部坏帧 → 优先Stage 06 Trim/Post；
6. `NO_SALVAGE`才按正常Failure Diagnosis决定完整重生。

失败：`TEMPORAL_SALVAGE_NOT_ASSESSED / SALVAGE_DIRECTOR_INVARIANT_BREAK / SALVAGE_CONTINUITY_MISMATCH`时不得进入额外Take决策。

## 与Retry / Escalation的关系

Failure Diagnosis负责回答“错在哪里”；`Retry / Escalation Policy`负责回答“用多大成本处理”。

默认顺序：

1. 先查Temporal Salvage：能保留现有成功Window + Trim / 小修解决 → 不重生已成功部分；
2. 使用当前有效Video QC Report定位问题来源；默认读取External Video QC Report，不重复观看视频；若用户主动启用LOCAL_SELF_CHECK，则以亲检结果复核；
3. 有明确可修问题 → 最小修改Prompt，只生成1个新Take；
4. 已非常接近目标且高度疑似随机波动 → 可选建议同一Prompt再试1次；
5. Reference Overload → 简化Reference Pack；
6. 复杂Segment持续失败 → 回Segment Planner拆段。

See `retry_escalation_policy.md`.

## Continuity联合诊断

诊断前额外判断当前差异属于Continuity Priority的P0 / P1 / P2哪一级。

处理规则：
- P0错误 → 正常进入最小回退；
- P1差异 → 先判断是否真正影响观看/剪辑，再决定是否修；
- P2差异 → 默认不触发重生。



## MUSICAL-COMBAT / IMPACT-VFX FAILURE（音乐战斗 / 打击特效失败）

### MUSICAL-COMBAT
症状：角色Music Identity只剩换色、音符、五线谱或术语标签；实际Footwork、Attack Cadence、Weapon Kinetics、Recovery与Tactical Timing和其他角色没有区别。

优先检查：`music_identity_mapping.md` → `music_identity_registry.md` → `cinematic_combat_vfx_engine.md` → 当前Combat Design Brief。先确认Music Identity Authority，再把音乐术语翻译成可见时间/运动语法；不要继续加更多音符图案。

### IMPACT-VFX
症状：命中点不清、目标无因飞走、所有重击只靠震屏、VFX像贴图Glow、技能都变成爆炸/光炮、环境完全不响应、技能后一帧清空。

优先检查：Contact Point / Force Direction → Compression / Force Propagation / Recoil → Environment Proof → VFX Cause / Source / Spatial Geometry / Medium Interaction / Decay → New Combat State。若环境已经被破坏或持续场已经建立，写回World State，不得下一Segment重置。

最小修改原则：Impact错就只修ACTION / PHYSICS / VFX /必要Camera，不重做身份/画风；Music Translation错就保留技能Canon和角色资产，只重编Timing / Weapon Kinetics / Tactical Function。

## REFERENCE-FIDELITY｜低清控制参考污染高清母资产

症状：新视频继承整张九宫格/故事版、Ending Frame、Render/Cinematic Style Board或Global/Scene Color Card的低清、简化人物、截图柔化、压缩模糊或低细节密度，导致已经上传的高清人物/场景/道具Master失效。

优先修法：
1. 不先重做高清母资产；
2. 加载`reference_role_fidelity_isolation.md` + `render_quality_authority.md`；
3. 仅在**已观察到低清/版式污染**的字段上降级：先保留Storyboard独有的Temporal/Action Sequence，再对受污染的Composite/Detail字段选择关键Panel、Clean Crop或由HD Anchor接管；不得一律把整张Storyboard解析为TEXT_CONTROL或删除整板；
4. Ending Frame只保留连续性；若该模型容易被其画质带偏且Continuity Snapshot足够，降为TEXT_CONTROL；
5. Render Style只保留绘画语言；Cinematic Shot Style只保留项目级摄影语法且不覆盖Storyboard；综合色只保留当前最直接Global/Scene/Shot层级，三者都不承担对象细节；
6. 确认当前Task真正需要的Character / Environment / Prop / Weapon高清Authority被标为`HD_OBJECT_AUTHORITY_IMAGE`；Environment / Prop已有Shot-matched Coverage时优先Coverage，不机械回退Parent Master；
7. 重跑`REFERENCE_FIDELITY_FAIL` Gate，只重编必要Reference执行结果 + 唯一直接Render Fidelity语句后再试。

**低清图放大/超分不能修复Authority错误。** 它仍然是CONTROL，不会因此升级为Fidelity Master。


## AUTO-BGM / AUDIO BOUNDARY FAILURE（自动配乐 / 声音边界失败）

症状：视频模型自行生成BGM、情绪音乐、战斗音乐、悬疑铺底、cinematic score，或把Music Identity误解成自动配乐指令。

处理：
1. 检查FINAL VIDEO PROMPT在需要声音边界时是否只保留一个直接的“不要生成背景配乐”执行句；
2. 保留必要Dialogue/VO、Ambience、Foley/SFX与明确Diegetic/Source Music；
3. 若随机BGM可在后期干净移除，优先Post修；
4. 若随机BGM与对白/环境声严重混合且无法分离，按AUDIO GENERATION FAILURE重试；
5. 不把随机生成BGM升级为正式配乐，正式BGM仍回Stage 06。


## Failure-before-Compute（额外Take前成本判断）
在任何额外Video Take前读取 `personal_creator_cost_efficiency_engine.md`：先判断问题能否在Text / Static Patch / Storyboard / Camera Contract / Trim中更便宜地解决。只有T3/T4且Prompt/Reference/Blocking已正确、剩余问题主要属于模型随机性时，才允许继续使用受限候选预算。


## Revision QC Scope Freeze
Failure Diagnosis输出Minimum Necessary Change后，必须建立/更新`qc_scope_freeze_ledger.md`：上一轮已PASS且不受本次改动影响的维度标FROZEN_PASS；本次问题标OPEN_REVISION_TARGET；只有Change Surface确实触及才REOPEN。下一轮Web QC Evidence Pack按该Scope选图。

## Image Candidate Backup Check（图片候选备份检查）

当Stage 03/04的Primary Candidate QC失败且同组存在Backup时，先检查Backup是否已经避开同一失败点：
- Backup明显解决该P0/P1问题 → Backup升级为Primary进入Deep QC；
- Backup仍有同类问题 → 才进入Revision / Fresh Regen；
- 不在已有可用Backup时立即重新生成新图。

该规则只适用于图片/Storyboard候选，不影响Video单Take成本策略。

## Revision vs Fresh Regen Binding（返修与重生分流）

诊断为“当前图片大部分正确，只需修改局部/少量字段”时，后续任务必须标`REVISION_IMAGE / LOCAL_PATCH`，并把**失败Candidate本身**绑定为`REVISION_SOURCE_IMAGE / EDIT_TARGET`。Parent Master只能提供必要Canon Support。

只有诊断明确认为当前Candidate不值得保留、需要从正式Authority重新生成时，才标`FRESH_REGEN`并以Master为Primary Source。禁止嘴上说“修改当前图”，Reference却只@Master。

若绑定错误，标`REVISION_TARGET_BINDING_FAIL`，先修Reference Pack，不生成。

## Reference Completeness Failure
如果当前镜头关键可见人物/场景方向/道具/武器/实体/状态没有被Reference Pack覆盖，标`REFERENCE_COVERAGE_GAP`；如果只是槽位不足，标`REFERENCE_SLOT_OVERFLOW`。两者都不得直接通过增加Video Take解决。


### `BODY PRESENTATION FAILURE`｜身材美与服装呈现冲突
症状：所有成年角色都被收腰/贴身/高腰模板化；Oversized被强行掐腰；宽松Look把人物画成另一副身材；冷天为了“显身材”出现不自然贴体结构；或变身礼服虽然华丽，却把同一人物既定Body Identity / Appeal完全吞掉。

路由：`body_identity_presentation_authority.md` → `character_appeal_silhouette_system.md` → Daily走`wardrobe_style_design_engine.md`，Transformation走`transformation_splendor_architecture.md` + `transformation_asset_standard.md`。先确认Body Identity，再选择DIRECT / FRAMED / PROPORTIONAL / IMPLIED / CONTRAST；不得用更多贴身关键词解决。

状态：`BODY_IDENTITY_DRIFT / BODY_BEAUTY_SUPPRESSED / BODY_PRESENTATION_TEMPLATE_COLLAPSE / FAKE_WAIST_CORRECTION_FAIL / BODYLINE_KEYWORD_OVERLOAD / TRANSFORMATION_BODY_IDENTITY_DRIFT / TRANSFORMATION_BODY_BEAUTY_SUPPRESSED / TRANSFORMATION_BODY_PRESENTATION_TEMPLATE_COLLAPSE`。

### `SOURCE WARDROBE ADAPTATION FAILURE`｜小说服装Authority错误
症状：普通小说服装描述被机械照抄，或真正影响剧情的服装事实在Skill重设计中丢失。

路由：`source_wardrobe_adaptation_authority.md` → `character_costume_dramaturgy.md` → `wardrobe_style_design_engine.md`。

状态：`NOVEL_WARDROBE_LITERALISM_FAIL / STORY_WARDROBE_FACT_LOSS_FAIL`。


### `COLOR AUTHORITY PRESERVATION`｜综合色视觉权威丢失/漂移
症状：同Scene重建/补图/Assembly/FMH/Support/Anchor/Video颜色逐轮偏移；Scene-bound图片/Shot Execution漏掉Approved Scene Color Card；或Final Video虽然Primary Visual综合色已正确却仍机械占用色卡槽，挤掉更关键的Identity/Prop/Environment/Continuity Reference。

优先检查：`color_authority_preservation_gate.md` → `color_script_derivation_engine.md` → `reference_resolver.md`。
- 图片/Shot Execution有Approved Scene Card但未绑定 → `SCENE_COLOR_AUTHORITY_REUSE_MISS / COLOR_AUTHORITY_BINDING_GAP`；Final Video则先检查`scene_color_authority_id`与Primary Visual血缘，`LINEAGE_ONLY`合法，不得仅因未@色卡报错；
- 复合色卡污染 → 先按目标模型Capability决定Direct Color Reference / Crop / Dedicated Channel；只有已发生色块/版式泄漏，或`ROLE_SEPARATION=VERIFIED_FAIL`且无安全Color-Only Crop / Dedicated Channel可保留所需字段时才升级`SCENE_COLOR_APPLIED_REFERENCE`；
- 平台支持原生视觉Reference但未真实绑定 → `COLOR_NATIVE_BINDING_MISS`；
- 色卡越权改Identity/Geometry → `COLOR_AUTHORITY_BLEED`。


### `REFERENCE_LAYOUT_LITERALIZATION / REFERENCE_SAMPLE_CONTENT_BLEED`｜控制Reference版式或样例内容泄漏
症状：Video出现色块/色条/gradient矩形、九宫格/Panel边框/分屏、Board标题/编号/标注，或突然复制Style/Color Board里的示例人物、车辆、地点/构图。
优先检查：`visual_reference_routing.md` → Executor Input Map → Color/Style/Storyboard视觉输入的当前Capability/Role Route是否正确。
处理：确认是哪种Reference Route发生实际Leak → 只升级失败路线（Role Lock / Panel Split / Crop / Applied Reference）→ 更新当前Reference Binding Map。没有Leak时不因Board类别主动增加中间资产。

### `VOICE / PROSODY`｜配音节奏与句尾执行失败
症状：重要台词语速全程一样、停顿机械按标点、重音平均、句尾语调与潜台词冲突、角色随机换音区/音色、多人对白轮流念稿。
优先检查：`actor_performance_engine.md` → `voice_direction_prosody_engine.md` → `voice_identity_audio_status.md`。
若只是TTS参数执行偏差，Stage 06重建`VOICE_TTS_HANDOFF`；若`VOICE_DIRECTION_PLAN`本身缺Trigger/Meaning/Objectve/Tactic/Subtext或Pace/Pause/Stress/Terminal执行逻辑，回Stage 02补受影响Line，再由Stage 05重编`VOICE_PROMPT_HANDOFF`。不要单纯换音色。


## Current｜Prompt Surface / Metadata Leakage

**症状：** 生成Prompt正文出现`Reference Responsibilities`、资产全名/版本、内部ID、MUST_BIND/Authority/Resolver解释，或出现`TASK_SHELL / INPUT_LABEL / LOCAL_PATH / FILE_METADATA`等操作者壳，或真实@Token后挂着长资产名和职责说明。

**处理：** 重新执行Allowlist Extraction + `SURFACE_LINT_REPORT`。仅加一句“不要出现文件名/路径”不算修复；所有Forbidden Counter必须归零。失败码：`LOCAL_PATH_LEAK / FILE_NAME_LEAK / TASK_SHELL_LEAK / SURFACE_LINT_NOT_RUN / PROMPT_SURFACE_SANITIZATION_FAIL`。

**Diagnosis：** 这是Compiler Surface失败，不是画面美术问题；不要消耗新Take测试。

**处理：**
1. 冻结当前Task Contract /真实Reference绑定；
2. 保留`EXECUTOR BINDING PACKET`供操作者；
3. 运行`model_facing_prompt_surface_sanitizer.md`；
4. 把Role字段归并到Subject / Environment / Color / Entry / Camera / Timeline；
5. 真实Token只保留最短执行句；
6. 若Token对应Color/Style/Storyboard Board，先核对`REFERENCE ROUTING MANIFEST`：只要Direct Route没有`VERIFIED_FAIL`且没有实际Leak证据，就优先保留原视觉输入；`UNKNOWN / Route未验证`本身不是降级理由。只有Capability明确不匹配、真实发生Literalization/Sample Bleed、槽位冲突或用户明确要求时，才改Panel/Crop/Applied Reference。不得仅因Reference类别自动替换；
7. 重新编译同一Prompt，不重设计剧情/导演。

失败码：`MODEL_FACING_METADATA_LEAK / REFERENCE_ADMIN_TEXT_LEAK / PIPELINE_JARGON_LEAK / NATIVE_TOKEN_OVERANNOTATION / UNROUTED_CONTROL_REFERENCE_TOKEN / PROMPT_SURFACE_SANITIZATION_FAIL`。

## Current｜Style Projection / Style Drift

### `STYLE TAG ONLY`｜内部有完整Style DNA，模型Prompt只剩抽象标签
症状：Prompt只有“二维电影插画 / 欧陆复古 / 忧郁克制 / 保持一致”等，补图或Video逐轮出现另一种模型味。

诊断顺序：
1. `style_authority_projection_gate.md`是否触发；
2. 是否形成`STYLE PROJECTION CARD / Fingerprint`；
3. Reference Resolver是否保留最直接Style Continuity视觉证据；
4. Sanitizer / Semantic Dedup是否误删渲染语言；
5. Prompt正确但实际结果仍漂移时，归类为`MODEL_EXECUTION_VARIANCE`并走视觉QC/Revision，而不是继续无限加抽象形容词。

失败码：`STYLE_AUTHORITY_PROJECTION_MISS / STYLE_TAG_ONLY_FAIL / STYLE_EVIDENCE_BINDING_GAP / STYLE_PROJECTION_SANITIZER_OVERSTRIP`。



## Current｜Stale Prompt Artifact Closure
当Workspace已有旧Prompt文件、旧Compiler版本正文、旧任务壳或“沿旧Prompt继续改”请求时，必须读取`stale_prompt_artifact_gate.md`。旧Prompt只恢复任务意图，不可作为当前文字母版；统一Fresh Recompile后再走Surface Sanitizer + Prompt Egress。

## Current｜Prompt Constraint / Shot Overload Failure

### `PROMPT_CONSTRAINT_CONFLICT`
症状：同一Camera/AUDIO/Action/Reference/State出现互斥指令；Prompt每次生成结果随机选择不同解释。
处理：回`VIDEO_EXECUTION_STATE`和`prompt_constraint_solver.md`，按Authority裁决为唯一状态；不要继续加Negative。

### `REFERENCE_CONTENT_ROLE_CONFLICT`
症状：Prompt说某@图控制人物/道具，但当前实际Token图中没有对应证据。
处理：重做当前`REFERENCE BINDING CONTENT MAP`；检查UI槽位/附件/Token/Adapter Handle是否真的指向预期资产。无法由当前有效视觉Evidence核验时先补确认，不生成。

### `SHOT_PROOF_CAPACITY_EXCEEDED / MOTION_LOAD_OVERLOAD`
症状：镜头逻辑无冲突但同一时间窗要求太多独立动作/微小物件/Camera变化，反复废片。
处理顺序：降P2 → 合并从动作 → 补静态/Previs Proof → 调整景别/Blocking → 只有Director允许时Split；禁止无限加Prompt。

### `QC_CONTRACT_BACKFLOW`
症状：Final Prompt尾部出现“成片必须满足/自检/QC检查”再次复述Timeline/Audio/Camera。
处理：删除QC Block；若其中有真正遗漏的Generation事实，回对应Owner写一次并重新Conflict Solve。
