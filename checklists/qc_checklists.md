# AI漫剧 QC（质检）清单

> **阅读方式：** 以中文理解和执行为主，同时保留值得学习的专业英文术语。专业词第一次出现时写成“English Term（中文解释）”；后续可直接使用已解释过的英文标签，方便边做边熟悉影视与AI生产词汇。


## Stage 01｜Source Parse → Screenplay Adaptation → Screenplay Lock质检

### 01A Source Narrative Parse
- [ ] 已登记Source Mode；小说/最终剧本/草稿/Hybrid/Outline没有混为同一Authority
- [ ] 核心事件、人物动机/关系、世界规则、因果、Setup/Reveal/Payoff、必须保留对白/信息已进入`SOURCE NARRATIVE FACT MAP`
- [ ] 已区分Visible Action / Dialogue / Internal Thought / Narration / Descriptive Prose / Sound Event
- [ ] Scene Boundary Candidate没有按小说换段/换句机械切Scene
- [ ] 01A没有Shot / Lens / Camera / Storyboard / Reference / Asset越权

### 01B Screenplay Adaptation
- [ ] 每个非直译改编可追踪到KEEP / COMPRESS / MERGE / SPLIT / EXTERNALIZE / VISUALIZE / AURALIZE / DIALOGUE_ADAPT / SUBTEXT / RELOCATE / DELETE_REDUNDANT之一
- [ ] Scene Split/Merge由时间、地点、戏剧Objective/Turn决定，不由AI视频时长或小说段落决定
- [ ] 文学心理已转成可演行为/对白/声音或保留为Subtext；没有假设观众自动知道人物内心
- [ ] 对白口语可演，没有把Narration直接塞成说明性台词
- [ ] Locked Canon / Reveal / Setup-Payoff没有因压缩、移动、删除而改变意义
- [ ] 单集15–18分钟只作为宏观戏剧密度约束；没有在Stage 01分Shot秒数、Padding或强压自然表演
- [ ] 剧本草稿没有Shot / Lens / Camera / Focus / CUT / Storyboard / Reference / Asset指令

### 01C Screenplay Lock
- [ ] 每Scene已有Scene ID / INT-EXT / Location / Time / Dramatic Purpose / Characters / Objective / Obstacle / Turn
- [ ] Action / Dialogue / Sound按因果可执行，Entry State与Exit Story State可继承
- [ ] Adaptation Decision Ledger可追踪；关键Canon无静默改写
- [ ] Novel/Hybrid/Outline/Screenplay Draft改编后已进入`SCREENPLAY QC PASSED / WAITING APPROVAL`并获得用户明确批准
- [ ] 用户明确提供Final Screenplay时也完成Source Parse + Screenplay QC，而不是直接跳导演
- [ ] Workspace已记录`EPISODE SCREENPLAY LOCKED`
- [ ] 没有`EPISODE SCREENPLAY LOCKED`时Stage 02没有开始正式Director Intelligence

## Stage 02｜时长 / 导演拆解质检

- [ ] 本集目标总时长在15:00–18:00（900–1080秒）
- [ ] 已区分整集Runtime Target与单次生成平台能力；Skill本身没有固定单次视频秒数上限
- [ ] 每个Segment都有Director Target Duration与简短Duration Rationale，时长由Beat/对白/表演/动作/Camera需要决定，不机械套固定秒数
- [ ] 没有仅因Director Target超过历史10秒范围自动拆分；只有当前真实平台Hard Max要求时才做自然拆分
- [ ] 没有为了填满平台时长加入Dead Hold/重复动作，也没有为了适配平台上限压缩自然对白、关键反应或动作物理
- [ ] Scene预算合计与本集目标基本一致
- [ ] Beat预算能回卷到所属Scene，Shot预算能回卷到所属Beat
- [ ] 有对白/VO的Shot已计入真实语流、真正有因的停顿和必要反应；普通呼吸融入Speech Phrase而非单独占一个Beat
- [ ] 重要人物交流已建立Actor Performance Brief：Given Circumstances / Objective / Stakes / Obstacle / Relationship / Tactic / Subtext清楚
- [ ] Beat边界优先由Objective / Tactic / 关系判断 / 新事实变化决定，没有把每个句号或每句台词机械拆成新Beat
- [ ] Listener / Speaker都按Active Listening处理：新刺激是否改变判断与策略，而不是为了“有表演”逐句安排动作
- [ ] Scene若存在明显背景群体，已建立Crowd Presence Brief；没有把几十个路人逐人套Active Listening
- [ ] Crowd已区分Featured Background / Crowd Cluster / Deep Background Mass，并记录Density / Zones / Primary Flow / Stationary Activity / Attention Baseline
- [ ] 若存在会影响群众的强Stimulus，已规划Reaction Propagation；没有默认所有人同时转头/逃跑
- [ ] 没有把自然需要较长时间的台词硬压进过短镜头
- [ ] 每个Shot有明确Shot Purpose（Spatial / Information / Action / Reaction / Performance / Insert / Transition等）
- [ ] Shot Purpose分布符合戏剧需要，没有连续大量同类镜头导致节奏单调
- [ ] 每个重要Scene已建立`Scene Visual Thesis`，不是只写抽象情绪；Visual Thesis能落到空间/距离/构图关系
- [ ] 新Environment在Stage 02只建立Functional Spatial Requirement Draft；没有在正式Environment Geography未批准前凭空写死门窗/通道/镜头空间
- [ ] 重要人物关系已建立Dramatic Geometry / Blocking Plan；Objective / Tactic变化会在需要时转译成APPROACH / WITHDRAW / BLOCK_EXIT / KEEP_BARRIER / PROTECT等空间行为
- [ ] 重要多人Scene已锁Primary 180 Axis / Screen Side / Eyeline / Movement Direction；有意越轴有Re-establish方法
- [ ] 重要Scene已检查Distance Arc与Depth Plan；没有无理由全程保持同一安全距离
- [ ] 重要多人Shot不存在“同深度 + 相似人物尺寸 + 均匀间距 + 全身完整展示”的默认构图；有意仪式性陈列除外
- [ ] Detailed Shot Contract按复杂度记录Focus Owner / Critical Visual Read / Shot Size / Screen Occupancy / Distance / FG-MG-BG / Entry/Landing Camera Geometry / Lens Family / Focus Plan / Stabilization / Blocking / Axis / Camera Intent / Motion Priority / Cut Motivation / Shot Relation
- [ ] Critical Visual Read与景别/主体占比一致：要求观众看清Eye Motif / Contact / Injury / Prop Detail时没有安排在不可读远景
- [ ] Scene Shot Progression有整体摄影推进逻辑，不是所有Shot各自合理但整场距离/视角完全不变
- [ ] 每个明确CUT都有Information / Power / Eyeline / Action / Reaction / Spatial / Rhythm / Match / Ellipsis / Transformation等动机；没有机械一句台词一个正反打
- [ ] T3/T4或Camera影响空间/Blocking时，Stage 02已建立Camera Intent并按需提前生成初版Camera Motion Contract；Stage 04不会重新发明运镜理由
- [ ] 当“声音缺失/关键画内声音/Contact SFX/声音桥”本身改变叙事或CUT时，Stage 02已建立Dramatic Sound/Silence Intent；没有把这类导演因果全部推迟到Stage 06
- [ ] 当灯灭/门光/聚光/Transformation光线会改变主体可读性时，Stage 02已锁Narrative Lighting Function与Critical Visibility；具体综合色仍服从Global→Scene→Shot Color Authority
- [ ] 正式锁Shot / Segment前已运行World State Continuity Audit：每个Scene边界/重大Beat边界都有Exit State → Required Entry State → State Diff
- [ ] 上一状态若仍在行驶/步行/奔跑等明显移动中，下一状态进入“抵达后”时已让观众感到Arrival真正发生；没有无因从moving直接跳成静态已到达
- [ ] 必要过渡采用DIRECT / IMPLIED / RESIDUAL / VISIBLE / INTENTIONAL ELLIPSIS中的合理形式；没有用`SCENE_OPENING`掩盖CONTINUITY ERROR
- [ ] Transition遵守Minimum Necessary Bridge：足够解释状态变化但没有把停车/开门/步行等拆成流水账
- [ ] 人物进入/离开有来源；新进入者的Knowledge Access与其实际进入时间一致，没有凭空知道未听见的信息
- [ ] 关键Prop有Owner / Holder / Location / Visible / State来源；没有凭空出现、消失、换手、展开/收起、损坏/复原
- [ ] Ongoing Physical Task跨CUT/Scene有继续、完成、被打断、放弃或转交的结果，没有自动清零
- [ ] Injury / Fatigue / Wetness / Dirt / Blood / Costume temporary state / Transformation在换Scene后按原因延续或改变，没有World Reset；完整Transformation Recovery若已触发，则伤势合法更新为Post-Recovery State且旧伤没有被错误刷回
- [ ] Environment Runtime State（门锁、灯、电、破坏、火烟水、Crowd、重要Audio World State）没有无因恢复默认
- [ ] Knowledge / Suspicion / Trust / Relationship / unresolved Objective / Emotional Pressure在换Scene后按剧情延续，没有人物“大脑清缓存”
- [ ] Transition Audit产生的必要外景/入口/停车区/连接空间等正式资产已提前进入Episode Asset Requirement Manifest
- [ ] Stage 02已输出人物/服装状态、场景、道具、特殊状态等资产需求标签
- [ ] Stage 02已输出季节、气候、天气、温度、室内外、时间、场合、活动等服装环境条件
- [ ] 已完成Segment Planner：每个Segment明确包含哪些Shot、Director Target Duration和CUT关系；是否拆分由戏剧结构与当前真实平台能力决定
- [ ] Storyboard的Panel/Shot可在Director Target Duration内自然执行；若明显不足已DURATION_REPLAN，而不是删除关键表演
- [ ] 没有机械“一Shot一Segment”或“一Scene一Segment”，Segment边界按生成稳定性和戏剧单元判断
- [ ] HIGH复杂度Segment若仍决定一次生成，已有明确理由；否则已合理拆分
- [ ] 战斗/追逐Scene已建立Engagement Distance Ladder / Spatial Dominance / Attack Lane / Escape Lane / Depth Strategy / Contact Read Shot / Initiative Shift Visual；不存在`COMBAT_LINEUP_FAIL`
- [ ] 重要Montage已有Montage Thesis / Ordering / Connection Device / Information Gain / Duration Rhythm / Return-to-Mainline Trigger，不是资产PPT
- [ ] 首次/关键变身：已有Approved设计则建立Transformation Presentation Contract；首次设计尚未完成则只建立Presentation Requirement Draft，锁Silhouette/Eye/Material/Weapon-Body/Visual Level Gap的“可读要求”，没有在Stage 02凭空设计具体服装
- [ ] 每个Segment已标记Shot Investment Tier（T1/T2/T3/T4）；只有真正的首次变身、Boss关键Hit、核心情绪Close-up、结尾Hook或高宣发价值镜头进入T4，没有全片Hero化
- [ ] 场景已按Location Investment Tier（L1/L2/L3）决定Coverage；没有为了保险机械生成360°
- [ ] Stage 02已建立Environment / Prop Shot Coverage Matrix；每个新增Coverage需求都能回指真实Shot、Camera/Visible Side、Required State与`Why Master Is Insufficient`

- [ ] Stage 02已建立`Video Risk-Driven Static Reference Matrix`；每个T3/T4、关键Insert、复杂Interaction/Contact、严重伤势/破损、关键机关/攻击形态都判断`Static Ambiguity / Static-Solvable / Existing Authority Enough / Required Ref / Owner Stage / Why`
- [ ] `Existing Authority Enough`不是只按“理论上能推断”判断；若低成本高清静态证据能显著降低昂贵Video失败概率，已路由到Coverage / Persistent State / Stage 03 Support / Stage 03 Shot Assembly / Stage 04 Video Conditioning
- [ ] Stage 02已完成`Shot Assembly Need Analysis`：对多人关系、人物进入功能空间、Montage情境、人物-场景-道具同框等情况判断是否需要`SHOT_ASSEMBLY_ASSET`
- [ ] `SHOT_ASSEMBLY_ASSET`只在“多一张高清静态组装图确实能降低昂贵Video风险”时生成；没有把所有Shot一律资产化
- [ ] 每个Required Shot Assembly已有Assembly Contract：Scope / Framing Family / Parent Sources / Spatial Occupancy / Holder-Contact / Visibility Priority / Canon Locks / Scoped Cast Boundary明确；没有写成Storyboard时间轴
- [ ] Shot Assembly默认16:9高清单帧时，其比例来自Assembly资产用途，不是从Storyboard Sheet/Panel继承；
- [ ] `SHOT_ASSEMBLY_ASSET`不是直接由Storyboard宫格放大、清稿或描画得到；反复/命名人物使用Approved Character Authority；任何清楚可见的一次性`SCOPED_CAST / NON_RECURRING`都必须先有Approved FMH/Minor Human Master，Assembly只继承其Appearance并锁当前Scene/Shot Group的人景物关系，不得首次建立人物外观；Environment / 关键Prop / State使用Approved Authority
- [ ] 无未解决`SHOT_ASSEMBLY_GAP / SHOT_ASSEMBLY_AUTHORITY_FAIL`
- [ ] 若已有`SHOT_ASSEMBLY_ASSET`，Stage 04/05已正确将其作为关系/同框/空间占位参考；若已存在更精确的`VIDEO_CONDITIONING_KEYFRAME`，两者职责没有串位
- [ ] 速度曲线、动作叠接、步态、Crowd时序、Camera Motion、对白/微表情Timing等时间行为没有被错误资产化为静态Support图
- [ ] Character资产没有被Environment / Prop Coverage规则重新拆分或无理由新增人物视图
- [ ] Episode Workspace已记录当前Scene / Segment / Next Action
- [ ] Stage 02汇总资产需求时已执行Reuse First识别，能复用的APPROVED资产没有被列入无意义重复生成队列
- [ ] Stage 02只规划Scene所需资产职责；Scene Pack在Episode Asset Freeze后才建立/更新，没有在Stage 02提前作为正式资产放行入口
- [ ] Episode Asset Requirement Manifest明确区分REUSE / TO BUILD / COVERAGE TO BUILD / TRANSFORMATION / PERSISTENT STATE / SUPPORT REF TO BUILD / SHOT ASSEMBLY TO BUILD，并明确排除Storyboard与Ending Frame
- [ ] Stage 02已把所有Scene / Shot / Segment资产需求汇总成整集Episode Asset Requirement Manifest并去重，避免进入Stage 04/05后逐Segment零散发现正式资产缺口
- [ ] 没有为了凑时长而加入无信息重复镜头或平均慢动作
- [ ] 若当前平台Hard Max要求拆分，只在自然Beat/CUT/Thought/Action Landing处分Segment；没有为平台上限硬压对白/表演，也没有为填满Slot增加无信息内容


