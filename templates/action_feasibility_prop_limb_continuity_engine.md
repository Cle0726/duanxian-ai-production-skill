# Action Feasibility & Prop-Limb Continuity Engine（动作可行性与肢体-道具连续性引擎）

> **用途：** 在Stage 04分镜动作设计与Stage 05 FINAL VIDEO PROMPT编译前，主动证明“角色的身体、手脚、支撑关系与道具在每个动作Beat中都能物理成立”。它解决的不是“剧情上道具属于谁”，而是“下一秒做这个动作时，哪只手/哪条腿可用、当前支撑是否仍存在、换手/放下/接触/重心转移是否有必要前置动作”。
>
> **定位：** 本引擎是六阶段外侧的内部动作求解层，**不是Stage 07**。它与`world_state_continuity_engine.md`互补：World State负责跨Scene/Beat/Segment的语义守恒；本引擎负责Shot/Beat内部的瞬时身体资源、支撑图与动作前置条件。

## 1｜核心原则：Solve Before Prompt（先求解，再写提示词）

任何涉及人物身体动作、持物、接触、支撑、坐/站/走/跑、开门、拿放物体、换手、扶人、战斗、多人接触的Segment，在进入最终动作描述前按：

**State → Requirement → Resource / Support Audit → Conflict → Minimal Physical Resolution → Bridge → Execution → Exit State**

禁止只写：
> “她拿着伞。她把手按到喉咙。”

而不回答：
- 哪只手持伞？
- 哪只手去摸喉咙？
- 目标手是否空闲？
- 伞的支撑是否持续？
- 若必须用持伞手，伞是否先换手/放下/交给他人？
- 动作完成后两只手和伞分别在哪里？

**正向可执行解优先于末尾禁令。** 与其只写“不要让伞悬空”，更优先写“右手持续握住伞柄，空闲左手抬起按住喉咙”。

## 2｜与World State / Performance / Action Physics的职责边界

### World State Continuity回答
- 道具Identity / Owner / Holder / Location / State；
- Ongoing Physical Task是否延续；
- 人物/道具/伤势/环境如何跨CUT或Scene守恒；若完整Transformation已经触发Recovery，动作可行性必须读取Post-Recovery Injury State，不能继续把已修复肢体当受伤资源。

### Actor Performance回答
- 为什么角色现在要做这个动作；
- Objective / Tactic / Stimulus / Listening如何让动作发生。

### Action Feasibility回答
- **哪个身体资源执行动作；**
- **该资源当前是否可用；**
- **原本由它维持的支撑/接触/持物如何处理；**
- **需要哪些最小前置Bridge才能让动作合法。**

### Natural Motion / Kinematic Performance回答
- 合法动作怎样通过Functional Preparation、整个人体动力链、动作叠接、自然关节弧线、速度/步态与Settle完成；
- Storyboard静态Anchor之间怎样建立Motion Corridor，避免机械Pose插值。

### Action Physics回答
- 在自然动作路径已经确定后，具体处理接触、受力、惯性、反作用、材质与环境反馈。

固定顺序：

**Performance Intent → Action Feasibility Solver → Natural Motion / Kinematic Performance → Action Physics → Prompt Compiler**

不得把“物理上做不到”误当成表演细节问题，也不得靠视频生成后的QC才第一次发现。

## 3｜Body Resource / Occupancy State（身体资源与占用状态）

只激活当前动作真正涉及的字段，不要求每个普通镜头填满整张表。

建议资源：

