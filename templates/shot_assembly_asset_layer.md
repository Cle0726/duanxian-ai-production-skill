# Shot Assembly Asset Layer（镜头组装资产层）

> **用途：** 本模板用于 Stage 02 → Stage 03，补齐“设定资产已经齐了，但真正昂贵的视频镜头仍缺少一张可执行静态组装图”的情况。
>
> **核心定义：** `SHOT_ASSEMBLY_ASSET` 不是Storyboard宫格，不是Ending Frame，不是直接拿分镜低清图放大；它是一张**高质量静态资产图**，由已批准的人物、场景、道具、状态与当前Scene光色组装而成，用来提前解决“这一类镜头里人物如何进入场景、道具如何出现在手里、站位关系如何成立”的问题。

---

## 1｜为什么需要这一层

仅有以下资产仍可能不够拍：
- Character / Environment / Prop Canon Master；
- Derived Coverage；
- Production Support Reference；
- 文字化的Director Intent。

因为视频模型真正容易猜错的常常不是“对象是什么”，而是：
- 人物如何位于场景中；
- 人与人的前后关系；
- 人与道具在当前镜头中的接触关系；
- 医院、车内、舞台等复杂空间里谁处于哪个功能位置；
- 这一镜是更接近关系中景、半全景、对置构图还是偏侧面观察。

当这些问题如果不提前用静态图组装出来，会显著提高后续视频失败率时，应建立`SHOT_ASSEMBLY_ASSET`。

---

## 2｜与其他层的边界

### 2.1 不是Canon Master
它不重新定义角色长相、场景地理、道具结构。所有基础身份与结构继续来自已批准Canon / Coverage。

### 2.2 不是Production Support Reference
Support更偏“局部高风险证据”：扶抱、压伤、递交、机关、伤口、一次性形态、轻量小道具。

`SHOT_ASSEMBLY_ASSET`更偏**整镜或整类镜头的组装关系**：
- Character A + Scoped Figure B + Environment C + Key Prop/Lighting State；
- 三人 + 旅行车内 + 节目单 + 视线关系；
- 演员 + 舞台 + 钢琴 + 幕布 + 退场通道。

### 2.3 不是Storyboard
Stage 02 Detailed Shot Contract负责Shot层的距离、轴线、Blocking、Camera Intent与视觉主次；Storyboard负责把已Reconciled的导演契约落实成具体Panel构图、剪辑执行与动作Anchor，允许低清与抽象。

`SHOT_ASSEMBLY_ASSET`负责把已知的人/景/物/状态组合成一张高清静态生产图；它可以受导演意图影响，但**不得直接从九宫格/宫格分镜放大或清稿**来冒充资产。

### 2.4 不是Additional Video Conditioning Keyframe
`VIDEO_CONDITIONING_KEYFRAME` 依赖 Approved Storyboard，服务于某一具体Shot的最终视频执行。

`SHOT_ASSEMBLY_ASSET` 属于 Stage 03 资产层，先于正式Storyboard，可服务：
- 一组重复出现的关系镜头；
- 一个复杂情境的前置静态落地；
- 多个同类镜头的关系基准。

---

## 3｜触发条件（Stage 02）

若满足下列任意一类，标记：`SHOT_ASSEMBLY_REQUIRED`

1. **多人关系镜头**：同一镜中至少2个明确人物，且站位/前后关系/谁清楚谁弱化会显著影响镜头可读性。
2. **人物-场景关系关键**：人物在床位、驾驶位、后排、台阶、舞台、门区、柜台等功能位置上的关系很重要。
3. **人物-道具-场景同时成立**：同一镜里必须同时让人物、场景与道具成立，单独看Master不够。
4. **昂贵视频风险高**：这类镜头若靠视频模型自行拼装，极易出现空间错位、站位错位、接触漂移、道具出现在错误手中等问题。
5. **Montage / 一次性情境镜头**：不值得把所有路人和小物都做成正式Canon，但值得直接做一张“情境组装图”。
6. **有复用价值**：后续多个镜头或多个片段会反复以同一关系出现。

---

## 4｜不应触发的情况

以下更适合别的资产层：
- 只缺一个反面/背面/开盖态 → Coverage；
- 只缺伤口、裂纹、血迹、湿损等持续状态 → Persistent State；
- 只缺递交、扶抱、局部接触、插入细节 → Support Reference；
- 只缺具体镜位、剪辑节奏、镜头长短 → Storyboard；
- 只缺动作过程、速度、步态、Camera Motion → Stage 04/05时间系统。

