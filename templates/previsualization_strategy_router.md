# Previsualization Strategy Router（强制Shot分镜基线 + 自适应补充预演）｜Current Authority

> **最高规则：** 每一个正式`Shot`在进入Stage 05 Video之前，必须先被实际生成并批准的**纯净白描 Clean Structural Storyboard Panel Set**视觉覆盖。不存在“简单镜头直接跳过Storyboard”、也不存在“用彩色精修图/Keyframe/Shot Execution Frame替代白描Storyboard”的捷径。
>
> **核心：** `MANDATORY SHOT STORYBOARD BASELINE → RISK-DRIVEN SUPPLEMENTAL PREVIS → STAGE 04 QC/APPROVAL → VIDEO`。
>
> 宫格数量不是KPI，Panel数量也不等于Shot数量；但**每一个Shot必须至少在Mandatory Board里有可定位Panel Coverage**。长镜可以由多个Panel表达同一Shot的连续状态，不得因Panel数量制造假CUT。

---

## 1｜Mandatory Shot Storyboard Baseline（不可省略）

Stage 02完成Detailed Shot Contract + Segment Plan后，必须为当前Segment建立`SHOT_STORYBOARD_COVERAGE_PLAN`。**Baseline视觉风格只有一种：纯净白描Clean Panel。**

### A. `CLEAN_STRUCTURAL_STORYBOARD`｜唯一Mandatory Baseline：纯净白描Panel Set
用于快速、低成本、清楚证明：
- 每个Shot的构图、人物位置、前中后景、视线与遮挡；
- Shot之间真实CUT / Match Cut关系通过Panel顺序与外部Metadata证明，CUT字样本身不烧进图片；
- 同一Shot内部Start / Key Change / Landing等必要状态；
- Camera方向、运动路径、主体移动方向与空间落点。

白描可以是黑白/灰阶、清晰线稿、低装饰；图片内不得出现文字、数字、箭头、时间码、CUT或镜头说明。**它不是最终Render Style / Color / Identity Fidelity Authority**。

### B. `CLEAN_STORYBOARD_BOARD`｜白描宫格/Sequence Board（不是第二种Baseline风格）
它只能由A类Approved白描Clean Panels通过`tools/storyboard_grid_assembler.py`确定性拼版得到，用于整体查看Shot顺序与关系；**不得把“高可读故事版”解释成彩色精修或最终渲染风格，也不得由图像模型直接生成带字/箭头的整页。** 若人物身份细节对白描不足，补最小Rendered Human Anchor或后续Video Conditioning，但不得把该Rendered资产反向替代白描Baseline。

### Coverage硬要求
- `Detailed Shot Contract`里的**每个Shot ID必须至少被一个实际生成并批准的白描Baseline Panel覆盖**；
- 有明显位移、动作阶段、Focus/Camera变化或状态变化的Shot，必须增加足够Panel证明关键节点，不能只放一个静态Panel糊过去；
- Multi-shot Segment：每个Shot都必须可定位，真实CUT / Match Cut必须明确；
- Long Take / One-shot：可以多个Panel都属于同一Shot，必须标清`SAME SHOT / NO CUT`语义，Panel不能被错误解释成多个Shot；SAME SHOT / NO CUT只存在Metadata，不写进图片；
- Montage：每个实际Montage Shot至少有一个Panel；需要Match/节奏关系时补关键过渡Panel；
- 不规定固定4/6/9格。2/3/4/6/9或其他Layout按信息密度决定，但不得以“简化”为由漏Shot。

Stage 04如果没有实际生成并批准Baseline Board，统一标：
`MANDATORY_SHOT_STORYBOARD_MISSING`。

---

## 2｜Supplemental Previs（只能补充，不能替代Baseline）

