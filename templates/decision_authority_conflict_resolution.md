# Decision Authority & Conflict Resolution（决策权与冲突裁决）

> **用途：** 让Skill在一人制片流程中自动承担导演/执行层判断，减少无意义提问；同时保证真正会改变《断弦之歌》Canon的冲突不会被偷偷猜掉。

## 1｜核心规则：先裁决，再提问

遇到缺失、歧义、冲突时固定执行：

**Locate Authority → Compare Scope → Auto Resolve if Safe → Mark Derived/Open if Needed → Continue → Ask Only if Canon-Blocking**

禁止因为字段没填满、存在多个“都能拍”的导演方案、或AI执行细节未指定，就把选择题丢给用户。

## 2｜默认自动决定（DO NOT ASK）

**Director Intelligence Boundary（Current Rule）：** “自动决定”不等于“生产模块随便决定”。Stage 02的Shot景别、机位、POV、Reaction、Blocking、Cut等必须通过Director Intelligence → Department Critique（按Tier）→ Director Judge产生；Approved资产、Reference、成本与模型限制只在Selected Plan之后决定执行方式。

以下通常属于Skill导演/生产执行权：
- Shot景别、机位、必要运镜；
- Segment时长与是否拆Segment：导演自动决定完成Beat所需的最短自然时长；Skill不设置固定单次生成上限。只有当前平台明确Hard Max或真实执行结构需要时，才在Execution Translation自然拆分；
- Panel数量与信息增量；
- Reference Pack选择、职责与上传顺序建议；
- Actor Performance的Objective / Obstacle / Tactic / Subtext / Listening Response / Beat Boundary，以及Reaction Latency、Emotion Intensity与Emotional Carrier；
- 日常对白的Thought Intention、Speech Phrase、Continuity Bridge、视线、手部、Listener Flow与必要换气表现，只要不改变剧情事实；
- Combat Archetype、Measure、Initiative、Footwork、攻防交换与Counter Window，只要不创造新Lore能力；
- 动作物理后摇、惯性、站位暴露、恢复窗口等Execution Consequence；
- P1/P2连续性修正与已明确Authority下的最小必要修订。
- 新场景综合色派生：从Global Color DNA自动建立Scene Color Extension Spec；满足重复使用/显著气候材质差异/多镜漂移风险时自动标记Stage 03需要正式Scene Color Extension Card，不反问用户“要不要做色卡”。
- World State Continuity的导演连接：Visual / Residual / Implied Bridge选择、Arrival Shot、普通开门/下车/收起道具/人物离场等最小必要连接，只要不创造新Story/World Canon。
- Action Feasibility的执行裁决：优先使用空闲手、维持当前Held Prop支撑、补最小换手/放下/重心转移/靠近/接触Bridge，只要不改变Story/Canon含义；标记`DERIVED PHYSICAL RESOLUTION`。

这些都应给出Skill的最佳导演判断，不问“你想选A还是B”。

## 3｜Authority按领域裁决

不是“某一个文件永远最高”，而是看冲突属于哪个领域：

- **Story Event / Outcome**：当前`EPISODE SCREENPLAY LOCK`；其Locked Story Facts必须可追溯到最新用户批准的小说/Canon/Final Screenplay Source。
- **World Canon / Long-term Mechanic**：正式世界观、Canon Ledger、用户已拍板P0规则。
- **Character Identity**：Approved Character Master / Transformation Master。
- **Current Costume / Prop Structure**：当前剧情阶段Approved Master。
- **Current Semantic World State**：Stage 02 World State Ledger + 已确认剧情事实，负责跨Scene的Prop / Injury / Knowledge / Environment Runtime / Motion / Relationship carryover。若完整Transformation触发`TRANSFORMATION_RECOVERY`，Post-Recovery Injury State立即成为当前语义伤势Authority，旧Pre-Recovery Injury不得继续覆盖它。
- **Current Precise Visual State**：真实Approved Previous Ending Frame + Continuity Snapshot，负责CONTINUITY_ENTRY的具体视觉起点。
- **Scene Canon Geometry**：Approved Environment Canon Master / Geography Spec。
- **Current Shot View Geometry**：若存在匹配机位的Approved Environment Derived Coverage，则Coverage优先承担当前可见方向Authority；Parent Master只补仍独有Canon字段。
- **Render Style / Drawing Grammar**：Project Style DNA + Approved Render Style Anchor / Evidence Board。
- **Cinematic Shot Grammar**：Approved Cinematic Shot Style Anchor；若与当前Director / Storyboard具体Camera冲突，以当前Shot Contract为准。
- **Color Authority**：Global Color DNA → Scene Color Extension → Shot Lighting Variant；下层只覆盖自己范围内的综合色/光色变量，不重写上层项目语法。
- **Music Identity**：Approved Music Identity Card / Registry。
- **Combat Long-term Rule**：Combat Canon + Combat Choreography Engine；小说中的单次旧动作不自动升级为Combat Canon。
- **Current Combat Choreography**：Story提供Narrative Goal / Victory Condition，Combat Engine负责运行时推导。

