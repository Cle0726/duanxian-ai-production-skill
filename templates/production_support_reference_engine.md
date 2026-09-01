# Production Support Reference & Video Risk Reduction Engine（生产辅助参考与视频风险前置消解引擎）

> **适用范围：Stage 02 → Stage 03 → Stage 04 → Stage 05。**
>
> 当前项目的真实成本结构是：**静态图片生成成本很低，Video Take成本很高。** 因此本引擎不以“尽量少做图片”为目标，而以“在进入昂贵视频前，用充分、直接、职责清楚的高清静态证据消除可预见歧义”为目标。
>
> 本引擎**不是Stage 07**，也不改变Character Master / Environment Master / Prop Master现有Canon流程。

---

> **V4.4 Override｜Mandatory Video Conditioning：** `VIDEO_CONDITIONING_KEYFRAME`不再代表“只有T3/T4才有的可选静态保险”。所有正式Video Unit都必须在Approved Storyboard之后拥有最小`VIDEO CONDITIONING ASSET`。简单Shot可以仅1张`VIDEO_FIRST_FRAME / SHOT_EXECUTION_FRAME`；复杂Shot才增加Target / Last / Contact / Key Pose。旧文中“普通T1/T2可完全不做镜头级执行图直接Video”的规则失效。完整Owner：`video_conditioning_asset_architecture.md`。

## 1｜核心原则

**Do not ask only “Can the model infer it?” Ask “Is the remaining ambiguity cheap to remove before video?”**

Stage 02/03不再只问：
> `Approved Master + Text Spec理论上够不够？`

还必须继续问：
> `如果现在多生成一张低成本高清静态参考，是否能显著降低Stage 04/05特别是Video的错误概率、返工概率或Reference歧义？`

若答案为YES，并且该问题确实能被静态图解决，则优先在视频前解决。

这不等于“每个Shot都做一张图”。新增任何Support Reference仍必须证明：
1. 当前真实Shot/Segment确实需要；
2. 现有Approved Authority + Text + Storyboard不能稳定唯一执行；
3. 静态图能够解决这个歧义，而不是把时间/动作问题伪装成图片问题；
4. 生成该图的成本明显低于一次Video失败的预期成本。

---

## 2｜四类静态视觉Authority必须分清

### 2.1 Canon / Coverage Authority
回答：**“这个对象/空间到底是什么？”**

包括：
- Character / Transformation Master；
- Environment / Prop / Weapon Canon Master；
- Environment / Prop Derived Coverage；
- 正式Persistent State Variant；
- 正式Detail Master。

这类图可以成为`HD_OBJECT_AUTHORITY_IMAGE`。

### 2.2 Production Support Reference（Stage 03）
回答：**“当前高风险生产任务里，模型还需要额外看清什么，才能不靠猜？”**

它是由Approved Canon/Coverage派生的高清生产辅助图，统一输入模式：

`HD_PRODUCTION_SUPPORT_IMAGE`

它可以控制指定的：
- Interaction Geometry（交互几何）；
- Complex Contact（复杂接触/扶抱/压迫/递交关系）；
- Transient High-Risk State（短暂但高风险的可见状态）；
- Entity Action State（一次性但形态容易猜错的攻击/动作状态）；
- Mechanism Use Evidence（机关/操作使用证据，前提是结构Canon已经由Master/Coverage定义）；
- Scoped Minor Prop Appearance（只在当前Scene/Shot使用、无需升级项目Canon的小型交互道具外观）；
- Shot Detail Evidence（一次性Insert/局部可读性证据，前提是不借此发明新的长期Canon结构）。

**它不是新的Canon设计。** 与Master/Coverage冲突时，Master/Coverage优先。

### 2.3 Shot Assembly Asset（Stage 03）
回答：**“当前人物、场景、道具各自已经定义好了，但视频还缺一张‘这些元素如何在同一镜头类型里成立’的高清静态组装图吗？”**

命名角色：

`HD_SHOT_ASSEMBLY_IMAGE`

它由已批准Character / Environment / Prop / Persistent State / Scene Color等Authority组装而成，用于：
- 多人物关系镜头；
- 人物进入功能空间（病床、驾驶位、后排、舞台、门区等）；
- 人景物同时同框的复杂镜头；
- Montage一次性情境镜头。

