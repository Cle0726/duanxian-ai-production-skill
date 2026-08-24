# 断弦 AI Production Skill

**Production-grade AI 漫剧 / AI Video 制作工作流 Skill｜V4.5.7**

这是一个面向长流程 AI 漫剧与 AI 视频生产的可执行工作流系统。它不把“写 Prompt”当成生产完成，而是把导演规划、资产生产、白描分镜、空间连续性、实体绑定、声音表演、视频参考路由、生成任务和 QC 连接成可验证的状态机。

> 当前仓库以《断弦之歌》的生产需求为主要验证场景，但核心 Controller、Schema、Validator、Reference Resolver、Voice Direction 与 Generation Spine 按可复用工作流设计。

## 核心能力

- **六阶段生产 Controller**：Narrative → Director / Editorial → Asset Build & Freeze → Storyboard → Video Conditioning / Video → Post / Voice / Master。
- **Contact Sheet First 白描分镜**：多镜头 / 高动作密度场景优先一次生成 `4 / 6 / 9 / 12 / 16 / 25...` 白描宫格，再确定性切格进入后续流程。
- **匿名白描 + 实体绑定**：白描像素只保留匿名几何人物；`H_A / H_B / P_A / E_A...` 在离图 Metadata 中绑定真实 Character / Minor Human / Prop / Environment。
- **Base Visual Authority**：每个正式 Environment / Sub-location 都有空场景 Clean Master；每个清楚可见的配角 / 一次性功能人物都有独立 FMH / Minor Human Master。
- **资产多但不乱**：通过 `entity_id / location_entity_id + reuse_key + asset_family_id + version + lineage` 去重、复用、升级和追踪血缘。
- **Spatial Canon + Multiview**：世界位置与画面位置分离；反打可以改变 Screen Left/Right，但不能无依据改变 World Zone。
- **Generation Envelope**：Formal Shot 与真实 Generation Call 分离，支持 `ONER / SEQUENTIAL_MULTISHOT / TIMED_MULTISHOT / FREESTYLE_BROLL`。
- **Minimum Sufficient Reference Pack**：Stage 03 可以拥有丰富资产库，Stage 05 只把当前镜头真正需要的最小 Reference Pack 发送给生成模型。
- **Entity Binding → Video Job 闭环**：Storyboard Slot、真实 Entity、Direct `@asset`、Final Video Prompt 和实际 Generation Job `required_bindings` 可机械追踪。
- **Voice Direction / Prosody 闭环**：重要 Dialogue / VO 使用结构化 `VOICE_DIRECTION_PLAN` 控制 Trigger / Meaning / Objective / Tactic / Subtext，以及 Loudness / Pace / Pause / Stress / Pitch-Energy / Terminal Intonation；Stage 05 生成并验证 `VOICE_PROMPT_HANDOFF`，Stage 06 基于 Picture Lock 生成 `VOICE_TTS_HANDOFF`。
- **可执行 Validator / Regression**：关键 Gate 不是文档约定，而是由 Schema、Lint、Failure Router、状态机和测试共同约束。

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
VOICE_DIRECTION_PLAN + VIDEO EXECUTION PLAN
      ↓
Final Video Prompt + VOICE_PROMPT_HANDOFF
      ↓
Generation Job → QC → Approved Take
      ↓
