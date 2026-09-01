# Actor Performance Engine（演员表演引擎｜意图、倾听与现场反应）

> **用途：** 作为Stage 02 / 04 / 05人物表演的上游导演引擎。它不直接规定“眉毛动几次、呼吸几次”，而是先回答：角色此刻处在什么情境、想从对方/场景得到什么、遇到什么阻力、正在采取什么策略、刚刚真正听见/看见了什么、因此是否调整策略。`performance_causality_emotional_acting.md`负责把这些演员逻辑继续翻译成可见表演。

## 1｜核心原则：Action Before Expression（先行动意图，后表情结果）

角色不是在“展示情绪”，而是在当前规定情境中**做一件有目的的事**。

内部推导顺序：

**Actor Intention Layer → Live Response Layer → Visible Performance Layer**

### Layer A｜Actor Intention（演员意图层）
1. `Given Circumstances`｜当前已知事实、地点、时间、关系、刚刚发生的事；
2. `Objective`｜角色此刻真正想从对方/场景得到什么；
3. `Stakes`｜得不到会失去什么；
4. `Obstacle`｜什么阻止他达到目标；
5. `Relationship / Power`｜角色如何看待对方，当前权力/亲疏/信任关系如何；
6. `Action / Tactic`｜角色此刻采取什么可演的策略去影响对方；
7. `Subtext`｜字面台词与真实意图之间是否存在差异。

### Layer B｜Live Response（现场反应层）
1. `Attention`｜角色真正把注意力放在哪里；
2. `Stimulus`｜对方/环境刚刚给了什么新刺激；
3. `Meaning Appraisal`｜这个刺激对当前Objective意味着什么；
4. `Authentic Response`｜第一真实反应是什么；
5. `Adjustment`｜原策略还有效吗，是否需要换Tactic；
6. `Beat Shift`｜只有当Objective、Tactic、关系判断或场景事实发生有意义变化时才进入新Beat。

### Layer C｜Visible Performance（可见表演层）
由上述两层再推导：
- Gaze / Focus；
- Ongoing Physical Task；
- Voice / Speech Rhythm；
- Face / Eye / Jaw Leakage；
- Gesture / Posture；
- Spatial Relationship / Distance；
- Breath（仅在真正承载情绪或生理信息时显性）；
- Recovery / New Stable State（只在真实Beat或策略阶段结束时发生）。

**禁止倒过来：** 不得先决定“这里要皱眉+吸气+握拳”，再给这些动作硬找理由。

## 2｜Playable Objective（可表演目标）

Objective必须是角色在当前Scene/Beat中可以追求的东西，例如：
- 让对方相信我；
- 让对方留下；
- 让对方停止追问；
- 逼对方承认；
- 保护某人；
- 获得一个答案；
- 隐藏自己的异常；
- 争取时间；
- 让对方放松警惕；
- 让团队继续行动。

避免把纯情绪当Objective，例如：
- “我要悲伤”；
- “我要紧张”；
- “我要表现害怕”。

情绪是角色追求目标、遭遇阻力、接收刺激过程中产生的状态，不是演员的主要行动任务。

## 3｜Action / Tactic（行动策略）

Tactic应尽量使用可演、指向他人的行动动词。常见方向包括但不限于：
- 试探 / 探问；
- 安抚 / 稳住；
- 说服 / 拉拢；
- 逼迫 / 施压；
- 警告 / 威慑；
- 隐瞒 / 掩饰；
- 转移 / 回避；
- 挑衅 / 激怒；
- 软化 / 缓和；
- 保护 / 挡住；
- 引导 / 诱使；
- 拒绝 / 推开；
- 承认 / 坦白；
- 观察 / 验证；
- 拖延 / 争取时间。

同一句台词，因为Tactic不同，表演应该不同。

例如“我没事”：
- Tactic=安抚：对视更稳定，语句完整，动作继续；
- Tactic=隐瞒：回答偏快，注意力回到原任务，不主动展开；
- Tactic=拒绝追问：句尾更硬，距离/视线可能关闭交流；
- Tactic=说服自己：声音与身体可能出现细小不一致。

## 4｜Active Listening（主动倾听）

Listener不是“没台词也得动一下”，而是**持续接收对方，并判断新信息是否改变自己的Objective / Tactic / Relationship判断**。

**Scope：** 本节针对可识别的单个Speaker/Listener/第三人。若背景是多人Crowd，不逐人套Active Listening；改由`crowd_presence_ambient_life_engine.md`控制Cluster活动、注意力和Reaction Propagation。

固定流程：

