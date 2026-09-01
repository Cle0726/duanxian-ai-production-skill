# Video Conditioning Asset Architecture｜V4.4

> **最高原则：** 每一个正式Video Unit在消耗Video Take前，必须先完成一次“最终静态化”：把Approved Canon + Current World State + Approved Storyboard合成为可直接执行的Primary Visual Conditioning Asset。复杂度决定需要几张，不决定“有没有”。

## 1｜它解决什么

Stage 03回答：人物/场景/道具是什么；Stage 04 Storyboard回答：导演怎么拍；本层回答：

> **“这个Video Unit真正送进视频模型的第一幅/关键静态画面到底长什么样？”**

因此它位于`APPROVED PREVIS SET`之后、`VIDEO_GENERATION_READY`之前。

## 2｜输入Authority

必须继承当前有效版本：
- Approved Storyboard / Detailed Shot Contract；
- Character / Transformation / Wardrobe / Adornment；
- Environment Clean Canon / Coverage / Geography；
- Prop / Weapon / Vehicle；
- Current World State / Injury / Damage / Weather / Crowd；
- Color / Style；
- Previous Approved Ending Frame（CONTINUITY_ENTRY时）；
- 必要Production Support / Shot Assembly。

本层不得创造新Canon、不得改Director Core、不得把辅助Reference版式抄进最终Frame。

## 3｜Video Unit最小资产计划

### SIMPLE_STATIC / LIGHT_MOTION
最低：`VIDEO_FIRST_FRAME` 1张。

### CAMERA_MOVE_WITH_EXPLICIT_TARGET
最低：`VIDEO_FIRST_FRAME + VIDEO_TARGET_FRAME`。
适用于明确推近/拉远/移到另一构图；Target Frame锁落点，不要求视频模型自行猜“推到哪里”。

### STATE_CHANGE / PERFORMANCE_TRANSITION
最低：`FIRST + LAST`；中间状态容易漂时增加`KEY_POSE`。

### PROP_HANDOFF / COMPLEX_CONTACT
最低：`FIRST + CONTACT_FRAME`；落点重要时增加`LAST`。

### COMBAT
最低：`FIRST + CONTACT/KEY_POSE + LANDING`，数量由真实Beat决定，不按固定三张KPI。

### TRANSFORMATION
最低：`BEFORE + TRANSFORMATION_KEY + AFTER`；复杂变身可增加关键阶段，但不无脑逐秒画。

### HARD_CUT / SPACE_DISCONTINUITY
默认把Cut两侧视为不同Video Unit：
- A：`CUT_EXIT_FRAME`（若Exit构图重要）
- B：`CUT_ENTRY_FRAME` / `FIRST_FRAME`

若目标平台已验证能够在单一Video Job内稳定完成多Shot硬切，可以保留单Job，但A/B两个Sub-unit仍必须各自有time-scoped Primary Visual；不得让A/B场景辅助资产同时无边界地参与全时段。

## 4｜Shot Execution Frame生成

标准路径：

`Approved Storyboard → Resolve Current State → Resolve Visual Asset Roles → Generate/Promote Shot Execution Frame → Static QC → User/Batch Approval → VIDEO_CONDITIONING_READY`

优先复用：如果已有Approved Storyboard Panel / Shot Assembly / Coverage View已经完全满足当前静态状态，可执行Promotion，不必重新生成。

## 5｜画面洁净要求

Primary Visual Conditioning必须：
- 单一最终画面，不是多格拼版；
- 无标题、Caption、箭头、时间轴、Reference边框；
- 最终输出比例正确；
- 只出现Shot Contract允许的可见人物/群众/道具/状态；
- Camera Distance / Height / Axis / Composition / Blocking与Storyboard一致；
- 人物身份、Current Look、伤势、Prop持有、环境状态正确；
- 不把Color/Style/Design Board的排版本身复制进画面；
- 静态几何、脸、手、关键接触先通过图片QC。

## 6｜Environment Clean Canon + Current State合成

长期场景Parent必须尽量保持Clean：固定建筑、固定家具、稳定地标、基础材质。以下剧情临时内容默认属于Current State，不烤进Parent Canon：
- 临时顾客/路人/剧情人物；
- 打碎的杯子、临时散落物；
- 血迹、烟、火、爆炸、临时破坏；
- 当前Shot特殊天气/照明效果（除非它是该地点长期Canonical状态）。

Shot Execution Frame再把Clean Canon与Current State合成。这样复用地点时不会把旧剧情状态永久带回。

## 7｜Reference Pack关系

Primary Visual不是唯一Reference。最终Video仍可同时使用：
- Character Master（Identity）
- Environment / Design Board（Geometry / Design）
- Color Board（Color）
- Style Board（Render）
- Whole Storyboard（Timeline / Cut / Blocking）

