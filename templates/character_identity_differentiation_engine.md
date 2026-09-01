# Character Identity Differentiation Engine（角色个体识别与反模板引擎）

> **用途：** 防止《断弦之歌》角色在同一画风下逐渐收敛成“同一张脸 + 同一种发型 + 同一套眼睛 + 同一个衣柜换颜色”。本引擎只强化**个体识别**，不改变项目统一二维画风。
>
> **适用：** 正式Character Master、新人物、主要/反复角色、所有可变身圣谱者。一次性SCOPED_CAST可使用Light Profile，不强制完整资产组。

---

## 1｜核心原则

**Same World ≠ Same Face. Same Beauty Standard ≠ Same Person.**

项目统一的是：
- 绘画方法；
- 时代与世界观；
-综合色组织；
- 材质与审美边界。

不得统一成：
- 同一脸型；
- 同一眼裂/眉眼关系；
- 同一刘海 + 长直发；
- 同一“美女V脸”；
- 同一套变身眼妆换颜色；
- 同一服装廓形换配色。

---

## 2｜Character Identity Stack（角色身份栈）

每个正式角色至少建立五个并行身份层：

1. `FACE ID` → 读取 `face_identity_matrix.md`
2. `HAIR ID` → 读取 `hair_identity_architecture.md`
3. `EYE ID` → 日常眼部 + 可变身角色读取 `eye_signature_ledger.md`
4. `WARDROBE ID` → 读取 `wardrobe_style_design_engine.md` + `wardrobe_diversity_design_matrix.md`
5. `ADORNMENT ID` → 读取 `personal_adornment_identity_system.md`

五层必须互相支持，但不能只有一个层负责“区别角色”。

例如：
- 不能只靠发色区分两张同脸；
- 不能只靠服装区分相同脸和相同头发；
- 不能只靠瞳孔颜色区分两个圣谱者；
- 不能只靠随机耳环/项链区分两个同模板人物；
- 不能只靠“一个冷艳、一个温柔”这种抽象形容词通过QC。

---

## 3｜Identity Distinction Card（个体识别卡）

正式Character Master生成前必须建立：

```text
Character ID / Name:
Age Read / Maturity:
FACE ID Summary:
- Face Outline:
- Midface / Jaw / Chin:
- Nose / Mouth Signature:
- Brow-Eye Relationship:
- Resting Expression:

HAIR ID Summary:
- Far Silhouette:
- Part / Fringe Grammar:
- Side-Face Framing:
- Back / Nape Architecture:
- Texture / Clump Grammar:

EYE ID Summary:
- Base Eye Aperture / Outer-corner Trend:
- Lid / Lash / Brow Signature:
- Iris Scale / Default Gaze:
- Transform Eye Signature (if applicable):

WARDROBE ID Summary:
- Personal Wardrobe Archetype:
- Silhouette Family:
- Proportion Rhythm:
- Collar / Shoulder / Waist Language:
- Layer Density / Material / Footwear:
- Forbidden Generic Outfit:

ADORNMENT ID Summary:
- Strategy: SIGNATURE / ROTATING / FUNCTIONAL / MINIMAL / INTENTIONAL_NONE
- Primary Signature Adornment:
- Placement / Scale / Shape:
- Material / Wear:
- Wardrobe / Hair Relationship:
- Forbidden Generic Accessory Pattern:

Closest Existing Character:
Non-color Differences:
Collision Result:
```

---

## 4｜Four-View Identity Lock（四视图身份锁）

`DV-01 / TF-01`的2×2四视图不是“同一张标准美脸配不同角度”。四格分别承担不同身份证据：

### FRONT FACE
必须清楚读出：
- 脸型宽窄与下颌；
- 眼距、眼裂、上/下眼睑趋势；
- 眉眼距离与眉峰；
- 鼻/唇/下巴识别点；
- 刘海与发际线；
- 可变身角色的核心眼部签名（TF-01）。

### SIDE FACE
必须清楚读出：
- 额头—鼻梁—鼻尖—唇—下巴的侧面节奏；
- 眼窝/睫毛侧视轮廓；
- 颧区/下颌转折；
- 耳前发、鬓角、后脑体积；
- 变身眼线/眼影的侧面延伸方式（TF-01）。

