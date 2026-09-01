# Asset Intake（生产结果自动接收）

> **用途：** 用户把刚生成的图片、分镜或视频候选上传回来时，Skill优先根据当前生产上下文自动判断“这些是什么、属于哪个Episode / Scene / Segment / Job”，不要让用户重复解释已经明确的任务。

## 核心原则

**Use current production context first.** 先读当前 `Episode Workspace（单集生产工作区）`、最近一次已发出的生成任务、当前Queue（队列）和用户本轮标注，再给上传结果归类。

Asset Intake只负责**识别、分组、绑定生产任务并送去下一步**；它不自动把候选标成 `APPROVED（已批准）`。Functional Minor Human通过QC并获用户批准后使用`APPROVED SCOPED FIGURE`；Shot Assembly使用`APPROVED ASSEMBLY`；二者都不是长期Canon APPROVED。

## 自动识别顺序

收到用户上传结果后，按下面顺序判断：

1. 用户是否明确写了“图1/图2是……”或指定了Episode / Scene / Segment？有则优先采用。
2. 当前Workspace是否只有一个等待回收结果的Pending Job（待回收任务）？若是，默认绑定到该任务。
3. 最近一次Skill输出的是哪类生成Prompt：人物母图 / Personal Adornment Detail（AD-01） / 场景母图 / 道具母图 / Production Support Reference / Shot Assembly Asset / Additional Video Conditioning Keyframe / Render/Cinematic Style Board / Global或Scene Color Card / Lighting Reference / Storyboard / Video？
4. 上传数量是否与当前Pending Job对应？图片/Stage 04 Previs先读`Image Candidate Policy / Planned Candidate Count`；Design-bearing Master通常2张、高风险可4张、Coverage、Stage 03 Production Support与Shot Assembly通常2张、普通Previs Component通常1张/复杂可2张、Additional Video Conditioning Keyframe需要时通常2张、Revision通常1张。**FINAL VIDEO PROMPT仍默认期望1个Video Take；只有T3/T4已通过Failure-before-Compute并提高Take Budget时，才允许合法出现多个计划内Take。**
5. 当前Queue中是否有唯一可匹配的任务？
6. 若仍有多个同等合理解释，才要求用户补一句最必要的说明；不要因为能通过上下文判断的小问题打断生产。

## 支持的结果类型

- `ASSET CANDIDATE`：人物 / Personal Adornment Detail / 场景 / 道具 / 武器 / 变身 / 状态变体 / Production Support Reference / Shot Assembly Asset / Render Style Evidence / Cinematic Shot Style Evidence / Global Color Card / Scene Color Extension Card / Lighting Reference / 其他Stage 03候选；
- `SHOT SUPPORT CANDIDATE`：Approved Storyboard之后生成的Additional Video Conditioning Keyframe候选；属于Stage 04生产支持，不是Canon Asset；
- `PREVIS / STORYBOARD CANDIDATE`：Stage 04自适应预演候选；可为Hero Frame / Keyframe Pair / Panel Board / Blocking Board / Action Pose Chain / Spatial Map / Camera Path / Transformation / Montage / Continuity Board或HYBRID Component。旧`STORYBOARD CANDIDATE`字段继续兼容；
- `VIDEO TAKE`：视频生成候选；
- `ENDING FRAME CANDIDATE`：尾帧候选；
- `POST OUTPUT`：后期测试/成片版本；
- `PATCH REFERENCE / PATCH DESIGN AUTHORITY`：用户提供的正确局部图案、零件、纹样、裂纹、配件或局部结构参考；这类图片不是被编辑母图，必须绑定到对应Local Patch Job。

## 自动归档字段

内部至少形成：

```text
【Asset Intake】
Episode：EP__
Scene：S__
Segment：SEG__ / N/A
Job Type：PREVIS / STORYBOARD CANDIDATE
Job ID：若已有则沿用
Candidates：01 / 02 / 03 / 04
Source Prompt：当前对应Prompt版本
Current Status：RECEIVED
Next Action：Candidate Triage → QC
```

若是Stage 03资产：

```text
Asset ID：沿用现有ID；没有才使用项目建议编号
Asset Type：Character / Functional Minor Human / Personal Adornment Detail / Environment / Prop / Weapon / Transformation / State Variant / Production Support（含Lightweight Interaction Prop / Shot Detail） / Shot Assembly / Render Style / Cinematic Shot Style / Global Color / Scene Color Extension / Lighting Reference
Version：候选版本
Current Status：WIP / CURRENT候选
Next Action：Candidate Triage → Asset QC → 等待批准
```


## Local Patch / Inpaint Intake

若当前Pending Job是局部重绘 / Inpaint / 定点修改，Asset Intake先读取 `inpaint_local_patch_authority_engine.md`，**先识别Edit Target Type**（ASSET_MASTER / STORYBOARD / VIDEO_FRAME_REFERENCE / APPROVED_ENDING_FRAME），再按用户当前标注与上下文自动分配：