- [ ] 每个Segment已在Stage 02登记Entry Mode：CONTINUITY_ENTRY / CUT_ENTRY / SCENE_OPENING
- [ ] 涉及Music Identity的Scene已区分稳定Character Leitmotif与临时Scene Emotion / Action Intensity，没有用当前情绪重写角色核心音乐身份
- [ ] 战斗涉及Music Identity时已建立Musical Time Grammar / Tactical Function：音乐影响Timing / Footwork / Weapon Kinetics / Recovery，而不是只计划换色VFX/音符
- [ ] 重要战斗已预先确定Impact Scale / Key Contact / Force Direction / VFX Physical Principle / Persistent Combat State，Stage 02没有用“华丽特效”占位
- [ ] 重复/复杂标志VFX已判断TEXT_GRAMMAR_ONLY还是VFX_REFERENCE_REQUIRED；普通击打没有无意义新增VFX母图
### Director Intelligence Core｜Current
- [ ] 每个Scene已标`D0 CONNECTIVE / D1 DRAMATIC / D2 SIGNATURE`
- [ ] Audience Knowledge / Emotion IN→OUT、Dramatic Question、Felt Intent已明确；Felt Intent不是摄影关键词
- [ ] D1至少2个、D2至少3个真正不同的Directorial Interpretation；不存在`DIRECTOR_OPTION_COLLAPSE`
- [ ] Director Judge前的Option/选择理由没有使用现有资产、Reference槽位、Platform Duration Profile、Video成本或“模型更容易”作为优劣依据；不存在`DIRECTOR_PREMATURE_PRODUCTION_CONTEXT_FAIL`
- [ ] D1/D2已执行Actor / Cinematographer / Editor Critique；Critique没有用“模型难生成”越权否决艺术方案
- [ ] Director Judge明确Selected Option / Rejected Alternatives / Accepted Critiques / Non-Negotiable Directorial Invariants
- [ ] Selected方案不是多数票拼盘，不存在`DIRECTOR_SYNTHESIS_MUSH_FAIL`；实质SYNTHESIS若组合多个Option策略，已对受影响部门做Targeted Re-Critique，不存在`DIRECTOR_SYNTHESIS_UNREVIEWED`
- [ ] Detailed Shot Contract之前已完成Sequence Arc：Attention / Knowledge / Distance / Performance Access / Reaction Economy / Cut Density / Closing Image
- [ ] Reaction Shot、Close-up、慢推、正反打等均能回指Sequence Function，不存在`GENERIC_COVERAGE_FALLBACK_FAIL`
- [ ] Reference槽位、已有资产、Platform Duration Profile、模型能力只在Director Judge之后进入Execution Translation
- [ ] 若执行限制冲突，已走`AI_EXECUTION_CONSTRAINT_CONFLICT / DIRECTOR_INVARIANT_SPATIAL_CONFLICT`返回Director Judge；没有静默修改POV / Reveal / Blocking / Reaction / Key Cut-Hold
- [ ] Judge若批准妥协并改变Invariant，Decision Card / Sequence Arc / Detailed Shot Contract已按Change Impact同步更新，不存在`DIRECTOR_COMPROMISE_PROPAGATION_GAP`

## Existing Project Migration｜旧项目迁移质检

- [ ] 已有`DIRECTOR CORE LOCKED / DIRECTOR BREAKDOWN READY`或Stage 03/04/05/06成果的旧Episode没有因为切换新版Skill从Stage 01重做
- [ ] `GRANDFATHERED`只作为迁移处置标签，没有替代APPROVED状态
- [ ] 只有旧记录中已有明确用户批准依据的成果继续保持APPROVED；旧QC PASS没有自动升级批准
- [ ] 已批准人物/场景/道具/变身/Storyboard/Video/Ending Frame优先继承，而不是为新版字段完整重做
- [ ] 已建立Retroactive Episode Asset Freeze；只补当前后续生产真正缺失的正式Master
- [ ] 旧APPROVED CONTINUITY_ENTRY Storyboard只有在真实Ending Frame出现P0/P1冲突时才做最小Continuity Recheck
- [ ] 已APPROVED Video没有重新做Video QC或重生成；缺Snapshot时优先补记录
- [ ] 尚未生成Video的旧FINAL VIDEO PROMPT只恢复有效Task/Director/World State意图，旧正文不Patch；已按当前Reference Routing + Execution State + Conflict/Shot Proof/Readiness Fresh Recompile
- [ ] 旧内容缺Reference Snapshot时先标MIGRATION REVIEW，没有整集直接判STALE
- [ ] Migration Result已经明确Inherited / Review / Stale / Missing Future-Critical Assets / Freeze / Current Segment / Next Action
- [ ] `Migration Status=COMPLETE`时仍核对`Migration Applied Skill Version`；版本不一致已执行`MIGRATION_DELTA_AUDIT`，没有因旧COMPLETE状态跳过当前路由/Prompt/队列清理


## Stage 03｜资产质检

### Director Spatial Reconciliation Gate
- [ ] 新Environment Canon Master + Geography一批准即先运行Pass A并得到`DIRECTOR GEOGRAPHY PRECHECK PASSED`；没有先批量生成依赖错误Shot Contract的Coverage / Shot Assembly
- [ ] Pass A已检查`Functional Zone / Sightline / Movement Lane / Camera Placement / Depth / Axis / Blocking / Critical Visual Read`；Coverage / Assembly完成后Pass B再次验证最终执行支持
- [ ] 若真实空间与Detailed Shot Contract冲突，只Patch受影响Director Shot并重算其Segment/资产依赖；没有无差别推倒整场
- [ ] 缺视角走`ASSET_COVERAGE_GAP`、缺静态多人关系走`SHOT_ASSEMBLY_GAP`、功能空间本体错误走`ENVIRONMENT_FUNCTIONAL_GEOGRAPHY_CONFLICT`；没有把导演冲突误诊成Video随机性
- [ ] 进入Episode Freeze前状态明确为`DIRECTOR SPATIAL RECONCILED`；首次/关键Transformation适用时同时为`TRANSFORMATION PRESENTATION RECONCILED`

### Personal Creator Cost Gate
- [ ] 已执行Static-First Stop Gate：静态图上可见的P0/P1身份、结构、空间、光照、Contact问题未被带去Stage 05“试试看”
- [ ] APPROVED Master只有局部错误时优先Local Patch并冻结正确区域，没有为小错误整张重生
- [ ] Local Patch / Inpaint已明确EDIT_TARGET与PATCH_DESIGN_AUTHORITY职责；存在正确局部图案/结构参考时没有只@母图
- [ ] 若QC结论是“修改当前失败Candidate”，Reference Pack已把该Candidate本身绑定为EDIT_TARGET / REVISION_SOURCE_IMAGE；没有只绑定Parent Master却声称在修改Candidate
- [ ] 每张Generation Reference都有明确Why Now / Authority Field / Most Direct理由；“同场景/同人物/母图更正式”没有被当成充分理由
- [ ] PATCH_DESIGN_AUTHORITY只控制Mask内Authorized Change，没有把其背景/构图/综合色/无关身份扩散到Base Master
- [ ] Mask外Frozen Region与Base Master一致；未出现脸/服装/背景/光照/数量等P0/P1漂移
- [ ] 没有Patch图片Authority时已明确`PATCH_DESIGN_AUTHORITY = TEXT-ONLY`，且文字目标唯一可执行
- [ ] Character / Environment Master保持Clean Input：身份/结构清楚，未把单场雨雾、战斗爆闪、临时综合色烤进长期Authority
- [ ] Environment / Prop均遵守Master First：先有一张APPROVED Canon Master + Structure/Geography Spec，再按Shot Coverage补衍生视图

- [ ] Stage 02标记`Required Ref = SUPPORT_REF / Owner Stage = 03`的项目已经生成对应Production Support Reference；没有把复杂交互/Contact/短暂高风险状态硬塞进普通Coverage
- [ ] Production Support Reference只承担被授权的Interaction / Contact / Transient State / Entity Action State / Mechanism Use Evidence；Identity / Canon Structure / Geography仍由正式对象Authority负责
- [ ] 低复用但当前Shot会清楚拿/递/操作的小物件可使用`LIGHTWEIGHT_INTERACTION_PROP_REF`，一次性关键Insert可使用`SHOT_DETAIL_REF`；如果它们重复跨Scene、承担因果关键或需长期结构一致，已升级正式Prop/Detail Authority，没有让Support长期冒充Canon
- [ ] 跨多个Shot/Segment持续的严重伤势、显著破损等没有长期冒充Support Ref，而是升级为正式Persistent State Variant；若后续Transformation Recovery修复伤势，该Injury Variant在恢复点正确终止/失效
- [ ] 同一个风险只有一个静态Owner；没有Coverage + State Variant + Support Ref重复建图互相冲突
- [ ] Required Stage 03 Support Ref已完成Fast Triage → Deep QC → 用户批准为`APPROVED SUPPORT`后才计入Episode Asset Freeze；`APPROVED SUPPORT`没有误写成`APPROVED CANON`
- [ ] Environment Coverage符合L1/L2/L3投资等级，新增视图能明确回指Triggered Shot并降低Blocking/反打/动作连续性风险，没有机械360°
- [ ] Prop没有默认生成正/背/侧/顶/底全套；只有真实Shot会清楚看到Master未覆盖结构/状态时才补Derived Coverage
- [ ] 每张Derived Coverage都有Parent Master + Triggered By Shot(s) + Why Master Is Insufficient，并且没有重设计Parent Master
- [ ] Character资产体系保持原有规则，没有被Coverage Engine误改
- [ ] 重复/复杂VFX只有在确实降低下游漂移时才建立Effect Reference，普通击打没有为“保险”新增资产


### Asset Anatomy Integrity（Current Rule）
- [ ] 只要当前正式资产 / Shot Assembly / 关键Anchor存在清楚可读手部，已执行`Hand / Limb Anatomy Integrity Gate`
- [ ] 已给可读手部分级：`HERO_HAND / FUNCTION_HAND / SECONDARY_HAND / BACKGROUND_HAND`；没有把前景叙事手按“背景小瑕疵”放过
- [ ] `HERO_HAND / FUNCTION_HAND`不存在明显手指数异常、指头粘连、掌面/拇指关系错误、关节链错误、腕部连接错误或透视断裂
- [ ] 持物/触碰/扶持/摸喉等接触真实成立；手部没有与道具或身体穿模、融合、悬空假接触
- [ ] 若整体图正确但手部局部错误，已优先Local Patch或切换无同类问题的Backup，而不是把明显手错直接PASS

### Foreground Figure Integrity（Current Rule）
- [ ] 只要当前正式资产 / Shot Assembly / 关键Anchor存在清楚可读的前景主脸、情绪脸、前景手或关键接触，已执行`Foreground Figure Integrity Gate`
- [ ] 已给前景可读脸部分级：`HERO_FACE / FUNCTION_FACE / SECONDARY_FACE / BACKGROUND_FACE`；没有把主脸问题按“整体氛围正确”放过
- [ ] `HERO_FACE / FUNCTION_FACE`不存在明显眼位漂移、嘴鼻错层、耳位离谱、脸部透视断裂或面部融化
- [ ] 关键接触（摸喉/抓领口/持伞/扶持/握把等）真实成立；不存在悬空假接触、穿模、磁吸式黏连或无因融合
- [ ] 前景局部没有明显黏连、复制块、局部透视崩坏；若只是局部错误，已优先Local Patch或切换无同类问题的Backup

### Revision / Inpaint / Wardrobe Visibility Integrity
- [ ] REVISE后复检已建立QC Scope Freeze Ledger；FROZEN_PASS、OPEN_REVISION_TARGET、REOPENED与Revision Surface清楚，没有无理由重审已冻结维度
- [ ] Web QC Evidence Priority按本轮OPEN/REOPENED维度动态选择；Render Style复检时Render Style Evidence已升级P0；Cinematic Shot Style复检只使用摄影语法Evidence；已冻结身份/结构未无意义占10图槽
- [ ] Multi-Pass复检每个Pass重复同一完整Candidate Group并绑定相同Object/Version/Candidate ID；没有PASS-A看A、PASS-B换B
- [ ] Local Patch已按Edit Target Type路由：Asset回Stage 03，Storyboard回Stage 04；没有把Storyboard Patch误送Asset QC
- [ ] Approved Ending Frame没有被Inpaint/PS后继续冒充真实Previous Ending Frame Authority
- [ ] Local Patch区分Mask / Dependent Integration Region / Frozen Region；Integration Fringe只修物理必然阴影/反光/遮挡/接缝，没有扩大重绘
- [ ] 同一结构在多视图/多分区重复出现时已建立Instance Map并同步修正全部应一致实例
- [ ] COAT_OFF/脱外套等若暴露此前从未定义的大面积内层结构，已触发Wardrobe Visibility Escalation并补最小Outfit Configuration Reference；Stage 04/05没有凭空设计


