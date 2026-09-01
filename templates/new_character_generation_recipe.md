# New Character Generation Recipe（新人物统一抽卡配方）

> **用途：** 当《断弦之歌》出现尚未建立APPROVED Character Master（已批准人物母图）的新人物时，Stage 03默认读取本模板。目标是继承已经被项目实际生成验证过的**二维插画生成策略、去写实策略、线条/皮肤/头发/色彩语言**，同时建立独立身份，让新人物像“同一部作品、同一位画师体系”中的新角色。

## 1｜来源与定位

本Recipe提炼自项目内已经成功生成并批准的人物资产Prompt共同结构。它与 `project_style_dna.md` 的职责不同：

- `Project Style DNA`：定义**最终结果应该长什么样**；
- `New Character Generation Recipe`：定义**新人物Prompt应该按什么结构组织，才能更容易生成到该画风**；
- `Character Design Data`：定义**这个新人物是谁**，包括年龄、骨相、气质、发型、身材、职业、服装等。

**绝对禁止：** 为了保持画风，直接复制任何现有角色的脸型、眼睛、发型、年龄、服装或个人气质。

## 2｜核心生成策略（Verified Prompt Strategy）

### 2.1 Prompt前段先锁定二维插画方向

新人物Prompt开头必须先明确二维插画方向。全局反写实/反3D限制由本文件第7节统一从Project Style DNA编译一次，不在前段重复。默认保留这套已验证的**正向**语言逻辑：

```text
anime illustration, 2D illustrated character art, clean digital painting,
hand-drawn illustrated line art, cel-inspired color blocking with soft painterly shading,
illustrated key visual
```

> **注意：** 这里的 `anime illustration / cel-inspired` 是**生成控制词**，目的是把模型从真人/3D方向拉回二维插画；它们不意味着最终画面要变成扁平赛璐璐或夸张动漫脸。最终视觉判断仍以 `project_style_dna.md` + 正式Render Style Authority为准。

### 2.2 通用画法模块

```text
art style: Japanese anime-inspired 2D illustration with restrained dark European retro mood,
clean confident linework,
flat-to-soft illustrated color blocking transitioning into soft painterly light gradients,
matte illustrated skin,
stylized but structurally clear facial rendering,
rich but restrained color palette with controlled chroma concentration and selective saturation,
subtle brush texture,
European retro fashion illustration atmosphere
```

这里保留的是**画法**，不是人物身份。

### 2.3 新人物身份模块必须重新设计

根据剧本、角色功能和世界观自动生成，不得套用任何现有角色模板：

- 性别 / 年龄段；
- 地域与欧洲骨相方向；
- **Face Identity Matrix**：脸型、额头/颧区、面中长度、下颌/下巴、鼻、嘴、眼距、眉眼关系、默认表情；
- **Base Eye Identity**：眼裂比例、外眼角、上下眼睑、睫毛组织、虹膜尺度与默认视线；
- **Hair Identity Architecture**：远景剪影、头顶体积、分缝/刘海、脸旁发、侧面体积、后发结构、发尾与发束质感；
- 身高、体型、肩颈、姿态；成年角色体型按短剧流量审美理想化：女性允许明显胸腰臀曲线、长腿与窈窕比例，**可具体描写丰满胸型体积感、纤细腰、圆润臀腿线、饱满腿线**；男性允许宽肩窄腰、清晰胸背肩腹线条，**可具体描写胸肌轮廓、腹肌分区、结实前臂**；不同角色身材类型需区分（丰满/窈窕/高挑/健美等），禁止全员同一副身材；体型描述必须写入Prompt的IDENTITY高权重段，生成时身材被弱化按 `BODY_IDENTITY_DRIFT / BODY_BEAUTY_SUPPRESSED` 处理并重试； 身体身份与服装呈现必须分权，读取`body_identity_presentation_authority.md`，不得要求所有新人物都靠收腰/贴身/高腰证明好身材；
- 职业、阶层、生活经历带来的克制差异；
- 气质方向按流量审美放开：成年角色允许成熟妩媚、冷艳、飒爽、攻击性吸引力等方向，清纯/保守不再是默认选项；气质必须与人格、职业与世界观一致，并与Appeal Hook互相支撑；未成年角色不使用成人性感化规则，但允许完整的非性化人格差异，不限定为可爱/清爽模板；
- 不得通过毛孔、真实皱纹、脏污或3D骨相表达年龄/经历。

### 2.3.1 新人物反模板前置

首次角色生成前必须读取：
- `character_identity_differentiation_engine.md`
- `face_identity_matrix.md`
- `hair_identity_architecture.md`
- `wardrobe_diversity_design_matrix.md`

先建立Identity Distinction Card并与项目现有角色做Collision Check；不是“生成后发现像别人再补救”。

