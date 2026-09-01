# Cinematography Grammar（摄影语言语法）｜Current Authority

> **用途：** 补齐Detailed Shot Contract里真正会改变观众观看方式的摄影字段，同时避免把Skill再次扩成“每镜头填满摄影教材”。只有会改变叙事、空间可读性、表演访问或Video执行稳定性的字段才填写。
>
> **核心：** `Shot Function → Camera Position/View → Lens Family → Focus Plan → Motion/Stabilization → Landing → Shot Relation`。Stage 02锁意图；Stage 04证明；Stage 05只编译当前镜头真正需要的执行字段。

## 1｜字段与唯一Owner

### 1.1 Entry Camera Geometry / View
- `Entry Camera Height`：GROUND / LOW / WAIST-CHEST / EYE / HIGH / OVERHEAD。
- `Entry Vertical Angle`：LEVEL / UPWARD / DOWNWARD / TOP-DOWN。
- `Entry Subject View`：FRONTAL / FRONT_3_4 / PROFILE / REAR_3_4 / BACK / OTS / POV / OTHER。

**Camera Height是相对当前主要主体/动作平面的摄影机位置，Vertical Angle是镜头朝向，不得混写。** 例如“LOW + LEVEL”和“EYE + DOWNWARD”不是同一镜头；`OVERHEAD`也不自动等于`TOP-DOWN`。这里记录的是镜头进入时的Camera Geometry；若PAN / TILT / CRANE / ARC / FOLLOW等运动会合法改变Angle / Height / Subject View，变化过程与`Landing Camera Geometry`由`CAMERA_TIMELINE`拥有，不能把Entry值误当成全段冻结值。

### 1.2 Lens Family
只写叙事需要的透视关系，不默认追求毫米数：
- `WIDE_PERSPECTIVE`：空间与前后距离被强调，近处形体透视更明显；
- `NORMAL`：自然空间关系；
- `PORTRAIT_COMPRESSION`：轻度压缩背景与主体关系，减少近距离透视夸张；
- `LONG_LENS_OBSERVATION`：明显压缩空间、远距离观察/隔离；
- `MACRO_DETAIL`：只有真正Insert/微小物件可读性需要时使用。

毫米数只能作为目标模型/平台明确支持时的**可选执行映射**，不能反过来替代`Lens Family + Shot Function`。

### 1.3 Focus Plan
`Focus Owner`仍属于Visual Hierarchy；摄影层只决定它如何被光学访问：

```text
Focus Plane：FG / MG / BG / SUBJECT_SPECIFIC
Depth of Field：DEEP / MODERATE / SELECTIVE / SHALLOW
Focus Behavior：HOLD / RACK / TRANSFER
Focus Trigger：<仅RACK/TRANSFER需要>
Focus Landing：<焦点最终落在哪里>
```

规则：
- `RACK / TRANSFER`必须有两个可辨识深度目标和叙事Trigger；不能为了“电影感”随机拉焦；
- Critical Visual Read若需要同时看清两个平面，不能同时要求极浅景深；
- 静态Storyboard无法证明连续拉焦速度时，只证明Start/End Focus State，动态曲线留给Video执行。

### 1.4 Stabilization / Support
- `LOCKED_OFF`：机位、朝向均锁死；与任何实际Camera平移/旋转运动互斥；
- `TRIPOD_HEAD`：位置固定，可Pan/Tilt；
- `DOLLY_RAIL / CRANE / VEHICLE_MOUNT`：由真实平台/场景需要时填写；
- `GIMBAL_STABILIZED`：移动但画面稳定；
- `SHOULDER / HANDHELD`：允许有因微扰，必须服务主观/冲击，不等于随机抖动。

`HANDHELD`是支撑/稳定方式，不再作为Pan/Dolly/Truck同级的“运动类型”。

### 1.5 Motion Curve
只有Camera真的移动且速度变化影响可读性时填写：
`CONSTANT / EASE_IN / EASE_OUT / EASE_IN_OUT / ACCELERATING / DECELERATING`。

默认简单慢推/跟随优先`CONSTANT`；禁止只写“缓缓推进”而让模型自行加速。

## 2｜Shot Relation Grammar（相邻镜头关系）

