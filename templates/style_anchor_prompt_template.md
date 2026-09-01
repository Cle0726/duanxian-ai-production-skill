# Style Anchor Prompt Template（视觉风格板模板）

> **用途：** 当前Style Authority拆为 `Render Style Anchor（绘制画风锚点）` 与 `Cinematic Shot Style Anchor（镜头画风/摄影语法锚点）`。详细权限先读取 `visual_style_authority_engine.md`。
>
> 本模板只负责建立/整理风格证据，不替代Character / Environment / Prop Authority，也不把Style Board自身画质当成下游清晰度标准。
> **Current Copy Surface Gate：** 任何真正送给图片模型的新Style Board Prompt都必须通过`model_facing_prompt_surface_sanitizer.md`；不得输出“资产目标/Authority Boundary/输入图/文件名/路径/内部Role”等生产说明。完成Style Board / Evidence后，下游Stage 03/04/05通过`style_authority_projection_gate.md`决定视觉Direct Binding + MINIMAL文字，或在无视觉输入时使用FULL风格句群。

## 1｜先判断：需要“生成新风格板”还是“整理Approved Evidence”

### A. APPROVED_STYLE_EVIDENCE_BOARD（优先）
当项目已经有稳定、已批准的人物、场景、道具或镜头时，优先从真实Approved资产中挑选代表图组成Evidence Board。

可以包含：
- 项目真实角色；
- 项目真实场景；
- 真实已批准镜头；
- 已批准材质/道具细节。

但下游只读取它被授权的Style Grammar，**不能把Evidence Board中的具体身份、服装、场景几何、道具结构迁移到别的对象。** 真正作为模型Reference时按目标模型Capability与真实风险路由：只要平台可接收相应图片Reference、`DIRECT_STYLE_BOARD != VERIFIED_FAIL`且没有已观察Sample Content Bleed / Layout Literalization，就优先Direct Bind并使用最短Role Lock；`UNKNOWN`本身不触发降级。只有真实Bleed/Literalization、已证明槽位问题、用户要求或`ROLE_SEPARATION=VERIFIED_FAIL`才改变Direct路线；Role Separation失败优先CONTROL_CROP / Dedicated Channel，生成式STYLE_APPLIED_REFERENCE只在无安全非生成式隔离时使用；TEXT_CONTROL只补充视觉输入无法表达的剩余风格约束。

### B. GENERATIVE_STYLE_BOARD
只有项目尚未形成稳定正式视觉证据，或用户明确要探索新画风时，才生成匿名/泛化Style Board。

匿名人物与泛化环境只是避免未批准内容进入Canon的保护手段，**不是成熟项目必须遵守的固定版式。**

## 2｜Render Style Anchor（绘制画风锚点）

它必须回答：
- 人物怎么画；
- 线稿怎么画；
- 皮肤/头发怎么表现；
- 色块与柔和阴影怎么配合；
- 环境如何保持与人物同一二维绘画系统；
- 皮革/木材/金属/针织/石材/玻璃等材质用什么绘画方法表达。

它**不负责**：
- 当前人物是谁；
- 当前地点几何；
- 当前道具结构；
- 某一镜的具体机位/构图；
- 清晰度、锐度、像素密度或最终完成质量。

## 3｜Cinematic Shot Style Anchor（镜头画风 / 摄影语法锚点）

它回答：
- 项目通常怎样使用Wide / Medium / Profile / OTS / Interior Ensemble；
- 人物与环境面积关系；
- 前景/中景/后景如何组织；
- 留白/负空间如何使用；
- 玻璃、窗框、门框、雨线、反射等如何成为空间层次；
- 实际灯源怎样参与视觉引导；
- 整体摄影节奏是克制、文学、安静还是炫技。

它**不负责**：
- 复制某张参考的精确相机位置；
- 覆盖Director Breakdown / Storyboard已经锁定的Shot；
- 角色动作/Blocking；
- 场景几何；
- 对象身份/清晰度。

**Storyboard / Director Shot Contract > Cinematic Shot Style Anchor。**

## 4｜Board Canvas / Layout（版式）

Style Authority不绑定固定比例：
- 4:3横向证据板可以；
- 16:9横向开发板可以；
- 竖版信息卡可以；
- 自由拼板可以。

版式只服务信息组织。**不得因为Style Board是4:3或16:9，就把Character Master / Environment Master / Storyboard / Video改成同一比例。**

若生成新的Style Board：
- 使用中性浅灰/暖灰排版底；
- 分隔简洁；
- 不把纸张纹理/旧纸印刷感烤进人物或场景本体；
- 标题/标签只在用户确实需要信息卡时加入，不作为Style本体。

## 5｜Generative Render Style Board推荐内容（仅从零建风格时）

可选6类证据，不要求固定3×2：
1. 匿名成年男性半身：欧洲骨相、二维动漫影响比例；
2. 匿名成年女性半身：中性表演，用于展示二维脸部绘画方法；不得定义项目女性角色统一脸型/眼型；
3. 匿名人物全身：成熟近现代欧洲都市服装比例；
4. 泛化旧欧洲环境：任选与当前项目基准相符的室外/室内；
5. 材质小样：皮革、木、金属、针织、石材、玻璃；
6. 色块只作为综合色关系辅助，正式综合色权威仍交给`color_script_derivation_engine.md`。

