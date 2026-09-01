# Adaptive Color Script Derivation Engine（自适应综合色脚本派生引擎）

> **用途：** 让《断弦之歌》保持同一综合色DNA，同时允许雪原、白天旧城、医院、遗迹、暖室内、花园等新环境拥有自己的综合色扩展，而不是把某一张“夜雨蓝灰 + 琥珀灯”参考硬贴到所有Scene。
>
> **核心结构：** `Global Color DNA → Scene Color Extension → Shot Lighting Variant`。
>
> **核心原则：Color DNA defines relationships, not a saturation ceiling（综合色DNA定义关系，不定义全局饱和度上限）。**

## 1｜Global Color DNA｜全局综合色DNA

Global Color DNA是项目长期**色彩组织语法**，不是固定调色板、固定滤镜或固定综合色强度。

它负责：
- 深色/中性色在需要时怎样建立结构而不死黑、不脏灰；
- 颜色怎样集中在少数互相关联的色族中，而不是满画面随机彩色；
- 明度结构与主体分离怎样保持清楚；
- 肤色怎样保留生命感，不被环境统一压灰或橙染；
- 皮革、旧木、纸张、金属、织物等材质如何拥有自己的综合色重量；
- 实际灯源、人物识别色、叙事强调色怎样在需要时明确显色；
- 人物综合色与环境综合色如何协调，而不是互相吞没；
- 哪些赛博霓虹、无功能糖果色、综合色平均铺满、全局橙蓝大片滤镜等不属于项目主体系。

### 1.1 Color Flexibility Clause｜综合色弹性条款
Global Color DNA**不得**被解释成：
- Scene综合色根据剧情、材质、光源与场景功能推导，不使用全局统一饱和度模板；
- 所有Scene都偏灰；
- 所有Scene都必须深色；
- 所有暖色都只能占极小面积；
- 所有综合色都必须低于某个纯度；
- 夜雨、蓝灰、琥珀灯是永久组合；
- 某组Hex是每个镜头必须复现的配额。

Scene / Shot可以因为白昼、雪、皮革、肤色、花园、舞台灯、火焰、魔法FX、节庆、室内材质或剧情焦点而出现更清亮、更暖、更纯或更高综合色密度的区域，只要综合色仍有**功能、层级、来源和叙事理由**。

### Functional Color Map｜功能性色彩地图
推荐按职责记录，而不是只记录Hex：
1. `STRUCTURE_DARKS`｜世界结构深色；
2. `ENVIRONMENT_BASE`｜环境空气/墙面/远景承接色；
3. `MATERIAL_FAMILY`｜皮革/木材/金属/纸张/织物等材质综合色；
4. `SKIN_FAMILY`｜人物肤色家族；
5. `CHARACTER_ACCENTS`｜人物识别辅助色；
6. `LIGHT_ACCENTS`｜实际光源与剧情强调色；
7. `FX_EXCEPTION`｜剧情FX允许受控突破的综合色范围。

Hex可作为采样/登记证据，但**语义职责与综合色关系优先于死守Hex**。

## 2｜综合色原则：Controlled Chroma Concentration & Selective Saturation

项目主综合色应描述为：

**rich but restrained palette + controlled chroma concentration + selective saturation + controlled contrast + preserved value hierarchy**

中文：**综合色丰富但克制；颜色集中在少数受控色族中，允许选择性显色，并保持清楚的明度层级与主体分离。**

这里的“克制”指的是**综合色组织有秩序**，不是把每个颜色都压低饱和度。

### 2.1 允许明确显色的典型来源
以下来源可以根据当前Scene自然达到中等甚至较高的局部综合色存在感：
- 活着的肤色与唇色；
- 角色自身识别色；
- 皮革、木材、旧布料等本来就有综合色重量的材质；
- 路灯、台灯、剧院灯、窗光等真实光源；
- 叙事焦点道具；
- 剧情明确的VFX / Threat / Transformation FX；
- 当前场景自身的季节、植物、雪、室内装潢或其他大面积环境综合色。

### 2.2 禁止的不是“颜色强”，而是“颜色无组织”
重点避免：
- 无叙事理由的高纯色到处平均出现；
- 每个区域都争夺综合色焦点；
- 全画面统一橙染、蓝染或灰雾滤镜；
- 黑色死黑、浅色死白导致层级断裂；
- 人物肤色被环境综合色吞掉；
- 为了“统一”把暖灯、皮革、肤色和人物辅助色全部压成同一灰度。

## 3｜Scene Color Extension｜场景综合色扩展

每个新场景先从Global Color DNA派生文字版`Scene Color Extension Spec`，只改变环境需要改变的部分，保留项目长期的综合色组织原则。

### 必须继承（Global Invariants）
- 色族有组织、有功能，不做综合色随机扩散；
- 清楚明度层级与主体分离；
- 深色在出现时有结构，不死黑；
- 肤色家族与人物识别色保持可读；
- 实际光源/剧情强调色可以明确显色，但有来源和范围；
- 人物与环境仍属于同一二维综合色体系；
- **不继承固定饱和度上限、不继承固定夜雨蓝灰、不继承上一Scene的综合色比例。**