Picture Lock → VOICE_TTS_HANDOFF → Master
```

## Contact Sheet First Storyboard

多镜头或复杂动作段落默认先生成整张白描 Contact Sheet，再切格。

- `SHOT_GRID`：一格主要对应一个正式 Shot；
- `BEAT_GRID`：多个格可属于同一个 Shot，适合打斗、追逐、舞蹈、长镜头和复杂 Blocking。

**25 格不等于 25 个 CUT。** 它也可以表达一个复杂 Shot 中的 25 个动作 / Blocking 节点。

白描像素必须匿名，但实体不匿名：A/B/C 等 Slot 只存在于离图 Metadata，随后绑定真实人物 / 道具 / 场景资产并进入 Stage 05。

## Base Visual Authority

当前 V4.5.7 的硬规则：

1. 每个被正式 Scene / Event / Shot 使用的 Location / Sub-location，`Tier S/A/B/C` 都必须有一张 Approved **空场景 Clean Master**；
2. 每个清楚可见的一次性配角 / 功能人物，都必须有一张 Approved **FMH / Minor Human Master**；
3. Storyboard、Shot Assembly、Rendered Previs 只能补关系 / 动作 / 姿态，不能替代 Base Master；
4. 真正不可辨认的 Deep Background Crowd 才允许 `TEXT_ONLY`；
5. 同一 Entity 通过 `reuse_key / asset_family_id / version / lineage` 复用，不因换 Shot 重做母图。

## Voice Direction & Prosody

声音系统明确分离：

```text
Voice Identity
≠ Current Emotion
≠ Prosody
≠ Mix Loudness
```

重要对白会结构化记录：

- Trigger Event / Meaning Appraisal；
- Objective / Tactic / Subtext；
- Affect / Arousal / Control；
- Performance Loudness；
- Pace Curve；
- Pause Map；
- Stress / De-emphasis；
- Pitch / Energy Contour；
- Terminal Intonation；
- Texture Adjustment；
- Interrupt / Overlap / Listening；
- Body ↔ Voice Coupling；
- Landing / Carryover。

Stage 05 必须证明这些关键控制真正进入 Final Video Prompt；Stage 06 只允许基于 Picture Lock 调整真实时间，不允许静默修改已批准的 Voice Identity、句尾走势或表演意图。无对白单元也显式生成 `NOT_REQUIRED` Handoff，不能靠“缺文件”猜是否适用。

## 目录导航

| 目录 | 作用 |
| --- | --- |
| `controller/` | Workflow、Route、Authority、Gate、Failure Router |
| `state/` | 生产状态与结构化 Authority Schema |
| `runtime/` | Story / Director / Asset / Reference / Video Runtime Schema |
| `templates/` | 各阶段 Source Authority 与 Prompt / SOP |
| `tools/` | 确定性 Planner、Splitter、Resolver、Compiler、Generation Job 工具 |
| `validators/` | Gate、Binding、Continuity、Asset、Prompt、Voice、Architecture 校验 |
| `adapters/` | Generation / Web QC 平台适配 |
| `tests/` | Smoke、Regression、Adversarial、V4.5.7 专项测试 |
| `docs/` | 架构升级说明与验证报告 |

## Final Audit｜2026-08-24

最终 Voice Direction 逻辑闭环后进行了全仓库审计。

- 35 个 `tests/run_*.py` 回归程序最终均通过；
- `run_v457_integrity_tests.py` 完整 PASS；
- `run_v457_logic_closure_tests.py` 完整 PASS；
- Voice Direction normal + adversarial closure PASS；
- YAML：137 个，解析错误 0；
- Python：125 个，语法错误 0；
- State/Runtime Schema：44 个，Draft 2020-12 Meta Schema 错误 0；
- `v457_architecture_lint`：`errors=[] / warnings=[]`；
- Gate Producer：PASS；
- YAML Duplicate Key：PASS；
- `__pycache__ / *.pyc / *.pyo`：0；
- 常见 Secret / API Key 模式扫描：0 命中。

本轮审计还修复了 Voice Plan 覆盖绕过、`dialogue_required=false` 绕过、多 Pause/Stress 丢失、Stage 06 背景台词静默跳过、Picture Lock Fingerprint 缺失、Voice Handoff Fingerprint 验真、Ghost Gate Producer、Prompt Artifact Voice 防绕过等问题。

在当前 deterministic / schema / static / regression 覆盖范围内，没有已知阻断性逻辑断链。模型 / Provider 生成误差继续交由现有 QC / Retry / Failure Router 处理。

## License

当前仓库**尚未授予开源许可证**。除非仓库后续明确加入 License，否则请不要假定代码、模板或工作流可以被复制、修改或再发布。
