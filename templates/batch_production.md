# Batch Production（批量生产）

> **目标：** 对一人制片真正适合并行的工作批量处理，但不破坏 `Episode Asset Pack First`、连续性和Approval Gate。

## 1. Episode Asset Batch（整集资产批量）

Stage 02达到`DIRECTOR BREAKDOWN READY`后，先完成适用Location的`SPATIAL_CANON` Build/QC/Approval，再根据 `Final Episode Asset Requirement Manifest` 扫描整个Episode。Environment在进入视觉Batch前必须已有Locked Spatial Canon；Environment / Prop随后完成`Shot Coverage Matrix`，把Canonical Master与真实Shot触发的Coverage分开：

- `REUSE`：已有且适用的APPROVED Character / Environment / Prop / Weapon / Transformation资产；
- `COVERAGE TO BUILD`：仅Environment / Prop使用；必须有Parent Master + Triggered Shot(s)，不得作为“顺手多做几个视角”的批量理由；
- `SUPPORT REF TO BUILD`：Stage 02 Video Risk Matrix明确Required、Owner Stage=03的Interaction / Contact / Transient State / Entity Action高清辅助参考；
- `SHOT ASSEMBLY TO BUILD`：Stage 02 Shot Assembly Need Analysis明确Required的多人关系 / 人景物组合 / Montage情境高清组装资产；
- `TO BUILD`：本集确实缺失的正式资产；
- `PERSISTENT STATE`：必要持久状态变体；
- `EXCLUDED`：Storyboard / Ending Frame / Video Take / 临时测试图。

Stage 03对**互不依赖的普通正式资产默认组成Asset Batch Packet**：建议每批3–6个Asset Prompt Job一次交付。每个Job同时携带`Image Candidate Policy / Planned Candidate Count`：Design-bearing Master默认2、高风险可4、Environment / Prop Coverage、Functional Minor Human、Stage 03 Production Support、Performance Support、Narrative FX Reference与Shot Assembly默认2。这里“3–6个”指不同Job数量，不是每个Job只生成1张。场景/道具遵守依赖顺序：**Canon Master先APPROVED，Derived Coverage才能进入后续Batch**；FMH必须已有Stage 02 `SCOPED_CAST_BRIEF`；Production Support与Shot Assembly也必须等其必要Parent Authorities可用后再生成；Shot Assembly中的反复/命名人物必须已有Character Authority，一次性`SCOPED_CAST / NON_RECURRING`必须已有Stage 02 Scoped Cast Brief与Visual Owner。不能把同一对象未批准的Master和多个猜测视角同时批量抽卡。用户生成后若交给网页版多模态模型做Batch QC，必须另按`web_multimodal_qc_upload_budget.md`执行Evidence Packing：**单个Web QC Batch全部图片合计不得超过`platform_profile.image_upload_cap`（当前Profile=10）**，超过自动拆B01/B02；Prompt生产批次大小不等于Web QC上传批次大小。Skill执行Batch Intake / Batch QC，只返工失败项；但每个资产仍必须经过QC + 用户批准。只有真实APPROVED资产计入Episode Asset Freeze Gate。

以下不强行批量：首次圣谱者核心变身设计、存在明显前后依赖的TE/TF/TC/WP链、必须先看前一结果才能决定后续结构的资产、用户明确要求逐个制作。批量减少交互次数，不压缩单个Prompt。

**Production Mode在整集状态到达 `EPISODE ASSET FROZEN` 前，不开始正式Storyboard。**

## 2. Storyboard Batch（资产冻结后的分镜批量）

Episode Asset Pack冻结后才允许批量Storyboard。Storyboard批量只生成`WHITE_LINE_STORYBOARD_ONLY`独立白描Clean Panels；Sequence Board只由这些Panel用确定性工具后拼，不批量生成带字/箭头页面。批量审批仍按“全部Panel到`QC_PASS_WAITING_APPROVAL` → 拼Review Board → 用户批准一次Storyboard Set → Approval Record锁定Mandatory Panel IDs/Fingerprints → 批量Promotion”执行。Camera/Timing/Cut/Action/Performance等离图说明必须正规化进`storyboard_handoff`并逐项进入对应Final Video Prompt。