### 通用
- [ ] 当前Episode已读取完整Episode Asset Requirement Manifest，Stage 03按整集而不是按Segment零散生产正式资产
- [ ] 本集所有关键Character / Environment / Prop / Weapon / Transformation /必要Persistent State均已有有效APPROVED版本；Environment / Prop的当前Shot必要Coverage也已纳入Freeze
- [ ] 所有清楚可见的功能性/一次性人物需求都有Stage 02 `SCOPED_CAST_BRIEF`并已生成/深检/批准独立FMH/Minor Human Master（`APPROVED SCOPED FIGURE`）；Shot Assembly / PREVIS_HUMAN_ANCHOR / Mandatory白描只能继承该Appearance并控制关系、姿态、动作或Contact，不能替代人物母图。真正深背景不可辨认群众才允许TEXT_ONLY；不存在`FUNCTIONAL_MINOR_HUMAN_GAP`或`VIDEO_MODEL_GUESS`
- [ ] 每个主要/反复/可变身人物已建立`Character Asset Requirement Set`；DV-01 / DF-02 / HA-01的REUSE/TO BUILD状态明确，DF-01 / AD-01 / PR-01只在真实镜头需要时标Required
- [ ] Episode Freeze没有只凭“已有Character Master”放行；所有Required人物锁资产已真实QC + 用户APPROVED，无`CHARACTER_IDENTITY_LOCK_GAP / ADORNMENT_ASSET_GAP`
- [ ] Storyboard Grid / Storyboard Sheet与Previous-Segment Ending Frame没有被错误计入Episode Asset Pack
- [ ] 已完成Episode Asset Freeze Gate并在Workspace记录`EPISODE ASSET FROZEN`；Freeze前没有输出正式Storyboard Prompt
- [ ] Scene Pack只从冻结Episode Asset Pack抽取调用子集，没有因为某Scene资产先齐就绕过整集Freeze
- [ ] 每个正式人物/场景/道具/画风/色卡资产都有对应母图生成提示词
- [ ] Stage 03模型执行Prompt已通过Semantic Dedup：身份/结构/材质/画风/限制各有唯一Owner，没有在多个区块同义复述或正向+反向镜像重复
- [ ] 母图提示词明确“负责什么 / 不负责什么”
- [ ] 正式资产已登记稳定ID、版本与WIP（制作中）/ CURRENT（当前在用）/ APPROVED（已批准）/ DEPRECATED（已废弃）状态
- [ ] 用户/项目已有资产编号被保留，没有为了模板随意重命名
- [ ] DEPRECATED资产不会被下游误引用
- [ ] 下游按镜头职责调用必要资产，不是无脑附加全部参考图
- [ ] Stage 03图片Job已读取Image Candidate Strategy：Design-bearing Master默认2张、高风险可4张、Environment / Prop Coverage与Stage 03 Production Support默认2张；用户明确覆盖除外
- [ ] 同一图片Candidate Group共享同一个Task Contract / Canon / Style / Color / Aspect Ratio；没有把换脸、换设计、换场景几何的多个方案伪装成普通候选
- [ ] 多候选已先Fast Triage得到Primary / Backup，再对Primary做Deep QC；Primary失败时先检查Backup是否已解决同一问题，再决定Revision / Fresh Regen
- [ ] 只有最终QC PASS + 用户APPROVED的一张进入Registry / Freeze；Backup没有自动升级为正式Authority
- [ ] 图片候选数量与Video Take预算已隔离，不存在`CANDIDATE_POLICY_BLEED_FAIL`
- [ ] 用户上传新资产候选后已先执行Asset Intake自动绑定当前生产任务，没有要求重复填写可从Workspace推断的信息
- [ ] 正式APPROVED资产版本变化时已执行Change Impact，只把真实受影响项标记REVIEW / STALE，未整集无差别作废
- [ ] 用户批准正式图片资产后已触发Approved Asset Archiver：先确认Active Project Root和真实Source Path；执行Source exists/is_file/size/readable检查 → Copy-first → Target exists/is_file/size检查 → Source/Target SHA-256真实比对；全部PASS才允许ARCHIVED，否则ARCHIVE PENDING
- [ ] QC PASSED但尚未APPROVED的候选没有被错误写入approved目录
- [ ] 自动归档默认Copy-first，没有未经用户要求删除原候选
- [ ] 只更新Markdown/Registry不算归档成功；目标正式文件必须在文件系统中真实存在且大小>0
- [ ] SHA-256 PASS来自真实源文件和真实目标文件的字节计算，不是路径/文件名/UI引用的Hash

### 人物资产
- [ ] 人物资产使用项目统一资产语言（2×2人物页、脸部、表情/头发/变身结构等按实际需要）
- [ ] 人物身份/造型类Prompt已显式写明9:16竖向高分辨率画布；没有因为Style Board / Color Card的版式或Storyboard / Final Video是16:9而被错误覆盖
- [ ] `DV-01 / TF-01`虽然是2×2四视图，但整张Sheet真实保持9:16竖版；全身格从头顶到鞋底完整可读，脸部格仍有足够像素
- [ ] TE眼部/WP武器/TS时序等若使用非9:16，确实属于专项资产例外，并未反向污染人物Character Master比例
- [ ] 人物母图身份、年龄、骨相、发型、比例足够稳定
- [ ] 主要/反复人物已建立`Identity Distinction Card`，Face ID / Hair ID / Eye ID / Wardrobe ID / Adornment ID不是抽象“冷艳/温柔/帅气”标签，而是可见结构
- [ ] FRONT FACE能读出脸型、眉眼、鼻唇与Base Eye Identity；SIDE FACE能读出鼻唇侧面节奏、眼窝/眼线侧视与后脑体积；BACK能读出真实后发架构
- [ ] 与最相近现有角色比较后，不存在`CHARACTER_TEMPLATE_COLLISION_FAIL`：没有“同脸换发色”“同刘海换颜色”“同眼型换眼影”“同衣服换综合色”
- [ ] 主要/反复角色若DV-01不足以锁住脸/发身份，已补`DF-02 / HA-01`等现有身份资产，而不是只靠文字维持
- [ ] 人物母图生成前已完成Wardrobe & Environment Analysis（服装与环境适配分析）
- [ ] 当前剧情阶段完整服装已直接整合进人物母图，而不是无必要拆出独立Wardrobe Master（独立服装母图）
- [ ] 服装符合季节/天气/温度感/室内外/时间/场合/活动与角色身份
- [ ] 只有完整造型阶段变化才建立新人物母图版本
- [ ] COAT_OPEN / 轻微WET / DUSTY / LIGHT_BLOOD等短期变化没有被过度资产化
- [ ] 人物资产仍属于《断弦之歌》统一二维绘画语言，无摄影/3D/AAA风格漂移
- [ ] 临时分镜/尾帧/测试图没有反向替代正式人物身份或项目画风锚点
- [ ] 首次建档的新人物已读取New Character Generation Recipe，没有从零猜画风
- [ ] 新人物继承的是线条/皮肤/头发/渲染/综合色语言，而不是复制任何现有角色的脸、发型、服装和气质
- [ ] 日常人物保持20世纪晚期欧洲都市/地区现实服装基础与适度旧欧洲优雅感；法式都市简约只是可选子语言，没有把全员锁进同一法式长外套模板，也没有漂成戏服化历史造型/steampunk cosplay
- [ ] 人物保持动漫影响的角色设计吸引力与清楚轮廓，但眼型、眉眼力度、面部平面与气质服从各自Face/Eye ID；没有重新滑回“全员柔和大眼 / 同一种优雅漂亮脸”的模板
- [ ] 成年角色已完成Character Appeal设计：至少能说清Primary Appeal Hook、Body-Line Emphasis与Silhouette Hook
- [ ] 在没有明确剧情理由时，正式人物没有被默认“全包保守化”到几乎没有任何魅力焦点
- [ ] 女性角色没有机械套用同一种露肤模板；男性角色也没有全部收敛成高领长外套模板
- [ ] 若当前确为夜雨/夜外景，冷灰/蓝灰空气与局部暖实际灯源关系自然；若是白昼/雪原/医院/遗迹/暖室内等其他Scene，则已从Global Color DNA派生对应综合色，而不是强行套夜雨基线
- [ ] 综合色保持色族集中与功能层级，但没有被统一压成低彩度；肤色、材质、角色识别色与实际光源可按Scene自然显色，同时明度层级和主体分离清楚
- [ ] 新人物仍保持2D插画锁：无真人皮肤毛孔、无摄影感、无3D/AAA游戏脸、无照片级逐根毛发
- [ ] 中年/老年人物没有因为通用防写实负面词被错误年轻化；年龄通过二维骨相、姿态、少量绘画线条与发色正确表达


### CHARACTER IDENTITY DIFFERENTIATION GATE｜脸 / 眼 / 发反模板
- [ ] Face Identity Matrix已锁定Face Outline / Midface / Jaw / Chin / Nose / Mouth / Eye Spacing / Brow-Eye / Resting Expression / Distinctive Feature
- [ ] Hair Identity Architecture已锁定Far Silhouette / Part-Fringe / Face-framing / Side Volume / Back Mass / End Shape / Texture Grammar
- [ ] Eye Identity已区分基础眼型和变身眼部，不依赖颜色作为主要差异
- [ ] 遮住头发后仍能从脸部结构区分主要角色；遮住脸后仍能从发型剪影/服装轮廓大致区分
- [ ] 差异保持同一画风，没有为了“不同”把角色做成不同渲染体系或夸张畸形
- [ ] 主要/反复角色已完成Personal Adornment Opportunity Review；没有把“克制”机械执行成全员什么也不戴
- [ ] Signature Adornment若存在，其类别、位置、尺度、形状、材质、磨损/佩戴习惯与角色身份一致，不是随机首饰
- [ ] 装饰密度有主次，通常1个Primary + 0–1个Secondary；没有耳环/项链/戒指/手链机械全套堆叠
- [ ] 同场角色没有共享同一种细链/耳环/手表模板换颜色；INTENTIONAL_NONE有明确人物理由
- [ ] 稳定个人装饰在DV-01各角度与当前Look中位置一致；近景如需AD-01，Reference Field Coverage没有漏掉
- [ ] ROTATING角色已有Rotation Pool / Wear Conditions / Current Active Adornment / Current LOOK Binding；跨Scene没有随机换件
- [ ] 若AD-01被Stage 02判Required，它已在Episode Freeze前真实APPROVED；Current Look本身足够时没有机械重复生成AD-01
- [ ] 变身装饰的RETAIN / REMOVE(STOW) / ABSORB / TRANSLATE / REPLACE有合法World State去向；解除变身恢复Pre-Transformation Adornment Snapshot或已有剧情变化结果

### 圣谱者变身资产
- [ ] 只有剧情明确可变身的角色进入Transformation Asset流程；未确认角色没有被擅自添加礼服/音符瞳/武器/TS序列
- [ ] 变身设计先回答来源类型、人格状态、Accord模式、人格主题与剧情支持的Music Identity，没有为了“专业”擅自编造调性/曲名/作曲家
- [ ] 已建立Music Identity Card：Emotion Core / Personality Core / Music Direction / Rhythm Profile / Visual Grammar，并区分CANON与DERIVED
- [ ] 没有把“摇滚/悲伤/回忆”等音乐标签仅翻译成颜色；礼服、眼影、头发、瞳孔、音乐武器与动作节奏都有结构变化
- [ ] Transformation Beauty Core Five全部成立：礼服=惊艳、眼影=精致、头发=气场、瞳孔=身份、音乐武器=音乐与战斗实体
- [ ] Transformation Completion已记录Pre-Transformation Injury Snapshot / Recovery Eligibility / Post-Recovery Injury State；ELIGIBLE伤口在完整变身后不被强制继承，解除变身后也不回滚；旧衣物血迹/破损与环境痕迹没有被身体恢复误清零
- [ ] 已建立`Transformation Splendor Profile`：Large Silhouette / Medium Architecture / Small Detail / Material Contrast / Hair Splendor / Weapon-Body Silhouette / Focal Chroma-Light层级成立
- [ ] 缩到缩略图时仍有Large Scale Silhouette Hook，不是只有金线/裙片/小饰件变复杂
- [ ] 材质存在明确层级，不是整套同一暗色哑光布 + 少量金属边
- [ ] 与普通人物同框时Visual Level Gap明显；变身读起来是Visual Icon而不是“更复杂的日常服”
- [ ] 当前项目允许的大胆身体线条/暴露几何被有意识整合进角色结构，但没有替代Music Identity / Silhouette / Material层级
- [ ] 变身礼服已继承Normal Body Identity与角色Appeal，并单独选择Transformation Body Presentation Mode；礼服的负空间/框景/比例/材质/动态让人物身材美继续成立，不要求照搬Daily模式，也没有全员套同一束腰/深V/高开衩公式
- [ ] 音乐武器同时体现音乐结构/演奏动作/战斗功能，不是普通武器贴音符，也不是真实乐器直接加刀刃
- [ ] 变身前后先认得出是同一个人：脸型、年龄、眼型、发际线、身高体型为P0连续性
- [ ] `TF-01 / TE-03 / TH-01 / TC-01 / WP-01`作为Canonical Master Set管理，但下游没有机械五项全塞
- [ ] TE-01~05是同一双眼睛的状态系统；TE-04未新增设计，TE-05只表达剧情专属异常/成长状态
- [ ] 生成TF / TE前已建立Eye Signature Spec并对现有圣谱者执行Eye Signature Collision Check；资料不足时标记UNIQUENESS REVIEW PENDING，没有假装无撞型
- [ ] 日常Base Eye Identity至少有3项非颜色结构差异；变身眼部不靠“字段数量”证明独特，而是Primary Eye Signature / Secondary Graphic / Iris Architecture / Side-view组合与最相近圣谱者明显不同
- [ ] 变身眼部已执行`Musical Eye Motif System + Registry`：Eye Makeup Presence不是NONE，Primary Eye Signature清楚；MAIN/CORE有Secondary Graphic；Periocular Emblem最多0–1
- [ ] Music Identity通过LITERAL_NOTATION / DERIVED_MUSICAL_GLYPH / MUSICAL_GEOMETRY进入眼部；不强迫标准Notation，但Musical Origin Trace成立
- [ ] 眼部不是普通眼妆上贴一个音符，也没有因为字段过多出现`EYE_SIGNATURE_OVERDESIGN_FAIL`
- [ ] 不同圣谱者不存在“同一Primary/Secondary组合只换颜色、镜像、旋转或轻微移动”的模板复用
- [ ] 瞳孔符号像存在于虹膜内部，不是贴纸/LED灯泡；外部音符发饰/胸针不能替代真正瞳孔签名
- [ ] TF-01的FRONT FACE / SIDE FACE中Eye Signature真实可读；FRONT能看清瞳孔/眼影主结构，SIDE能看清眼线/眼影外眼角延伸；Prompt写了但图中看不清时不算执行
- [ ] 已有APPROVED TE-03时，它作为Eye Design Authority；TF修订、海报、分镜和视频没有擅自美化/弱化/通用化眼部结构
- [ ] TE-03已把Primary Eye Signature / Carrier / Placement / Translation / Geometry / Formation / Cross-Core Echo升为Canonical字段，批准后写入Musical Eye Motif Registry
- [ ] Storyboard / Video若眼妆达到可读程度，Reference Field Coverage把`TRANSFORMATION_EYE_SIGNATURE / MUSICAL_EYE_MOTIF`列为Critical，MCU/CU/ECU优先使用TE-03
- [ ] TH-01继承Normal Hair ID的发际线、分缝/刘海、Face-framing与主要后发轮廓；没有全员“长发舒展+发梢渐变+飘带”模板，也没有无理由暴增发量
- [ ] 变身礼服先有一句可记住的Costume Thesis，再有Primary / Secondary Costume Signature；不是从“暗黑哥特+金线”默认开始
- [ ] Style Family已主动选择；Dark Gothic只是可选之一，没有出现`STYLE_FAMILY_DEFAULT_COLLAPSE`
- [ ] 成年角色Boldness Dial可按人格进入ASSERTIVE / BOLD / EDITORIAL；身体线条、暴露几何、极端比例没有被“高级/克制”无理由压平
- [ ] Graphic Block / Negative Space通过Flat Color / Icon Test；华丽不依赖小纹样存活
- [ ] Material Contrast可以明显大胆，但主次清楚；不是整套暗色哑光布+少量旧金
- [ ] Music Identity至少改变Large Form / Medium Geometry / Material-Motion中的两层
- [ ] 正背裁片可连接，并允许跑动/转身/举臂/使用武器；功能修正没有磨掉Primary Costume Signature
- [ ] Accord Baton（圣约指挥棒）与Virtuoso Weapon（圣谱者武器）没有混淆
- [ ] Linked TS-01时序正确：共鸣触发 → 眼部/礼服启动 → 谱线推进 → 礼服完成 → 发梢完成/指挥棒生成 → 抛/交乐监 → 乐监接棒/节拍纹 → 武器生成 → 战斗状态锁定
- [ ] Solo分支无乐监接棒时，圣约指挥棒自行消散，未错误生成标准契约武器；角色专属例外必须有剧情/Approved Master依据
- [ ] TM-01 / FX-01仅在复杂且容易漂移时按需建立，没有为凑资产清单机械生成
- [ ] 普通Transformation FX没有被错误套用Threat Layer；只有敌对/污染/失控异常才使用威胁层视觉语言

