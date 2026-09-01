# Character Closet Registry（角色衣柜登记系统）

> **用途：** 记录主要/反复出现角色“实际拥有”的日常服装与已批准搭配，让季节换装像真实人物从自己的衣柜里选择，而不是AI每个Scene凭空发明新皮肤。
>
> 默认是**文字型长期Registry**，不是强制生成一整张“衣柜母图”。它首先解决连续性、人物审美与个人创作者成本。

---

## 1｜Closet建立时机

以下人物建立Persistent Closet：
- 主角、主要配角；
- 一季内多次出现且会经历不同天气/场合的人物；
- 服装本身承担人物塑造或剧情识别的人物。

一次性群众/路人不强制完整Closet，可使用Light Wardrobe Profile。

每个Closet必须绑定：
- `Character ID`
- `Character Fashion DNA`
- `Wardrobe Diversity Matrix Ref`
- `Character Appeal Hooks`
- `Body Identity Authority Ref`
- 当前时代/地区/职业限制

---

## 2｜Closet Item ID（衣柜单品编号）

推荐类别：
- `OW-##` Outerwear｜外套
- `TP-##` Top｜衬衫/针织/上衣
- `MD-##` Mid Layer｜中间层
- `BT-##` Bottom｜裤/裙
- `DR-##` Dress｜连衣裙/一体式造型（含bodycon紧身连衣短裙、bodysuit连体衣、jumpsuit连体裤、背心裙）
- `SH-##` Shoes｜鞋靴
- `HO-##` Hosiery｜连裤袜/丝袜/裤袜（记录颜色与厚度：透明/半透明/不透；颜色服从角色Personal Palette与Hosiery Language，黑/白/米白/深灰/酒红/深棕等）
- `SC-##` Scarf｜围巾
- `GL-##` Gloves｜手套
- `HD-##` Headwear｜帽/头饰
- `AC-##` Accessory / Adornment｜非剧情关键日常个人装饰；角色Signature Adornment也登记在此，读取`personal_adornment_identity_system.md`

每件单品至少记录：
- `Item ID`
- `Name`
- `Category`
- `Season Range`
- `Weather Suitability`
- `Occasion / Formality`
- `Material`
- `Color`
- `Silhouette Function`
- `Appeal Function`（它如何帮助Primary/Secondary Appeal；无则写无）
- `Mobility`
- `Signature Detail`
- `Compatibility`（常与哪些Item搭配）
- `Forbidden Pairing`（如有）
- `First Approved Appearance`
- `Continuity Notes`
- `Adornment Identity Role`（仅AC类：SIGNATURE / ROTATING / FUNCTIONAL / SECONDARY）
- `Rotation Pool`（ROTATING时：AC IDs + Wear Conditions + LOOK Binding）
- `Current Active Adornment`（当前Scene/Episode真正佩戴的AC ID）

---

## 3｜Approved Look Recipe（批准穿搭配方）

角色每出现一套正式长期造型，建立一个`LOOK ID`，例如：

`LOOK-FALL-RAIN-01`
- TP-02
- MD-01
- OW-03
- BT-01
- SH-02
- SC-01

Look记录：
- `Story Phase`
- `Season / Climate`
- `Scene Type`
- `Formality`
- `Primary Appeal Carrier`
- `Secondary Appeal Carrier`
- `Silhouette Summary`
- `Color Balance`
- `Approved Character Master ID`
- `Allowed Runtime Configurations`（COAT_ON / OPEN / OFF等）
- `Body Presentation Mode`
- `Preserved Appeal Hook`
- `Body Beauty Evidence`
- `Costume Dramaturgy Ref`
- `Source Wardrobe Classification / Locked Plot Fields`

同一Look可跨多个Scene复用。

---

## 4｜Closet-First Outfit Assembly（衣柜优先搭配）

进入新的季节/场景/场合时，按以下顺序自动决策：

1. 读取Source Wardrobe Classification + Costume Dramaturgy（为什么穿）；
2. 读取Character Fashion DNA + Body Identity/Presentation Authority；
3. 读取环境与场合需求；
4. 从Closet筛选功能适配单品；
5. 检查是否能形成符合Project Wardrobe Canon的完整Look；
6. 选择当前`Body Presentation Mode`，确认Body Identity / Appeal仍成立；
7. 读取`wardrobe_diversity_design_matrix.md`检查真正的Styling/Structure撞型；并读取`personal_adornment_identity_system.md`检查当前Look是否保留Signature Adornment或合理INTENTIONAL_NONE；
8. 若可满足，优先复用/重组已有单品；
9. 只有现有Closet无法同时满足`剧情事实 + Dressing Motivation + 功能 + 人格 + 审美 + Body Beauty`时，才提出New Item。

### New Item Admission Gate（新单品准入）
新增单品必须写出：
- 为什么现有衣柜解决不了；
- 解决哪个明确需求；
- 是否未来可复用；
- 是否改变角色Fashion DNA（默认NO）；
- 是否需要新Character Master。

