# Camera Motion Contract（摄影机运动契约）

> **用途：** 把Stage 02的导演运镜意图与Stage 04/05的物理执行分开，避免Storyboard临场发明Camera，或视频模型把Pan/Truck、Dolly/Zoom混淆。Entry Camera Geometry / Lens Family / Focus / Stabilization由`cinematography_grammar.md`拥有；本文件拥有Camera运动路径、速度，以及运动导致的合法Geometry Change与Landing Geometry。

## 1｜Stage 02 Camera Intent（导演层）

Stage 02先回答“为什么动”，再决定“怎么动”：

```text
Narrative Camera Intent：STATIC PRESSURE / SLOW APPROACH / SLOW WITHDRAWAL / SUBJECT FOLLOW / LATERAL REVEAL / REVEAL TRAVEL / COMBAT PURSUIT / IMPACT WITNESS / SUBJECTIVE INSTABILITY / OTHER
Why Camera Moves / Does Not Move：
Relation to Subject：靠近 / 远离 / 保持 / 侧向揭示 / 围绕
Required Landing Information：运镜结束必须得到什么新信息
Axis / Screen Direction Constraint：
Critical Read Protection：不能遮住什么
```

普通T1/T2若Camera不构成主要叙事变量，到这里即可。

T3/T4、Combat、Transformation Hero Reveal、复杂空间Reveal或运动存在明显歧义时，Stage 02继续建立初版Physical Contract。

## 2｜Physical Contract Fields（执行层）

```text
Camera Motion Type：STATIC / STATIC_BODY / PAN / TILT / DOLLY / TRUCK / CRANE / ARC / FOLLOW / COMPOUND / OTHER
Start Framing：
Pivot / Physical Path：
Axis / Horizon：
Focal Behavior：FOCAL_LENGTH_HOLD / ALLOW_ZOOM（仅明确需要；ALLOW_ZOOM默认指有意的焦距变化，不把数字裁切伪装成光学镜头运动）
Expected Parallax：YES / NO
Subject Relation：主体在画面中的相对变化
Geometry Change：NONE / HEIGHT / ANGLE / VIEW / COMBINATION
Landing Camera Geometry：<只有运动会改变Height / Angle / Subject View时填写>
Start Trigger：
Speed：
Motion Curve：CONSTANT / EASE_IN / EASE_OUT / EASE_IN_OUT / ACCELERATING / DECELERATING（按需）
Stop / Landing：
Forbidden Ambiguity：仅列本镜头最容易误解的1–3项
```

## 3｜Canonical Meanings

- **STATIC**：Camera position / orientation / focal length从首帧到尾帧全部不变；不漂移、不自动push-in；运动来自人物/场景。
- **STATIC_BODY**：Camera position / orientation固定，但允许`Focal Behavior=ALLOW_ZOOM`；仅在导演明确需要焦距变化时使用，不把它和Dolly混写。
- **PAN**：Camera位置不变，绕垂直轴水平旋转；不是Truck，不是Dolly，不是Zoom。
- **TILT**：Camera位置不变，绕水平轴上下旋转；不是Crane升降。
- **DOLLY IN / OUT**：Camera沿视线方向物理前后移动；焦距默认保持；应产生真实视差；不是Zoom。
- **TRUCK LEFT / RIGHT**：Camera整体水平平移；不是Pan。
- **CRANE / PEDESTAL**：Camera发生真实垂直位移；不是Tilt。
- **ARC**：Camera围绕主体按指定弧线移动；必须写方向/终点，禁止默认360°环绕。
- **FOLLOW**：Camera维持与主体的移动关系；具体物理方式可由Dolly/Gimbal/Shoulder等执行，不能只写“跟拍”让模型猜。
- **HANDHELD / SHOULDER / GIMBAL**属于`cinematography_grammar.md`的Stabilization / Support，不再与Pan/Dolly/Truck混成同级运动类型。

## 4｜Stage 04

Storyboard必须继承Stage 02 Cinematography Grammar + Camera Intent，并证明：
- Camera有足够物理空间完成运动；
- 不越轴或越轴有明确设计；
- 运镜不会遮挡Critical Visual Read / Contact / 表演关键点；
- 运镜开始与停止有叙事Trigger；
- 最终Landing Frame承担Stage 02要求的新信息。

Stage 04只允许精化Path / Motion Curve / Landing / Panel Anchor。若必须改变核心Camera Intent、Entry/Landing Camera Geometry、Lens Family、Focus Strategy、Stabilization、Axis或Blocking，标`DIRECTOR SHOT CONTRACT CONFLICT`，回Stage 02最小Patch。

## 5｜Stage 05

Prompt只编译当前镜头需要的字段，不输出模板解释。Camera是叙事/空间观察方式，不得替代动作物理与Impact。

当`Motion Priority != CAMERA`时，不得为了“电影感”额外添加复杂Camera。Camera Motion必须服从主体动作可读性。

## Current｜Unique Camera Timeline Owner
Stage 05运动状态只允许由`VIDEO_EXECUTION_STATE.CAMERA_TIMELINE`拥有。每个时间窗必须是唯一Motion/Path/Speed/Motion Curve/Focal Behavior/Geometry Change/Landing Camera Geometry/Landing Composition；Entry Height/View/Angle、Lens/DOF/Stabilization由`CINEMATOGRAPHY_STATE`拥有，动态焦点由`FOCUS_TIMELINE`拥有。PAN/TILT/CRANE/ARC等合法Geometry Change不得被误判成“Entry Geometry冲突”。禁止`静止或轻推 / pan或truck / 可轻微zoom`等OR分支进入Final Prompt。若来源冲突，先由`prompt_constraint_solver.md`裁决，不能让视频模型选择。
