# Web QC Handoff（网页版视频QC交接）

> **用途：** 把“完整观看AI视频并做视觉QC”默认交给网页版验证端；本地Skill负责生产控制、Prompt版本、连续性和返工，避免本地重复读取同一个大视频消耗额度。
> **关键体验：** 用户不应该自己拼QC说明。Skill必须直接给出一个**完整、连续、可一键复制到网页版的 `WEB_QC_COPY_PROMPT`**。
> **去重边界：** Web QC属于验收层；其中的QC检查项不得反向复制进 `FINAL VIDEO PROMPT`。
>
> 这不是Stage 07，只是Stage 05 Video QC的执行模式。
> **上传数量Primary Authority：** 所有图片附件数量、B01/B02拆包与Multi-Pass规则服从 `web_multimodal_qc_upload_budget.md`；本文件不得覆盖10图硬上限。Revision Recheck若只修订部分问题，同时读取`qc_scope_freeze_ledger.md`，但新Video Take仍对Identity / Major Spatial Continuity做P0 Sanity Check。

**Current Reference Display Rule（Current Rule）：** `WEB_QC_UPLOAD_LIST`可以保留文件名 / Asset ID / Version帮助用户找到正确文件；`WEB_QC_COPY_PROMPT`中的`@图N`只写Evidence Role / Input Mode，不再重复长文件名。该`@图N`仅用于本批QC证据映射，不得复制回FINAL VIDEO PROMPT。

**Current Free-Tier Watermark Exception（Current Rule）：** 所有Web Video QC必须同时读取`web_qc_platform_watermark_exception.md`；`Dola AI`与`豆包AI生成`平台水印为QC中性，不得因水印本体判P0/P1/P2、文字/Logo污染、画面质量失败或要求重生成。只有水印实际遮挡关键证据时才按证据遮挡处理。

## 1｜两种QC模式

### WEB_QC_DEFAULT（默认）

正式Video Take生成后，本地Skill默认**不亲自重复读取完整视频**。

本地Skill负责提供：
1. `WEB_QC_UPLOAD_LIST`：网页版需要上传什么；
2. `WEB_QC_COPY_PROMPT`：一个完整代码块，用户整段复制到网页版即可；
3. `QC Batch / Image Count`：明确本批为B01/B02及`N / 10 images`；
4. 用户把网页版返回的QC文字贴回后，导入为 `External Video QC Report`。

网页版需要看到当前Video Take，以及Upload List要求的实际Reference Pack图像。网页版不需要安装本Skill，也不需要用户重新解释项目规则。

### LOCAL_SELF_CHECK（用户主动亲检）

只有用户明确表示以下意图时才启动：
- “你亲自检查这个视频”；
- “你自己看一下”；
- “我拿不准，你复核”；
- “网页版说得不清楚，你亲自判断”；
- 其他明确要求本地Skill直接观看视频的表达。

启动后，本地Skill读取实际Video Take和必要参考图，按同一Stage 05 QC标准完整检查。

**禁止自动触发。** 即使External Report写 `INSUFFICIENT_EVIDENCE / UNCERTAIN`，也只能提示用户可以选择LOCAL_SELF_CHECK，不能擅自读取完整视频。

---

## 2｜强制用户可见输出契约

### 2.1 QC Packet只在真实Video Take存在后输出

`FINAL VIDEO PROMPT`交付阶段只负责生成视频；可以内部预建QC Contract / Evidence需求，但**不得提前输出**`WEB_QC_UPLOAD_LIST / WEB_QC_COPY_PROMPT`，也不得假定未来Take ID、实际Reference Pack或上传顺序。

真实Video Take生成并进入Stage 05 QC后，必须一次性向用户输出：
1. `QC Batch / WEB_QC_IMAGE_COUNT` —— 明确本批Batch ID与`N / 10`；
2. `WEB_QC_UPLOAD_LIST` —— 当前真实Video Take与本批实际Reference证据；
3. `WEB_QC_COPY_PROMPT` —— **完整代码块，直接复制到网页版验证。**

