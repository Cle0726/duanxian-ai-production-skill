# Crowd Presence & Ambient Life Engine（群体存在感与环境生命引擎）

> **用途：** 处理咖啡馆、街道、车站、宴会厅、剧院大厅、市场、候车区、观众席、群众撤离、围观人群等“背景中存在多名非主叙事人物”的镜头。
>
> 本引擎解决的不是单个第三人的Active Listening，而是：**让群体在时间里持续存在、各自有生活任务、反应不同步，同时始终服从前景叙事焦点。**
>
> 本引擎属于Stage 02 / 04 / 05的控制层，**不是Stage 07，也不是新的角色资产系统。** Character资产规则保持不变。

---

## 1｜核心问题定义

AI视频常见错误：
- 两个前景角色开始对白后，背景所有人突然像截图一样冻结；
- 背景人群全部做同一个循环动作；
- 主角说一句话，所有背景人物同时转头；
- 群体为了“显得活着”持续高频晃动，抢走主角注意力；
- 某个本来在行走的人进入对白段后无因停成静态Pose；
- 人群密度、移动方向、聚集区域在CUT后随机重置；
- 背景人物突然全部消失或突然增殖；
- 远景群众被错误要求保持每个人精确脸部/身份/微表演，浪费模型容量并污染主角稳定性。

本引擎的基本原则：

> **Crowd is not a still background plate. Crowd is not one giant Actor either.**
>
> 群体不是静态背景板，也不是一个统一反应的大角色。

---

## 2｜Authority边界

### 2.1 Actor vs Crowd

- **Narrative Actor（剧情人物）**：使用`actor_performance_engine.md`，有Objective / Tactic / Listening / Relationship等完整演员逻辑。
- **Featured Background Actor（可识别背景个体）**：当某个背景人物会被清楚看见、重复出现、承担明确任务或稍后进入剧情时，可使用轻量Actor逻辑：`Ongoing Task + Attention State + Trigger + Exit`。
- **Crowd Cluster（群体小簇）**：不逐人导演；按区域/功能组织为2–5个Cluster，使用活动、密度、注意力和运动节奏控制。
- **Deep Background Mass（深背景人群）**：只控制密度、流向、速度差、空间深度与不完全同步，不要求逐人身份连续。

### 2.2 Narrative Importance ≠ Crowd Attention

观众知道主角重要，不代表场景里的群众知道。

除非群众真实感知到足够强的Stimulus，否则：
- 主角低声秘密对白不会让整间咖啡馆都看向他们；
- 主角情绪变化不会自动广播给后方路人；
- 前景人物的叙事权重不能被编译成背景集体注意力。

### 2.3 Environment Master ≠ Crowd Time Behavior

Environment Master可以定义空间与初始人群氛围，但**静态场景图/Storyboard只定义“人在哪里”，不拥有“这些人在时间里怎么活着”的Authority。**

Crowd时间行为由本引擎 + World State Runtime控制。

---

## 3｜Crowd Tier Classification（群体层级分类）

每个含群体的Scene / Shot先分类：

### Tier A｜Narrative Actors
- 当前剧情主角/配角；
- 完整Actor Performance；
- 身份、服装、道具、连续性严格。

### Tier B｜Featured Background Actors
适用于：
- 会被清楚识别；
- 会与前景人物产生短暂交互；
- 持续承担可见现实任务；
- 后续会再次出现。

只需建立：
- Role / Zone；
- Ongoing Task；
- Attention State；
- Trigger Response；
- Exit State。

不因“背景有很多人”给每个人建立完整Character Master。

### Tier C｜Crowd Clusters
按空间/活动拆成Cluster，例如：
- 靠窗两桌：低声交谈；
- 柜台区：点单、接杯、整理；
- 入口区：进出、脱外套、找座位；
- 站台边：候车、少量行走；
- 远处通道：双向缓慢流动。

每个Cluster最多保留当前镜头真正需要的几个字段，不逐人列动作。

### Tier D｜Deep Background Mass
只保留：
- Density；
- Flow Direction；
- Speed Variation；
- General Activity；
- Spatial Depth；
- Reaction Level。

远景/虚化背景不要求精确脸部、手指或每人身份。

---

## 4｜Crowd Runtime State（群体运行时状态）

World State中的Crowd State升级为：

```text
Crowd Runtime State
- Approx Population / Density：
- Zones / Cluster IDs：
- Primary Flow(s)：
- Speed Range：
- Stationary Activity Zones：
- Entry / Exit Sources：
- Attention Distribution：
- Current Stimulus：NONE / LOCAL / SCENE-WIDE
- Reaction Propagation State：
- Persistent Crowd Change：
```

### Density只要求叙事级连续

Crowd不是逐帧人口统计系统。默认按：
- LOW
- MEDIUM
- HIGH
- PACKED

