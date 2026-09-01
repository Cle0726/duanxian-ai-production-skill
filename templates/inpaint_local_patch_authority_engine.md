# Inpaint & Local Patch Authority Engine（局部重绘 / Inpaint 权限引擎）

> **用途：** 当APPROVED / QC候选图片只有局部错误，且用户要求“局部重绘、定点改、Mask修补、Inpaint、不要整张重生”时使用。图片候选策略中Revision / Inpaint属于I4：默认先1次定向编辑，不因为图片生成便宜就同时做多张Patch变体。
> **Prompt去重：** 局部修补Prompt交付前读取`prompt_semantic_deduplication_engine.md`。EDIT_TARGET / PATCH_DESIGN_AUTHORITY / Frozen Region各自只说明一次职责；不要把同一修改目标在“问题描述、修正要求、负面限制”三处重复。
>
> **Primary Rule：EDIT TARGET负责“哪里保持原样”，PATCH DESIGN AUTHORITY负责“局部要改成什么样”。二者不得混用。**

---

## 1｜五类Reference Role必须分开

### A. EDIT_TARGET / REVISION_SOURCE_IMAGE（编辑底图 / 真正待修改图）
- 这是**实际被修改的整张图片**；它可以是APPROVED Master，也可以是QC失败但值得局部修正的当前Candidate；
- 控制：Mask外原始像素、人物身份、原构图、原比例、原服装大结构、原光照/综合色、原空间关系；
- 它回答的是：**“到底在哪一张现有结果上改？”**。若QC说“修改候选A”，这里必须就是候选A，不能偷换成Parent Master。
- 它**不能自动回答**：局部究竟要改成什么新结构。

### B. PATCH_DESIGN_AUTHORITY（局部重绘图案 / 结构Authority）
- 当用户已经上传或项目已有明确的“正确局部设计图、局部结构参考、正确纹样/配件/零件/裂纹/武器端部”等时，必须作为单独Reference加入；
- 控制范围严格限制在Mask Region；
- 它回答的是：**“这个局部要改成什么样？”**
- 禁止把它的背景、构图、人物身份、综合色或无关结构复制到Base Master。

### C. STYLE_AUTHORITY（画风Authority）
- 只控制被修补区域的二维画法、线稿、材质表现方法；不承担清晰度、锐度、细节密度或最终完成质量Authority；
- 通常使用Render Style Anchor / Approved Style Evidence；综合色兼容另由当前Global/Scene/Shot Color Authority负责；
- 不控制Patch结构，不控制Base Master整体构图。

### D. IDENTITY_AUTHORITY（身份Authority）
- 只有Patch触及脸、发型大形、身体比例、关键服装身份结构、角色专属武器/道具身份时才加入；
- 若EDIT_TARGET本身已是清楚的APPROVED Character/Prop Master且Mask不碰身份核心，可不额外增加Identity图；
- Identity Authority不得扩权到Mask外重新设计。

### E. MASK_REGION / DEPENDENT_INTEGRATION_REGION / FROZEN_REGION（主修改区 / 物理整合边缘 / 冻结区）
- `MASK_REGION`：唯一允许发生**设计变化**的主区域；
- `DEPENDENT_INTEGRATION_REGION`：紧贴Mask的最小物理整合边缘，只允许因新结构必然产生的接触阴影、反光、遮挡边缘、接缝、局部材质连续性变化；不得借此扩大设计重绘；
- `FROZEN_REGION`：上述两区之外全部区域；必须保持Base Master原始内容不变；
- 若平台支持真实Mask，优先使用真实Mask；若只支持文字指令，则必须用明确空间描述锁定边界。

**Integration Fringe不是第二个自由Mask。** 例如把小零件换大后，允许修正紧邻投影，但不能顺便改背景、服装或整体光照。

---

## 1.1｜Edit Target Type Routing（编辑对象类型路由）

Local Patch不是默认Stage 03。先判断被编辑对象：

- `ASSET_MASTER`（Character / Environment / Prop / Weapon / Transformation）→ 回Stage 03 Asset QC；
- `STORYBOARD` → 回Stage 04 Storyboard QC，只复检受影响Panel / Continuity / Action / Performance；
- `VIDEO_FRAME_REFERENCE`（非正式Ending Frame的普通截图/辅助Reference）→ 只能作为辅助图，不自动升级为正式Continuity Authority；
- `APPROVED_ENDING_FRAME` → **禁止Inpaint后继续作为Previous Ending Frame Authority**；见下条。

### Approved Ending Frame Protection
Previous Ending Frame必须来自对应APPROVED VIDEO的真实稳定帧。若尾帧本身不好：
1. 优先在同一APPROVED VIDEO内选择另一个真实稳定时间点；
2. 若没有可用真实帧，返修Video / 重新批准Video；
3. **不得Inpaint / Photoshop / 生成一张理想尾帧，再冒充真实Video Ending Frame。**