### 场景资产
- [ ] 每个正式子空间先有一张高质量Environment Canon Master，空间几何、出入口、固定结构、尺度和主光方向清楚
- [ ] Hero Master批准后已有Geography / Blocking Spec；大型地点需要时已拆成可生产子环境
- [ ] Derived Coverage只由Shot Coverage触发；Reverse / Side / Door-side / Zone等多角度都回指同一Parent Master并属于同一空间
- [ ] 没有为了“完整设定”机械生成360°；L1在当前Shot静态歧义已LOW时停止扩图，但没有用“L1/理论可推断”掩盖真实高Video风险的Coverage或Production Support需求
- [ ] 关键地标与摄影轴线可识别
- [ ] 天气/时间Condition没有无必要变成新Environment identity（场景身份/地点本身）
- [ ] Environment State Variant（场景持久状态变体）只改变授权状态，没有重建空间
- [ ] 背景仍属于项目二维绘画体系，不是照片贴图/3D建筑渲染
- [ ] 前景人物/匿名功能人物与背景处于同一环境空间：接地、反射、透视、雨雾、光照交换、遮挡与景深统一，没有cutout / pasted / sticker-like前景分离

### 道具资产
- [ ] 道具先有一张正式高清Prop Canon Master，轮廓、比例、尺寸、材质、非对称识别点与功能结构清楚
- [ ] 人物持握/佩戴道具有Human Scale（人物比例参照）依据，并有必要Structure Spec
- [ ] 没有默认正/背/侧/顶/底全套；每张Derived Coverage都由真实Shot的Visible Side / Close-up / Interaction / State需求触发
- [ ] 功能部件、开合/折叠/展开逻辑稳定，Coverage View没有改变设计
- [ ] 文本类道具的物理结构与需要准确显示的文字内容分开管理
- [ ] Prop State Variant（道具持久状态变体）只用于持续/结构性状态，未为角度/短暂反光等制造冗余资产
- [ ] 道具没有随机新增零件、结构融化或武器类型漂移

### State / Color
- [ ] Global / Scene Color Card只管对应层级的综合色与光色，不承担清晰度、身份、几何或镜头构图职责
- [ ] 当前Scene已有Approved Scene Color Card，或存在Scene-matched视觉综合色基准时，场景绑定型资产已执行`SCENE COLOR AUTHORITY SCAN`；Scene Card或Color-Only Crop实际进入`MUST_BIND_COLOR_AUTHORITY`，不存在`SCENE_COLOR_AUTHORITY_REUSE_MISS / COLOR_AUTHORITY_BINDING_GAP`
- [ ] 复合综合色Reference即使含样例人物/车辆/场景，也不因类别自动退成文字；已有Approved Color-Only Crop且完整保留综合色关系时可优先用更窄的Color视觉Owner，否则按当前Direct Route与真实Leak证据裁决
- [ ] 当前Scene已明确使用Global基线或Scene Color Extension；新地点没有机械继承上一Scene综合色
- [ ] 只有反复使用/综合色差异显著/多镜漂移风险高时才生成正式Scene Color Extension Card；普通一次性变化使用文字Spec
- [ ] Shot Lighting Variant保持临时状态，没有无因升级为永久Environment identity
- [ ] 70/20/10若被使用，只作为全局综合色平衡启发，不按每个Shot面积机械执行
- [ ] 真正需要的Base Master（基础母图） → State Variant（持久状态变体）正确继承身份/几何
- [ ] 审核通过的Canon Master与必要Derived Coverage已登记；Stage 04/05按Task选择最直接Approved HD Object Authority，不重新设计，也不机械附加Parent Master

- [ ] 若存在VFX_REFERENCE_REQUIRED，Effect Reference只锁标志性VFX的Source / Geometry / Contact / Environment / Decay，不替代角色/武器/场景Master，也不预画Storyboard

- [ ] 若Stage 03候选交给网页版多模态Verifier，已执行`WEB_MULTIMODAL_IMAGE_CAP = 10`；单批Candidates + Authorities总图数≤10，超过已自动拆B01/B02且同一资产候选组未无理由拆散
- [ ] Web Asset QC每个Batch的@图编号都按本批实际上传顺序从@图1重新编号，没有出现@图11或跨批沿用图号
- [ ] 若候选带`Dola AI`或`豆包AI生成`免费额度平台水印，QC已按`QC_NEUTRAL_ALLOWED_PLATFORM_WATERMARK`忽略水印本体，没有记P0/P1/P2、Candidate降级或返工目标；只有真实遮挡关键证据时才记Evidence Occlusion

## Stage 04｜分镜 QC

### White-line Storyboard Universal Gate
- [ ] 当前Segment的**每一个正式Shot**都在`SHOT_STATE.storyboard.mandatory_panel_asset_ids`中有明确白描Panel计划；T19时每张计划Panel都有真实Selected Candidate并达到`QC_PASS_WAITING_APPROVAL`，T20后同一Panel Fingerprint已被用户Approval Record覆盖并Promote为Approved；没有任何Shot用彩色精修图、Hero/Keyframe、Shot Execution Frame、Spatial Map或Camera Path顶替Baseline
- [ ] Mandatory Baseline全部满足`STORYBOARD_RENDER_MODE = WHITE_LINE_STORYBOARD_ONLY`；需要更高身份/材质信息时只追加Rendered Human Anchor/Video Conditioning，不反向替代白描分镜
- [ ] Mandatory白描Panel只继承Scene Color的Value/Lighting血缘：`projection_mode=VALUE_LIGHTING_LINEAGE_ONLY`且没有综合色`COLOR_AUTHORITY` Direct Binding/@色卡；综合色相从Shot Execution/Video Conditioning阶段恢复
- [ ] 所有Storyboard Panel像素内无任何文字、数字、Shot/Panel ID、时间码、CUT、Camera术语、箭头、运动轨迹线、说明框、气泡、字幕或Logo（不可避免平台水印仅按既有QC例外处理）
- [ ] 宫格/Sequence Board只由同一批白描Clean Panels确定性拼版：用户审阅版可由`QC_PASS_WAITING_APPROVAL` Panels组成，最终版只引用Approved Panels；图像模型没有直接生成Storyboard Grid/Page，也没有在图内加入文字、编号或箭头
- [ ] Camera Motion / Timing / Cut-NoCut / Action Beat / Performance / Eyeline / Shot Relation / Landing等离图说明已进入`VIDEO_EXECUTION_PLAN.storyboard_handoff`；每个REQUIRED项的`prompt_anchor`在Final Video Prompt中真实出现，不以泛关键词替代；不存在`STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP`

### Director Contract Inheritance Gate
- [ ] Storyboard生成前已读取`DIRECTOR SPATIAL RECONCILED`的Detailed Shot Contract，而不是仅凭剧本/基础景别重新导演
- [ ] Focus Owner / Critical Visual Read / Shot Size / Screen Occupancy / Inter-character Distance / FG-MG-BG / Overlap-Crop / Entry/Landing Camera Geometry / Lens Family / Focus Plan / Stabilization / Axis / Screen Direction / Eyeline均按Stage 02执行
- [ ] Storyboard没有为了“所有人物都看清”自动把前中后景压平、取消合理遮挡/裁切或把多人排成同一横线
- [ ] Stage 02 Camera Intent得到继承；Stage 04只精化具体Path/Landing，不无因改变核心Camera关系
- [ ] 每个CUT能追溯到Stage 02 Cut Motivation；没有机械一句台词一次正反打
- [ ] Combat Shot保持Engagement Distance Ladder / Attack Lane / Contact Read / Initiative Shift Visual；不存在`COMBAT_LINEUP_FAIL`
- [ ] Montage保持Stage 02 Montage Design Brief的信息递进与连接原则，不退化成地点PPT
- [ ] 首次/关键Transformation保持Presentation Contract与Splendor Reveal Priority；没有用平视全身站立消解变身视觉等级
- [ ] 若Storyboard必须改变核心Blocking / Distance / Axis / Camera Intent才能成立，已标`DIRECTOR SHOT CONTRACT CONFLICT`回Stage 02最小Patch，而不是在Stage 04静默重设计

### Storyboard Revision / Web QC Integrity
- [ ] Storyboard Revision只重新检查受影响Panel/Continuity/Action/Performance；上一轮FROZEN_PASS维度未被个人审美重新推翻
- [ ] 网页Storyboard QC使用`web_asset_storyboard_qc_handoff.md`固定Schema，直接给N/10、上传顺序、完整Copy Prompt和`WEB_STORYBOARD_QC_RESULT`返回格式
- [ ] Storyboard / Previs若带`Dola AI`或`豆包AI生成`平台水印，不因水印本体判质量失败、文字/Logo污染或要求返工；水印遮挡关键Proof Evidence时才按Evidence Occlusion处理
- [ ] Storyboard局部Patch仍属于Stage 04；Reference职责区分EDIT_TARGET / PATCH_DESIGN / Character / Environment / Ending Frame
- [ ] 音乐机制承担叙事时已建立Planned Visual Beat Map，关键Panel标记Phrase Start / Hold / Protected Sync Point / Major Contact / Cadence，不靠画音符解释