或大致人数区间记录。

不要因为P2级单个路人增减触发返工；但明显“半满大厅突然空无一人”属于P0/P1连续性错误。

---

## 5｜Crowd Motion Field（群体运动场）

含群体的中/大全景，按Zone定义运动场，而不是逐人动作清单。

模板：

```text
CROWD MOTION FIELD
Zone A：
- Density：
- Primary Flow：
- Speed：
- Activity：
- Attention：

Zone B：
...
```

示例：

```text
Zone A｜站台边缘
Density：MEDIUM
Primary Flow：LEFT → RIGHT，少量逆向
Speed：SLOW–MEDIUM
Activity：候车 + 零星行走
Attention：主要关注列车/同行者，不关注前景对白

Zone B｜长椅
Density：LOW
Primary Flow：NONE
Activity：坐着、阅读、整理行李
Attention：LOCAL
```

### Motion Field原则
- 人群运动允许不同速度；
- 允许局部静止区；
- 不要求所有人持续移动；
- 不允许整片背景因为前景对白自动暂停；
- CUT后若仍为同一时间/空间，主流Flow与Density默认延续。

---

## 6｜Ambient Motion Contract（环境生命运动契约）

每个含群体的Video Segment，在Stage 04/05建立**最小环境生命契约**。

它回答：

> 在整个Segment期间，哪些低强度背景活动必须继续，才能避免“截图感”？

### 6.1 Contract不是动作清单

通常只保留2–4条：
- 一组坐客继续低强度交谈与自然姿态变化；
- 柜台人员持续当前工作任务；
- 一两名远处行人以不同速度经过；
- 深背景保持轻微、不规则空间流动。

### 6.2 Life ≠ Constant Motion

“活着”不等于每个人不断晃动。

合法稳定状态：
- 坐着阅读；
- 靠墙等待；
- 看菜单；
- 低声交谈；
- 看向站台；
- 长时间保持同一姿态。

只要其任务和注意力连续，就不算冻结。

### 6.3 Freeze定义

以下更接近真实`CROWD_FREEZE`：
- 正在行走的人无Trigger突然固定数秒；
- 整个Cluster在前景对白开始时同时停止所有原任务；
- 背景全部变成完全静态照片，没有任何时间变化；
- 前后帧群体姿态完全锁死且不符合当前活动。

---

## 7｜Attention Distribution（注意力分布）

含群体Scene建立简短Crowd Attention Map：

```text
Crowd Attention Map
Cluster A：SELF / COMPANION / TASK / ENVIRONMENT / FOREGROUND PARTIAL / FOREGROUND DIRECT
Cluster B：...
```

默认优先：
- SELF / COMPANION / TASK / ENVIRONMENT；
- 只有Stimulus真正可感知时升级关注前景。

### 不允许的默认行为
- 所有人因主角开口同时看向主角；
- 所有人因主角表情变化同步反应；
- 背景Actor为了证明“在听”不断点头/眨眼；
- 远处群众无因知道前景低声对白内容。

---

## 8｜Reaction Propagation（群体反应传播）

当存在足以影响群众的Stimulus，例如：
- 巨响；
- 爆炸；
- 玻璃碎裂；
- 武器显现；
- 有人突然倒地；
- 警报；
- 明显超自然现象；

禁止编译成“所有人同时转头/尖叫/逃跑”。

先运行：

`Stimulus Reach → Local Perception → Near-field Reaction → Social Propagation → Uneven Response → New Crowd State`

### 8.1 距离/可见性差异

Near Field：
- 最先感知；
- 反应更快、更明确。

Mid Field：
- 稍后因声音/视觉或看到近处人反应而注意。

Far Field：
- 可能延迟、部分无反应、继续原任务。

### 8.2 时间错开

根据镜头时长，用自然的几十毫秒到数秒级错开：
- 第一批先停顿/转头；
- 第二批随后看过去；
- 外围有人继续走、有人迟疑、有人离开。

不要求精确写每个人时间码；只要明确**反应是分层、非同步传播**。

---

## 9｜Motion Desynchronization（动作去同步）

为了防止“复制NPC”，群体动作必须遵守：

- 不同Cluster使用不同主任务；
- 同Cluster内允许相似活动，但Start Time / Speed / Amplitude不完全一致；
- 不让所有人同时喝杯子、转头、走一步、抬手；
- 不用统一循环动作填充整段；
- 若镜头时长较长，至少一个背景活动发生自然阶段变化，例如“行人经过后离开画面 / 柜台完成一次递杯 / 一桌人姿态轻微变化”。

### Anti-Clone原则

不要求远景每个人有独特身份设计，但应避免明显的：
- 同脸复制；
- 同服装复制；
- 同Pose复制；
- 等距排列；
- 同步循环。

