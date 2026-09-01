# Combat Choreography Engine（《断弦之歌》战斗编排引擎）

> **定位：** 这是《断弦之歌》的项目级 Combat Engine。它不是当前小说的“战斗事件数据库”，也不把某一集、某一名角色、某一套技能写死为永久打法。它从项目长期设定与当前Scene输入中，**运行时推导**本场战斗的目的、距离、攻防、打击感、紧张感、技能互动和多人协同。
>
> **长期原则：Episode Change ≠ Skill Rewrite。** 小说后续新增人物、调整集数、改换对手或新增战斗，正常情况下只更新当前Story / Character / Asset输入，不重写Combat Engine。
>
> **电影打击/VFX执行：** 有Music Identity、共鸣技能、重要接触或超自然VFX时，同时读取 `cinematic_combat_vfx_engine.md`。

## 1｜Project Combat DNA（项目战斗DNA）

《断弦之歌》的战斗优先建立在六件事上：

1. **Narrative Goal（剧情目的）**：为什么现在必须发生冲突；
2. **Victory Condition（胜利条件）**：击败、阻止、救援、拖延、撤离、夺取、破核心、守住区域、恢复选择权等；
3. **Tempo / Initiative（节奏权 / 主动权）**：谁正在逼迫谁回应，主动权何时交换；
4. **Measure / Space（距离 / 空间）**：攻击是否真的够得到，退路、掩体、狭窄区、危险区是否影响选择；
5. **Cost / Consequence（代价 / 后果）**：强动作与强技能必须有可感知的承诺度、恢复窗口或剧情已确认的代价；其中`Execution Consequence`可从动作物理推导，`Lore Cost`必须有Story / Canon依据；
6. **Character Choice（人物选择）**：关键时刻“是否出手、如何出手、愿意承担什么”可以比单纯命中更重要。

**禁止默认：** 检测到“战斗”就自动生成“冲刺→格挡→技能→爆炸→终结技”。

## 2｜Combat Canon（长期战斗Canon）

### 2.1 Synchronized Dissolution（同步消散）｜P0

战斗结束、变身解除时：

**Virtuoso Weapon（圣谱者武器） + Transformation Costume（变身礼服） + Accord Baton（圣约指挥棒）在同一解除阶段同步消散。**

- 不允许礼服已经完全解除后，战斗武器作为实体继续残留；
- 不允许战后把圣约指挥棒作为日常实体继续携带；
- 若小说草稿出现与此冲突的临时描写，Stage 02–05转译时按当前Combat Canon修正，不把草稿残留升级成新规则；
- 永久性日常道具是否存在，由其正式Prop / Character Canon另行决定，不得因为外形像战斗武器就自动等同。

### 2.2 Story Input ≠ Combat Canon

小说 / 大纲主要提供：
- 当前剧情事实；
- 参与人物；
- 情绪与人物关系；
- 当前伤势 / 状态；
- 战斗的起因、结果与不可改的剧情节点；
- 已经明确存在的能力、武器或限制。

Combat Engine负责把这些内容转译成**可执行动画战斗语言**。

不得把单一草稿中的一次动作、一次武器状态、一次技能写法，自动提升为长期项目规则。

## 3｜Combat Conflict Audit（战斗冲突审查）

当Story / World / Character / Asset / Current Skill之间出现不一致时，先分类，不静默拼接：

- `HARD_CONFLICT`：两条规则无法同时成立；必须裁决后才能进入正式Storyboard / Video；
- `COMPATIBLE_VARIATION`：只是不同场次的合法变化，可共存；
- `UPGRADE_CANDIDATE`：新写法可能更适合项目，但尚未成为Canon；标记建议，不自动改世界规则；
- `OPEN_NONBLOCKING`：信息不足，但当前Scene可用不定死Canon的保守临时方案继续；不得因此阻塞或询问用户。

**P0规则：** 未解决的HARD_CONFLICT不得带入FINAL VIDEO PROMPT。

## 4｜Runtime Combat Inference（运行时战斗推导）

每场战斗先建立一次临时 `Combat Design Brief`，至少读取：

- Narrative Goal；
- Victory Condition；
- Participants / Alliances；
- Current Emotional State；
- Current Injury / Fatigue；若刚完成完整Transformation，Current Injury必须取Post-Recovery Injury State，Fatigue仍独立判断；
- Weapon Geometry；
- Mobility；
- Combat Temperament；
- Music Motion Grammar；
- Accord / Cost State（若适用）；
- Opponent Mechanics；
- Scene Geometry / Environmental Material；
- Collateral / Rescue Constraints；
- Must-Happen Story Beats。