编辑过的帧如确有创作用途，只能标记`EDITED VISUAL REFERENCE / NOT CONTINUITY AUTHORITY`。

---

## 2｜Reference Binding硬规则

### 2.0 Revision Source Binding（返修源图绑定）
只要用户/QC表达的是“在这张结果上修改”，当前失败/待修改Candidate就是`EDIT_TARGET / REVISION_SOURCE_IMAGE`且必须上传。Parent Canon Master若需要，只能作为Identity / Structure / Geography Support；**不得因为Parent更正式就取代Candidate成为底图。** 实际文件绑定保存在Executor Input Map，模型正文不写Asset ID/文件名。

若决定放弃Candidate、从Parent Master重新生成一张新图，任务必须明确改为`FRESH_REGEN`，不能继续称为“修改这张图”。

### 2.1 有“重绘图案参考”时
只要用户/项目提供了明确局部参考，内部Binding必须把编辑底图、局部设计证据与必要画风证据分开；**这些Role名称不进入Copy Surface**。

模型侧只保留直接编辑结果，例如：

```text
只修改已指定的局部区域，把目标结构修正为已绑定参考所示的形态、比例与图案；区域外的人物身份、构图、背景、光线、综合色和其他已正确细节保持不变。新旧边缘自然衔接，不新增重复零件、鬼影或无关改动。
```

具体哪一张输入承担哪个内部Role，由Executor Input Map / 平台原生输入槽位绑定；不得靠`@图N + 文件名`伪绑定。

**禁止：**
- 只@母图，却在文字里说“改成参考图案”，但没有真正上传/绑定该图案；
- 用EDIT_TARGET自身代替PATCH_DESIGN_AUTHORITY；
- 把PATCH_DESIGN_AUTHORITY当成整图Style Transfer来源；
- 因为Patch Reference更清晰，就让它覆盖人物脸、场景构图或综合色。

### 2.2 没有“重绘图案参考”时
若任务只是：
- 删除多余物；
- 补齐被遮挡/缺失的小区域；
- 修平孔洞；
- 修正简单手指/阴影/边缘；
- 文字可以唯一描述目标；

允许只有`EDIT_TARGET + TEXT PATCH SPEC`。

此时必须写清：
- Authorized Change；
- Patch Region；
- Frozen Region；
- 期望局部完成态。

### 2.3 用户给了局部参考但未明确角色
Resolver默认判断：
- 若参考图明显是“正确局部造型/图案/零件”，绑定为`PATCH_DESIGN_AUTHORITY`；
- 若参考图只是项目画风板，绑定为`STYLE_AUTHORITY`；
- 若参考图是同一角色/道具完整Approved Master，且用于保持身份，绑定为`IDENTITY_AUTHORITY`；
- 若无法唯一判断但局部设计差异会产生P0结构变化，才询问；否则按最窄职责自动绑定。

### 2.4 Multi-Region / Repeated Instance Patch（多区域 / 重复实例同步修补）
如果同一对象的同一结构在一张Sheet中重复出现（正视/侧视/特写/背视等），本次Authorized Change必须先建立`INSTANCE MAP`：

```text
INSTANCE-01｜Panel 1正视｜位置...
INSTANCE-02｜Panel 3侧视｜位置...
INSTANCE-03｜Panel 5特写｜位置...
```

- 同一结构修改默认同步作用于所有**可见且应一致**的实例；
- 不能只修最明显的一格，让其他视图保留旧结构；
- 若某一视图因角度确实不可见，标记`N/A`而不是凭空新增；
- 多实例可使用多个Mask，但所有Mask共享同一PATCH_DESIGN_AUTHORITY和结构约束；
- QC必须逐实例检查方向、数量、比例与位置关系。

---

## 3｜Patch Authority Priority（局部权限优先级）

### Mask内
1. 用户当前明确的Authorized Change；
2. PATCH_DESIGN_AUTHORITY；
3. IDENTITY_AUTHORITY（仅身份相关字段）；
4. STYLE_AUTHORITY（仅画法/材质字段）；
5. EDIT_TARGET用于保持周边连续性。

### Mask外
1. EDIT_TARGET / BASE MASTER为绝对Authority；
2. 其他参考全部无权改动。

**一句话：Mask内“按新设计修”，Mask外“按原图冻结”。**

---

## 4｜No Authority Bleed（禁止权限外溢）