```text
LEFT_HAND：FREE / OCCUPIED / SUPPORTING / CONTACTING / TRANSFERRING / RESTRICTED
RIGHT_HAND：FREE / OCCUPIED / SUPPORTING / CONTACTING / TRANSFERRING / RESTRICTED
LEFT_ARM / RIGHT_ARM：AVAILABLE / LOADED / PINNED / SUPPORTING / RESTRICTED
LEFT_LEG / RIGHT_LEG：SUPPORT / MOVING / KICKING / KNEELING / RESTRICTED
TORSO：UPRIGHT / LEANING / TURNING / SUPPORTED / FALLING
HEAD_GAZE：TARGET / DIRECTION / RESTRICTED
MOUTH：SPEAKING / HOLDING_OBJECT / OCCLUDED（仅必要时）
CURRENT_SUPPORT：地面/椅子/墙/他人/扶手等
CURRENT_CONTACT：手-物 / 手-人 / 脚-地 / 身体-环境
HELD_PROPS：Prop ID → Limb / Grip / State
WORN_OR_ATTACHED_PROPS：不占手但可能限制动作的物件
ONGOING_TASK：CONTINUE / SLOW / INTERRUPT / COMPLETE / TRANSFER / ABANDON
```

### Occupancy Rule
同一身体资源不能同时承担两个互斥任务。

例：
```text
RIGHT_HAND = HOLDING_UMBRELLA
Requested = RIGHT_HAND_TO_THROAT
=> CONFLICT
```

若`LEFT_HAND = FREE`且剧情未指定必须右手：
```text
Minimal Physical Resolution = LEFT_HAND_TO_THROAT
```

## 4｜Support Graph（支撑图）

对会因为手/脚/身体离开而失去支撑的关键对象，建立最小支撑关系：

```text
Umbrella → supported_by Right Hand → connected_to Character Body
Cup → supported_by Left Hand
Suitcase → Handle → Right Hand
Body Weight → Pelvis → Chair
Body Partial Weight → Left Palm → Wall
Injured Person → supported_by Character A Right Arm + Character B Shoulder
```

### Support Conservation Rule
如果动作删除一条必要Support Edge（支撑边），必须满足至少一个条件：
1. 新支撑在删除前已经建立；
2. 物体被合法放置到稳定表面；
3. 物体被合法转交给他人；
4. 剧情明确要求Drop / Fall，并写出重力与后果。

否则：

`PROP_SUPPORT_LOSS = HARD FAIL`

**关键例：** 右手撑伞 → 右手去摸喉咙，而无左手接伞、放下伞或掉伞动作，即为支撑边凭空消失。

## 5｜Action Preconditions（动作前置条件）

每个重要动作先判断所需条件。

### Reach / Touch
- 目标部位在可达范围；
- 执行肢体可用；
- 必要时先释放/转移持物；
- 有`Approach → Contact`，不能从远处直接跳到接触完成。

### Pick Up
- 手可用；
- 物体可达；
- 先接触/形成Grip，再离开原支撑面。

### Put Down
- 找到稳定落点；
- 物体先接触落点，再释放Grip。

### Hand Transfer
- Receiver Hand先接触并承担控制；
- Holder Hand再释放；
- 中间不得出现无人支撑的Gap，除非明确抛接。

### Sit / Stand
- 身体与椅子/支撑位置关系成立；
- 坐下前有重心下降与接触；
- 站起前有足部/躯干承担重量。

### Step / Kick / Kneel
- 抬起的腿不能继续是唯一承重腿；
- 先将重心转移到另一支撑点，再执行抬腿。

### Open / Close / Turn / Pull
- 手已到达可操作部位；
- 旋转/拉动方向与关节/铰链/把手结构一致；
- 若另一只手在稳定物体/身体，保留该支撑任务。

### Carry / Support Another Person
- 承重肢体和身体姿态足以维持负载；
- 若要用同一肢体做新动作，必须先转移负载。

## 6｜Conflict Types（硬冲突类型）

### `LIMB_OCCUPANCY_CONFLICT`
同一手/脚/肢体被要求同时执行互斥动作。

### `PROP_SUPPORT_LOSS`
支撑道具/负载的身体部位离开后没有新支撑。

### `PROP_TRANSFER_GAP`
物体从A手/人物突然变到B手/人物，没有交接、放置或抛接链。

### `CONTACT_PRECONDITION_MISSING`
接触结果出现，但缺少靠近/到达/Grip/落位等前置条件。

### `SUPPORT_BALANCE_CONFLICT`
承重脚/手被抽走，但重心没有先转移。

### `SIMULTANEOUS_ACTION_CONFLICT`
单独都可做，但当前身体资源下不能同时成立。