然后推导本场 `Combat Grammar（战斗语法）`。新人物加入时建立临时Combat Profile即可，**不要求修改Skill本体**。

## 5｜Runtime Combat Profile（运行时战斗画像）

对本场真正参与战斗的角色，按需推导：

### Weapon Geometry（武器几何）
- 有效距离：贴身 / 近 / 中 / 远；
- 单手 / 双手；
- 刺 / 斩 / 架 / 压 / 缠 / 射 / 牵引 / 控制；
- 重量感与转向惯性；
- 是否可变长度 / 形态；
- 防御面与死角。

### Combat Temperament（战斗性格）
- aggressive / cautious / probing / protective / controlling / deceptive；
- 更愿意试探、换血、守线、反击、拖延还是压迫；
- 当前心理状态是否改变其正常习惯。

### Risk & Defense（风险与防御）
- `Commitment`｜出招承诺度：试探 / 半承诺 / 全承诺；
- `Defense Preference`｜闪避、拨挡、硬挡、截击、后撤、侧移、控制距离；
- `Recovery`｜动作完成后的回收与暴露窗口。

### Music Motion Grammar（音乐动作语法）
Music Identity先进入`Musical Combat Translation Layer`，转译为可被战斗执行的时间/运动语法，例如：
- Attack Cadence；
- Rest / Hold；
- Acceleration / Deceleration；
- Repetition / Variation；
- Sustain；
- Syncopation / Off-beat；
- Counterpoint / Initiative Handoff；
- Crescendo / Diminuendo；
- Recovery Weight / Closure。

再由这些字段改变Footwork、Commitment、Weapon Kinetics、Defense、Recovery与Tactical Timing。**不同角色不能只换VFX颜色而动作语法完全相同。**

具体转译与电影VFX见 `cinematic_combat_vfx_engine.md`。**Stage 05不因此自动生成BGM。**

## 6｜Combat Archetype Selector（战斗原型选择）

先选择最匹配的战斗目的，可组合但不要堆满：

- `DUEL`｜一对一决斗：距离、读取、骗招、反击窗口；
- `CONTROL_DUEL`｜控制战：争夺节奏 / 空间 / 行动权，不一定需要击倒；
- `PROTECTION`｜护卫战：保护目标、承压、换位、截击；
- `RESCUE_UNDER_PRESSURE`｜压力营救：救人是主目标，敌人只是阻力；
- `CORE_BREAK`｜破核心：观察机制→暴露核心→精确破坏；
- `PURSUIT_ESCAPE`｜追逐 / 撤离：路线、拦截、窗口、出口；
- `HOLD_THE_LINE`｜守线：在时间条件内守住区域；
- `MULTI_FRONT`｜多线协同：不同角色同时承担不同目标；
- `PSYCHOLOGICAL_COMBAT`｜心理战：感知、记忆、意志与动作互相影响；
- `CHOICE_CONFLICT`｜选择冲突战：关键胜点可能是收手、拒绝、让出决定权，而不是击倒。

胜利条件决定动作；动作不得反过来替剧情创造错误目标。

## 7｜Combat Exchange Grammar（攻防交换语法）

一个清晰的 `Combat Exchange（攻防交换）`优先按以下因果建立：

**State → Read → Intent → Setup / Footwork → Threat → Defense Choice → Contact / Evade → Impact / Deflection → Counter Window → Follow-through → Recovery → Initiative Shift / New State**

不是每次都机械填满所有节点，但必须回答：
- 为什么现在出手；
- 为什么对方能看见 / 来不及看见；
- 攻击距离是否成立；
- 防守方式为什么有效；
- 谁在接触后得到下一次行动权。

### No Turn-Based Loop
禁止长期形成：A打一招→B打一招→A打一招→B打一招。

允许：
- 连续压迫；
- 一方夺回主动；
- 假动作诱导；
- 连续防守直到出现窗口；
- 第三方截断；
- 环境迫使双方改变距离。

## 8｜Duel Grammar（决斗语法）

决斗优先管理：
- `Measure`｜有效距离；
- `Line`｜攻击线；
- `Angle`｜进攻 / 防守角度；
- `Feint`｜假动作；
- `Parry / Deflect`｜拨挡 / 偏转；
- `Bind / Pressure`｜兵器接触后的压制；
- `Counter Window`｜反击窗口；
- `Recovery`｜收招；
- `Near Miss`｜险些命中。

