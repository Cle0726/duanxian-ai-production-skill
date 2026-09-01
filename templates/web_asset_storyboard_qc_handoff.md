# Web Asset & Storyboard QC Handoff（网页版图片资产 / 分镜QC交接）

> **用途：** 为Stage 03 Asset QC与Stage 04 Storyboard QC提供与Video QC同等级的标准化网页版交接协议。
>
> 图片数量、B01/B02拆包、Multi-Pass统一服从 `web_multimodal_qc_upload_budget.md`；修订复检范围服从 `qc_scope_freeze_ledger.md`。

---

**Current Reference Display Rule（Current Rule）：** Upload List可以保留文件名 / Asset ID / Version帮助定位文件；Copy Prompt里的动态`@图N`只写Evidence Role，不重复长文件名。QC编号不得污染图片/Storyboard Generation Prompt。

**Current Free-Tier Watermark Exception（Current Rule）：** Web Asset / Storyboard / Previs QC统一读取`web_qc_platform_watermark_exception.md`；`Dola AI`与`豆包AI生成`水印为QC中性，不参与候选优劣、P0/P1/P2或Revision Target。只有实际遮挡关键证据时才按证据遮挡处理。

## 1｜统一交付结构

每个网页版Asset/Storyboard QC Batch必须直接给用户：

1. `QC Batch ID`；
2. `Image Count: N / 10`；
3. `WEB_QC_UPLOAD_LIST`；
4. 一个完整连续、可直接复制的`WEB_ASSET_QC_COPY_PROMPT`或`WEB_STORYBOARD_QC_COPY_PROMPT`；
5. 若为Revision Recheck，必须包含QC Scope Freeze。

不得只说“上传这些图让网页检查”。

---

## 2｜WEB_ASSET_QC_COPY_PROMPT标准

动态编译时必须包含：

```text
你现在是《断弦之歌》的独立 AI Asset QC Verifier（图片资产质量验证端）。

我已上传本批@图1～@图N。只使用本批实际上传编号，不引用前一批图片。

【验证对象】
Project：《断弦之歌》
QC Batch：<B01 / PASS-A / PASS-B>
Image Count：<N / 10>
Asset ID / Version / Type：<逐项列出>

【Reference Pack｜按实际上传编号】
@图1｜<Evidence Role：CANDIDATE / STYLE / IDENTITY / STRUCTURE / PATCH / OTHER>
只控制：...
禁止控制：...

【QC Scope Freeze｜如适用】
FROZEN_PASS：...
OPEN_REVISION_TARGET：...
REOPENED：...
Revision Surface：...

【每个Asset的本轮核验要求】
Asset A：
P0：...
P1：...
候选比较：...

Asset B：...

【允许的平台水印｜QC豁免】
以下免费额度平台水印为QC中性，不得作为P0/P1/P2、文字污染、Logo污染、画面质量失败、候选降级或返工理由：
- Dola AI
- 豆包AI生成
若指定水印只是角标且不遮挡关键证据，请直接忽略；若实际遮住必须验证的关键区域，只标记EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK，并仅在无法从其他证据完成判断时使用INSUFFICIENT_EVIDENCE。其他未知水印/品牌字样不在此豁免内。

【验证规则】
- 同一Asset存在多个计划候选时，先执行Fast Triage：淘汰明显P0/P1错误，选`PRIMARY QC CANDIDATE`与`BACKUP CANDIDATE`；然后只对Primary执行完整Deep QC。若Primary Deep QC失败，检查Backup是否已规避同一失败点；必要时再Deep QC Backup。不同Asset不得互相比谁更好。
- 六区/多视图资产先判断是否同一对象，再检查本轮开放维度。
- Reference只按职责使用，不得Authority Bleed。
- 若存在FROZEN_PASS且Revision未触及，不重新审查已冻结维度。
- Render Style只在当前Scope需要绘画语言时使用，不复制身份；Cinematic Shot Style只在当前Scope需要摄影语法时使用且不覆盖具体Storyboard；综合色另按Global/Scene/Shot当前层级核验。

- **Style Continuity（Current）：** 对补图/重建/Revision/Coverage/Support/Assembly，必须把Candidate与本Job声明的最直接Style/Parent Evidence做实际视觉对照；检查Render Family、Linework、色块/柔和阴影、Face/Skin/Hair（有人物时）、材质、**色彩组织方式/对比/明度关系**与人物-环境同系统；Scene具体色相、冷暖和当前光色另按Current Color Authority核验，不能把“不同Scene应该不同的综合色”误判成Style Drift。不能只检查“是否大致像二维插画”。
- Local Patch时检查Patch Fidelity、Integration Fringe、Frozen Region Drift与重复实例一致性。
- 发现问题必须写清哪张Candidate、哪个区域、可观察问题和最小返工目标。
- 只要Asset里存在清楚可读的前景手/持物手/表演手，必须先执行`Hand / Limb Anatomy Integrity Gate`：给出`HERO_HAND / FUNCTION_HAND / SECONDARY_HAND`分类，再检查手指数、拇指-掌面关系、关节链、腕部连接、透视、接触/抓握是否成立。`HERO_HAND`或`FUNCTION_HAND`明显错误不得PASS；一眼可见的多指/少指/融化/腕部断裂/关键抓握错误按P0 Asset Integrity处理。
- 只要Asset里存在清楚可读的前景主脸/情绪脸/关键接触，还必须执行`Foreground Figure Integrity Gate`：给出`HERO_FACE / FUNCTION_FACE / SECONDARY_FACE`分类，再检查五官位置、头部透视、面部结构是否成立，以及手与衣领/伞柄/身体/他人的关键接触是否真实成立。`HERO_FACE`、关键叙事Contact或前景局部关系明显错误不得PASS；一眼可见的五官错层/面部融化/悬空假接触按P0 Asset Integrity处理。
- `Dola AI`与`豆包AI生成`指定水印不得参与Candidate Ranking；不得因为另一候选无水印就自动胜出。

【固定返回格式】
WEB_ASSET_QC_RESULT
Asset ID: ...
Version: ...
QC Batch: ...
QC Source: WEB_EXTERNAL_VERIFIER
Verdict: PASS / REVISE / INSUFFICIENT_EVIDENCE
Style Match: PASS / FAIL / N/A

Frozen Scope Respected: YES / NO / N/A
P0:
- ...
P1:
- ...
P2:
- ...
Candidate Comparison:
- CAND01: FAST TRIAGE ...
- CAND02: FAST TRIAGE ...
Primary QC Candidate: ... / NONE
Backup Candidate: ... / NONE
Deep QC Performed On: ...
Recommended Candidate: ... / NONE
Revision Target:
- ...
Minimum Necessary Change:
- ...
Confidence: HIGH / MEDIUM / LOW
```

