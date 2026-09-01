# Style Authority Projection Gate（风格权威投影）｜Current Authority

> **最高原则：** `VISUAL STYLE EVIDENCE FIRST; TEXT ONLY FILLS THE GAP.`
>
> **Current Rule：** 已绑定可靠Approved视觉Style Evidence时，Reference仍是主要Style Authority，但Stage 05不得因此压缩掉当前镜头真正需要的绘画语言、人物/环境融合、材质、光影与综合色执行。可以避免逐条复读完整Project Render Core，但“视觉已绑定”不等于“文字只许一句”。

## 1｜Style Source Hierarchy
1. 同一对象/同一Scene Approved Parent或Revision Source；
2. 同一Scene/同一视觉家族Approved正式图；
3. Approved Render Style Reference / Style Board；
4. `VERIFIED_VISUAL_STYLE_FINGERPRINT`；
5. Project Style DNA。

实际Approved视觉证据回答“项目现在真正长什么样”；Style DNA回答允许范围。冲突时`STYLE_FINGERPRINT_DNA_CONFLICT`，不自动平均。

## 2｜STYLE PROJECTION CARD（内部）

```text
Visual Style Evidence Binding: BOUND / NOT_AVAILABLE / PLATFORM_UNSUPPORTED
Evidence Type: PARENT / SCENE_IMAGE / STYLE_REFERENCE / STYLE_BOARD / NONE
Text Style Detail Level: MINIMAL / FULL
Render Family: ...
Linework/Shading: ...
Human Rendering: ... <有人物时>
Material Rendering: ...
Palette/Contrast Organization: ...
Drift Risks: ...
Status: PASS / FAIL
```

## 3｜MINIMAL模式：视觉Reference已经锁风格

当`Visual Style Evidence Binding = BOUND`且Reference Content/Role验证通过：
- Final Video Prompt不机械抄写整套Project Style DNA，但必须保留当前Shot真正影响生成结果的绘制语言、人物/环境统一渲染、材质和防照片/3D漂移描述；
- 对Seedance详细Prompt允许多句直接画面语言，不再限制为“只保留1句”；
- 如果综合色另有Color Reference，Style段避免把综合色Authority改写成第二套综合色；但`video_prompt_template.md`仍要求在光影综合色段写当前Shot具体光线/综合色执行；
- 如果人物身份已有Character/FMH Base Authority，不重新设计人物；Assembly/Previs只继承身份并补当前镜头关系/姿态，同时保留必要的外观/服装一致性确认。

视觉证据是主要Style Owner；文字是执行补强。两者互补，不以“短”作为质量目标。

## 4｜FULL模式：没有可用视觉风格证据

只有`NOT_AVAILABLE / PLATFORM_UNSUPPORTED`时，才需要把Project Render Core写成可执行语言。至少覆盖：
- 二维绘画/渲染家族；
- 线稿 + 色块/柔和绘画阴影；
- 有人物时的人脸/皮肤/头发表现；
- 环境材质的二维概括；
- 对比/明度/色彩组织；
- 禁止明显照片/3D/PBR漂移。

项目基础核心仍为：带动漫影响的二维叙事插画、细而克制的手绘结构线、受控色块与柔和绘画阴影、人物/道具/环境同一绘画系统。Scene具体色相由Color Authority负责，不烤进全局Style。

## 5｜Style Board直接绑定

Style Board是否直传由`visual_reference_routing.md`的Capability/Risk路由决定。只要平台可接收相应图片Reference、`DIRECT_STYLE_BOARD != VERIFIED_FAIL`且没有已观察Sample Content Bleed / Layout Literalization，就优先让Approved Style Board直接承担Render Style字段；能力`UNKNOWN`本身不触发降级。已观察示例内容串入/版式直译、`ROLE_SEPARATION=VERIFIED_FAIL`、已证明槽位冲突或用户明确要求时可以改变Direct路线；其中Role Separation失败优先Clean Crop / Dedicated Style Channel，只有不存在安全非生成式隔离时才允许生成式Applied Reference。


## 6｜Fail

- `STYLE_AUTHORITY_PROJECTION_MISS`
- `STYLE_EVIDENCE_BINDING_GAP`
- `STYLE_ROLE_SCOPE_VIOLATION`
- `STYLE_FINGERPRINT_DNA_CONFLICT`
- `STYLE_TAG_ONLY_FAIL`：**仅在Text是唯一Style Control且文字又只有抽象Tag时成立。**