- [ ] Episode Asset Pack已冻结；Storyboard只调用冻结资产，不重新设计人物身份、正式服装、场景几何、道具/武器结构
- [ ] Storyboard生成前已建立Key Visible Asset Register / Reference Field Coverage Map；当前会清楚入镜的主要人物、当前Environment方向、关键Prop / Weapon / Vehicle / Entity / Persistent State均有对应Approved视觉Authority
- [ ] 没有为了让@图数量更少而删掉关键可见资产；多张Reference只要承担不同Critical Field就是合法的
- [ ] 若多人关系/人物进入功能空间/人景物组合需要Approved Shot Assembly，已正确使用`HD_SHOT_ASSEMBLY_IMAGE`；Assembly没有被误当作万能Identity / Structure Authority
- [ ] 任一Critical Field缺失时已触发`REFERENCE_COVERAGE_GAP`并回Stage 03补齐，而不是靠Storyboard文字临时发明
- [ ] Stage 04 Storyboard Prompt已通过Semantic Dedup Hard Gate：内部Performance / Action Feasibility / Natural Motion / Crowd / Combat分析已并入对应Panel的Integrated Execution，没有独立长块复述
- [ ] 若Storyboard阶段发现真实正式资产缺口，已标记`EPISODE ASSET FREEZE BROKEN`并回Stage 03补齐，而不是用Storyboard临时补设定
- [ ] **每一个Panel内部都是最终成片16:9构图；整张Storyboard Sheet（分镜整页）不被错误强制成16:9**
- [ ] 相邻画格动作可以自然连接；姿态差异明显时已建立Motion Corridor，不依赖Pose A→Pose B最短插值
- [ ] 起停/坐站/大转身/Reach等关键动作有必要Functional Preparation与整个人体Kinetic Chain；大转身不存在脚底滑轮式旋转
- [ ] 可安全叠接的动作没有被机械拆成“做完A停一下再做B”；关节路径与动作幅度符合人物/景别
- [ ] 每一格都有明确的信息增量（动作 / 情绪 / 空间 / 摄影机 / 连续性 / 叙事至少一项）
- [ ] 删除某格若不影响执行与理解，则已合并/删除，而非凑格数
- [ ] 人物左右关系正确，无意外镜像
- [ ] 摄影轴线稳定，除非明确设计越轴
- [ ] 重心变化与动作动力学合理
- [ ] 已执行Action Feasibility Quick Check：新动作使用的手/脚当前可用，没有同一肢体互斥占用
- [ ] Held Prop / Body Load / Inter-character Support在动作前后都有连续支撑来源，没有“角色手离开后物体悬空”
- [ ] 换手/放下/拾取/交接存在合法Transfer或接触链；必要时Storyboard能读出Micro Bridge
- [ ] Touch/Grab/Sit/Stand/Step/Kick等动作具备Approach / Reach / Contact / Grip / Weight Shift等必要前置条件
- [ ] Ongoing Physical Task明确CONTINUE / SLOW / INTERRUPT / COMPLETE / TRANSFER / ABANDON，没有因新表演动作自动清零
- [ ] 复杂动作Exit明确下一Panel所需的肢体、道具、支撑、接触和姿态状态；不存在`ACTION_FEASIBILITY_FAIL`
- [ ] 人物表演能追溯到当前Objective / Obstacle / Tactic / Stimulus，不是独立拼表情清单
- [ ] 人物表情/眼神确实随演员行动与信息变化而变化
- [ ] 重要情绪不是只写“害怕/震惊/关心”等抽象词，而是先有Objective / Tactic / Trigger，再有Intensity / Visible Signals / Suppression / Timing
- [ ] 表演细节与景别可见性匹配；远景把心理信息转译为重心/步伐/距离/身体方向，而不是直接删掉心理信息或堆不可见微表情
- [ ] 1–3项微动作规则被正确理解为主要Emotional Carrier，不是机械删除所有次级身体后续
- [ ] 有意义的Involuntary Leak + Controlled Response得到保留，只有真正物理执行冲突被修正
- [ ] 关键表演不是纯姿势切换
- [ ] 对话场景的Active Listening自然：已知信息可以维持状态，真正改变判断的刺激才推进反应；未说话人物没有无因冻结
- [ ] 有明确Trigger / 注意力落点 / 后续行动的Triggered Stillness被当成有效表演，没有为了“不能冻结”强行加动作；Listener也没有抢走说话者焦点
- [ ] 含明显Crowd的Storyboard已附`Crowd Motion Intent`；静态Panel只锁Blocking，没有把背景人物姿势误当成整段Video静止Authority
- [ ] Crowd Cluster的持续任务、主流Flow和Attention Baseline清楚；前景对白不会让背景整片Pause
- [ ] Background Activity强度低于Foreground Narrative Priority；没有为了防冻结让所有背景人高频乱动抢戏
- [ ] 强Stimulus时Crowd Reaction按近场→中场→外围不均匀传播，没有同步广播式群体反应
- [ ] 重要日常对白存在潜台词/Speech-Body Coupling：回答速度、停顿原因、视线、原任务动作或声音至少有必要的具体联系
- [ ] 多句对白按Objective / Tactic / Thought Intention与Speech Phrase连续表演；句号没有自动触发表情/姿态归零或Recovery
- [ ] 句与句之间存在Body Continuity / Continuity Bridge（原任务、视线、姿态、表情状态或对听者的观察至少一项持续）
- [ ] Breath=IMPLICIT时Storyboard/Video指令不把普通呼吸当主要可见动作；只有明确情绪/疲劳/疼痛/受击等原因时才升级为可见换气信号
- [ ] 有需要时包含反应镜头/插入特写/环境镜头
- [ ] 没有连续大量同构图双人站桩中景
- [ ] 道具结构与位置稳定
- [ ] 攻击/互动路线清楚
- [ ] 场景结构没有漂移
- [ ] Entry Mode执行正确：CONTINUITY_ENTRY时上一段尾帧能自然接入；CUT_ENTRY / SCENE_OPENING不强求上一尾帧；本段Exit仍为后续连续性提供可用状态
- [ ] Storyboard已执行当前World State Transition Ref：即使是CUT_ENTRY / SCENE_OPENING，也没有无因重置Prop / Injury / Wetness / Knowledge / Environment Runtime / Objective等语义状态；若Transformation Recovery已合法改变Injury，则Storyboard使用新状态而非旧伤
- [ ] 已明确哪些画格属于同一连续Shot，哪些位置执行CUT / Match Cut
- [ ] T3/T4或存在歧义的摄影已建立Cinematography Grammar；复杂运镜另有Camera Motion Contract，明确Pan/Truck、Dolly/Zoom、Tilt/Crane的物理区别、Motion Curve、视差与Landing；Storyboard证明场地/焦点有条件完成
- [ ] 宫格参考不会污染正式成片画质
- [ ] Reference Resolver只选择本Segment真正需要的参考图，没有Reference Overload（参考图过载）
- [ ] Storyboard实际使用的Reference Pack已保存资产ID / 版本 / 职责到Workspace；对应Storyboard获批后冻结为Reference Pack Snapshot
- [ ] Stage 04开始前Episode Workspace已为`EPISODE ASSET FROZEN`；若为CONTINUITY_ENTRY且上一Segment真实Approved Ending Frame尚未产生，本段保持`WAITING PREVIOUS ENDING FRAME`，没有提前生成正式Storyboard
- [ ] CONTINUITY_ENTRY正式Storyboard使用真实上一段APPROVED Ending Frame；没有用计划Exit或上一Storyboard尾格冒充；若上游Ending Frame后来变化，才执行Continuity Recheck并只修必要开头
- [ ] 当前Segment的Detailed Shot Contract中**每个Shot**都已由`CLEAN_STRUCTURAL_STORYBOARD`或`CLEAN_STORYBOARD_BOARD`至少一个Panel覆盖；无`SHOT_STORYBOARD_COVERAGE_GAP`
- [ ] Multi-shot Segment的真实CUT/Match Cut在Board中明确；Long Take的多Panel没有被误标成多Shot/假CUT
- [ ] Hero Frame / Keyframe Pair / Spatial Map / Camera Path / Contact Chain只作为Supplemental Evidence，没有单独冒充Mandatory Storyboard
- [ ] 不机械固定4/6/9格，但任何Shot都没有因“简单”被跳过
- [ ] Storyboard审批顺序正确：先全部Panel真实生成+Visual QC=`QC_PASS_WAITING_APPROVAL` → 确定性拼Review Board → 用户批准Storyboard Set → Approval Record记录全部Mandatory Panel IDs/Fingerprints → Jobs Promotion；不存在先Promotion再让用户批准的双审批/倒序审批
- [ ] Approved Storyboard只有真实Source Path解析、Copy、Target后置验证与Source/Target SHA-256全部PASS后才标ARCHIVED；否则明确ARCHIVE PENDING
- [ ] Stage 04实际图片输入与Semantic Role一一对应，没有绑定错图；精确映射保存在Executor Input Map
- [ ] Stage 04 Generation Prompt已通过Surface Sanitizer：没有Reference职责表、文件名、Raw Asset ID/Version/Path、`TASK_SHELL / INPUT_LABEL / OUTPUT_ADMIN_SHELL`或内部Authority/MUST_BIND解释；平台确需原生Token时仅保留真实Token + 最短执行句；Web QC动态@图号是独立QC例外；`SURFACE_LINT_REPORT`全部为0
- [ ] Stage 04当前Scene的Director Decision Card + Sequence Arc有效；Previs/Storyboard没有改变Segment-scope Audience Alignment / Reveal / Reaction Give-Deny / Key Hold-Cut，且不存在`DIRECTOR_INVARIANT_EXECUTION_FAIL`
- [ ] Reference Budget已区分MUST / CONDITIONAL / TEXT-ONLY；没有为了“多参考更保险”造成Reference Overload
- [ ] 连续性差异已按P0 Must Match / P1 Should Match / P2 May Vary判断；P2差异没有单独触发返工
- [ ] QC失败时已先做Failure Diagnosis，没有无理由整条Prompt重写
- [ ] 同一Scene多个Storyboard可批量生成/批量QC时，没有无意义逐个往返
- [ ] 普通Storyboard默认1张；多人/战斗/复杂Blocking/复杂Camera等高风险Storyboard可按Image Candidate Strategy计划2张
- [ ] 多个Storyboard候选已先做Candidate Triage，生产正确性优先于单纯“最好看”

- [ ] 每个Video Unit已有最小Primary Conditioning；只有高风险/复杂状态变化才额外增加`VIDEO_CONDITIONING_KEYFRAME`，普通Shot不机械增加额外帧
- [ ] Additional Video Conditioning Keyframe严格继承Approved Storyboard Camera / Blocking与当前Approved Object Authorities，不重设计人物/衣服/道具/场景，不改变World State
- [ ] Additional Video Conditioning Keyframe若前景人物脸/手/关键接触清楚可读，已通过Asset Anatomy + Foreground Figure Integrity；明显硬伤不得标`APPROVED_VIDEO_CONDITIONING`
- [ ] 额外Video Conditioning Keyframe候选数按风险决定；通过后状态为`APPROVED_VIDEO_CONDITIONING`，不是Canon
- [ ] Video Conditioning发生在Approved Clean Storyboard之后；其批准是进入Final Video的硬前置，Stage 03只负责提前登记策略。

### Combat Storyboard补充（适用时）
- [ ] 已明确Narrative Goal / Victory Condition / Combat Archetype，不是为了“有战斗”机械互殴
- [ ] Combat Conflict Audit无未解决HARD_CONFLICT；小说单次动作没有被自动升级为长期Canon
- [ ] 有效距离、攻击线、重心、接触点与主动权在画格中可读
- [ ] 攻防以Combat Exchange组织，不是A/B轮流出招
- [ ] 不同武器保留不同Measure / Geometry / Defense Grammar
- [ ] 紧张感来自危险接近、停顿、Commitment与后果，不是全程高速抖镜
- [ ] 多人战有Focus Owner / Threat Priority / Role / Spatial Lane，不排队出招
- [ ] Combat Performance与攻防因果耦合，主要角色没有在连续Exchange中变成扑克脸；表情/呼吸/视线由Read / Threat / Contact / Relationship触发
- [ ] 已区分Execution Consequence与Lore Cost：动作后摇/惯性/站位暴露可推导；圣约反噬/寿命/新伤势等长期代价未凭空发明
- [ ] 已确认Cost / Injury若影响战斗，优先用可见性能变化表达；未凭空发明代价
- [ ] 若Storyboard覆盖战斗解除，Weapon + Costume + Accord Baton同步消散

- [ ] 若Storyboard交给网页版多模态Verifier，单个Web QC Batch总图片数≤10；跨Batch共享Authority需要时已重复上传并重新编号
- [ ] Storyboard Web QC Copy Prompt没有引用本批未上传图片；若单个Storyboard所需P0 Evidence>10已采用Multi-Pass而不是随机丢Authority

## Stage 05｜视频 QC

### Current｜Video Generation Constraint Preflight
- [ ] Final Prompt自然语言成稿前已有`VIDEO_EXECUTION_STATE`；多人/空间交互等触发条件成立时同时有`SPATIAL_EXECUTION_STATE`，Camera/Audio/Reference/Action/Spatial字段均单一Owner
- [ ] `PROMPT CONFLICT PREFLIGHT` Hard Conflict Count = 0，Spatial Position/Trajectory/Relation/Target/Owner冲突均为0
- [ ] Native @Token已通过Content-Role Verification；没有“图2控人物但图2没人”
- [ ] WORLD_POPULATION与FRAME_VISIBLE_POPULATION分开，没有人数语义冲突
- [ ] Shot Proof Capacity证明所有P0 Critical Read在当前景别可辨；Micro Object P0/P1已证明Legibility
- [ ] Motion Load没有OVERLOAD；P2精确计数/装饰动作没有挤占主要动作
- [ ] Camera每个时间窗只有一个状态，无“静止或轻推”分支
- [ ] Entry/Landing Camera Geometry、Lens Family、DOF、Stabilization与Camera Timeline单一Owner；PAN/TILT/CRANE/ARC造成的合法Geometry Change已写入Timeline，没有把Entry Geometry错误冻结全段
- [ ] `STATIC`没有同时Zoom / Geometry Change；`LOCKED_OFF`没有同时Pan/Tilt/Dolly/Truck/Crane/Arc/Follow
- [ ] RACK / TRANSFER Focus有两个不同且可辨识的Start/Landing目标与叙事Trigger；没有装饰性随机拉焦
- [ ] Audio使用Typed State，无`Breath ON + All Human Sound OFF`父子冲突
- [ ] Generation Contract与QC Contract分离；Final Prompt没有`成片必须满足 / 自检 / QC检查 / PASS条件`复读块
- [ ] `VIDEO_GENERATION_READY`只允许进入Compiler；真正交付前Final Candidate已通过`POST_COMPILE_CONSTRAINT_CLOSURE`，New Constraint / Missing MODEL_TEXT / State Contradiction / Ambiguous Exclusive / Multi-owner全部=0


### Continuity Authenticity / Visual Beat Integrity
- [ ] Previous Ending Frame只来自对应APPROVED Video真实稳定帧；没有使用生成/修补/美化后的假尾帧作为Continuity Authority
- [ ] 上游Approved Storyboard / Ending Frame / Music Motion Authority换版后已执行Change Impact；未生成的旧Final Video Prompt若受影响已标STALE并最小重编
- [ ] 音乐化战斗/变身/关键Hit在Video批准后从真实Take记录Visual Beat Timestamp Map；计划时间没有冒充实际时间
- [ ] Stage 05仍NO AUTO BGM；Visual Beat Map只记录动作时间结构，不要求视频模型自动生成正式配乐

