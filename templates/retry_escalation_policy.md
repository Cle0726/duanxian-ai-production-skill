# Retry / Escalation Policy（自动返工与升级处理）

> **用途：** 在一人制片预算下，优先通过“当前QC结果 → 找出真正问题 → 最小修改”提高下一次成功率，而不是靠无上限多Take碰运气。默认QC执行端为WEB_EXTERNAL_VERIFIER；只有用户主动要求时才是LOCAL_SELF_CHECK。与 `personal_creator_cost_efficiency_engine.md` 的Shot Investment Tier共同决定额外Take预算。

## Adaptive Take Budget总原则

**1 FINAL VIDEO PROMPT = 默认从1个Video Take起步。**

- T1/T2不预先生成双Take/多Take；T3/T4也先从1 Take开始，只有Static/Storyboard Gate已通过且Failure Diagnosis证明模型随机性成为主要瓶颈时才启用受限候选预算；
- 每次新结果都必须由当前QC执行端完整观看并完成Video QC；默认由网页版执行，本地不重复观看；
- 能Trim / Post小修解决就不重生；
- 有明确Prompt、动作、Camera、CUT、Reference问题时，先诊断再最小修改Prompt，然后只生成1个新Take；
- T1/T2只有结果已经非常接近目标、Prompt结构基本正确、剩余问题高度疑似模型随机波动时，才可以**可选建议**使用完全相同Prompt再生成1次；
- T3/T4在满足上述条件时可以进入受限候选预算，通常总Take不超过3–4；每一次新增Take前仍先做Failure-before-Compute；
- 候选预算不是Gate要求，也不得自动用满。

## 成本优先梯度

**Temporal Salvage / Post / Trim → Diagnose → Residual-Only Fix/Generation → Optional Exact Retry / Limited Candidate Budget（仅近似随机）→ Reference Simplification → Re-plan / Split**

### Level 0｜Temporal Salvage / Post / Trim First

任何非PASS或局部失败Take先读取`video_temporal_salvage_qc.md`。如果已有`CLEAN_KEEP / CONDITIONAL_KEEP / HANDLE_ONLY`，先保留这些真实Source Windows；若只存在末尾少量畸形可裁掉、一帧闪烁、轻微停顿/音效问题、画面可用但音频需替换等，优先Stage 06解决，不重生已成功画面。只有失败区间无法独立补足、或Director明确要求不可切Long Take时，才允许考虑整Take重生。

### Level 1｜Diagnose First（先看完整视频再判断）

Video QC不通过后先执行 `Failure Diagnosis`。先区分：
- Prompt/动作路径问题；
- Camera / CUT / Timing问题；
- Reference职责/过载问题；
- Identity / Prop / Space问题；
- 真正的Random Generation Failure。

不得因为“这次不够好”就默认再抽一个Take。

### Level 2｜Local Prompt Fix（局部修Prompt）

如果问题有明确可描述原因，只修改故障模块，例如：
- ACTION / PHYSICS → 动作路径、重心、接触；
- CAMERA → 运镜与机位；
- PROP DRIFT → 道具结构/比例/接触；
- CUT / TIMING → 时间轴与切点；
- PERFORMANCE → 眼神、呼吸、身体表演；
- AUDIO BOUNDARY → NO AUTO BGM / 声音边界。

修改后只生成 **1个新Take**，再完整QC。不要一次要求多个候选。

### Level 3｜Optional Exact Retry（可选同Prompt再试1次）

只在以下条件同时成立时允许推荐：
1. 当前结果已经非常接近通过；
2. Prompt / Reference / Shot结构没有明确设计错误；
3. 剩余问题属于偶发手部、短暂局部变形、单次随机执行偏差等；
4. 再试一次比修改Prompt更可能省时间；
5. 用户预算允许。

输出必须写成“**可选建议：同一Prompt再试1次**”，不能写成“下一步必须再生成一个Take”。

同一Prompt最多建议额外重试 **1次**。如果仍出现同类问题，停止抽随机，回到Diagnosis / Local Prompt Fix。

### Level 4｜Reference Simplification

若故障表现为混脸、混服装、空间冲突或职责污染：
- 重新运行Reference Resolver；
- 删除无职责参考图；
- 检查DEPRECATED或错误版本资产是否混入；
- 不靠继续增加参考图解决Reference Overload。

### Level 5｜Segment Re-plan / Split

如果复杂动作或多镜头结构在局部修正后仍稳定失败，回Segment Planner重新规划，必要时拆Segment，而不是继续付费抽Take。

## Stop Rule（停止规则）

- 不允许全片默认双Take；
- 不允许“每次都同Prompt再生成一次看看”；
- T1/T2同Prompt可选重试1次后仍失败 → 必须诊断/改Prompt；T3/T4若启用候选预算，总Take达到当前预算上限仍无合格结果 → 必须停止抽随机并重新诊断/拆段；
- 局部修正后仍稳定失败 → 检查Reference / Segment结构；
- 高复杂度持续失败 → 优先拆Segment。

用户明确要求继续尝试随机结果时除外。

## Continuity Priority停止条件

如果唯一问题被判断为P2连续性差异，不进入重生；直接保留当前结果。P1只有在造成明显跳变时才进入局部处理，避免为微小差异消耗生成次数。
