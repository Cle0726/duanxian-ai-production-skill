# System Integrity Authority｜V4.3 Cross-Module Invariants

> **用途：** 只检查跨模块不变量，不重复Actor、Camera、Color、Reference、Action、QC等领域细节。领域正确性由各自Source Authority与Local Gate负责。

## I-01｜Stage Ownership

每个Stage只能创建/修改其拥有的Authority。Stage 04不得无因重导演；Stage 05不得为模型方便静默修改Director Core；Stage 06不得回写Canon。

## I-02｜Workflow Integrity

状态转换只能依据`controller/workflow_state_machine.yaml`。不得因为“看起来已经可以”跳过Lock、Freeze、Storyboard Approval、Video Approval或Continuity prerequisites。

## I-03｜Approval Authenticity

`QC PASS`、`Candidate Recommended`、`READY`均不等于`APPROVED`。需要User Approval的Transition只有在用户明确批准且Approval Record写入后成立。

## I-04｜Evidence Authenticity

不存在真实图像、视频、文件或可访问Evidence时，不得声称已完成视觉检查、文件归档、Ending Frame提取或真实Hash验证。UI预览/文件名字符串不等于文件字节。

## I-05｜Continuity Evidence Authenticity

正式Previous Ending Frame只能来自真实`APPROVED VIDEO`。Storyboard尾格、计划Exit、AI推测Frame、Local Patch后的伪尾帧不得冒充Continuity Authority。

## I-06｜Authority Provenance

下游State/Runtime必须可追溯到当前有效Source版本。正式Lock/Freeze/Approval应记录`artifact_id + version + fingerprint/hash + status + source_refs`；无法得到真实文件Hash时使用结构化内容Fingerprint并明确类型。

## I-07｜Authority Change Propagation

任何Source Authority、Approved Asset、Director Core、Scene Color、Storyboard或关键Reference版本变化，必须运行Change Impact并使受影响Runtime标记`STALE`。只重开受影响依赖，不默认全项目重做。

## I-08｜No Silent Director Drift

执行层如果平台/模型限制会损害Director Invariant，返回Execution Constraint Conflict或回Director Judge；不得静默换成Generic Coverage、删除关键Beat或改变角色关系。

## I-09｜Runtime Cannot Create Authority

Runtime Capsule只能压缩、投影、解析Source Authority，不能创造新的Canon、导演决定、资产身份或平台能力。Runtime缺字段时回源，不用猜测补齐。

## I-10｜Revision Scope Integrity

Revision先冻结QC Scope。已经CLOSED且未受Change Impact影响的维度不重复打开；失败Candidate如果是Edit Target，应保留其Revision Source身份。修复一个局部错误不得顺手重设计其他已Approved字段。

## I-11｜Fresh Compile Integrity

旧Prompt、旧Compiler文字或失败Prompt只能恢复Intent/已批准状态。发生Stale、Constraint Conflict、Post-Compile Closure失败时必须从Resolved State Fresh Compile，不允许在旧Prompt末尾无限追加“再不要……”补丁。

## I-12｜Prompt Surface Integrity

模型执行Prompt只包含执行内容。Stage、Gate、Authority、Registry、Runtime字段名、本地路径、内部Asset ID/Version、QC Checklist、文件管理文本不得泄漏到Copy Surface，除非目标模型真实需要的Reference Token。

## I-13｜Capability Boundary

平台时长、图片槽位、音频能力、文件写入能力、QC能力未知时保持`UNKNOWN`。不得把经验默认值冒充Verified Capability；已配置Adapter/Profile的值只对该Profile有效。

## I-14｜State/Route Single Source of Truth

Flow只由`controller/workflow_state_machine.yaml`拥有；Route只由`controller/route_registry.yaml`拥有；Authority Owner索引只由`controller/authority_registry.yaml`拥有。兼容Markdown不得维护第二份可执行表。

## I-15｜No Blind Visual Guessing

当前Controller没有视觉能力时，图片实际内容只能来自Fingerprint匹配的Current `VISUAL_EVIDENCE`或用户明确提供的视觉事实。文件名、Asset ID、原生成Prompt、历史意图、旧描述都不能替代真实观察；Text-only Controller不得创建新的视觉PASS。

## Preflight

正式任务出站前只做四问：

1. 当前Transition是否合法？
2. 当前事实是否来自唯一Owner且版本有效？
3. Required Runtime/Local Gate是否PASS？
4. Evidence/Approval是否真实？

任一答案为否，BLOCK并按`controller/failure_router.yaml`最小回退。

## Current｜Perception & Anti-Pattern Integrity

- **Perception Before Optics：** D1/D2 Formal Shot不得在`UNRESOLVED_STATE / RELATIONAL_PRESSURE`未建立时直接用Shot Size/Lens替代导演判断。
- **Close-up Has A Cost：** CU/ECU/Detail必须证明不可替代的信息收益与被牺牲的空间信息；“更有情绪”不是Authority。
- **Camera Has Two Reasons：** Camera Position同时满足物理可行与叙事观看理由。
- **Execution Density ≠ Salience Density：** 详细Prompt不得把所有执行事实升级为同等视觉重点。
- **Anti-pattern Telemetry Is Advisory：** 历史重复Warning不得自动改变导演方案；只有无Intent的模式坍缩才要求Review。
- **Causal Sequence Must Resist Shuffle：** 声明为CAUSAL的Sequence必须有可验证的信息/动作/视线/声音依赖；Associative/Montage不得被误判成因果失败。