**Receive → Understand → Assign Meaning → Keep / Adjust Tactic → Visible Response if Needed**

规则：
- 已知、无新增意义的信息可以几乎没有外显变化；
- 真正改变判断的关键词/动作才需要推进外部状态；
- Listener可以保持原任务、姿态或视线很久，只要注意力逻辑连续；
- 不按每一句台词机械点头、眨眼、皱眉；
- 说话者也必须Listening：如果看到对方反应变化，后半句的语速、力度、措辞或Tactic可以调整。

## 5｜Beat Boundary（Beat边界由策略变化决定）

**Punctuation ≠ Beat。Sentence End ≠ Recovery。**

只有以下情况之一真正发生时，才优先考虑进入新Beat：
- Objective改变；
- 原Tactic失败，角色换了一种办法；
- 新事实改变了角色理解；
- 关系/权力状态发生可读变化；
- 对方的回应迫使角色重新选择行动；
- 一个明确行动阶段完成并进入新的追求。

同一Thought Intention / Tactic内的多句对白保持连续心理流，不在每个句号执行`Recovery / New Stable State`。

## 6｜Triggered Stillness（有因静止）

“静止”本身可以是强表演。

当明确刺激让人物的原任务、步伐、语言或视线突然停住时，可以使用：

**Stimulus → Task/Movement Interrupted → Brief Stillness → Meaning Processed → Next Action**

这属于`Triggered Stillness`，不是NPC冻结。

QC只否定：
- 无原因长期待机；
- 没有注意力/心理连续性的僵住；
- 背景角色像等待下一条模型命令。

有明确Trigger、持续时间、注意力落点和后续行动的短暂静止应保留。

## 7｜Ongoing Physical Task（持续现实任务）

日常表演优先让角色处在具体、自然、与场景有关的现实行为里，例如：
- 整理节目单/文件；
- 修理/收拾工具；
- 倒水、穿衣、收伞；
- 看窗外、驾驶、走路；
- 检查道具、关门、整理桌面。

任务的意义不是“让手一直动”，而是给心理变化一个真实载体：
- 动作继续；
- 变慢；
- 停住；
- 变得更用力/更精确；
- 做错一步；
- 放弃原任务；
- 转向另一个人。

Ongoing Task必须服务场景，不得为了“自然”无意义忙活。**当新的表演动作需要占用正在维持Ongoing Task的手/脚/支撑资源时，不得默认为旧任务自动消失；交给`action_feasibility_prop_limb_continuity_engine.md`决定继续、减速、中断、转交、放下或使用空闲肢体。**

## 8｜Emotion Is a Result（情绪是结果，不是动作清单）

内部仍可记录`Surface Emotion / Inner Emotion / Suppression / Intensity`，但它们必须由：

**Objective + Obstacle + Stimulus + Relationship + Tactic Outcome**

解释。

情绪强度不按“动了几个身体部位”计算。强烈情绪可以只通过一个高度准确的载体泄露；克制人物即使Intensity很高，也可能只出现：
- 视线停住；
- 手部张力变化；
- 语速/声音力度变化；
- 原任务中断。

判断Intensity优先看：
- 对Objective/判断影响多大；
- 控制情绪需要多大努力；
- 是否改变Tactic；
- 是否影响动作/声音稳定；
- 泄露持续多久。

## 9｜Camera Acting（镜头表演尺度）

镜头越近，不代表需要更多动作，而是更小的变化就有重量。

- ECU / CU：更少、更精确；焦点、眼睑、唇压、下颌、极小的任务中断就足够；
- MCU / MS：视线、手部任务、身体朝向、距离、声音节奏共同工作；
- WS / EWS：主要通过步伐、停顿、距离、方向、是否靠近/远离和任务中断表达心理。

禁止因为近景就机械增加眨眼、眉毛、吞咽、呼吸等数量。

## 10｜Voice / Speech Action（声音与台词行动）

声音不是独立“情绪滤镜”，而是Tactic的一部分。Stage 02/04/05可根据当前策略推导：
- 回答是立即还是延迟；
- 语速是保持、变快、变慢；
- 句子是否完整；
- 关键词是否加重/减轻；
- 句尾是开放、收紧、截断还是主动留给对方；
- 音量/力度是否因策略调整而变化。

停顿必须有用途：理解、选择、隐瞒、等待回应、被击中、真实换气或策略改变。不要把停顿当“高级表演”的默认装饰。

## 11｜Breath Placement（呼吸在演员系统中的位置）