> **Editorial Boundary：** 本节只描述摄影镜头之间的视觉连接语义。Sequence级“为什么此刻切、切点落在动作/视线/声音哪里、用什么Transition、视角如何转移”由`editorial_grammar_engine.md`唯一拥有。


`Cut Motivation`回答“为什么切”；`Shot Relation`回答“前后两个镜头如何连接”。只在真实CUT存在时填写最直接的一种或少数必要关系：
- `ESTABLISH_TO_DETAIL / DETAIL_TO_REVEAL`
- `ACTION_TO_CONSEQUENCE / CAUSE_TO_EFFECT`
- `GAZE_TO_OBJECT / EYELINE_MATCH`
- `MATCH_ON_ACTION / MATCH_ON_SHAPE`
- `WITHHOLD_TO_REVEAL`
- `WIDE_INSERT_RETURN`
- `SOUND_LED_REVEAL`
- `SPATIAL_REORIENTATION`

没有CUT时写`CONTINUOUS_HOLD`，不得为了“镜头语言丰富”虚构Shot Relation。

## 3｜Shot Size不是审美标签

景别必须服务当前Read Function：
- `SPATIAL READ`：需要读空间/多人关系时优先Wide体系；
- `RELATIONSHIP READ`：需要读两人距离/权力时优先Two-shot / Medium体系；
- `PERFORMANCE READ`：需要读表情/细微行为时才进入MCU/CU；
- `DETAIL EVIDENCE`：微小道具/伤势/接触点需要Insert/ECU。

**Close-up不是情绪自动奖励；Wide也不是默认安全镜头。** Shot Size必须与`Critical Visual Read / Performance Access / Shot Proof Capacity`一致。

## 4｜Stage 02 / 04 / 05边界

### Stage 02｜Director Contract
按需锁：`Entry Camera Height / Entry Vertical Angle / Entry Subject View / Lens Family / Focus Plan / Stabilization / Shot Relation`。若Camera Motion会改变Geometry，还必须锁其叙事要求与`Landing Camera Geometry`，但不需要在导演层写逐帧工程路径。
普通T1/T2只填写会改变镜头含义的字段；T3/T4、关键Reveal、复杂多人/动作、主观镜头或焦点转移才完整填写。

### Stage 04｜Previs Proof
只执行/证明Stage 02已锁字段：
- Entry构图是否从指定高度/方向成立；若Camera Motion改变Geometry，Landing Geometry是否也成立；
- Lens Family要求的前后景关系是否可见；
- Focus Start/End是否有可辨识目标；
- Camera Path与Stabilization是否物理兼容；
- 相邻Panel/CUT是否保留Shot Relation。

不得为了“分镜更漂亮”换Entry/Landing Camera Geometry、Lens Family、Focus Strategy或Shot Relation。

### Stage 05｜Typed Execution
唯一Owner：
- `CINEMATOGRAPHY_STATE`：Entry Height / Entry Vertical Angle / Entry Subject View / Lens Family / DOF / Stabilization；
- `CAMERA_TIMELINE`：Motion / Path / Speed / Motion Curve / Focal Behavior / Geometry Change / Landing Camera Geometry / Landing Composition；
- `FOCUS_TIMELINE`：Focus Plane / Focus Behavior / Trigger / Landing。

Final Prompt只写模型执行真正需要的字段。Reference已经明确构图/机位/风格时不重复摄影理论说明。

## 5｜Hard Conflict

以下未解决不得进入Final Video Prompt：
- `CINEMATOGRAPHY_STATE_CONFLICT`：同一时间Camera Height / Vertical Angle / Subject View / Lens Family / DOF / Stabilization出现互斥值；
- `FOCUS_STATE_CONFLICT`：同一时间要求互斥Focus Plane / Focus Behavior，或RACK/TRANSFER缺少合法Start→Landing；
- `LOCKED_OFF_MOTION_CONFLICT`：LOCKED_OFF同时又要求Pan/Tilt/Dolly/Truck/Crane/Arc/Follow等实际Camera Motion；
- `FOCUS_READABILITY_CONFLICT`：Critical Read要求同时清楚，但DOF/Focus Plan使其不可读；
- `SHOT_RELATION_CONFLICT`：Cut Motivation与实际前后镜头连接方式不成立。

## 6｜防止再次过度工程化

