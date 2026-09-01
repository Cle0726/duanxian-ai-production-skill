# Generation Execution Spine｜V4.5.7

> **目标：** 把“应该生成什么”变成可继续执行的真实资产链。任何图片/视频生成都必须经过真实`Generation Job → Host Execute → Result Capture`。图片随后进入`Image QC → Approval → Asset Promotion → Registry`；视频进入`VIDEO_TAKE_CAPTURED → VIDEO_RUNTIME → Video QC → User Approval`，**视频不得走图片Asset Promotion**。不得停在“只输出Prompt”。

## 1｜唯一执行链

图片：`Asset Requirement → GENERATION_JOB → Dispatch → Color/Reference Preflight → Host Generate → Candidate Capture → Image QC → Approval → Promote Asset → ASSET_REGISTRY → GENERATION_RUNTIME Complete → Next Job`
视频：`Video Requirement → GENERATION_ENVELOPE → Multi-shot Grid Gate（非ONER） → VIDEO_EXECUTION_PLAN → VIDEO_PROMPT_ARTIFACT → GENERATION_JOB → Dispatch(STAGE_05_VIDEO) → Primary Visual + Scene Color Authority/Reference-Budget Preflight → Host Generate → VIDEO_TAKE_CAPTURED → VIDEO_RUNTIME → Video QC → User Approval → APPROVED_VIDEO`

只要当前宿主具备对应生成能力，Controller必须真正调用该能力。只有能力明确`UNAVAILABLE`时才允许`MANUAL_HANDOFF`，并把Job标为`BLOCKED / WAITING_EXTERNAL_RESULT`语义，不得假装已生成。

## 2｜Generation Job是一等状态

每次真实生成必须有`generation_job_id / target_asset_id / target_asset_type / route / attempt_no / required_bindings / lineage / result_handles / status`。Video Job还必须绑定当前`generation_envelope_id + format_mode`。Candidate只是一次Job的输出，不等同于Approved Asset。

图片Job：`PLANNED → READY → RUNNING → RESULT_AVAILABLE → CANDIDATE_CAPTURED → QC_PASS_WAITING_APPROVAL → APPROVED_PROMOTED`。
视频Job：`PLANNED → READY → RUNNING → RESULT_AVAILABLE → CANDIDATE_CAPTURED → VIDEO_TAKE_CAPTURED`，之后由Stage 05 Video QC/Approval管理，不进入`APPROVED_PROMOTED`。

失败只回到`RETRY_REQUIRED`或`BLOCKED`，不得无记录地重新生成。Retry后必须递增`attempt_no`并让上一轮Candidate失去可选资格。

## 3｜Stage 03内部派发

`EPISODE_ASSET_BUILD`保持主Workflow State，不为每种资产新增Stage。它读取`REQUIRED_VIEW_GENERATION_QUEUE / Final Manifest / Generation Runtime`，逐Job调用子Route：
- Character → `CHARACTER_MASTER`
- Functional Minor Human Master → `FUNCTIONAL_MINOR_HUMAN_MASTER`
- Empty Environment Master / Environment Master/Coverage/Event/Reciprocal/Predictive → `ENVIRONMENT_MASTER_COVERAGE`
- Prop Master/Coverage → `PROP_MASTER_COVERAGE`
- Transformation → `TRANSFORMATION_FIRST_DESIGN / TRANSFORMATION_REPEAT`
- Scene Color Card → `SCENE_COLOR_CARD_DERIVATION`
- Production Support → `PRODUCTION_SUPPORT_REFERENCE`
- Shot Assembly → `SHOT_ASSEMBLY_ASSET`

Queue未清空不得宣称`REQUIRED_ASSETS_COMPLETE`。

## 4｜Candidate Capture ≠ Canon Archive

真实生成结果一出现就先保存/登记为Candidate：`generated/candidates/<job_id>/...`或宿主等价持久句柄。这个动作只证明“结果存在”。

只有**图片**QC通过并获得用户或已授权Batch Approval后，才Promote为正式Asset并进入Approved目录/Registry。视频Take只写入VIDEO_RUNTIME等待Video QC；不得把视频Take当图片资产Promote。不得把“保存文件”与“批准Canon”绑成一个动作。

## 5｜母图→Coverage→Shot Execution→Video血缘

必须保留可追踪`parent_asset_ids + derivation_kind + source_generation_job_ids`：

`Environment/Prop/Character Master`
→ `Required Coverage`（只补真实缺口）
→ `Shot Execution Frame`（把当前人物/场景/道具/World State/Storyboard合成成最终静态镜头）
→ `Video Job Primary Visual`

