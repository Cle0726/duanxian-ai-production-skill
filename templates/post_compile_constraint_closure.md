# Post-Compile Constraint Closure（编译后约束闭环）｜Current Authority

> **目的：** 解决“Typed State已经无冲突，但Natural-language Compiler / Dedup / Egress Rewrite又重新制造冲突”的最后一公里问题。
>
> **核心：** `PRE-COMPILE PASS ≠ FINAL PROMPT PASS.` Final Prompt必须在所有会改写文字的步骤完成后反向解析，并与`RESOLVED VIDEO_EXECUTION_STATE`逐字段比对。

## 1｜唯一合法顺序

`Typed State → Conflict Solver → Shot Proof/Readiness → Natural-language Compile → Semantic Dedup → Surface Sanitizer → Egress Rewrite → POST-COMPILE REVERSE CHECK → Mechanical Surface Lint → FINAL_COPY_SURFACE`

Post-Compile Closure检查的是**真正准备交付的最终候选正文**，不是早期Internal Draft。

## 2｜Surface Requirement

每条Resolved Constraint在Typed State中标记：
- `MODEL_TEXT`：视频模型必须从文字读到；
- `VISUAL_REFERENCE`：由已验证视觉Reference承担，Final Prompt可不复述；
- `INTERNAL_ONLY`：只用于求解/QC/生产控制，不应进入模型正文。

因此“Final Prompt没有把全部State复述一遍”不算缺失；只有`MODEL_TEXT`必需事实缺失才Fail。

## 3｜Reverse Claim Map

Final Candidate生成后，内部把正文重新解析成与Typed State同Schema的`POST_COMPILE_CLAIM_MAP`：

```text
POST_COMPILE_CLAIM_MAP
- DOMAIN
- SUBJECT
- PREDICATE
- VALUE
- TARGET（适用时）
- TIME_SCOPE
- FRAME_SCOPE
- POLARITY
- OWNER = PROMPT_COMPILER
```

自然语言里的同义词必须先Canonicalize，例如“完全固定/锁定机位”→`CAMERA.MOTION=STATIC`；“缓慢推近”→`DOLLY_IN`；“无任何人类声音”→`ALL_HUMAN_SOUND=OFF`。

## 4｜五项零容忍检查

```text
POST_COMPILE_CONSTRAINT_CLOSURE
NEW_CONSTRAINT_IN_PROMPT = 0
MISSING_REQUIRED_MODEL_TEXT = 0
STATE_CONTRADICTION = 0
AMBIGUOUS_EXCLUSIVE_VALUE = 0
MULTI_OWNER_REINTRODUCED = 0
STATUS = PASS / BLOCKED
```

### NEW_CONSTRAINT_IN_PROMPT
Prompt出现Resolved State没有授权的新Lens、Focus、Camera Move、动作、声音、空间关系、综合色/Style状态等。

### MISSING_REQUIRED_MODEL_TEXT
标记`SURFACE_REQUIREMENT=MODEL_TEXT`的P0/必要执行事实没有出现在Final Candidate。

### STATE_CONTRADICTION
Final Candidate与Resolved State值相反，或自身重新出现Camera/Audio/Temporal/Spatial/Action/Focus等Hard Conflict。**同值但时间范围被Compiler擅自扩大也属于矛盾**：例如State只锁`0–2s STATIC`，Prompt写成`0–5s全程静止`不得视为“同义”。`WORLD`与`FRAME_VISIBLE`等Frame Scope也不得互换。

### AMBIGUOUS_EXCLUSIVE_VALUE
Final Candidate重新出现“静止或轻推 / A或B / maybe / alternatively”等互斥分支。

### MULTI_OWNER_REINTRODUCED
Final正文同一事实出现两套来源/两种表述并重新产生不同值；所有最终语义Claim的Owner必须收敛为`PROMPT_COMPILER`。

## 5｜必须覆盖的反查域

至少检查：
- Camera Motion / Focal Behavior / Entry-Landing Geometry；
- Lens / DOF / Stabilization / Focus；
- Audio父子Ontology（Dialogue/Scream/Shout/Word-forming/Breath/Gasp）；
- Action Preconditions / State Order / Exit；
- Spatial Start / Relation / Direction / Target / End；
- World vs Frame-visible Scope；
- MODEL_TEXT时间窗是否完整覆盖且没有向未授权时段扩张；
- Reference Role经过Compiler后是否被错误文字化成另一套Authority；
- P0 Director Invariants中实际需要写给模型的Hold/Cut/Reveal/Reaction执行事实。

## 6｜失败后的唯一修复

`POST_COMPILE_CONSTRAINT_CLOSURE != PASS`：

**禁止在Final Prompt上Patch一句。**

执行：
`Discard Candidate → Return to Resolved Typed State → Correct Owner/Surface Requirement if needed → Fresh Compile → Reverse Check again.`

理由：在已经冲突的自然语言上继续追加“修正说明”会产生新的优先级歧义与旧句残留。

## 7｜Mechanical Lint

有脚本能力时必须运行`validators/post_compile_constraint_lint.py`，输入`resolved_constraints + prompt_claims`。脚本负责：
- Prompt内部Mechanical Conflict；
- Prompt Claim是否有Resolved授权；
- MODEL_TEXT必需事实是否缺失；
- 值/极性是否与Resolved State矛盾；
- 是否重新出现多Owner。

无法机械判定的导演语义、隐喻或复杂空间关系仍由本Closure做语义裁决。**机械PASS不能替代语义反查。**

## 8｜Blind执行

DeepSeek可以对自己刚生成的文字做Reverse Claim Map；这不需要视觉能力。只有某个Claim是否与真实Reference空间/人物内容一致需要看图时，才调用Visual Handoff。

Blind版不得因为“我刚刚就是按State写的”而跳过反查；Compiler输出本身就是被审对象。
