# World State Continuity Engine（世界状态连续性引擎）

> **用途：** 在Stage 02导演拆解时，先证明“这个世界怎样从上一状态变成下一状态”，再做Shot / Segment与Episode Asset Requirement Manifest。它解决人物、车辆、道具、服装临时状态、伤势、环境破坏、知识、关系与行动任务在换Scene / Beat / Segment时凭空出现、凭空消失、瞬移或重置的问题。
>
> 服装与个人装饰运行时状态与 `character_closet_registry.md` / `personal_adornment_identity_system.md` 共享同一事实源：当前LOOK、已穿/携带/脱下单品、Active Adornment、Rotation Pool绑定、湿度、污渍、破损和最后一次Transition不得分叉。
>
> 核心原则：**世界可以省略过程，但不能无因刷新状态。**

---

## 1｜核心定律：State Conservation（状态守恒）

任何重要状态从A变成B时，都必须满足至少一种：

1. **Visible Transition｜可见转变**：观众直接看到关键变化发生；
2. **Residual Transition｜余波式转变**：过程可省略，但新镜头明确保留“刚刚发生过”的痕迹；
3. **Implied Transition｜可安全推断转变**：上下文已经给足原因，观众可自然补全；
4. **Intentional Ellipsis｜有意省略**：明确的时间/空间跳跃，且新状态不与已知事实冲突；
5. **World Mechanic｜世界规则转变**：已有Canon明确允许生成/消散/瞬移/恢复等机制；其中`TRANSFORMATION_RECOVERY`是当前已确认机制：角色成功完成合法完整变身时，普通可恢复伤口可在Transformation Completion节点真实修复。

如果以上都不成立，则标记：

`CONTINUITY GAP / ILLEGAL STATE JUMP`

### Nothing Spawns. Nothing Vanishes.
普通人物、车辆、道具、伤势、湿度、破损、知识、关系状态不能因为换Scene就刷新。

唯一例外是：
- 已确认的世界机制；
- 明确的时间跳跃足以解释变化；
- 过程被合理省略且观众仍能读出前因后果。

例如已确认P0 Combat Canon：
`Virtuoso Weapon + Transformation Costume + Accord Baton`在战斗结束/变身解除时同步消散，属于合法World Mechanic。

当前新增P0 Transformation Canon：
`TRANSFORMATION_RECOVERY`＝**成功完成合法完整变身时，变身前普通可恢复伤口可以在完成点真实修复。** 这不是Scene Reset，也不是视觉遮盖；它必须产生新的身体World State。解除变身后继承该Post-Recovery State，不得把旧伤重新刷回。

---

## 2｜不是流水账：Minimum Necessary Bridge（最小必要过渡）

本引擎**不要求把所有操作步骤拍出来**。

错误理解：
> 开车 → 踩刹车 → 拉手刹 → 解安全带 → 开门 → 左脚落地 → 右脚落地 → 关门 → 走到剧院。

正确目标：
> 只保留让观众相信“A状态确实合理落到B状态”的最小证据。

判断问题不是：
> “中间每一步拍了吗？”

而是：
> **“观众能不能理解这个新状态是怎么来的？”**

---

## 3｜World State Ledger（世界状态账本）

Stage 02为每个重要Scene / Transition维护语义状态，不要求把所有字段都写进最终Prompt，只记录当前剧情真正会影响连续性的项目。

### A. Time / Location
- Current Location：
- Previous Location：
- Time / Elapsed Time：
- Interior / Exterior / Vehicle：
- Route / Entry Point / Exit Point（重要时）：

### B. Motion State
- Character Motion：静止 / 步行 / 奔跑 / 摔倒 / 被拖拽 / 其他
- Vehicle Motion：行驶 / 减速 / 刚停稳 / 停放 / 启动 / 其他
- Current Momentum / Direction（重要时）：

