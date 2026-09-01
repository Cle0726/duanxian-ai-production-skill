# 03.1｜人物资产标准模板


## 1. 资产定位
人物资产是分镜/视频/海报/连续性所依赖的正式母资产，不是普通角色插图。

## 2. 项目标准资产语言
### 日常 / 当前剧情阶段（Normal / story-phase）
- DV-01：2×2人物资产页（FRONT FACE / SIDE FACE / FRONT BODY / BACK）
- DF-01：标准正脸
- DF-02：标准3/4脸
- EX-01：六宫格表情表
- HA-01：头发结构页
- PR-01：人物关联核心道具页（需要时）
- AD-01：Signature Adornment Detail（个人标志装饰高清局部页，按需）

### 变身角色（Transformable characters，仅剧情明确时）
- TF-01
- TE-01~TE-05
- TH-01
- TC-01
- TM-01
- WP-01
- TS-01
- FX-01

变身角色必须同时读取 `transformation_asset_standard.md`。其中 `TF-01 / TE-03 / TH-01 / TC-01 / WP-01` 组成Canonical Transformation Master Set（正式变身母资产组）；它们是正式设计基准，不代表每个镜头都要同时引用。`TM-01 / FX-01` 为按需资产，不为凑清单机械生成。

这些是标准语言，不代表每名人物机械生成全部项目；以实际生产需求和Registry（资产登记表/台账）为准。

### 2.1 Identity Lock Set（主要人物身份锁定组）
对**主要 / 反复出现 / 可变身角色**，`DV-01`不能长期作为唯一脸发Authority。默认身份锁定组至少包括：
- `DV-01`：2×2总身份/服装/正侧背；
- `DF-02`：标准3/4脸，验证Face ID在非正侧角度仍成立；
- `HA-01`：头发结构页，锁远景剪影、分缝/刘海、脸旁发、侧面体积、后发与发尾。

此外必须读取`character_asset_requirement_set.md`建立该角色本集`Character Asset Requirement Set`：`DF-01 / AD-01 / PR-01`只在真实镜头与识别风险需要时升级为REQUIRED。若DV-01的FRONT FACE像素或面部细节仍不足，可生成`DF-01`标准正脸；若个人装饰在近景成为Critical且DV-01不足以锁定，生成`AD-01`；剧情关键人物关联物件则走`PR-01 / Prop Authority`。可变身角色另由`TE-03`锁Transformation Eye Signature、`TH-01`锁变身发型结构。

这不是为了“资产齐全”机械出图，而是因为脸/发/关键个人装饰属于高频下游Authority；图片成本低时应在Stage 03把可预见的静态识别风险提前消掉。

## 3. DV/TF固定格式

**Canvas Authority：必须先读取 `asset_aspect_ratio_authority.md`。** `DV-01 / TF-01`整张人物四视图母图固定使用**9:16竖向高分辨率画布**，不是16:9。Style Board / Color Card或最终视频的横向比例不得覆盖人物资产比例。

- 9:16 vertical / portrait-oriented full sheet
- 2×2
- FRONT FACE / SIDE FACE / FRONT BODY / BACK
- 纯净中性背景
- 同一柔和光
- 无剧情动作
- 无夸张透视
- 四格必须是同一个人、同一版本、同一服装、同一材质和比例

## 4. EX-01
默认使用**9:16竖向高分辨率画布 + 2×3六宫格**。同一人物、接近同一头部角度/光线，使用眼神、眼睑、眉、嘴唇/下颌与面部肌肉张力表现差异，不改变脸型。

`DF-01 / DF-02 / HA-01`同属人物身份/造型资产，默认同样使用9:16竖版。TE眼部超近特写、WP武器等专项资产按 `asset_aspect_ratio_authority.md` 的例外规则执行。

