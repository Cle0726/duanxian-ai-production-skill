# Typed Video Execution State（结构化视频执行状态）｜Current Authority

> **V4.3 Temporal Scope：** `start/end`与`time_scope`的机械重叠语义由`validators/temporal_scope.py`统一拥有，Pre-Compile与Post-Compile Validator不得各自实现不同的时间重叠规则。

> **目的：** Stage 05不再允许Style / Camera / Performance / Audio / Reference / Physics等模块各自直接往Final Prompt追加自然语言。所有模块先把“它认为必须成立的事实”写入同一个`VIDEO_EXECUTION_STATE`，再由Conflict Solver检查是否能够同时成立。
>
> **核心原则：** `MODULES WRITE STATE, NOT PROMPT TEXT.`

## 1｜VIDEO_EXECUTION_STATE Schema

```text
VIDEO_EXECUTION_STATE
Segment / Shot：
Narrative Core：<当前生成真正必须表达的1–3个核心变化>
Narrative Duration：
Generation Duration：<若平台固定Slot与叙事时长不同才填写>
Trim Handle：<N/A或不承担新叙事的余量>

DIRECTOR_INVARIANTS
- Audience Alignment：
- Reveal / Withhold：
- Reaction Give / Deny：
- Opening / Closing Function：

FRAME_SCOPE
- WORLD_POPULATION：<世界中实际存在多少人/物>
- FRAME_VISIBLE_POPULATION：<当前构图清楚看见多少>
- FOCUS_OWNER：
- CRITICAL_VISUAL_READS：<P0/P1/P2>

REFERENCE_BINDING_MAP
- Binding Handle / Binding Mode / Expected Fields / Verified Actual Content / Evidence Source / Result

CINEMATOGRAPHY_STATE
- Entry Camera Height / Entry Vertical Angle / Entry Subject View
- Lens Family / Depth of Field
- Stabilization / Support

CAMERA_TIMELINE
- start-end / Motion / Path / Speed / Motion Curve / Focal Behavior / Geometry Change / Landing Camera Geometry / Landing Composition

SPATIAL_EXECUTION_STATE
- shot scope / stable environment anchors
- subject / start horizontal region / start depth / orientation / relation + target
- motion vector / path / motion target
- end horizontal region / end depth / end relation / visibility-occlusion change
- prop / start holder-region-depth / release-trajectory-contact target / end-rest target

FOCUS_TIMELINE
- start-end / Focus Plane / Focus Behavior / Trigger / Landing

SUBJECT_STATE
- subject / state / time scope / frame scope / priority

ACTION_TIMELINE
- start-end / subject / primary action / secondary action / prop/contact / exit

AUDIO_STATE
- DIALOGUE：ON/OFF
- SCREAM：ON/OFF
- SHOUT：ON/OFF
- WORD_FORMING_VOCALIZATION：ON/OFF
- NONVERBAL_BREATH：ON/OFF
- GASP：ON/OFF/CONDITIONAL
- FOLEY：ON/OFF + events
- AMBIENCE：ON/OFF + events
- BGM：ON/OFF

STYLE_COLOR_STATE
- Render Core：
- Scene Color：
- Shot Lighting：

RESTRICTION_STATE
- 仅记录仍有真实污染路径且未被正向状态解决的残余限制
```

## 2｜Typed Constraint Record

Execution State中的每个可冲突事实都可规范化为：

```text
CONSTRAINT_ID
DOMAIN
SUBJECT
PREDICATE
VALUE
ALLOWED_VALUES = <ACTION_SET等集合约束适用时>
TIME_SCOPE
FRAME_SCOPE
POLARITY = POSITIVE / NEGATIVE
HARDNESS = HARD / SOFT
PRIORITY = P0 / P1 / P2
AUTHORITY_SOURCE
OWNER
SURFACE_REQUIREMENT = MODEL_TEXT / VISUAL_REFERENCE / INTERNAL_ONLY
```

`TIME_SCOPE`未知时不得假造精确秒数；可使用`ENTRY / BRAKE_EVENT / AFTERMATH / EXIT`等已锁Beat范围。


