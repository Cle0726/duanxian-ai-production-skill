# 03.3｜道具资产标准模板

> **Current Rule：道具采用 Master First → Coverage Driven。** 角色资产规则不受影响。

## 1. 何时资产化
重复出现、因果关键、身份锚点、动作关键、结构复杂、容易漂移时建立正式Prop Master（道具母图）。

Stage 03必须同时读取 `shot_coverage_asset_derivation.md`：**先建立一张正式高清Canon Master，再根据Stage 02真实Shot Coverage倒推必要视角/状态；禁止默认正背侧细节全套。**

## 2. Registry（道具登记表 / 台账）
- Prop ID（道具编号；保留既有ID，无ID时才建议PROP-*）
- Name（名称）
- Type（类型：个人道具/剧情道具/武器/文件等）
- Owner（所属角色，如有）
- Version（版本） / Status（状态）
- Dimensions（尺寸） / Human Scale（和手掌/人物身高的比例参照）
- Materials（材质）
- Function（功能）
- State Variants（持续状态变体）
- First Appearance（首次出现） / Used Episodes（使用集数）
- Mother Prompt（母图提示词） / Approved Canon Master（已批准正式主图）
- Structure Spec Ref（结构文字规格）
- Derived Coverage Views（由哪些Shot触发、Parent Master、版本/状态）

- Production Support References不属于Prop Canon组成；若Canon已定但当前复杂交互/Contact需要高清证据，按`production_support_reference_engine.md`单独登记为APPROVED SUPPORT。

`PR-01` / `WP-01`可继续作为“资产页类型”；Prop ID则是这个道具本身的全项目唯一编号。

## 3. Canon Master必须固定
一道具原则上先做**一张正式高清Hero Master**，优先选择最能读清轮廓、体量、材质、功能结构和识别细节的视角。

必须固定：
- 轮廓/几何
- 长宽厚度与Human Scale
- 材质
- 功能结构
- 非对称识别点
- 可动/开合/折叠/展开方式（如有）
- 可持握/操作区域
- 不能变化的Design Locks

**Canon Master不要求在同一张图里机械塞正/背/侧/顶/底。**

## 4. Structure Spec优先于无意义多视图
主图批准后先用文字记录主图看不到但下游必须知道的结构：正反面定义、非对称点、内外侧、机关、开合顺序、尺寸比例等。

只有Stage 02 Shot Coverage证明当前真实镜头存在**固定对象结构/可见面/开合结构**的图像级风险，且现有Approved Authority仍留下足以增加下游Video风险的静态歧义时，才生成Derived Coverage View。不能仅用“理论上文字可推”作为停止理由；但复杂手-物Interaction / Contact等非结构问题应转`production_support_reference_engine.md`，不要伪装成Coverage。

## 5. Derived Coverage View（衍生覆盖视图）
典型触发：
- Insert / Close-up明确看到背面/侧面/顶部/内侧；
- 剧情要求OPEN / UNFOLDED / MECHANISM_VISIBLE；
- 道具会翻转、落地、桌面俯拍，且关键结构易猜错；
- 反打后非对称结构必须保持；
- 近距离操作需要明确手与功能部件关系。

每张衍生图必须登记`Parent Master + Triggered By Shot(s) + Coverage Need + Why Master Is Insufficient`。

衍生图必须继承Approved Canon Master，**只补该角度/状态可见信息，不得改设计。**

## 6. 文本类道具
物理纸张结构/折痕/老化/版式与“需要准确可读的文字内容”分开管理，避免每镜随机生成文字。

## 7. State Variant（道具持续状态变体）
CLOSED→OPEN→DAMAGED、INTACT→CRACKED→SHATTERED等用于持续/结构性状态。

角度本身不是State Variant；短暂反光、普通手握、轻微湿水通常也不建Variant。若OPEN等状态只在一个镜头短暂出现且结构简单，可由Coverage/Prompt解决；只有持续跨镜头且结构显著变化时升级正式State Variant。

## 8. QC（道具质检）
- Canon Master是否一张图就足以清楚定义正式道具身份？
- 是否先跑过Shot Coverage，而不是默认生成正/侧/背全套？
- 每张Derived Coverage是否都有真实Shot触发与明确风险收益？
- same object across views（所有衍生视图必须还是同一个东西）
- scale（尺寸/人物比例稳定）
- function（功能结构正确）
- no random parts（不能随机多零件）
- story truth（符合剧情事实）
- style（画风一致）
- state continuity（状态连续）
- Coverage View是否错误承担Storyboard构图/临时动作职责？

## 9. PROP_CANON_VIEW_SET / IDENTITY-BEARING SURFACE（新增）

对剧情关键、非对称、开合、翻转、复杂机械或高频近拍道具，单一Hero Master不再总是足够。此类对象必须先识别`IDENTITY-BEARING SURFACES`：
- `FRONT_FACE`
- `REVERSE_FACE`
- `FUNCTIONAL_SIDE`
- `TOP_MECHANISM`
- `OPEN_INTERIOR`
- 其它真正承载身份信息且会被镜头看见的面

然后只为**CRITICAL**表面建立最小`PROP_CANON_VIEW_SET`，而不是机械六视图。示例：
- 盒子：`HERO_3Q_FRONT + REVERSE_3Q + OPEN_STATE`
- 武器/乐器：`HERO_3Q + FUNCTIONAL_SIDE + REVERSE_3Q + TOP_OR_ACTIVE_STATE`

新增硬门：`VISUAL_SURFACE_CLOSURE_GATE`。当后续镜头要看见某个Critical Surface，而当前Approved Authority既没有图像证据也无法由邻近Approved视角可靠推出时，报`PROP_VIEW_CLOSURE_GAP`，返回Stage 03补最小Canon View；不得在最终视频时让模型临场发明该面。

Coverage父级也升级为：`Nearest Visual Parent(s)`，不再默认永远只看Hero Master。新角度应优先继承与其最接近的已批准视角。
