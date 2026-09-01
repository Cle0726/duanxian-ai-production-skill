# Editorial Grammar Engine（剪辑语法与视角切换引擎）｜Current Authority

> **用途：** 为《断弦之歌》建立独立的剪辑Authority。摄影语言回答“当前Shot怎么看”，本文件回答“为什么此刻切、切到谁/什么视角、切后观众获得什么，以及整段Sequence如何形成节奏”。
>
> **核心：** `Audience State → Viewpoint Role → Edit Trigger → Cut Timing → Continuity Strategy → Information Delta → Rhythm Landing`。
>
> **执行策略边界：** `EDITORIAL_PLAN.editing_mode`只表达剪辑意图是否允许模型内Multi-shot；实际一次生成装入几个Formal Shot、采用哪种`FORMAT_MODE`，由`generation_envelope_engine.md / GENERATION_ENVELOPE`拥有。`ASSEMBLY_FIRST`仍是稳定回退；当目标Provider支持受控Multi-shot且证据完整时，可由Generation Envelope把相邻Formal Shots打包进同一次调用。

## 1｜Authority Boundary

### 本文件唯一拥有
- Sequence级 `Viewpoint Arc`；
- `Editing Mode`：`ASSEMBLY_FIRST / IN_MODEL_MULTISHOT`，这里只表示“是否允许模型内多镜头”的Director/Editorial策略，不等同于实际Provider `FORMAT_MODE`；
- 每个真实Cut的 `Edit Function / Cut Trigger / Cut Timing / Transition Type`；
- `Continuity Strategy`与有意不连续设计；
- `Audio Bridge`（J-cut / L-cut / Sound-led Cut）的画面剪辑意图；
- `Editorial Hold / Tail / Handle`需求；
- Sequence级 `Cut Density / Rhythm Contrast`；
- Stage 06最终组接时的Planned Editorial EDL语义。

### 本文件不拥有
- Camera Height / Angle / Subject View / Lens / Focus / Stabilization：归`cinematography_grammar.md`；
- Camera Path / Speed / Landing Geometry：归`camera_motion_contract.md`；
- Actor Blocking / Performance：归Director / Performance Authority；
- Shot Relation中的世界/空间证明：归`SHOT_RELATION_GRAPH + SPATIAL_CANON`；
- 正式BGM、混音：归Stage 06 Post。

**剪辑不能反向发明一套新的摄影机事实。** 如果为了成立某个Cut必须改变既有Shot Contract，返回Stage 02做最小Director Patch。

## 2｜Viewpoint Role（视角职责）

每个Formal Shot按“观众此刻站在哪里”选择一个主职责，不为丰富而随机换角度：

- `OBJECTIVE_OBSERVER`：相对客观地读空间、多人关系或完整动作；
- `CHARACTER_ALIGNED`：贴近某角色的主观关注，但不是严格POV；
- `OTS_RELATIONAL`：从一方肩后读取关系、权力和视线；
- `POV_DIRECT`：严格角色所见；
- `REACTION_ACCESS`：观众被允许读某人的反应；
- `DETAIL_EVIDENCE`：道具、手、伤势、眼睛、接触等证据；
- `ENVIRONMENT_WITNESS`：让环境/空间本身承担信息；
- `DISTANT_OBSERVATION`：远距离观察、监视、隔离感；
- `DISORIENTED_SUBJECTIVE`：有明确叙事原因的失衡主观；
- `OTHER`。

`Viewpoint Role`不是Shot Size替代品。同一角色对齐可以Wide，也可以CU；真正景别仍由Cinematography Grammar决定。

## 3｜Cut Trigger（切点触发）

每个CUT必须有一个主触发。常用合法触发：

- `INFORMATION_CHANGE`：新信息进入或旧信息被重新解释；
- `GAZE_TRIGGER`：视线落到某对象后切到对象/POV；
- `ACTION_TRIGGER`：动作开始、接触或完成触发切换；
- `REACTION_THRESHOLD`：不是“有人说话就切”，而是反应跨过值得看的阈值；
- `POWER_SHIFT`：空间/关系权力改变；
- `SOUND_TRIGGER`：声音先建立下一信息或空间；
- `RHYTHM_TRIGGER`：停顿、冲击、节奏对比本身承担戏剧功能；
- `SPATIAL_REORIENTATION`：观众需要重建空间；
- `TEMPORAL_ELLIPSIS`：有意省略时间；
- `MOTIF_MATCH`：形状、动作方向、构图或主题母题形成连接；
- `TRANSFORMATION_REVEAL`；
- `OTHER`。

