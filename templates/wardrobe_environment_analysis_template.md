# 服装与环境适配分析模板


本模板用于 **Stage 03（第03阶段：图片资产）**，并且必须在人物母图生成之前使用。它负责判断角色在当前剧情阶段到底应该穿什么；正式设计必须同时读取 `source_wardrobe_adaptation_authority.md` + `character_costume_dramaturgy.md` + `wardrobe_style_design_engine.md` + `character_closet_registry.md` + `character_appeal_silhouette_system.md` + `body_identity_presentation_authority.md`。分析结果直接写进人物母图提示词，默认不再单独做一张Wardrobe Master（服装母图）给下游拼。

## A｜Scene / Character（场次 / 人物）
- Scene / Story Phase ID（场次 / 剧情阶段编号）：
- Character（人物）：
- 时间 / 地点：

## B｜环境条件
- 季节：
- 地区 / 气候：
- 天气：
- 温度感（没有依据时不要编精确数字）：
- 时间（白天 / 夜晚 / 清晨等）：
- 室内 / 室外 / 交通工具：
- 场合 / 社交正式度：
- 活动（步行 / 调查 / 驾驶 / 演出 / 追逐 / 战斗等）：
- 年代 / 世界观限制：

## C｜人物条件
- 角色身份 / 职业：
- Character Fashion DNA ID / Summary：
- Character Closet ID：
- 当前可复用Approved LOOK / Item：
- 性格与审美：
- 经济 / 生活质感线索：
- 行动便利性需求：
- 剧情必须保留的固定造型元素：
- Source Wardrobe Classification：WARDROBE_PLOT_FACT / SIGNATURE_CUE / DESCRIPTIVE_CUE / NONE
- Locked Story Wardrobe Fields（仅剧情必要字段）：
- Costume Dramaturgy Brief Ref：
- Dressing Motivation / Self-Presentation：

## C.5｜项目时代服装引导

默认人物日常服装以 **20世纪70—90年代欧洲都市/地区现实服装光谱** 为时代基底，并允许克制旧欧洲优雅感。法式都市简约只是可选子语言之一；具体角色还可偏中欧实用、北方功能、南欧柔软层叠、职业制服化、工匠旧物复用等。统一的是时代与世界，不是同一套廓形。**时代只管单品类型与材质质感，身材呈现与身体线条按现代短剧流量审美执行，不因复古而降级；“克制”只约束装饰数量，不约束身材呈现。**

- 旧城、旧剧院、古堡、石墙只代表环境历史，不自动等于历史戏服；
- 优先近现代欧洲实用衣装：羊毛外套、衬衫/高领、实用皮夹克、直筒裤、长裙/连衣裙、针织围巾、皮鞋/短靴；
- 重点避免“戏服化、贵族化、cosplay化”的period costume，而不是机械禁止一切旧欧洲细节；
- 舞台戏服、历史复原、特殊仪式或变身礼服由剧情另行决定。

## D｜当前剧情阶段完整造型判定
- 人物母图ID：
- 造型阶段名称：
- 内层：
- 外层：
- 裤 / 裙 / 连体系（bodycon / bodysuit / jumpsuit等）：
- 连裤袜 / 丝袜（颜色与厚度，按Hosiery Language分配）：
- 鞋靴：
- 围巾 / 帽子 / 手套：
- 固定饰品 / 剧情关键饰品：
- 材质与厚度：
- 为什么符合环境 / 场合 / 活动：
- 如何保持该角色自身审美与身份：
- Closet-First结果：复用现有LOOK / 重组现有Item / 新增Item（说明原因）：
- Primary Appeal Hook如何保留/呈现（不要求每次“放大”）：
- Secondary Appeal Hook如何保留/呈现：
- Body Presentation Mode：DIRECT / FRAMED / PROPORTIONAL / IMPLIED / CONTRAST / MIXED
- Preserved Appeal Hook：
- Body Beauty Evidence（2–4个真正可见证据）：
- 是否触发No Lazy Styling检查（复用单品合法；只检查是否存在新的整体搭配逻辑）：

**输出原则：以上造型直接写入人物母图生成提示词，生成“人物身份 + 当前阶段完整服装”的正式人物母图。不要默认拆成身份图 + 独立服装图供下游融合。**

## E｜是否需要新的角色人物母图？
仅在明显完整造型阶段变化时新建，例如：
- 跨天主动换装；
- 换季 / 大幅地区气候变化；
- 正式演出 / 社交场合；
- 伪装 / 剧情明确换衣；
- 其他长期阶段变化。

若只是进入车内、外套解开/脱下、轻微淋湿、灰尘、少量血迹等，通常继续沿用同一人物母图，并在 `Wardrobe State Ledger` 中记录，不重新设计整套衣服。

## F｜短期状态连续性
- 室外 → 车内：
- 车内 → 室内：
- COAT_ON（外套穿好） / COAT_OPEN（外套敞开） / COAT_OFF（外套脱下）如何连续：
- WET（湿） / DUSTY（灰尘） / LIGHT_BLOOD（少量血迹）等如何由上一段尾帧继承：
- 哪些只需Stage 04/05（分镜/视频）文字控制：
- 是否存在长期持续且难稳定的状态，需要正式State Variant（持久状态变体）：

## G｜Stage 03（图片资产阶段）正式输出
- 当前剧情阶段人物母图：
- 必要的长期State Variant母图（没有则写“无”）：
- Stage 04/05应直接引用的人物母图ID：

## H｜审核问题
- 服装是否符合季节/天气/温度感/场合/活动？
- 是否保持近现代欧洲都市复古的实用性，同时保留角色自己的旧欧洲优雅感，而没有戏服化？
- 是否仍然像这个角色会穿的东西，并符合其Character Fashion DNA？
- 是否优先从Character Closet重组，而不是每个Scene凭空发明新衣服？
- 是否形成完整Look，而非“旧衣服+一件大衣/围巾”的懒惰式换装？
- 与同Scene其他主要角色相比，是否存在真正的Styling/Structure撞型？同品类本身不算撞型；Hosiery/Pattern/配饰也不应机械全员同款。
- 成年角色既定Body Identity / Appeal是否仍成立？当前Body Presentation Mode是否自然？宽松/Oversized是否被合法使用，而非被强行掐腰或无理由吞掉身材？
- 成年主要角色在手机封面尺度是否具备可传播的第一眼流量钩子（脸/身材/发型/剪影/暴露几何）？
- 是否已经整合进人物母图，而不是无必要拆出服装母图？
- 是否只有在真正完整换装时才生成新人物母图？
- 是否把短期变化优先交给连续性状态 + 分镜 + 视频Prompt？CONTINUITY_ENTRY可用上一段尾帧，CUT_ENTRY / SCENE_OPENING用剧情状态/Storyboard继承。
- 若建立长期State Variant，它是否确实有必要并继承当前人物母图？