### C. Character Presence / Spatial State
- Characters Present：
- Entering / Leaving：
- Position / Left-Right：
- Body Orientation：
- Gaze / Attention Target：
- Current Contact（扶住、抓住、靠墙、坐在车内等）：

### D. Prop Persistence / Possession
每个剧情关键道具至少可追踪：
- Prop ID：
- Owner：
- Current Holder：
- Current Location：
- Visible：YES / NO
- State：折叠/展开、开/关、完整/破损、装载/卸下等
- Last Confirmed Transition：

**Visible = NO 不等于不存在。**

例如节目单收进大衣内袋后：
`Holder = Character A / Location = coat inner pocket / Visible = NO`

之后重新拿出时才有明确来源。

### E. Ongoing Physical Task
- 当前正在做什么：驾驶、整理工具、折纸、擦拭、找钥匙、扶人、观察设备等
- 下一Beat：继续 / 完成 / 被打断 / 主动放弃 / 转交他人

Scene/CUT不能自动把Ongoing Task清零。

### F. Costume / Body Condition
- Current LOOK ID：
- Items Worn：
- Detached / Carried Wardrobe：物品ID + Holder / Location / State
- Costume Configuration：穿好 / 敞开 / 脱下 / 卷袖等
- Active Personal Adornment：AC IDs + Placement + State
- Detached / Stowed Adornment：AC ID + Holder / Location / State
- Adornment Current LOOK Binding：
- Pre-Transformation Adornment Snapshot（变身时）：
- Adornment Transformation Rule / Physical Disposition（变身时）：
- Wetness / Dirt / Blood / Damage：
- Injury / Pain / Fatigue：
- Pre-Transformation Injury Snapshot（变身时）：
- Transformation Recovery Eligibility：ELIGIBLE / PARTIAL / NOT ELIGIBLE + Reason
- Transformation Recovery Result：NOT TRIGGERED / RECOVERED / PARTIALLY RECOVERED / BLOCKED BY CANON
- Post-Recovery Injury State：
- Transformation State：
- Temporary Physical Limitation：

换Scene不自动恢复干净、无伤或默认姿态。**但成功完成合法完整变身不是普通换Scene，而是允许触发`TRANSFORMATION_RECOVERY`的World Mechanic。** 若伤势为ELIGIBLE，则变身完成点把身体状态更新为`Post-Recovery Injury State`：普通开放伤口可闭合/消失，相关活动性出血可停止，由该伤口直接造成的临时动作限制可解除；之后Transformation State与解除变身后的日常身体都继承新状态，不得恢复旧伤。独立疲劳、圣约消耗、永久疤痕/永久身体特征、不可逆损伤、死亡或最新Canon明确不可修复的伤势不自动清零。

变身只暂停**正在穿着**的Daily Wardrobe；已经脱下、拿在手里、放在场景中的衣物继续作为普通World State物体存在，不能因Transformation凭空消失。**身体伤口被修复不等于旧衣物/环境被清洗或倒带：** Pre-Transformation Daily衣物上的血迹、破损，掉落物与环境血迹/破坏继续守恒，除非另有明确机制。稳定个人装饰同样遵守State Conservation：RETAIN持续存在；REMOVE必须有Stow去向；ABSORB/物理TRANSLATE必须由Canon World Mechanic支持；REPLACE不能抹掉原日常物件。解除变身默认恢复Pre-Transformation Adornment Snapshot，除非期间发生有因变化。

### G. Knowledge / Relationship / Objective
- Knowledge State：谁已经知道什么
- Suspicion / Trust / Relationship Shift：
- Current Objective / Unresolved Intention：
- Emotional Pressure Carryover：

**Scene Change ≠ Memory Reset。**
角色不能凭空知道未接收的信息，也不能无因忘记刚发生的重大事实。