**险些命中可以比连续真命中更紧张。**

不同武器必须打出不同距离和动作逻辑；禁止把长枪、短刃、弦线、盾、刺剑全部编成同一种“挥砍”。

## 9｜Impact Logic（打击感逻辑）

打击感不是“镜头抖一下”。重接触优先遵循：

**Intent → Setup → Acceleration → Contact Point Lock → Compression → Micro Hit Hold → Force Propagation → Recoil → Secondary Motion → Environment Proof → Aftermath → New Combat State**

`Contact Point Lock`至少明确武器/身体哪一部分接触目标哪个位置，以及Force Direction；目标反应应从接触点沿结构/关节→主体质量→重心→支撑点传播。

可见反馈按需包括：
- 身体重心；
- 前后脚承重；
- 腕 / 肘 / 肩的力传导；
- 武器回弹或滑开；
- 衣摆 / 头发 / 碎屑比主接触稍后跟进；
- 环境表面震动 / 尘屑 / 雨水反馈。

`Micro Hit Hold`是极短的视觉停顿感，不要求模型执行精确毫秒，也不能把动作冻成明显卡顿。Light / Medium / Heavy / Massive Impact使用不同程度的速度压缩，不靠“震屏大小”分级。具体见 `cinematic_combat_vfx_engine.md`。

## 10｜Tension Curve（紧张感曲线）

紧张感优先来自：
- Threat Knowledge：观众知道危险在哪里；
- Uncertainty：不知道谁会先失误；
- Proximity：危险逐步进入有效距离；
- Delay / Hold：启动前的短暂停顿；
- Commitment：一旦出招就暴露后果；
- Consequence：失误会改变场面或人物状态。

禁止把“全程高速 + 全程Camera Shake + 全程大特效”当成紧张感。

推荐结构：
**Approach → Probe → First Real Contact → Separation / Reassessment → Escalation → Mistake / Break → Payoff**。

## 11｜Skill Interaction Grammar（技能互动语法）

每个剧情已确认的技能，在战斗编排中转译为：

**Setup → Tell → Startup → Effect → Counterplay → Cost → Recovery**

先判断技能主要改变什么：
- Tempo / Time；
- Distance；
- Space / Area；
- Mobility；
- Defense；
- Perception / Information；
- Control；
- Damage / Core Break。

### Skill vs Skill
技能对抗不能默认变成两束能量正面对撞。

优先判断：
- 是否能偏转；
- 是否能穿透；
- 是否能打断Startup；
- 是否能绕开作用区域；
- 是否能用距离 / 环境破解；
- 是否能诱骗对方提前释放；
- 是否需要先破坏支撑机制。

## 11.1｜Execution Consequence ≠ Lore Cost

Combat Engine必须区分：

### Execution Consequence｜执行后果｜可自动推导
- Recovery变长；
- 重攻击后武器需要回收；
- 惯性导致短暂站位暴露；
- Guard暂时打开；
- Initiative因Commitment转移；
- 脚步/重心需要重新稳定。

这些属于动作物理和战术承诺，不是在创造新世界观。

### Lore Cost｜设定代价｜不可擅自创造
- 圣约反噬；
- 寿命消耗；
- 固定能量百分比；
- 未设定的吐血/内伤；
- 精神损耗；
- 新的技能冷却机制；
- 其他会成为长期Canon的副作用。

只有Story / World Canon / Current State明确存在时才能使用。为了“战斗有代价”不得临时编一个Lore Cost。

## 12｜Visible Cost Degradation（可见式战斗衰减）

若Story / World / Current State已经确认存在消耗、伤势或过载，则尽量把“快撑不住了”转译为可见性能变化，而不是只写一句疲惫：

- Effective Range ↓；
- Precision ↓；
- Recovery ↑；
- Grip Strength ↓；
- Stability ↓；
- Step Length / Mobility ↓；
- Reaction Delay ↑；
- Breath Control ↓；
- Defensive Coverage ↓；
- Skill Area / Duration ↓。

**不得凭空发明未被当前项目确认的伤势或代价。**

## 13｜Dissonant Combat Generator（噪骸战斗生成逻辑）

当当前世界资料确认敌人为噪骸时，使用其项目既有构成输入进行推导，而不是套固定怪物动作：