不得：
- 在Video尚不存在时提前打印QC Upload List / Copy Prompt；
- 只说“已准备WEB_QC_PACKET”但在真正进入QC后仍不展示Prompt；
- 只给文件名或路径，要求用户自己拼装；
- 让用户自己把参考图职责、QC标准和返回格式重新组合。

### 2.2 WEB_QC_PACKET的定义

`WEB_QC_PACKET`不再代表“一个需要用户自己阅读整理的长文档”。它只是内部交接对象，必须由以下内容组成：

- `QC Batch ID`
- `WEB_QC_UPLOAD_LIST`
- `WEB_QC_IMAGE_COUNT (<=10)`
- `WEB_QC_COPY_PROMPT`

可选保存文件：
`<SEGMENT_ID>_WEB_QC_PACKET_<PROMPT_VERSION>.md`

**但文件保存不能替代聊天中直接展示可复制Prompt。**

---

## 3｜WEB_QC_UPLOAD_LIST

### 3.0 Web Multimodal Image Cap

生成Upload List前先执行：`WEB_MULTIMODAL_IMAGE_CAP = platform_profile.image_upload_cap`（当前Profile=10）。Stage 05一个正常QC Batch = `1 Video Take + N Reference Images`，其中 `N <= platform_profile.image_upload_cap`（当前=10）。若本次验证所需图片超过10，必须先按`web_multimodal_qc_upload_budget.md`删除CONDITIONAL/TEXT-ONLY化；仍超出则拆成`B01 / B02...`或`PASS-A / PASS-B`。**禁止输出@图11，禁止让用户自己决定删哪张。**

每个Batch的Copy Prompt都必须写`QC Batch: Bxx`并按本批实际上传顺序从@图1重新编号。

**Temporal Salvage Multi-Pass Merge：** 若同一Video Take因Reference证据超过10图而拆成B01/B02或PASS-A/PASS-B，每个Required Pass只对自己的QC Scope下结论，但最终`TEMPORAL_SALVAGE_MAP`必须在所有Required Pass完成后合并。合并时先收集所有Pass的真实时间边界，把时间轴切成Atomic Intervals；任何Required Pass在某区间发现使素材不可用的P0/P1，则该区间不得因另一Pass写KEEP而被保留。若各Pass结论无法保守兼容，标`SALVAGE_MULTIPASS_CONFLICT`并补充针对同一Take的验证，不得把KEEP窗口做并集。


必须基于**本次真正用于生成视频的 Video Reference Pack Snapshot**，不能重新随意换图或写死@编号。

输出格式应尽量简单，例如：

```text
【WEB QC 上传材料】
1. <SEGMENT_ID>_TAKE01.mp4
2. @图<本批实际编号>｜<Evidence Role / Input Mode>
3. @图<本批实际编号>｜<Evidence Role / Input Mode>
...

不用上传：
- TEXT-ONLY约束
- 本次未使用的角色/道具/场景资产
```

逐项Reference必须在后面的Copy Prompt里说明：
- 允许控制什么；
- 禁止控制什么；
- Reference Tier：MUST / CONDITIONAL（必要时）。

保持以下Authority：
- Storyboard = Shot / Composition / Action Anchor Authority，**NOT render-quality reference**；
- Previous Ending Frame = Continuity Authority，**NOT render-quality reference**；
- Character / Prop / Environment Master分别决定自身正式设计与细节；
- Render Style Anchor只决定项目绘画语言/风格方法；Cinematic Shot Style Anchor只决定项目级摄影语法且不得覆盖本次Storyboard具体Camera；对象结构、材质与细节分别由当前Task最直接的Approved HD Object Authority决定；场景/道具当前视角已有Approved Coverage时优先Coverage；综合色按当前最直接的Global Color DNA / Scene Color Extension / Shot Lighting Variant核对。

---

## 4｜WEB_QC_COPY_PROMPT标准模板