### H. Environment Runtime State
- Door / Window / Lock：
- Light / Power：
- Global Color DNA Ref：项目级综合色语法，不随Scene切换清零
- Scene Color Extension Ref / Spec：当前地点综合色派生；换地点时重新裁决，不沿用上一Scene Extension
- Current Shot / Segment Lighting Variant：NONE / TEXT_CONTROL / Approved Lighting Ref；若灯灭、火焰、雷光等改变真实环境照明，必须同步写入Light / Power并按State Diff延续
- Weather：
- Fire / Smoke / Water：
- Environment Damage：
- Important Object Placement：
- Crowd Runtime State（适用时；读取`crowd_presence_ambient_life_engine.md`）：Density / Zones+Clusters / Primary Flow(s) / Stationary Activity Zones / Entry-Exit Sources / Attention Distribution / Current Stimulus / Reaction Propagation State / Persistent Crowd Change：
- Audio World State（失声、警报、持续机械声、雨声等重要规则）：

Environment Master负责“原本长什么样”；Runtime State负责“现在已经发生了什么”。

---

## 4｜State Diff Pass（状态差异检查）

任何相邻Scene / Beat / Segment，在正式拆Shot前先比较：

`EXIT STATE A → REQUIRED ENTRY STATE B`

逐项找出变化：

- 地点是否改变？
- 人物是否移动了大距离？
- 车辆是否从运动变静止 / 反之？
- 人物是否进入 / 离开？
- 道具是否换手、收起、展开、损坏、消失？
- 门窗/灯/设备状态是否改变？
- 衣服是否突然干净/干燥/恢复？
- 伤势、疲劳、血迹是否倒退？若变化发生在Transformation Completion，先检查是否为合法`TRANSFORMATION_RECOVERY`，不要把真实修复误判为连续性错误。
- 场景破坏是否被重置？
- 人物是否突然知道了不该知道的信息？
- Crowd是否在CUT/Scene后无因从活跃变冻结、Density突变、主流Flow反向、已发生的撤离/聚集状态被重置？
- 关系/目标/情绪压力是否无因归零？
- 环境声/世界规则是否无因恢复？

每个Diff必须被分类，不允许默默忽略P0变化。

---

## 5｜Transition Classification（过渡分类）

### A. `DIRECT_CONTINUITY`
A与B直接连续，不需要新增桥。

例：
> 同一房间，Character A从桌边转身走向门口。

### B. `IMPLIED_TRANSITION`
中间步骤虽然没拍，但上下文已经足够让观众自然补全。

例：
> Character A说“我们走吧” → CUT → 同一建筑门外，两人已经走出来。

前提：不存在锁门、道具转移、伤势变化等新的未解释P0问题。

### C. `RESIDUAL_BRIDGE`
不必拍完整过程，但要让新镜头保留“刚发生过”的余波。

例：
> 前一Scene车还在行驶 → CUT到剧院外，车身刚刚停稳、车灯/雨刷仍在工作，车门已经开始打开。

观众能感觉：
> **他们刚到，不是车凭空停在那里。**

### D. `VISIBLE_BRIDGE`
必须让观众看见关键状态改变。

常见触发：
- 重要目的地首次抵达；
- 上一状态有明显动势（行驶/奔跑/追逐），下一状态突然静止；
- 关键人物进入/离开；
- 关键道具换手/被收起/被取出；
- 剧情门/锁/障碍必须被处理；
- 伤势/环境状态发生不可忽略变化。

例：
> 车内对白末尾已看到剧院轮廓 → CUT外景，旅行车从雨中驶近并靠边减速 → CUT中景，人物正在开门下车。

### E. `INTENTIONAL_ELLIPSIS`
明确有意跳过一段时间/路程。

必须满足：
- 时间/空间跳跃可读；
- 新状态不违反旧状态；
- 关键Prop / Injury / Knowledge等仍有合理来源。

### F. `CONTINUITY_ERROR`
没有任何合法桥能够解释。

例：
> 工具箱已明确留在车内 → 角色没有返回车辆 → 下一Scene突然在地下室打开同一工具箱。