Patch Prompt必须明确禁止：
- 改脸、年龄、发型、体型（除非Mask授权）；
- 改人物站位、姿势、镜头、裁切；
- 改服装其余裁片与配色；
- 改背景、环境几何、灯光方向；
- 改未授权道具数量/位置；
- 因Patch Reference构图不同而重构Base Master；
- 因局部材质参考更写实而把整图变真人/3D/PBR；
- “顺手美化”未授权区域。

---

## 5｜Patch Prompt标准结构

内部先完成Edit Target / Patch Design / Style / Identity / Mask权限判断，然后**只把可执行结果投影到Copy Surface**。禁止把内部Role表、Asset ID、文件名、路径、版本号、`【Task】/【EDIT TARGET】/【PATCH DESIGN AUTHORITY】`等任务壳复制给模型。

推荐模型侧骨架：

```text
仅编辑指定区域，不重新生成整张图。
把指定区域修改为：<唯一、具体的局部完成态>。
必要时同步修正紧邻边缘的接触阴影、反光、遮挡边缘与接缝，使新结构与原图透视、尺度、光向、线稿、材质和旧化程度自然一致。
区域外保持原图不变：人物身份、比例、姿势、构图、服装其他区域、背景、光线、综合色与已正确细节全部保持。
不新增未授权物体，不改变未授权区域，不产生重复零件、鬼影或接缝。
```

若平台必须在正文引用已绑定输入，只允许真实Native Token + 最短执行句；Token后不得附文件名、Asset ID、Version或内部Role。交付前必须经过`model_facing_prompt_surface_sanitizer.md`并使`SURFACE_LINT_REPORT`全部为0。
---

## 6｜同一对象的“局部Authority”类型

以下都可成为PATCH_DESIGN_AUTHORITY：
- Approved局部裁切图；
- 同一资产另一视图中已经确认的正确结构；
- 专项TE/TH/TC/WP/Prop Detail；
- 用户当前上传并明确说“按这个图案/结构重绘”的图片；
- 从Approved Master提取并批准的Detail Authority；
- 修订候选中仅用于某个已批准局部的Patch Source。

**但“它是同一对象”不等于“它可以控制整张图”。** Resolver必须把权限缩到实际Patch字段。

---

## 7｜Patch Provenance扩展记录

每次局部重绘必须记录：
- Base Master Asset ID / Version；
- EDIT_TARGET Reference；
- PATCH_DESIGN_AUTHORITY Reference（若有）；
- STYLE / IDENTITY Authority（若有）；
- Mask Region / Instance Map；
- Dependent Integration Region；
- Authorized Change；
- Frozen Regions；
- Composite / Inpaint Method；
- Result Version；
- QC Result；
- User Approval Status。

若没有Patch Design Authority，写：`PATCH_DESIGN_AUTHORITY = TEXT-ONLY`。

---

## 8｜QC Gate

Local Patch完成后，QC只重新审查：
1. Authorized Change是否正确完成；
2. Patch是否忠实继承PATCH_DESIGN_AUTHORITY；
3. Patch与Base Master的透视/光照/材质/线稿是否自然融合；
4. Dependent Integration Region是否只发生物理必然的阴影/反光/遮挡/接缝变化，没有扩大重绘；
5. Frozen Region是否发生任何P0/P1漂移；
6. 是否新增重复物、接缝、鬼影、错误数量；
7. 若是跨视图/重复实例同一结构，所有INSTANCE方向/比例/位置/数量是否一致。

**Frozen Region一旦发生P0/P1变化，Patch FAIL；Dependent Integration Region超出物理必然范围也FAIL；不能因为局部改对了就PASS。**

---

## 9｜Reference Budget兼容

局部修补时Reference Resolver优先顺序：
1. EDIT_TARGET / REVISION_SOURCE_IMAGE（MUST；QC失败返修时就是失败候选本身）；
2. PATCH_DESIGN_AUTHORITY（有明确局部参考时MUST）；
3. 身份相关且Mask触及身份核心时的IDENTITY_AUTHORITY（CONDITIONAL→MUST）；
4. STYLE_AUTHORITY（通常CONDITIONAL；项目Style DNA文字始终保留）；
5. 删除与Patch无关参考。

局部Inpaint不得因为“参考越多越保险”塞入整个Episode Asset Pack。

---

## 10｜与Personal Creator Cost Efficiency的关系

本文件是`Master Freeze + Local Patch`的执行Authority：
- `personal_creator_cost_efficiency_engine.md`决定**什么时候应该Patch而不是重生**；
- 本文件决定**Patch时到底@谁、各Reference控制什么、哪些区域冻结**；
- `reference_resolver.md`负责最终实际图片输入绑定；`execution_reference_semantics.md`负责把内部绑定投影成无文件名/无Raw Asset ID的Semantic Role；
- `checklists/qc_checklists.md`负责验收。