它**不是Storyboard，不允许直接从九宫格分镜清稿生成**；也不是新Canon。

### 2.4 Additional Video Conditioning Keyframe（Stage 04）
回答：**“Approved Storyboard已经定了这个Shot怎么拍，但低清/宫格控制图不足以作为昂贵Video的高保真视觉执行锚点时，最终这一镜应该以怎样的高清构图与接触状态进入Video？”**

命名角色：

`VIDEO_CONDITIONING_KEYFRAME`

输入模式仍使用：

`HD_PRODUCTION_SUPPORT_IMAGE`

它必须在Approved Storyboard之后生成，由：
- Approved Storyboard的当前Shot构图/Blocking；
- 当前最直接Approved HD Object Authorities；
- 当前Scene/Shot综合色与Lighting；
- 已解决的Action Feasibility / Natural Motion关键状态

共同派生。

它**不是Storyboard替代品，也不是Canon Master**；它只是把低清Storyboard的“怎么拍”翻译成一张高清、当前Shot专用的执行锚图，从而避免Video把宫格模糊度当最终画质。

---

## 3｜Stage 02：Video Risk-Driven Static Reference Matrix

导演锁定Detailed Shot Contract / Segment后，在Final Episode Asset Requirement Manifest之前必须额外做一次静态风险判断；其输出先进入Raw Asset Demand Set，再由`asset_consolidation_sufficiency_audit.md`跨Shot合并，不直接一Shot一资产。

```text
| Shot/Segment | Investment Tier | 关键视觉任务 | Static Ambiguity | Interaction/Contact | State Persistence | Static-Solvable? | Existing Authority Enough? | Required Ref | Owner Stage | Why |
|---|---|---|---|---|---|---|---|---|---|---|
| SH__ | T1/T2/T3/T4 | ... | LOW/MED/HIGH | LOW/MED/HIGH | NONE/SHOT/MULTI-SHOT/SEGMENT+ | YES/NO | YES/NO | NONE / COVERAGE / PERSISTENT_STATE / SUPPORT_REF / SHOT_ASSEMBLY / SHOT_EXECUTION_FRAME | 03/04 | ... |
```

### 3.1 Static Ambiguity HIGH的典型条件
- 多人物同时同框，且站位/谁在前后/谁持有道具会显著影响镜头可读性；
- 复杂功能空间中，人物与床位/驾驶位/舞台/门区等位置关系必须稳定；
- Insert / Close-up需要看清此前未定义或不可读的关键结构；
- 关键机关/开合/操作方式若让模型自行补全很容易猜错；
- 复杂手-物交互、换手、递交、插入、压迫、拉扯、装配；
- 多人扶抱、拖拽、治疗、格斗纠缠等复杂接触；
- 伤势/破损/血迹/湿损等状态会跨多个Shot/Segment持续且位置必须稳定；若随后完整变身触发Recovery，则伤势Persistent State在恢复点终止，不得跨越恢复点继续引用；
- 怪物/武器/机关存在一次性但非常具体的Action State，若只看Master容易生成错误形态；
- T3/T4视频镜头的Blocking/接触/空间关系虽然Storyboard可读，但低清控制图不足以稳定传递给Video；
- 已知模型在同类镜头上有高概率生成手、接触、局部结构或空间关系错误。

### 3.2 Static-Solvable = NO时禁止造图
以下主要是时间行为问题，不要错误地靠多做静态图解决：
- 动作速度曲线；
- Action Overlap / Coarticulation；
- 起步/停步/Pivot等运动过程；
- Crowd是否持续活动、Reaction Propagation；
- Camera Motion本身；
- 对白节奏、微表情时机、呼吸、停顿；
- 受力传播与惯性过程。

这些继续交给Stage 04/05的Action / Natural Motion / Crowd / Camera / Timeline系统。

---

## 4｜决策路由：不要重复建资产

发现高风险视觉需求时按以下顺序路由：

### 0. 这是“低复用、低Canon价值，但当前镜头必须看清/操作”的小物件或局部吗？
→ Stage 03 `LIGHTWEIGHT_INTERACTION_PROP_REF / SHOT_DETAIL_REF`