## 5. 《断弦之歌》人物资产画风
人物资产必须严格遵守 `project_style_dna.md`。最重要的人物画风规则如下：
- 明确的 anime-influenced 2D illustrated character art（动漫影响的二维角色插画），不是照片、3D或游戏角色。
- clean hand-drawn linework（清楚稳定的手绘线稿）必须保留，不能粗黑漫画化，也不能完全无描线；人物要先由线稿和色块立形，再叠柔和阴影。
- matte painted skin（哑光绘画皮肤），平滑干净、无毛孔、无摄影肤质。
- 理想化但克制的欧洲骨相，但**不允许全员共用同一标准美型脸**；脸型、面中、下颌、鼻唇、眉眼关系必须按角色区分。眼睛可略大但自然，结构与默认视线要角色专属；`semi-realistic` 只修饰骨相，不主导整张脸向真人写实漂移。
- 头发先组织大块发束，再少量细丝丰富边缘，不做照片级逐根毛发。
- 项目叙事总体可保持欧陆、克制、文学感，但**人物自身气质不得被统一成“忧郁安静”模板**。外向、锋利、温暖、傲慢、顽皮、严谨、疲惫等角色性格应通过其Face ID / Eye ID / Hair ID / posture真实体现；统一的是画法，不是默认表情。
- 色彩服从Global Color DNA的综合色组织：色族集中、明度层级清楚；人物肤色、服装识别色与材质可以保留自然综合色存在感，不做统一低饱和/低对比/带灰度硬锁。黑色在出现时保留层次，浅色与暖光按当前Scene真实光色关系处理。
- 人物差异来自身份、骨相、年龄、发型、服装、表情与气质，不来自渲染风格改变。

## 5.1 新人物统一抽卡规则

当角色尚无APPROVED Character Master时，不从零猜画风，也不直接复制任何现有角色外貌。必须读取 `new_character_generation_recipe.md`，继承项目已经验证成功的二维插画Prompt结构、去写实策略、皮肤/头发/线稿/综合色语言，再为新人物单独设计骨相、脸型、眉眼、发型、体型、气质与当前完整服装。

一旦该新人物的Character Master被用户批准，后续身份一致性以其自己的APPROVED Character Master为最高人物视觉依据；通用Recipe不再替代身份母图。

## 5.1.1 Face / Hair / Eye Identity Lock（脸 / 发 / 眼身份锁）

正式主要/反复角色必须读取：
- `character_identity_differentiation_engine.md`
- `face_identity_matrix.md`
- `hair_identity_architecture.md`

生成前建立`Identity Distinction Card`。统一画风不得覆盖个体差异：
- 脸型、面中、下颌/下巴、鼻/嘴、眉眼关系必须有角色专属组合；
- 发型必须在远景轮廓、中景结构、近景发束三个尺度可区分；
- FRONT FACE / SIDE FACE必须读得出Face ID与Eye ID；BACK必须读得出真实后发架构；
- 不允许“同一张标准美脸 + 换发色/衣服”通过QC。

主要/反复角色若`DV-01`不足以锁定身份，应建立现有标准里的`DF-01 / DF-02 / HA-01`，不是靠Prompt文字长期维持。

**既有APPROVED保护：** 当前版本反模板规则不自动重做已经批准的人物。旧角色保持现有Authority；新人物必须避开旧角色模板，旧角色只有在用户明确要求或批准正式修订时才改。

## 5.1.2 Personal Adornment Identity Lock（个人装饰识别锁）
主要 / 反复角色必须读取 `personal_adornment_identity_system.md`。正式人物差异化由`Face / Hair / Eye / Wardrobe / Adornment`五层共同组成；人物母图不是默认“无首饰/无装饰”：需要主动判断SIGNATURE / ROTATING / FUNCTIONAL / MINIMAL / INTENTIONAL_NONE。

- 稳定个人装饰必须在DV-01相关角度保持位置、大小、形状与材质一致；
- 不得为了“丰富”机械堆耳环、项链、戒指；
- 不得为了“克制”让整个主要群像全部空白；
- 若装饰很小但属于重要识别点且会反复近景出现，可建立AD-01；
- 若物件承担剧情因果，则升级Prop Authority，不继续当普通Adornment。

## 5.2 圣谱者变身规则

当剧情明确角色可变身时，日常Character Master仍负责“这个人是谁”，变身资产负责“这个人如何显影为圣谱者”。不得用变身礼服反向覆盖日常身份，也不得把20世纪晚期日常服装规则强塞给剧情明确的圣谱者战斗礼服。具体执行统一读取 `transformation_asset_standard.md` + `music_identity_mapping.md` + `transformation_beauty_core_five.md`：先完成Music Identity，再建立礼服、眼影/眼周、头发、瞳孔/虹膜、音乐武器五核心。

TF-01 / TE-03生成前同时读取`eye_signature_ledger.md` + `musical_eye_motif_system.md`：先锁Base Eye Identity，再建立`Primary Eye Signature + Secondary Graphic（MAIN/CORE）+ optional Periocular Emblem + Musical Origin Trace`并做全项目碰撞。允许LITERAL_NOTATION / DERIVED_MUSICAL_GLYPH / MUSICAL_GEOMETRY，不强迫标准音符贴脸；已有APPROVED TE-03后，它成为Transformation Eye Design Authority，但仍必须继承日常眼型与眉眼身份。