这是Render/QC层的多样性要求，不等于必须给每个路人建立正式资产。

---

## 10｜Foreground Priority（前景叙事优先）

Crowd生命感必须服从主镜头。

### 强度限制
- Dialogue / Performance CU-MCU：背景运动低强度，避免大幅穿越主体脸部；
- MS：允许可读的Cluster活动，但不能与主角同级表演；
- WS：可以更清楚呈现Cluster和流动；
- EWS：主要控制Density / Flow / Spatial Rhythm，不导演微表情。

### Background Activity Budget

同一镜头内背景可见动作信息应少于前景主动作信息。

如果背景活动开始抢戏：
1. 降低Amplitude；
2. 降低Reaction Level；
3. 把个体动作合并为Cluster状态；
4. 深背景改为轻微不规则流动。

---

## 11｜Shot-scale Crowd Translation（景别转译）

### ECU / CU
- 背景严重虚化时，只要求微弱、异步的人体/光影/空间活动；
- 不要求明确群众面部或手部动作；
- 不让背景人物大幅横穿主体头部，除非镜头设计明确需要。

### MCU / MS
- 1–3个Cluster活动足够；
- 可有Featured Background Actor持续现实任务；
- 明确主角对话期间背景继续原任务。

### WS
- 建立Cluster / Zone / Flow；
- 注意入口/出口和主流方向；
- 避免整齐同步。

### EWS
- 以Density、流向、速度差、局部停留、空间深度为主；
- 不耗费Prompt预算描述远处单个人的微动作。

---

## 12｜Stage 02 Director Breakdown使用方式

只要Scene明显存在群体背景，Stage 02补：

```text
Crowd Presence Brief
- Crowd Tier Mix：A / B / C / D
- Approx Density：
- Crowd Zones / Cluster Functions：
- Primary Flow(s)：
- Stationary Activity Zones：
- Crowd Attention Baseline：
- Potential Crowd-wide Stimulus：NONE / ...
- Reaction Propagation Need：NO / YES
- Featured Background Actors：NONE / ...
- Continuity Carryover：
```

Stage 02不逐人写背景动作，也不为一次性群众建立完整角色资产。

---

## 13｜Stage 04 Storyboard使用方式

Storyboard必须同时区分：

### Spatial Blocking
- 群体/Cluster在哪里；
- 哪些区域允许运动；
- 是否会遮挡前景行动线；
- 入口/出口及主流方向。

### Crowd Motion Intent
Storyboard是静态图，因此必须附文字说明时间行为：

```text
Crowd Motion Intent
- Cluster A：CONTINUE low-intensity conversation
- Cluster B：staff continues service task
- Cluster C：1–2 pedestrians cross asynchronously
- Crowd Attention：mostly TASK/COMPANION, not foreground
- Reaction：NONE / LOCAL / PROPAGATING
```

**Storyboard Panel中的静态群众姿势不能被解释成“视频里保持静止”。**

### Storyboard Crowd Gate

进入Stage 05前确认：
- 主前景表演清楚；
- Crowd Blocking不会挡住主动作；
- 有最小Ambient Motion Contract；
- Attention逻辑合理；
- 强Stimulus时Reaction Propagation已规划；
- 没有要求所有群众同级反应。

---

## 14｜Stage 05 Prompt Compilation

内部完整运行本引擎，但**模型侧不再建立独立 `Crowd / Ambient Life`区块**。所有群体时间行为必须由`prompt_semantic_deduplication_engine.md`编译进对应Shot的`Integrated Shot Timeline`，在真正发生的时间点写一次。

通常只保留2–4条当前镜头真正需要的背景生命事实，例如：
- 前景对白期间，靠窗两桌继续低强度、不同步交谈；
- 柜台员工持续当前整理/递取任务；
- 远端通道只有零星行人以不同速度经过；
- 若发生强刺激，近场少数人先反应，中场随后传播，外围部分人继续原任务。

编译限制：
- 不输出独立Crowd摘要复述Timeline；
- 不把Cluster分析表全部塞给模型；
- 不逐人编号几十个路人；
- 不用“everyone keeps moving”这类高风险模糊命令；
- 优先正向描述持续任务和不同步行为，不堆“No freeze / no clone / no sync”禁令。

---

## 15｜Crowd Hard Gate（群体生命硬闸门）

当镜头中存在明显Crowd/Extras时，Stage 05编译前检查：

- [ ] 已识别Narrative Actor / Featured Background / Crowd Cluster / Deep Background Mass；
- [ ] Crowd Runtime State有Density / Zone / Flow等最小连续信息；
- [ ] 至少有一个可持续的Ambient Motion Contract，或当前群体静止有明确剧情原因；
- [ ] 背景注意力没有因主角叙事重要性自动锁向主角；
- [ ] 强Stimulus的群体反应采用Propagation而不是同步广播；
- [ ] Crowd活动强度低于当前Foreground Narrative Priority；
- [ ] Storyboard静态群体没有被错误当成Video时间行为Authority；
- [ ] CUT/Scene边界没有无因重置群体密度、Zone、主流Flow或已发生的撤离/聚集状态。