### `ONGOING_TASK_DROP`
新表演动作出现后，旧的现实任务无因消失或被模型忘记。

### `ACTION_EXIT_STATE_GAP`
动作完成后没有明确手、道具、姿态、接触或支撑的落点，下一Beat容易随机Reset。

### `INTER_CHARACTER_LOAD_CONFLICT`
扶人/拉人/抱持/搀扶等多人负载关系被新动作无因打断。

### `GEOMETRY_REACH_CONFLICT`
人物/道具空间距离或身体朝向使目标动作不可达，却没有移动/转身/靠近Bridge。

## 7｜Minimal Physical Resolution（最小物理解）

Skill默认自动解决**不改变Story / Canon / Character Identity / 剧情结果**的执行冲突，不反问用户。

优先级：
1. 使用当前空闲且自然的肢体；
2. 保持当前持物/支撑任务不变；
3. 必要时加入最短Transfer / Put-down / Shift-weight / Turn / Step / Reach Bridge；
4. 保持角色习惯、**当前有效伤势状态（含Transformation Recovery后的Post-Recovery State）**、惯用手、服装限制与当前Blocking；
5. 选择最少动作、最少新信息、最易被模型稳定执行的解。

### 示例A｜空闲手可直接解决
```text
State：Right Hand holds umbrella; Left Hand free.
Requirement：touch throat.
Resolution：Left Hand touches throat; Right Hand preserves umbrella support.
```

### 示例B｜剧情指定必须用持物手
```text
State：Right Hand holds umbrella; Left Hand free.
Requirement：Right Hand touches throat.
Bridge：Left Hand reaches umbrella handle → establishes grip → Right Hand releases → Right Hand rises to throat.
```

### 示例C｜双手都被占用
```text
State：Both Hands carry tray.
Requirement：Both Hands cover ears.
```
若Story没有说明托盘处理方式，`Put Down / Hand Off / Drop`会产生不同剧情含义，不得偷偷任选。标记：

`ACTION_DECISION_REQUIRED = STORY-SIGNIFICANT`

由`decision_authority_conflict_resolution.md`判断是否需要ASK_REQUIRED。

## 8｜Micro Transition / Action Bridge（微动作桥）

Bridge不是为了炫技，而是为了满足动作前置条件。

常用Bridge：
- FREE_HAND_SELECT｜改用空闲手；
- HAND_TRANSFER｜换手；
- PUT_DOWN / PICK_UP｜放下/拿起；
- HAND_OFF｜交给他人；
- SHIFT_WEIGHT｜重心转移；
- STEP_IN / TURN / LEAN｜靠近/转身/俯身；
- TASK_SLOW / TASK_INTERRUPT / TASK_RESUME｜原任务减速/中断/恢复；
- CONTACT_ESTABLISH / RELEASE｜建立/释放接触。

**Bridge只在必要时显性化。** 普通、低信息、可被模型稳定理解的微小动作可合并进一条连续正向动作描述；但支撑、换手、重心、多人负载这类P0物理关系不得省略到失去因果。

## 9｜Action State Table（复杂Beat内部状态表）

复杂或高风险Beat在Stage 04/05内部建立短表，不直接复制给模型：

| Beat | Left Hand | Right Hand | Support / Contact | Prop State | Ongoing Task | Exit |
|---|---|---|---|---|---|---|
| B01 | FREE | Umbrella | Umbrella→RH | OPEN | WALK | walking |
| B02 | rising to throat | Umbrella | Umbrella→RH | OPEN | SLOW | near stop |
| B03 | on throat | Umbrella | Umbrella→RH | OPEN | INTERRUPT | stationary |

一旦出现：
```text
B01 Right Hand = Umbrella
B02 Right Hand = Throat
Umbrella Support = NONE
```
即触发`PROP_SUPPORT_LOSS`。

### 何时必须建表
- 两个以上持物/接触对象；
- 双手/双脚同时有任务；
- 换手、放下、拾取、开门、穿脱、扶人；
- 坐/站/跪/跌倒/起身；
- 战斗武器与表演动作交织；
- 多人接触、拉扯、抱持、搀扶；
- 上一次生成已经出现悬空/穿模/换手/支撑错误；
- Shot Investment Tier T3/T4中的复杂身体动作。