Skill必须把下面结构**动态填充后输出成一个不中断的代码块**。用户应能全选 → 复制 → 粘贴到网页版，不需要补写任何项目说明。

```text
你现在是《断弦之歌》的独立 AI Video QC Verifier（视频质量验证端）。

我已经在本次对话上传：
- 当前待验证的 Video Take；
- 下方列出的本批 @参考图（本批图片总数不超过10张）。

只使用**本批实际上传**的@图编号进行判断，不要引用前一批次的@图编号。

请不要重新设计剧情、镜头或角色，不要用你自己的审美替换已批准方案。你的任务只是：完整观看实际视频，并判断它是否正确执行本次 FINAL VIDEO PROMPT 与 Reference Authority。

────────────────
【验证对象】
Project：《断弦之歌》
Episode：<EPISODE_ID / NAME>
Scene：<SCENE_ID / NAME>
Segment：<SEGMENT_ID>
Prompt Version：<PROMPT_VERSION>
Video Take：TAKE01
QC Batch：<B01 / PASS-A / PASS-B>
Reference Image Count：<N / 10>
Entry Mode：<CONTINUITY_ENTRY / CUT_ENTRY / SCENE_OPENING>
Director Target Duration：<TARGET_DURATION>
Platform Duration Profile：<UNDECLARED / FLEXIBLE / FIXED_SLOTS / HARD_MAX / FIXED_SLOTS+HARD_MAX>
Execution Duration Mapping：<DIRECT / SLOT __ / SPLIT / PENDING PLATFORM MAPPING>

────────────────
【QC Scope Freeze｜修订复检时填写；首次Take则N/A】
FROZEN_PASS：<... / N/A>
OPEN_REVISION_TARGET：<... / N/A>
REOPENED：<... / N/A>
Revision Surface：<... / N/A>

说明：新Video Take仍需对Character Identity / Major Spatial Continuity做快速P0 Sanity Check；但不得因为个人审美重新推翻与本轮Revision无关的已冻结设计维度。

────────────────
【本次 @Reference Pack｜按实际上传编号】

@图1｜<Evidence Role>
Type：<Character / Environment / Prop / Weapon / Ending Frame / Storyboard Panel / Render Style / Cinematic Shot Style / Global Color / Scene Color / Lighting>
Reference Tier：<MUST / CONDITIONAL>
允许控制：<本图职责>
禁止控制：<不得越权内容>

@图2｜...

<继续列完本次实际上传的所有Reference；不得添加本次未使用资产>

特别注意：
- Approved Storyboard只控制Shot顺序、构图、景别、动作节点与必要镜头关系，不控制最终渲染画质。
- Previous Ending Frame只控制起始站位、朝向、摄影轴线、动作阶段、重心和当前道具状态，不控制最终渲染画质。
- 人物、服装、武器/道具、场景的正式身份、结构、材质与细节分别服从当前Task最直接的Approved HD Object Authority；Environment / Prop当前视角已有Approved Coverage时不得无理由退回泛化Parent Master。
- Render Style（若上传）只核对绘画语言；Cinematic Shot Style（若上传）只核对摄影语法且不覆盖具体Storyboard；综合色Reference（若上传）只核对当前层级综合色/光色；不得拿这些控制图自身像素细节作为成片清晰表现标准。

────────────────
【本次实际 FINAL VIDEO PROMPT｜原样】

<完整粘贴本次真正用于生成TAKE01的FINAL VIDEO PROMPT，禁止摘要、改写或省略>

────────────────
【导演执行索引】

Shot Timeline：
<简洁列出SH01 / CUT / SH02 / Match Cut等实际时间结构>

Entry：
<本段起始状态>

Trigger：
<触发点>

Performance：
<关键表演路径>

Action Physics：
<关键身体受力 / 接触 / 惯性要求>

Combat Choreography：
<如为战斗/追逐：Victory Condition / Measure / Initiative / Exchange / Impact / Counterplay；否则N/A>

Exit：
<本段必须结束到的稳定状态>

Music Identity / Motion Grammar：
<如有则写；无则N/A。这里只验证动作节奏，不要求自动生成BGM>

Voice Mode：
<FINAL_VOICE / TEMP_SYNC_AUDIO / NO_DIALOGUE_AUDIO>

────────────────
【允许的平台水印｜QC豁免】
以下免费额度平台水印为QC中性，不得作为P0/P1/P2、文字污染、Logo污染、画面质量失败或返工理由：
- Dola AI
- 豆包AI生成
若指定水印只是角标且不遮挡关键证据，请直接忽略；若实际遮住必须验证的关键区域，只标记EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK，并仅在无法从其他证据完成判断时使用INSUFFICIENT_EVIDENCE。其他未知水印/品牌字样不在此豁免内。

────────────────
【验证方法｜必须执行】

1. 第一遍：从头到尾完整观看视频，不要只看首帧、尾帧或抽帧。
2. 第二遍：按时间轴复查关键Shot、CUT / Match Cut、人物表演、动作、接触、武器/道具、Director Target Duration和Exit State；特别检查“持物手开始新动作后原物体是否仍有支撑、换手是否真的发生、Ongoing Task是否凭空消失”。
   若镜头有明显背景群体，同时检查：前景对白期间Crowd是否整片冻结、是否同步转头/循环、是否无因全部盯主角、强刺激反应是否分层传播、CUT后Density/Flow是否重置。
3. 发现问题时尽量给出具体Timestamp，例如：00:04.2–00:05.1。
4. 不允许只写“感觉不自然”“动作不好”“可以优化”；必须描述肉眼可观察的问题。
5. 不重新设计已经批准的剧情或镜头；只判断执行偏差。
6. 按Reference Authority验证，不得拿Storyboard或Ending Frame的低细节/截图感当正式画质标准。
7. 检查是否出现 AUTO BGM。Stage 05只允许必要Dialogue/VO、Ambience、Foley/SFX，以及剧情明确存在的Diegetic/Source Music；没有剧情内音乐时应为MUSIC = NONE。
8. 如果有Dialogue并且Voice Mode = TEMP_SYNC_AUDIO，不要因为临时音色不是最终角色声纹判失败；只检查必要同步与明显异常。
9. 必须判断问题来源，不要一看到失败就默认建议重生成。
10. 遵守Adaptive Take Budget：T1/T2不能因为“多一个候选更保险”而要求第二Take；T3/T4也只有上游Gate通过且Failure Diagnosis证明随机性为主因时才能使用受限候选预算。
11. 验证时长执行：Director Target必须>0并符合Approved Sequence；Skill不设置固定最大秒数。若当前任务提供了可靠Platform Duration Profile，检查实际Slot / Requested Duration / Hard Max映射是否一致；未提供时不得虚构。若平台时长大于Target，多余尾部应是可Trim的稳定余量，不应新增剧情动作凑满；也不得为适配平台上限异常压缩对白/动作。
12. `Dola AI`与`豆包AI生成`属于允许的平台水印：水印本体必须完全从P0/P1/P2、Render Quality、文字/Logo污染与Revision Target中排除；只有实际遮挡关键验证区域时才记录证据遮挡。

────────────────
【必须检查的维度】

- Character Identity：脸、年龄、发型、服装、变身状态是否漂移
- Environment / Spatial Continuity：空间结构、站位、左右关系、轴线
- Entry Continuity：仅CONTINUITY_ENTRY检查上一段承接
- Shot Execution：Shot数量、景别、机位、CUT / Match Cut、时序
- Duration Execution：Director Target是否>0且符合Approved Sequence；Platform Duration Profile是否来自可靠当前信息；Execution Mapping是否兼容真实平台；是否存在Padding / Forced Compression
- Performance：先判断角色Objective / Tactic / Active Listening是否能从行为中读出，再检查眼神、原任务、声音/语流、手部/姿态、Thought Continuity、Speech Phrase、Continuity Bridge、Listener Flow与情绪层次；有因Triggered Stillness不算冻结。Breath=IMPLICIT时不要求看见呼吸，只有有原因的可见换气才检查Cause / Degree / Timing / Recovery。特别检查是否出现“说一句→身体归零→重启下一句”的机械循环
- Crowd Presence / Ambient Life（适用时）：背景群体是否持续低强度、异步地维持自己的任务；是否出现整片截图冻结、同步循环、全体无因关注主角、Crowd抢戏、Reaction Broadcast、Density/Flow Reset或明显复制NPC
- Action Feasibility / Prop-Limb Continuity：具体执行手/脚与当前占用是否一致；Held Prop / Body Load / Inter-character Support是否持续；换手/放下/拾取/交接是否有可见或可信Bridge；接触/坐站/迈步是否有Approach / Grip / Release / Weight Shift；Ongoing Task与Exit State是否连续
- Natural Motion：动作合法后再检查是否存在Pose插值、机器人串行、脚底滑转、不自然直线手臂、缺准备/减速/余韵、幅度过大等；
- Action Physics：在自然动作路径成立后再检查接触、受力、惯性、回弹、漂浮/穿模
- Combat Choreography（适用时）：有效距离、Initiative、攻防因果、Counter Window、Impact、Skill Counterplay、多人是否排队出招、已确认Cost是否可见、战斗解除时Weapon/Costume/Baton是否同步消散
- Prop / Weapon：结构、尺寸、方向、握持、生成/消失逻辑
- Render Quality / Style：是否正确使用当前最直接Approved HD Object Authority，并保持项目绘画语言；控制图没有抢对象细节Authority
- Style Continuity（Current）：实际Video是否仍保持声明的Render Family、手绘线稿、受控色块+柔和绘画阴影、人物脸/哑光皮肤/发束（有人物时）、材质表现、**色彩组织方式/对比/明度关系**与人物-环境同一二维绘画系统；Scene具体色相/冷暖/光色由Current Color Authority单独判断，不因合法Scene综合色变化判Style Fail；不得只因为“也是二维”就判一致。
- Audio Boundary：是否出现禁止的AUTO BGM或明显不该存在的声音
- Voice Status：按Voice Mode验证
- Exit State：是否落到下一Segment可继续使用的稳定状态

### Temporal Salvage QC（必须）
只要Whole-Take不是完整PASS，或存在局部时间错误/可Trim区间，必须继续读取`video_temporal_salvage_qc.md`，从头到尾按真实时间轴划分可用与不可用区间。不能因为中间有P0/P1就停止观看后半段；也不能因为整体REVISE就省略可用片段判断。

每个时间窗至少判断：Visual Validity / Temporal Integrity / Editorial Utility / Entry-Exit Cutability / Continuity / Director Invariants，并把Video与Audio用途分开。若无真实可用窗口明确写`NO_SALVAGE`；证据不足则写`INSUFFICIENT_EVIDENCE`，不得猜时间戳。 **Temporal Salvage Map必须从00:00.00覆盖到真实Source Duration，不得留未分类Gap；坏区间也要明确REJECT。**

问题优先分级：
P0 = 必须返工，影响身份/剧情/连续性/核心镜头逻辑
P1 = 明显质量问题，但未必推翻整段
P2 = 可接受的小波动或可后期处理项

Root Cause只能优先从以下类别判断：
PROMPT_ERROR
REFERENCE_ERROR
MODEL_EXECUTION_VARIANCE
CONTINUITY_ERROR
ASSET_ERROR
POST_FIXABLE
INSUFFICIENT_EVIDENCE

────────────────
【最终返回格式｜请严格按此输出】

WEB_VIDEO_QC_RESULT

Segment: <SEGMENT_ID>
Prompt Version: <PROMPT_VERSION>
Video Take: TAKE01
Source Duration: <actual duration>
QC Source: WEB_EXTERNAL_VERIFIER

Verdict: PASS / REVISE / OPTIONAL_SAME_PROMPT_RETRY / INSUFFICIENT_EVIDENCE
Style Match: PASS / FAIL / N/A
Temporal Salvage Status: FULL_TAKE_USABLE / SALVAGE_AVAILABLE / NO_SALVAGE / INSUFFICIENT_EVIDENCE

Temporal Salvage Map:
- <IN>–<OUT>｜CLEAN_KEEP / CONDITIONAL_KEEP / HANDLE_ONLY / REJECT｜Editorial Function｜VIDEO_USE: KEEP/CONDITIONAL/REJECT｜AUDIO_USE: KEEP/REPLACE/AUDIO_ONLY/REJECT｜ENTRY_CUT｜EXIT_CUT｜Continuity｜Director Invariants｜Conditions｜Why

P0:
- ...

P1:
- ...

P2:
- ...

Timestamp Issues:
- 00:00.0–00:00.0｜具体可观察问题｜对应Prompt/Reference要求

Root Cause:
<PROMPT_ERROR / REFERENCE_ERROR / MODEL_EXECUTION_VARIANCE / CONTINUITY_ERROR / ASSET_ERROR / POST_FIXABLE / INSUFFICIENT_EVIDENCE>

Prompt Diagnosis:
- 已正确执行的模块：...
- 真正需要修改的模块：...

Recommended Action:
<PASS_TO_USER_APPROVAL / KEEP_SALVAGE_AND_POST / KEEP_SALVAGE_AND_REVISE_REMAINDER / POST_FIX_ONLY / MINIMUM_PROMPT_REVISION / OPTIONAL_SAME_PROMPT_RETRY / REQUEST_MISSING_EVIDENCE>

Minimum Necessary Change:
- 只有需要改Prompt时填写；只写最小必要修改，不重写已经正确的部分。

Confidence:
HIGH / MEDIUM / LOW

额外规则：
- 如果Prompt本身基本正确、实际视频已经非常接近目标，只剩高度疑似模型随机执行差异，才允许 Verdict = OPTIONAL_SAME_PROMPT_RETRY。
- OPTIONAL_SAME_PROMPT_RETRY只是可选建议，不是Gate要求。
- PASS只代表Video QC通过，不代表用户已经APPROVED。
- Whole-Take REVISE不代表`NO_SALVAGE`；必须继续看到结尾并判断所有时间窗。
- `CLEAN_KEEP / CONDITIONAL_KEEP / HANDLE_ONLY`都只是Salvage Candidate；不得在QC阶段自动升级APPROVED。
- 原计划若是不可切Long Take，Salvage判断必须明确Director Invariant风险，不能为了节省成本自动制造CUT。
- 如果证据不足，输出INSUFFICIENT_EVIDENCE并明确缺什么，不要猜。
```

