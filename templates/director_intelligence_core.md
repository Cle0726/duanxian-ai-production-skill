# Director Intelligence Core（导演智能核心） Current Authority

> **Stage 02 Input Gate：** 正式Director Intelligence只读取当前`EPISODE SCREENPLAY LOCK`作为Story/Scene Authority。旧Story Lock、小说原段、未批准Screenplay Draft只能作为Source Evidence，不能绕过Stage 01直接进入Shot/Camera设计。
> **用途：** 重构Stage 02上半层。先做导演解释与审美选择，再做Blocking / Camera / Shot；最后才进入AI执行翻译与资产规划。
>
> **核心原则：** `Story Truth → Audience Experience → Directorial Interpretation → Department Critique → Director Judge → Sequence Arc → Staging / Camera / Shot → AI Execution Translation`。
>
> **禁止反向驱动：** Reference槽位、已有资产数量、免费额度、模型“喜欢什么镜头”、Prompt容易写什么，都不能在Director Judge之前决定导演方案。

## 1｜Directorial Importance Tier

每个Scene先分类，避免所有小场都跑昂贵辩论：

- `D0 CONNECTIVE`：纯连接/功能性短场；1个导演方案即可，但仍要写Audience Change + Sequence Function，并由Director Judge做轻量确认，形成D0 Decision Card；不要求为了凑数制造假Option或三部门辩论。
- `D1 DRAMATIC`：有明确关系、信息或情绪变化；至少2个真正不同的导演Interpretation，再做轻量Critique + Judge。
- `D2 SIGNATURE`：关键情绪、首次重要登场、变身、重大揭示、核心战斗、Episode转折；至少3个Interpretation，完整Actor / Cinematographer / Editor Critique + Director Judge。

复杂度不是Tier唯一依据。一个安静的两人对话也可以是D2。

### Approved Director Grammar Context
如项目已有`director_taste_grammar_bible.md`中的APPROVED Grammar，可在提出Options前读取其`Context / Audience Effect / Preferred Strategy / Exceptions`。它只提供审美记忆，不提供现成Shot答案；当前Scene如果与Grammar Context不匹配，直接不用。

## 2｜Audience State Before Camera

在讨论Shot Size之前先回答：

```text
Audience Knowledge IN：观众进场前知道什么 / 误以为什么
Audience Emotion IN：观众进场前主要处于什么感受
Dramatic Question：这一场观众真正等待什么答案/变化
Felt Intent：这场戏主要想让观众“身体上/情绪上”感到什么
Audience Knowledge OUT：离场时新增/修正/失去什么认知
Audience Emotion OUT：离场时情绪被推到哪里
Withheld Information：故意暂时不给观众什么
Reveal Event：何时、通过谁/什么空间关系让它出现
```

`Felt Intent`必须是观众体验，不是摄影词：
- 合法：“让观众先感到主体的行动受阻，再意识到更大的环境规则已经改变。”
- 不合法：“用长焦+慢推制造压迫。”——这是实现，不是Intent。

失败：`AUDIENCE_STATE_UNRESOLVED`。

## 3｜Scene Directorial Thesis

在Audience State基础上形成一句**导演命题**：

```text
Directorial Thesis = 谁/什么控制观众注意力 + 关系如何变化 + 信息如何被给予/拒绝
```

例：
- “不把次要对象当戏剧中心；始终让主体的行动落进一个拒绝回应的空间，直到环境本身成为观众真正读到的压力。”
- “先让观众误以为这是普通医疗谈话，再逐步让门口距离和沉默把‘治疗’变成伦理威胁。”

不能只是“悲伤、紧张、电影感、压迫”。

失败：`DIRECTOR_THESIS_ABSTRACT_FAIL`。

## 4｜Directorial Interpretation Candidates

候选不是三条Prompt，也不是同一镜头换焦段。每个候选必须改变至少两个**导演层变量**：
- POV / Alignment：跟谁看；
- Spatial Thesis：谁被空间压住 / 谁控制空间；
- Reveal Strategy：先给什么、后给什么；
- Temporal Strategy：长镜 / 碎切 / 留白 / 延迟；
- Distance Strategy：何时靠近/拒绝靠近；
- Reaction Strategy：是否给Reaction、何时不给；
- Sound/Silence Strategy：声音是否主导揭示；
- Visual Motif / Negative Space Strategy。

候选模板：

```text
OPTION A｜<一句导演解释>
Audience Alignment：
Spatial Strategy：
Reveal / Withhold：
Temporal / Cut Strategy：
Distance / Perspective Arc：
Performance Emphasis：
Sound / Silence Role：
Signature Image / End Image：
Narrative Strength：
Risk / Cost to Meaning：不是AI成本，而是可能伤害叙事的地方
```

