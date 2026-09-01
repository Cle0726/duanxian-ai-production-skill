# Performance Causality & Emotional Acting（表演因果与情绪表演）

> **用途：** 作为 `actor_performance_engine.md` 的下游执行层，把Objective / Tactic / Listening / Adjustment翻译成Stage 04 Storyboard与Stage 05 Video Prompt中的具体可见行为。重点解决：眼睛/眨眼/眉头不自然、无因待机、情绪外露过满或过假、多人场景一起反应、未感知先反应，以及日常对白中“说完一句就停一下、身体归零、明显吸一口气再启动下一句”的机械节奏。

## 核心原则

**先运行Actor Performance Engine。** Performance Causality不能脱离人物Objective / Obstacle / Tactic / Relationship独立生成微动作。

演员逻辑确定后，可见表演因果是：

**Baseline → Stimulus → Perception → Processing Delay → Involuntary Leak → Controlled Response → Body Follow-through → Secondary Reaction → Landing / Continue / New Stable State**

中文：

**原始状态 → 刺激发生 → 人物察觉 → 理解延迟 → 不受控泄露 → 主动控制后的正式反应 → 身体后续动作 → 第二人物反应 → 落点 / 新稳定状态**

`Recovery / New Stable State`不是每句台词都要执行的固定尾动作。同一Objective / Tactic / Thought Intention持续时，表演状态跨句延续；只有真实Beat结束、策略改变、关系判断改变或行动阶段完成时才进入Recovery / New State。

### 核心硬规则｜Abstract Emotion Is Not Performance

`害怕 / 震惊 / 悲伤 / 愤怒 / 紧张 / 关心 / 冷静`只能作为**内部心理标签**，不能单独作为Storyboard / Video模型的表演指令。

重要情绪必须进一步转换为：

**Trigger → Intensity → Visible Signals → Suppression / Reveal → Timing → Landing / Continue / New State**

例如不能只写“她明显受到了惊吓”；必须说明她先看见什么、反应多强、眼神/呼吸/手/下颌/重心中哪些发生了什么、是否压住、持续多久、之后恢复到什么状态。

## Performance Signal Preservation（表演信号保留）

**任何承载人物心理、判断、情绪变化或关系变化的有效微动作，不得仅因为“模型可能难执行”而删除。**

当信息过密时，处理顺序是：
1. **合并**：把属于同一心理因果的细节写成一个连贯表演，而不是独立动作清单；
2. **排序**：明确先看见、再泄露、再控制、再行动；
3. **分时**：把不同信号放在不同0.x秒/动作阶段，而不是要求同一瞬间全部发生；
4. **景别转译**：保留心理信息，但换成当前景别真正看得见的载体；
5. **必要时拆Segment / Shot**：若真正关键的表演与动作无法在当前时长内读清，宁可拆分，不把人物情感删掉。

禁止把一组具体表演压缩成一个抽象词来“省Prompt”。

## A｜Natural Face Behavior（自然面部行为）

### 1. Baseline Face
先定义人物在本Beat开始时的自然脸部基线：
- 眼睑开合状态
- 眉头中性 / 轻紧 / 放松
- 视线落点
- 嘴唇自然闭合 / 微张
- 生理/呼吸基线（通常隐式存在；只有被剧情或生理状态放大时才成为可见表演信号）

### 2. Blink Logic（眨眼逻辑）
- 普通对话允许自然眨眼；
- 情绪被击中时可短暂停止眨眼；
- 转移视线前后、话题切换、恢复镇定时可出现一次自然眨眼；
- 高度专注/警觉通常减少眨眼，不是疯狂眨眼；
- 不要机械每句台词都配一次眨眼。

### 3. Gaze Logic（视线逻辑）
- 明确视线原本落点；
- 触发后视线先看哪里；
- 是否先看对方眼睛，还是先看手、道具、门口；
- 视线是立即偏移还是停顿半拍后偏移；
- 是否重新看回去。

