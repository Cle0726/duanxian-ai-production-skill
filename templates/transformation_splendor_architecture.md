# Transformation Splendor Architecture（圣谱者变身华丽度与图标化设计架构）

> **用途：** 解决“细节不少但仍平”“所有人都像暗色哥特礼服换颜色”“越想高级越不敢设计”的问题。目标不是堆装饰，而是让圣谱者从`Daily Human`跃迁为**角色专属Visual Icon**。
>
> **核心原则：** `Concept first → Hero Decisions → Graphic Structure → Splendor Support.`

---

## 1｜先做Costume Thesis，不先堆字段

每个首次/核心圣谱者先写：

`Transformation Costume Thesis｜一句话礼服核心命题`

要求：
- 一句话能说明最核心的时装概念；
- 最多两个主概念，不允许“哥特+巴洛克+歌剧+军装+玫瑰+谱线+链条……”无限叠加；
- 必须来自Character Theme + Music Identity + Body / Motion需求；
- 不能从“我要一套黑红金华丽礼服”开始。

如果遮掉脸和武器后，只能概括成“漂亮暗黑礼服 / 高级哥特女战士 / 帅气长外套”，判`TRANSFORMATION_COSTUME_GENERIC_FAIL`。

---

## 2｜Style Family是开放选择，不是默认哥特

`Dark Gothic / Gothic Romance`可以使用，但它只是**可选Style Family之一**，没有默认优先级。

允许的方向**包含但不限于**：
- Opera / Stage Couture；
- Modern / Avant-garde Couture；
- Romantic / Poetic；
- Art Deco / Graphic Luxury；
- Classical Myth Reinterpretation；
- Ballet / Dance-derived；
- Ceremonial / Sacred Geometry；
- Military Deconstruction；
- Aristocratic Eccentricity；
- Instrument-Architecture Fashion；
- Minimal Monumental；
- Glam / Nightlife / Editorial；
- Gothic / Dark Romantic；
- Organic / Floral / Wing-like；
- Mechanical / Constructivist；
- 其他由Music Identity推导出的角色专属语言。

**世界统一靠Project Render Style / Music Logic / Canon材质表现，不靠所有人穿同一种暗黑哥特。**

如果多个圣谱者无角色理由自动收敛为`黑/酒红/旧金 + 束腰 + 长裙尾 + 哥特纹样`，判`STYLE_FAMILY_DEFAULT_COLLAPSE`。

---

## 3｜Hero Costume Decisions｜只锁2–3个超强决定

### Primary Costume Signature｜必须1个
全身第一眼最重要的结构，例如：
- 极端分裂长尾；
- 巨大不对称肩/袖；
- 强烈前短后长比例；
- 巨大头部/后背轮廓；
- 明确裤装/长靴/身体切口形成的图标；
- 武器与身体共同形成的特殊负形。

### Secondary Costume Signature｜必须1个
第二记忆点，最好来自不同尺度或不同身体区域。

### Tertiary Accent｜0–1
可以是头饰、腰部结构、胸前Glyph、鞋靴、特殊饰件等。**超过3个同等级Hero Decisions，先做减法。**

所有刺绣、谱纹、滚边、珠宝、小金属等默认属于Supporting Detail，不得和Hero Signature抢权重。

---

## 4｜Graphic Block Design｜先看大色块，不先看花纹

正式礼服必须明确：
- 主综合色块；
- 次综合色块；
- 肤色 / 透明区域形成的负空间；
- 高光/金属/发光Accent的面积等级；
- 各大块如何顺着身体和轮廓构成图形。

`rich but restrained`的含义是**色族数量受控、功能清楚**，不是所有综合色都压暗。

允许角色使用高纯红、洋红、青、蓝、白、金属色或其他强综合色，只要：
- 集中在少数大块；
- 明度层级清楚；
- 属于角色Music Identity；
- 不变成杂综合色平均铺满。

### Flat Color Test｜Icon｜Graphic Block
移除纹理、刺绣、珠宝、Glow，只保留大综合色与皮肤负空间。

如果设计立刻失去识别度，判`COSTUME_GRAPHIC_STRUCTURE_FAIL`。

---

## 5｜Negative Space Architecture｜“哪里没有布”也是正式结构

对于成年角色，负空间不只属于“性感选项”，而是Silhouette Geometry的一部分。

允许更大胆地使用：
- 深V / 胸前大开口；
- 单肩 / 双肩大面积开放；
- 露背 / 脊柱线；
- 侧腰切口；
- 腹部/胸腹结构性开洞；
- 高开衩（含**高开衩到腰**）；
- 前短后长；
- 透视层与实体布料交错（含**大面积透视/透明层**）；
- 比基尼式上衣（bikini top）结构；
- 低腰/露髋结构；
- 裤装/裙装之间的大负形；
- 手臂与躯干、裙尾与腿部之间的空间洞口。