不要求所有板都必须包含“夜雨旧城”；新项目阶段可以选择能代表当前视觉语言的其他环境。

## 6｜人物主画法（长期规则）

```text
anime-influenced 2D illustrated character art,
clean hand-drawn linework,
cel-inspired controlled color blocking with soft painterly shading,
idealized semi-realistic European facial structure,
anime-influenced proportions,
anime-influenced illustrated eye proportions without a fixed universal eye shape,
facial planes shown as rendering examples only, not a universal face template,
matte painted skin,
readable hair masses with a few fine strands,
unified 2D character-environment rendering system,
restrained melancholic literary mood.
```

综合色不要写成全局`low-saturation / compressed-chroma / low-contrast`硬锁，统一表达为综合色组织原则：

```text
rich but restrained palette,
controlled chroma concentration,
selective saturation according to skin, material, practical light and narrative focus,
controlled contrast,
preserved value hierarchy,
clear subject-background separation,
scene-adaptive chroma; never globally greyed or color-starved.
```

## 7｜Render Style Board Prompt骨架（需要生成新板时）

真正给模型时不输出内部Authority说明，直接写可见结果：

```text
Create a clean production render-style evidence board for a 2D illustrated dramatic series. Use only the evidence zones actually needed to demonstrate linework, facial rendering, hair grouping, material painting, environment-character integration and controlled color behavior; do not force a fixed grid.

Japanese-anime-influenced 2D illustration with clean confident hand-drawn linework, cel-inspired controlled color blocking with soft painterly shading, matte painted skin, readable grouped hair masses, aged and lived-in materials expressed through 2D painting rather than photoreal PBR rendering, and one unified character-environment rendering language.

Rich but restrained palette, controlled chroma concentration, selective saturation where skin, materials and practical lights need color presence, controlled contrast, preserved value hierarchy, clear subject-background separation, scene-adaptive chroma without a whole-frame color wash.

Use anonymous generic subjects and environments only when new evidence is needed. Do not establish a recurring character identity, exact location geometry, exact shot composition or object canon. No photorealism, live action, 3D/CGI/PBR look, pore-level skin, plastic hair, cyberpunk neon, orange-blue blockbuster grading or hyper-saturated fashion illustration.
```

内部可以记录“它只承担Style Grammar”，但这句Authority说明不复制给生成模型。

## 8｜Cinematic Shot Style Board Prompt骨架（仅确实需要生成时）

```text
Create a compact cinematic-composition evidence board for the same 2D illustrated project. Show only a few genuinely distinct examples of wide, medium, profile, over-the-shoulder, interior ensemble and environmental composition as needed. Emphasize subject-to-environment scale, foreground/midground/background layering, negative space, doors/windows/glass/reflection as depth devices, and practical light sources as compositional guides.

Keep the examples generic rather than copying any existing shot exactly. Do not establish character identity, exact location geometry or a specific final shot blocking.
```

## 9｜QC

### Render Style Anchor
- 人物仍是项目正式二维插画体系，而非真人/3D/欧式绘本；
- 线稿、皮肤、头发、材质表现方法统一；
-综合色有组织但不被统一压低彩度；综合色强度可随Scene变化，同时明度结构清楚、不灰糊、不综合色散乱；
- Evidence中的角色/场景没有变成下游身份Authority；
- 版式比例没有被写成项目输出比例。

### Cinematic Shot Style Anchor
- 能看出项目独特的镜头组织习惯；
- 不只是“漂亮电影截图合集”；
- 没有固定某个地点/角色的精确Blocking；
- 不与Storyboard具体机位Authority冲突；
- 不承担清晰度或对象细节。

失败：`VISUAL_STYLE_AUTHORITY_FAIL`。


## Current｜Video Downstream Isolation

Render Style Board / Style Evidence Board属于`VISUAL_STYLE_CONTROL_AUTHORITY`。它可以证明“怎么画”，但整板中的人物、地点、样片构图、综合色块、标签与版式对剧情内容Authority=0。进入Final Video前必须读取`visual_reference_routing.md`：若当前Approved Character/Environment/Assembly已经更直接体现同一Render Style，可优先使用这些正式图；若`DIRECT_STYLE_BOARD != VERIFIED_FAIL`且当前没有已观察Sample Content Bleed / Layout Literalization，multi-example Style Board可以直接承担Render Style字段，并用最短Role Lock限制样例人物/构图越权；`UNKNOWN`不等于禁止。已发生Sample Content Bleed、布局Literalization、`ROLE_SEPARATION=VERIFIED_FAIL`、已证明槽位冲突或用户明确要求时可以改变Direct路线；Role Separation失败优先Clean Crop / Dedicated Style Channel，只有不存在安全非生成式隔离时才使用`STYLE_APPLIED_SCENE_REFERENCE`。**专用Style-only Channel不是Direct Bind的唯一合法条件。**
