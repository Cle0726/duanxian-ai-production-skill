# Wardrobe Style Design Engine（服装风格设计引擎）

> **用途：** 为《断弦之歌》所有日常状态人物建立“同一世界、不同衣柜”的服装审美系统。它解决的不是“天气冷就加大衣”，也不是让所有人穿成同一家品牌，而是：**在统一时代/世界质感下，让不同人物拥有不同的服装廓形、比例、材质、层次、职业/阶层痕迹与穿衣习惯。**
>
> **Authority位置：** Stage 02先读取`source_wardrobe_adaptation_authority.md`分类小说/剧本服装线索，并用`character_costume_dramaturgy.md`决定人物为什么这样穿；Stage 03再调用本引擎完成具体服装设计，并写入Character Master。Body Identity与当前LOOK的呈现方式分别服从`body_identity_presentation_authority.md`。Stage 04/05不得重新发明正式服装，只能继承已批准造型和短期穿着状态。

---

## 1｜Project Wardrobe Canon（项目日常服装总审美）

《断弦之歌》的日常服装统一采用：

**20世纪70—90年代欧洲都市/地区真实服装光谱 × 克制旧欧洲审美（克制只约束装饰数量，不约束身材呈现） × 真实可穿 × 角色个人Fashion DNA × 当前Global/Scene Color DNA。**

`French-inspired Urban Minimalism（法式都市简约）`保留为**可选子语言**，不再是所有角色的默认制服。其他人物可根据地域、职业、阶层、人格使用中欧实用剪裁、北方功能型、南欧柔软层叠、工匠/驾驶员/医护/知识分子/旧贵族残余/流浪艺术家等不同子语言，只要仍属于同一世界。

它不是当代网红“法式穿搭”，不是巴黎时装周，也不是历史戏服。核心是：
- 简洁但有比例设计；
- 都市、成熟、克制、文学感；其中“克制”只约束装饰与配饰数量，不压低人物身体魅力。版型呈现方式保持中立：贴身、合体、宽松、Oversized、框景、比例、暗示或对比都可，只要既定Body Identity与Appeal在整套Look中成立；
- 通过版型、材质、层次和身体线条体现品味，不靠堆装饰；但克制不等于全员无装饰，主要/反复角色应读取`personal_adornment_identity_system.md`判断是否需要个人Signature Adornment；
- 看起来像角色真的拥有并反复穿这些衣服；
- 日常可穿、能行动、符合天气与职业；
- 旧建筑/古堡/歌剧院不自动把人物变成贵族、维多利亚或舞台Cosplay。

### 1.1 Shared World Language（共享世界语言）
- 轮廓：根据角色可采用修长纵向、短上衣长腿、柔和A线、直身功能型、结构肩、落肩、宽裤/窄裤、裙装/连衣裙等不同族；禁止把“高级感”固定成同一种收腰长线；但无论哪个轮廓族，既定Body Identity与整体身体美必须成立；**宽松、直身、茧型、Oversized、阔腿、流动轮廓均为合法设计**。身体魅力可通过DIRECT / FRAMED / PROPORTIONAL / IMPLIED / CONTRAST等方式表达，不再把“显身材”机械等同于每层收腰/贴身/高腰；
- 单品示例（**开放清单，包括但不限于下列条目；清单是起点不是菜单，清单外的创新组合优先级高于清单内照抄**）：
  - 上装：衬衫（打结/露肩/下摆敞开穿法）、短款上衣/露脐衫、紧身针织/高领修身衫、束身衣式上衣（bustier top）、一字肩/露肩上衣、背心/吊带背心、开衫、马甲；
  - 下装：包臀裙（铅笔裙）、A字短裙、百褶短裙、高开衩长裙、鱼尾裙、高腰短裤、皮质短裤、紧身牛仔裤、喇叭裤、高腰直筒裤、紧身皮裤、直筒/宽腿/锥形裤；
  - 连体系：紧身连衣短裙（bodycon）、连体衣（bodysuit）、背心裙、连体裤（jumpsuit）；
  - 外套：收腰短夹克、机车皮夹克、束腰风衣、X型毛呢大衣、羊毛/呢料外套、旧皮夹克、工装外套；
  - 鞋靴：细高跟、尖头高跟、高跟短靴、高跟玛丽珍、过膝长靴、短靴、长靴、皮鞋、实用鞋；**高跟鞋是日常默认可选项，不再只限正式场合**，只要满足剧情里的行走/跑动基本要求；高跟鞋/高跟短靴+连裤袜或丝袜是日常显腿线的高效组合；
  - 袜类：**连裤袜/丝袜（Hosiery）**——透明/半透明/不透厚款按季节分级；颜色包括但不限于黑、白、米白、深灰、酒红、深棕，按角色气质与Personal Palette分配；白色系适合学院/清冷/少女气质，黑色系适合成熟妩媚路线；**禁止全员黑丝、也禁止全员白丝**，颜色与厚度按角色区分；
  - 其他：围巾、手套、工作制服单品等；