### 2.4 眼睛规则

可以保留“较真人略大、清楚、有表现力”的插画化眼睛，但必须根据角色差异重新设计。

**禁止把通用Recipe机械写成：**
- 所有人都是“large anime eyes”；
- 所有人都是圆润少年/少女脸；
- 多名女性角色共享同一张脸或同一眼型模板；
- 多名男性角色共享同一张脸或同一骨相模板。

推荐写法：

```text
anime-influenced illustrated eyes with character-specific proportions,
explicit character-specific eye aperture, outer-corner trend, upper/lower lid geometry,
brow-eye spacing and lash organization,
character-specific iris scale and default gaze,
stylized facial planes that preserve the approved Face Identity Matrix,
expressive without exaggerated manga proportions
```

## 3｜皮肤、头发与线稿的通用成功规则

### Skin（皮肤）
统一保留：

```text
smooth matte illustrated skin,
soft simplified tonal shading
```

### Hair（头发）
绘画方法可以统一，但**发型设计不能统一**。结构必须先服从`hair_identity_architecture.md`，再使用以下通用绘画语言：

```text
hair drawn with clean flowing illustrated linework,
organized in readable larger hair masses and strands,
illustrated hair grouped into controlled larger clumps rather than microscopic strand detail
```

### Linework（线稿）
- 干净、克制、有结构；
- 人物轮廓、五官、发束、服装裁片有明确但不过粗的线；
- 不做粗黑漫画线；
- 不允许线稿完全消失成无描线写实概念图。

## 4｜服装自动设计规则

若小说/剧本提供服装描述，先读取`source_wardrobe_adaptation_authority.md`分类；普通描写不是最终造型硬锁，剧情必要字段才锁定。

新人物服装不能从任何现有角色直接复制，也不能只把“法式都市简约”当作全员默认制服。先读取 `wardrobe_environment_analysis_template.md` + `wardrobe_style_design_engine.md` + `wardrobe_diversity_design_matrix.md`，根据：

**季节 + 气候 + 地区 + 室内/室外 + 职业 + 阶层 + 场合 + 活动 + 世界观年代限制**

自动设计完整当前剧情阶段服装。

### 4.1 默认时代服装引导
除非剧情明确另有要求，日常人物以 **20世纪70—90年代欧洲都市/地区现实服装光谱** 为主要时代基底，同时允许法式都市极简、中欧实用、北方功能、南欧柔软层叠、工匠/职业/阶层等不同个人子语言。

可使用但不得机械全员套用：长/短外套、风衣、旧皮夹克、工装/职业外层、衬衫、马甲/背心、开衫、不同领型针织、直筒/宽腿/锥形裤、不同长度裙装/连衣裙、工作制服元素、皮鞋/短靴/长靴/实用鞋。具体组合必须由角色Fashion DNA与Wardrobe Diversity Matrix决定。

不要把“旧剧院/古堡/历史建筑”自动翻译成戏服化历史造型；只需要避免 costume-like period fashion / steampunk cosplay，不需要在Prompt里反复堆砌具体历史服装禁词。

共同美术语言可以继承：
- 欧洲复古；
- 法式/中欧/北欧等符合人物地区和身份的克制剪裁；
-综合色色族集中、人物识别清楚；不要求统一低饱和，肤色、服装与材质可按Character DNA自然显色，同时保留清楚明度层级与人物可读性；
- 清楚服装裁片与柔和织物线条；
- 不堆无剧情意义的装饰；但克制不等于空白。主要/反复新角色必须读取`personal_adornment_identity_system.md`，主动判断是否适合1件Signature Adornment或0–1件Secondary装饰；`INTENTIONAL_NONE`需要角色理由。

人物母图直接包含当前完整服装与当前批准的个人装饰，不默认拆独立Wardrobe Master。若Signature Adornment很小且会在近景反复可见，可按需建立`AD-01`。

服装差异不得主要依靠换颜色。新人物与同Scene/同年龄层角色不要求机械凑够固定数量的结构差异；综合比较`Silhouette / Proportion Rhythm / Collar-Neckline / Shoulder-Waist / Layer Density / Bottom-Hem / Footwear / Material Mix / Body Presentation / Styling Habit`，只要整体Styling Signature清楚区分即可。只有多维同时高度重合、远看像同一套模板时才返工。

## 5｜Color Recipe（综合色彩配方）

新人物必须服从Global Color DNA与`project_style_dna.md`，但可以有自己的识别色；进入具体Scene后由Scene Color Extension / Shot Lighting决定环境光色。

综合色由Character Fashion DNA + Global Color DNA决定，不设所有新人物共用的固定综合色清单。