### FRONT BODY
必须读出：
- 体型/肩颈/姿态；
- 当前完整Look的比例与廓形；
- 发型与服装整体如何共同形成角色剪影。

### BACK
必须读出：
- 后脑/发束/束发点/发尾真实结构；
- 肩背与服装后片；
- 发型不能只是“正面长发的随机背面”。

如果四格只证明“是同一个漂亮角色”，却不能证明“为什么不是项目里另一个角色”，判：
`CHARACTER IDENTITY WEAK`。

---

## 5｜Cross-Character Collision Matrix（跨角色撞型矩阵）

正式角色与同年龄/同性别表达最接近的至少3名现有角色比较：

### Face维度
`Face Outline / Midface Length / Jaw / Chin / Nose / Mouth / Eye Spacing / Brow-Eye Relationship / Resting Expression`

### Hair维度
`Far Silhouette / Crown Volume / Part / Fringe / Face-framing / Side Volume / Back Mass / End Shape / Texture Grammar / Asymmetry`

### Eye维度
`Eye Aperture / Outer Corner / Upper Lid / Lower Lid / Lash Pattern / Iris Scale / Gaze / Transform Eye Signature`

### Wardrobe维度
`Silhouette Family / Proportion Rhythm / Collar-Neckline / Shoulder / Waist / Layer Density / Bottom-Hem / Footwear / Material Mix / Styling Habit`

### Adornment维度
`Adornment Strategy / Category / Placement / Scale / Shape-Motif / Material / Asymmetry / Wear Habit`

### Hard Fail
- 两名核心角色可被描述为“同脸换发色”；
- 同脸型 + 同眼型 + 同刘海结构同时成立；
- 两名可变身角色“同款眼妆/瞳孔换颜色”；
- 同Scene多个角色像同一品牌同一季Lookbook；
- 多个主要角色全员无装饰且没有明确理由，或都戴同位置同类别的模板首饰；
- 角色的所有差异只能用综合色描述。

标记：`CHARACTER_TEMPLATE_COLLISION_FAIL`。

---

## 6｜差异不等于夸张

反模板不要求每个人都怪异或漫画化：
- 可以都美型，但骨相与五官节奏不同；
- 可以都长发，但轮廓、分缝、脸旁发、后发、发尾与动态不同；
- 可以都穿欧陆复古，但廓形、比例、材质、层次与穿衣人格不同；
- 可以都拥有音乐化眼部，但结构语法不同。

**目标是“同一位美术设计的不同人物”，不是“不同画风拼盘”。**

---

## 7｜Stage / Authority

### Stage 03
- 新人物先建立Identity Distinction Card；
- 通过Collision Check后再编译Character Master Prompt；
- 主要/反复角色、可变身角色必须完整执行；
- 一次性SCOPED_CAST可只记录2–4个强识别点。

### Stage 04/05
- 不重新发明脸型、发型、眼妆或服装；
- 当前镜头可见这些关键特征时，Reference Resolver必须选择足以承载对应身份字段的Approved资产。

---


## 7.1｜Existing Approved Character Protection（既有已批准角色保护）

当前版本的反模板规则**不自动重设计已经APPROVED的角色**。已有Character Master / TE-03 / TH-01 / Approved Look继续是Authority。

只有以下情况才进入正式重设计：
- 用户明确要求重做；
- 当前生成的新版本已经出现明显模板碰撞；
- 旧资产本身无法支撑后续生产且用户批准修订。

对旧角色发现“历史上相似”，默认记录Collision Note并优先保证未来新角色避开，不擅自改脸。

## 8｜QC

至少PASS：
- `FACE DISTINCT`：遮住头发仍能从脸部结构区分；
- `HAIR DISTINCT`：缩成剪影仍能从发型轮廓大致区分；
- `EYE DISTINCT`：近景不靠颜色即可识别眼部语言；
- `WARDROBE DISTINCT`：遮住脸后仍能从服装比例/廓形看出穿衣人格；
- `SAME WORLD`：差异没有破坏统一画风。