存在未解决问题时：

`CROWD_PRESENCE_FAIL`

返回Stage 04或重编Crowd模块；**不得靠多Take碰运气。**

---

## 16｜QC Failure Codes

### CROWD_FREEZE
背景群体在时间中无因整片静止，像截图。

### CROWD_SYNC
多人出现明显同步转头、同步点头、同步喝水、同步起步等机械动作。

### CROWD_ATTENTION_HIJACK
群众无因全部关注前景，或背景表演强度抢走主角焦点。

### CROWD_FLOW_RESET
CUT / Segment后Density / Flow / Cluster位置无因重置。

### CROWD_REACTION_PREMATURE
Stimulus尚未发生或尚不可感知时群众提前反应。

### CROWD_REACTION_BROADCAST
本应局部传播的刺激被所有群众同时接收并同步反应。

### CROWD_CLONE_ARTIFACT
明显同脸、同服装、同Pose、等距复制或统一循环导致人工复制感。

### CROWD_OVERDIRECTED
为了避免冻结，给背景塞入过多高频动作，导致抢戏或模型失稳。

---

## 17｜Failure Diagnosis与Minimum Necessary Change

Crowd问题优先局部修正：

### 如果是冻结
补：
- 2–3条低强度持续任务；
- 一个远处异步移动；
- 必要的时间阶段变化。

不要整段重写主角Performance。

### 如果是同步
补：
- Cluster分组；
- 不同Start/Speed；
- Reaction Propagation；
- 删除“所有人一起”式语言。

### 如果背景抢戏
降低：
- Background amplitude；
- Attention to foreground；
- Featured extras数量；
- 可见动作种类。

### 如果Flow重置
修World State / Crowd Runtime State，不靠Video Prompt单独猜。

---

## 18｜Crowd Continuity Priority

### P0
- 剧情要求的撤离/聚集/封锁状态；
- 群体是否仍存在；
- 重大危险下的人群整体方向；
- 群体是否阻塞/开放关键行动路径。

### P1
- Density等级；
- Cluster大致区域；
- 主流Flow方向；
- 已经触发的注意力/恐慌/撤离状态。

### P2
- 某个无剧情意义路人的精确脸；
- 单个人是否在上一镜头第3排还是第4排；
- 小幅随机姿态差异。

P2不作为跨镜头硬锁，避免把群众做成高成本角色资产工程。

---

## 19｜与Reference / Render Quality的关系

- Crowd不因Storyboard低清而继承“静态截图感”；
- Crowd不是通过上传几十张路人参考图解决；
- 除Featured Background Actor确有必要外，不为一次性Crowd占用大量Reference Slots；
- 人群整体服装时代、色彩分布、密度与活动类型可由Environment / Project Style / Wardrobe时代规则 + Crowd Profile共同控制；
- 主角Character Master始终优先保证身份稳定。

---

## 20｜Runtime Capsule最小字段

正常重复生产只保留：

```text
Crowd Runtime Capsule
- Tier Mix：
- Density：
- Zones / Clusters：
- Primary Flow：
- Ambient Motion Contract：
- Attention Baseline：
- Current Stimulus / Propagation State：
- Foreground Priority：
- Carryover Delta：
```

复杂群体异常、规则变化或QC失败时回读完整本文件。

---

## 21｜Decision Authority

默认自动决定：
- Cluster怎么分；
- 哪些背景任务最自然；
- 哪一批人先反应；
- 背景动作强度；
- CU/MS/WS/EWS下需要多少群体细节。

只有当群众行为会改变Story Canon，例如：
- 群众是否已经知道关键秘密；
- 是否发生大规模伤亡；
- 是否必须形成暴动/撤离/围捕；
- 某个背景人物是否实际是重要剧情角色；

且现有Authority无法判断时，才升级ASK_REQUIRED。

---

## 22｜最简原则

> **Foreground actors perform the story. Background crowds continue the world.**
>
> 前景人物负责演剧情；背景群体负责让世界持续运转。

生产目标不是让每个背景人都“有动作”，而是让观众感觉：

> **即使镜头没有在拍他们，他们的生活也没有被暂停。**

## Current｜World Occupancy ≠ Frame-visible Occupancy
群体数量必须区分`WORLD_POPULATION`与`FRAME_VISIBLE_POPULATION`。剧情可规定“车厢实际有二十多人”，但当前Wide/Low-angle构图可以只清楚看见若干侧面/背影；不能把世界人数自动翻译成必须全部入画。两者混用标`SCOPE_CONFLICT`。
