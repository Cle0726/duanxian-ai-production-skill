# 《断弦之歌》Project Style DNA（项目统一画风DNA）

> **用途：** 这是《断弦之歌》所有正式图片资产、分镜图、视频Prompt共同调用的最高优先级统一画风规则。它回答的不是“谁是谁”，而是“整个项目到底怎么画”。

## 1. 总定义（Master Definition）

《断弦之歌》的统一正式画风不是泛化的“暗黑插画”，也不是把所有Scene锁成同一种“夜雨蓝灰”，而是：

**欧陆复古、忧郁克制、电影化、带明显动漫影响的人物导向二维叙事插画体系。**

更准确地说，是：

**anime-influenced 2D illustrated character art + clean hand-drawn linework + cel-inspired controlled color blocking with soft painterly shading + idealized semi-realistic European facial structure + rich-but-restrained color language + controlled chroma concentration + selective saturation + controlled contrast + preserved value hierarchy + European retro cinematic atmosphere**

重点不是“越黑越恐怖”，也不是“越灰越统一”，而是：
- 二维插画体系必须非常明确；
- 人物脸必须干净、理想化、审美化；
- 场景必须有电影氛围，但不是照片级写实；
- 综合色强调**色族集中、功能清楚与选择性显色**；不要求常规画面统一低饱和，Scene可根据材质、肤色、天气、实际光源与叙事重点自然提高或降低综合色强度，但明度结构与主体分离必须清楚；
- 雨夜旧城是第一季重要Baseline Motif（基准氛围母题），不是所有地点/天气/时间的永久色卡；
- 暖光、肤色生命色、剧情FX和局部强调允许受控突破，不做整画面橙染；
- 黑色必须有层次，白色优先骨白/奶油白，金色/酒红等强调色按叙事需要受控出现。

视觉权限进一步拆分读取：
- `visual_style_authority_engine.md`：Render Style Grammar与Cinematic Shot Grammar分权；
- `color_script_derivation_engine.md`：Global Color DNA → Scene Color Extension → Shot Lighting Variant。

## 2. Style DNA（核心不可漂移特征）

### 2.1 画种与渲染本质
- 主体画种必须是 **anime-influenced 2D illustrated character art（带动漫影响的二维角色插画）**；
- `semi-realistic` 只用于修饰骨相、五官结构和气质，不可反客为主把人物推向真人化或欧式绘本化；
- 不是照片，不是真人，不是live action；
- 不是欧美3A游戏角色，不是3D render，不是CGI；
- 不是无描线厚重油画；
- 允许 **cel-inspired controlled color blocking + soft painterly shading（受控色块 + 柔和绘画阴影）**；
- 禁止廉价、低细节、僵硬的纯平涂卡通赛璐璐，但不能误伤项目本身需要的二维插画结构；
- 是 **clean hand-drawn linework + soft painterly rendering（清楚手绘线稿 + 柔和绘画渲染）** 的统一体系。

### 2.2 线稿系统（Linework）
- 保留 **delicate controlled dark linework（细、稳、克制的深色结构线）**；
- 线稿颜色以深棕黑/深灰黑为主，不用死黑漫画线；
- 五官、发束、服装裁片、主要褶皱、关键结构应有清楚线稿辅助；
- 脸部外轮廓和皮肤过渡处线稿可更轻；
- 背景可比人物弱线一些，但仍属于同一二维绘画体系。
- 人物必须先由线稿与色块建立，再由柔和阴影补体积，不能直接滑向无描线写实绘本感。

### 2.3 人物与环境统一原则
- 人物与环境必须属于 **同一绘画系统**；
- 不能出现“人物是乙女插画、背景是写实概念图”的断裂；
- 背景可以比人物略软、略低对比，但不能像另一种作品；
- 任何正式图都要保持“角色能直接进入该场景”的完成度。

## 3. Character Rendering Rules（人物绘制规则）

### 3.1 脸部设计
- 人物采用 **理想化但克制的欧洲骨相**；
- 眼睛比真人略大、读形清楚，但自然、克制；不得画成极端夸张动漫大眼，也不得缩回接近真人比例导致整张脸写实化。
- 鼻梁、鼻尖、唇线、下颌必须清楚，但整体柔和、审美化；
- 不能出现粗硬欧美男模骨相、深陷小眼、极重眉骨、过强法令纹；
- 也不能漂成幼态甜妹脸、扁平二次元脸、K-pop网红脸。