---

## 5｜数据结构：Shot Assembly Need Analysis

```text
| Scene/Shot Group | Core Situation | Character Set | Environment Set | Prop Set | Why Master/Coverage Not Enough | Reuse Scope | Assembly Needed? | Assembly Type |
|---|---|---|---|---|---|---|---|---|
| SC__/SH__ | 主体A + 功能人物B + 场景C | Character A / Scoped Figure B | Environment C | Key Prop D | 需要确定人物、道具、站位与空间/光色关系 | Multi-shot / Montage | YES | CHARACTER_SCENE_PROP_COMPOSITE |
```

### Assembly Type建议
- `CHARACTER_SCENE_COMPOSITE`
- `CHARACTER_SCENE_PROP_COMPOSITE`
- `MULTI_CHARACTER_RELATION_COMPOSITE`
- `MONTAGE_SITUATION_COMPOSITE`
- `SPATIAL_INTERACTION_COMPOSITE`

---

## 5.1｜Assembly Contract（组装资产契约）

每张Assembly在生成Prompt前先建立以下静态契约。它描述**资产层面的关系落地**，不写视频时间轴，也不替代Storyboard：

```text
Assembly ID：ASM_...
Scope：Episode / Scene / Shot Group
Assembly Type：...
Framing Family：RELATION_WIDE / MEDIUM_GROUP / PROFILE_RELATION / FUNCTIONAL_SPACE_VIEW / INSERT_SITUATION / OTHER
Character Sources：<Approved Character IDs> + <SCOPED_CAST_BRIEF if any>
Environment Source：<Most Direct Approved Master/Coverage>
Prop / Entity Sources：<只列当前组装必须看清的关键项>
Persistent State：<如有>
Spatial Occupancy：谁位于哪个Zone / 前中后层 / 功能位置
Holder / Contact：关键道具属于谁、谁与谁接触
Visibility Priority：哪些脸/手/道具/空间锚点必须清楚，哪些可被部分遮挡
Scene Color / Lighting：当前Scene层级
Canon Locks：不得改变的身份/结构/Geography
Scoped Cast Boundary：<若有，限定Scene/Shot Group>
Not Storyboard：NO CUT / NO TIMELINE / NO PANEL COPYING
```

### 静态姿态原则
- 选择能说明关系、持物、空间位置的**自然中性或剧情相关静态瞬间**；
- 不为表现“动作完整过程”把同一人物画出多个重影/连续姿势；
- 不机械复制某个Storyboard Panel；Director只提供关系/镜头族意图，正式具体Camera仍留Stage 04；
- 若一个Assembly无法同时清楚表达两个互相冲突的关系目标，应拆为两个有明确Scope的Assembly，而不是在一张图塞多个方案。

---

## 6｜Stage 03生成规则

生成时必须满足：
1. 反复/命名/后续可识别人物已有Approved Character Authority；**一次性Montage/匿名功能人物**可由Stage 02明确建立`SCOPED_CAST_BRIEF`，不强制先做项目级Character Master；
2. 已有Approved Environment / 关键Prop Authorities（若该镜实际需要）；
3. 对新Environment已经完成`DIRECTOR GEOGRAPHY PRECHECK PASSED`；若Stage 02导演关系与真实Geography冲突，必须先Patch Director Contract，再生成依赖它的Assembly；
4. 当前Scene Color Extension / Lighting Baseline已明确；
5. 当前Persistent State若必要已建立；
6. 当前任务目标是“资产层面的高清静态组装”，不是剧情分镜草图。

输入角色：
- Character Authorities（反复/命名人物）
- `SCOPED_CAST_BRIEF`（仅一次性Montage/匿名功能人物；定义年龄段、职业/社会身份、服装逻辑、必要外貌差异，不建立全项目身份）
- Environment Authority / Coverage
- Required Prop Authorities
- Scene Color / Lighting
- 必要Support Ref（仅辅助局部关系，不篡位）
- Director Assembly Brief（文字）

输出角色：
- `SHOT_ASSEMBLY_ASSET`
- 输入模式：`HD_SHOT_ASSEMBLY_IMAGE`
- 资产性质：`APPROVED ASSEMBLY`（非Canon）

候选策略：默认 **2 Candidates**。

### 6.1｜Scoped Cast Rule（一次性人物范围规则）