普通人物站立说话、单一自由手小动作等无需机械建表，但仍执行快速Occupancy Check。

## 10｜Stage 04 Integration（分镜阶段）

Stage 04在确定每个关键Panel/Shot动作之前：
1. 从World State读取当前Holder / Ongoing Task / Body Condition；
2. 从Performance得到动作意图；
3. 运行Body Resource + Support Graph；
4. 解决冲突与必要Bridge；
5. Storyboard只画**已经物理成立**的动作锚点；
6. Exit State记录下一Panel/Shot继续需要的手、道具、姿态、支撑。

Storyboard不能只画“动作结果Pose”而省略决定性前置动作。例如换手是当前剧情动作成立的必要条件时，至少一个Panel/同Shot中间状态必须让交接可读。

### Stage 04 Hard Fail
存在以下任一项不得通过Storyboard QC：
- 关键Held Prop无支撑来源；
- 同一肢体互斥占用；
- 明确换手无Transfer；
- 重要接触无Approach；
- 抬起唯一承重肢体无重心转移；
- Ongoing Task无因消失；
- Exit State无法解释下一Panel。

## 11｜Stage 05 Preflight（视频提示词编译前硬闸门）

Prompt Compiler在输出`FINAL VIDEO PROMPT`之前必须执行：

```text
ACTION FEASIBILITY PREFLIGHT
[ ] Held Props all have continuous support
[ ] Limb occupancy has no unresolved conflict
[ ] Prop transfer has an explicit hand-off / placement / throw-catch path when required
[ ] Contact actions contain necessary approach / reach / grip / release preconditions
[ ] Weight-bearing transitions occur before lifting a support limb
[ ] Ongoing Physical Task is CONTINUE / SLOW / INTERRUPT / COMPLETE / TRANSFER / ABANDON, never silently reset
[ ] Inter-character support/load is conserved
[ ] Exit State defines relevant limbs / props / posture / contact / support for next Beat
```

任何一项失败：

`ACTION_FEASIBILITY_FAIL`

**不得输出FINAL VIDEO PROMPT。**

能通过Minimal Physical Resolution修复的，Skill自动补Bridge后重新检查；只有会改变剧情意义且Authority无法裁决时才升级`ACTION_DECISION_REQUIRED`。

## 12｜Downstream Compilation（下游编译）

本引擎的直接产物是**合法动作骨架**，不是最终模型Prompt。内部State Table、Conflict Code、Support Graph不要原样塞给视频模型。

合法骨架至少回答：
- 当前持续任务；
- 执行动作的明确肢体；
- 必要Bridge；
- 支撑/持握如何继续；
- Approach / Contact / Release；
- Exit State。

随后必须交给`natural_motion_kinematic_performance_engine.md`，把骨架自然化为Preparation / Kinetic Chain / Motion Arc / Overlap / Velocity / Locomotion / Settle / Residual Motion；最后由`prompt_semantic_deduplication_engine.md`把这一整条动作链只写入对应`Integrated Shot Timeline`一次。

因此本层不再自己生成一套“最终动作段 + 末尾No-floating禁令”。正向合法解与自然运动合并后若已覆盖风险，后文不得重复同义禁止项。

## 13｜Combat Integration（战斗接入）

战斗仍由`combat_choreography_engine.md`决定战术与Exchange，本引擎负责每个Exchange内部的身体资源可行性：
- 双手武器不能无因腾出一只手做表演；
- 格挡手仍承受接触/压力时不能同时抓别的目标；
- 支撑脚抬起前必须先转移重心；
- 抓住/扶住同伴后，负载关系不能在下一击无因消失；
- 武器换手必须有Transfer；
- 当前仍受伤/受限的肢体不能被当作FREE资源；若伤势已通过Transformation Recovery合法解除，则不得继续套用旧限制；
- Contact Point与Action Feasibility一致。

