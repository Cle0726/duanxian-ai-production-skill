# Natural Motion & Kinematic Performance Engine（自然动作与身体运动表演引擎）

> **用途：** 把已经通过Action Feasibility的“物理可行动作”进一步求解成真人更自然的运动过程。它不负责决定角色为什么动，也不负责证明道具/肢体是否合法；它负责回答：**这个合法动作由整个人体怎样准备、启动、叠接、传递、减速与落位，才不像Pose A到Pose B的机械插值。**
>
> **定位：** 六阶段外侧的内部动作表演层，不是Stage 07。固定职责链：
> `Performance Intent → Action Feasibility → Natural Motion / Kinematic Performance → Action Physics → Prompt Compiler`。

## 1｜核心原则：Valid Motion ≠ Natural Motion

Action Feasibility证明“能这样做”；Natural Motion证明“真人通常会怎样完成”。

禁止把：
- `站着 → 手到喉咙`
- `坐着 → 站着`
- `朝前 → 转身180°`
- `手在身侧 → 抓住杯子`

直接当作两张Pose之间的最短插值。

每个重要动作按：

**Intent / Trigger → Functional Preparation → Kinetic Chain → Motion Corridor → Contact / Commitment → Deceleration / Settle → Residual Motion → Exit**

求解。

## 2｜与相邻引擎的职责边界

### Actor Performance负责
- 为什么现在动；
- Objective / Tactic / Stimulus / Subtext；
- 哪个微表情或身体变化具有心理意义。

### Action Feasibility负责
- 哪只手/脚可用；
- Held Prop / Support / Contact是否合法；
- 换手、放下、重心转移等必要前置Bridge。

### Natural Motion负责
- 动作从身体哪个部位开始；
- 哪些部位先后跟随；
- 哪些动作可以重叠而不是排队执行；
- 肢体走什么自然弧线；
- 动作速度、幅度、减速和余韵；
- Storyboard两个静态锚点之间的Motion Corridor。

### Action Physics负责
- 重力、接触、受力、碰撞、惯性、反作用、材质与环境反馈。

**不得互相重复职责。** 最终模型Prompt只保留合并后的可见执行链，不输出四套分析说明。

## 3｜Whole-Body Kinetic Chain（整个人体动力链）

动作不是孤立肢体移动。根据目标角度、速度、负载与人物状态，选择最小必要链条。

### 常见转向链
- 小角度注意变化：`Eyes → Head`
- 中等转向：`Eyes → Head → Shoulder / Upper Torso`
- 大幅转身：`Eyes → Head → Torso → Pelvis → Foot Replant / Pivot`

### 上肢动作链
- Reach：`Attention / Gaze（适用时） → Shoulder Release → Elbow Path → Forearm → Wrist / Fingers → Contact`
- Lift / Carry：`Grip Established → Elbow / Shoulder Load → Torso Counterbalance → Object Leaves Support`
- Put Down：`Torso / Arm guides → Object contacts support → Weight transfers → Fingers release`

### 起坐链
- Stand：`Feet establish support → Torso inclines / COM moves forward → Pelvis leaves seat → Knee/Hip extension → Balance settle`
- Sit：`Position chair → Weight shifts back/down → Pelvis contacts seat → Load transfers → Torso settles`

禁止所有身体部位同帧启动、同帧停止，除非动作本身是突然受击/强制僵直且剧情支持。

## 4｜Functional Preparation（功能性准备）

不是每个动作都加夸张“预备动作”，只补完成目标真正需要的准备。

示例：
- 拿杯子：视觉确认（若需要）→手臂接近→手指按杯体预张开→Contact→Grip→Lift；
- 开门：靠近把手→手掌/手指到位→Grip/Press/Turn→门体开始运动；
- 站起：脚先成为有效支撑→重心前移→再离座；
- 突然停步：步幅先缩短/制动→重心回收→最后一步落稳，而不是身体瞬间冻结。

若准备动作没有功能、心理或物理价值，删除。

## 5｜Action Overlap / Coarticulation（动作叠接）

真人动作默认允许安全重叠，不把每个动作排成“完成A→停→开始B”。

内部对相邻动作标：
- `SEQUENTIAL_REQUIRED`：必须先后（如Grip建立后才能Lift）；
- `OVERLAP_ALLOWED`：可以自然叠接（如步幅变短时手已经开始抬）；
- `OVERLAP_PREFERRED`：若完全串行会显得机器人（如转头与上半身跟随、说话与持续手上任务）；
- `SIMULTANEOUS_FORBIDDEN`：资源/物理冲突。

