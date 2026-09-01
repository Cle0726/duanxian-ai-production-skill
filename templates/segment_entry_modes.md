# Segment Entry Modes（视频段落入场模式）

> **用途：** 解决“并不是每个Segment都需要上一段视频尾帧”的问题。Stage 02在Segment Plan阶段先决定Entry Mode，Stage 04/05按该模式选择连续性输入。**Entry Mode只控制图像连续性输入，不代表World State是否继承；世界状态统一服从`world_state_continuity_engine.md`。**

## 1｜三种正式模式

### A. `CONTINUITY_ENTRY`｜连续接入
用于同一时间、同一空间、动作/表演直接延续的相邻Segment。

必须：
- 使用上一段**最终实际采用输出**的真实Ending Frame作为Continuity Authority；来源可以是`APPROVED VIDEO`，或已进入最终剪辑且明确作为上一Segment收尾的`APPROVED_SALVAGE_CLIP`；`SALVAGE_CANDIDATE`本身不具备此Authority；
- 读取上一段 `Continuity Snapshot`；
- 新Segment第一时刻继承人物站位、左右、朝向、轴线、姿态、重心、视线、关键道具状态。

Ending Frame只负责连续性，不负责成片画质；画质职责继续服从 `render_quality_authority.md`。

### B. `CUT_ENTRY`｜明确切入
用于Segment边界本身就是一个明确编辑切点：例如同Scene内直接硬切到另一个景别、视角、人物或插入镜头，且不要求新Segment首帧复制上一Segment尾帧构图。

默认：
- **不把Previous Ending Frame作为图像输入**；
- 通过已批准Storyboard、Shot/CUT关系、必要文字连续性说明完成切入；
- 仍需继承剧情上必须连续的P0状态，例如服装、伤势、道具是否在手、人物是否已经起身；伤势若已在合法Transformation Completion被修复，则继承Post-Recovery Injury State。

若某个Match Cut确实需要上一段具体形状/动作作为匹配源，Reference Resolver可把上一尾帧提升为`CONDITIONAL`，但不得默认加入。

### C. `SCENE_OPENING`｜Scene / Episode开场
用于：
- Episode第一段；
- 新Scene；
- 明确时间跳跃；
- 明确地点切换；
- 蒙太奇新单元；
- 不需要上一段视觉连续性的独立开场。

规则：
- `Previous-Segment Ending Frame = NOT REQUIRED`；
- 首帧由Approved Storyboard + 当前必要Approved HD Object Authorities定义；
- 不为了“工作流统一”强行附加上一Scene尾帧；
- **SCENE_OPENING ≠ World State Reset**：Prop去向、伤势/疲劳、湿度/污渍、变身状态、Knowledge、关系/Objective、世界级声音/环境规则以及已发生的剧情事实仍从World State Ledger继承。若Ledger已有`TRANSFORMATION_RECOVERY=RECOVERED`，不得从更早帧重新继承旧伤。

## 2｜Entry Mode判定

Stage 02 / Segment Planner按以下顺序判断：
1. 是否Episode/Scene新开场、时间或地点明确跳变？→ `SCENE_OPENING`；
2. 是否设计为明确CUT，首帧不需要复制上一段构图/姿态？→ `CUT_ENTRY`；
3. 是否动作/表演直接续接？→ `CONTINUITY_ENTRY`。

如果剧情状态连续但画面明确CUT，使用`CUT_ENTRY`，并用World State Delta + 必要文字继承P0状态，不自动绑定上一尾帧。

如果Scene/地点变化前后存在`VISIBLE_BRIDGE / RESIDUAL_BRIDGE`，该Bridge必须已经在Stage 02作为Transition Beat规划完成；不要把`SCENE_OPENING`当作允许跳过Arrival / Entry / Prop去向的理由。

## 3｜对Stage 04/05的影响

- `CONTINUITY_ENTRY`：Storyboard / Video Reference Pack中加入Previous Ending Frame；
- `CUT_ENTRY`：默认不加入；只在Match Cut等真实视觉匹配需要时按条件加入；
- `SCENE_OPENING`：禁止把上一Scene尾帧当默认输入。

所有Prompt都必须显式写出：`Entry Mode = ...`。