若战术设计要求一个当前物理不可能的动作：能在不改变Stage 02核心Distance / Axis / Spatial Dominance的前提下用局部动作桥解决，Stage 04只修Micro-Blocking / Exchange；若必须改变核心Blocking / Distance / Axis / Attack Lane，则回Stage 02做Director Contract最小Patch。不在Stage 05用语言硬压模型。

## 14｜Decision Authority（自动裁决与提问）

### `DERIVED PHYSICAL RESOLUTION`
可安全自动决定：
- 使用空闲手；
- 同手任务冲突时做最小换手；
- 为坐下/迈步/转身补最小重心与靠近动作；
- 保持已有Held Prop/Support；
- 原任务自然减速、短暂中断后恢复。

### `OPEN_NONBLOCKING`
不影响当前镜头物理可行性的细节，如非关键惯用手尚未建档，可按当前Blocking选最自然解并记录为本段Derived，不升级长期Canon。

### `ASK_REQUIRED / STORY-SIGNIFICANT`
只有当所有合法解都会改变剧情意义，例如：
- 必须丢掉关键物品还是放下；
- 是否松开正在悬挂/救援的角色；
- 是否让关键道具损坏；
- 谁接过会改变责任/关系/Knowledge；
且现有Story/Canon/Authority无法裁决时，才允许问用户。

## 15｜QC / Failure Routing

### 生成前发现
- 物理可行性冲突 → 先判断是否仅Micro-Blocking/动作桥：是则Stage 04修；若影响Stage 02核心Blocking / Distance / Axis则回Stage 02最小Patch；若只是Stage 05遗漏且Storyboard已有合法解，则只重编Prompt。

### 生成后发现
- Prompt里没有明确合法动作解 → `ACTION_FEASIBILITY / PROP-LIMB CONTINUITY DESIGN FAILURE`，回Stage 04/05最小修正；
- Prompt已有明确合法解但模型偶发悬空/错手 → `RANDOM GENERATION FAILURE`或`ACTION EXECUTION FAILURE`，按Failure-before-Compute处理；
- Prop结构本身错误 → Stage 03；
- 跨Scene Holder/Location来源错误 → Stage 02 World State；
- 战术/Blocking本身不成立 → Stage 04 Combat/Storyboard。

## 16｜Action Feasibility QC

每个高风险动作至少回答：
1. 谁在做？
2. 用哪个身体资源？
3. 该资源当前是否FREE/可用？
4. 原来由它维持的Held Prop / Support / Contact怎么办？
5. 是否需要Transfer / Put-down / Shift-weight / Step / Turn / Reach？
6. 接触前置条件是否完整？
7. Ongoing Task是继续、减速、中断、完成还是转交？
8. 动作结束后各肢体、道具、支撑和身体姿态在哪里？

如果第3–8项任何一项无法回答，不得把动作直接交给视频模型。

## Current｜Action Set Consistency
如果某段声明“人物唯一允许动作/唯一动作范围”，该声明必须进入Typed `ACTION_SET`。后续Timeline若要求同一主体新增动作，必须显式更新Action Set并重新Conflict Solve；不得一边写“唯一动作=急刹反应”一边又追加独立掰扶手动作。失败：`ACTION_SET_CONFLICT`。

## V4.5.5｜Everyday Ergonomic Baseline

本引擎的Support/Reach规则前移到普通静态资产QC：坐、站、靠、拿、开门、乘车等不需要等到Video动作阶段才第一次检查。

普通剧情至少证明：
- 坐姿有真实Seat/Support Surface，腿脚与家具留有空间；
- 站姿脚与地面/支撑成立，身体不穿墙/扶手/座椅；
- 手持/操作物在可达范围并符合Affordance；
- 人体尺度与空间/家具尺度合理；
- 人物从当前Zone到目标门/通道/设备存在可行路径。

静态资产已经出现明显`ERGONOMIC_SUPPORT_FAIL / HUMAN_ENVIRONMENT_INTERSECTION_FAIL / GEOMETRY_REACH_CONFLICT`时必须Stage 03修正，禁止带入Storyboard/Video“试试看”。
