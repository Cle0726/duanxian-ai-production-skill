# Continuity Priority（连续性优先级）

> **用途：** 把“必须连续”和“没必要为了它返工”的细节分开，避免一人制片为了无剧情价值的小差异反复重生。

## 核心原则

连续性不是“每一个像素都一样”。QC和Failure Diagnosis应先判断问题属于哪一级，再决定是否返工。

当Locked Editorial Plan允许真实切镜时，默认采用`STORYBOARD_BLOCKING_APPROXIMATE`：Approved Storyboard结尾与下一镜入口只需在人物集合、世界Zone/Anchor、Screen Side或动作方向、深度、朝向、动作Phase、关键接触、道具Holder与数量这些P0字段上合理。微姿态、衣褶、粒子、像素纹理、压缩噪声和非剧情性综合色不跨Cut强锁；过渡由动作匹配、反应切、空间重定向、声桥、J-cut/L-cut或形状/方向匹配承担。

## P0｜Must Match（必须一致）

出现明显错误时通常需要修正：

- 人物身份、年龄感、当前剧情阶段主要造型；
- 人物左右位置、朝向、关键视线与摄影轴线；
- 当前动作状态与上一段必须承接的重心/接触关系；
- 关键道具是否存在、由谁持有、结构和剧情状态；
- 场景主要空间几何、门窗/舞台/座位等当前镜头依赖的固定结构；
- 已发生的剧情状态不能无因倒退，例如伤口/破损/开合状态若必须持续；**但完整Transformation Completion触发的`TRANSFORMATION_RECOVERY`属于有因状态转变，恢复后的伤口状态本身成为新的P0连续性基线。**
- CUT前后必须维持的因果和空间关系。
- 人物是否在场、进入/离开的来源，以及大跨度位置变化是否有合法过渡；
- 车辆/人物从“移动中→抵达后”的核心状态是否有可读Arrival；
- 关键Knowledge State：角色不得凭空知道未接收的信息；
- Environment Runtime State中的剧情性门/锁/停电/破坏/火烟水等不得无因复原；
- SCENE_OPENING不得清空伤势、湿度、Prop去向、Knowledge、关系/Objective等已发生状态；若伤势已经被Transformation Recovery合法修复，则同样不得在Scene Opening把旧伤重新恢复。

## P1｜Should Match（尽量一致）

明显跳变时应检查，但不自动等于整段重做：

- 发型大轮廓和主要发束方向；
- 主光方向、综合色和主要明暗关系；
- 主要衣料垂坠、围巾/外套的大状态；
- 背景主要材质和大型固定物体的视觉一致；
- 不影响剧情的次级姿态差异。

先判断是否观众实际能察觉、是否影响镜头连接，再决定返工。

## P2｜May Vary（允许自然变化）

默认不能仅凭这些差异要求重生：

- 单根头发位置；
- 微小衣褶；
- 雨滴/灰尘/烟雾具体粒子位置；
- 无剧情作用的小反光；
- 背景很小的污渍、纹理噪声；
- 不影响人物身份与结构的极轻微绘画随机差异。

## Story Override（剧情提升优先级）

某个平时属于P1/P2的细节，如果本Scene明确把它当剧情信息，就自动提升到P0。

例如：
- “围巾突然不见”是剧情线索 → 围巾状态P0；
- 某一滴血是关键Reveal → 该血迹位置可提升；
- 普通雨滴不是剧情信息 → 仍为P2。

## QC使用规则

发现连续性差异时先输出：

```text
Continuity Issue：围巾褶皱略不同
Priority：P2
Decision：不返工，继续生产
```

或：

```text
Continuity Issue：关键道具从Character A右手消失
Priority：P0
Decision：必须修正
```

## 与Failure Diagnosis / Retry关系

- P0错误：进入Failure Diagnosis，决定最小回退；
- P1错误：先检查是否影响观看/剪辑，再决定是否局部修；
- P2差异：默认忽略，不触发Retry / Regeneration；
- 不允许把P2差异通过不断增加负面词“锁死”，导致Prompt越来越重。


## Current｜Approved Salvage Clip Continuity
`SALVAGE_CANDIDATE`不具备连续性Authority。只有当某片段已经：
1. 被最终剪辑采用并升级`APPROVED_SALVAGE_CLIP`；
2. 真实成为当前Segment最终视觉结束；
3. 其Trim-out真实时间点通过Ending Frame QC；
才允许从该真实Source Take末帧建立Previous Ending Frame。

因此“源Take整体REVISE”并不永久禁止其中片段进入连续性链，但必须先经过片段批准与最终剪辑位置确认。