### 可以派生（Scene Variables）
- Environment Base Hue Family；
-综合色强度 / Chroma Density；
- 空气综合色 / 雾 / 天空 / 雪 / 植被 / 室内墙面；
- 新的大面积材质综合色；
- 日夜、季节、气候造成的综合色偏移；
- Scene主光色与辅光关系；
- 该地点自己的局部Accent Family；
-综合色是更轻、更浓、更冷、更暖、更清澈或更中性。

### 示例（只说明派生方法，不是固定色表）
- 雪原可以更轻、更清、更冷，也可以因夕阳/火堆出现明显暖色；
- 阴天旧城白昼可以以石材与天空中性色为基底，但不要求全面去色；
- 暖室内可以让皮革、木材、织物与暖灯综合色明显变丰富，同时避免无来源全画面橙染；
- 医疗/制度空间可以更干净、更冷或更中性，但不能自动漂成现代蓝白科幻UI；
- 遗迹/异常空间可以调用Threat / FX Exception，但不能无因改写正常人物肤色和主绘画系统；
- 花园/自然Scene可以拥有真实的植物综合色密度，只要仍通过项目的材质、明度与叙事层级组织，而不是为了“统一”全部灰化。


## 3.1｜Interior / Exterior Look Domain（V4.5.2）

同一Location Entity可以同时拥有室外与室内视觉身份，但默认不要强行用一套综合色图覆盖两者。长期/多镜Set至少登记：
- `EXTERIOR_LOOK`：天气、天空/环境基底、室外主光、远景综合色；
- `INTERIOR_LOOK`：室内材质、Practical Light、窗光关系、室内综合色密度。

两者共同继承Global Color DNA；若视觉关系高度一致可以共享Card，但必须显式说明共享原因。Look Domain一旦Approved，应一路投射到Coverage、Storyboard Execution Frame与Video，而不是静态图阶段结束后失效。

## 4｜V4.5.7 Scene Color Card自动派生与生成

**当前项目规则覆盖旧“按需才生成Scene Card”的默认。** 一个Approved `GLOBAL_COLOR_CARD / BASE_COLOR_CARD`作为综合色根。只要进入新的Scene或新的Interior/Exterior Look Domain，且当前Scope尚无Approved Scene Color Card，Controller必须自动派生文字Spec并立即创建`SCENE_COLOR_EXTENSION_CARD` Generation Job。

标准链路：
`Base Color Card → Scene Color Extension Spec → Scene Color Card Generation Job → Candidate QC/Approval → Scene Color Authority → Scene-bound Image / Shot Execution / Video`。

以下情况自动触发：
- 新`scene_id`；
- 同一Location发生`EXTERIOR_LOOK ↔ INTERIOR_LOOK`切换；
- 日夜/季节/长期材质环境构成新的持久Look Domain；
- 用户明确要求该Scene拥有独立综合色身份。

以下情况不重复建Scene Card：
- 同一Scene内普通镜头切换；
- 临时雷光、火光、灯灭等Shot Lighting Variant；
- 已有Approved且Scope完全匹配的Scene Card可直接复用。

正式Scene Color Extension Card必须记录：
- `Parent Global Color DNA / Base Color Card`；
- `derivation_kind = SCENE_COLOR_FROM_BASE`；
- `Scene / Location / Look Domain Scope`；
- `Inherited Invariants`；
- `Derived Variables`；
- `Chroma Density / Selective Saturation Logic`；
- `Material Families`；
- `Light Relationship`；
- `Character/Skin Preservation`；
- `Not Responsible For`：对象结构、身份、镜头构图、清晰度。

Scene Card未批准时，依赖它的Scene-bound正式图片Generation Job保持等待；不得用上一场景色卡或纯文字静默顶替。

## 5｜Shot Lighting Variant｜镜头光色变体

Shot Lighting Variant只负责当前Shot/Segment的临时照明与事件变化，例如：
- 灯灭/恢复；
- 门打开后暖光进入；
- 雷光；
- 火焰；
- 战斗FX；
- 聚光灯；
- 车辆经过造成短暂光扫；
- 同一场景从正常状态转为紧急状态。

默认用`TEXT_CONTROL`写进World State / Integrated Timeline，不自动生成新色卡图。

只有该Lighting State会持续跨大量Shot、模型反复漂移、且文字无法稳定时，才升级成可复用`LIGHTING_VARIANT_REFERENCE`。

## 6｜综合色层级冲突裁决

按以下顺序：
1. `Global Color DNA`决定不可漂移的项目综合色**组织语法与边界**；
2. `Scene Color Extension`决定当前地点/气候/材质的综合色派生，包括当前综合色强度；
3. `Shot Lighting Variant`决定当前时刻的临时光色与局部综合色提升/压低；
4. `Storyboard / Director`决定视觉叙事重点与画面分配；
5. `Character / Prop / Environment HD Object Authority`仍决定对象本身结构与材质细节。