仅仅“想让这一Scene更新鲜”不构成新增理由。 **“小说里提到过这件衣服”本身也不构成新增理由**；除非它是`WARDROBE_PLOT_FACT`或确实符合当前Skill设计。

---

## 4.1｜Wardrobe Visibility Escalation Gate（服装可见性升级闸门）

`COAT_OPEN / COAT_OFF / GLOVES_OFF`不自动等于“只是Runtime小变化”。先判断这次穿脱是否暴露了**此前从未被Approved Visual Authority定义的大面积服装结构**。

### Runtime State足够
可直接沿用现有Master，当：
- 只是敞开一点外套，内层已经在Approved Master中清楚可见；
- 围巾松开/脱下后露出的领口已有明确设计；
- 手套脱下，手部身份已有Character Master；
- 变化不新增重要裁片、腰线、袖型、下装连接或Signature Detail。

### 必须回Stage 03补最小视觉Authority
若穿脱会暴露：
- 完整上衣/衬衫/针织此前完全不可见；
- 腰线、裙腰/裤腰、背部裁片、袖型等此前未定义；
- 新可见区域承担Primary/Secondary Appeal Hook；
- Storyboard/Video模型若无图必然需要“猜设计”。

则标记：`WARDROBE VISIBILITY GAP`。

优先建立**最小 Outfit Configuration Reference**，而不是机械重做整套2×2 Character Master。例如：
- 正面半身：COAT_OFF状态；
- 背面/侧面仅在确实影响后续镜头时补；
- 使用现有Character Master + Closet Item定义保持身份。

补充Reference批准后进入Closet，并成为该LOOK允许的Runtime Configuration Authority。

---

## 5｜Wardrobe State Ledger（服装状态台账）

World State对当前实际穿着进行运行时记录：

- `LOOK ID`
- `Items Worn`
- `Items Carried`
- `Items Removed + Location`
- `COAT_ON / COAT_OPEN / COAT_OFF`
- `SCARF_ON / LOOSE / OFF`
- `GLOVES_ON / OFF`
- `WETNESS`
- `DIRT / DUST`
- `DAMAGE / TEAR`
- `BLOOD / STAIN`
- `Last Confirmed Wardrobe Transition`

**Nothing Spawns. Nothing Vanishes.**
如果角色脱下大衣，下一Scene要么仍穿着、拿着、放在明确位置，或存在合理的Implied Transition；不能CUT后凭空消失。

---

## 6｜Transformation Return Rule（变身解除返回规则）

圣谱者进入Transformation时，先把日常衣物分成两类：

### A. WORN WARDROBE｜正在穿着的日常Look
- 当前真正穿在身体上的日常服装进入`SUSPENDED WORN WARDROBE STATE`；
- 变身礼服/武器/圣约指挥棒按Transformation Authority执行；
- 战斗结束后恢复**战斗开始前同一Daily LOOK ID与Runtime Configuration**，包括湿度、破损、COAT_OPEN等。

### B. DETACHED / CARRIED WARDROBE｜已脱下或独立携带的衣物
- 已经脱下拿在手里、搭在臂弯、放在椅子/车里/地上的大衣、围巾、手套等，**不随Transformation凭空消失**；
- 它们作为普通World State物体继续记录`Holder / Location / State`；
- 若变身动作需要腾手，必须有可见/可推断的放下、交给他人、掉落或其他合理Transition；
- 不能用“变身了”把手里的大衣吃掉。

战斗结束同步解除后：
- 恢复WORN部分的原日常Look；
- DETACHED / CARRIED物品继续保持战斗期间真实World State结果；
- 不得返回默认服装、错误季节Look或凭空把已丢失/放下物品重新穿回身上。

---

## 7｜Closet Growth（衣柜增长）

衣柜可以随剧情成长，但增长必须有原因：
- 跨季节采购；
- 新地区气候；
- 正式活动；
- 职业/身份变化；
- 他人赠送；
- 角色主动审美改变；
- 服装损坏/遗失后的替换；
- 剧情明确的Character Costume Arc。

新单品进入Closet后成为可复用长期资源，不应只服务一张图后被遗忘。

---

## 8｜Character Costume Arc（服装人物弧光，可选）

若剧情确实存在长期人物变化，可记录：
- 早期Fashion DNA表现；
- 中期变化；
- 后期变化；
- 哪些改变来自人物主动选择，哪些只是天气/场合；
- 哪些Signature Item保留作为身份连续性。

**不得把普通换季误判为人物成长。**

---

## 9｜成本控制

- Closet Registry默认只写文字，不额外制造“每件衣服一张资产图”；
- 优先复用Approved Character Master与已有单品结构；
- 只有正式长期Look进入剧情才生成必要Character Master；
- 局部新单品若可通过Local Patch稳定加入，优先Patch，不整个人物重生；执行时读取`inpaint_local_patch_authority_engine.md`，新单品图/结构图若已存在必须作为PATCH_DESIGN_AUTHORITY；
- 角色衣柜用于减少随机重设计与视频重抽，而不是增加资产负担。