此时不能靠Storyboard“顺便画出来”掩盖。

---

## 6｜Arrival Must Be Felt（到达必须被感受到）

当上一状态仍是明显移动中，而下一状态已经进入“抵达后”，优先判断观众是否真正感受到**到达**。

适用：
- 行驶车辆 → 停车/下车
- 步行/奔跑 → 抵达目的地
- 火车 → 进站
- 船 → 靠岸
- 电梯 → 到层
- 追逐 → 冲入新空间

### 三种合法表达

**Visual Arrival｜直接看见到达**
> 车辆驶入目的地、减速并落位。

**Residual Arrival｜看见刚到的余波**
> 车辆刚停稳，发动机/雨刷/灯仍延续，人物已开始开门。

**Context-Supported Ellipsis｜上下文支持的省略**
> 前一镜已明确“到了”且目的地已近在眼前，下一镜直接从正在下车开始。

### 强制升级到VISIBLE / RESIDUAL的情况
- 目的地首次作为重要Environment Reveal；
- 上一镜强烈强调移动；
- Arrival同时承担空间建立、人物分流、道具去向、天气暴露等多个连续性功能；
- 直接跳到室内会产生“瞬移感”。

**原则：观众不必看完整停车过程，但必须感觉移动状态已经合理落地。**

---

## 7｜Entry / Exit Logic（进入与离开）

人物不能无因出现在场或消失。

每次角色阵容变化检查：
- 从哪里进入？
- 从哪里离开？
- 是否需要观众看见？
- 离开后是否还听得到/看得到？
- 新进入者合理听到了多少信息？

### Information Access
人物进入时间同时决定Knowledge State。

例：
> Character C在对话后半段才进入，则不能自动知道前半段私密信息，除非另有信息来源。

---

## 8｜Prop Persistence & State Transition（道具持续与状态变化）

关键道具执行“物品守恒”：

`Identity → Owner → Holder/Location → State → Transition → New Holder/Location/State`

必须解释：
- 为什么从右手变左手；
- 为什么从A变成B持有；
- 为什么从可见变不可见；
- 为什么折叠变展开；
- 为什么关闭变打开；
- 为什么完整变损坏；
- 为什么留在车里的东西后来出现在建筑里。

允许通过CUT省略“很普通的手部操作”，但**新状态必须有可信来源**。进入Stage 04/05后，若同一Shot/Beat内发生持物手参与新动作、换手、放下/拾取、支撑变化或多人负载变化，继续交给`action_feasibility_prop_limb_continuity_engine.md`证明瞬时肢体占用与Support Chain；World State的“Holder正确”不自动等于动作过程物理可行。

---

## 9｜Character State Carryover（人物状态延续）

以下状态默认跨Scene / CUT持续，直到有原因改变：
- Injury / Pain / Fatigue（**Transformation Completion可作为伤口改变的合法原因；一旦RECOVERED，后续继承Post-Recovery State而不是旧伤**）
- Wetness / Dirt / Blood
- Costume temporary configuration + Detached/Carried Wardrobe Holder/Location
- Transformation state
- Ongoing physical task的结果
- Knowledge
- Suspicion / Trust / Relationship tension
- Unresolved Objective / Emotional Pressure

例：
> 室外淋雨 → 刚进入剧院：发梢/外套仍应保留刚淋雨的状态；
> 受伤后只换房间：伤势不能因为Scene Opening恢复；若期间成功完成合法完整变身并触发`TRANSFORMATION_RECOVERY`，则新Scene应继承恢复后的伤势状态；
> 刚得知重大秘密：下一Scene不自动回到Neutral。

---

## 10｜Environment Runtime Continuity（环境运行状态）

场景身份与场景当前状态分开：

**Environment Master**
> 空间几何、固定结构、正常状态。

**Runtime Environment State**
> 当前灯光/门窗/破坏/烟雾/水/火/散落物/群众方向等；综合色使用当前Scene Color Extension，临时Shot Lighting Variant只有在真实改变环境照明状态时才跨Shot/Segment延续。