禁止把“镜头够久了”“想丰富一点”“每句台词换一边”当合法Cut Trigger。

## 4｜Cut Timing（切在动作/感知的哪里）

Cut不能只有类型，还要有时机：

- `BEFORE_ACTION`：切到新视角后动作才发生，制造期待/预告；
- `ON_ACTION`：动作中切，利用运动连续隐藏切点；
- `AFTER_ACTION`：动作完成后保留结果，再切到后果/反应；
- `ON_GAZE_LANDING`：视线落定后切所见；
- `BEFORE_REACTION`：先给反应位，让观众等待信息穿透；
- `ON_REACTION_LEAK`：微表情开始泄露时切入；
- `AFTER_REACTION_HOLD`：让反应成立后再离开；
- `ON_SOUND_PRELAP`：下一Shot声音先进入，再切画面；
- `ON_SOUND_TAIL`：画面先切，上一Shot声音延后；
- `ON_IMPACT`：接触/冲击节点；
- `ON_SILENCE`：声音骤停或留白成为切点；
- `OTHER`。

## 5｜Transition Type（转场类型）

默认优先`HARD_CUT`。只有叙事需要时使用：

- `HARD_CUT`
- `MATCH_CUT`
- `SMASH_CUT`
- `J_CUT`
- `L_CUT`
- `DISSOLVE`
- `FADE`
- `WIPE_OR_GRAPHIC_TRANSITION`（必须有明确风格/叙事理由）
- `JUMP_CUT_INTENTIONAL`（只用于明确时间压缩/主观断裂）
- `OTHER`

不要用Dissolve/Fade掩盖没有Cut Motivation的问题。

## 6｜Continuity Strategy（连续性策略）

每个相邻Shot至少明确最主要的连续策略：

- `MATCH_ON_ACTION`
- `EYELINE_MATCH`
- `SCREEN_DIRECTION_HOLD`
- `SPATIAL_ANCHOR_HOLD`
- `GRAPHIC_MATCH`
- `MOTION_VECTOR_MATCH`
- `SOUND_BRIDGE`
- `PERFORMANCE_CONTINUITY`
- `PROP_STATE_CONTINUITY`
- `LIGHT_COLOR_CONTINUITY`
- `INTENTIONAL_DISCONTINUITY`
- `NONE_REQUIRED`

如果选择`INTENTIONAL_DISCONTINUITY`，必须写Audience Effect；不能把轴线错乱、动作跳变包装成“实验剪辑”。

## 7｜Viewpoint Arc（整段视角弧线）

Sequence不能只做“Wide → Medium → Close”的机械景别阶梯。至少回答：

```text
Opening Viewpoint：观众从谁/什么位置进入
Alignment Owner：观众最初跟谁
Access Escalation：什么时候允许更靠近/更主观
Viewpoint Transfer：什么时候把注意权交给另一角色/对象/空间
Denial：什么重要反应故意不切给观众
Reveal Viewpoint：关键Reveal由谁的视角或什么证据完成
Closing Viewpoint：结束时观众被留在哪一边
```

一个健康的Sequence可以长时间不切；关键是**每次切都改变观看关系**。反过来，即使切很多，如果所有镜头都还是同一人物、同一高度、同一方向、同一信息，也仍然是单一。

## 8｜Editing Patterns（可调用剪辑方法，不是固定模板）

### 8.1 Gaze → Object → Reaction
角色注意到某物 → 切对象/证据 → 选择是否立即给Reaction。适合线索、危险、欲望、怀疑。

### 8.2 Action → Consequence
动作启动或接触点切换 → 下一Shot优先证明后果，而不是重复同一动作。

### 8.3 Wide → Insert → Return
先建立空间 → 插入关键小证据 → 回到原关系确认后果。Insert必须有信息职责。

### 8.4 Withhold → Reveal
故意不给观众关键面孔/对象 → 到阈值才切给完整信息。适合威胁、变身、关系揭示。

### 8.5 Asymmetric Dialogue
不自动正反打。可以长期留在一方、用Two-shot/OTS/环境阻隔；只有权力、理解或压制失败改变时才把Performance Access交给另一方。

### 8.6 Sound-led Cut
下一空间的声响先进入（J-cut）或上一空间声音延后（L-cut），用于引导、连续、悬念或隐藏硬切。

### 8.7 Match Cut
用动作方向、形状、姿态、构图、母题或声音连接两个不同Shot。必须有真实可匹配Anchor。

### 8.8 Parallel / Intercut
两个并行事件轮换，每次返回都必须增加压力、知识或因果；禁止纯粹A/B轮播。