### 典型自然叠接
```text
Walking amplitude ↓
    Left arm begins rising ↗
        Body forward inertia ↓
            Hand reaches throat
                Final step settles
```

而不是：
```text
Walk STOP → Hand START → Hand STOP → Touch START
```

## 6｜Motion Corridor Between Storyboard Anchors（分镜锚点之间的运动走廊）

Storyboard Panel只定义关键姿态/构图锚点，不定义两锚点间“最短插值”。

Stage 04/05对任何存在明显姿态差异的相邻Anchor建立最小Motion Corridor：

```text
Anchor A：当前姿态 / 支撑 / 任务
→ Preparation：必要准备
→ Transition Path：身体链、步伐、肢体弧线、动作叠接
→ Commitment / Contact：动作真正成立的点
→ Settle / Residual：减速与余韵
→ Anchor B / Exit
```

只有以下情况必须显式记录Motion Corridor：
- 大幅转身/坐站/起停/上下楼/弯腰/跪起；
- 手从一个明显位置移动到另一位置；
- 持物/交互/多人接触；
- Storyboard两Panel姿态差异大；
- 上次生成出现滑步、机械插值、肢体直线漂移、突然定格。

普通微小姿态变化可快速求解，不机械建表。

## 7｜Motion Arc / Joint Path（运动弧线与关节路径）

默认遵循人体关节自然路径，不让四肢沿不合理直线“滑动”。

可选Path Class：
- `NATURAL_ARC`：肩/肘/腕共同形成弧线；
- `SURFACE_FOLLOW`：沿桌面/墙/衣物表面移动；
- `BODY_AVOIDANCE_ARC`：绕开躯干/衣物/道具；
- `DIRECT_REACH`：短距离且结构允许的直接Reach；
- `PIVOT_PATH`：围绕足部/骨盆支点转向；
- `STEP_AROUND`：大角度转身用步伐重新种脚，而不是脚底旋滑。

复杂动作只需选最相关路径，不在Prompt里堆人体解剖术语。

## 8｜Velocity Profile（速度曲线）

动作速度必须与意图、重量、危险度、精细度匹配。

内部可选：
- `CAUTIOUS_CONTACT`：慢启动→接近目标继续减速→轻Contact；
- `NORMAL_REACH`：平滑启动→中段稳定→接近目标减速；
- `URGENT_CATCH`：快速启动/加速→接触后由手臂吸收剩余动量；
- `HEAVY_LIFT`：准备明显→缓慢建立负载→稳定抬起→受重量限制；
- `SUDDEN_REACTION`：短延迟→快速启动→随后出现Recovery，而不是瞬时Teleport；
- `CONTROLLED_STOP`：逐步制动→最后一步/支撑落稳→余运动消散。

禁止对所有动作统一写“缓慢自然”“丝滑流畅”。速度词必须有动作原因。

## 9｜Locomotion & Footwork（日常步态与脚步）

日常走、停、转、后退、上下台阶需要最小足部逻辑：
- 当前支撑脚 / 移动脚；
- 起步前重心是否可转移；
- 停步时最后一步如何落稳；
- 大角度转向采用Pivot还是Step-around；
- 转身后脚是否重新种稳，禁止脚底滑轮式旋转；
- 一边走一边做上肢动作时，避免所有步态突然Pause，除非表演/危险触发真正停步；
- 上下楼/跨越障碍时，高度变化与脚步必须有支撑顺序。

不要求普通镜头逐帧写左右脚；只有高风险Locomotion才显式化。

## 10｜Motion Amplitude & Economy（动作幅度与经济性）

默认使用：**Minimum Sufficient Motion｜最小充分动作。**

动作幅度由：
- Objective / Tactic；
- 人物性格与当前克制程度；
- 镜头景别；
- 距离/空间；
- 负载/伤势；
- 紧迫程度

共同决定。

规则：
- CU / MCU：允许眼、头、手、肩的微小变化承担重量，不为“看得见”放大到全身；
- MS：可读的上半身、手上任务、重心变化；
- WS：主要靠步伐、方向、距离、停/走、身体朝向表达；
- 克制人物在高情绪强度下仍可使用很小动作；
- 不让所有动作都变成夸张后仰、猛转身、大幅挥手。

