# Video Generation Readiness Gate（视频生成技术就绪）｜V4.4

> **用途：** 这是Stage 05入口技术Gate。它不再只问“Reference够不够”，还必须证明每个Video Unit已经拥有Approved Primary Visual Conditioning。

```text
VIDEO GENERATION READINESS
Director Invariants: PASS
Mandatory Shot Storyboard Coverage: PASS
Approved Mandatory Shot Storyboard: PRESENT
Generation Envelope: VALID
Multi-shot White-line Storyboard Grid Gate: PASS / NOT_REQUIRED
Video Conditioning Runtime: VALID
Video Conditioning Readiness: PASS
Primary Visual Coverage: PASS
Direct Video Eligibility: PASS
Auxiliary Reference Role Scope: PASS
Reference Content-Role: PASS
Reference Route / Capability: PASS
Typed Execution State: PASS
Video Execution Plan: FROZEN_FOR_COMPILE / PASS
Prompt Conflict Preflight: Hard Conflict = 0
Spatial Execution State: COMPLETE / N/A
Action / Natural Motion: PASS
Cinematography / Camera / Focus / Audio State: PASS
Shot Proof Capacity: PASS
Motion / Instruction Load: PASS or ACCEPTABLE_WITH_PROOF
Supplemental Previs Required Risks: PROVEN / N/A
Generation/QC Separation: PASS
Style Control: VISUAL_BOUND or TEXT_FULL_PASS
Color Control: PASS
Reference Literalization Risk: ACCEPTABLE / ROUTED
Stale Prompt: NO
Prompt Surface / Egress: PASS
STATUS: VIDEO_GENERATION_READY / BLOCKED
```

## Blocking Routing
- `VIDEO_CONDITIONING_READY != PASS` → 返回Stage 04 Video Conditioning，不允许抽Video Take；
- 只有Environment/Character/Color/Design/Whole Storyboard等辅助资产、没有Primary Visual → `PRIMARY_VISUAL_CONDITIONING_GAP`；
- Primary Visual是宫格/拼板/带文字箭头，或含未授权人物/错误World State → `VIDEO_CONDITIONING_FRAME_FAIL`；
- Critical/Readable人物没有视觉Authority → 回Stage 03/04建立最小Authority并重建Conditioning Frame；
- Storyboard/综合色/Style Reference路由不匹配平台能力 → 重组辅助Reference Pack，不取消Primary Visual；
- Cinematography/Focus冲突 → 回Stage 02/04最小Patch；
- Conflict → `prompt_constraint_solver.md`；
- Mandatory Storyboard缺失/漏Shot → Stage 04补Panel；
- `GENERATION_ENVELOPE`缺失/格式与Shot数量冲突 → Stage 04B重新解析Envelope；
- 非ONER Envelope没有Approved白描宫格、CUT顺序与宫格顺序不一致、Board Fingerprint不一致或Grid QC失败 → `MULTISHOT_STORYBOARD_GRID_GATE_PASS=false`，返回Stage 04/04B补Panel或重跑`storyboard_grid_assembler.py`；
- `VIDEO_EXECUTION_PLAN_PASS != YES` → 先回`video_execution_plan.md`解决Reference / Spatial / Limb / Performance / Camera / Timing / Physics / Audio冲突，禁止直接写Final Prompt；
- Motion Load过高 → 降低非必要约束或增加必要Keyframe / Shot Split；
- Stale Prompt → Fresh Recompile。

`MANDATORY_SHOT_STORYBOARD_COVERAGE != PASS`、`APPROVED MANDATORY SHOT STORYBOARD`缺失、`GENERATION_ENVELOPE_VALID != PASS`、Multi-shot时`MULTISHOT_STORYBOARD_GRID_GATE_PASS != PASS`、或`VIDEO_CONDITIONING_READY != PASS`任一成立时，正式Video Prompt必须WITHHOLD。

## Final Delivery Boundary
`VIDEO_GENERATION_READY`表示Resolved State可以进入/完成Compiler；自然语言交付仍须通过Egress与`POST_COMPILE_CONSTRAINT_CLOSURE=PASS`。