Baseline Storyboard之后，再按Primary Risk Driver选择**可选补充Component**。以下形式全部失去“单独直通Stage 05”的资格：
- `SINGLE_HERO_FRAME`；
- `KEYFRAME_PAIR`；
- `ACTION_CONTACT_KEY_POSE_CHAIN`；
- `SPATIAL_BLOCKING_MAP`；
- `CAMERA_PATH_PREVIS`；
- `TRANSFORMATION_REVEAL_BOARD`；
- `MONTAGE_RHYTHM_BOARD`；
- `CONTINUITY_BRIDGE_BOARD`；
- 任何Hero/Map/Path/Anchor/Diagram。

它们仍可作为Supplemental Proof解决特定风险，但**不能替代Mandatory Shot Storyboard Coverage**。

`STANDARD_PANEL_BOARD / BLOCKING_SEQUENCE_BOARD`如果本身已经满足第1节全部Shot Coverage要求，可直接作为Mandatory Baseline，不需要再画第二套重复Board。

---

## 3｜Risk Driver（决定补什么，不决定能否跳Storyboard）

每个Segment先标一个`PRIMARY_RISK_DRIVER`，必要时最多两个Secondary：
- `COMPOSITION_EMOTION`
- `START_END_STATE_DELTA`
- `MULTI_BEAT_NARRATIVE`
- `BLOCKING_DISTANCE`
- `ACTION_CONTACT_PHYSICS`
- `SPATIAL_GEOGRAPHY`
- `CAMERA_PATH`
- `FOCUS_DEPTH_HANDOFF`
- `TRANSFORMATION_STATE_PROGRESSION`
- `MONTAGE_RHYTHM_MATCH`
- `CONTINUITY_HANDOFF`
- `CROWD_FLOW`

Risk Driver回答的是：**Baseline Board之外，还需要什么额外静态证据才能显著降低Video失败？**

常见补充：
- COMPOSITION_EMOTION → Hero Frame（可选）
- START_END_STATE_DELTA / FOCUS_DEPTH_HANDOFF → Keyframe Pair（可选）
- ACTION_CONTACT_PHYSICS → Contact Key Pose Chain（可选）
- SPATIAL_GEOGRAPHY / CROWD_FLOW → Spatial Blocking Map（可选）
- CAMERA_PATH → Camera Path Previs（可选）
- TRANSFORMATION → Transformation Detail/Reveal补充（可选）
- CONTINUITY_HANDOFF → Continuity Bridge补充（可选）

**没有Supplemental Risk并不等于没有Storyboard；只等于`Supplemental Previs = NONE`。**

---

## 4｜Stage 02输出：Shot Storyboard Coverage Contract

每个Segment必须记录：

```text
【Shot Storyboard Coverage Contract】
Segment：SEG-__
Mandatory Baseline Type：CLEAN_STRUCTURAL_STORYBOARD_PANEL_SET（固定；CLEAN_STORYBOARD_BOARD仅为确定性Review派生物）
Shot Count：__

SHOT_STORYBOARD_COVERAGE_PLAN
- SH01｜Panel __｜Start / Key State / Landing｜CUT semantics: ...
- SH02｜Panel __｜...｜CUT semantics: ...
...

All Shots Covered：YES / NO
Panel Count Rationale：<按真实信息节点，不按固定4/6/9 KPI>

Primary Risk Driver：<one>
Supplemental Previs：NONE / HERO_FRAME / KEYFRAME_PAIR / ACTION_CONTACT_KEY_POSE_CHAIN / SPATIAL_BLOCKING_MAP / CAMERA_PATH_PREVIS / ...
Supplemental Proof Question：<仅适用时>

Stage 04 Additional Video Conditioning Keyframe Review：NOT YET / REVIEW AFTER APPROVED STORYBOARD
Stage 03 Asset Accounting Impact：NONE
```

Stage 02只规划Coverage，不生成Stage 04图。

---

## 5｜Stage 02 Hard Gates

