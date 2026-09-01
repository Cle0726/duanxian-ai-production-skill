# Spatial Execution Translation（空间执行转译）｜Current Authority

> **目的：** 修复“导演内部有Blocking/FG-MG-BG，但Final Video Prompt把空间关系压没了”的问题。`VISUAL-FIRST ≠ SPATIAL-TEXT-OFF`。
>
> **核心分权：** `Reference owns static appearance/composition; text owns dynamic spatial execution.` 视觉Reference优先承担静态身份、环境几何、综合色、已批准构图；文字必须承担视频期间真正变化的**位置、朝向、相对关系、运动方向、目标与落点**。

## 1｜何时必须建立Spatial Execution State

以下任一成立时，Stage 02C / Stage 05必须建立`SPATIAL_EXECUTION_STATE`：
- ≥2个清楚可读主体需要保持左右/前后/距离/遮挡关系；
- 人物与Prop/门/床/桌/车辆/出口等发生接近、绕行、穿越、进入、退出或接触；
- FG/MG/BG交换、Crossing、Reveal、Occlusion承担叙事；
- 动作有明确空间目标或落点；
- Axis / Screen Direction / Eyeline要求依赖主体空间关系；
- Multi-shot Segment中CUT前后需要维持或有意重置屏幕方向。

单主体、无位移、Reference已清楚证明构图且空间变化不承担信息时，可以`SPATIAL_TEXT=N/A`，不得为形式完整重复整张图。

## 2｜空间字段

优先使用**区域 + 深度 + 相对关系 + 移动方向 + 落点**，不默认写像素坐标。

```text
SPATIAL_EXECUTION_STATE
SHOT_SCOPE：<SH01 / SH02...；单Shot可省略重复标签>
STABLE_ENV_ANCHORS：<仅列当前动作真正依赖的Door/Bed/Table/Exit等固定锚点>

SUBJECT_SPATIAL_STATE
- Subject：
- Start Horizontal Region：LEFT / CENTER / RIGHT / EDGE_LEFT / EDGE_RIGHT / N/A
- Start Depth：FG / MG / BG / N/A
- Start Orientation：FACING_LEFT / FACING_RIGHT / TOWARD_CAMERA / AWAY_CAMERA / TOWARD_<TARGET> / OTHER
- Start Relation：BESIDE / IN_FRONT_OF / BEHIND / BETWEEN / NEAR / FAR / BLOCKED_BY / N/A + Target
- Motion Vector / Path：LEFT_TO_RIGHT / RIGHT_TO_LEFT / FG_TO_BG / BG_TO_FG / DIAGONAL / APPROACH_<TARGET> / WITHDRAW_FROM_<TARGET> / CROSS / HOLD
- Motion Target：<Subject / Prop / Environment Anchor / N/A>
- End Horizontal Region：
- End Depth：
- End Relation：<必要时>
- Visibility / Occlusion Change：<只有叙事需要时>

PROP_SPATIAL_STATE
- Prop：
- Start Holder/Region/Depth：
- Release / Trajectory / Contact Target：
- End Region/Depth/Rest Target：
```

## 3｜Stage职责

### Stage 02B｜Director Spatial Design
`cinematic_spatial_staging_engine.md`决定戏剧空间、Blocking、Distance、FG/MG/BG、Axis/Eyeline。这里仍是导演Authority。

### Stage 02C｜Execution Translation
本方法把已锁的`Blocking Start→Change→End + Environment Geography + Shot Relation`转成最小`SPATIAL_EXECUTION_STATE`。**不得在此重新导演。**

### Stage 04｜Previs Proof
Hero/Keyframe/4格/6格/9格/Spatial Map/Camera Path只负责证明必要空间Anchor、路径与Landing。若实际Approved Geography证明原路径不成立，返回Director Spatial Reconciliation；不得在Stage 04偷偷换左右/入口/落点。

### Stage 05｜Prompt Compile
- Reference已证明的静态房间结构、人物外观、t=0普通构图不长篇复述；
- **动态空间变化必须进入Integrated Timeline或紧邻动作句**；
- 两人以上时优先用稳定主体标签，不用含糊“他们”；
- 只写真正影响执行的`LEFT/CENTER/RIGHT + FG/MG/BG + RELATION + MOTION + END`；
- CUT进入新Shot时按该Shot重新声明必要空间状态，不把上一个Shot的屏幕左右机械继承到新机位。

模型侧示例结构（不是固定文案）：
`护士位于画面左侧中景，婴儿床在右侧中景；护士保持3/4背影向右靠近，最终停在床左侧。婴儿始终留在右侧中景可读位置。`

## 4｜空间唯一Owner

- 人物/Prop动态位置、相对关系、运动路径与落点：`SPATIAL_EXECUTION_STATE`唯一Owner；
- Camera自身位置/角度/运动：`CINEMATOGRAPHY_STATE / CAMERA_TIMELINE`；
- 环境固定几何：Approved Environment Geography / Reference Authority；
- `ACTION_TIMELINE`拥有“做什么”，但涉及“从哪里到哪里/朝谁/落在哪里”时必须引用Spatial State，不得另写第二套方向。

## 5｜Hard Conflict

以下未解决不得编译Final Prompt：
- `SPATIAL_POSITION_CONFLICT`：同一主体同一时段被要求位于互斥区域/深度；
- `SPATIAL_TRAJECTORY_CONFLICT`：Start→Motion→End不相容，或同一主体同时间向互斥方向移动；
- `SPATIAL_RELATION_CONFLICT`：同一主体对同一Target同时要求互斥关系（如`IN_FRONT_OF`与`BEHIND`）；
- `SPATIAL_TARGET_GEOGRAPHY_CONFLICT`：运动目标与Approved Geography/Anchor方向不相容；
- `SPATIAL_SCOPE_CONFLICT`：World位置、Frame Region、Off-screen状态被混成同一字段；
- `SPATIAL_OWNER_CONFLICT`：Blocking/Action/Camera模块各自写出第二套主体位置。

**禁止用“后一句覆盖前一句”修空间冲突。** 先回唯一Spatial State裁决，再重新编译。

## 6｜Blind执行

DeepSeek如果需要知道某人物/门/床/Prop在实际Reference的左/右/前/后，而文字Registry不足以唯一确认：
`VISUAL SPATIAL FACT REQUIRED → External Visual Handoff → WAIT FOR EVIDENCE`。

不得因为文件名、资产ID或旧Prompt曾写“门在右侧”就自称看到了真实位置。已验证且当前版本未变的Spatial Evidence可复用，不必每个Shot重复验图。