- 材质：羊毛、呢料、棉、亚麻感织物、细针织、旧皮革、丝质/柔软衬里、弹力针织、漆面/金属细部；
- 表面：哑光、轻旧化、有生活痕迹，拒绝廉价亮面塑料感；
- 综合色：先从Character Fashion DNA、季节、地区与Global Color DNA推导；深海军蓝、炭灰、烟草棕、灰玫瑰、灰紫褐、烟橄榄、骨白、暗酒红、旧金等只是项目历史常见色族示例，**不是固定综合色清单或饱和度上限**。

### 1.2 禁止错误理解
- 不得把“法式”理解成贝雷帽+条纹衫的刻板符号套装；
- 不得把“简约”理解成全员黑色高领+长大衣；
- 不得把“复古”理解成历史戏服；
- 不得把“高级”理解成所有人穿同一个奢侈品牌画册；
- 不得把“冬装”理解成在原造型外机械加一件大衣；
- 不得把“性感/身材美”理解成全员套同一暴露模板；主动暴露几何与贴身剪裁是正式设计手段，但每个角色的暴露结构、身体线条重点仍需与人格一致并互相区分。

---


### 1.3 Fashion Spectrum Permission（服装子语言开放范围）

同一时代/世界不等于同一品牌。角色个人Fashion DNA允许更大胆地落在不同子语言上，包含但不限于：Sharp Tailoring、Soft Romantic、Art-school / Bohemian、Nightlife Glam、Leather / Biker、Utilitarian、Minimal Severe、Retro Sport、Aristocratic Eccentric、Avant-garde Accent、Subculture-influenced等；必须按角色地域、职业、阶层、人格和剧情条件筛选。

- `Dark / Gothic`只能是个别角色可能拥有的子语言之一，**不是项目默认高级答案**；
- 成年角色可以使用更明确的贴身、短长比例反差、强肩线、高腰、透视内层、皮革/丝质/金属等Fashion Statement；
- 现实可穿不等于“保守”，而是结构和场合有解释；
- 主要群像若全部落入“深色长外套 + 高领 + 旧皮鞋”的安全区，即使单看都好看也属于Diversity不足。

## 2｜Character Fashion DNA（角色个人服装DNA）

每个主要/反复出现人物在第一次正式日常造型设计时，必须建立长期`Character Fashion DNA`。Fashion DNA描述**这个人如何穿衣**，而不是锁死某一套衣服。

### 必填字段
1. `Fashion Personality`｜穿衣人格
   - 例：克制知识分子 / 温柔都市古典 / 利落实干 / 精确秩序 / 流浪艺术家等。
2. `Silhouette Family`｜惯用轮廓族
   - 修长纵向 / 短外套+长腿 / 柔和长线 / 窄腰长摆 / 直线功能型等。
3. `Fit Preference`｜合体程度
   - 修身 / 合体 / 直身 / 局部宽松；禁止只写“好看”。
4. `Layering Logic`｜层次逻辑
   - 常用层数、内外长短关系、是否偏极简、是否喜欢开放领口/叠穿。
5. `Collar / Neckline Language`｜领口语言
6. `Material Preference`｜材质偏好
7. `Personal Palette`｜个人综合色习惯
8. `Signature Items / Details`｜惯用单品与细节
9. `Personal Adornment Strategy`｜SIGNATURE / ROTATING / FUNCTIONAL / MINIMAL / INTENTIONAL_NONE；读取`personal_adornment_identity_system.md`
10. `Footwear Language`｜鞋靴语言
11. `Styling Habits`｜穿衣习惯
    - 扣紧/敞开、卷袖、围巾打法、手套、首饰克制程度等。
12. `Primary Appeal Hook`｜主要魅力焦点
13. `Secondary Appeal Hook`｜次级魅力焦点
14. `Body-Line Emphasis`｜身体魅力重点（继承Body Identity，不规定每套服装的呈现手法）
15. `Silhouette Hook`｜剪影焦点
16. `Motion Appeal`｜动态魅力点
17. `Forbidden Generic Pattern`｜该角色绝不能滑向的通用模板
18. `Boldness Dial`｜RESTRAINED / ASSERTIVE / BOLD / EDITORIAL；继承角色Appeal Authority，不能被天气/高级感无理由降级；开放程度必须由性格/身份/职业/剧情位置推导，不按Scene机械凑档位；若AI无人物依据把群像统一推成同一种大胆公式，判`BOLDNESS DISTRIBUTION COLLAPSE`
19. `Category Family Signature`｜品类族签名：记录角色长期偏好的**Dominant Family + Justified Alternatives**。重复品类不等于重复造型；裙装型/裤装型角色可以长期保持偏好，只有剧情、场合、人物主动审美变化或反模板需要且不伤害Identity时才切换品类。