- 不为普通镜头机械填写所有字段；
- 不把毫米数、镜头品牌、摄影术语当质量本身；
- 不因为增加Lens/Focus字段就重复描述Reference已经锁定的构图；
- 不允许Stage 05临时添加“电影感拉焦 / 手持 / 长焦压缩”等未经过Stage 02锁定的装饰动作；
- 摄影语法服务Audience State、Critical Read与动作可读性，不反向主导剧情。

## Current｜Perception-First Cinematography Contract

> **新增Owner字段：** `CAMERA_ETHICS / ATTENTION_FLOW / SHOT_SCALE_JUSTIFICATION / CAMERA_PLACEMENT_JUSTIFICATION / COMPOSITION_MECHANISM / VISUAL_FORCE_STACK / VISUAL_SALIENCE_BUDGET`。这些字段属于Stage 02摄影判断；Editorial只能消费，Stage 05只能执行。

### Camera Ethics｜观众为什么站在这里
每个Formal Shot选择一个主观看伦理：
`NEUTRAL_WITNESS / INVOLVED_PARTICIPANT / FORBIDDEN_WITNESS / DISTANT_OBSERVER / SURVEILLANCE_OBSERVER / TRAPPED_OBSERVER / CHARACTER_ALIGNED / MISINFORMED_OBSERVER / OTHER`。

它不是机位名称。`FORBIDDEN_WITNESS`可以由门外、玻璃后或远距长焦实现；具体几何仍由Camera Contract决定。

### Attention Flow｜注意力流量
每镜在锁机位前先写：

```text
Entry：观众第一眼从哪里进入
Resistance：什么遮挡/延迟/加速注意力；没有时明确NONE_INTENTIONAL
Decisive Landing：必须读到的决定性信息
Residual Information：边缘/背景/失焦里故意保留什么；没有时明确NONE_INTENTIONAL
Exit：视线如何离开画面或被下一镜接走
```

如果这五项只是在复述“人物在中间、背景有门”，标`ATTENTION_FLOW_GAP`。Attention Flow必须描述观看顺序，不是元素清单。

### Shot Scale Justification｜景别不是免费情绪增强器
所有Shot都记录`required_information + narrative_gain`。CU / ECU / DETAIL / INSERT额外必须回答：
- `why_wider_fails`：为什么更宽看不到当前必须读到的信息；
- `spatial_information_sacrificed`：靠近后主动牺牲了什么空间信息；
- `narrative_gain`：这种牺牲换来了什么不可替代的叙事收益。

“更有情绪 / 更电影 / 更紧张 / 更好看”不是合法理由。失败：`CLOSEUP_JUSTIFICATION_WEAK / CLOSEUP_SPATIAL_COST_GAP`。

### Camera Placement Double Justification
每个重要Shot同时写：
- `physical`：摄影机在世界空间中为什么能在这里；
- `narrative`：导演为什么要让观众站在这里。

物理可达但叙事无理由，或叙事有理由但穿墙/占用不可能，都不得锁定。

### Composition Mechanism Budget
每镜只允许`1 Primary Composition Mechanism + 最多1 Secondary`。不是禁止复杂画面，而是防止“中轴+极端俯拍+门框+镜面+大负空间+前景虚焦”同时竞争。

### Visual Force Stack
每镜最多：`1 Primary Visual Force + 2 Supporting Forces`。例如`Spatial Pressure + Performance + Color`。特殊Lens/光学事件若存在必须消耗一个Supporting位置，除非它本身就是Primary。

### Visual Salience Budget
Prompt可以很详细，但画面显著信息必须克制：

```text
Primary Salience：唯一主注意点
Secondary Salience：可选的第二线索
Ambient Information：只需存在、不抢注意力的环境事实
Suppressed Information：必须退到背景/暗部/遮挡的信息
Allowed Mundane Area：允许普通、空、软、暗、不设计的区域
```

`Execution Density ≠ Visual Salience Density`。Stage 05详细Prompt不能把每个Runtime事实都变成视觉主角。

Hard Fail：`CAMERA_ETHICS_GAP / ATTENTION_FLOW_GAP / SHOT_SCALE_JUSTIFICATION_GAP / CAMERA_PLACEMENT_JUSTIFICATION_GAP / VISUAL_FORCE_STACK_OVERLOAD / VISUAL_SALIENCE_BUDGET_GAP`。