可参考但**不得机械套用**的历史常见色族包括：charcoal / deep navy / ash gray / brown / ivory / dusty rose / gray violet等；角色也可以根据身份、地区、剧情阶段和服装材质使用更清亮、更暖或综合色更明确的综合色。

长期要求：
- soft illustrated gradient shading；
- no realistic photographic color complexity；
- avoid arbitrary hyper-saturated fashion color scatter；
- selective saturation is allowed when it belongs to the character and remains compatible with the project Color DNA。

**角色识别色 ≠ 改变项目画风。**

## 6｜默认人物母图格式

新人物第一次正式建档默认优先生成：

```text
9:16 vertical high-resolution character reference sheet,
portrait-oriented canvas,
2x2 grid layout on plain neutral gray background,
four panels:
FRONT FACE,
SIDE FACE,
FRONT BODY,
BACK,
clean panel dividers,
consistent character identity, outfit, proportions and rendering across all four panels
```

除非角色当前生产需求明显不适合2×2，否则以此作为第一张Character Master候选。**该2×2的整张Sheet仍固定9:16竖版，不得因为项目视频/Storyboard常用16:9而改成横版。**

## 7｜Negative Lock（负面锁去重）

新人物正式Prompt的全局反写实/反3D/反摄影限制，**只从 `project_style_dna.md` 的 `Negative Style Lock` 编译一次**，本文件不再维护第二份同义长列表。

在全局锁之后，只追加新人物任务真正独有的限制：

```text
consistent facial identity across all panels,
no unrequested accessories,
no identity cloning from existing characters,
no unintended age drift
```

年龄必须按角色设定执行：年轻角色避免意外老化；中年/老年角色不能被通用负面词错误年轻化，年龄通过二维骨相、姿态、少量绘画线条与发色表达。

**Verified Generation Recipe仍保留正向关键词**（anime-influenced 2D illustration / hand-drawn linework / cel-inspired color blocking / soft painterly shading / matte skin等）；本次只删除重复Negative，不改变已验证成功的正向画风配方。

## 8｜Reference Binding（参考图绑定）

生成新人物时，优先调用：

1. `Render Style Anchor / Approved Style Evidence`：已经批准的《断弦之歌》绘画语言参考；
2. `Global Color DNA / Color Script`：控制项目综合色语法；
3. 与该人物剧情阶段相关的服装/职业/道具结构参考（如必要）；
4. 新人物尚无Character Master时，**不得把任何现有人物母图当成新人物的身份参考**。

如确实需要用现有角色图帮助模型理解项目画法，只能标记为：

> **Style-only Reference（只参考画法）**：只参考二维线条、皮肤渲染、头发画法、阴影与材质表现方法，不复制脸、发型、体型、服装、配饰或身份；不把该参考图的清晰度、锐度、细节密度或完成质量当作输出Authority。

## 9｜自动生成流程

当剧本出现新人物且没有APPROVED Character Master时：

1. 读取角色剧情功能与世界观；
2. 判断是否值得资产化（路过背景人不机械建完整母图）；
3. 读取Project Style DNA；
4. 读取本New Character Generation Recipe；
5. 自动设计与现有角色有区分度的骨相、脸型、眉眼、发型、体型与气质；
6. 运行Wardrobe & Environment Analysis，设计当前完整服装；
7. 输出完整可复制2×2 Character Master Prompt；
8. 用户生成候选；
9. Candidate Triage + QC；
10. 用户明确批准后 → APPROVED → Approved Asset Archiver归档；
11. 后续镜头只调用该角色自己的APPROVED Character Master，不再依赖通用抽卡Recipe维持身份。

## 10｜新人物QC

除了Stage 03通用QC，额外检查：

- **Same Project Style**：是否像《断弦之歌》同一作品；
- **Distinct Identity**：是否明显不是某个现有角色简单换发型、换衣服；
- **2D Lock**：是否仍是二维插画，没有真人/3D/游戏化；
- **Skin Lock**：皮肤是否哑光无毛孔；
- **Hair Lock**：是否是插画发束而非照片级逐根毛发；
- **Face Diversity**：新人物年龄、脸型、眉眼与角色功能是否独立成立；
- **Wardrobe Logic**：服装是否符合季节、环境、职业和年代；
- **Color Cohesion**：有自己的识别色，但没有跳出项目综合色体系。

## 11｜失败处理

如果新人物反复偏真人：
- 先检查Prompt前段是否仍然强锁二维插画；
- 检查是否混入“realistic skin / photorealistic / cinematic live-action”等高权重冲突词；
- 检查参考图是否带入真人/3D风格；
- 强化Anti-Realism Lock；
- 不要无限增加互相冲突的风格词。

如果新人物画风对但“像旧角色换皮”：
- 不改Style模块；
- 只重写Character Design Data：脸型、眉眼、鼻颌、发型、年龄感、体型、气质和服装识别点。