### 3.2 皮肤渲染
- 必须是 **matte painted skin（哑光绘画皮肤）**；
- 平滑、干净、无毛孔、无高频肤质噪点；
- 用柔和色块和低对比明暗表现体积；
- 禁止真实皮下散射、油亮高光、摄影皮肤、粉底感、写真磨皮感。

### 3.3 头发绘制
- 头发以 **大块发束组织整体体积，小量细丝丰富边缘**；
- 发丝方向必须自然、可读；
- 高光是柔和面状，不是3D塑料高光条；
- 可有轻微潮湿、凌乱、空气感，但不能油腻；
- 禁止照片级逐根毛发、3D发丝、塑料发片感。

### 3.4 人物气质
- **项目叙事氛围**可偏欧陆、忧郁、克制、文学感与神秘感，但这不是所有角色的默认人格/表情模板；不同角色必须保留自己的情绪基线、年龄感、脸部重心与姿态。
- 表情常常偏内收，不做夸张热血型漫画表演；
- “美”可以同时具有旧时代电影感、成熟魅力、商业传播力与大胆时装性；项目不追求全场景明艳商业广告感，但**人物设计与圣谱者变身不因“克制”被自动压成保守、暗色、低综合色或无身体线条**。

### 3.5 Era & Wardrobe Guidance（时代与服装引导）
- 日常服装以 **20世纪70—90年代欧洲都市/地区真实服装光谱** 为时代基底；法式都市简约只是可选子语言之一。不同人物可按地域、职业、阶层与人格形成不同廓形/比例/材质/穿法，但必须属于同一世界；

- **Dark Gothic / Gothic Romance只是一种可选角色子语言，不是《断弦之歌》圣谱者的默认风格。** Transformation可以在统一Project Render Style下使用Opera Couture、Avant-garde、Art Deco、Ballet-derived、Ceremonial、Mythic、Military Deconstruction、Glam、Minimal Monumental、Instrument-Architecture等更广谱方向；
- Transformation不受日常“现实可穿”的同等限制：它可以更高定、更极端、更图形化、更性感、更强材质反差，只要仍能解释为该角色Music Identity并满足战斗动作；
- 服装强调克制比例、干净剪影、成熟都市感、真实可穿与人物个人审美；推荐羊毛外套、风衣、皮夹克、高领/衬衫、针织、直筒裤、克制长裙/连衣裙、针织围巾、普通皮鞋/短靴；
- “换季”不是给原服装机械加一件大衣，而是在角色自己的Fashion DNA与Closet中重新组织完整Look；
- 主要人物必须有各自Character Fashion DNA，统一时代与风格但不能像同一品牌Lookbook；
- 核心原则不是“禁止一切历史感”，而是 **避免戏服化、舞台化、贵族化的历史服装造型**；
- 旧建筑、古堡、老剧院可以历史悠久，但日常人物仍然是近现代欧洲都市生活中的人。

### 3.6 Character Appeal & Silhouette（角色魅力与剪影）
- 《断弦之歌》的人物必须“好看且有吸引力”，吸引力应来自**骨相、发型、肩颈、腰线、腿线、手部、衣摆、武器姿态与清楚剪影**；成年角色的身材比例可按短剧流量审美理想化设计；
- 成年角色除非剧情/人格明确要求封闭克制，否则不应默认被设计成“全包保守化”；
- 女性角色不默认短裙露腿模板，男性角色不默认高领长外套全包模板；
- 每名角色都应有可言说的 `Appeal Hook（魅力焦点）` 与 `Silhouette Hook（剪影焦点）`；
- 角色魅力必须服从本项目的欧陆复古、歌剧化、成熟感与受控综合色组织；渲染风格层面不得漂向偶像化画风或廉价手游皮肤质感；不以“全面降饱和”作为角色魅力成立条件。

## 4. Environment Rendering Rules（场景绘制规则）

### 4.1 场景总方向
- 旧欧洲城市、旧剧院、旧交通工具、旧店铺、老室内、雪原、遗迹等都必须服从同一二维绘画体系；
- **夜雨旧城是重要基准场景，不是Environment Master Definition本身**；
- 新地点根据自身天气、季节、时间、材质与剧情功能派生Scene Color Extension，不把旧场景综合色机械复制过去；
- 场景服务叙事，不做脱离剧情的大场景炫技概念图。