Video Job必须能从自身回查到Shot Execution Frame，再回查到其Master/Coverage父资产。

## 6｜Color Authority贯穿生成链

所有可见生成必须解析一个对应Color Authority：
- 普通Scene-bound Image / Shot Execution → 当前`SCENE_COLOR_CARD`直接绑定；
- Final Video → 必须记录当前`SCENE_COLOR_CARD` Authority与Primary Visual同源综合色血缘；默认`LINEAGE_ONLY`不额外占槽，只有Reference Budget选择`DIRECT_COLOR_REFERENCE`时才直接绑定色卡；
- Mandatory白描Storyboard Panel → 记录当前`SCENE_COLOR_CARD`血缘，但`projection_mode=VALUE_LIGHTING_LINEAGE_ONLY`且不得把综合色卡直接绑定给图像模型；
- Scene-independent Character/Prop/Transformation Master → `GLOBAL_COLOR_CARD`；
- 没有对应Approved Color Authority时，先创建/完成Color Job，不得静默丢综合色。

目标平台为Named Mention时，图片任务的综合色Direct Binding必须以真实`@资产`进入Prompt；Final Video只有在`DIRECT_COLOR_REFERENCE`模式下才出现综合色`@资产`。**Mandatory白描Storyboard例外：不得写综合色`@资产`给图像模型，只保留离图Value/Lighting血缘。** 其它宿主使用其真实Native Reference Binding，禁止伪造`@`。

## 7｜完成条件

Stage 03完成不是“Prompt都准备好了”，而是：所有Required **Image Job**已`APPROVED_PROMOTED`或明确`NOT_REQUIRED`，且Promotion已真实闭环到Asset Registry；Required View与Color Binding均通过Validator。Stage 05的Video Job完成条件是`VIDEO_TAKE_CAPTURED`并写入VIDEO_RUNTIME，随后继续Video QC/Approval。

## Current｜Storyboard + Video Prompt Closure

### Storyboard
`STORYBOARD_CONTACT_SHEET / STORYBOARD_CLEAN_PANEL / ACTION_CONTACT_KEY_POSE_CHAIN / SPATIAL_BLOCKING_MAP / CAMERA_PATH_PREVIS`是可派发Image Job类型。多镜头/多Beat的Mandatory白描默认派发**一个`STORYBOARD_CONTACT_SHEET` Image Job**，随后用`tools/storyboard_contact_sheet_splitter.py`确定性得到`STORYBOARD_CLEAN_PANEL`；这些Derived Panels不得伪造独立Image Job。真正单Panel镜头/修复任务才直接派发`STORYBOARD_CLEAN_PANEL`。`STORYBOARD_CLEAN_SEQUENCE_BOARD`**不是**图像生成任务，只能由`tools/storyboard_grid_assembler.py`从已QC/Approved Clean Panels确定性拼版。任何非ONER Generation Envelope仍必须拥有与CUT顺序一致的可验证Storyboard Proof；Sequence Board只作为确定性Review/辅助证据。

### Video
Video Job在进入`READY`前必须已经绑定：
- `generation_envelope_id + format_mode`；
- 非ONER时`MULTISHOT_STORYBOARD_GRID_GATE_PASS=true`；
- `video_unit_id`；
- Frozen `VIDEO_EXECUTION_PLAN`的`execution_plan_ref + execution_plan_fingerprint`；
- 通过Detail/Combat/Authority完整性检查、且不受Skill字符上限约束的`VIDEO_PROMPT_ARTIFACT`；
- `prompt_ref + prompt_fingerprint + prompt_artifact_ref`。

任何一项为空，`NO VIDEO GENERATION`。Execution Plan任一Source Fingerprint变化后Plan=`STALE`，其下游Prompt与Video Job同步失效，必须从最小受影响层重编译。

### Continuity Loop
Approved Video不得直接跳Post。必须先：
`Approved Video → Real Ending Frame Capture → Continuity Snapshot → Advance Video Unit`。
若存在下一Video Unit，回到该Unit的Stage 04 Storyboard；只有`NO_REMAINING_VIDEO_UNITS + REQUIRED_SEGMENTS_APPROVED`才允许进入Stage 06。


## V4.5.7｜Base Visual Authority Queue

Stage 03必须把`EMPTY_ENVIRONMENT_MASTER`和`FUNCTIONAL_MINOR_HUMAN_ASSET / MINOR_HUMAN_MASTER`当作普通Required Image Job直接进入Generation Queue，不得因为资产只服务一次Scene/Shot而跳过。图片数量可以增加，但每个Job必须通过稳定`entity_id / location_entity_id + reuse_key + asset_family_id + version + lineage`去重和复用。
