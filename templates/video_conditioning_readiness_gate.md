# Video Conditioning Readiness Gate｜V4.4

> **用途：** 在Stage 05前确认每个Video Unit已经拥有合格的Primary Visual Conditioning；辅助Reference可以继续参与，但不能替代Primary Visual。

```text
VIDEO CONDITIONING READINESS
Approved Storyboard: PRESENT
Video Unit Plan: COMPLETE
Primary Visual Coverage: PASS
Primary Visual Asset Status: APPROVED
Direct Video Eligibility: PASS
Shot Contract Fidelity: PASS
Current World State Projection: PASS
Visible Entity Exactness: PASS
Character / Wardrobe / Injury / Prop State: PASS / N/A
Environment Geometry / Zone / Camera Side: PASS
Frame Cleanliness: PASS
Multi-panel / Caption / Arrow Contamination: NONE
Auxiliary Reference Role Scope: PASS
Time-scoped Reference Isolation: PASS
Cut Decomposition / Multi-shot Capability: RESOLVED / N/A
STATUS: VIDEO_CONDITIONING_READY / BLOCKED
```

## 1｜Primary Visual Coverage
每个`video_unit_id`至少一个Approved Primary Visual：
- SIMPLE → FIRST/EXECUTION FRAME；
- 有明确落点 → FIRST + TARGET/LAST；
- Contact/Combat/Transformation → 按`video_conditioning_asset_architecture.md`增加关键节点。

只存在Environment Master + Color Board + Design Board + Whole Storyboard时：

`PRIMARY_VISUAL_CONDITIONING_GAP = FAIL`

即使这些辅助Reference全部Approved，也不能宣布Video Ready。

## 2｜Promotion
若StoryBoard Panel、Coverage或Shot Assembly已经等于最终Video入口，可以Promotion，但必须记录：
- source asset；
- current shot/video unit；
- current state fingerprint；
- promotion QC；
- approval record。

未经Promotion，不因“高清/Approved/看起来够用”自动取得Primary权限。

## 3｜Frame Cleanliness Hard Fail
- 宫格/拼版作为Primary；
- 文字/箭头/时间码/说明框进入Primary；
- 未授权人物/群众；
- 当前剧情临时状态错；
- Camera/Blocking与Approved Storyboard不一致；
- 角色/服装/伤势/道具状态错。

## 4｜Cut
跨空间Hard Cut默认拆Video Unit。若保留单Job：每个Sub-unit必须独立Primary Visual + time scope；Reference不得跨Cut无界生效。

## 5｜输出
PASS时写入：
- `VIDEO_CONDITIONING_READY`
- Conditioning Runtime fingerprint
- Primary Visual asset IDs / fingerprints
- Approval refs

任何Primary Visual变化都会使`VIDEO_RUNTIME`和旧Final Prompt变为STALE。

## V4.5｜Relation Readiness

除V4.4的单Video Unit Primary Visual检查外，还必须读取`SHOT_RELATION_GRAPH + VISUAL_ASSET_OBLIGATION`：
- 所有`fulfill_by=STAGE_04_VIDEO_CONDITIONING_QC`的Required Obligation已FULFILLED或有真实Waiver；
- 需要Exit/Entry Pair的Relation存在成对Primary Visual；
- `boundary_pairs[].alignment_status = PASS`；
- A端Attention Target与B端Reveal对象一致；
- 关系型辅助资产（Clue View / Location Identity / Sightline）没有被错误省略。

否则`VIDEO_CONDITIONING_READY = BLOCKED`。


## V4.5.2 Strategy Closure
`qc_status=PASS`不是Frame证据。进入READY前必须机械检查Strategy Required Roles：FIRST_TARGET=FIRST+TARGET；FIRST_LAST=FIRST+LAST；CONTACT_CHAIN=FIRST+CONTACT；TRANSFORMATION_CHAIN=FIRST+KEY+AFTER；KEY_POSE_CHAIN=FIRST+至少1 KEY；CUT Pair两端必须真实绑定对应Obligation/Registry资产。缺失统一报`CONDITIONING_STRATEGY_FRAME_GAP`或`CUT_PAIR_*`。

## V4.5.7｜Identity Readability at Platform Scale

Primary Visual通过普通Static QC后，还不能自动取得“人物身份已锁定”结论。对当前Shot里清楚入镜/身份关键的命名人物，必须运行`identity_readability_gate.md`：把Primary Visual按目标平台实际有效尺度检查。

- `PLATFORM_ACTUAL_SCALE / PLATFORM_PROFILE_SIMULATION`才是有效依据；原图分辨率、文件MB大小不算；
- 任一Required人物`FAIL / UNKNOWN` → `IDENTITY_READABILITY_FAIL`；
- FAIL后Primary Visual可以继续控制构图/Blocking，但不得成为该人物唯一Identity Authority；
- 必须Direct Bind对应Approved人物母图/Current Look/FMH Master，或重新生成可读的Primary Visual并重新评估；
- 白描Storyboard与Environment Master都不能补人物身份。

`IDENTITY_READABILITY_PASS`是`VIDEO_CONDITIONING_READY`的硬门之一。