### 4. Brow / Lid Logic（眉眼逻辑）
- 怀疑：眉间轻微收拢；
- 压抑：上眼睑轻微下降或视线稳定但不完全对视；
- 警觉：眼睑先停住，再略提；
- 悲伤：不一定大皱眉，可更多体现在眼神失稳、下眼睑与呼吸。

### 5. Focus / Pupil Logic（焦点逻辑）
不强迫每次都写“瞳孔放大/缩小”。更优先写：
- 聚焦稳定 / 短暂失焦 / 被某点锁住；
- 回神感；
- 关键词出现后注视逻辑如何改变。

## B｜Micro Action Selection（微动作选择）

**每个Beat优先选择1–3个主要Emotional Carrier（情绪载体），不机械填满所有部位。这里的1–3是“主要信息载体”，不是整个人体只能出现1–3个动作。与主载体存在因果关系的次级动作、惯性、呼吸或姿态后续可以自然保留。**

常用微动作库：
- 有明确触发时的换气变化：短暂停住 / 变浅 / 变深 / 恢复
- 拇指压紧、手指停顿、握持张力变化
- 肩线轻降 / 肩颈微紧
- 下颌轻绷
- 重心微偏
- 视线短暂偏离 / 重新锁定

### Shot-scale Translation（景别转译）
心理信息不得因为景别远而被删除，而应换成可见载体：
- ECU / CU：眼睑、焦点、唇压、下颌、必要时可见的细微换气、指尖；
- MCU / MS：视线、手部、肩线、身体朝向、动作速度；只有当前换气本身承载情绪/生理信息时才把它写成可见信号；
- WS / EWS：步伐停顿、重心、距离、身体方向、是否靠近/远离、动作节奏。

例如“想说但忍住”在近景可表现为嘴唇启动后停住；在远景则可表现为身体欲向前一步却停住。**心理含义保留，显示方式随景别改变。**

## C｜Listener Presence（听者存在感）

### Background Listener Rule｜仅明确个体，不等于Crowd
这里的Background Listener指**可识别、可追踪的单个未说话人物**。听者首先遵守`actor_performance_engine.md`的Active Listening：**持续接收，不等于持续做动作。** 若背景是多人群体/群众，不逐人套本规则，改读`crowd_presence_ambient_life_engine.md`。

优先保持：
- 当前Ongoing Task / 姿态 / 空间关系；
- 清楚的注意力落点；
- 已形成的表情/身体状态连续性；
- 对说话内容的理解与当前Tactic。

只有新信息真正改变Meaning / Objective / Tactic时，才推进可见反应，例如：
- 原任务减速或停住；
- 视线从原目标转向说话者/关键道具；
- 手部张力改变；
- 身体距离或朝向改变；
- 有原因的Triggered Stillness；
- 下一句回应的速度、力度或策略发生变化。

自然眨眼与普通生理活动可以存在，但不是为了“证明角色活着”而安排的表演任务。

要求：
- 不得无因待机/冻结；
- 有明确Trigger、注意力落点和后续行动的`Triggered Stillness`属于有效表演；
- 不得逐句打卡反应；
- 不得抢主表演，除非听者反应本身就是镜头目的。

### Listener Emotion
听者不是空白背景，要判断：
- 是否听懂；
- 新信息对当前Objective意味着什么；
- 是否被击中；
- 是否试图掩饰；
- 是否因此调整Tactic、下一句对白或身体行动。

## D｜Reaction Cascade（反应连锁）

对关键刺激建立：
- Trigger Owner：谁制造刺激；
- Primary Perceiver：谁第一个察觉；
- Reaction Latency：立即 / 极短延迟 / 明显延迟 / 压抑后才显露；
- Primary Reaction：第一反应；
- Secondary Perceiver：谁观察到了第一反应；
- Secondary Reaction：第二人物如何响应；
- Physical Follow-through：道具、衣物、重心、环境如何继续响应；
- New Stable State：最终稳定状态。