以下任一未解决，不得`DIRECTOR BREAKDOWN READY`：
- `MANDATORY_SHOT_STORYBOARD_NOT_PLANNED`｜存在Shot但没有Baseline Board计划；
- `SHOT_STORYBOARD_COVERAGE_GAP`｜至少一个Shot没有Panel Coverage；
- `STORYBOARD_FALSE_CUT_FAIL`｜连续Shot被Panel布局误写成CUT，或真实CUT被吞掉；
- `STORYBOARD_EVIDENCE_INSUFFICIENT`｜运动/Blocking/Camera/状态变化存在，但Panel不足以证明关键节点；
- `PREVIS_REDUNDANCY_FAIL`｜Baseline与Supplement重复堆同一信息；
- `PREVIS_DIRECTOR_AUTHORITY_BLEED`｜为适配Board格式改变Director Core。

旧`PREVIS_STRATEGY_NOT_ASSIGNED / PREVIS_MODE_RISK_MISMATCH / PREVIS_EVIDENCE_INSUFFICIENT`若出现在旧Workspace，迁移时映射到当前Coverage Contract，不得恢复“单Hero/Pair直通”的旧语义。

---

## 6｜Stage 04执行顺序

固定顺序：
1. 读取Reconciled Detailed Shot Contract；
2. 生成**Mandatory Baseline Board**；
3. 检查每个Shot Coverage + Cut Semantics + Blocking/Camera/Spatial继承；
4. 若有Supplemental Previs，再生成所需Hero/Pair/Map/Path/Contact Chain等；
5. 所有Required Component通过QC；
6. 用户明确批准；
7. 登记`APPROVED PREVIS SET`，其中必须包含`APPROVED MANDATORY SHOT STORYBOARD`。

Stage 04不得：
- 用一张Hero Frame代替Storyboard；
- 用Keyframe Pair代替Multi-shot Coverage；
- 用Spatial Map / Camera Path Diagram代替每Shot构图与Shot/Cut关系；
- 因为Shot很简单就跳过Baseline；
- 为了凑4/6/9格制造无意义Panel。

---

## 7｜PREVIS_HUMAN_ANCHOR边界

旧`PREVIS_HUMAN_ANCHOR`的Appearance Owner语义已废弃：
- `CLEAN_STORYBOARD_BOARD`只承担白描导演证据，不建立最终Face / Render / Color Authority；
- `CLEAN_STRUCTURAL_STORYBOARD`只承担Blocking / Silhouette / Pose / Action Beat；
- 任何清楚配角必须先继承Approved FMH/Minor Human Master；Rendered Human Anchor只能补姿态/表演/接触，不得首次发明人物外观；
- 反复/命名人物继续使用正式Character/FMH Authority。

---


## V4.4｜Storyboard → Video Conditioning Handoff

Mandatory Storyboard批准后**不能直接等价于VIDEO_GENERATION_READY**。下一步固定进入`VIDEO CONDITIONING ASSET BUILD`：

`APPROVED PREVIS SET → VIDEO CONDITIONING IN PROGRESS → CONDITIONING QC/APPROVAL → VIDEO CONDITIONING READY → Stage 05`

Whole Board / Panel仍可按Capability直接进入Video Reference Pack并保持Director/Temporal Authority，但它们默认是Control Reference，**不能仅凭Storyboard存在满足Primary Visual Conditioning**。

Mandatory白描Clean Storyboard Panel**禁止执行`PROMOTE_TO_VIDEO_CONDITIONING`作为Primary Visual**。它可以进入Video Reference Pack承担Director/Blocking/Temporal Control Reference；最终Primary Visual必须来自Approved Shot Execution Frame / Video First Frame / Target Frame / Key Pose等Video Conditioning资产。

详细Owner：`visual_asset_usage_authority.md` + `video_conditioning_asset_architecture.md`。

## 8｜Stage 05 Mandatory Storyboard Gate