- [ ] 输入关系符合新主链：本段必要正式资产来自冻结Episode Asset Pack；`APPROVED MANDATORY SHOT STORYBOARD`覆盖当前Segment全部Shot；Supplemental Previs按需；CONTINUITY_ENTRY使用真实上一段APPROVED Ending Frame，CUT_ENTRY / SCENE_OPENING未强行绑定尾帧
- [ ] Final Video前已建立Key Visible Asset Register / Reference Field Coverage Map；当前镜头清楚可读的主要人物、Environment方向、关键Prop / Weapon / Vehicle / Entity / Persistent State全部Covered=YES
- [ ] PERSONAL_ADORNMENT为Critical时：Current Look足够则不重复加AD-01；不足且有Approved AD-01则AD-01=MUST；不足且无AD-01则已阻止Storyboard/Video并回Stage 03补图
- [ ] Reference Pack执行`Minimum Sufficient`而不是“最少图”：关键资产多时允许多图输入；只删除同字段真实冗余Reference
- [ ] 若使用Approved `SHOT_ASSEMBLY_ASSET`，它只承载多人关系/人景物组装/空间占位；清楚可见的一次性`SCOPED_CAST / NON_RECURRING`外观仍由独立Approved FMH/Minor Human Master承担，Assembly不得成为人物Identity/Appearance Authority；正式角色Identity、道具结构、场景Geometry继续由对应HD Object Authority承担
- [ ] 无未解决`SHOT_ASSEMBLY_GAP / SHOT_ASSEMBLY_AUTHORITY_FAIL`
- [ ] 槽位压力没有通过静默删关键图解决；已先去冗余、TEXT_CONTROL、Assembly/Anchor重组，仍超限则标`REFERENCE_SLOT_OVERFLOW`并回上游处理
- [ ] 宫格画格被正确理解为视觉锚点，没有机械地一格切一次镜头
- [ ] Segment内部Shot级时间轴与分镜批准的连续/切镜关系一致
- [ ] 模型要求执行的CUT / Match Cut出现在正确时间点，切前切后构图正确
- [ ] 连续Shot内部没有用变形、甩镜、突然变焦或瞬移伪装切镜
- [ ] 身份、五官、发型、服装稳定
- [ ] 人物没有复制
- [ ] 左右/朝向/摄影轴线正确
- [ ] FINAL VIDEO PROMPT编译前已通过Director Invariant Preflight；Decision Card + Sequence Arc + Approved Previs的Segment-scope Invariants一致，不存在`DIRECTOR_INVARIANT_EXECUTION_FAIL / DIRECTOR_COMPROMISE_PROPAGATION_GAP`
- [ ] FINAL VIDEO PROMPT在编译前通过Action Feasibility Hard Gate；不存在未解决`ACTION_FEASIBILITY_FAIL`
- [ ] FINAL VIDEO PROMPT在Action Feasibility后通过Natural Motion Hard Gate；不存在未解决`NATURAL_MOTION_FAIL`，明显姿态变化已有可执行Motion Corridor
- [ ] 每个关键Held Prop都有持续Support；角色腾出持物手前已经换手/放下/交接，或明确剧情性Drop
- [ ] 新动作使用的具体肢体与当前Occupancy一致；空闲手可解决时没有让持物手无因离开
- [ ] 接触/抓取/坐站/迈步/踢击/转身具备必要Approach、Grip/Release、Weight Shift与空间可达性
- [ ] Ongoing Physical Task在新动作中继续、减速、中断、完成或转交均有明确结果，不会被模型当作Reset
- [ ] Action Exit锁定相关手、Prop、Support、Contact和姿态，使下一Beat不会随机重新摆位
- [ ] 动作先后符合提示词
- [ ] 重心、受力、惯性、接触可信
- [ ] 战斗/追逐Segment的Victory Condition被动作贯彻；Micro-objective清楚
- [ ] 有效距离没有跳跃或瞬移，Initiative交换有因果
- [ ] 攻防不是轮流播动作，至少一个Combat Exchange能读出Setup→Threat→Defense→Contact/Near Miss→Counter/Recovery
- [ ] 武器接触没有漂浮/磁吸；重击有准备、传力、回弹与Secondary Motion，不只靠Camera Shake
- [ ] Skill Interaction存在Counterplay，没有默认对波/爆炸解决
- [ ] Music Identity真正改变Timing / Footwork / Weapon Kinetics / Recovery / Tactical Timing；不同角色不是同动作只换VFX颜色
- [ ] 可见音乐符号只在Canon/Approved Asset已确认且承担机制时使用，没有满屏随机音符/五线谱/魔法阵
- [ ] 重要Contact明确武器/身体接触位置与Force Direction；目标反应沿接触点→主体质量→重心/支撑传播，不是无因整体飞走
- [ ] Heavy/Massive Impact有Compression / Force Propagation / Recoil / Secondary Motion / Environment Proof / Aftermath，不靠随机Camera Shake
- [ ] Near Miss也产生合理的重心、气流/雨雾/材质或Recovery后果
- [ ] VFX存在Cause / Source / Formation / Spatial Geometry / Environment Interaction / Contact / Lighting / Decay；遮挡和透视正确，不像后期贴图
- [ ] Environment Proof优先使用雨、雾、灰尘、水面、幕布、金属/玻璃/冰等真实介质；没有为“华丽”无因增加粒子暴风
- [ ] 重要Exchange结束形成New Combat State；Distance / Initiative / Weapon / Damage / Persistent Field没有在下个Segment自动重置
- [ ] 已确认Cost / Injury在动作性能中可见；未新增未经Story/Canon支持的伤势
- [ ] 多人战没有排队攻击或背景角色等待“回合”
- [ ] Camera没有遮住关键攻击线、接触点和方向变化
- [ ] 若本Segment覆盖战斗结束，Virtuoso Weapon + Transformation Costume + Accord Baton同步消散
- [ ] 手部与道具没有穿模或结构融合
- [ ] 表演能读出角色当前Objective / Tactic / Listening变化，并通过眼神、原任务、声音、面部或空间关系具体落地，不是木偶式pose变化
- [ ] 模型Prompt没有用抽象情绪词代替演员行动；关键表演能看出Objective / Tactic / Trigger / Visible Signal / Suppression / Landing
- [ ] 有心理意义的微动作没有为了“模型稳定”被直接删掉；过密信息通过合并/排序/分时/景别转译处理
- [ ] 战斗中的Performance与Read / Threat / Contact / Recovery同步发生，主要角色不是动作正确但面无表情
- [ ] 对白人物保持Actor/Thought Continuity：同一Objective / Tactic下没有“每句结束就Recovery/重启”的循环
- [ ] Speech Phrase按语义、语速、情绪和真实换气需要组织，不是按标点机械切段
- [ ] Breath=IMPLICIT时最终Prompt主要通过持续姿态/任务/语流表达自然连续性，没有反复点名胸口/肩线呼吸；成片也没有周期性胸口泵动
- [ ] 若呼吸成为Visible Signal，能读出Cause / Degree / Timing / Recovery，而不是泛化的大幅胸口起伏
- [ ] Listener Flow按意义变化推进；未说话角色不无因待机，也不逐句点头/眨眼“打卡”；有因Triggered Stillness可成立
- [ ] 含明显背景群体时FINAL VIDEO PROMPT已通过Crowd Presence Hard Gate；不存在未解决`CROWD_PRESENCE_FAIL`
- [ ] 背景群体在前景对白/表演期间保持低强度、异步的生活连续性，没有整片变成截图；合法静止有任务/注意力原因
- [ ] Crowd Attention符合可感知信息范围；没有因主角叙事重要性让所有群众无因盯向主角
- [ ] 群体动作没有明显同步循环、同Pose复制或统一起步/转头；远景不要求逐人精细表演
- [ ] 强Stimulus后的Crowd Reaction存在距离/可见性/社交传播差异，而不是所有人零延迟同步反应
- [ ] Crowd Density / Cluster / Primary Flow / 撤离或聚集状态没有在CUT / Segment后无因Reset
- [ ] Background Activity没有抢过前景Actor；若背景过强已先降Amplitude/Reaction Level而不是重写主角Performance
- [ ] 运镜与人物动作的启动时机自然
- [ ] 复杂/歧义Camera遵守Cinematography Grammar + Camera Motion Contract：Height/View/Lens/Focus/Stabilization、物理路径、轴线、Focal Behavior、Motion Curve、视差、启动与Landing正确，没有把Dolly误成Zoom、Pan误成Truck、Tilt误成Crane或把Handheld当运动类型
- [ ] 没有无意义自动切镜或360°环绕
- [ ] 场景、道具、光线没有明显漂移
- [ ] Video没有把Segment/Scene边界当作世界刷新点：人物进出、Motion/Arrival、Prop去向、伤势/湿度、环境破坏、Knowledge与Ongoing Task均符合World State Ledger / Transition Audit；变身完成后若Recovery=RECOVERED，Video不保留旧开放伤口，也不在解除变身后让旧伤复现
- [ ] Segment尾帧稳定，可直接提取为下一段的连续性尾帧
- [ ] 分镜/尾帧的黑白、线稿、模糊、低细节没有污染正式画面
- [ ] Approved Storyboard已明确标记为Storyboard Authority / NOT a render-quality reference，只控制Shot、构图、动作节点与CUT关系
- [ ] 若本Segment实际使用Previous Ending Frame，它已明确标记为Continuity Authority / NOT a render-quality reference，只控制起始站位、朝向、轴线、动作阶段、重心与道具状态
- [ ] 已通过Reference Completeness + Fidelity Firewall（无`REFERENCE_COVERAGE_GAP / REFERENCE_SLOT_OVERFLOW / REFERENCE_FIDELITY_FAIL`）；Reference Pack中每张图都有Input Mode，低清控制图没有被当成`HD_OBJECT_AUTHORITY_IMAGE`，当前Shot已有匹配Environment / Prop Coverage时未无理由退回泛化Parent Master
- [ ] 已通过Visual Style Authority Gate（无`VISUAL_STYLE_AUTHORITY_FAIL`）：Render Style与Cinematic Shot Style职责分离，后者没有覆盖具体Storyboard
- [ ] 已通过Adaptive Color Derivation Gate（无`COLOR_DERIVATION_FAIL`）：当前综合色层级明确，新Scene未被旧Scene色卡锁死，且没有无必要同时上传Global / Scene / Shot三层综合色图
- [ ] 当前Final Video若有Approved Scene Color Authority，综合色视觉控制没有丢失；Color Card/Crop可按Capability Route直接绑定，只有Direct Fail、已观察Literalization、已证明槽位冲突、用户明确要求，或`ROLE_SEPARATION=VERIFIED_FAIL`且无安全Color-Only Crop / Dedicated Channel时才改Applied Reference
- [ ] 综合色视觉绑定只控制综合色/光色；没有越权改人物Identity、场景Geometry、Storyboard Camera
- [ ] Approved Storyboard被作为真正视觉控制使用：平台支持Board则可整板，支持多图则用关键Panel；没有因为担心宫格而把关键动作/构图全部退成文字
- [ ] 被OMIT的综合色卡/整板/人群档案若仍含当前镜头必要信息，已完成`ROUTE CHANGE → PRESERVE REQUIRED FIELDS`，没有发生`REFERENCE_FIELD_PRESERVATION_MISS`