战斗破坏、停电、门被打开、玻璃破碎后，回到同一地点时默认继承，除非：
- 明确修复；
- 足够时间过去；
- 已确认世界机制恢复。

---

## 11｜Transition Beat Generator（过渡Beat生成器）

State Diff发现需要桥时，Stage 02自动生成**最小必要Transition Beat**，不询问用户普通导演选择。

输出：

```text
【Transition Audit｜SCENE_A → SCENE_B】

Exit State：
- Vehicle：moving
- Characters：A driver / B passenger / C rear seat
- Prop X：B hand
- Weather：rain

Required Entry State：
- Vehicle：parked outside Destination
- Characters：walking toward entrance
- Prop X：B coat inner pocket
- Wetness：light rain exposure

State Diff：
- MOVING → ARRIVED
- IN VEHICLE → OUTSIDE
- PROP VISIBLE → POCKETED
- DRY/INTERIOR → LIGHT WETNESS

Classification：VISIBLE_BRIDGE

Minimum Necessary Bridge：
1. 目的地雨夜外景；车辆从街道驶近并减速落位。
2. CUT中景；车门正在打开，人物开始下车。
3. Character B在下车/走向入口过程中把Prop X收进内袋。

New Asset Impact：
- Destination Exterior / Entrance environment required

Story Impact：
- DERIVED DIRECTORIAL CONNECTIVE TISSUE
- 不改变`EPISODE SCREENPLAY LOCK / Locked Story Facts`
```

如果`RESIDUAL_BRIDGE`更省时且足够清楚，就不强制完整Visual Arrival。

---

## 12｜Bridge Economy（过渡经济性）

过渡不是为了“完整”，而是为了**可理解**。

优先：
1. 一镜解决多个状态变化；
2. 用环境建立镜头同时承担Arrival；
3. 用角色正在下车/进门的动作承担位置转变；
4. 用Ongoing Task自然解决道具收起/转交；
5. 必要时用Sound Bridge / J-cut / L-cut辅助，但声音不能替代必须可读的P0视觉因果。

避免：
- 为每一个门把手、脚步、停车步骤建立独立Shot；
- 重复展示观众已经理解的动作；
- Transition Beat比剧情Beat更长；
- 为连续性把一集拖成生活流水账。

---

## 13｜Stage 02执行顺序

正式Stage 02顺序升级为：

**EPISODE SCREENPLAY LOCK**
→ **Screenplay Scene**
→ **World State Ledger**
→ **State Diff / Transition Audit**
→ **必要Transition Beat补齐**
→ **Actor / Combat Brief**
→ **Detailed Shot Contract / Director Core**
→ **Segment Plan**
→ **Raw Asset Demand → Asset Consolidation & Sufficiency Audit → Final Episode Asset Requirement Manifest**

也就是说：
> 先让故事世界逻辑接得上，再锁镜头和资产。

---

## 14｜对Stage 03的影响

Transition Audit如果发现新Bridge需要正式空间资产，例如：
- 剧院外观/入口
- 车外停车区域
- 建筑之间的必经连接空间
- 重要门厅/走廊

则必须在Stage 02进入Raw Asset Demand，并在Asset Consolidation & Sufficiency Audit后写入Final Episode Asset Requirement Manifest。

不能等Stage 04才发现：
> “需要拍抵达，但根本没有这个Environment Master。”

短期湿度、轻灰尘、临时开门等仍优先作为Runtime State，不因本引擎过度资产化。

---

## 15｜对Stage 04 / 05的影响

World State Ledger负责**语义状态连续性**；
Previous Ending Frame + Continuity Snapshot负责**相邻CONTINUITY_ENTRY的精确视觉连续性**。

两者不是替代关系。

### SCENE_OPENING特别规则
`SCENE_OPENING`只表示：
> 不默认使用上一Scene Ending Frame作为图像输入。