## E｜Emotional Acting（情绪表演）

### 1. Surface Emotion / Inner Emotion
区分：
- 表面情绪是什么；
- 内在真实情绪是什么。

### 2. Suppression Level（压抑程度）
- HIGH：高压抑型，情绪优先从少数真实泄露点出现，例如手、视线、停顿或被触发后的换气变化；
- MEDIUM：中度克制；
- LOW：较直接外露。

### 3. Emotion Intensity（情绪强度）
可用0–5，但**数字不是模型表演指令，也不按“动了几个身体部位”判断**。强度优先衡量：对Objective/判断影响多大、压住情绪需要多大努力、是否迫使Tactic改变、是否影响声音/动作稳定、泄露持续多久。
- 0 中性：维持Baseline，不为“有戏”强行加反应；
- 1 轻微波动：几乎不改变当前Tactic，只产生极小可读偏移；
- 2 明显但克制：人物感知到变化并需要轻微调整，但整体控制稳定；
- 3 难以完全忽略：情绪开始影响注意力、语速、原任务或策略选择；可以只通过一个高度准确的载体泄露；
- 4 强烈外露：明显改变声音、动作节奏、空间关系或Tactic，但仍有目标行为；
- 5 失控边缘：情绪显著打断原动作、判断、语言或姿态稳定。

Skill必须根据上下文自动判断“多强”，不能把所有惊讶都演成瞪眼后退，也不能为了表现L3/L4机械增加身体部位数量。

### 4. Emotion Arc（情绪弧线）
每个Beat或Shot应写清：
- 起点情绪；
- 触发点；
- 上升 / 压抑 / 迟疑；
- 落点。

### 5. Emotional Leakage（情绪泄露）
人物尝试控制但还是漏出来的细小证据，例如：
- 说话短暂卡顿；
- 视线偏开一瞬；
- 手部动作停顿；
- 嘴唇比平时更紧；
- 眉头轻动后立即恢复。

## E.1｜Psychological Counterforce vs Execution Conflict（心理对抗 vs 执行冲突）

看似相反的表演不一定是错误。先判断：

### A. Psychological Counterforce｜有意义的心理对抗｜保留
例如：
- 害怕，但不后退；
- 想哭，但把嘴唇压紧；
- 生气，但说话仍然平；
- 疲惫，但逼自己维持Guard；
- 想看对方，却故意避开视线。

这种结构通常应写成：
**Involuntary Leak（真实情绪漏出） → Controlled Response（主动压制/伪装）**。
两者同时存在会增加人物真实感，禁止因为“情绪方向不同”而自动删掉其中一边。

### B. Execution Conflict｜真正执行冲突｜修正
只有物理或感知上不能同时成立才算冲突，例如：
- 同一瞬间重心全力向前又全力后撤；
- 眼睛完全闭合同时精准视觉追踪剑尖；
- 同一只手同时松开道具又持续紧握；

这些属于**执行资源冲突**，不要直接删除有意义的心理动作；先交给`action_feasibility_prop_limb_continuity_engine.md`做Limb Occupancy / Support / Minimal Bridge求解。若可改用空闲手或最小换手解决，应保留表演意图；合法后再交给`natural_motion_kinematic_performance_engine.md`决定身体链、动作叠接与自然落位，避免微表情正确但身体动作像机器人。
- 同一瞬间身体完全放松又进行最大力量爆发。

修正方式是调整时序、左右身体部位或动作阶段，不是删除心理信息。

## F｜Keyword Reaction Trigger（关键词反应触发）

对白场景可拆成：
- 哪个词先触发注意；
- 哪个词真正击中；
- 角色在何时做出理解完成的反应；
- 说话者是否因观察到对方反应而调整语速、音量或后半句。

## F.1｜Dialogue Performance Chain（日常对白表演链）

日常聊天不是“说话人嘴动 + 听者待机”。对白优先按：

