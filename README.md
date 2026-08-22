# 断弦 AI Production Skill

**Production-grade AI 漫剧 / AI Video 制作工作流 Skill｜V4.5.7**

这是一个面向长流程 AI 漫剧与 AI 视频生产的可执行工作流系统。它不把“写 Prompt”当成生产完成，而是把**导演规划、资产生产、白描分镜、空间连续性、实体绑定、视频参考路由、生成任务和 QC**连接成可验证的状态机。

> 当前仓库以《断弦之歌》的生产需求为主要验证场景，但核心 Controller、Schema、Validator、Reference Resolver 与 Generation Spine 按可复用工作流设计。

## 核心能力

- **六阶段生产 Controller**：Narrative → Director / Editorial → Asset Build & Freeze → Storyboard → Video Conditioning → Video / Assembly。
- **Contact Sheet First 白描分镜**：多镜头 / 高动作密度场景优先一次生成 `4 / 6 / 9 / 12 / 16 / 25...` 白描宫格，再确定性切格进入后续流程。
- **匿名白描 + 实体绑定**：白描像素只保留匿名几何人物；`H_A / H_B / P_A / E_A...` 在离图 Metadata 中绑定真实 Character / Minor Human / Prop / Environment。
- **Base Visual Authority**：每个正式 Environment / Sub-location 都有空场景 Clean Master；每个清楚可见的配角 / 一次性功能人物都有独立 FMH / Minor Human Master。
- **资产多但不乱**：通过 `entity_id / location_entity_id + reuse_key + asset_family_id + version + lineage` 做去重、复用、升级和血缘追踪。
- **Spatial Canon + Multiview**：世界位置与画面位置分离；反打可以换 Screen Left/Right，但不能无依据改变 World Zone。环境和道具按实际摄影方向补 Visual Anchor / Canon View，而不是机械六视图。
- **Generation Envelope**：Formal Shot 与真实 Generation Call 分离，支持 `ONER / SEQUENTIAL_MULTISHOT / TIMED_MULTISHOT / FREESTYLE_BROLL`。
- **Minimum Sufficient Reference Pack**：Stage 03 可以拥有丰富资产库，Stage 05 只把当前镜头真正需要的最小 Reference Pack 发送给生成模型。
- **Entity Binding → Video Job 闭环**：Storyboard Slot、真实 Entity、Direct `@asset`、Final Video Prompt 和实际 Generation Job `required_bindings` 可机械追踪。
- **可执行 Validator / Regression**：关键 Gate 不是文档约定，而是由 Schema、Lint、Failure Router 和测试共同约束。

## 主链路

```text
Source Narrative
      ↓
Director / Editorial / Generation Envelope
      ↓
Base Visual Authority + Asset Build / Freeze
      ↓
4/6/9/12/16/25... White-line Contact Sheet
      ↓
Deterministic Panel Split
      ↓
Storyboard Entity Binding + Spatial / Action Metadata
      ↓
Shot Execution / Video Conditioning
      ↓
Reference Resolver → Minimum Sufficient @Assets
      ↓
VIDEO EXECUTION PLAN
      ↓
Final Video Prompt
      ↓
Generation Job → QC → Approved Take → Continuity Snapshot
```

## 白描和视觉资产为什么分开

白描负责证明**怎么拍**：构图、Blocking、Camera、Action Beat、Cut 与空间关系。人物和场景母图负责证明**到底长什么样**。

因此：

- 一次性配角也不会由视频模型现场随机发明外观；
- 一次性场景也不会因为没有空场景母图而随机漂移；
- 白描仍保持匿名，不与最终角色身份竞争；
- 视频阶段可以从完整资产库中只选当前镜头真正需要的最小 `@Reference` 集合。

## Contact Sheet First Storyboard

多镜头或复杂动作段落默认先生成整张白描 Contact Sheet，再切格：

```text
Scene / Sequence
      ↓
Storyboard Density Analysis
      ↓
4 / 6 / 9 / 12 / 16 / 25 / Custom
      ↓
White-line Contact Sheet
      ↓
Visual QC
      ↓
Deterministic Splitter
      ↓
Clean Panels
      ↓
Panel → Shot / Beat Mapping
      ↓
Entity Binding
```

两类宫格：