普通呼吸属于底层生理连续性，不是默认动作任务。只有当呼吸本身成为：
- 生理负担；
- 情绪控制；
- 惊吓/疼痛/受击反应；
- 叹气/哽咽/笑；
- 语音组织的重要变化；

才升级成Visible Performance。

`Music Identity`中的`Breath Pattern`默认表示**乐句感、蓄放、发力组织与动作节奏**，不自动等于可见胸腔呼吸。只有本Actor/Performance系统已经判定`VISIBLE_WITH_CAUSE`时，才允许把它落实为真实可见换气。

## 12｜Combat Acting（战斗中的演员逻辑）

战斗不是退出演员状态。

在Combat Engine之前/同时先明确：
- 当前Objective：击败、拖延、保护、夺取、逃离、逼对方暴露等；
- 当前Obstacle：距离、对手读取、伤势、第三者、环境、心理顾虑；
- 当前Tactic：试探、压迫、诱骗、守线、拖延、牺牲距离换窗口等；
- Stimulus：对手线路变化、保护对象受威胁、技能Tell、Near Miss、受击；
- Adjustment：Tactic是否改变。

Combat Exchange里的视线、下颌、握持、惊险反应、受击后控制等，必须由这些演员逻辑与战术事件共同触发。

## 13｜Stage 02 / 04 / 05 Integration

### Stage 02｜Actor Performance Brief
重要人物交流/表演Scene至少内部锁定：
- Given Circumstances；
- Objective；
- Stakes；
- Obstacle；
- Relationship / Power；
- Tactic；
- Subtext；
- Ongoing Physical Task；
- 可能造成Tactic变化的Stimulus / Beat Shift。

不需要在Stage 02写满微表情。

### Stage 04｜Storyboard
先让每个关键Panel/Shot看得出：
- 人物正在追求什么；
- 当前Tactic有没有变化；
- 刺激从哪里来；
- Ongoing Task / Spatial Relationship如何承载变化；
再调用Performance Causality设计可见信号。

### Stage 05｜Video Prompt
内部先完成Actor Engine推导，再把心理/表演信号交给Action Feasibility与Natural Motion共同求解身体执行；最后由Semantic Dedup编进`Integrated Shot Timeline`，不再单独输出一段重复的Performance摘要。

最终模型Prompt优先写：
- 人物正在做的现实任务；
- 若动作涉及持物/支撑/接触，先由Action Feasibility Engine锁定实际执行肢体与必要Bridge，再由Natural Motion Engine决定Preparation / Kinetic Chain / Overlap / Settle；
- 当前交流/行动意图；
- 对方哪一个刺激真正改变了行为；
- 具体的视线/任务/声音/身体变化；
- 变化如何延续到下一句/下一动作。

不要把`Objective / Obstacle / Tactic`整张分析表原样塞给模型。

## 14｜Decision Authority

Objective、Tactic、Listening Response、Beat Boundary、Ongoing Task、Visible Carrier通常属于当前Scene导演执行层，默认由Skill根据Story / Character / Relationship自动推导并标`DERIVED PERFORMANCE`，不询问用户。

只有当两种选择会改变长期Canon、人物核心关系事实或剧情结果，且Authority无法裁决时，才允许`ASK_REQUIRED`。

## 15｜Actor Performance QC

每个重要可见表演都应该能回答：
1. 角色此刻想得到什么？
2. 什么阻止他？
3. 他现在采取什么办法？
4. 刚刚哪个刺激真正改变了他？
5. 外部变化是Tactic/Listening的结果，还是随机“加戏”？

失败征象：
- 只有情绪标签，没有Objective / Action；
- 每句台词都重新开始一套表情；
- Listener为了“不能冻结”而不断做无意义动作；
- 角色收到新信息却没有任何理解/策略变化，或在信息发生前提前反应；
- 微动作很多，但无法解释它们为什么发生；
- 角色的手部/身体一直忙，但与场景任务无关；
- 每个句号都Recovery；
- 有因静止被误判成冻结并强行加动作；
- 镜头越近动作越多，导致表演过满；
- 战斗动作正确，但角色当前Objective/Tactic完全不可读。


## Current｜Voice Direction Handoff

本Engine的`Voice / Speech Action`只负责从Objective / Tactic / Subtext决定“回答快慢、开放/关闭交流、是否留白、声音力度策略”。重要Dialogue/VO之后必须交给`voice_direction_prosody_engine.md`继续求解Speech Phrase、Pace Curve、Pause Map、Stress / De-emphasis、Pitch/Energy与Sentence-final Intonation。Actor Intent是原因，Prosody是声音执行结果。