## 5.3 Character Appeal & Silhouette（角色魅力与剪影）

无论日常人物还是圣谱者变身，只要角色是正式可传播的核心人物设计，都必须同时读取 `character_appeal_silhouette_system.md` + `body_identity_presentation_authority.md`。日常造型还必须读取 `wardrobe_style_design_engine.md` + `wardrobe_diversity_design_matrix.md`；主要/反复出现角色同时读取 `character_closet_registry.md`。

最少要说明：
- `Primary Appeal Hook`（主要魅力焦点）
- `Secondary Appeal Hook`（次级魅力焦点）
- `Exposure Geometry`（开放区域几何）
- `Body-Line Emphasis`（身体线条重点）
- `Silhouette Hook`（剪影焦点）
- `Boldness Dial`（RESTRAINED / ASSERTIVE / BOLD / EDITORIAL；成年角色）

原则：
- 成年角色除非剧情明确要求封闭/禁欲/监察/人工秩序感，否则不应默认全包保守化；
- 女性角色不能全部依赖同一种“短裙+大腿/露肩”模板；
- 男性角色不能全部收敛为“高领+长外套+全包死”；
- 角色魅力必须和人格、时代感、功能性与项目统一画风一起成立；
- 季节/场景换装不得无理由抹掉既有Primary Appeal Hook、Body-Line Emphasis与Silhouette Hook；读取`body_identity_presentation_authority.md`区分Body Identity与当前LOOK的呈现方式。冷天/功能装可用DIRECT / FRAMED / PROPORTIONAL / IMPLIED / CONTRAST等方式保留身体美，宽松/Oversized本身不构成失败；只有Body Identity漂移或整套Look无理由吞掉Appeal时才返工；
- 未成年人物只做辨识度、可爱/气质与剪影魅力，不使用成人身体性感化规则。


## 6. 参考图职责
- Render Style Anchor / Approved Style Evidence：只管“怎么画”，不管人物是谁；Cinematic Shot Style不参与Character Master身份画布。
- Approved Character Master（已批准人物母图）：只管人物身份 + 当前剧情阶段正式服装。
- Task-specific Reference（当前任务专项参考）：只管这次要做的眼睛/头发/礼服/武器等结构。
- Storyboard / Pose / Scene / Ending Frame（分镜 / 姿势 / 场景 / 尾帧）：只管动作、空间和连续性，不能升级成新的人物身份来源。

## 7. 防链式污染
临时生成图不得因为“最新”就替代原批准风格锚点/人物主资产。若需修订正式主资产，显式产生新版本并重新QC（质检）/批准。

### 7.1 Clean Input / Master Patch
人物Master首先是下游机器可读的Identity / Design Authority：保持中性背景、柔和可读光、清楚轮廓与材质边界；不要把单场雨雾、战斗逆光、强综合色、爆闪烤进身份母图。

APPROVED Master若只有局部问题，默认冻结脸、体型、服装大结构、综合色等正确区域，只对授权区域做Mask / Local Patch，再合成回Base Master并重新QC。不得为了一个扣件、链条、手指或局部阴影整张重生。具体读取 `personal_creator_cost_efficiency_engine.md` + `inpaint_local_patch_authority_engine.md`。若用户已有“正确局部图案/结构参考”，必须单独@为PATCH_DESIGN_AUTHORITY；人物母图自身只作为EDIT_TARGET。

## 8. QC（质检）
- Identity（身份）：还是不是同一个人。
- Design（设计）：服装、发型、结构有没有跑。
- Style（画风）：还是不是《断弦之歌》统一二维画法。
- Distinction（个体差异）：Face / Hair / Eye / Wardrobe有没有和现有角色模板撞型。

任一不通过，不进入Stage 04/05。


## Body Identity Lock补充
人物母图锁定稳定Body Identity；具体LOOK只改变Body Presentation Mode，不得因宽松/贴身服装改变人物本身肩胸腰胯腿比例。详细读取`body_identity_presentation_authority.md`。


## Source Wardrobe Adaptation补充
人物正式LOOK若来自小说/剧本服装描写，必须先读取`source_wardrobe_adaptation_authority.md`分类。普通描述只作Soft Evidence；只有真正影响剧情/身份/连续性的`WARDROBE_PLOT_FACT`锁必要字段。最终服装仍由Stage 03 Skill Wardrobe设计。
