# Prompt Constraint Solver & Conflict Matrix（提示词约束求解器）｜Current Authority

> **目的：** `Semantic Dedup`只解决“同一件事说了多次”；本Solver解决更危险的问题：**两条不同指令能否同时成立。** Final Prompt之前必须在`VIDEO_EXECUTION_STATE`上求解冲突，而不是把互斥要求交给视频模型猜。

## 1｜Mandatory Conflict Classes

### VALUE_CONFLICT
同一`SUBJECT + PREDICATE + TIME_SCOPE`出现互斥Value。
例：Camera 0–2s=`STATIC`同时=`DOLLY_IN`。

### TEMPORAL_CONFLICT
同一对象在重叠时间被要求执行不可并行状态。

### POSITIVE_NEGATIVE_CONFLICT
正向允许内容被更宽泛的Negative再次禁止。
例：`NONVERBAL_BREATH=ON`，同时写`ALL_HUMAN_SOUND=OFF`。

### AUDIO_ON_OFF_CONFLICT
同一声音类别或父子声音类别在同时间同时ON/OFF。

### REFERENCE_OWNER_CONFLICT
同一关键字段被两个不同Reference同时声明为唯一Authority，且没有主从关系。

### REFERENCE_CONTENT_ROLE_CONFLICT
实际Reference Binding声称控制人物/道具/综合色等字段，但当前已验证绑定图不包含对应证据；无论Binding来自UI Slot、Attachment、Native Token或API Handle都适用。

### STATE_ORDER_CONFLICT
事件前后顺序不可能同时成立。
例：硬币在急刹前既要求“掌心”又要求“已在地面滚动”。

### SCOPE_CONFLICT
把World State、Frame-visible State、Off-screen State混成同一个事实。
例：`车厢20+乘客`不等于`画面必须看见20+人`。

### ACTION_SET_CONFLICT
某段声明“人物唯一允许动作=A”，后续却要求同一人物执行B。

### CAMERA_STATE_CONFLICT
Camera的Motion / Focal Behavior / Geometry Change存在互斥组合。`STATIC`不能同时Zoom、改变Camera Geometry，也不能出现Entry/Landing Geometry不一致。

### CINEMATOGRAPHY_STATE_CONFLICT
同一时间Camera Height / Vertical Angle / Subject View / Lens Family / DOF / Stabilization出现互斥状态，或Stage 05临时加入Stage 02未锁定的装饰性Lens/Focus/Handheld。

### FOCUS_STATE_CONFLICT
同一时间Focus Plane / Focus Behavior互斥；或要求RACK/TRANSFER但没有两个可辨识深度目标、Trigger与Landing。DOF属于`CINEMATOGRAPHY_STATE`，其互斥值归`CINEMATOGRAPHY_STATE_CONFLICT`。

### LOCKED_OFF_MOTION_CONFLICT
`LOCKED_OFF`同时要求Pan/Tilt/Dolly/Truck/Crane/Arc/Follow等实际Camera Motion。

### SPATIAL_POSITION_CONFLICT
同一主体在重叠时间被要求位于互斥Frame Region / Depth，且不是已声明的连续Movement Transition。

### SPATIAL_TRAJECTORY_CONFLICT
主体Start / Motion Direction / Motion Target / End Landing互不相容，或同一时间要求互斥移动方向。

### SPATIAL_RELATION_CONFLICT
同一主体对同一Target同一时间要求互斥关系，例如同时`IN_FRONT_OF`与`BEHIND`。

### SPATIAL_TARGET_GEOGRAPHY_CONFLICT
Movement Target与当前Approved Environment Geography / Verified Anchor位置不相容。

### SPATIAL_OWNER_CONFLICT
Blocking / Action / Camera或后处理模块重新声明第二套人物/Prop位置、方向或落点。

### REFERENCE_TEXT_SUPPRESSION_CONFLICT
某Reference/Binding/Dedup/Sanitizer规则以“图片已经画清”“已经@绑定”“Runtime已有摘要”为理由，要求删除当前Shot仍需要的镜头目标、起始状态、人物/服装、空间、道具、构图/景别、Camera、Timeline、动作/表演/视线、肢体占用、物理、环境动态、光影综合色、声音/对白/呼吸、Ending State或必要限制。

裁决：**Reference负责稳定与字段Authority，不拥有Stage 05正文裁剪权。** 保留当前Shot可执行文字，删除压缩指令。