但它们都是字段级Authority。**Primary Visual负责最终镜头静态画面入口。**

## 8｜Cost原则

图片便宜、Video Take昂贵，因此：
- 每个Video Unit至少做1个Primary Visual；
- 复杂度只增加必要Keyframe；
- 有可Promotion的Approved资产就复用；
- 静态错误必须在本层修，不把“先抽一条Video看看”当QC策略。

## 9｜Hard Gates

- `VIDEO_CONDITIONING_PLAN_MISSING`
- `PRIMARY_VISUAL_CONDITIONING_GAP`
- `SHOT_EXECUTION_FRAME_STATE_MISMATCH`
- `UNSCRIPTED_VISIBLE_ENTITY_FAIL`
- `TRANSIENT_STATE_BAKED_INTO_CANON_FAIL`
- `MULTIPANEL_PRIMARY_VISUAL_FAIL`
- `VIDEO_CONDITIONING_PROMOTION_FAIL`
- `CUT_TIME_SCOPE_REFERENCE_BLEED`

## V4.5｜Pairwise Boundary Conditioning（边界成对静态化）

V4.4要求每个Video Unit有Primary Visual；V4.5再要求：**当两个Video Unit之间存在有意义的Shot Relation时，边界必须成对验证，而不是只分别检查两张图。**

对`CLUE_REVEAL_CUT / LOOK_POV_REVEAL / MATCH_CUT / CONTINUITY_CUT / ACTION_CONSEQUENCE`等：

`A_EXIT (or A relevant end state) ↔ Relation Contract ↔ B_ENTRY`

必须共同回答：
- A离开前是否真的建立了source_visual_fact / Attention Target；
- B进入时是否立即呈现destination_visual_fact；
- shared entity / location identity / motif是否成立；
- 是否发生未经授权的空间融合、物件穿越或“模型自己发明连接”。

`HARD_LOCATION_CUT`若导演明确要求无语义/空间桥，可声明`NO_SPATIAL_CONTINUITY_REQUIRED`，但仍需证明这是有意断开，不是缺失规划。

失败：`CUT_PAIR_ALIGNMENT_FAIL / CLUE_REVEAL_PAIR_FAIL / LOCATION_IDENTITY_PAIR_FAIL / ARBITRARY_ENTRY_FRAME_FAIL`。

## V4.5.7｜Master Lineage + Scene Color Continuity

Video Conditioning不再把Shot Execution Frame视为孤立新图。每个新生成/Promotion的Primary Visual必须登记：
`parent_asset_ids / source_generation_job_ids / scene_color_authority_id`。

标准血缘：
`Approved Master/Coverage + Current World State + Approved Storyboard + Scene Color Card → Shot Execution Frame → Video Job`。

综合色硬规则：
- 当前Video Unit必须有`scene_color_authority_id`；
- Primary Visual必须登记并继承同一个`scene_color_authority_id`；
- `scene_color_reference_mode`必须明确为`LINEAGE_ONLY / TEXT_CONTROL / DIRECT_REFERENCE`。默认`LINEAGE_ONLY`；
- 只有`DIRECT_REFERENCE`模式时，`required_reference_bindings`才必须包含该Scene Color Asset且`role = COLOR_AUTHORITY`；非Direct模式不得为“保险”继续占槽；
- Named Asset平台生成Shot Execution Frame时仍必须`@对应Scene Color Card`，因为这是上游综合色烘焙阶段；进入Video Job后是否再次@由Reference Budget决定。

失败：`VIDEO_COLOR_BINDING_MISSING / VIDEO_COLOR_REFERENCE_MODE_CONFLICT / SCENE_COLOR_BINDING_MISSING / ASSET_LINEAGE_GAP`。

## V4.5.7｜Identity Readability is not Resolution

Shot Execution Frame生成后新增一次`PLATFORM-SCALE IDENTITY READABILITY QC`。对命名/身份关键人物，原图高清、文件很大、镜头整体漂亮都不能替代平台有效尺度身份核验。失败时不必推翻该Primary Visual的Composition Authority，但必须把对应Character/FMH Master作为Direct Identity Authority，或重生身份可读的执行帧。

## Multimodal All-Round Reference Default

Stage 04B / Stage 05默认按`MULTIMODAL_ALL_ROUND_REFERENCE`规划：一个Video Unit可以组合人物图、场景图、道具图、Storyboard Panel、Execution Frame、Ending Frame，以及已登记的音频Reference。动作与运镜只能由Storyboard/Action Key Pose/Camera Path Metadata/文字执行约束表达，禁止使用参考视频。资产生产可以完整，但Video Job必须保持`MINIMUM_SUFFICIENT_REFERENCE_SET`，不能把“模型支持全能参考”解释成“资产越多越全塞”。