适用：食物纸袋、一次性票据、临时包装、普通生活用品等，在当前Scene/Shot中被清楚持握/递交/操作，但不值得建立项目级Prop Master。

**升级条件：** 若该物件重复跨Scene使用、承担因果关键线索、结构/纹样必须长期稳定、后续会被特写识别，则不能继续当轻量Support，升级为正式Prop / Detail Authority。

### A. 这是“对象/空间本身尚未被定义”的结构问题？
→ `CANON MASTER / DETAIL MASTER / DERIVED COVERAGE`

例：道具内部结构、舞台反方向空间、非对称物体背面。

### B. 这是“跨多个Shot/Segment持续、结构上明显变化”的状态？
→ `PERSISTENT STATE VARIANT`

例：严重伤势、明显破损、持续性烧毁、长期Transformation异常状态。普通可恢复伤势若在后续Transformation Completion被修复，则其Persistent State只覆盖恢复点之前。

### B.5 这不是局部Support，而是需要一张“人物+场景+道具”高清组装图吗？
→ `SHOT_ASSEMBLY_ASSET`

适用：多人物+环境+关键道具需要同框关系证明、一次性功能人物需要与场景共同落位、或Montage情境镜头需要先锁组合关系等。

### C. Canon已经定义，但当前高风险动作需要额外看清一次交互/接触/短暂状态？
→ Stage 03 `PRODUCTION SUPPORT REFERENCE`

例：两人扶抱时手臂/身体接触关系、角色把关键物插入机关的局部操作关系、一次性攻击形态。

### D. 问题依赖“Approved Storyboard的准确构图/站位”，而且低清Storyboard可能让Video误读？
→ Stage 04 `VIDEO_CONDITIONING_KEYFRAME`

### E. Text + Approved Authority + Storyboard已经足够唯一，或静态图无法解决？
→ `NONE`

**禁止同一个字段问题由Coverage + Support Ref + Shot Assembly + Shot Anchor平权重复控制。一个字段一个Primary Owner；但同一镜头可以同时存在多个不同关键资产/字段的必要Reference。**

---

## 5｜Stage 03 Production Support Reference类型

### 5.1 INTERACTION_GEOMETRY_REF
用于：
- 复杂手-物操作；
- 两人递交/抢夺/扶持；
- 物体进入/离开机关；
- 多部位接触关系需要高清锚定。

只锁：接触位置、持握方式、相对尺度、局部朝向。

不锁：完整时间过程、动作速度、最终Camera Motion。

### 5.2 COMPLEX_CONTACT_REF
用于：
- 抱住、接住、拖拽、压迫伤口、搀扶、多人支撑；
- 战斗中高度复杂但可用单帧说明的关键Contact State。

必须继承Action Feasibility已确认的Limb Occupancy / Support关系。

### 5.3 TRANSIENT_STATE_REF
用于：
- 只持续少量Shot、但视觉错误代价很高的临时状态；
- 不值得升级为正式Persistent State Variant，但Video不能自由猜。

若状态后来证明跨多个Segment持续，自动升级为`PERSISTENT_STATE_VARIANT`，不要让Support Ref长期冒充状态Canon。

### 5.4 ENTITY_ACTION_STATE_REF
用于：
- 怪物、机关、特殊武器某一次高风险动作形态；
- Canon Master已定义主体，但当前动作形态非常具体且视频模型容易随机改结构。

若该形态会反复出现并成为稳定机制，升级为正式State / Detail Authority。

---

### 5.5 LIGHTWEIGHT_INTERACTION_PROP_REF
用于：
- 低复用、无需项目级Canon Master，但在当前Scene/Shot被清楚拿取、递交、放置、食用或操作的小型道具；
- 图片成本很低，而让Video自由猜形状/尺度/持握关系反而增加失败风险的情况。

它可以在限定Scope内控制：`LOCAL_PROP_APPEARANCE / SCALE / HOLDER CONTACT / CURRENT STATE`。

不得：
- 冒充项目级Prop Canon；
- 与正文已明确事实冲突；
- 因为便宜就给每个背景苹果、硬币、杯子建立图片。

### 5.6 SHOT_DETAIL_REF
用于：
- 一次性Insert / Close-up必须读清的局部信息；
- 当前局部并不值得升级为可复用Detail Master，但昂贵Video不能自由补全。

