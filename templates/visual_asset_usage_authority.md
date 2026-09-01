# Visual Asset Usage Authority｜V4.4

> **目的：** 定义《断弦之歌》每一种静态图片“是什么、能控制什么、能不能直接进入Video、能不能作为Primary Visual Conditioning”。本文件管理**使用权限**，不决定具体镜头构图。

## 1｜核心原则

1. **可以上传 ≠ 可以主导最终画面。** Color Board、Style Board、Environment Design Board、Whole Storyboard都可以按平台能力进入Video Reference Pack，但只能控制授权字段。
2. **Primary Visual Conditioning必须是镜头级、单画面、状态准确的Approved视觉资产。** 没有Primary Visual时，不得仅靠多个辅助Reference拼成`VIDEO_GENERATION_READY`。
3. **一张图一个主要职责。** Identity / Environment / Color / Director Timeline / Primary Frame可以由不同图承担；不得因为多图输入就把它们平权。
4. **权限由Asset Metadata声明。** Resolver不得凭文件名、画面“看起来像”或历史习惯自行提升权限。
5. **Promotion必须显式发生。** Storyboard Panel、Shot Assembly或Environment View只有经过Shot-specific QC并登记`PROMOTED_TO_VIDEO_CONDITIONING`后，才能成为Primary Visual。

## 2｜视觉Authority等级

### A. CANON / OBJECT AUTHORITY
用于回答“对象/地点是什么”。例如：
- CHARACTER_MASTER
- TRANSFORMATION_MASTER
- ENVIRONMENT_CLEAN_CANON
- ENVIRONMENT_COVERAGE
- PROP_MASTER / PROP_COVERAGE

可以直接作为Video辅助Reference；默认**不自动满足Primary Visual Conditioning**，因为它们通常没有锁定当前Shot的完整构图与World State。

### B. DESIGN / STYLE CONTROL
例如：
- ENVIRONMENT_DESIGN_BOARD
- MECHANISM_DESIGN_BOARD
- COLOR_STYLE_BOARD
- RENDER_STYLE_BOARD
- MATERIAL_BOARD

允许进入Video Reference Pack，分别控制设计细节、材质、综合色、Render Style。它们默认：
- `direct_video_input_allowed = true`（平台允许视觉Reference时）；
- `primary_visual_eligible = false`；
- 不得控制Camera、Shot Layout、Blocking、First Frame Composition。

### C. DIRECTOR / TEMPORAL CONTROL
例如：
- STORYBOARD_WHOLE_BOARD
- STORYBOARD_PANEL
- CAMERA_PATH_MAP
- FIRST_LAST_PLANNING_PAIR

允许按Capability直接视觉绑定，拥有Shot / Composition / Blocking / Temporal Beat / Cut等被批准字段。Whole Board默认不是Primary Visual，因为宫格/文字/箭头/多时刻并非最终单画面。

`STORYBOARD_PANEL`只有满足以下全部条件才可Promotion：单Shot、单画面、最终比例、无文字/箭头/宫格边框、人物/场景/服装/道具/World State准确、Render/Color达到视频入口要求、通过Video Conditioning QC。

### D. VIDEO CONDITIONING AUTHORITY
允许作为Primary Visual：
- VIDEO_FIRST_FRAME
- VIDEO_SHOT_EXECUTION_FRAME
- VIDEO_TARGET_FRAME
- VIDEO_LAST_FRAME
- VIDEO_KEY_POSE
- VIDEO_CONTACT_FRAME
- VIDEO_CUT_EXIT_FRAME
- VIDEO_CUT_ENTRY_FRAME

这些资产必须是**Shot-specific**，并记录`shot_id / video_unit_id / time_scope / source_refs / approval_ref / fingerprint`。

## 3｜默认权限矩阵

| Asset Type | 可进入Video Reference Pack | 默认Primary Visual | 主要职责 |
|---|---:|---:|---|
| Character Master | YES | NO | 身份/服装/体态 |
| Environment Clean Canon | YES | NO | 地点几何/材质 |
| Environment Coverage | YES | CONDITIONAL PROMOTION | 当前方向/固定结构 |
| Prop Master/Coverage | YES | NO | 道具结构/状态 |
| Environment/Mechanism Design Board | YES | NO | 设计细节/材质 |
| Color Board | YES | NO | 色彩/明度/综合色 |
| Style Board | YES | NO | Render Style |
| Storyboard Whole Board | YES | NO | Shot时序/Blocking/Cut/Camera Intent |
| Storyboard Panel | YES | CONDITIONAL PROMOTION | 当前Panel构图/Blocking |
| Shot Assembly | YES | CONDITIONAL PROMOTION | 人景物组合 |
| Production Support Reference | YES | CONDITIONAL PROMOTION | 接触/瞬时状态/局部风险 |
| Performance Support | YES | NO | 特殊表情/动作姿态/Contact静态形态 |
| Narrative FX Reference | YES | NO | 剧情型FX形态/状态/静态环境交互 |
| Narrative FX State Sheet | CONDITIONAL | NO | 多状态Canon拆解，默认先派生单帧或Execution Frame吸收 |
| Approved Video Conditioning Frame | YES | YES | 最终Video入口画面 |