### Copy Prompt编译要求

- 上述尖括号占位符在交付给用户前必须全部动态填好；不允许把 `<SEGMENT_ID>` 这种未填字段留给用户自己补。
- `FINAL VIDEO PROMPT`必须原样完整嵌入，不能写“见上文”或“使用之前Prompt”。因为网页版是独立验证会话。
- Reference Pack必须使用**本次实际上传顺序和动态@编号**。
- 若某检查维度本段不适用，Copy Prompt中可标 `N/A`，但不得让用户自己删除。
- 整个 `WEB_QC_COPY_PROMPT`必须是**一个连续代码块**，不能拆成多个零散段落让用户拼接。

---

## 5｜External Video QC Report导入规则

用户把网页版结果文字贴回本地Skill后：

1. 识别 `Segment / Prompt Version / Video Take`；
2. 与当前Workspace Pending Job核对；
3. 标记：`QC Source = WEB_EXTERNAL_VERIFIER`；
4. 保存/记录External Report内容；
5. 先执行Allowed Platform Watermark Normalization：若External Report把`Dola AI`或`豆包AI生成`水印本体列为P0/P1/P2、Render Quality失败、文字/Logo污染或Revision Target，删除该误判；若删除后无其他真实问题，不得据此要求返工；若指定水印实际遮挡关键证据，则转写为`EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK`后再判断证据充分性；
6. **不再次要求上传同一Video Take供本地重复观看**；
7. 根据Verdict推进：
   - `PASS` → `VIDEO QC PASSED / WAITING APPROVAL`；
   - `REVISE` → 先导入Temporal Salvage Map并登记`SALVAGE_CANDIDATE`（若有），再进入Failure Diagnosis / Prompt Compiler，只对剩余失败内容做Minimum Necessary Change；
   - `OPTIONAL_SAME_PROMPT_RETRY` → 仅作为可选建议，不阻塞；
   - `INSUFFICIENT_EVIDENCE` → 请求网页版补充缺失证据，或提示用户可主动选择LOCAL_SELF_CHECK。