若该局部揭示的是**长期存在的固定Canon结构**（例如关键机关内部构造、反复识别的纹样），应升级为`DETAIL MASTER / DERIVED COVERAGE`，而不是长期留在Support层。

## 6｜Stage 04 Video Conditioning资产计划（V4.4）

**每个正式Video Unit都必须有Primary Visual Conditioning；复杂度只决定数量与类型。**

- T1/T2简单镜头：至少`VIDEO_FIRST_FRAME / VIDEO_SHOT_EXECUTION_FRAME` 1张；已有合格Approved Panel/Coverage/Assembly可Promotion，避免重复生成。
- 明确推近/拉远/目标构图：`FIRST + TARGET`。
- T3/T4、多人接触、战斗、变身、复杂状态变化：按真实风险增加`KEY_POSE / CONTACT / LAST`。
- Hard Cut跨空间：默认拆成独立Video Unit；若平台已验证单Job硬切，Cut两侧仍各有独立time-scoped Primary Visual。

不得用Environment Master、Color Board、Design Board、Whole Storyboard的组合替代缺失Primary Visual；这些图仍允许作为辅助字段Authority进入Video。

### 6.1 生产顺序
`Approved Storyboard → Current State Resolve → Asset Role Resolve → Generate/Promote Conditioning Frame → Static QC → Approval → VIDEO_CONDITIONING_READY`

### 6.2 不得做什么
- 不改变Approved Storyboard Camera / Blocking / Cut；
- 不重设计Character / Environment / Prop Canon；
- 不复制Storyboard宫格、设计板拼版、色板布局；
- 不把临时剧情状态写回Clean Canon；
- 不为了“更漂亮”推翻Director Intent。

## 6.3｜Support / Anchor Prompt编译规则

Production Support与Additional Video Conditioning Keyframe的**内部分析可以详细，真正图片模型Prompt必须短而任务绑定**，并继续执行`task_bound_reference_binding.md` + `prompt_semantic_deduplication_engine.md`。

### Stage 03 Production Support Prompt
内部先求解：这张Support要证明的可见结果、最直接Parent视觉来源、允许变化的接触/持握/相对尺度/局部朝向/暂态形态、需要看清的区域，以及必须保持的人脸/服装/对象结构/场景Geography。**这些是内部语义字段，不是模型侧栏目标题。**

最终Copy Surface只把它们改写成一段直接视觉执行语言；不得输出`OUTPUT TARGET / REFERENCE BINDING / AUTHORIZED FIELDS / CANON BOUNDARY`等内部标签，也不要把整份Director分析、Video Timeline、未来动作或所有Canon再复制一遍。

### Stage 04 Video Conditioning / HD Support Prompt
内部绑定关系：
- 当前Shot HD Support Anchor = 本次静态输出对象；
- Approved Storyboard当前Panel / Shot解析结果 = Camera / Composition / Blocking控制；
- 当前最直接Approved HD Object Authorities = Identity / Structure / Geography；
- 必要Approved Stage 03 Support = Interaction / Contact / Transient State；
- 当前Scene Color / Shot Lighting = Color/Light Control。

这些Role只留内部；最终图片Prompt只描述要画出的当前Shot高清静态状态。输出目标是**当前Shot的高清静态执行锚图**，不是重新设计Storyboard。Stage 05采用字段级Owner：Anchor可成为高清Composition / Contact / Exact Composite的Primary；若Storyboard/Panel仍独占Temporal Beat、Action Sequence或多状态推进，它继续作为视觉控制，不因Anchor存在而整资产降级或删除。

## 7｜命名与登记

Stage 03 Support Reference建议：

```text
SUP_<EP>_<SHOT_OR_ASSET>_<TYPE>_v001
```

Stage 04 Shot Anchor建议：

```text
ANCHOR_<EP>_<SCENE>_<SHOT>_HD_v001
```

登记字段：