它**绝不表示**：
> World State Reset。

所以新Scene仍必须继承：
- Props
- Injury（若已发生`TRANSFORMATION_RECOVERY`则继承Post-Recovery Injury State，禁止旧伤回滚）
- Wetness / Dirt
- Knowledge
- Relationship / Objective carryover
- Environment-wide world rules
- 已经发生的剧情事实

### CUT_ENTRY
即使不使用上一尾帧，也必须读取相关World State Delta，防止道具、伤势、方向、任务状态在CUT后刷新；若Delta包含`TRANSFORMATION_RECOVERY`，必须把恢复后的伤势作为新基线。

### CONTINUITY_ENTRY
同时使用：
- World State Ledger / Delta
- Approved Previous Ending Frame
- Continuity Snapshot

---

## 16｜Continuity Priority配合

World State Diff按现有`continuity_priority.md`分级：

### P0
- 人物是否在场 / 去向
- 关键Prop holder/location/state
- 车辆/移动状态的核心因果
- 伤势/变身/剧情破损（含Transformation Recovery Eligibility / Result / Post-Recovery Injury State）
- Knowledge access
- 重要门/锁/环境机制
- 已确认剧情事实

### P1
- 轻微湿度范围
- 主要衣服开合/凌乱
- 环境破坏的大致程度
- Crowd Density等级 / Cluster大致区域 / 主流Flow / 已触发的注意力或撤离状态

### P2
- 单滴雨水
- 小衣褶
- 小灰尘
- 无剧情意义的细粒子位置

本引擎不允许P2细节把过渡变成高成本锁死。

---

## 17｜Decision Authority / Question Policy

以下默认`DERIVED`并自动决定：
- 是否用Visual / Residual / Implied Bridge；
- Arrival Shot景别与最小长度；
- 普通开门、下车、收起道具等连接动作；
- Bridge是否合入建立镜头；
- 如何用最少Shot解决状态落地。

只有以下情况才可能`ASK_REQUIRED`：
- 两个Authority对“人物究竟去了哪里 / 谁拿走关键道具 / 门是否锁死 / 时间是否足够 / 某人是否知道秘密”等P0 Story/Canon事实互相冲突；
- 任一自动解释都会创造新的不可逆剧情事实或世界机制。

---

## 18｜QC快速检查

每次Stage 02结束前问：

- 上一Scene还在移动，下一Scene是否让观众感到真正抵达？
- 人物有没有凭空进入/离开？
- 关键道具有没有凭空出现/消失/换手/变状态？
- 正在做的任务有没有CUT后无因归零？
- 衣服、湿度、污渍、伤势有没有换场刷新？Transformation Recovery若已合法触发，是否反而错误继承/恢复了旧伤？
- Environment Damage / Door / Light / Power有没有自动恢复？
- 谁知道什么是否有合法信息来源？
- 重大情绪/关系/目标有没有因为换Scene重置？
- 是否把可安全省略的操作拍成了流水账？
- 必要Bridge是否已经提前产生资产需求？
- `SCENE_OPENING`是否被错误理解成World Reset？

全部通过后，才进入正式Shot / Segment锁定与Episode Asset Manifest。

## V4.5.5｜Mundane Reality Continuity

World State除大伤势/剧情道具外，正式记录会影响普通现实可信度的最小状态：`Seat/Functional Position / Door-Window / Vehicle Motion / Wetness-Dirt-Damage / Ongoing Task / Entry-Exit`。

普通相邻Shot/连续时间内：
- 人物不能从前乘客位无因跳到后排；
- 物件不能无因换Holder/位置；
- 雨湿、污渍、破损、开关门、车辆行驶/停稳不能因新图Reset；
- 行为任务不能因CUT自动消失。

如果新视觉资产与这些状态冲突，先判`MUNDANE_CONTINUITY_FAIL`并回查Owner；不要把图片的新状态直接写回Canon。