## 4｜Promotion规则

已有资产可以避免重复生成，但必须经过显式Promotion：

`Existing Visual Asset → Shot Contract Match → Current State Projection → Clean Frame QC → VIDEO CONDITIONING PROMOTION PASS`

Promotion只在**整张图已经等于当前Video Unit所需静态状态**时成立。不能只因为：
- “是高清图”；
- “是Approved资产”；
- “是Storyboard Panel”；
- “看起来差不多”；
- “Reference槽位不够”；

就升级为Primary Visual。

## 5｜辅助Reference Role Lock

辅助图进入Video时必须有最短职责句：
- Color Board：只取综合色/明度/冷暖，不复制色块/排版；
- Design Board：只取设计细节/材质，不复制拼版/边框；
- Whole Storyboard：只取Shot时序/Blocking/Camera/Cut，不复制宫格/文字；
- Style Board：只取绘画语言，不复制示例人物/版式。

Role Lock不是万能补丁。如果当前平台已真实发生Layout Literalization，应由`visual_reference_routing.md`升级到Panel Split / Clean Crop / Dedicated Channel，而不是继续靠文字硬压。

## 6｜Hard Gates

- `PRIMARY_VISUAL_CONDITIONING_GAP`：Video Unit没有Approved Primary Visual。
- `DIRECT_VIDEO_ELIGIBILITY_FAIL`：被标为Primary的资产没有Direct Video Eligibility。
- `ASSET_ROLE_ESCALATION_FAIL`：辅助资产未经Promotion擅自取得Primary Visual权限。
- `LAYOUT_LITERALIZATION_RISK_UNROUTED`：已观察到拼板/宫格/色板版式复制，却仍按同一路线直绑。
- `ASSET_USAGE_ROLE_CONFLICT`：同一图片在同一任务承担互相冲突的Authority。

## 7｜重要边界

本规则**不禁止**设计板、色板、Whole Storyboard进入Video。它只禁止：

> **用辅助Authority代替缺失的Shot-specific Primary Visual，然后把昂贵Video Take当成构图/空间/状态试错工具。**

## V4.5｜Relation Role Metadata

视觉资产除了Identity/Color/Spatial/Primary等字段Authority，还可以承担**关系证明角色**：
- `CLUE_SOURCE`
- `LOCATION_VISIBILITY_PROOF`
- `LOCATION_IDENTITY_PROOF`
- `CUT_EXIT`
- `CUT_ENTRY`
- `MATCH_MOTIF`
- `POV_TARGET`

关系证明角色不会自动把辅助资产提升为Primary Visual；它只说明该图在Shot Relation Contract中证明哪条事实。Resolver必须保留这种Role，不得把“同一Location Entity”的证明误简化成普通Environment Reference。


## V4.5.2 Clean Storyboard
正式Storyboard视觉资产默认是`CLEAN_STORYBOARD_PANEL`或由其确定性拼成的Clean Sequence Board。带文字、箭头、时间码、CUT、Shot/Panel Label的图片不再是本项目正式Storyboard产物；这些信息属于外部Metadata。Planning Diagram可保留文字/箭头，但其`primary_visual_eligible=false`。


## V4.5.3｜Evidence-backed Usage

`allowed_roles / primary_visual_eligible / direct_input_allowed`仍是资产设计权限；Text-only Controller还必须读取Current Visual Evidence确认“这一个具体文件版本实际没有违反该角色”。设计权限不能替代对真实生成结果的观察。

## V4.5.7｜Lineage / Color Consumption

`VIDEO_SHOT_EXECUTION_FRAME`等Primary Visual必须带可追踪Lineage，不允许作为无父来源的孤立最终图。对Scene-bound任务，`scene_color_authority_id`是独立必需字段：Primary Visual负责最终静态构图并承载已经烘焙进去的当前综合色结果，Scene Color Card仍是综合色/明度/光色关系的上游Authority。**Authority必须存在，但不等于Final Video每次都要再次Direct Bind色卡。**

## V4.5.7｜Primary Visual Identity Readability Boundary

`primary_visual_eligible=true`只代表资产类型允许承担Primary Visual，不代表这一个具体文件在当前镜头尺度下足以承担人物Identity。

对命名/身份关键人物：只有`IDENTITY_READABILITY_ASSESSMENT`在平台有效缩放尺度得到PASS，Primary Visual才可作为该人物唯一身份视觉依据。FAIL/UNKNOWN时必须额外Direct Bind真实人物Identity Authority或重生可读执行帧。

Storyboard Whole/Panel（白描）只拥有Blocking/Timing/Camera/Action权限；Environment Clean Canon/Coverage只拥有空间/材质/Geometry权限；二者均不具备补人物Identity Readability的权限。

## V4.5.7｜Performance / Narrative FX Usage Boundary

- Performance Support必须继承Character/FMH Identity，不得晋升为人物Identity Authority；
- Narrative FX Reference不得晋升为Environment/Prop Canon；
- 两类资产都不能代替Shot-specific Primary Visual Conditioning；
- `MULTI_PANEL` Performance Sheet / Narrative FX State Sheet默认不直接绑定Final Video；
- 项目执行策略禁止Reference Video，不能用视频参考替代表演/FX静态Authority。