## 2.1｜Mechanical Lint Normalization
- Exclusive HARD Constraint不得把`A OR B / A或B`塞进同一个VALUE；必须先由Owner裁决成唯一值，否则`AMBIGUOUS_EXCLUSIVE_VALUE`。
- Camera Motion统一使用`CAMERA / <camera> / MOTION / STATIC|DOLLY_IN|...`，重叠时间STATIC与移动状态触发`CAMERA_STATE_CONFLICT`。
- Entry Camera Height / Entry Vertical Angle / Entry Subject View / Lens Family / DOF / Stabilization使用唯一值；同一有效时间点出现互斥值触发`CINEMATOGRAPHY_STATE_CONFLICT`。由已锁Camera Motion合法产生的Height / Angle / View变化必须写进`CAMERA_TIMELINE.Geometry Change / Landing Camera Geometry`，不得拿Entry值当全段冻结值。
- `STABILIZATION=LOCKED_OFF`与任何移动/旋转Camera Motion重叠时触发`LOCKED_OFF_MOTION_CONFLICT`。
- DOF由`CINEMATOGRAPHY_STATE`唯一拥有；Focus Plane / Focus Behavior由`FOCUS_TIMELINE`唯一拥有。DOF出现互斥值触发`CINEMATOGRAPHY_STATE_CONFLICT`；Focus Plane / Focus Behavior互斥，或RACK/TRANSFER缺少可辨识Start→Landing时触发`FOCUS_STATE_CONFLICT`。
- `HUMAN_AUDIO / ALL_HUMAN_SOUND / HUMAN_SOUND = OFF`均视为声音父类；与`NONVERBAL_BREATH/GASP/... = ON`重叠时触发`AUDIO_ON_OFF_CONFLICT`。
- `ACTION_SET`若声明`ALLOWED_VALUES`，同一Subject/时间窗出现集合外动作触发`ACTION_SET_CONFLICT`。
- `SPATIAL`域统一使用Frame Region / Depth / Relation / Motion Direction / Target / End Landing；同一主体重叠时间出现互斥位置触发`SPATIAL_POSITION_CONFLICT`，Start→Motion→End不相容触发`SPATIAL_TRAJECTORY_CONFLICT`，同一Target互斥前后关系触发`SPATIAL_RELATION_CONFLICT`。
- 世界人数与画面可见人数必须用`WORLD_POPULATION`和`FRAME_VISIBLE_POPULATION`分字段；不得使用一个泛化`POPULATION`跨WORLD/FRAME_VISIBLE Scope。

## 3｜单一字段Owner
- Entry Camera Geometry与固定光学/支撑属性只由`CINEMATOGRAPHY_STATE`拥有；Camera运动及其合法Geometry Change/Landing只由`CAMERA_TIMELINE`拥有；动态焦点只由`FOCUS_TIMELINE`拥有。别的模块不得再写“或许静止/或许慢推/电影感拉焦/改成长焦”等第二套Camera指令。
- 声音开关只由`AUDIO_STATE`拥有；剧情文学描述中的“寂静”不能直接覆盖已允许的Nonverbal Breath。
- Reference实际绑定职责只由`REFERENCE_BINDING_MAP`拥有；UI槽位、Attachment、Native Token、API Handle都属于Binding Handle，后文人物/综合色/环境段不得重新把同一字段指向另一张图。
- 动态动作只由`ACTION_TIMELINE`拥有；Entry只拥有t=0状态。
- 人物/Prop的动态Frame Region、Depth、Orientation、Relation、Motion Target与End Landing只由`SPATIAL_EXECUTION_STATE`拥有；`ACTION_TIMELINE`描述做什么但不得另写第二套左右/前后/落点；Camera自身空间由Camera Owner负责。
- WORLD_POPULATION与FRAME_VISIBLE_POPULATION必须分字段，禁止用一个“人数”字段同时表达世界占用与画面可见数量。

## 3.1｜Model Surface Responsibility
- `MODEL_TEXT`：模型必须从Final Prompt读到；
- `VISUAL_REFERENCE`：已由真实视觉输入承担，可不在文字复述；
- `INTERNAL_ONLY`：仅用于求解/QC，不得进入模型正文。

该标记供`post_compile_constraint_closure.md`判断“真正缺失”而不是强迫Final Prompt复述全部内部State。

## 4｜Hard Gate
没有完成`VIDEO_EXECUTION_STATE`，或存在同一事实由两个Owner同时持有：
`EXECUTION_STATE_INCOMPLETE / EXECUTION_FIELD_MULTI_OWNER` → `PROMPT_COMPILATION_BLOCKED`。