`Exposure Geometry`可以是Primary / Secondary Costume Signature，而不是只能当小魅力点。

**大胆不等于全员暴露。** 某些角色最强图标可能恰好是封闭、巨大、庄严的体量；关键是它必须是角色主动的设计选择，而不是系统默认保守化。

---

## 6｜Adult Sensuality & Body-Line Boldness｜成年性感与身体线条权限

成年角色的`Boldness Dial`允许：
`RESTRAINED / ASSERTIVE / BOLD / EDITORIAL`

由人格、Music Identity、身体类型和角色定位决定，不以“高级感”为理由自动降到RESTRAINED。

### 可大胆设计
- 女性：胸腰臀曲线、肩颈锁骨、背部、腰腹、长腿、臀腿比例、束身结构、贴身裁切；
- 男性：肩胸背、窄腰、腹部、前臂、颈侧、长腿、开襟与贴身结构；
- 理想化比例可以更强，只要仍属于当前二维角色画风并保留角色之间身材差异；
- 性感可以来自大面积身体线条与开放区域，也可以来自极端贴身、结构张力、动作与材质，而不只靠裸露。

### Body Beauty Synchronization｜身体魅力同步
Transformation Costume仍由本Splendor Profile定义，不把Daily LOOK照搬过来；但必须读取`body_identity_presentation_authority.md`，继承稳定Body Identity与角色Appeal Hook，并为礼服单独选择`Transformation Body Presentation Mode`。

礼服可以比日常更华丽、更大体量、更开放或更戏剧化；身体美可以通过DIRECT / FRAMED / PROPORTIONAL / IMPLIED / CONTRAST / MIXED同步升级。重点是让**礼服的图标性与人物身体魅力共同成立**，而不是二选一。

大型裙摆、披片、肩背结构可以遮住部分身体，但必须有明确比例/框景/负空间/动态关系，让观众仍能感到这是这个角色原本的肩颈、腰胯、腿身比、胸背或其他核心Appeal。

**不要求Daily与Transformation使用相同Presentation Mode。** 例如日常可`CONTRAST`，变身可`DIRECT + PROPORTIONAL`；或者日常`DIRECT`，变身反而用`FRAMED + IMPLIED`。

### 不允许的“假大胆”
- 所有女性同一深V+高开衩；
- 所有男性同一开襟胸肌；
- 用裸露面积代替Costume Thesis；
- 身体变成通用商业模板，人物体型差异被抹掉。

如果Character Brief明确要求ASSERTIVE/BOLD/EDITORIAL，但最终被自动修回高领、长袖、暗色全包、身体线条不可读，判`TRANSFORMATION_BOLDNESS_SUPPRESSED_FAIL`。

**Boldness反模板（与日常装共用）：** 每名圣谱者的`Boldness Dial`服从自己的Music Identity、人格、身体与已批准视觉Authority，不按群像机械凑RESTRAINED/ASSERTIVE配额。若系统无角色依据地把不同圣谱者全部推成同一种BOLD/EDITORIAL暴露公式，才判`BOLDNESS DISTRIBUTION COLLAPSE`；克制设计可以成为强Icon，但不能为了“平衡档位”擅自改角色。

未成年角色不使用成人性感权限。

---

## 7｜Splendor Architecture｜Hero Decisions之后再建立华丽层级

### A. Large Scale｜大轮廓
Hero Costume Decision必须至少有一个进入Large Scale：
- 极端长度 / 宽度 / 不对称；
- 大型裙尾 / 披片 / 袖 / 肩 / 帽 / 发型 / 后背结构；
- 武器与身体共同形成Hero Silhouette；
- 大型正负空间。

允许比现实服装更大胆、更“奇怪但漂亮”。**先判断是否有图标性，再判断怎样让它可战斗。不要在概念阶段先把所有异常比例修平。**

### B. Medium Scale｜服装建筑
- 肩—胸—腰—胯—腿的结构关系；
- 裙 / 裤 / 袖 / 领 / 束身 / 装甲或软结构；
- Exposure / Negative Space；
- Music Identity怎样改变裁片节奏、重复、断裂、对称和重心；
- Adornment与主体的主次。

### C. Small Scale｜精密层
- 眼部Graphic；
- 刺绣 / 蚀刻 / 谱纹 / 金属连接；
- 珠宝 / 饰件 / 细小发光；
- 近景材质信息。

Small Scale必须服务Hero Signatures，不能用数量补救大结构普通。

---

## 8｜Material Contrast｜材质允许更大胆