**Environment Material + Local Obsession + Anti-Music Element + Music Residue + Body Structure + Scene Geometry**

推导：
- Movement Logic；
- Attack Logic；
- Defense / Regeneration Logic；
- Environmental Interaction；
- Vulnerability Reveal；
- Core / Break Condition；
- Defeat Aftermath。

噪骸战斗优先形成“观察→生存→读机制→改变位置→暴露弱点→完成目标”的过程，而不是默认HP磨血。

## 14｜Multi-character Combat（多人战）

多人战必须明确：
- `Focus Owner`｜当前镜头主要动作承担者；
- `Threat Priority`｜谁正受最大威胁；
- `Combat Role`｜压制 / 保护 / 控制 / 破核心 / 救援 / 撤离；
- `Spatial Lane`｜每个人当前活动区域；
- `Cross-support`｜谁帮助谁获得窗口；
- `Initiative Handoff`｜主动权如何在角色间传递。

禁止：
- 所有人围着一个目标排队出招；
- 所有人同一时刻做同级大动作；
- 背景角色冻结等下一回合；
- 为展示技能而破坏救援 / 护卫 / 撤离等主目标。

## 14.1｜Combat-Performance Coupling（战斗—表演耦合）

Combat Choreography只负责“怎么打”是不完整的。主要人物在战斗中必须同时遵守 `actor_performance_engine.md` + `performance_causality_emotional_acting.md`。先明确战斗中的Objective / Obstacle / Tactic（例如保护、拖延、逼弱点、撤离），再把它与攻防交换绑定。

每个重要Exchange并行推导：
- **Tactical Chain**：Read → Decision → Commitment → Threat → Defense / Evade → Contact / Near Miss → Counter → Recovery → Initiative Shift；
- **Actor / Performance Chain**：Objective / Tactic → Perception → Meaning → Micro Reaction → Emotional Leak → Adjustment / Controlled Response → After-effect / New Focus。

两条链必须交织：
- 先看见攻击线并判断它对当前Objective意味着什么，才有对应视线 / 眉眼 / 握持 / 必要时的换气变化；
- 险避与受击后应有符合程度的短促反应；
- 保护型、暴躁型、谨慎型、恐惧但强撑的人面对同一攻击不应演成同一张脸；
- 表演不得独立于Read / Threat / Contact / Relationship随机发生。

**禁止用“模型执行困难”为理由删除有心理意义的战斗微动作。** 信息过密时先合并、排序、分时、景别转译；必要时拆分Exchange / Shot / Segment，而不是把角色做成扑克脸。

## 15｜Stage 02 Integration（导演拆解）

遇到真实战斗 / 追逐 / 高强度行动Scene时，Stage 02先完成 `Combat Design Brief`，再把战术因果转译成**空间导演**。读取`director_architecture_engine.md` + `cinematic_spatial_staging_engine.md`。

基础Brief：
- Narrative Goal；
- Victory Condition；
- Combat Archetype；
- Must-Happen Story Beats；
- Participants / Roles；
- Scene Geometry / Hazard Zones；
- Primary Tactical Problem；
- Cost / Injury State；Transformation Recovery只修复其授权范围内的伤口，不自动清空独立Lore Cost / Fatigue；
- Combat Conflict Audit；
- Asset Needs。

随后必须锁：
- `Engagement Distance Ladder`：Entry → Threat → Weapon Reach → Contact/Near Miss → Exit；
- `Spatial Dominance`：谁占中心/出口/高位/障碍区；
- `Attack Lane / Escape Lane`；
- `Depth Strategy`：谁在FG/MG/BG，何时换层；
- `Contact Read Shot`：哪一个Shot必须清楚看见接触点/险些命中；
- `Initiative Shift Visual`：主动权变化时距离、构图或人物占比怎样改变；
- `Combat Coverage Rhythm`：Spatial Read / Compression / Commitment / Contact / Consequence中本场真正需要哪些，不机械五镜。

**不在Stage 02写满每一次挥剑，但也不能把距离、空间和Camera全部推迟到Stage 04。**

## 16｜Stage 04 Integration（战斗Storyboard）

Stage 04先继承Stage 02的Engagement Distance Ladder / Depth Strategy / Contact Read / Axis / Camera Intent，不得把战斗重新排成阵容展示。若真实Environment证明某条Attack Lane不成立，回`director_spatial_reconciliation_gate.md`做最小Director Patch。