`12–19`必须继承 `character_appeal_silhouette_system.md`，不得由本服装引擎重新发明另一套魅力Authority。

---

## 2.1｜Wardrobe Diversity Matrix（服装多样性矩阵）

每个主要/反复角色建立Fashion DNA时必须同时读取`wardrobe_diversity_design_matrix.md`，至少锁定：
- Wardrobe Archetype
- Silhouette Family
- Proportion Rhythm
- Shoulder Language
- Collar / Neckline Language
- Waist Treatment
- Layer Density
- Bottom / Hem Language
- Material Mix
- Footwear Language
- Hosiery Language｜连裤袜/丝袜颜色与厚度习惯（黑色系/白色系/深色系，透明/半透明/不透）
- Category Family｜主品类族（裙装族/裤装族/连体系/混搭族等）
- Styling Habit
- Forbidden Template

**综合色不是主要区分手段。** 如果两套衣服只换颜色仍像同一品牌同一Look，视为设计未完成。

## 3｜Seasonal / Scenario Full-Outfit Translation（季节/场景完整穿搭转译）

每次剧情进入明显的新季节、地区、正式度或长期生活阶段时，先读取：

`Source Wardrobe Classification → Character Costume Dramaturgy → Project Wardrobe Canon → Character Fashion DNA → Character Closet → Body Identity/Presentation Authority → Environment/Season/Occasion → Appeal Hooks`

再输出完整造型，而不是“旧造型+一件功能单品”。

### 3.1 完整造型至少重新判断
- 内层Top / Shirt / Knit；
- 中间层（如需要）；
- 外层；
- 下装（裤/裙/连衣裙）；
- 鞋靴；
- 围巾/帽/手套；
- 固定饰品与剧情道具关系；
- 材质厚度；
- 上下装比例；
- 综合色比例；
- Primary / Secondary Appeal如何在当前天气下继续成立；
- 动作便利性；
- 当前Scene的穿脱配置。

### 3.2 No Lazy Styling（禁止懒惰式搭配）
不再把“已有Look + 大衣/围巾/手套”本身判错。Closet复用与现实成衣叠搭是合法且优先的；真正检查的是**加入/移除单品以后有没有形成新的整体Styling Logic**。

以下判 `WARDROBE STYLING LAZY`：
- 只机械增加保暖/防雨单品，比例、开合、内外层可见关系、综合色/材质与Body Presentation完全没有重新判断；
- 同一套衣服只换综合色冒充新季节/新场合Look；
- 环境变化明显却仍使用不合理厚度或穿脱状态；
- 只满足功能，不回答人物的Dressing Motivation、Fashion DNA与当前Self-Presentation；
- 复用单品后整体仍像旧Look的无思考复制，而不是合理的Closet recombination。

**合法复用示例：** 黑高领 + 长裤在新Scene加入长大衣，只要大衣长度/开合改变了整体比例，内层露出关系、材质对比、综合色层级与Body Presentation都经过明确判断，即可形成优秀新Look。

禁止的是“没有新的搭配逻辑”，不是禁止“旧衣服 + 新外层”。

---

## 4｜Appeal Preservation Under Wardrobe（服装下的人物魅力保留）

服装功能性不能无理由覆盖人物既有魅力设计。

### 4.1 成年角色与Cold-Weather Body Beauty Strategy（冷天身体美策略）

冷天取消固定数量的“显身材措施”硬计数。读取`body_identity_presentation_authority.md`，只要求：
- 保暖/防雨/活动逻辑成立；
- 既定Body Identity不漂移；
- 至少一个主要Appeal Hook或身体比例关系仍然成立；
- 角色没有被服装吞成与其他人相同的无差别体块；
- Boldness / Fashion DNA没有因为“高级/寒冷”自动安全化。

可选呈现方式包含但不限于：
1. `DIRECT`：合体内层、开放领口、开衩、局部贴身；
2. `FRAMED`：宽/长外层敞开或结构性开口，把内层身体线条框出来；
3. `PROPORTIONAL`：高腰、短长、肩腿、上下体量关系；
4. `IMPLIED`：垂坠、省道、柔软材质与动态暗示；
5. `CONTRAST`：Oversized外层 × 窄内层 / 纤细腿，宽裤 × 合体上身等。