### Option Diversity Gate
如果A/B/C只是“Wide / Medium / Close”“静止 / 慢推 / 稍快推”的表面变化，标`DIRECTOR_OPTION_COLLAPSE`，重新提出真正不同的导演解释。

### Option Purity Gate｜导演候选不得被生产条件偷渡
在Director Judge锁定前，Option正文与选择理由不得使用以下内容作为优劣依据：
- “现有资产已经有这个角度”；
- “这个镜头模型更容易生成”；
- “Reference槽位不够”；
- “当前平台只有某些固定时长档位/最大时长”；
- “这样更省Video成本”；
- “某张Assembly已经做出来了所以就沿用它的构图”。

这些都属于后续Execution Translation。候选阶段只允许讨论**叙事含义、角色真相、空间/摄影逻辑、时间/剪辑逻辑、声音/沉默和观众体验**。若生产信息进入Option选择理由，标`DIRECTOR_PREMATURE_PRODUCTION_CONTEXT_FAIL`并重跑候选。

## 5｜Department Critique

Critique不是投票，也不是自动推翻导演。各部门只从自己的专业职责挑战方案。

### Actor Critique
检查：
- Blocking是否来自角色Objective / Tactic / Relationship，而不是为了画面好看；
- 是否逼角色做“导演想看”的反应，而不是角色此刻会做的事；
- 沉默、克制、主动/被动是否符合人物；
- 哪个Option最容易保住演员Thought Continuity。

输出：`ACTOR_SUPPORT / ACTOR_CONCERN / ACTOR_REJECT_REASON`。

### Cinematographer Critique
检查：
- POV与镜头距离是否服务Thesis；
- 空间、轴线、纵深、负空间是否形成视觉因果；
- 是否存在Generic Coverage / 安全双人中景 / 无意义慢推；
- 哪个Option具有真正可辨识的摄影组织，而不是“好看镜头堆砌”。

输出：`DP_SUPPORT / DP_CONCERN / DP_REJECT_REASON`。

### Editor Critique
检查：
- Sequence里的信息增量；
- Cut是否真的改变知识/权力/动作/空间/节奏；
- Reaction Shot是否过量；
- 是否可以不切得更有力量；
- Reveal与Withhold是否在正确时间发生。

输出：`EDITOR_SUPPORT / EDITOR_CONCERN / EDITOR_REJECT_REASON`。

### Conditional Specialists
只在相关时加载：
- Combat / Action：Action/Combat Choreography；
- Transformation：Transformation Presentation；
- Crowd：Crowd Presence；
- Sound-led Scene：Sound/Silence Review；
- Environment-dependent Scene：Production Design / Geography Constraint。

**Production / AI feasibility不属于艺术部门投票。** 它只能在Director Judge后提出Execution Risk，不能提前把“模型容易生成”当成选择理由。

## 6｜Director Judge

导演必须做最终裁决，不使用多数票。

```text
SELECTED OPTION：A / B / C / SYNTHESIS
Why This Serves Audience Best：
What Was Rejected：
Rejected Because：<叙事/角色/摄影/剪辑原因>
Accepted Critiques：哪些批评进入最终方案
Rejected Critiques：哪些意见有道理但不适合本场，为什么
Non-Negotiable Directorial Invariants：进入后续Stage后不可被生产层静默改写的3–7条核心关系
```

`SYNTHESIS`必须说明保留了哪些Option的什么，不得变成“全部都要”。

**Synthesis Revalidation：** 如果SYNTHESIS只是接受某个部门对Selected Option的局部修正，可直接锁定；如果它实质组合了两个以上Option的POV / Reveal / Temporal / Distance / Reaction / Spatial Strategy，必须让**受影响部门**对合成后的方案做一次Targeted Re-Critique，再由Director Judge确认。未经复核的实质合成不得锁定。

失败：
- `DIRECTOR_JUDGE_UNRESOLVED`
- `DIRECTOR_SYNTHESIS_MUSH_FAIL`（把所有意见混成无主次方案）
- `DIRECTOR_SYNTHESIS_UNREVIEWED`（实质合成后没有对受影响部门复核）

## 7｜Sequence Before Shot

Director Judge完成后，先建立整场/整段`Sequence Arc`，再设计Shot。

至少回答：
- Opening Image Function；
- Beat-to-Beat Attention Owner；
- Information Withhold / Release；
- Distance / Perspective Arc；
- Performance Access Arc（何时看脸、何时不看）；
- Reaction Economy；
- Cut Density Arc；
- Sound / Silence Arc（适用时）；
- Closing Image Function。

Sequence成立后才进入Dramatic Geometry / Blocking / Axis / Detailed Shot Contract。

失败：`SEQUENCE_ARC_FLAT_FAIL`。

## 8｜AI Execution Translation Boundary