关键战斗Panel应能读出：
- 距离变化；
- Music Identity适用时的Hold / Acceleration / Sustain / Off-beat / Counterpoint等可见时间结构；
- 主动权；
- 攻击起点 / 防守响应；
- 接触 / 险些命中；
- 重心与方向；
- Counter Window；
- 环境与队友作用；
- 当前Combat State发生了什么变化；
- 重要打击的Contact Point / Force Direction / Impact前后构图变化；
- VFX来源、空间几何和环境介质响应（适用时）。

复杂战斗优先以 `Combat Exchange` 为单位拆Panel / Segment，不用一张Storyboard把所有技能塞完。

## 17｜Stage 05 Integration（视频Prompt）

模型Prompt只编译**当前Segment看得见、必须执行的战斗因果**，不要把内部Combat Profile表格全部塞给视频模型。

推荐顺序：
1. Entry / Spatial State；
2. Current Initiative / Micro-objective；
3. Music-derived Timing（适用时）；
4. Body / Weapon Setup & Footwork；
5. Attack / Defense sequence；
6. Contact Point / Near Miss；
7. Impact Physics + VFX Cause / Spatial / Environment Response；
8. Counter / Recoil / Initiative Shift；
9. Cost / Aftermath（适用时）；
10. New Combat / Exit Stable State。

### Segment Complexity
为单次生成稳定性，复杂战斗通常让一个Segment承担：
- 1个清晰Micro-objective；或
- 1–2个完整Combat Exchange；或
- 1次复杂技能互动。

不要让单个Segment同时塞入七八次独立攻防、多人技能、复杂运镜和剧情反转；复杂度由可读性与Micro-objective决定，不按固定秒数判断。

## 18｜Combat QC（战斗QC）

必须检查：
- Victory Condition是否被动作贯彻；
- 有效距离是否成立；
- 人物是否瞬移进入攻击范围；
- 攻防先后是否有因果；
- Initiative是否可读；
- 武器接触点 / 方向 / 反作用是否可信；
- Impact是否有明确Contact Point / Force Direction、Compression、Force Propagation、Recoil与Aftermath；
- Music Identity是否真正改变Timing / Footwork / Weapon Kinetics / Recovery，而不是只换颜色/音符；
- VFX是否有Cause / Source / Spatial Geometry / Environment Interaction / Decay，而不是贴图Glow；
- 是否陷入轮流出招；
- Tension是否只有速度与抖镜；
- Skill Interaction是否有Counterplay；
- 已确认Cost是否可见；
- 多人战是否排队出招或背景冻结；
- Camera是否遮住关键接触和动作方向；
- 是否出现所有参战者同深度、同尺寸、均匀间距、完整全身的`COMBAT_LINEUP_FAIL`；
- Engagement Distance Ladder是否真实推进，还是一直停在安全中远距离；
- 主动权改变后构图/距离是否仍完全不变，导致战术关系不可读；
- Exit是否形成下一段可承接稳定状态；
- 战斗结束时Weapon + Costume + Accord Baton同步消散（若本Segment覆盖解除）。

## 19｜Failure Subtypes（战斗失败子类）

仍归入现有 `ACTION / PHYSICS` 主失败类型，使用子类定位：

- `RANGE_JUMP`｜距离跳跃 / 瞬移；
- `INITIATIVE_BREAK`｜主动权无因果乱跳；
- `TURN_BASED_LOOP`｜轮流出招；
- `CONTACT_FLOAT`｜武器接触漂浮 / 吸附；
- `IMPACT_WEAK`｜缺准备 / 传力 / 回弹；
- `TENSION_FLAT`｜全程同速无紧张曲线；
- `SKILL_CLASH_GENERIC`｜技能只会对波 / 爆炸；
- `COST_INVISIBLE`｜已确认代价没有反映到动作性能；
- `MULTI_FIGHT_QUEUE`｜多人排队攻击；
- `CAMERA_OBSCURES_ACTION`｜机位遮挡关键动作因果；
- `COMBAT_LINEUP_FAIL`｜战斗像人物阵容展示；
- `COMBAT_DISTANCE_FLAT`｜战斗距离没有压缩/释放关系；
- `INITIATIVE_VISUAL_FLAT`｜主动权变化但构图/距离无任何视觉反馈；
- `DISSOLUTION_MISMATCH`｜战斗结束Weapon / Costume / Baton消散不同步。

优先Minimum Necessary Change，不因一个错误重写整场已正确的Combat Design。