对于开场Montage、医院护士、路边母亲、接线员等**只在当前Scene/Shot Group使用、后续不需要识别延续**的人物：
- Stage 02可标记`SCOPED_CAST / NON_RECURRING`；
- Stage 02同时必须建立`SCOPED_CAST_BRIEF`。只要人物清楚可见，Appearance Owner固定为`FMH_ASSET`；若核心风险还有位置/同框/人景物关系，再额外生成`SHOT_ASSEMBLY_ASSET`。不得用Assembly替代人物母图，也不得默认为Video模型自由生成；
- 不要求为了这一镜额外建立完整四视图Character Master；
- `SCOPED_CHARACTER_APPEARANCE_AUTHORITY`只能由对应Approved `FMH_ASSET / MINOR_HUMAN_MASTER`承担；`SHOT_ASSEMBLY_ASSET`批准后仅可承担该范围内的关系、同框、空间占位、Contact、Pose或Transient State Authority，不得取得或替代Appearance Authority；
- 该权限只在记录的Scene/Shot Group有效，不能拿去别的Scene继续冒充同一人物；
- 如果人物后来重复出现、成为剧情线索、必须跨Scene保持身份，必须先升级为正式Character Master，再继续生产。

**已有正式Character Authority的人物绝不能被Assembly重新设计。**

---

## 7｜使用规则

### Stage 04
可将`SHOT_ASSEMBLY_ASSET`作为Storyboard前或Storyboard修订时的高质量关系参考，用于稳定：
- 角色在场景中的相对位置；
- 多角色同时出镜的画面组织；
- 道具位于谁手中、在画内何处。

但具体机位关系必须继承Stage 02 Reconciled Director Contract；Storyboard只精化Panel落点、构图执行与节奏，不重新发明核心机位/Blocking。

### Stage 05
若某段Video主要难点是“关系组合容易猜错”，可将`SHOT_ASSEMBLY_ASSET`作为Primary或Support输入之一；
若已经存在更针对性的`VIDEO_CONDITIONING_KEYFRAME`，则Anchor优先承担具体Shot执行，Assembly退为Support。

---

## 8｜Hard Rules

- 不得直接把Story Grid / 九宫格分镜放大、清稿或作为Assembly资产替代品。
- 不得用Assembly反向改写已有Canon身份、场景地理或道具结构；任何清楚可见的一次性`SCOPED_CAST / NON_RECURRING`都必须先有Approved FMH/Minor Human Master。Assembly只能继承该人物外观并锁当前Scene/Shot Group中的同框、站位、接触和状态，不得另起外观。
- 同一个Assembly组里的候选必须共享同一Task Contract，不得借候选探索不同设计宇宙。
- 只在“多一张静态组装图确实能显著降低昂贵视频风险”时生成；不把所有镜头都资产化。
- 对一次性小物和路人，不优先建Canon；更优先考虑MONTAGE_SITUATION_COMPOSITE。

## 9｜Failure / Freeze Codes
- `SHOT_ASSEMBLY_GAP`：Stage 04/05发现Stage 03本应存在的多人关系/人景物组装资产缺失；Break Freeze回Stage 03只补该Assembly。
- `SHOT_ASSEMBLY_AUTHORITY_FAIL`：Assembly越权改写已有角色/FMH身份、场景地理、道具结构；脱离Approved Base Master另起人物外观；或从Storyboard宫格直接清稿冒充资产。

生成/使用Assembly时仍必须通过`reference_field_coverage_map.md`：Assembly只覆盖它实际承载的关系字段，不能因为有一张Assembly就省掉未被它锁住的关键角色/道具Authority。

## V4.5.5｜Assembly Reality Contract

任何包含人物的`SHOT_ASSEMBLY_ASSET`必须绑定适用`REALISM_CONTRACT`，Assembly Contract新增：

```text
Expected Cast / Count
Character → Zone / Functional Position / Seat
Required Support Surface
Environment Functional Type / Vehicle Type
Capacity / Circulation Constraints
Object Affordance
Social-Spatial Constraints（仅剧情需要）
Scoped Realism Exceptions（若有）
```

Assembly不是“把正确人物塞进正确背景”就完成。人物数量正确但功能位置错、座位关系错、车辆内部被重构、人体与家具不成立、互动距离无因反常，都必须FAIL。只有Canon明确授权的超现实维度可以局部豁免。