**Baseline / Ongoing Task → Hear → Interpret → Internal Response → Suppress / Reveal → Visible Signal → Speak → Listener Reaction → Post-line Behavior**

### Subtext（潜台词）
Skill必须判断：
- 这句话字面意思和真实意图是否一致；
- 角色是在坦白、回避、撒谎、试探、敷衍、安慰、挑衅还是转移话题；
- 角色是否希望对方看出真实情绪；
- 对方有没有读到这个泄露信号。

潜台词不是额外台词，而应通过**回答速度、停顿、视线、手上原动作、身体距离、声音力度，以及有明确原因时的换气变化**等具体可观察信号表现。

### Speech-Body Coupling（语言—身体耦合）
一句台词的身体状态要与说话方式连在一起。例如同一句“我没事”：
- 真没事：正常对视，说完继续原动作；
- 有事但不想说：回答偏快、视线短暂回避、手上动作继续；
- 强撑：可表现为唇压、声音力度变化、动作仍维持控制；只有确有压抑/生理需要时才把换气写成可见表演；
- 生气否认：下颌收紧，回答短硬，视线更直接。

禁止只写“平静地 / 关心地 / 紧张地说”。这些词可以解释心理方向，但必须配具体表演。

### Dialogue Reaction Threshold（对白反应阈值）
不是每句话都值得明显反应。Skill根据人物关系与信息重要度自动判断：
- 普通信息：维持Baseline与原有任务连续性；视线可自然调整，生理呼吸作为隐式底层状态持续；
- 轻微在意：一个主要载体变化；
- 触碰敏感点：动作速度、停顿、视线或语速发生可读变化；
- 重大冲击：Objective / Tactic / 注意力或声音/动作稳定发生明显改变；外显可以集中在少数高价值载体，不要求“脸部 + 身体”同时全开。

这样让真正重要的停顿/眼神变化有重量，避免“每句台词都皱眉眨眼”。


## F.2｜Natural Dialogue Performance Engine（自然对白表演引擎）

> **目标：** 把对白理解成一个人物持续思考、持续做事、持续观察他人的过程，而不是“台词句子 + 句尾停止 + 重启下一句”的离散动画。

自然对白按以下正向流程组织：

**Thought Intention → Speech Phrase → Body Continuity → Continuity Bridge → Breath Integration → Keyword Shift → Listener Flow → New Stable State**

### 1. Thought Intention｜整段思想意图
先判断这一小段话中，角色脑子里真正正在完成什么：解释、回忆、试探、隐瞒、劝说、敷衍、确认、转移话题、逐渐承认某件事等。

多句台词如果属于同一个思想，就按**一个连续心理过程**表演。句号只结束文字句子，不自动结束人物的注意力、表情、姿势或当前任务。

若多句仍服务同一个Objective / Tactic，则保持同一演员行动；只有Tactic、关系判断或场景事实真正变化时才形成新的Actor Beat。

### 2. Speech Phrase｜自然语流组
对白的换气与停顿按：

**语义完整度 + 当前语速 + 情绪状态 + 实际换气需要**

来组织，而不是按逗号/句号机械切分。

- 两三个短句可以属于同一个连续Speech Phrase；
- 角色真正犹豫、思考、被击中、需要回答对方、刚运动完或受伤时，Speech Phrase可以自然变短；
- 停顿位置服务思想和表演，不服务标点本身。

### 3. Body Continuity｜身体连续性
人物开始说话前正在做什么，尽量让这个Ongoing Task贯穿对白：整理纸张、擦工具、看窗外、走路、倒水、收拾衣服、观察道具、驾驶等。

对白过程中身体不因一句话结束而“归零”。嘴唇短暂闭合时，至少一个连续状态仍在：原任务、视线目标、姿态、手部动作、身体朝向、表情基线或对另一人的注意力。