External Report不是用户批准。`PASS`仍然必须等待用户明确APPROVED。

### 允许非标准化粘贴

如果用户贴回的网页版结果没有完全遵守模板，但已经明确包含：
- 哪个Segment/Take；
- PASS还是有问题；
- 具体问题；
- 建议动作；

本地Skill应自动整理成External Video QC Report，不要求用户重新填写整张表。只有关键信息确实不足时才追问最小缺失项。

---

## 6｜LOCAL_SELF_CHECK亲检规则

用户主动要求亲检时：

1. `QC Mode = LOCAL_SELF_CHECK`；
2. 读取当前实际Video Take；
3. 读取Reference Resolver给出的QC必要参考图；
4. 完整观看并按Stage 05 QC执行；若非PASS或局部失败，继续完成Temporal Salvage Map，不得只报失败点；
5. 输出与Web Report兼容的结果结构，但写：`QC Source = LOCAL_SELF_CHECK`；
6. 如果已有External Report，要做“复核”，不是假装没看过外部结论；
7. 本地结论与外部结论冲突时，明确指出冲突项和依据，由用户决定是否批准/返工。

亲检不等于自动返工。即使LOCAL_SELF_CHECK发现问题，也仍按：
`POST_FIX → Minimum Prompt Revision → Optional Same-Prompt Retry → Segment Split`
顺序判断，继续遵守Adaptive Take Budget与Failure-before-Compute。