Transformation Material不需要永远停留在“暗色哑光布 + 少量旧金”。在统一二维渲染语言下，允许明显拉开：
- matte ↔ mirror / lacquer / polished metal；
- velvet ↔ glass / crystal / enamel；
- opaque ↔ translucent / sheer / membrane-like；
- soft drape ↔ rigid frame / corsetry / articulated structure；
- heavy ↔ floating / feather-light；
- aged material ↔ supernatural pristine / luminous material（当Music Identity支持）。

可以出现更强珠光、漆面、镜面、透明层、宝石/玻璃感、发光纤维、硬质金属结构；**关键是面积层级与角色专属，不是统一“旧金属化”。**

如果所有材质都被“成熟克制”压成同一暗哑表面，判`SPLENDOR_MATERIAL_FLAT`。

---

## 9｜Music Identity必须改变结构，不只加纹样

Music Identity至少要进入以下三个层级中的两个：
- `Large Form`：轮廓、比例、体量、重心；
- `Medium Geometry`：裁片、开口、重复、断裂、对称、负空间；
- `Material / Motion`：材质、重量、飘动、硬软、发光方式。

允许音乐转译更大胆、更非现实：节奏可变成极端切片比例；长音可变成长拖尾；断奏可变成悬空分离结构；共鸣可变成环状体量；复调可变成层叠但有主次的双结构。

**标准音符只是可选表达，不是Music Identity唯一可视化方法。**

---

## 10｜Transformation Splendor Profile

首次/核心角色至少记录：
- Costume Thesis；
- Style Family（开放选择）；
- Boldness Dial；
- Primary Costume Signature；
- Secondary Costume Signature；
- Tertiary Accent（0–1）；
- Graphic Block Plan；
- Negative Space Architecture；
- Body-Line Emphasis；
- Transformation Body Presentation Mode；
- Preserved Appeal Hook(s)；
- Body-Costume Interaction / Body Beauty Evidence；
- Large Silhouette Hook；
- Medium Architecture；
- Primary Material Contrast；
- Secondary Material Contrast；
- Focal Chroma / Light；
- Hair Splendor Upgrade；
- Weapon-Body Silhouette；
- Music Identity Structural Translation；
- Daily → Transformation Visual Level Gap。

---

## 11｜Icon Tests

### Thumbnail Test
缩到手机缩略图：仍能看到Primary Costume Signature。

### Costume Icon Test
遮掉脸、发型细节和武器，只看身体+服装：主要/核心圣谱者仍能大致识别。

### Flat Color Test
移除小纹样与材质：大色块+负空间仍成立。

### Negative Space Test
转成黑色剪影与皮肤/透明区域的空洞关系：仍有角色专属节奏。

失败不靠“再加金边/珠宝/音符”修，返回Hero Decisions / Graphic Structure。

---

## 12｜与Stage 02 / 03衔接

Stage 02在首次设计尚未完成时只输出`Transformation Presentation Requirement Draft`：说明需要多大的Visual Level Gap、Silhouette可读距离、Eye Signature景别、Material Read、Weapon-Body Icon，不提前发明具体Costume Thesis。

Stage 03实际设计Approved后，把真实Splendor Profile回交`director_spatial_reconciliation_gate.md`，执行`TRANSFORMATION PRESENTATION RECONCILED`。

导演必须至少给Primary Costume Signature一个真正可读的镜头；否则设计再好也会被拍平。

---

## 13｜Hard Gates

- `TRANSFORMATION_COSTUME_GENERIC_FAIL`｜礼服只能用泛化风格词描述，没有角色独有Thesis；
- `STYLE_FAMILY_DEFAULT_COLLAPSE`｜多个角色无理由自动收敛到同一暗黑哥特/同类时装模板；
- `TRANSFORMATION_SPLENDOR_FLAT_FAIL`｜Daily→Transform视觉等级差不足；
- `SPLENDOR_LARGE_SCALE_MISSING`｜无远景Hero Signature；
- `COSTUME_GRAPHIC_STRUCTURE_FAIL`｜Flat Color后设计崩塌；
- `SPLENDOR_MATERIAL_FLAT`｜材质被统一压平；
- `SPLENDOR_DETAIL_NO_HIERARCHY`｜小细节与大结构抢权重；
- `TRANSFORMATION_BOLDNESS_SUPPRESSED_FAIL`｜批准的大胆方向被系统自动保守化；
- `TRANSFORMATION_BODY_IDENTITY_DRIFT`｜华丽礼服改变了人物本身的身体身份；
- `TRANSFORMATION_BODY_BEAUTY_SUPPRESSED`｜礼服图标成立但无理由完全吞掉人物既定身体魅力；
- `TRANSFORMATION_BODY_PRESENTATION_TEMPLATE_COLLAPSE`｜多个圣谱者被机械套成同一种身体呈现公式。

> **最终目标：** 不是“每个人都更华丽”，而是**每个人都有自己敢做、敢删、敢放大的2–3个视觉决定**。Dark Gothic可以属于某个人，但不能属于所有人。