### 4. Continuity Bridge｜句间连续表演桥
相邻Speech Phrase之间优先用一个自然桥接动作维持“思想还没断”：
- 手上原任务继续或略微减速；
- 视线保持、转移或重新落点；
- 头部/身体朝向延续；
- 表情状态不重置，只发生小幅推进；
- 说话者观察听者后继续下一句；
- 听者的反应反过来改变说话者后半句。

**停顿不是空白。** 有意义的停顿里仍应存在思想、观察或未完成的身体行为。

### 5. Breath Integration｜呼吸融入语流
正常呼吸首先被视为**隐式生理连续性**，自然嵌入说话与动作，而不是独立的“胸口呼吸动画”。

日常平静状态下：
- 肩线、锁骨与整个上半身总体稳定；
- 换气幅度很轻，分散在肋部/上腹与整体躯干的极小体积变化中；
- 衣领、围巾、吊坠等胸前参照物不应因为普通换气而出现明显周期性上下泵动；
- 一次Speech Phrase结束后，只在真实需要时发生轻微换气，并继续原有思想与身体状态。

当呼吸本身成为剧情/表演信息时，才升级为Visible Signal，例如：
- 刚跑完、体力下降；
- 疼痛、受击、强行恢复；
- 突然恐惧导致吸气被截断；
- 想哭但压住；
- 叹气、笑、哽咽；
- 明确的情绪平复过程。

此时必须写清：**Cause → Degree → Body Location / Visible Effect → Timing → Recovery**，而不是只写“呼吸明显”。

### 6. Keyword Shift｜关键词改变表演方向
一句话中真正改变角色判断或关系的词，才触发表演状态推进。例如：视线从道具转向对方、原动作减速、唇压改变、声音力度变化、短暂换气中断等。

前面的普通词不需要重复制造新反应；角色的状态可以跨越多个句子持续积累，直到关键词真正改变它。

### 7. Listener Flow｜听者连续流
听者不按每个句号逐句“打卡反应”。先保持Baseline / Ongoing Task；只有信息重要度越过Reaction Threshold时才改变状态，并让这个新状态持续一段时间。

例如：先在车窗倒影里观察 → 听到关键词后才真正看向说话者 → 后面两句话保持观察 → 再在新的信息点改变姿态。这样听者一直活着，但不会像NPC每句话点头/眨眼。

### 8. New Stable State｜对白后的新状态
一小段交流结束后，明确人物和开始时相比发生了什么：更警惕、更靠近、更回避、更相信、更怀疑、原任务停下、开始看着某人、关系略微变冷/变近等。

这让整段对白形成表演弧，而不是每一句都独立开始、独立结束。**若Objective / Tactic仍未完成，则不强行落到Recovery；当前状态直接连续进入下一Speech Phrase / Shot。**

### Dialogue Compilation Rule｜进入Stage 05时怎么写
不要把上述8步原样做成模型动作清单。Compiler应把它们压成**连续自然表演描述**：

**正在做什么 + 这段话的思想方向 + 语流如何连续 + 哪个关键词真正改变状态 + 句间由什么动作/视线桥接 + 需要时如何自然换气 + 听者何时改变状态 + 最终落点。**

模型最终看到的是“一个人在连续地想、说、做、听”，而不是八个独立任务。

## G｜Reaction Priority（反应优先级）

多人镜头中明确：
- Main Reactor：主反应者；
- Secondary Reactor：次反应者；
- Background Listener：背景听者。

防止所有人一起做同级反应。

## H｜No Premature Reaction（禁止提前反应）

- 未感知Trigger前不得提前做对应反应；
- 对白关键词未说出前，听者不得提前演到结论；
- 攻击未启动前，防守者不得提前躲避；
- 道具未碰撞前，人物不得提前因碰撞结果反应。

## I｜Combat-Performance Coupling（战斗—表演耦合）

战斗时Performance绝不暂停，并先继承Actor Engine中的当前Objective / Obstacle / Tactic。每个重要Combat Exchange同时存在两条链，并在时间上交织：