---

## 7｜成本保护锁

- 默认模式永远是 `WEB_QC_DEFAULT`；
- 不因为视频“看起来复杂”自动切换LOCAL_SELF_CHECK；
- 不因为External Report置信度低自动读取视频；
- 用户没有要求亲检时，本地Skill不得以“保险”为理由重复视觉分析同一个完整视频；
- 本地仍负责判断External Report与Workspace / Prompt版本是否匹配，不能盲收别的Segment结果；
- 亲检是用户可随时调用的兜底能力，不是每段都必须做的第二道QC。


## Current｜Reference Leakage + Voice QC

实际Video QC必须额外检查：
- 是否出现综合色色块/色条/gradient rectangles、Storyboard格线/边框/分屏、Style/Reference Board标题/样板布局等`REFERENCE_LAYOUT_LITERALIZATION_LEAK`；
- 当前Scene是否被Style/Color Board示例地点/人物/车辆无因替换；
- 有Dialogue/VO时，实际语速、停顿节点、重音、句尾走势是否与本轮`VOICE_DIRECTION_PLAN / VOICE_PROMPT_HANDOFF / FINAL VIDEO PROMPT`一致；若Verifier可听音频，检查同角色Voice Identity是否漂移；
- 无听觉证据时不得猜Prosody PASS，返回INSUFFICIENT_EVIDENCE或按可用证据限定结论。


## Current｜Temporal Salvage QC
Video QC返回结构必须把Whole-Take Verdict和Temporal Salvage Status分开。任何`SALVAGE_AVAILABLE`结果必须登记真实Source Take与IN/OUT，并保留Source File；候选片段未获最终采用前不得产生正式Ending Frame Authority。