## 11｜Residual / Secondary Motion（残余与次级运动）

主体动作完成后，必要时保留短暂余韵：
- 衣摆/大衣/头发；
- 雨伞、包、吊坠、武器；
- 手臂/肩线因制动产生的小幅跟随；
- 椅子、门、杯中液体等被动作带动的对象。

余韵必须：
- 来源明确；
- 幅度低于主动作；
- 自然衰减；
- 不为了“画面一直动”制造循环。

## 12｜Performance Bandwidth（模型执行带宽）

自然不是动作越多越好。每个短Beat先保留：
1. 剧情/物理不可省的主动作；
2. 最重要的1–3个Emotional Carrier；
3. 让动作自然成立的Preparation / Overlap / Settle；
4. 必要环境/群体反馈。

若信息超载，按：
`合并同一因果链 → 删除无功能装饰动作 → 分时 → 景别转译 → 拆Shot/Segment`。

不得先删除有心理意义的微表情，也不得为了保留微表情而删掉支撑/重心等P0动作逻辑。

## 13｜Stage 04 Integration

Storyboard设计时：
1. 先由Actor Performance确定意图；
2. Action Feasibility证明合法；
3. 对姿态变化明显的Anchor建立Motion Corridor；
4. 标记必要Kinetic Chain / Preparation / Overlap / Locomotion / Settle；
5. Panel只画关键Anchor，不试图把所有过渡塞进静态宫格；
6. 将必要过渡写进Storyboard Motion Intent，供Stage 05继续执行。

### Stage 04 Natural Motion Fail
- 两Panel只能靠人体直线插值才能连接；
- 大转身无Pivot/Step-around；
- 起停/坐站无准备与重心过程；
- 相邻动作被机械串行，出现明显“做完一个再做一个”的机器人节拍；
- 动作幅度与人物/景别严重不匹配。

标记：`NATURAL_MOTION_GAP`。

## 14｜Stage 05 Natural Motion Preflight

FINAL VIDEO PROMPT编译前确认：
```text
[ ] Important pose changes have a valid Motion Corridor
[ ] Whole-body kinetic chain is plausible for the required amplitude
[ ] Required preparation exists; decorative anticipation is removed
[ ] Adjacent actions are overlapped where natural and sequential where physically necessary
[ ] Limb paths follow natural joint arcs / pivot / step-around as appropriate
[ ] Velocity profile matches intent, precision, load and urgency
[ ] Locomotion has credible start/stop/turn/foot support when visible
[ ] Motion amplitude is minimum-sufficient for character + shot scale
[ ] Residual motion exists only where caused and decays naturally
[ ] Performance bandwidth is not overloaded
```

任一关键项失败：`NATURAL_MOTION_FAIL`，返回Stage 04或只重编当前Motion Corridor；**不得靠多Take碰运气。**

## 15｜Model Prompt Compilation

内部分析不要原样复制给模型。最终只保留**一条时间上连续的自然动作链**，并由Prompt Compiler放进对应Shot时间点。

### 差
> 她停止走路。她抬起左手。她把左手放到喉咙。右手握着伞。不要让伞悬空。

### 更好
> 她仍由右手撑伞向前走，听见雨点打在伞面后步幅不自觉缩短；身体还带着最后一点前行惯性时，空闲左臂已经自然松开，前臂沿身体前侧的弧线缓慢抬起，指尖先试探性触到颈前，手掌随后轻贴喉咙。接触发生时她才真正停稳，右手始终维持伞柄支撑，伞面因停步轻微余摆一次后重新稳定。

这段已经同时包含：动作合法性、自然叠接、关节弧线、速度、停步、支撑与余韵。**后文不得再重复写同一动作事实。**

## 16｜与战斗系统

战斗继续以`combat_choreography_engine.md` + `cinematic_combat_vfx_engine.md`为高强度动作Authority。本引擎只补：
- 真实步法/支点；
- 预备与Recovery的人体链；
- 动作之间的叠接；
- 非攻击性身体过渡；
- 近景表演与战斗动作的带宽协调。

不得用“自然动作”把战斗降速成舞蹈，也不得覆盖Combat Initiative / Contact / Counterplay / Force Direction。

## 17｜Hard Rule

**Action Feasibility解决“别穿帮”；Natural Motion解决“别像机器人”。**

两者必须分层求解，最终只编译一次可见动作链。