Director Core选定后，才允许读取AI平台约束、Reference槽位、当前可靠Platform Duration Profile、资产现状、静态图ROI等。

Production Translation可以：
- 若当前真实平台Hard Max确实需要，把一个导演Sequence在自然边界拆成多个可执行Segment；
- 建Coverage / Assembly / FMH / Support / Anchor；
- 为模型稳定把同一导演动作拆成更明确执行链；
- 调整输入Reference方式。

Production Translation**不能静默改变**：
- Audience Alignment；
- Reveal顺序；
- 核心Blocking关系；
- POV；
- 是否给/不给关键Reaction；
- Sequence的关键Cut / Hold；
- Non-Negotiable Directorial Invariants。

如果AI执行或后续真实Approved Geography / Asset Reality确实无法保持其中某项，输出：
`AI_EXECUTION_CONSTRAINT_CONFLICT`或`DIRECTOR_INVARIANT_SPATIAL_CONFLICT` → 列出冲突 → 返回Director Judge做**明确导演妥协**。

一旦妥协改变任一Director Invariant，不得只Patch某个Shot文本：必须更新`DIRECTOR_INTELLIGENCE_DECISION_CARD`，重跑受影响的Sequence Arc，再最小传播到Director Architecture → Segment / Previs / Asset Need。

不得自动用“模型更稳的普通镜头”替代。

失败：`AI_CONSTRAINT_BACKDRIVE_FAIL / DIRECTOR_COMPROMISE_PROPAGATION_GAP`。

## 9｜Anti-Generic Directing Gate

以下模式若没有当前Scene特定原因，视为Generic Coverage风险：
- Establishing → 双人中景 → 正反打 → Reaction → Wide收尾机械套用；
- 每句台词切一次；
- 每次情绪变化都慢推；
- 重要人物登场默认低机位Hero Shot；
- 所有反应都给脸；
- 所有角色都完整展示；
- 关键情绪一定Close-up；
- 用“电影感 / cinematic / dramatic lighting”代替导演解释。

不是禁止这些镜头，而是**每次使用必须能回指Selected Thesis / Sequence Function**。

失败：`GENERIC_COVERAGE_FALLBACK_FAIL`。

## Current｜Director Perception & Anti-Pattern Memory

> **Authority upgrade：** 本节拥有`UNRESOLVED_STATE / RELATIONAL_PRESSURE / SHOT_GRAMMAR_HISTORY / CREATIVE_DRIFT_TELEMETRY`的导演语义。它不拥有具体Lens、Camera Height、Cut Type或Prompt措辞。

### A｜Unresolved State Before Camera
在任何D1/D2 Scene进入摄影设计前，先写：

```text
UNRESOLVED_STATE
What Character Wants：
What Prevents Resolution：
Why It Cannot Resolve Now：
What Can Change The State：
```

D0 Connective允许写`connective_exception_reason`，但不能用“只是过场”绕过真正存在的戏剧压力。

抽象情绪不算Unresolved State。“悲伤 / 紧张 / 神秘”必须进一步落到角色此刻无法立即解决的具体矛盾。

### B｜Relational Pressure
随后写：

```text
RELATIONAL_PRESSURE
Pressure Source：
Pressure Target：
Knowledge Asymmetry：
Power Asymmetry：
Spatial Constraint：
Social Constraint：
```

没有明显不对等时允许明确写`NONE / BALANCED`，但不得留空。该结构只说明关系压力，不提前决定门框、特写、长焦等实现。

### C｜Shot Grammar History
`DIRECTOR_RUNTIME.shot_grammar_history`只记录已经Locked/Approved的Shot Grammar签名，不记录废弃候选。它用于回答“最近到底拍了什么”，字段包括景别家族、Viewpoint Role、Camera Ethics、主要构图机制、Camera Character、Cut Type、特殊光学事件和Breathing/Peak角色。

历史是**审美记忆，不是禁用列表**。重复可以是有意风格；若当前Scene明确需要重复，记录`intentional_pattern_reason`即可。不得为了降低统计重复率而随机换角度。

### D｜Creative Drift Telemetry
跨Sequence / Episode仅发出Warning：
- `SHOT_SCALE_BIAS`
- `CAMERA_ETHICS_BIAS`
- `VIEWPOINT_ROLE_BIAS`
- `COMPOSITION_PATTERN_COLLAPSE`
- `CAMERA_CHARACTER_BIAS`
- `EDITORIAL_PATTERN_COLLAPSE`

这些Warning必须由Director判断是`INTENTIONAL_PATTERN`还是无意识坍缩；**不能自动强迫多切、广角、鱼眼或陌生机位**。

Hard Fail：`UNRESOLVED_STATE_GAP / RELATIONAL_PRESSURE_GAP`。