- [ ] 当前Segment进入Final Video前已通过Video Risk Static Reference Gate，不存在`VIDEO_RISK_REFERENCE_GAP / SUPPORT_REFERENCE_AUTHORITY_FAIL`
- [ ] 若已有Approved Production Support / Additional Video Conditioning Keyframe，其输入模式为`HD_PRODUCTION_SUPPORT_IMAGE`，只控制授权的Interaction / Contact / Transient State / Exact Shot Composite，没有覆盖Identity / Canon Structure / Geography
- [ ] 若已有Approved Shot Assembly，其输入模式为`HD_SHOT_ASSEMBLY_IMAGE`，只控制多人关系 / 人景物组装 / 空间占位；它没有覆盖的关键对象字段仍由对应HD Object Authority承担
- [ ] Approved Additional Video Conditioning Keyframe存在时已按**字段级**去重：重复Composite/Contact不平权；Storyboard独有Temporal Beat / Action Sequence / 多Panel状态递进仍保留必要视觉控制，没有被单帧Anchor整资产TEXT化
- [ ] Previous Ending Frame只承担连续性；若当前模型存在明显低清污染风险且Continuity Snapshot足够，已评估TEXT_CONTROL而不是机械强传图
- [ ] Render Style Anchor只承担绘画语言；Cinematic Shot Style Anchor只承担项目级摄影语法且没有覆盖Storyboard具体Camera/Blocking；综合色Reference只承担当前Global/Scene/Shot层级综合色/光色；均未被写成清晰度、锐度、纹理或综合画质来源
- [ ] 人物、道具/武器、场景分别从当前Task最直接的APPROVED HD Object Authority（Master / Coverage / Detail / State）恢复正式结构、材质与细节；Project Style DNA只统一绘画语言
- [ ] FINAL VIDEO PROMPT需要声音边界时只包含**一次**直接的“不要生成背景配乐”执行句；不出现Audio Boundary/MUSIC=NONE/Stage 06管理标签，也没有同义重复
- [ ] FINAL VIDEO PROMPT已通过Semantic Dedup Hard Gate；同一事实只有一个Owner，不存在`PROMPT_REDUNDANCY_FAIL`
- [ ] Entry只写t=0状态；所有时间变化统一在Integrated Shot Timeline执行，没有再单列Performance / Action / Crowd / Environment摘要复述
- [ ] 已有明确正向动作解时没有再追加同义Negative；Reference职责与Global Lock没有跨区重复解释
- [ ] Stage 05只允许必要Dialogue/VO、Ambience、Foley/SFX和明确剧情内的Diegetic/Source Music
- [ ] 若没有明确剧情内音乐，已按 `MUSIC = NONE` 执行；没有自动情绪铺底、战斗音乐、悬疑音乐、变身配乐或cinematic score
- [ ] Music Identity / Rhythm Profile只控制人物视觉与动作节奏，没有被错误翻译成“自动生成该风格BGM”
- [ ] 需要Dialogue/VO时已明确Voice Mode；无Approved Voice Master的对白为TEMP_SYNC_AUDIO并标记Stage 06必须替换，没有把随机模型音色当正式声纹
- [ ] 已有APPROVED Music Identity的角色在Stage 05使用Character Leitmotif + Scene Emotion + Action Intensity形成Effective Motion Grammar，没有因单场情绪改写核心音乐人格
- [ ] FINAL VIDEO PROMPT需要额外保真句时只包含**一次**直接画面语言；不出现Render Quality Lock/Reference Pack/Approved Authority等内部术语，且未继承控制图的宫格感、草图感、截图柔化、压缩模糊或低细节密度
- [ ] 若实际使用的尾帧/分镜与正式母图在“站位”和“正式外观”上冲突，已按职责拆解：连续性字段服从尾帧，身份/结构/材质字段服从对应Master，而不是整张图二选一
- [ ] FINAL VIDEO PROMPT使用当前Segment的Reference Pack，未混入无职责旧资产
- [ ] Task-Bound Reference Binding无未解决`REFERENCE_COVERAGE_GAP / REFERENCE_SLOT_OVERFLOW / REFERENCE_RELEVANCE_FAIL / REVISION_TARGET_BINDING_FAIL / NEGATIVE_RELEVANCE_FAIL`；关键可见资产全部覆盖，每张实际图片输入都能回答Why Now / What Field / Most Direct
- [ ] FINAL VIDEO PROMPT没有Reference职责行政块、文件名 / Raw Asset ID / Version / Path；Reference Role已消解到真实执行区块；平台确需原生@Token时仅保留真实Token + 最短执行句，Token后无内部名称/版本/职责长解释
- [ ] 不存在`PSEUDO_IMAGE_MENTION_FAIL / EXECUTION_REFERENCE_METADATA_LEAK / REFERENCE_ROLE_MAPPING_AMBIGUOUS`；若目标平台要求图片引用，使用平台真实原生Handle/Slot而不是Skill自造Token
- [ ] Reference Budget优先保住所有Critical / MUST字段；槽位受限时先裁真正冗余与可安全TEXT_CONTROL项，再用Assembly/Anchor重组；Critical仍超限则`REFERENCE_SLOT_OVERFLOW`并考虑回上游重组或拆Segment
- [ ] 模型执行Prompt正文没有混入Adaptive Take Budget / Shot Investment Tier、WEB_QC、LOCAL_SELF_CHECK、Approval Gate、Reference Budget算法、QC动态编号算法、Asset ID / Version / Path或Workspace/归档等内部生产规则
- [ ] Task-Specific Restrictions只写当前Segment独有风险，没有再次复制全局反写实、Render Quality或NO AUTO BGM长列表
- [ ] 具体人物/地点/怪物/未来Beat排除项都能回指当前Reference / Control / Continuity / 已证实Failure的真实污染路径；当前输入里不存在的实体没有被无效点名
- [ ] 当前Shot已有匹配Environment / Prop Coverage时优先使用对应视角；没有机械加入不匹配机位的Hero Master争夺空间控制权
- [ ] 正向执行内容（镜头/表演/动作/物理）明显多于禁止项，没有形成“禁止项堆叠Prompt”
- [ ] Video实际使用的Reference Pack已保存资产ID / 版本 / Reference Tier / Entry Mode / Storyboard版本，以及实际使用时的Previous Ending Frame来源；视频获批后冻结为历史Snapshot
- [ ] Video QC PASS与用户APPROVED已分开记录；用户未明确批准时没有提前交接正式Ending Frame / Continuity Snapshot
- [ ] Executor Input Map中的实际输入顺序/平台Handle与Semantic Role一致；Generation Prompt不显示内部编号
- [ ] 视频连续性问题已按P0/P1/P2判断；单根头发、微小衣褶、雨滴等P2自然变化没有触发无意义重生
- [ ] 生成阶段没有夹带`WEB_QC_UPLOAD_LIST / WEB_QC_COPY_PROMPT`；拿到实际Video Take并进入QC后才单独生成完整QC Packet
- [ ] Stage 05 Web QC按`1 Video Take + <=10 Reference Images`装包；Upload List明确`QC Batch`与`Reference Image Count N/10`，没有@图11
- [ ] 若Video QC所需图片证据>10，已先删CONDITIONAL/TEXT-ONLY化；仍超限则拆PASS-A/PASS-B并计划本地Merge，不要求网页端跨批猜测
- [ ] WEB_QC_COPY_PROMPT所有动态字段已填完，没有遗留`<SEGMENT_ID>`等占位符；已原样内嵌本次完整FINAL VIDEO PROMPT、实际@Reference Pack职责、验证方法和标准化返回格式
- [ ] WEB_QC_COPY_PROMPT是一个连续可全选复制的代码块，网页版不安装本Skill也能独立完成QC
- [ ] WEB_QC_COPY_PROMPT已显式写入免费额度水印豁免：`Dola AI`与`豆包AI生成`水印本体不得记P0/P1/P2、Render Quality失败、文字/Logo污染或Revision Target；仅实际遮挡关键证据时记`EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK`
- [ ] 默认Video QC Mode为WEB_QC_DEFAULT；用户贴回External Report后已核对Segment / Prompt Version / Take，并且没有要求本地重复读取同一完整视频
- [ ] 只有用户明确要求“亲自检查/复核”时才执行LOCAL_SELF_CHECK；外部结论LOW CONFIDENCE / INSUFFICIENT_EVIDENCE没有自动触发本地视频读取
- [ ] External Video QC PASS仍然只进入WAITING APPROVAL，没有替代用户明确批准
- [ ] 图片阶段的2–4张候选策略没有被套用到Video；不存在`CANDIDATE_POLICY_BLEED_FAIL`
- [ ] 每个FINAL VIDEO PROMPT默认从1个Video Take起步；T1/T2未预生成多Take；T3/T4若启用受限候选预算，已有Static/Storyboard Gate通过 + Failure Diagnosis证明随机性为主因，并且Take数量未超过当前预算上限
- [ ] 失败时先分类IDENTITY / STYLE / SPACE / PROP / PERFORMANCE / CROWD-PRESENCE / ACTION-FEASIBILITY / ACTION-PHYSICS / MUSICAL-COMBAT / IMPACT-VFX / CAMERA / CUT-TIMING-DURATION / REFERENCE OVERLOAD / RANDOM FAILURE
- [ ] 使用Minimum Necessary Change；有明确问题时先完整诊断并最小修改Prompt，再只生成1个新Take；没有靠双Take/多Take碰运气
- [ ] QC结果与Next Action已回写Episode Workspace
- [ ] 若用户已经额外产生多个Video Take，才执行Candidate Triage；Candidate Triage没有被用作预先生成多个Take的理由
- [ ] Ending Frame通过专门QC：无严重运动模糊、轴线清楚、关键状态可判断、不在CUT中间
- [ ] Approved Video已生成Continuity Snapshot并写回Workspace
- [ ] Approved Ending Frame只有真实Source Path解析、Copy、Target后置验证与Source/Target SHA-256全部PASS后才标ARCHIVED；否则明确ARCHIVE PENDING
- [ ] 重试遵守Adaptive Take Budget：先Trim/Post修 → 完整诊断 → 局部修Prompt；T1/T2仅近似合格且随机波动时可选再试1次；T3/T4额外Take前执行Failure-before-Compute，达到预算上限仍失败则停止盲抽并简化Reference/回Stage 04/拆Segment
- [ ] 未出现同一错误无限“再生成一次看看”
- [ ] Failure Diagnosis后的Prompt修改由Prompt Compiler保持其余正确模块不变，并重新输出完整Prompt

- [ ] FINAL VIDEO PROMPT的Director Target Duration满足`duration > 0`并与Approved Sequence一致；不存在Skill级固定最大秒数检查
- [ ] Platform Duration Profile只来自当前可靠平台信息；若未提供保持UNDECLARED，不虚构Slot/Hard Max；若平台有Slot，多余Slot只作为可Trim余量，没有新增剧情动作填满
- [ ] 多Shot同Segment累计目标时长与Approved Sequence一致；是否拆分由戏剧结构和当前真实平台能力决定，不按固定10秒切

## Stage 06｜成片 QC

### Music Sync Integrity
- [ ] 有Visual Beat Map的Segment已优先读取实际APPROVED Take Timestamp Map
- [ ] Protected Sync Point（关键Contact/第四拍/断裂/变身完成等）优先通过BGM剪辑、Duck、Drop或轻微Time-Stretch对齐，没有为现成BGM破坏已批准动作因果
- [ ] Rest/Hold没有被持续高强度BGM淹没；关键Contact SFX没有被BGM盖住
- [ ] Video Take换版后旧Visual Beat Timestamp Map已标STALE并重建

### Picture / pacing
- [ ] 最终单集成片时长在15:00–18:00
- [ ] 镜头节奏与Scene/Beat时长预算基本一致
- [ ] 情绪镜头有足够停留，不被过早切断
- [ ] 动作镜头没有因停留过久而失速
- [ ] 模型执行的CUT / Match Cut在最终剪辑中仍有明确视觉/动作依据
- [ ] 不同Segment之间曝光、色温、饱和度、线稿/纹理清晰度、颗粒/柔化没有明显跳变

### Dialogue / performance
- [ ] 对白、VO、口型与实际Speech Phrase / 自然换气基本同步
- [ ] 没有为了Lip Sync强迫台词以不自然速度播放
- [ ] 有意义的换气、停顿与听者反应没有被粗剪删除；普通句间没有被额外制造空白停顿
- [ ] 所有TEMP_SYNC_AUDIO已替换为正式声音；同一角色跨Segment最终音色/年龄感/语言或口音要求保持一致

### Ambience / SFX / Foley
- [ ] 同一Scene的Ambience声床连续，没有每到新Segment就重新起头或断掉
- [ ] 同一地点的混响/空间感基本一致
- [ ] 脚步、衣料、道具接触、撞击等Foley/SFX与可见动作接触点同步
- [ ] 不存在与画面重量/材质明显不匹配的通用SFX

### BGM / sound bridge
- [ ] BGM按Scene/Beat的Cue Map推进，而不是每个Segment各起一首/一段
- [ ] Cue In / Build / Duck / Hit / Drop / Cue Out符合戏剧节奏
- [ ] BGM没有掩盖关键表演和对白
- [ ] 需要时使用J-cut / L-cut保持声音连续与情绪流动
- [ ] CUT / Match Cut两侧的声音过渡自然，没有机械断音
- [ ] 涉及Music Identity的角色，BGM方向参考稳定Character Leitmotif + 当前Scene Emotion / Action Intensity，没有因一次悲伤/战斗场景把角色长期音乐身份彻底换掉

### Master
- [ ] 对白、BGM、SFX、Ambience响度层级清楚且全片一致
- [ ] 字幕时长、安全区、画幅统一
- [ ] 已从头到尾完整播放检查，而不是只检查单独Segment
- [ ] 若问题来自资产，回Stage 03；来自分镜，回Stage 04；来自生成，回Stage 05；来自结构节奏，回Stage 02；来自故事因果，回Stage 01


## Performance Causality补充检查（Stage 04 / 05）

- 是否存在Natural Face Behavior：正常眨眼、视线逻辑、眉眼参与，而不是长期瞪眼不眨；
- 是否先能说明Given Circumstances / Objective / Obstacle / Tactic，再进入Baseline / Trigger / Delay / Leak / Controlled Response / Landing；
- 重要情绪是否由Objective / Obstacle / Stimulus / Tactic Outcome解释；Intensity是否按对判断/策略/控制的影响判断，而不是按身体部位数量；
- 是否保留有心理意义的微动作，并在过密时使用合并/排序/分时/景别转译，而不是直接删除；
- 是否把`Involuntary Leak + Controlled Response`这种真实心理对抗误删成“矛盾”；
- 多人场景中是否存在Active Listening：未说话角色不无因站岗；有因Triggered Stillness是否被正确保留；
- 重要日常对白是否存在Objective / Tactic / Subtext与Speech-Body Coupling；是否有Thought Intention / Speech Phrase / Body Continuity / Continuity Bridge / Listener Flow；
- Breath=IMPLICIT时是否避免把呼吸单独编成可见动作；可见换气是否有明确Cause / Degree / Timing / Recovery；
- 战斗是否存在Combat-Performance Coupling，动作与表演互为因果而非两个孤立模块；
- 是否明确主反应者 / 次反应者 / 背景听者，避免所有人同级同时反应；
- 是否出现Premature Reaction：在Trigger发生前提前反应。
- 每个重要可见微动作是否能解释“角色为什么现在这么做”；若无法追溯到Objective / Tactic / Stimulus，应视为随机加戏；
- Beat Shift是否来自策略/目标/关系/事实变化，而不是文字标点；
- 镜头越近是否只是表演幅度更精确，而不是动作数量机械增多。


## WARDROBE DESIGN GATE｜日常服装审美与角色衣柜
- [ ] 日常共享的是20世纪70—90年代欧洲都市/地区服装世界；French-inspired Urban Minimalism只是可选子语言，不是全员默认制服，也不是现代网红法式/历史戏服。
- [ ] 主要/反复角色已有Character Fashion DNA、Wardrobe Diversity Matrix Ref与Character Closet Ref。
- [ ] 当前Look通过`No Lazy Styling`：Closet旧单品+大衣/围巾等现实复用完全合法；只有机械加功能件、只换色、且没有新的比例/开合/层次/材质/综合色/Body Presentation逻辑时才判`WARDROBE STYLING LAZY`。
- [ ] 优先复用/重组Closet Item；新增单品已通过New Item Admission Gate。
- [ ] 当前Look符合季节/天气/场合/活动，同时仍像这个角色自己会穿。
- [ ] 成年角色Primary/Secondary Appeal、Body-Line Emphasis、Silhouette Hook、Motion Appeal没有被无理由抹掉；极端天气下已用版型/比例等合法转译。
- [ ] 未成年角色没有成人身体性感化，只使用辨识度/气质/可爱度/剪影魅力。
- [ ] 与同Scene其他主要角色不存在`WARDROBE TEMPLATE COLLISION`：不按固定“3项差异”凑配额；综合比较Silhouette / Proportion / Collar / Layer / Material / Footwear / Body Presentation / Styling Habit后，整体Styling Signature应清楚区分，不能只换综合色。
- [ ] Wardrobe State Ledger与World State一致，脱下/携带/湿水/污渍/破损没有凭空重置。