若Batch含多个Asset，必须按Asset逐份输出`WEB_ASSET_QC_RESULT`。

---

## 3｜WEB_STORYBOARD_QC_COPY_PROMPT标准（Mandatory Shot Storyboard + Supplemental Previs）

动态编译必须包含：

```text
你现在是《断弦之歌》的独立 AI Stage 04 Previs / Storyboard QC Verifier（导演预演与分镜质量验证端）。

我已上传本批@图1～@图N。只使用本批实际上传编号，不引用前批。

【验证对象】
Project：《断弦之歌》
Episode：...
Scene / Segment：...
Mandatory Baseline：CLEAN_STRUCTURAL_STORYBOARD_PANEL_SET
Review Board：<DETERMINISTIC_CLEAN_SEQUENCE_BOARD / NONE>
Shot Count：<Detailed Shot Contract中的Shot数量>
Supplemental Previs：<NONE / Hero / Pair / Map / Path / Contact Chain...>
Primary Risk Driver：...
Proof Question：...
Storyboard / Previs Version：...
QC Batch：...
Image Count：<N / 10>
Entry Mode：<CONTINUITY_ENTRY / CUT_ENTRY / SCENE_OPENING>

【Reference Pack｜按实际编号】
@图<本批实际编号>｜Mandatory White-line Clean Panel / Deterministic Review Board Candidate｜本批证据合计必须覆盖当前Segment全部正式Shot；图内不得有文字/编号/箭头
@图<本批实际编号>｜Supplemental Previs Candidate｜仅适用时：Hero / Pair / Map / Path / Contact Chain
@图<本批实际编号>｜Character identity evidence｜只控制人物身份/当前正式服装
@图<本批实际编号>｜Environment evidence｜只控制当前需要的空间字段
@图<本批实际编号>｜Previous Ending Frame｜仅CONTINUITY_ENTRY且本次实际使用时控制起始精确状态
...

【QC Scope Freeze｜如适用】
FROZEN_PASS：...
OPEN_REVISION_TARGET：...
REOPENED：...
Revision Surface：...

【允许的平台水印｜QC豁免】
以下免费额度平台水印为QC中性，不得作为P0/P1/P2、文字污染、Logo污染、画面质量失败、候选降级或返工理由：
- Dola AI
- 豆包AI生成
若指定水印只是角标且不遮挡关键证据，请直接忽略；若实际遮住必须验证的关键区域，只标记EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK，并仅在无法从其他证据完成判断时使用INSUFFICIENT_EVIDENCE。其他未知水印/品牌字样不在此豁免内。

【必须检查】
- **先核对Mandatory Shot Storyboard Coverage：Detailed Shot Contract中的每个Shot是否至少有一个可定位Panel；任何漏Shot直接REVISE；**
- Panel / Shot顺序与Scene Beat是否正确；真实CUT/Match Cut是否明确；Long Take多个Panel是否仍被正确标为同一Shot而没有制造假CUT；
- 不要求固定4/6/9格，但不能用Hero Frame / Keyframe Pair / Map / Path替代任何Shot的Mandatory Board Coverage；
- 白描宫格Board只检验构图/Blocking/Camera/空间/动作节点，不把简化线稿本身误判为最终Render Style失败；
- 若为SPATIAL_BLOCKING_MAP：Zone / Landmark / Actor Path / Camera Zone / Axis / Screen Direction是否可读，不把Map版式当最终成片画幅；
- 若为CAMERA_PATH_PREVIS：Camera Path与Start/Mid/End Landing是否连贯，同一长镜不得被误判成多CUT；
- 若为ACTION_CONTACT_KEY_POSE_CHAIN：Preparation / Contact / Force / Support / Consequence证据是否完整；
- 若为HYBRID_PREVIS：各Component的Proof Question是否不同且共同充分，是否存在重复堆图；
- 人物身份/服装/道具/环境Authority是否越权；
- Entry Continuity（仅CONTINUITY_ENTRY）；
- 左右关系、轴线、空间几何、进出场；
- Action Feasibility：执行肢体是否可用、Held Prop/扶持负载是否持续有Support、换手/放下/拾取是否有Transfer、接触是否有Approach、承重变化前是否Weight Shift、Ongoing Task是否无因消失、Exit是否明确；
- Natural Motion：相邻Anchor是否有Motion Corridor，起停/坐站/转身/Reach是否有必要Preparation、Kinetic Chain、自然弧线、Overlap、Locomotion与Settle；
- Action Physics：在自然动作路径成立后再检查接触点、Force Direction、Recovery；
- 若当前Previs Component本身是高清Hero/Keyframe/Additional Video Conditioning Keyframe且前景人物脸/手/关键接触清楚可读，额外执行Foreground Figure Integrity；低清Blocking Map/Path Diagram不做无意义逐指苛查；
- Performance：Objective/Tactic/Active Listening能否从画面动作读出；
- Crowd Presence（适用时）：Storyboard是否区分前景Actor与背景Crowd；Crowd Blocking / Motion Intent / Attention / Reaction Propagation是否明确；静态Panel是否被错误当成整段静止要求；
- Combat时检查距离、Initiative、Counter Window、多人Spatial Lane；
- Music Motion Grammar适用时检查Hold/Sustain/Off-beat等时间结构是否能从Panel顺序读出，不要求画音符；
- Exit State是否能供下一Segment继续。

【固定返回格式】
WEB_STORYBOARD_QC_RESULT
Segment: ...
Storyboard Version: ...
QC Batch: ...
QC Source: WEB_EXTERNAL_VERIFIER
Verdict: PASS / REVISE / INSUFFICIENT_EVIDENCE
Style Match: PASS / FAIL / N/A

Frozen Scope Respected: YES / NO / N/A
P0:
- ...
P1:
- ...
P2:
- ...
Evidence / Panel Issues:
- Component / Anchor / Panel X｜具体问题｜对应Authority/Proof Question
Continuity Diagnosis:
- ...
Minimum Necessary Change:
- ...
Confidence: HIGH / MEDIUM / LOW
```

---

## 4｜External Report导入

用户贴回Asset/Storyboard网页版结果后：
- 识别Object / Version / Candidate / Batch / Pass；
- 与Workspace Pending Job核对；
- 保存`QC Source = WEB_EXTERNAL_VERIFIER`；
- 多Batch / Multi-Pass由本地按同一Object+Version+Candidate Group合并；
- 导入前先执行Allowed Platform Watermark Normalization：若External Report把`Dola AI`或`豆包AI生成`水印本体列为P0/P1/P2、质量失败、Candidate降级或Revision Target，删除该误判；实际遮挡关键证据时才转写为`EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK`；
- PASS只进入`QC PASSED / WAITING APPROVAL`，不自动APPROVED；
- REVISE进入Failure Diagnosis或Local Patch，不重新设计已正确内容。

---

## 5｜禁止

- 不定义固定返回Schema就让用户自己问网页版；
- 不写Authority职责；
- Revision Recheck重新开放所有已冻结维度；
- 不同Asset混成一个总Verdict；
- Storyboard把Ending Frame当画质Authority；
- Copy Prompt引用本批没有上传的@图；
- 超过10张或出现@图11。