如果两个来源各自在自己的职责范围内都成立，不把它们错误视为冲突。

## 4｜四种处理状态

### AUTO_RESOLVED
Authority清楚，Skill自动采用正确来源并继续。

### DERIVED
不是Canon事实，而是Skill为了当前执行推导出的导演决定。可以继续使用，但不得反向写成长期世界观。

### OPEN_NONBLOCKING
长期设定暂未确定，但当前Scene可以用不定死Canon的保守方案继续。不得为了补齐表格询问用户。

### ASK_REQUIRED
只有同时满足以下条件才允许问用户：
1. 冲突会改变剧情事实、人物身份、长期世界机制或P0 Canon；
2. 当前Authority无法裁决；
3. 任何一个自动选择都会把一个不可逆的长期设定写死。

提问必须一次只问真正阻塞的高价值问题，并说明两个Authority冲突在哪里。

## 5｜Approval Gate例外

“少提问”不等于“自动批准”。

以下仍必须保留用户明确批准：
- Storyboard QC PASS → WAITING APPROVAL；
- Video QC PASS → WAITING APPROVAL；
- 需要用户正式确定的新Canon / 长期设计；
- 其他现有Approval Gate明确要求的正式批准。

不得用Decision Authority绕过Approval。

## 6｜表演决策

当小说只写“她害怕 / 他犹豫 / 她装作没事”时：
- 这不是ASK_REQUIRED；
- Skill先根据人物性格、关系、上下文推导Objective / Obstacle / Tactic / Stimulus，再推导Suppression、Intensity与具体Visible Signals；
- 结果标记为当前Scene的`DERIVED PERFORMANCE`，不是永久角色Canon；
- 不得只把抽象情绪词原样交给模型。

## 7｜战斗决策

当小说只写“角色挡下攻击 / 双方交战 / 保护某人”时：
- Story事实与Victory Condition保持不变；
- 距离、脚步、出手线路、格挡方式、Counter Window、Recovery由Combat Engine自动推导；
- Execution Consequence可自动推导；
- 新技能、新寿命代价、新圣约副作用、新伤势等Lore Cost不得擅自创造。

## 8｜QC

若Skill提出问题，先检查：
- 这个问题能否从现有Authority回答？
- 是否只是导演执行选择？
- 是否只是为了填满模板？
- 是否可以标`DERIVED`或`OPEN_NONBLOCKING`继续？

前三项任一为“是”，原则上不应询问用户。


## Wardrobe Source / Body Authority补充
服装冲突时优先级：用户最新明确要求/Approved Visual Canon → 真正`WARDROBE_PLOT_FACT` → Current Approved LOOK/Closet/World State → Stage 02 Costume Dramaturgy → Stage 03 Skill Wardrobe + Body Identity/Presentation → Signature/Descriptive Cue。普通小说服装描述不得覆盖Skill正式美术。Body Identity高于当前Garment Fit；当前LOOK只能选择呈现策略，不能改写人体Canon。

## Current｜Director Judge Authority（导演裁决权限）

Stage 02艺术选择的最终Owner是Director Judge，不是资产系统、Reference Resolver、Previs Router或Video模型。

- Actor / Cinematographer / Editor提供Critique，不按多数票自动决定；
- Production / AI feasibility只能在Selected Plan之后提出Execution Conflict；
- Reference槽位不足、已有资产不方便、某模型更擅长某类镜头，都不是自动改变POV / Reveal / Blocking / Reaction / Cut的权限；
- 若所有无损执行方案都失败，必须输出`AI_EXECUTION_CONSTRAINT_CONFLICT`并让Director Judge显式选妥协；
- 生产层静默把D2方案改成常规Wide/Medium/Reverse Coverage = `AI_CONSTRAINT_BACKDRIVE_FAIL`。

用户最新明确导演要求永远高于Skill自选；用户未指定时，Director Judge依据Audience Effect + Character Truth + Visual Logic + Sequence Logic自动裁决，不为普通导演选择反问用户。

## Current｜Director/Canon Conflict ≠ Prompt Constraint Conflict
本文件处理Story/Canon/Director Authority冲突；Final Video执行层的Camera ON/OFF、Audio父子类别、Reference Binding职责、State Order、Scope等互斥，统一交`prompt_constraint_solver.md`。不得因为“Director已经裁决”就假设最终Prompt内部自动无冲突。