- “这张是要改的母图/底图” → `EDIT_TARGET`；
- “QC不过，但这张只需稍微改/按这张继续修” → 当前失败Candidate自动绑定为`REVISION_SOURCE_IMAGE / EDIT_TARGET`；Parent Master仅作为必要Canon Support，不能替代失败Candidate；
- “这张不要了，从母图重新出一张” → `FRESH_REGEN`，此时才允许Parent Master重新成为Primary Source；
- “按这张图案/这个零件/这个局部重绘” → `PATCH_DESIGN_AUTHORITY`；
- “只参考画风” → `STYLE_AUTHORITY`；
- “用这张锁脸/身份/同一道具” → `IDENTITY_AUTHORITY`。

**若用户已经提供PATCH_DESIGN_AUTHORITY，不得因为当前Workspace里存在APPROVED Master就忽略该局部参考，也不得把Master自己升级为Patch Design Authority。**

若用户同时上传母图与局部参考，下一步直接交 `Reference Resolver → Patch Reference Mode` 动态编号；不要要求用户重新解释已经明确的“哪张是底图、哪张是重绘图案”。

### Patch Stage Routing
- Edit Target = ASSET_MASTER → Patch Result进入Stage 03 Asset QC；
- Edit Target = STORYBOARD → Patch Result进入Stage 04 Storyboard QC；
- Edit Target = APPROVED_ENDING_FRAME → 阻止“修图后继续当Ending Frame Authority”；应从Approved Video重新选真实帧或返修Video；
- Edit Target = 普通辅助截图 → 可编辑，但结果标记`EDITED VISUAL REFERENCE / NOT CONTINUITY AUTHORITY`。

若当前是REVISE后的复检，Asset Intake同时建立/更新`QC Scope Freeze Ledger`：继承上一轮FROZEN_PASS，记录本次Revision Surface，并只把真正被影响的维度标REOPENED。

## 自动下一步

- 图片/Storyboard多个计划候选 → `Candidate Triage（Fast Triage → Primary/Backup）`，再对Primary进入Deep QC；
- 单个图片/Storyboard候选 → 直接进入对应QC；
- 多个Video Take → 只有合法存在时才做Best Take Selection，不把图片候选策略套到Video；
- QC失败 → `Failure Diagnosis（失败诊断）`；
- 用户明确批准 → 状态更新为APPROVED → 调用Auto Naming + Approved Asset Archiver；归档后更新Registry / Workspace的Archive Status / Path；
- 视频批准 → `Ending Frame QC + Continuity Snapshot`；
- 不要让用户重复填写已经能从Workspace推断出的Episode / Scene / Segment / Asset ID。

## 与Episode Asset Batch / Storyboard Batch的关系

Stage 03整集资产批量回收时，Asset Intake先按Asset ID / Asset Type绑定Final Episode Asset Requirement Manifest中的Build Queue，再逐项进入Candidate Triage / QC / Approval；不得因为“同一批上传”把不同资产互相比。

Episode Asset Freeze后若一次回收多个Storyboard，Asset Intake再按Segment分组进入Candidate Triage / QC。不要把不同Segment候选互相比“谁最好”。

## 禁止

- 不要把“用户上传了”自动等同于“用户批准了”；
- 不要因为文件名混乱就忽略当前Workspace上下文；
- 不要把不同生成任务的候选混成一组；
- 不要在能唯一推断任务时要求用户重新说明“这些是什么”。
## Approved Asset Archiver交接

Asset Intake只负责识别候选，不负责提前归档。只有对应QC完成且用户明确批准后，才把已批准结果交给 `approved_asset_archiver.md`。

若文件本体当前可访问且已解析到真实Source Path：Archiver执行Source Preflight → 真实复制 → Target Postcondition → Source/Target SHA-256验证；全部通过后才写 `ARCHIVED`。若只在聊天UI可见、找不到真实Source Path、或任一验证失败：写 `ARCHIVE PENDING`，不要阻断内容的APPROVED状态，但必须把未物理保存事实写清楚。



## Web QC Report入口

用户贴回网页版Video QC文字结果时，不把它当成新的Video Take。按 `web_qc_handoff.md` 识别为External Video QC Report，核对Segment / Prompt Version / Take后写回Workspace。默认不要求用户重复上传同一视频给本地Skill；只有用户明确要求LOCAL_SELF_CHECK时才亲自读取。


## V4.5.3 Visual Evidence Intake

任何新图片进入正式Registry时先保存真实文件Fingerprint。若当前模型/人工已经实际看图，则在QC/批准同轮写`VISUAL_EVIDENCE`；若未看图，登记`visual_evidence_status=MISSING/UNKNOWN`，禁止从Prompt反推。Text-only模式只允许复用`CURRENT + fingerprint match`的视觉Evidence。