### 8.9 Elliptical Cut
省略不值得展示的过程，但Entry/Exit State必须连续可推断。

### 8.10 Smash / Contrast Cut
从高压到静止、从安静到冲击、从亲密到空旷等强反差；必须服务戏剧，不作为“酷”的默认转场。

## 9｜Editing Mode

### ASSEMBLY_FIRST（稳定回退 / 默认安全策略）
- `1 Formal Shot → 1 Approved Video Clip`；
- Shot内部通常`NO CUT`，但Camera可以合法运动；
- 视角变化通过相邻Formal Shots实现；
- Stage 06根据`EDITORIAL_PLAN`剪接Approved Clips；
- 优点：身份、空间、动作、构图、Color和Ending State更稳定，可单独Retry某一角度。

### IN_MODEL_MULTISHOT（允许Generation Envelope尝试受控Multi-shot）
只有同时满足时可用：
1. Director明确认为“一次模型内切镜”本身有价值；
2. 目标模型经过验证能稳定执行Multi-shot；
3. 每个子Shot有独立Shot Contract / Storyboard Evidence / Conditioning Evidence；
4. Cut Timeline没有与人物动作、空间、Reference产生未解冲突；
5. 失败后允许降级为ASSEMBLY_FIRST，而不重写导演意图。

**禁止为了“片段里看起来会切镜”随意启用IN_MODEL_MULTISHOT。** 但一旦Director允许且Provider能力/证据满足，后续不再强制`1 Shot = 1 Generation`；实际打包交给`GENERATION_ENVELOPE`。

## 10｜Editorial Plan结构

```text
EDITORIAL PLAN
Sequence ID：
Editing Mode：ASSEMBLY_FIRST / IN_MODEL_MULTISHOT
Opening Viewpoint：
Viewpoint Arc：
Cut Density Arc：
Rhythm Strategy：

SHOT VIEWPOINT MAP
- SH01：Viewpoint Role / Entry Function / Exit Function / Performance Access
- SH02：...

EDIT POINTS
- E01：SH01 → SH02
  - Edit Function：
  - Cut Trigger：
  - Cut Timing：
  - Transition Type：
  - Continuity Strategy：
  - Information Delta / Audience Change：
  - Audio Bridge：NONE / J / L / SOUND_MATCH
  - Required Tail / Handle：
  - Forbidden Failure：

Closing Viewpoint：
Status：DRAFT / LOCKED / REVISE_REQUIRED
```

机器结构见`state/editorial_plan.schema.yaml`。

## 11｜Stage 02 / 04 / 05 / 06边界

### Stage 02
Sequence Arc之后先建立`Editorial Intent Draft`：锁Viewpoint Arc、哪些Beat需要Hold/Transfer/Reveal以及切换触发原则；此时不要求已经有全部Shot ID。Director Architecture形成Shot Progression后，再把Draft映射为具体Formal Shots与Edit Points，并与Detailed Shot Contracts**同步锁定**为`EDITORIAL_PLAN=LOCKED`。不能先机械拆一堆Coverage，再事后补“为什么切”。

### Stage 04
每个Formal Shot有Mandatory Clean Storyboard Panel；相邻Panel/Board证明：
- Cut前后的Attention Target成立；
- Axis / Screen Direction / Eyeline / Action Vector满足Continuity Strategy；
- Reveal没有提前泄露；
- Insert / Reaction / POV确实承担指定信息；
- Cut点需要的Exit/Entry构图可执行。

### Stage 04B / Generation Envelope Handoff
Stage 04所有Formal Shot的Mandatory白描Panel批准后，由`generation_envelope_engine.md`决定执行打包：
- `ONER`：一个Formal Shot一个Envelope；
- 非`ONER`：两个以上相邻Formal Shots进入同一Envelope；
- **任何非ONER Envelope都必须把各CUT的Approved白描Panel按CUT顺序运行`storyboard_grid_assembler.py`得到白描宫格，并通过`MULTISHOT_STORYBOARD_GRID_GATE_PASS`。**

### Stage 05
Final Video Prompt不再假设永远只执行一个Formal Shot，而是执行**当前GENERATION_ENVELOPE**：
- ONER：只编译当前Formal Shot，模型内`NO CUT`；
- Multi-shot：按`CUT_CONTRACT[]`明确编译`SHOT BLOCK → CUT → SHOT BLOCK`，不得新增或省略Cut；
- 每个CUT继续保护`Edit Entry State / Protected Moment / Edit Exit State / Continuity Handoff`；
- Multi-shot白描宫格可作为结构辅助Reference，但永远不是Primary Visual；
- Provider不稳定或失败时，可降级为Single-shot Envelopes + Stage 06 Assembly，不得修改Editorial Plan。

