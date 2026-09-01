# Creature Performance Engine｜怪物/非人威胁表演引擎｜Current Authority

> **用途：** 防止怪物只作为“漂亮模型站在那里”。本引擎负责非人威胁的行为语言、重量、感知、捕猎式停顿、逼近、攻击准备、恢复与环境耦合。它不创造新的怪物能力；能力边界仍来自Story/World Canon。

## 0｜最高原则

`CREATURE ≠ STATIC PROP`

只要实体处于`ACTIVE_THREAT`，即使没有攻击，它也必须通过身体、感知、目标跟踪、重量、声音或有意静止持续施加威胁。

无理由“站着不动等主角来”判：`CREATURE_STATIC_PROP_FAIL`。

## 1｜Creature Performance Contract

每个清楚可见且承担Threat Function的怪物/非人实体，根据适用性锁：

```text
Threat Behavior Thesis
Perception Method
Locomotion Signature
Weight / Inertia
Body Coordination
Idle Threat Motion
Target Tracking
Approach Pattern
Pause Pattern
Attack Preparation
Commitment Motion
Recovery Behavior
Environment Coupling
Sound Coupling
Predatory Stillness Rule
```

这些字段描述行为规律，不规定每一秒固定动作。

## 2｜Predatory Stillness｜有意静止

怪物可以完全静止，但必须属于明确原因，例如：

- 等待猎物进入范围；
- 通过非视觉感知定位；
- 假装失活；
- 蓄力/压缩身体；
- 封堵出口；
- 让角色主动接近错误安全区。

此时登记：

`stillness.mode = PREDATORY_STILLNESS`

并说明：`reason + pressure_effect + exit_trigger`。

静止本身必须让威胁更强，而不是模型冻结。

## 3｜Creature Kinetic Read

高价值Threat至少要能读到：

- 身体哪一部分先感知/先启动；
- 重量如何传地/传墙/传水/传家具；
- 头/躯干/肢体是否有非人但一致的Coordination；
- Approach是否匀速、停顿、侧移、爬行、贴壁、拖行或突然加速；
- 攻击准备和真正Commitment之间有什么可读差异；
- 失败/命中后的Recovery是否延续其生物/机械逻辑。

禁止把“诡异”直接等同于随机抽搐、随机头部旋转、随机高速抖动。

## 4｜Environment Coupling

怪物必须根据体量和材质影响世界：

- Weight / Footfall / Surface Deflection；
- Door / Wall / Dust / Water / Loose Object Response；
- Light / Shadow Occlusion；
- Narrow-space Compression；
- 声音传播与距离感。

巨大Threat若没有Human / Environment Scale Anchor而又需要观众理解尺度，标`CREATURE_SCALE_READ_GAP`。

## 5｜Reference Pose Bias

Character/Creature Canon Master负责身份与结构，不自动拥有当前动作Pose。

若Canon Master是中性直立展示，而当前Shot要求：

- 爬行 / 贴墙；
- 极端前倾；
- 四肢重构后的低姿态；
- 高速冲刺；
- 捕猎式弓身；
- 大幅攻击准备；

必须评估`pose_bias_risk`。

`HIGH`时至少需要：

- `SHOT_EXECUTION_FRAME`，或
- `CREATURE_ACTION_ANCHOR` / `LOCOMOTION_ANCHOR` / `ATTACK_PREP_ANCHOR`

作为动作Primary；Canon Master退为Identity/Structure Support。

否则：`STATIC_CANON_POSE_CONFLICT`。

## 6｜Behavior Anchor不是固定资产套餐

按真实Shot需要选：

- `LOCOMOTION_ANCHOR`
- `THREAT_POSE_ANCHOR`
- `ATTACK_PREP_ANCHOR`
- `SCALE_ENVIRONMENT_ANCHOR`

没有对应风险就不生成。目标是解除Pose Prison，不是为每个怪物机械做动作图集。

## 7｜Threat Coverage Binding

Major/Hero Creature必须能绑定到`EXPERIENCE_PRESSURE_PLAN`中的至少一个Threat Role。首次重要Reveal通常应覆盖：

`Pre-Reveal Pressure → Creature Read → Encroachment/Scale → Commitment/Consequence`

具体顺序由导演决定，不套固定套路。

## 8｜Stage 04 / 05

Storyboard要证明怪物不只是一个静态轮廓：至少在必要Panel中表达感知方向、重心/体态、位移意图、威胁距离或有意Stillness。

Final Video Prompt必须把当前Video Unit真正需要的Creature行为编译成可见动作：

- 感知/锁定；
- 当前Body Coordination；
- Approach/Pause；
- Weight / Environment Response；
- Attack Prep / Commitment（适用时）；
- Landing / Recovery。

禁止仅写：`怪物缓慢靠近，十分恐怖。`

## 9｜Hard Fail

- `CREATURE_STATIC_PROP_FAIL`
- `CREATURE_PERFORMANCE_FIELD_GAP`
- `CREATURE_PREDATORY_STILLNESS_JUSTIFICATION_GAP`
- `CREATURE_SCALE_READ_GAP`
- `STATIC_CANON_POSE_CONFLICT`
- `CREATURE_THREAT_COVERAGE_BINDING_GAP`

> **最终原则：** 怪物的恐怖首先来自“它一直在做什么、如何感知、如何占据空间、如何改变环境”，不是来自给一张怪物母图加暗光和红色滤镜。