```text
Support ID：
Type：INTERACTION_GEOMETRY / COMPLEX_CONTACT / TRANSIENT_STATE / ENTITY_ACTION_STATE / LIGHTWEIGHT_INTERACTION_PROP / SHOT_DETAIL / VIDEO_CONDITIONING_KEYFRAME
Triggered By：Shot / Segment
Parent Authorities：
Authority Fields：
Why Existing References Are Insufficient：
Video Risk Reduced：
Stage Owner：03 / 04
Status：WIP / APPROVED SUPPORT / DEPRECATED
Canon Boundary：不得重定义...
```

`APPROVED SUPPORT`不是`APPROVED CANON`。Archive / Workspace必须保留区别。

---

## 8｜Episode Asset Freeze边界

### Stage 03 Required Support Ref
若Stage 02矩阵明确标记：
`Required Ref = SUPPORT_REF` 且 `Owner Stage = 03`

则它属于Episode Asset Pack的**Required Production Support**，必须完成QC + 用户批准后才能Freeze。

### Stage 04 Video Conditioning / Legacy Additional Video Conditioning Keyframe
因为它依赖Approved Storyboard，所以**不属于Stage 03 Episode Asset Freeze前置条件**。

若当前Video Conditioning Strategy要求额外Keyframe：
- Storyboard APPROVED后状态进入`VIDEO CONDITIONING IN PROGRESS`；
- Anchor批准后才允许该Segment输出FINAL VIDEO PROMPT。

这样不会形成“Stage 04资产反过来阻塞Stage 03 Freeze”的循环。

---

## 9｜Reference Resolver规则

Stage 05当前Shot存在Approved Support时：
- `IDENTITY / OBJECT STRUCTURE / GEOGRAPHY`仍由`HD_OBJECT_AUTHORITY_IMAGE`负责；
- `INTERACTION / CONTACT / TRANSIENT STATE / EXACT SHOT COMPOSITE`可由`HD_PRODUCTION_SUPPORT_IMAGE`作为该字段的PRIMARY；
- Approved Additional Video Conditioning Keyframe存在时只做**字段级去重**：Anchor接管其已证明覆盖的高清Composite / Contact / Shot-specific Blocking字段；Storyboard若仍独占Temporal Beat、Action Sequence、状态递进或多Panel运动证明，继续按Capability作为视觉控制。不得因为Anchor存在就整资产降为`TEXT_CONTROL`；
- Support已把某字段完整说明后，不再重复上传一组无职责Master“求保险”；仍缺身份/结构字段时才补最直接Object Authority。

每张Support仍必须通过：
`Why Now / What Field / Most Direct`。

---

## 10｜QC Hard Gate

### `VIDEO_RISK_REFERENCE_GAP`
出现以下任一情况：
- Stage 02已判定高Video风险且Static-Solvable，但没有路由到Coverage / Persistent State / Support Ref / Shot Anchor；
- T3/T4复杂接触镜头仍要求Video从多个分散Master与低清Storyboard自行猜最终接触关系；
- 严重跨镜状态没有正式State Authority；
- 已知关键机关/局部结构在Video中必须看清，却只有不可读Hero Master；
- 当前Reference Pack存在可由一张直接高清Support图消除的明显歧义，却直接进入昂贵Video。

→ 在进入Stage 05前返回最低必要上游层解决。

### `SUPPORT_REFERENCE_AUTHORITY_FAIL`
- Support Ref重设计Canon；
- Shot Anchor改变Approved Storyboard；
- Support Ref承担未授权Identity / Geography；
- 临时Support长期冒充Persistent State；
- 同一风险被Coverage / Support / Anchor重复建图并产生冲突。

→ 修正Owner与Authority边界。

---

## 11｜Stop Rule

本引擎的目标不是“图片越多越保险”，而是：

> **在昂贵Video开始前，不让模型对关键静态事实做本可提前消除的猜测。**

当当前Shot所有高价值静态不确定性已经由最直接的Approved Authority / Coverage / Support / Storyboard解决后，立即停止新增图片。

## V4.5.7｜Performance Support分流

若静态风险的Primary问题是**人物表情形态 / 人体姿态 / Contact Pose本身**，并且需要在Character/FMH Base Authority之上形成可复用的人物表演证据，优先进入`performance_asset_requirement_engine.md`，建立`PERFORMANCE_SUPPORT_AUTHORITY`。本引擎继续处理更通用的交互几何、短暂状态、机关使用和对象Action State。两个系统不得对同一字段平权重复建图。
