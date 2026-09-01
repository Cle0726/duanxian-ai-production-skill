# Visual Style Authority Engine（视觉风格权限引擎）

> **用途：** 把“怎么画”和“怎么拍”拆成两个不同的项目级长期Authority，避免一张Style Board既管线稿/材质，又偷偷覆盖Storyboard具体机位与构图。
>
> **核心原则：** `Render Style Grammar ≠ Cinematic Shot Grammar ≠ Shot-Specific Composition`。

## 1｜两类Style Authority

### A. Render Style Anchor｜绘制画风锚点
只控制“这个世界怎样被画出来”：
- 二维绘画语言与线稿；
- 人物脸部概括、哑光皮肤、发束组织；
- 色块与柔和绘画阴影；
- 人物与环境属于同一绘画系统；
- 皮革、针织、金属、木材、石材、玻璃等材质**表现方法**。

不控制：
- 具体人物身份/服装Canon；
- 具体场景几何；
- 具体道具结构；
- 当前Shot的精确机位、景别、站位；
- 图片自身的分辨率、锐度、细节密度或最终清晰度。

### B. Cinematic Shot Style Anchor｜镜头画风 / 摄影语法锚点
只控制“这个项目通常怎样把画面组织成镜头”：
- 景别与人物/环境面积关系的总体倾向；
- Profile / OTS / Wide / Interior Ensemble等构图语法；
- 前景/中景/后景层次；
- 留白与负空间习惯；
- 深度组织与环境信息密度；
- 实际光源在构图中的引导方式；
- 雨、玻璃、反射、窗框、门框等环境元素作为画面层次的使用方法。

不控制：
- 某一Shot必须复制参考图的精确相机坐标；
- 具体角色站位与动作；
- Storyboard已经锁定的Camera / Composition；
- 场景几何与对象身份；
- 最终清晰度。

**冲突时：Storyboard / Director Shot Contract > Cinematic Shot Style Anchor。** 镜头画风只能提供摄影语法，不得覆盖当前Shot的具体导演决定。

## 2｜Style Board有两种来源模式

### GENERATIVE_STYLE_BOARD｜从零建立
适用于项目尚无稳定正式资产时。可以用匿名人物、泛化环境、材质样本生成Style Board，避免错误把未批准角色/地点写进Canon。

### APPROVED_STYLE_EVIDENCE_BOARD｜批准资产证据板
适用于已经存在成熟APPROVED人物、场景、道具或镜头时。优先从真实Approved资产中挑选代表样本组成Evidence Board：
- 可以出现项目真实角色与真实场景；
- 它们在这张板上的职责仍然只是Style Evidence；
- 下游不得从Evidence Board迁移具体身份、服装、空间几何或道具结构；
- 若当前任务已经有更直接Character / Environment / Prop Authority，Evidence Board不得抢权。

**已有成熟正式资产时，Approved Evidence通常优先于重新生成匿名Style Board。** 不为了“格式标准”把已经验证的视觉效果重新抽卡一遍。


## 2.5｜VERIFIED_VISUAL_STYLE_FINGERPRINT（已验证视觉风格指纹）
为了让纯文本/低视觉能力执行端能够继承**真实已落地的项目风格**，Approved Style Evidence或一组稳定Approved正式图可以由多模态Verifier提炼一个文字Sidecar：

```text
VERIFIED_VISUAL_STYLE_FINGERPRINT
Source Asset IDs / Versions：...
Scope：PROJECT / SCENE_FAMILY / CHARACTER_FAMILY / OTHER
Render Family：...
Linework：...
Color Blocking / Shading：...
Face / Skin / Hair：<适用时>
Material Rendering：...
Palette / Contrast / Value：...
Atmosphere：...
Common Drift Risks：...
Verified By：WEB_EXTERNAL_VERIFIER / USER_VISUAL_APPROVAL
Status：CURRENT / STALE
```

规则：
- 它不是新画风设计，只是把真实Approved视觉证据翻译成可复用文字；
- 它不能覆盖`project_style_dna.md`，两者冲突时先复核Source是否已过时；
- 它不能在平台支持真实视觉Reference时成为“省掉绑定”的借口；视觉绑定与Style Projection仍按任务需要执行；
- Source版本、Render Style Authority或关键Scene视觉体系变化时Fingerprint立即STALE；
- Blind模型不得自行从文件名/Prompt推导Fingerprint，必须来自外部视觉分析或用户明确视觉结论。
- `Palette / Contrast / Value`记录的是综合色组织方法，不把某一Scene的具体蓝/红/暖灯色相烤进项目级Render Style；具体色相与当前光色仍由Color Authority控制。

## 3｜版式比例不是Style Authority

Render Style Board、Cinematic Shot Style Board、Color Card的整张版式比例由内容组织决定：
- 4:3、16:9、竖版信息卡、自由拼板均可；
- 版式比例不是项目画风的一部分；
- 下游Character Master / Environment Master / Storyboard / Video不得继承Style Board的画布比例。

`Asset Aspect Ratio Authority`永远由当前资产类型决定。