**合法示例：** Oversized Blazer + fitted inner；直身长大衣 + 高腰纵向内层；宽松针织 + 清楚腰位/裙长比例。不得为了过“显身材”QC，把本应Boxy/Oversized的版型强行掐腰。

失败只在整套Look把人物既定身体魅力与比例无理由完全吞没时成立，状态改为`BODY_BEAUTY_SUPPRESSED`；不再因“没有收腰/没有贴腿/没有露肤”单独失败。

### 4.2 未成年角色
- `Appeal`只表示角色魅力、可爱度、精神气质、轮廓辨识与服装个性；
- 禁止性感化Exposure Geometry、胸腰臀/腿部性化强调或成人化卖点；
- 重点使用脸、发型、色彩、鞋帽、外套轮廓、动作便利与生活感建立吸引力。

### 4.3 功能优先但不等于审美放弃
若极端天气、安全装备、职业制服或剧情必须覆盖既有身体线条：
- 先保证功能/安全；
- 再寻找新的合法魅力载体；
- 记录这是`TEMPORARY APPEAL SHIFT`，不是永久重写Character Fashion DNA。

---

## 5｜Character Distinction Gate（角色区分闸门）

同一Scene中主要角色的完整服装必须做横向比较：
- 轮廓是否过于相似；
- 长外套比例是否重复；
- 领口/层次是否重复；
- `Styling / Structure`是否撞型：同属裙装/裤装/西装/长外套本身不算冲突；只有比例、肩线、领口、腰位、层次、材质、身体呈现和穿法也高度相似时才需要调整。品类可重复，Character Fashion DNA不能重复；
- 连裤袜/丝袜是否全员同色（全员黑丝 / 全员白丝均属撞型）；
- 色彩是否全部挤在同一区间；
- 鞋靴、手部、围巾/配饰是否缺少个人习惯；
- Primary Appeal Hook是否撞型；
- 缩到手机屏幕时能否只看服装剪影大致分辨人物。

若“单看每个人都好看，但站在一起像同一品牌Lookbook”，判 `WARDROBE TEMPLATE COLLISION`，返回Stage 03重设计结构差异；不能只换颜色解决。

**创新组合优先：** 跨品类混搭（衬衫打结+高腰短裤+高跟、束身衣式上衣+鱼尾裙、连体裤+收腰短夹克等）与清单外的新组合比清单内照抄更符合本规则意图；品类清单是素材池而不是搭配菜单。

---

## 6｜Cost-Aware Design（个人创作者成本规则）

- 优先复用角色真实拥有的Closet Item，通过重新组合形成新Look；
- 不因为每个Scene不同就创建新衣服；
- 新增单品必须解决明确的季节/场合/剧情/剪影问题；
- 只有完整长期Look变化才建立新的Character Master；
- 短期COAT_OPEN / COAT_OFF / 袖口卷起 / 围巾松开 / WET / DUSTY等交给Runtime Costume State；
- 但COAT_OFF等若暴露此前未被Approved Visual Authority定义的大面积内层结构，触发`Wardrobe Visibility Escalation Gate`，回Stage 03补最小Outfit Configuration Reference，不允许Stage 04/05凭空设计；
- 不为了展示衣柜中的每个单品单独生成图片资产，默认使用文字Registry；只有关键造型真正进入正式剧情时才生成对应Character Master或必要Reference。

---

## 7｜QC Checklist

正式日常人物造型必须同时PASS：
- `PROJECT STYLE`：属于20世纪70—90年代欧洲现实服装世界，具体子语言符合该角色，而非全员法式同模板；
- `CHARACTER`：像这个角色会穿，而非通用漂亮衣服；
- `ENVIRONMENT`：季节/温度/天气/活动合理；
- `FULL OUTFIT`：是完整重新搭配，不是懒惰加层；
- `APPEAL`：既有Body-Line/Appeal Hook没有被无理由抹掉，且成年主要角色在手机封面尺度具备可传播的第一眼流量钩子，否则 `TRAFFIC APPEAL WEAK`；
- `BODY BEAUTY`：当前LOOK以角色适合的Body Presentation Mode保留既定Body Identity / Appeal；不得把“宽松”直接判Fail，也不得让服装无理由吞掉人物身材；失败读取`body_identity_presentation_authority.md`；
- `DISTINCTION`：与其他主要角色不撞型；
- `CLOSET LOGIC`：优先使用已拥有单品；新增单品有理由；
- `CONTINUITY`：穿脱、湿度、污渍、破损能被World State继承；
- `COST`：没有为一次性小变化无意义新增Master。