### Stage 06
以`EDITORIAL_PLAN`作为Picture Assembly的意图Authority；Approved Video Take提供真实素材Evidence。允许因真实Take质量做最小Editorial Salvage，但不得把Director已锁的Reveal、POV、Reaction Give-Deny、关键Hold/Cut静默改掉。

## 12｜Hard Fail / Warning

### Hard Fail
- `EDITORIAL_PLAN_GAP`：正式Sequence没有Locked Editorial Plan；
- `CUT_TRIGGER_MISSING`：真实Cut没有主触发；
- `CUT_INFORMATION_FUNCTION_GAP`：Cut既无信息/权力/空间/节奏变化，也无明确保留理由；
- `EDIT_RELATION_MISMATCH`：Editorial Plan与SHOT_RELATION_GRAPH相邻关系冲突；
- `EDIT_CONTINUITY_CONFLICT`：轴线、动作向量、视线、Prop/Performance连续性无法满足且不是有意不连续；
- `IN_MODEL_MULTISHOT_EVIDENCE_GAP`：模型内多镜头缺少独立子Shot证据；
- `MULTISHOT_STORYBOARD_GRID_MISSING`：非ONER Envelope没有对应白描宫格；
- `MULTISHOT_STORYBOARD_GRID_ORDER_MISMATCH`：宫格Panel顺序与CUT顺序不一致；
- `GENERATION_ENVELOPE_FORMAT_CONFLICT`：Shot/Cut数量与FORMAT_MODE冲突。

### Warning
- `VIEWPOINT_STAGNATION_RISK`：连续多个Shot保持相同视角职责、景别家族和主体方向，且没有Sustained策略说明；
- `MECHANICAL_REVERSE_SHOT_RISK`：机械A/B正反打重复，没有Power/Knowledge/Performance Access变化；
- `CUT_DENSITY_FLAT_RISK`：整段切点间隔过于机械；
- `REACTION_OVER_COVERAGE_RISK`：每句对白都自动切Reaction。

Warning用于提醒单调风险，不自动强迫多切。

## Current｜Information Causality, Hold Weight & Shuffle Test

### Information State Per Shot
每个Formal Shot不只写Cut后的`information_delta`，还维护：

```text
Information State IN：观众进入此镜前已知/误以为的事实
Information Revealed：此镜新增或修正的可读信息
Information Withheld：导演主动继续不给的信息
Information State OUT：离开此镜时观众的新状态
```

Breathing Shot可以几乎不Reveal，但仍必须明确IN/OUT；“什么都没发生”不等于“没有功能”。

### Sequence Logic
每个Sequence明确：
- `CAUSAL`：顺序改变会破坏因果/信息/动作/视线/声音依赖；
- `ASSOCIATIVE`：顺序主要由联想、主题或情绪组织；
- `MONTAGE`：通过并列/压缩形成意义。

### Editorial Weight
每Shot选择：`TRANSIENT / NORMAL / EMPHASIS / HOLD`。它表达观众应在该镜停留的相对权重，不直接等于固定秒数。

### Breathing Function
合法的低信息镜头：`DECOMPRESSION / ANTICIPATION / SPATIAL_REORIENTATION / EMOTIONAL_DELAY / TEMPORAL_REALISM`。无特殊功能写`NONE`。不得为了“每镜都有信息爆点”删除必要呼吸。

### Sequence Shuffle Test
CAUSAL Sequence在锁定前必须做反事实检查：若交换关键相邻Shot仍几乎不损失因果、知识、动作、Eyeline或Audio Dependency，则`SEQUENCE_SHUFFLE_TEST_FAIL / EDITORIAL_CAUSALITY_WEAK`，回到最小受影响Shot Relation。

`ASSOCIATIVE / MONTAGE`允许Shuffle不构成Hard Fail，但必须写清组织原则与为什么当前顺序仍然更好。

**注意：** Shuffle Test不是强迫所有Sequence“剧情化”。它只验证当前声明的Sequence Logic是否诚实。

### Anti-closeup Editorial Warning
Sequence内特写比例偏高只发`SEQUENCE_CLOSEUP_BIAS_RISK`；真正能否使用特写由Cinematography的`SHOT_SCALE_JUSTIFICATION`裁决。禁止Editorial为了统计平衡强插Wide。

Hard Fail：`SEQUENCE_LOGIC_GAP / SHOT_INFORMATION_STATE_GAP / SEQUENCE_SHUFFLE_TEST_GAP / SEQUENCE_SHUFFLE_TEST_FAIL`。