### 4.2 空间与细节
- 透视和空间必须可信；
- 建筑、内饰、街道和家具细节充分，但不追求建筑考据式极端高频；
- 氛围优先于写实炫技；
- 材质保持旧化/生活痕迹与二维概括；是否潮湿、积雪、干燥、洁净由当前Environment State决定，不作为全项目固定属性。

### 4.3 氛围系统
- 全局气质保持：**quiet / literary / melancholic / restrained / mysterious**；
- 夜雨Scene可以使用冷灰/蓝灰空气 + 局部暖窗灯/路灯 + 烟草棕/旧金反射；
- 白昼、雪原、医院、遗迹、暖室内等必须从Global Color DNA派生自己的环境基底与光色；
- 所有Scene都应 **controlled contrast, dark when appropriate, but never value-muddy or colorless**；
- 不把“忧郁克制”错误翻译成所有地点都低曝光、低对比、同一蓝灰滤镜。

## 5. Color System（综合色彩系统）

综合色执行统一读取 `color_script_derivation_engine.md`，采用三级结构：

**Global Color DNA → Scene Color Extension → Shot Lighting Variant**

### 5.1 Global Balance Heuristic
70 / 20 / 10若保留，只作为**全局综合色平衡启发**，不是每个Shot的面积配额：
- 稳定中性/深色/环境基底通常占主要视觉面积；
- 角色与服装综合色提供人物识别；
- 旧金、蜂蜜暖光、暗酒红、暮星紫等局部强调受控出现。

人物特写、雪原宽景、暖室内或强剧情灯光可以自然偏离，不能机械计算面积。

### 5.2 Functional Color Map
综合色优先按功能记录：
- `STRUCTURE_DARKS`：炭墨黑、暖煤黑、深褐黑、湿铁黑、烟灰褐等结构深色；
- `ENVIRONMENT_BASE`：随Scene派生的空气/墙面/天空/雪/远景基底；
- `MATERIAL_FAMILY`：皮革、木材、金属、纸张、石材等综合色；
- `SKIN_FAMILY`：灰暖/柔米/奶杏等保持生命感的肤色家族；
- `CHARACTER_ACCENTS`：人物自己的识别色；可按角色与当前Scene保持克制、柔和或明确显色，不设统一低饱和上限；
- `LIGHT_ACCENTS`：旧金、蜂蜜暖光、奶油光、暗酒红等实际光源/剧情强调；
- `FX_EXCEPTION`：剧情明确时允许短暂突破综合色基线的VFX。

Hex值可以登记，但**职责和综合色关系高于死守某个Hex**。

### 5.3 Contrast / Chroma Organization
综合色核心不是“low saturation”或“low contrast”，而是：

**rich but restrained palette + controlled chroma concentration + selective saturation + controlled contrast + preserved value hierarchy**

- 黑色在出现时必须有结构与层次；
- 皮肤与深衣、人物与背景、灯光与暗部必须能读开；
-综合色可以在皮肤、角色识别色、皮革/织物/木材、实际光源、关键道具与FX上明确显色；
- 避免的是无功能综合色平均铺满、无来源全画面橙染/蓝染、赛博霓虹与糖果色杂乱，而不是“综合色本身不能浓”；
- Scene Color Extension拥有当前场景综合色强度的派生权，不得用全局低饱和词把白昼、自然景观、暖室内、舞台或FX统一压灰。

### 5.4 Scene Adaptation
新地点/新气候/新Arc先派生文字版Scene Color Extension；只有反复出现、综合色差异显著或多镜稳定性风险高时才在Stage 03生成正式扩展色卡图。临时灯灭、雷光、火焰、战斗FX等优先作为Shot Lighting Variant，不自动升级为永久场景色卡。

## 6. Material Rules（材质规则）

### 6.1 常见材质统一写法
- **皮革**：旧化、微磨损、低反光、偏哑光；
- **羊毛/针织**：柔和、蓬松但不过分纤维化；
- **金属**：旧金属、暗金属、黑铁感，允许轻微氧化或潮湿痕迹；
- **木材**：旧木、深木色、低反光；
- **石材**：旧化、冷暖受环境影响；潮湿/反光/积雪等由当前Scene Condition决定；
- **玻璃**：仍以二维概括呈现；雨痕、结露、雪水、洁净反射等由当前Scene / Environment State决定，不把“有雨痕”写成全项目固定属性；
- **皮肤**：始终哑光，不转成摄影皮肤。