适合批量：
- `CUT_ENTRY`；
- `SCENE_OPENING`；
- 已经具备所需真实Previous Ending Frame的`CONTINUITY_ENTRY`；
- 多个Segment彼此没有未满足的连续性依赖。

不适合提前批量：
- `CONTINUITY_ENTRY`但上一Segment真实APPROVED VIDEO Ending Frame尚未产生。

这种Segment进入：

`WAITING PREVIOUS ENDING FRAME`

等真实Ending Frame出现后，再由Reference Resolver从冻结Episode Asset Pack + 真实尾帧生成本段Storyboard Reference Pack。

**正式连续性锚点仅使用上一段真实APPROVED Video Ending Frame。**

用户批量上传多个Storyboard后，可以做Batch Storyboard QC，只返工失败项；若使用网页版多模态Verifier，每个QC Batch总图片数必须`<=10`，共享Style/Environment等Authority在同一Batch只占1次，跨Batch需要时重新上传并重新编号。QC PASS与APPROVED仍然分开。

## 3. Candidate Batch（图片计划候选 / Video已有候选比较）

Stage 03图片多候选是正式默认能力，读取`image_candidate_strategy.md`；同一个图片资产按计划生成2–4张时，应视为同一Candidate Group并先Fast Triage。Clean Storyboard Panel普通1个候选、复杂可2个候选。Video则不因为存在Candidate Triage模块而预先多Take。

同一个图片资产或Storyboard的**计划Candidate Group**可以批量比较；用户额外生成的同Job候选也可并入Intake，但不得因此无限扩组。“本地已收到很多候选”不等于“网页版一次全传”。网页版QC先按10图硬上限自动拆包，尽量保持同一Asset的候选比较组完整。

正式Video不因为“批量”自动多Take：

**1 FINAL VIDEO PROMPT → 默认从1 Video Take起步。**

T1/T2保持单Take经济；T3/T4只有在上游Gate通过且Failure-before-Compute证明随机性为主因时才允许受限候选预算。多个Take存在时再做Best Take Selection。

## 4. Video保持连续顺序

Video不能为了批量而无视Ending Frame依赖。

默认：

`SEG01 Clean Storyboard → Video Conditioning → Video → QC → APPROVED VIDEO → Ending Frame → SEG02 Storyboard（若CONTINUITY_ENTRY） → Video Conditioning → Video`

`CUT_ENTRY / SCENE_OPENING`的Storyboard可以在资产冻结后提前完成，但Video仍按导演计划和实际依赖推进。

## 5. Episode Queue建议

```text
Episode Asset Manifest：READY
Episode Asset Pack：BUILD / FREEZE PENDING / FROZEN / FREEZE BROKEN
Asset Build Queue：...
Asset Approval Pending：...

Storyboard Ready Queue：只列已满足Entry Mode输入的Segment
Waiting Ending Frame Queue：仅CONTINUITY_ENTRY
Storyboard Failed Queue：只列需返工项
Video Conditioning Queue：只列Approved Previs且Required Frame Roles未完成的Video Unit
Video Queue：只列VIDEO_CONDITIONING_READY并按真实依赖排序
```

## 目标

- 先一次性看清本集要做哪些正式资产；
- 避免做到后面才反复发现缺母图；
- 不让Storyboard承担补人物/场景/道具设定的职责；
- 不用假尾帧提前做连续分镜；
- 视频继续执行Adaptive Take Budget：普通镜头从1 Take起步，不因批量而自动多Take；T3/T4额外候选仍需Failure-before-Compute。

## V4.5.4｜Multi-Scene Required View Batch Queue

批量场景资产生成前先跨Scene运行`view_coverage_planner.py`。批次按`P0/P1 MISSING → P2/P3 MISSING → 已覆盖方向的必要额外Candidate`排序。不同Scene可同批，但每个Job必须绑定唯一`view_requirement_id`；禁止因为某一场景好生成就连续堆相似角度，而让其它Scene关键方向一直为空。

## V4.5.5｜Batch Realism Stop Gate

批量场景/多视角生产按`Coverage Debt + Realism Debt`双队列执行。某Location一旦出现可重复的功能布局/人物落位P0错误，立即停止该Location后续批量派生，先修Realism/Spatial Owner；禁止把同一个错误Set扩散到更多视角。