### PROMPT_DENSITY_POLICY_CONFLICT
同一Stage 05任务同时出现“短Prompt/只写补充信息/Reference已足够”与“`PROMPT_LENGTH_CEILING = NONE`的完整详细Master Prompt”两种编译策略。

裁决：以`video_prompt_template.md + prompt_compiler.md`为Stage 05唯一Prompt Density Authority；先生成完整Master Prompt。平台若有已验证字符上限，只能由Target Adapter另产适配版，不能反写Source Master。

## 2｜Authority Resolution Priority
冲突不得靠“更晚出现的句子”覆盖。按下列顺序裁决：
1. 用户当前明确要求；
2. Story / World Canon；
3. Director Decision Card / Sequence Arc；
4. Approved Previs / Camera Contract；
5. Current World State / Continuity；
6. Most Direct Approved Visual Authority；
7. Execution-derived physical solution；
8. Style / aesthetic preference；
9. QC wording / convenience wording。

低Authority冲突项必须删除或改写；若两个同级P0 Authority冲突且现有规则无法裁决，返回上游，不得偷偷平均。

## 3｜Prompt Conflict Preflight

```text
PROMPT CONFLICT PREFLIGHT
Hard Conflict Count：0
Value Conflict：0
Temporal Conflict：0
Positive-Negative Conflict：0
Audio Conflict：0
Reference Owner Conflict：0
Reference Content-Role Conflict：0
State-Order Conflict：0
Scope Conflict：0
Action-Set Conflict：0
Camera Conflict：0
Cinematography Conflict：0
Focus Conflict：0
Spatial Position Conflict：0
Spatial Trajectory Conflict：0
Spatial Relation Conflict：0
Spatial Target/Geography Conflict：0
Spatial Owner Conflict：0
Reference Text Suppression Conflict：0
Prompt Density Policy Conflict：0
Resolution Log：<只留内部>
STATUS：PASS / BLOCKED
```

**任一未解决Hard Conflict > 0：`NO FINAL PROMPT`。**


## 3.1｜Mechanical Conflict Lint
Final Prompt前必须对结构化Constraint State运行`validators/prompt_constraint_lint.py`。Mechanical Lint至少覆盖：`AMBIGUOUS_EXCLUSIVE_VALUE / VALUE_CONFLICT / POSITIVE_NEGATIVE_CONFLICT / AUDIO_ON_OFF_CONFLICT / CAMERA_STATE_CONFLICT / CINEMATOGRAPHY_STATE_CONFLICT / FOCUS_STATE_CONFLICT / LOCKED_OFF_MOTION_CONFLICT / ACTION_SET_CONFLICT / SCOPE_CONFLICT / REFERENCE_BINDING_UNVERIFIED / REFERENCE_CONTENT_ROLE_CONFLICT / REFERENCE_OWNER_CONFLICT / STATE_ORDER_CONFLICT`。

机械Lint只负责可形式化冲突；无法机械判定的导演语义/物理互斥仍由本Solver裁决。两者任一BLOCK都不得出Prompt。

## 4｜SEG03 Regression Examples
- `NONVERBAL_BREATH=ON` + `ALL_HUMAN_SOUND=OFF` → FAIL，裁决为“无对白/惊叫/喊声；允许非语言喘气”。
- `0–2s STATIC OR DOLLY_IN` + `0–2s STATIC ONLY` → FAIL，必须唯一化Camera状态。
- 前文`@图2=CHARACTER`、后文`@图3=CHARACTER` → FAIL，先回Reference Binding Semantic Verification。
- `PASSENGER_ACTION_SET=BRAKE_REACTION_ONLY` + 10–13s新增`BEND_ARMREST` → FAIL，重新定义允许动作集合或删除低价值事件。

## 5｜与Semantic Dedup关系
固定顺序：`Typed State → Conflict Solver → Complexity/Proof → Natural-language Compile → Semantic Dedup → Surface/Egress Rewrite → Post-Compile Constraint Closure`。
**没有冲突 ≠ 没有重复；没有重复 ≠ 没有冲突。两者必须分别通过。**


## 6｜Post-Compile Boundary
本Solver只证明**Resolved State在编译前可同时成立**。Final Candidate仍必须执行`post_compile_constraint_closure.md`；若Compiler/Dedup/Egress Rewrite重新加入新Camera/Audio/Action/Spatial事实、遗漏MODEL_TEXT P0事实或制造矛盾，必须Fresh Compile，不得拿Preflight PASS为最终Prompt背书。