### 6.2 旧化原则
- 日常世界中的衣物、建筑、家具、普通金属与生活道具优先带有 **aged / lived-in / slightly worn（有使用痕迹、年代感、轻旧化）**；
- **圣谱者Transformation生成材质不受“全部轻旧化”硬锁。** 当Music Identity支持时，可使用洁净高光金属、漆面、镜面、玻璃/珐琅、珠光、半透明层、发光纤维等更大胆材质，与哑光/旧化部分形成角色专属Material Contrast；
- 但不能把整个世界变成廉价塑料/赛博霓虹，也不能把“大胆材质”平均铺满所有角色；
- 日常旧感应克制、可信、带文学气质；Transformation则以Music Identity与Splendor Hierarchy决定新旧、哑亮与硬软关系。

## 7. Threat Layer Rules（异物 / 威胁层规则）

剧情明确为敌对 / 污染 / 失控的异常物件、异常碎片或异常变身残响属于 **Threat Layer（异物层 / 威胁层）**。普通圣谱者的共鸣谱线、武器生成光迹与变身粒子属于Transformation FX Layer，不默认视为Threat Layer。

### 7.1 异物层特征
- 可以更黑、更尖锐、更复杂；
- 允许裂纹、缠绕、乐谱残片、黑弦、碎面具、烧焦黑铁、破损黑曜质感；
- 允许更强的不安定结构与视觉噪声；
- 允许比人物/环境更高的异质感与威胁感。

### 7.2 重要边界
- Threat Layer只控制威胁体自己；
- 不能反向污染所有角色、日常道具和常规场景的主渲染方式；
- 不能因为有怪异物件，就把整部作品画成粗砺恐怖概念图。

## 8. Negative Style Lock（强反向风格锁）

### 禁止出现
- photorealistic
- live action
- real actor likeness
- 3D render / CGI / Unreal / PBR
- AAA game character face
- line-less realism
- heavy impasto oil painting
- cheap flat cel shading
- low-detail simplistic anime rendering
- exaggerated oversized manga eyes
- pore skin / realistic skin texture / subsurface scattering
- plastic hair / oily hair highlight bands
- cyberpunk neon
- orange-blue blockbuster grading
- post-apocalyptic mud / tactical gear / modern fashion glamour
- glossy fashion illustration
- hyper-saturated candy colors

### 中文通俗版
不是照片，不是真人演员，不是影视写实概念图，不是欧美3A游戏角色，不是3D渲染，不是无描线写实，不是廉价低细节纯平涂动漫，不是夸张大眼萌系，不是高饱和时尚插画，不是赛博霓虹，不是橙蓝电影滤镜，不是末日泥污脏乱风，不是塑料发丝，不是毛孔皮肤。

## 9. Visual Style Authority职责定义

正式视觉风格不再由一个“Style Anchor”包办全部职责，统一读取 `visual_style_authority_engine.md`：

### Render Style Anchor
- 控制：二维绘画语言、线稿气质、脸部概括、皮肤/头发/材质的**表现方法**与风格气质；
- 不控制：身份、空间几何、具体镜头构图、对象清晰度或最终细节密度。

### Cinematic Shot Style Anchor
- 控制：景别倾向、人物/环境面积关系、OTS/Profile/Wide等摄影语法、前中后景层次、负空间、光源在构图中的使用习惯；
- 不控制：当前Shot已经由Director/Storyboard锁定的具体机位、站位、动作与空间几何；也不作为Stage 05缺失Lens / Focus / DOF / Stabilization / Camera Motion的补全Authority。

### Evidence Rule
已有成熟Approved资产时，可以直接组成`APPROVED_STYLE_EVIDENCE_BOARD`，无需为了“匿名标准格式”重新生成一套画风板。Evidence Board可以包含真实角色/场景，但下游只迁移其授权的Style Grammar，不能迁移身份/地点Canon。

### Canvas Rule
Style Board / Shot Style Board / Color Card版式比例由内容决定，4:3、16:9、竖版信息卡都可；**Style Board自身比例绝不是下游资产画布Authority。**
