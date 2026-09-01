# Runtime Efficiency System｜V4.3 Runtime Compilation Authority

> **用途：** 定义Source Authority如何编译为小型Runtime Capsule，以及何时必须失效回源。本文件不再重复业务Gate、Candidate数量、Web QC或Stage Transition。

## 1｜Authority > Runtime > Prompt

固定优先级：

`SOURCE AUTHORITY / APPROVED EVIDENCE → RUNTIME CAPSULE → TASK RESOLVED STATE → FINAL PROMPT`

Runtime不是自由摘要，不能创建Source中不存在的新Canon/导演决定/平台能力。

## 2｜Runtime标准元数据

所有Runtime至少包含：

```yaml
runtime_type: DIRECTOR_RUNTIME
schema_version: 1
skill_version: CURRENT_SKILL_VERSION
scope:
  episode_id: EP01
  scene_id: SC03
source_versions: {}
source_fingerprints: {}
runtime_fingerprint: "..."
status: VALID
compiled_at: "..."
invalidation_triggers: []
```

正式Schema：`runtime/*.schema.yaml`。

## 3｜十一种Runtime

### STORY_RUNTIME
Screenplay Lock、Story/Canon边界、Scene facts、不可改写的故事事实。

### DIRECTOR_RUNTIME
Director Judge结果、Sequence Arc、Directorial Invariants、Detailed Shot Contract、Camera/Blocking/Spatial设计、Director→AI Boundary。

### ASSET_RUNTIME
当前任务真正需要的Character/Transformation/Environment/Prop/Support/Assembly身份与版本，不携带无关角色理论全文。

### SCENE_RUNTIME
World State、Scene Geography、Style/Color、常驻人物/道具、Continuity State与当前Segment Delta。

### SPATIAL_CANON_RUNTIME
Locked Location Topology / Floor Plan / Zone / Door-Window / Sightline / Access / Elevation / Event Node绑定；回答世界空间事实，不承担导演Shot选择。

### REALISM_RUNTIME
保存当前任务适用的Everyday Realism Contract：Environment/Architecture/Vehicle/Human Ergonomics/Object Affordance/Social-Spatial/Mundane Physics/Mundane Continuity要求、局部Exception Scope与Open P0/P1 Realism Failure。它不替代Spatial Canon，而是约束“这个空间与人物在现实中能否这样存在和使用”。

### REFERENCE_RUNTIME
Key Visible Assets、Field Coverage、Task-Bound Bindings、Fidelity Scope、Route/Slot状态、unresolved fields。

### VISUAL_EVIDENCE_RUNTIME
保存当前任务相关资产的Current Visual Evidence摘要：Evidence Ref、Source Fingerprint、Fact/Issue Codes、Safe/Unsafe Roles与Text-only可用性。它是视觉事实缓存，不创造Canon，也不替代多模态检查。

### VIDEO_CONDITIONING_RUNTIME
Approved Clean Storyboard之后的First/Target/Last/Key/Contact/Exit/Entry静态执行帧、Primary/Auxiliary角色、Pairwise Alignment与Readiness。

### VIDEO_RUNTIME
Typed Execution State、Spatial Execution State、Camera/Focus/Action/Performance/Crowd/Audio/Duration约束与Constraint Fingerprint。

### QC_RUNTIME
当前任务Open QC Dimensions、Readiness结果、Candidate/Retry/Salvage状态、平台QC Profile与Revision Scope。

## 4｜Normal Fast Path

若Route要求的Runtime全部满足：

- `status = VALID`
- `skill_version = Current Skill Version`
- Source version/fingerprint匹配
- Scope覆盖当前Episode/Scene/Shot/Task
- Required fields完整
- 无Open P0/P1 Conflict

则直接执行Route的`execute_with`，不全文回读`compile_runtime_from_source`。

## 5｜Automatic Source Fallback

出现任一条件，相关Runtime立即`STALE`并只回读当前Route声明的最小Source Set：

- Skill版本变化；
- Source Authority版本/fingerprint变化；
- Approved Asset/Storyboard/Director Core/Scene Color/Reference版本变化；
- 当前任务超出Runtime Scope；
- Required field缺失；
- Authority冲突或P0/P1 QC失败；
- 新角色/新Transformation/新Mechanic首次定义；
- 用户要求完整重新审查规则；
- `VIDEO_EXECUTION_STATE`、Camera、Audio、Reference、Critical Read、Action Set发生变化；
- Post-Compile Closure失败。

回源后执行Minimum Necessary Recompile，不默认重建所有Runtime。

## 6｜Runtime Fingerprint

推荐对Canonical YAML/JSON内容按稳定key排序后计算SHA-256。工具：`tools/state_fingerprint.py`。

Fingerprint用于证明“这张Runtime来自哪组Source状态”，不冒充真实媒体文件Hash。

## 7｜Hot State vs Ledger

用户说“继续”时默认读取Hot State：当前Episode/Scene/Segment/Shot、当前Workflow State、Pending Job、Next Action、必要Runtime refs、Previous Approved Ending Frame、Approval refs与当前Open failures。

历史QC、旧Take、旧Reference Snapshot、Archive记录、已关闭Revision维度进入Ledger，只有Change Impact、迁移、争议回查或依赖复核时读取。

## 8｜Runtime不得牺牲质量

Runtime优化只减少重复读取，不改变以下硬要求：

- Director Intelligence与Director Invariants；
- Spatial Canon、Everyday Realism & Plausibility与Mandatory Clean Shot Storyboard；
- Mandatory Video Conditioning；
- World/Character/Wardrobe/Prop Continuity；
- Action Feasibility与Natural Motion；
- Performance/Crowd/Combat因果；
- Reference Coverage与Fidelity；
- Style/Color Authority；
- Constraint-First Video与Post-Compile Closure；
- QC/Approval真实性。

判断优先级：**一次做对 > 少读几百行。**


## 9｜Stage 05 Prompt Completeness Restoration

Runtime Fast Path只能减少重复读取，不能减少Final Video的执行信息。Stage 05进入Compiler前至少确认：镜头目标、起始状态、人物/服装必要确认、Scene空间、Prop状态、构图/景别、Camera、Timeline、逐段动作、Performance、Eyeline、Limb Occupancy、Physics、Environment Dynamics、Lighting/Color、Sound、Dialogue/Visible Breath、Ending State、Residual Restrictions均已覆盖或明确N/A。

`PROMPT_LENGTH_CEILING = NONE`。Runtime模式不得因为“Reference已绑定”“Capsule已经摘要”“Semantic Dedup”或历史字数范围把完整执行稿压短。若平台存在已验证字符上限，保存完整Source Master并另做Target Adapter版本。

## Current｜Director Perception Runtime Projection

`DIRECTOR_RUNTIME`的Hot Projection应保留当前Sequence的：
- `perception_context.unresolved_state`
- `perception_context.relational_pressure`
- `shot_perception_contracts`
- 最近窗口的`shot_grammar_history`
- `creative_drift_telemetry`摘要

History只保存轻量Grammar签名，不保存完整Prompt/Storyboard正文。推荐窗口24–40镜，长期Ledger可保存更多但不默认载入Hot Runtime。

`SHOT_GRAMMAR_HISTORY`由Locked/Approved事实派生，不能创造新Authority；Telemetry只输出Warning。Runtime若缺少当前正式Shot的Perception Contract，视为字段覆盖不足，回读最小Director/Cinematography Source重建，而不是用旧镜头历史猜当前答案。