**下层可以改变当前画面的综合色强度、冷暖、亮度与局部纯度，只要不破坏上层“综合色有组织、人物可读、材质/光源有逻辑”的语法。** Global Card也不能因为“全局”而硬把当前Scene锁回某个基准综合色。

## 7｜Reference Resolver规则

综合色参考遵守Minimum Reference Set：
- **先执行`color_authority_preservation_gate.md`：当前Scene已有Approved Scene Color Extension Card且任务属于其Scope时，Scene-bound Image / Shot Execution默认`VISUAL BIND FIRST`；Final Video默认`AUTHORITY LINEAGE FIRST`，已有正确综合色Primary Visual时不机械重复占色卡槽；**
- 若当前Scene已有Approved Scene Color Extension Card → 优先它承担当前综合色控制；Global Card通常转TEXT Authority，不机械同时上传；
- 新Scene/新Look Domain没有Scene Extension Card → 先执行`scene_color_card_auto_derivation.md`自动派生并生成Scene Card；Scene-bound正式图片/视频不得长期以Global Card或纯文字替代对应Scene Card；
- Shot Lighting Variant通常是TEXT_CONTROL；有Approved重复Lighting Reference且确有必要时才上传；
- 不把Global + Scene + Shot三张色卡全部上传“求保险”。

每张综合色图都必须通过`Why Now / What Field / Most Direct`。

### Composite Color Card Isolation｜复合色卡隔离
若Global / Scene Color Card同时包含角色、车辆、场景截图/示例图与色块：
- 示例图只证明综合色关系，不拥有其中人物身份、服装、车辆、道具或空间几何Authority；
- **当前Scene已有Approved Scene Color Card且任务属于其Scope时，不得仅因为整板有污染就直接降成TEXT_CONTROL。**
- 第一选择：使用已批准的`COLOR_ONLY_CONTROL_CROP`；
- 第二选择：对色块/光色关系区做**无生成式裁切**并登记为当前任务`CONTROL_CROP`；
- 只有综合色视觉Authority本来就不是Required，或平台客观不支持视觉Reference时才允许TEXT-only；
- 只有模型确实需要整板综合色关系且污染风险可接受时才使用整张`CONTROL_IMAGE`；
- 不因为Global Card顶部出现某角色/车内/剧院，就把这些实体带入当前Shot或写一串反向“不出现”。

综合色板的职责是**颜色关系**。污染的正确解法是隔离Crop，不是让综合色视觉Authority蒸发。具体绑定闸门读取`color_authority_preservation_gate.md`。

## 8｜70 / 20 / 10的正确地位

若项目保留70/20/10，它只是**Global Balance Heuristic（全局综合色平衡启发）**：
- 不能要求每个Shot按面积计算；
- 不能把它理解成“综合色只能占10%”；
- 人物特写、自然景观、雪原宽景、暖室内、剧院、强剧情灯光可以自然大幅偏离；
- 只在整季/整组镜头综合色分布失去层级时作为诊断参考。

## 9｜Color Derivation Hard Gate

Stage 03/04/05正式Prompt前检查：
- [ ] 当前Scene使用的是Global组织基线还是明确Scene Extension；
- [ ] 若当前Scope已有Approved Scene Color Card，已完成`SCENE COLOR AUTHORITY SCAN`：图片/Shot Execution选择最直接视觉综合色Authority；Final Video记录`scene_color_reference_mode`并只在Direct Trigger成立时加入色卡槽；
- [ ] 新环境没有被强制套用旧Scene的综合色；
- [ ] 没有全局`low-saturation / compressed chroma / desaturated`硬锁；
- [ ] 综合色采用色族集中 + 选择性显色 + 受控对比 + 清楚明度层级；
- [ ] 当前Scene允许根据材质、肤色、光源和叙事需要自然提高或降低综合色强度；
- [ ] 肤色/角色识别色没有被环境综合色吞没；
- [ ] Scene Extension只派生必要变量，没有重写Global Style DNA；
- [ ] Shot Lighting Variant没有被误升级成永久场景身份；
- [ ] 综合色Reference没有承担对象结构、清晰度或镜头构图；
- [ ] 复合色卡中的示例人物/场景/车辆没有被误迁移为当前Shot内容；
- [ ] 没有无必要同时上传Global / Scene / Shot三层综合色图。
- [ ] 新Scene/Look Domain已有Approved Scene Color Card，或其自动Generation Job正在合法等待审批；
- [ ] Scene-bound图片与Shot Execution直接绑定当前Scene Color Authority；Video保留同一Authority血缘，Named Asset平台仅在`DIRECT_REFERENCE`模式保留真实`@对应色卡`。

失败：`COLOR_DERIVATION_FAIL`，返回Stage 02/03综合色派生或Reference Resolver修正。