Stage 05任何Final Video Prompt之前必须同时满足Mandatory Storyboard Gate与V4.4 Video Conditioning Gate：
- `MANDATORY_SHOT_STORYBOARD_COVERAGE = PASS`；
- 当前Segment所有Shot均存在Approved**白描**Baseline Panel Coverage，且`STORYBOARD_RENDER_MODE = WHITE_LINE_STORYBOARD_ONLY`；
- `APPROVED PREVIS SET`包含`APPROVED MANDATORY SHOT STORYBOARD`；
- Supplemental Component缺失只在其被Stage 02标为Required时阻断；
- Board/Panel作为真实视觉控制按`visual_reference_routing.md`进入Direct Board / Panel Multi-reference / Key Panel / Clean Panel等路线；不得因为是白描就默认退成纯文字；但视频模型若不能安全理解多Panel Board，优先传独立Clean Panels，不要求模型解释Grid时序；
- 白描图像上的所有说明保持零像素注释；Camera/Timing/Cut/Action/Performance/Eyeline/Relation等离图说明必须被Stage 05编译进Final Video Prompt，否则`STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP`。

若目标平台无法安全使用Whole Board，允许拆Panel或选择关键Panel；**平台Reference路由限制不等于可以省略Stage 04 Storyboard生产与批准。**

失败：
`VIDEO_BLOCKED_BY_MANDATORY_STORYBOARD_GAP`。

---

## 9｜Existing Project / Legacy Compatibility

升级到本规则时：
- 已APPROVED Video不因新规则失效；
- 已APPROVED但尚未进入Video的旧Previs若只有Hero / Pair / Map / Path，没有覆盖全部Shot的Board，保留为Supplemental Evidence并标`LEGACY_PREVIS_BASELINE_GAP`；
- 只补当前尚未生成Video的Shot所缺Mandatory Board，不重做无关Approved资产；
- 旧字段`Approved Storyboard`不再能指向“只有Hero/Pair/Map/Path”的集合；它必须能解析到`APPROVED MANDATORY SHOT STORYBOARD`。

---

## 10｜Cost Boundary

本项目静态图成本低于Video，因此Mandatory Storyboard属于**Video失败前置消解成本**，不是可删优化项。但仍禁止无意义堆Panel：

`ALL SHOTS VISUALLY COVERED ≠ MAXIMUM PANEL COUNT`

目标是：**每个Shot先被看见、验证、批准，再让昂贵Video模型执行。**

## V4.5｜Shot Relation Visualization Gate

Mandatory Storyboard不仅覆盖Shot本身，还必须可视化`SHOT_RELATION_GRAPH`中对当前Cut有决定性的事实：
- Attention Target在A镜头是否真正可读；
- Look/POV/Clue对象是否指向唯一目标；
- B镜头是否立即证明它是A所指向的对象/地点/后果；
- Match Cut / Action / Eyeline / Spatial Relation是否在相邻Panel中成立。

Storyboard文字写着“CUT”但画面没有建立Cut Motivation，判`SHOT_RELATION_STORYBOARD_MISMATCH`。不得等Video阶段靠Prompt解释。

## Contact Sheet First Storyboard（新增）

当场景包含多个Formal Shot，或虽为单Shot但内部动作Beat很密时，Storyboard默认优先选择`CONTACT_SHEET_FIRST`：
1. 先生成一张完整白描Contact Sheet（4/6/9/12/16/25...）；
2. 通过匿名化、Blocking、Camera、Action、Editorial QC；
3. 再运行`tools/storyboard_contact_sheet_splitter.py`确定性切格，得到独立Clean Panels；
4. Stage 05继续使用这些切出的Panel和其Metadata，而不是把整张宫格直接当Primary Visual送视频模型。


## V4.5.7｜PREVIS_HUMAN_ANCHOR Appearance Ownership Deprecated

`PREVIS_HUMAN_ANCHOR`不再允许成为、共同承担或替代清楚配角的Appearance Owner。Stage 04 Previs只能继承已Approved的Character/FMH身份与画风，用来证明姿态、动作、Blocking或Contact。任何Readable Scoped Cast缺人物母图都必须回Stage 03补`FUNCTIONAL_MINOR_HUMAN_ASSET`。