**Tactical Chain：Read → Decision → Commitment → Threat → Defense / Evade → Contact / Near Miss → Counter Window → Recovery → Initiative Shift**

**Performance Chain：Perception → Micro Reaction → Emotional Leak → Controlled Response → After-effect / New Focus**

具体原则：
- Read阶段可以通过视线锁定、头部微转、呼吸变化体现“真的看见了”；
- Decision阶段的眉眼/下颌/握持变化必须服务判断，不是装饰；
- Near Miss / Impact后允许短促吸气、眼神失稳、疼痛压制、惊险泄露等真实后果；
- Controlled Response体现人物性格：谨慎、暴躁、保护型、恐惧但强撑的人面对同一攻击不能演成同一张脸；
- 高速动作中仍可保留短而明确的表演信号，不得把角色做成扑克脸；
- 也不得为了“表情丰富”把与战斗无关的眨眼/皱眉清单塞进每一招。所有信号必须由当下Read / Threat / Contact / Relationship触发。

当Combat动作与重要表演信息都很多时：先合并因果、再分时、再按景别转译；仍不可读时拆Shot / Segment，**不通过删掉人物情绪来换稳定性**。

## Stage 04 / 05使用方式

### Stage 04 Storyboard
先读取`actor_performance_engine.md`确定Objective / Tactic / Listening / Beat Shift，再在关键画格中优先写：
- Baseline
- Trigger
- 主反应者的微表情 / 微动作
- 听者存在感
- 情绪落点

### Stage 05 Video
内部先运行`actor_performance_engine.md`，再在Performance部分写：
- 面部自然行为（眼神、眨眼、眉眼）+ 生理连续性（呼吸默认融入语流；有因时才成为可见信号）
- Micro Action Selection + Emotional Carrier
- Listener Presence + Natural Dialogue Performance Engine（有对白时）
- Emotional Arc + Intensity + Visible Signals
- Reaction Cascade
- Combat-Performance Coupling（战斗时）

## QC检查重点

失败征象：
- 眼睛死、长期不眨眼、眉头完全不参与；
- 非说话角色无因待机/冻结；或有因Triggered Stillness被错误加动作破坏；
- 所有人一起反应；
- 情绪直接顶格，没有过程；
- 表面与内里没有差别；
- 只写“害怕/震惊/关心”等抽象情绪，没有具体Visible Signals与程度；
- 为了模型稳定把有心理意义的微动作直接删掉，而不是合并/排序/分时/转译；
- 有意义的“真实情绪泄露 + 主动压制”被误判为矛盾而删掉；
- 日常对白只有嘴动，没有潜台词、Speech-Body Coupling或Listener Reaction；
- 多句对白被切成“说一句→身体/表情归零→明显换气→再说一句”的重复循环；
- 普通呼吸被做成周期性胸口/肩线泵动，尤其胸前围巾、吊坠、衣领跟着明显上下移动；
- 句间停顿没有Objective / Thought / Ongoing Task / Gaze / Listener等Continuity Bridge，像模型在等待下一条命令；
- 同一Objective / Tactic内每个句号都执行Recovery / New State；
- 微动作很多，但无法追溯到Objective / Tactic / Stimulus；
- 战斗动作正确但主要角色长期扑克脸，Performance没有与Read/Threat/Impact耦合；
- 在Trigger发生前就先反应；
- 单个背景角色像站岗或抢戏；若是多人Crowd则另检查`CROWD_FREEZE / CROWD_SYNC / CROWD_ATTENTION_HIJACK`。


## Current｜Visible Acting / Vocal Acting Coupling

对白的声音变化与可见表演必须来自同一个Trigger / Meaning Appraisal。若一句话因被击中而出现Processing Pause、语速下降或句尾失去力度，可见的视线/原任务/下颌/姿态也要与同一Cause一致；不能声音像崩溃而身体完全无因保持另一种状态。具体Prosody交给`voice_direction_prosody_engine.md`。