## 4｜Reference Input Role

当Style图真正上传模型时：
- Render Style Anchor → `CONTROL_IMAGE / CONTROL_CROP / TEXT_CONTROL`，Role=`RENDER_STYLE_GRAMMAR`；
- Cinematic Shot Style Anchor → `CONTROL_IMAGE / CONTROL_CROP / TEXT_CONTROL`，Role=`CINEMATIC_SHOT_GRAMMAR`。

**Current Visual-First：** 已有Approved Visual Style Evidence且平台能够接收相应图片Reference时，优先让视觉证据承担Render Grammar；`DIRECT_STYLE_BOARD = UNKNOWN`本身不构成降级理由。文字只补当前镜头特有的剩余约束。只有目标模型明确不支持视觉Reference、槽位必须让给更高优先级身份/空间Authority，或项目实测已出现Sample Content Bleed / Layout Literalization时，才降级Crop / Applied Reference / TEXT_CONTROL。不能因为Project Style DNA“理论上可文字描述”就默认放弃已经存在的Approved视觉画风证据。

### Composite Evidence Board Routing｜复合证据板路由
Approved Style Evidence Board若包含真实角色、车辆、场景或道具，**不是无条件整板上传，也不是无条件禁用整板**：
- 平台可接收相应图片Reference、`DIRECT_STYLE_BOARD != VERIFIED_FAIL`、未观察到Sample Content Bleed / Layout Literalization，且整板关系本身有控制价值 → `CONTROL_IMAGE / DIRECT_BIND`；能力`UNKNOWN`允许先按Direct Bind试用，不预防性降级；
- 只需要某一种画法/摄影语法，或项目实测出现Sample Content Bleed → 裁对应Evidence为`CONTROL_CROP`；
- 视觉输入不可用或Reference槽位不足 → 才用`TEXT_CONTROL`补足；
- 板内出现的任何人物/地点/道具默认`ZERO IDENTITY / ZERO GEOMETRY AUTHORITY`，除非另有独立Approved Authority明确授权。

**Style Evidence的“真实项目来源”提高的是可信度，不提高它对当前对象身份/结构的权限。**

不得写：
- “以这张Style图为最终清晰度/完成质量标准”；
- “完全复制这张图的构图”；
- “按这张图的人物长相生成新人物”。

## 5｜Task-Bound选择

### Stage 02 Director Breakdown
- **Cinematic Shot Grammar必须在重要Scene的Shot设计前可用**，因为它属于导演语言输入，不应等到Stage 04才第一次读取；
- Stage 02只读取项目级景别倾向、Depth、Negative Space、OTS/Profile/Wide等摄影语法，不复制Style Board具体构图；
- Stage 02由`director_architecture_engine.md`建立真正的Shot-Specific Camera / Blocking / Distance / Axis / Cut Motivation；
- 若Cinematic Shot Style与当前戏剧/空间需要冲突，当前Director Shot Contract优先。

### Stage 03对象资产
- Render Style Grammar：通常有效；
- Cinematic Shot Grammar：通常不需要，除非该资产本身是Shot-bound视觉锚图；
- 不为了“电影感”给Character Master塞镜头构图参考。

### Stage 04 Storyboard
- Render Style Grammar：只保证分镜图与项目绘画系统一致；
- Cinematic Shot Grammar：可以影响镜头语言倾向；
- 具体Shot / Camera / Blocking仍由Director Breakdown + Storyboard决定。

### Stage 05 Video
- Render Style Grammar：维持绘画方式；
- Cinematic Shot Grammar：只提供项目级构图倾向，或强化Stage 02已经锁定且Stage 04已证明的摄影关系；**不得在Stage 05补发新的Entry/Landing Camera Geometry、Lens Family、Focus Behavior、DOF、Stabilization或Camera Motion。**
- 当前Shot若缺少上述Shot-specific摄影字段，回Stage 02最小Patch；不能拿Style Anchor填空。已锁Director Contract / Approved Previs永远优先。

## 6｜Style Authority Hard Gate

输出正式图片/Storyboard/Video Prompt前检查：
- [ ] Render Style与Cinematic Shot Style职责已分开；
- [ ] Cinematic Shot Style没有覆盖Director/Previs具体机位/站位，也没有在Stage 05新增Lens / Focus / DOF / Stabilization / Camera Motion；
- [ ] Style Board比例没有污染当前资产比例；
- [ ] Evidence Board中的具体人物/地点没有被迁移成当前对象身份；
- [ ] 复合Evidence Board已按Capability与真实风险选择DIRECT_BIND / CONTROL_IMAGE / CONTROL_CROP / TEXT_CONTROL；无失败证据时不因“整板”类别自动降级，发生Sample Bleed/Layout Literalization时才升级Crop/Applied；
- [ ] Style图没有承担对象高清细节/清晰度Authority；
- [ ] 已有成熟Approved Evidence时，没有无意义重新生成匿名Style Board。

失败：`VISUAL_STYLE_AUTHORITY_FAIL`，回到Reference Resolver / Style Authority重新裁决。