- `SHOT_GRID`：一格主要对应一个正式 Shot；
- `BEAT_GRID`：多个格可属于同一个 Shot，适合打斗、追逐、舞蹈、长镜头和复杂 Blocking。

**25 格不等于 25 个 CUT。** 它也可以表达一个复杂 Shot 中的 25 个动作 / Blocking 节点。

## Storyboard Entity Binding

白描像素匿名，但实体不匿名。

```text
Anonymous geometry
      ↓
H_A / H_B / P_A / E_A slots（仅 Metadata）
      ↓
STORYBOARD_ENTITY_BINDING_MAP
      ↓
Real Entity ID
      ↓
World Spatial State + Action State
      ↓
Reference Resolver
      ↓
Final Video Prompt / Generation Job
```

Slot ID 不画进白描，也不直接发送给模型。Stage 05 必须把它们反编译为真实人物 / 道具 / 场景的自然语言与必要 `@资产`。

## Base Visual Authority

当前 V4.5.7 的硬规则：

1. 每个被正式 Scene / Event / Shot 使用的 Location / Sub-location，`Tier S/A/B/C` 都必须有一张 Approved **空场景 Clean Master**；
2. 每个清楚可见的一次性配角 / 功能人物，都必须有一张 Approved **FMH / Minor Human Master**；
3. Storyboard、Shot Assembly、Rendered Previs 只能补关系 / 动作 / 姿态，不能替代 Base Master；
4. 真正不可辨认的 Deep Background Crowd 才允许 `TEXT_ONLY`；
5. `actor_authority_index` 会机械检查 Event Node 中的演员是否遗漏资产规划。

资产多本身不是问题。同一个 Entity 通过 `reuse_key / asset_family_id / version / lineage` 复用和升级，而不是每换一个镜头重新生成一套母图。

## 目录导航

| 目录 | 作用 |
| --- | --- |
| `controller/` | Workflow、Route、Authority、Gate、Failure Router |
| `state/` | 生产状态与结构化 Authority Schema |
| `runtime/` | Story / Director / Asset / Reference / Video Runtime Schema |
| `templates/` | 各阶段 Source Authority 与 Prompt / SOP |
| `tools/` | 确定性 Planner、Splitter、Resolver、Generation Job 工具 |
| `validators/` | Gate、Binding、Continuity、Asset、Prompt、Architecture 校验 |
| `adapters/` | Generation / Web QC 平台适配 |
| `tests/` | Smoke、Regression、Adversarial、V4.5.7 专项测试 |
| `docs/` | 架构升级说明与验证报告 |

## V4.5.7 当前重点

1. **Contact Sheet First Storyboard**：整张宫格先生成，QC 后确定性 Split；验证 Board 与创意 Contact Sheet 严格区分。
2. **Storyboard Entity Binding**：匿名白描不等于匿名实体，A/B/C Slot 必须绑定真实资产与世界空间状态。
3. **Base Visual Authority Hardening**：Tier C 一次性地点也有空场景 Master；清楚可见的一次性配角也有独立人物 Master。
4. **Adaptive Video Reference Budget**：资产库完整，但最终视频 Reference 仍采用最小充分集，避免 `@` 槽位机械堆满。
5. **Spatial Continuity & Multiview**：以 World Spatial State、Camera Projection、Motion Phase 和 Shot Boundary Contract 控制跨镜连续性。

## 验证状态

当前准备发布的 V4.5.7 源码已经通过以下重点专项 / 回归测试：

- Base Visual Authority
- Contact Sheet Storyboard
- Entity Binding → Video Closure
- Spatial / Multiview
- Generation Envelope
- Adaptive Video Reference Budget
- Director Perception
- Editorial
- Video Execution Plan
- Storyboard Hotfix
- Stage 05 Prompt Authority
- Prompt Restoration
- Combat Prompt
- Coverage Migration
- V4.5.7 Logic Closure

同时完成 YAML 解析、Python Compile、Gate Producer、YAML Duplicate Key 与 V4.5–V4.5.7 Architecture Lint 检查。

详细设计与验证记录见 `docs/`。

## License

当前仓库**尚未授予开源许可证**。除非仓库后续明确加入 License，否则请不要假定代码、模板或工作流可以被复制、修改或再发布。