## Body Identity / Presentation Gate
- [ ] 成年角色Body Identity已锁定，服装没有改变其肩胸腰胯腿等既定身体身份
- [ ] 当前LOOK已选择合理Body Presentation Mode：DIRECT / FRAMED / PROPORTIONAL / IMPLIED / CONTRAST / MIXED
- [ ] Body-Line Emphasis被理解为“魅力重点”，而不是要求每件衣服都收腰/贴身/高腰
- [ ] 宽松 / Oversized / 直身 / 阔腿等合法轮廓没有为了过QC被强行掐腰
- [ ] 冷天不再使用固定“显身材措施数量”配额，而是检查最终Body Beauty / Appeal / 比例是否成立
- [ ] 多名角色没有同时坍缩成同一套收腰+贴身+高腰模板

## Source Wardrobe / Costume Dramaturgy Gate
- [ ] 小说服装描述已分类；普通DESCRIPTIVE_CUE没有变成最终造型硬锁
- [ ] 真正WARDROBE_PLOT_FACT必要字段没有在重设计中丢失
- [ ] Stage 02已锁Dressing Knowledge Boundary / Motivation / Self-Presentation / Costume Narrative Function
- [ ] 没有用Scene后发生的事件倒推人物出门前的穿衣选择
- [ ] Stage 03负责具体WHAT/HOW，Stage 02没有越权发明未Approved的新裁片


### Current｜Voice Direction / Prosody QC
- [ ] 重要Dialogue/VO已从Actor Objective/Tactic/Subtext派生Voice Direction Card，不只有“悲伤/低沉/慢一点”等抽象词
- [ ] Performance Loudness与Stage 06 Mix Loudness分权；耳语/压低声音没有被Gain目标误导成大声表演
- [ ] 有意义台词已判断Pace Curve、Pause Map、Stress/De-emphasis与Sentence-final Intonation；停顿有明确原因，不按标点机械插入
- [ ] 同一角色Prosody变化仍保持Approved Voice Identity；没有因情绪随机换音区/音色/年龄感/口音
- [ ] 多人对白存在Listening / Interrupt / Overlap逻辑（适用时），不是机械轮流念稿

### Current｜Visual Reference Routing QC
- [ ] Color Card / Style Board / Storyboard / Contact Sheet都有Capability/Role Route；没有按类别一刀切禁止
- [ ] Approved Color Card / Style / Storyboard只要平台可接收图片且对应Direct Route未`VERIFIED_FAIL`、无真实Leak证据，就优先保留视觉控制；能力`UNKNOWN`没有被当成自动TEXT/Crop/Applied理由
- [ ] 平台支持4/6/9格或Storyboard Board时允许整板；支持多图时可用关键Panel；只有真实Leak历史才升级Crop/Applied Reference
- [ ] 实际Video没有不该出现的色块、格线、Panel边框、Board标题/UI，也没有复制无关样例人物/地点
- [ ] 已发生Reference Leakage的Retry没有沿用同一失败路线只加Negative


### Current｜Model-Facing Prompt Surface Sanitization QC
- [ ] Executor Binding Packet默认仅存内部运行时，不作为用户可见附录；用户可见Generation交付只剩单一Copy Surface（除非实际Reference Binding尚需一句最短操作提示）
- [ ] Copy Surface中不存在`TASK_SHELL / INPUT_MAPPING / OUTPUT_ADMIN_SHELL / LOCAL_FILE_METADATA`
- [ ] 模型正文没有`Reference Responsibilities / 三参考职责分离 / Existing Authority Reuse Scan / MUST_BIND_EXISTING_ASSETS / Executor Input Map`
- [ ] 模型正文没有`ENV_* / ASM_* / COLOR_* / *_MASTER_v001 / *_CROP_* / *_ASSEMBLY_*`等内部命名
- [ ] 平台确需@Token时，Token后只有最短画面执行句；不存在`@图N｜资产名（内部ID）：职责解释`
- [ ] Stage 05任何@Token都有明确且实际匹配的Reference Role；Capability可为`VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN`，其中`UNKNOWN`不等于禁用。Color Card、Style Board、Storyboard在Current Route允许时可合法Token化
- [ ] 综合色/环境/人物/Assembly的内部Role均已转写为主体、空间、综合色、构图、Entry/Timeline执行事实
- [ ] 无`MODEL_FACING_METADATA_LEAK / REFERENCE_ADMIN_TEXT_LEAK / PIPELINE_JARGON_LEAK / INTERNAL_HEADING_LEAK / NATIVE_TOKEN_OVERANNOTATION / UNROUTED_CONTROL_REFERENCE_TOKEN / PROMPT_SURFACE_SANITIZATION_FAIL`

### Current｜Style Authority Projection QC
- [ ] 正式Stage 03/04/05 Prompt存在有效`STYLE PROJECTION CARD / Fingerprint`
- [ ] 已绑定Approved Visual Style Evidence时允许Copy Surface只保留短Style continuity；没有视觉风格证据时才要求FULL Render Core
- [ ] `STYLE_TAG_ONLY_FAIL`只在Text是唯一风格控制且内容仍是抽象Tag时成立
- [ ] 有人物视觉Owner时不靠长风格文字重新发明脸/皮肤/头发
- [ ] 补图/重建/Revision存在最直接Style Continuity视觉证据时已真实绑定或有明确平台不支持理由
- [ ] Sanitizer / Dedup没有把Style Projection过度删薄
- [ ] 实际生成视觉若要进入APPROVED/Freeze，External/Web QC已经明确检查`Style Match: PASS / FAIL / N/A`，不能只验Prompt是否写对


### Current｜Video Temporal Salvage QC
- [ ] Whole-Take Verdict与Temporal Salvage Status分开记录；整体REVISE没有被误写成“整条无用”
- [ ] 非PASS/局部失败Take已完整看到结尾并建立Temporal Salvage Map
- [ ] Temporal Salvage Map覆盖00:00.00→Source Duration完整时间轴，无重叠、无未分类Gap；不可用区间明确REJECT
- [ ] Audio-only可用区间使用CONDITIONAL_KEEP + VIDEO_USE=REJECT + AUDIO_USE=AUDIO_ONLY，不被彻底REJECT误丢
- [ ] 所有Window按时间升序且不重叠；无真实Evidence时没有编造IN/OUT
- [ ] CLEAN_KEEP通过Visual / Temporal / Editorial / Entry-Exit Cutability / Continuity / Director Invariants
- [ ] CONDITIONAL_KEEP写清具体使用条件；HANDLE_ONLY没有被当独立Narrative Beat使用
- [ ] Video Use与Audio Use分开；画面可用但音频坏时优先Audio Replace
- [ ] 不为了抢救素材破坏不可切Long Take、Reveal顺序或Reaction Give-Deny
- [ ] SALVAGE_CANDIDATE没有自动升级APPROVED VIDEO / Ending Frame Authority
- [ ] 存在Salvage Candidate时Source Take已标Preserve Source File=TRUE
- [ ] 新增Take前Failure Diagnosis已先检查Salvage，避免重复生成已经成功的时间段
- [ ] Stage 06若使用Salvage已建立EDL并通过跨Take Identity/Axis/Action/Lighting/Style/Audio Continuity检查


### V4.5.2 Spatial Canon / Clean Storyboard
- [ ] 重要/复用Location在任何Environment视觉资产生成前已有Approved `SPATIAL_CANON`；Topology/Floor Plan/Zone/Door-Window/Sightline/Access均无矛盾。
- [ ] SHOT_RELATION_GRAPH中的`VISIBLE_FROM / EXTERIOR_INTERIOR_SAME_ENTITY`等声明能回指Locked Spatial Relation，而不是Director文字自证。
- [ ] Final Episode Asset Manifest包含所有到Stage 03 Freeze的Relation-driven Obligation；不存在“Graph里要求但资产队列里没排”的漏项。
- [ ] 每张正式Storyboard Panel是纯净视觉：无文字、数字、Shot/Panel ID、时间码、CUT、箭头、轨迹线、说明框、字幕；导演说明只在Metadata。
- [ ] 隐藏所有Metadata后，只看相邻Clean Panels仍能读出Attention Target / Reveal / POV / Match等核心关系证据。
- [ ] Sequence Board仅由Approved Clean Panels确定性拼版；图像模型未生成带注释Storyboard Page。
- [ ] FIRST_TARGET / FIRST_LAST / CONTACT / TRANSFORMATION / KEY_POSE等Conditioning策略的Required Frame Role齐全，不靠`qc_status=PASS`自证。
- [ ] CUT Pair的Exit/Entry资产真实存在Asset Registry，且分别履行该Relation的对应Obligation；不存在GHOST Asset或错Relation绑定。


## V4.5.2｜Virtual Set / Script-Grounded Spatial QC
- [ ] Event Node已经绑定Location / Zone / Anchor，而不是只有地点名；
- [ ] 跨节点移动的主要人物/群组有可验证Character Event Route；
- [ ] Outdoor Topology / Floor Plan展示的距离、坡向、门窗、路径与结构化Spatial Canon一致；
- [ ] Required Planning Diagram已用户批准；下游图片没有在上游未锁时提前批量生成；
- [ ] 每张Event/Coverage View回指正确Spatial Parent；多角度还回指正确Visual Parent；
- [ ] 正打/反打、前看/回看、入口/出口等关系视角按真实需求覆盖；
- [ ] Predictive Coverage来自已知未来Shot/高复用需求，不是固定九宫格收藏；
- [ ] Interior / Exterior Look Domain正确，未因同地点而机械混成一个光色状态；
- [ ] 主要/反复角色Voice Identity已锁或明确TEMP_SYNC/POST replacement例外；
- [ ] 每个正式TO BUILD资产都有WHY_REQUIRED / REQUIRED_BY / DOWNSTREAM_USE。


## V4.5.3 Visual Evidence / Text-only QC

- [ ] 当前Controller Mode已明确：`MULTIMODAL_ACTIVE / TEXT_ONLY_CONTINUATION`。
- [ ] Text-only模式下，每个被绑定的Image Asset都有Current Visual Evidence。
- [ ] Evidence的Source Fingerprint与当前Asset Fingerprint一致。
- [ ] Required Visual Facts由Evidence覆盖，不靠文件名或Prompt猜测。
- [ ] Evidence Issue Codes没有命中当前Shot的Forbidden Visual Facts。
- [ ] Primary Visual没有被Evidence标记为`primary_visual_eligible=false`。
- [ ] 多模态模型新批准正式图片后，Visual Evidence已写回项目状态。

## V4.5.4 Required View Realization QC

- [ ] 每个Event Node的`required_view_roles`都已物化为具体`view_requirement_id`。
- [ ] 每个方向都有明确`Camera Origin → Optical Axis → Must See`，没有只写“正视角/反打/侧面”。
- [ ] `VIEW_ROLE_COVERAGE_MATRIX`覆盖本集全部Scene，不以“生成数量很多”替代Coverage完整。
- [ ] 每个正式Coverage Asset回指真实`view_requirement_id`并继承Spatial Parent + Visual Parent。
- [ ] P0/P1 MISSING View已经优先补齐；没有在缺关键方向时继续堆同方向超预算Candidate。
- [ ] Final Selected Fulfillment Asset已经APPROVED。
- [ ] Current Visual Evidence证明Observed View Role、Camera Axis、Visible Anchors与Requirement一致。
- [ ] Must See Anchors真实可见；Forbidden Anchors/Facts未出现。
- [ ] 任一失败均阻断Episode Asset Freeze，并按`REQUIRED_VIEW_COVERAGE_GAP / REQUIRED_VIEW_VISUAL_MISMATCH`最小回滚。

## V4.5.5 Everyday Realism & Plausibility QC

### 普通剧情全局基线
- [ ] 当前Scene/Asset默认`REALISM_REQUIRED`；若有Transformation/Combat/Supernatural/Dream等例外，Exception精确限定Scope + Allowed Categories + Reason，没有“奇幻故事全局关闭现实性”。
- [ ] 先判断现实中是否成立，再判断构图/综合色/美术质量；明显不合理的漂亮图没有被APPROVE。

### Environment / Architecture / Vehicle
- [ ] 空间功能与具体类型明确；门、窗、楼梯、通道、操作区、家具净空和人体尺度基本可用。
- [ ] `VEHICLE`有具体Vehicle Type与`VEHICLE_LAYOUT`；驾驶控制区、乘员座位、出入口、通道、前后方向、容量与外部尺度相容。
- [ ] 派生图没有把正确Floor Plan/Vehicle Layout重构成另一个漂亮但功能不同的空间。

### Human Occupancy / Ergonomics
- [ ] Expected Cast Count与Observed Human Count一致；非群众镜头无额外陌生人/角色重复。
- [ ] 每个角色处于正确Zone / Seat / Functional Position；换位有World State来源。
- [ ] 坐/站/靠/持物有真实支撑，身体不穿墙/座椅/扶手，Reach与通行空间成立。
- [ ] 人体、家具、门窗、车辆尺度基本可信，没有为了塞人物无因拉大空间。

### Object / Social / Physics / Continuity
- [ ] 门、椅、柜、控制件、道具真的可操作/可使用；不是只有外形。
- [ ] 人物距离/朝向符合当前任务与关系；明显反常位置有`behavior_reason_ref`。
- [ ] 雨湿、污渍、破损、烟雾、碎玻璃、光源变化等遵守Cause→Effect，不无因增删。
- [ ] Seat/Zone/Holder/Door/Vehicle Motion/Wetness/Damage/Ongoing Task不因CUT或新图片无因Reset。

### Reconciliation
- [ ] P0/P1失败已先定位Source / Realism Contract / Spatial Canon / World State / Generated Asset / Visual Evidence Owner。
- [ ] 上游Canon正确时Reject错误Candidate，没有为了迁就漂亮图片修改Canon。
- [ ] Text-only模式只读取Current Visual Evidence的Observed Realism；UNKNOWN/MISSING已进入Visual Review Queue，没有猜PASS。
