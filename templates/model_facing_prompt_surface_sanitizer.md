# Model-Facing Prompt Surface Sanitizer（模型侧提示词表面净化器）｜Current Authority

> **用途：** Stage 03图片、Stage 04 Previs/Storyboard、Stage 05 Final Video、Revision/Inpaint在真正交给生成模型前的最后一跳。
>
> **最高原则：** `THE MODEL SEES ONLY EXECUTABLE CONTENT.` 生成模型只看它能执行的画面、动作、镜头、声音与当前任务必须调用的真实`@资产`Mention；它不看项目管理、资产台账、文件系统、上传说明、方法名、Gate、版本号或“我为什么这样绑图”的解释。**真实@资产Mention属于执行内容，不得在净化时被误删。**

## 1｜真正的 Copy Surface

`FINAL_COPY_SURFACE` = 用户实际复制/粘贴给图片或视频生成模型的那一块文字。

默认交付规则：
1. **用户可以先看到一份结构化“镜头执行分析”，随后只给一个真正可复制的Prompt代码块。分析区不属于Copy Surface，不得混入代码块。**
2. Internal Control Packet默认不打印给用户；留在Workspace/运行时。
3. Executor Binding Packet只有在“用户必须手动完成绑定且当前没有真实Native Token”时才单独显示，而且**绝不与Prompt放在同一代码块**。
4. 不打印输入清单、本地映射标签或文件元数据；但当前Host的Prompt Surface=`NAMED_ASSET_MENTION_REQUIRED`时，UI中已存在资产仍必须在正文显式`@资产`调用。
5. 每个当前任务强绑定Reference的**@Mention注释本身**只保留真实已验证Token + 简洁职责句；同一资产不重复@。这一规则只约束Token旁边的绑定说明，**不得用于缩短Final Video正文**。

> **Current Copy-Surface Rule：** 允许在Copy Surface外显示结构化`镜头执行分析`帮助用户审核导演执行；真正送给生成模型的仍只有一个FINAL_COPY_SURFACE。禁止把内部任务壳、Binding List、Registry、QC或隐藏推理混入分析或Prompt。

## 2｜正向白名单：Copy Surface只允许什么

### 2.1 IMAGE / ASSET
只允许：
- 实际画幅/比例/必要输出形式；
- 画面里必须出现的主体、环境、结构、姿态、状态；
- 构图、视角、空间关系；
- 画风、材质、综合色、光源；
- 可见连续性/身份保持；
- 当前任务真正必要的排除项；
- 当前任务强绑定资产的已验证`@资产`Mention（Current Generation Profile下必需）。

### 2.2 PREVIS / STORYBOARD
只允许：
- 实际需要的单帧/关键帧/分镜幅数与画幅；
- 每幅可见构图、人物状态、动作接触、空间关系与新增信息；
- 连续性、画风、综合色；
- 必要限制；
- 当前任务强绑定资产的已验证`@资产`Mention（Current Generation Profile下必需）。

### 2.3 FINAL VIDEO
只允许模型可执行的详细控制，包括：
- 镜头目标与实际时长；
- 当前任务强绑定资产的已验证`@资产`Mention；
- 人物外观/服装的必要一致性确认；
- Scene空间、Prop状态、构图、景别；
- Camera Geometry / Lens / Focus / Stabilization / Camera Timeline；
- t=0起始状态；
- 分段时间轴、动作、表演、视线、肢体占用与物理反馈；
- 环境动态；
- 光影、综合色与Shot Lighting变化；
- 对白、声音及必要Prosody/Visible Breath；
- Ending State / Continuity Landing；
- 可见成片质量、环境融合、当前任务真实必要限制。

**Sanitizer不得把“详细”误判为“元数据”。** 只要一句话能改变Seedance的可见运动、表演、摄影、空间、声音或连续性结果，就属于合法执行内容。

### 2.4 REVISION / INPAINT
只允许：
- 改哪里、改成什么；
- 哪些可见内容必须保持；
- 必要的局部结构/接触/综合色要求；
- 当前任务强绑定资产的已验证`@资产`Mention（Current Generation Profile下必需）。

**白名单之外的内容默认先删，再判断是否需要被转译。**

## 3｜Hard Forbidden：任何Prompt类型都不得进入Copy Surface

### 3.1 文件与资产元数据
- 文件名、扩展名、绝对/相对本地路径、下载目录、归档目录；
- Asset ID / Version / Registry Handle / Archive Path；
- 内部命名片段，如`*_MASTER_* / *_CROP_* / *_ASSEMBLY_* / *_AUTHORITY_* / *_PROFILE_*`；
- 任何仅用于找文件的编号、磁盘路径或版本后缀。

### 3.2 操作者任务壳 / 输入清单
以下属于**给人操作**，不是给生成模型执行，全部禁止进入Copy Surface：
- 任务说明壳、生成操作说明或给操作者看的步骤标题；
- 输入素材清单、本地图片映射标签或上传顺序说明；
- 输出文件管理、保存位置、下载目录或归档说明；
- 本地路径、文件名、资产名、版本号；
- 用任意伪编号标签冒充尚未建立的原生Reference Token。

> 若平台没有真实Token，**不得用本地映射标签假装绑定已经成立。** 绑定问题留给Executor层处理。

### 3.3 流水线行政语言
- Reference Responsibilities / 参考职责 / Reuse Scan / Binding List；
- MUST_BIND / CONDITIONAL / TEXT_ONLY / Approved / Authority / Resolver / Registry；
- Executor Input Map / Semantic Role / Why Now / Most Direct；
- Stage / Gate / Hard Fail / Failure Code / QC Packet / Capsule / Method；
- Platform Profile / Execution Mapping / Risk Driver / Proof Question / Deliverable Component；
- “本图只锁定……不决定……”“由文字导演”“三参考职责分离”等解释系统如何工作的句子。

### 3.4 非执行型内部标题
Copy Surface不得出现仅服务生产管理的标题，例如：
- Reference职责类标题；
- Existing Authority Scan类标题；
- Binding / Upload / Executor Map类标题；
- 输入/任务/输出/资产登记/QC审核等生产管理标题。

**允许的标题只应直接帮助模型理解执行内容**，例如“起始画面 / 镜头时间轴 / 对白与声音”。Stage 05默认是详细Master Prompt，可使用这些执行标题帮助模型理解时序；是否省标题不得成为压缩正文的理由。

## 4｜Reference的唯一合法模型侧表达

### 4.1 UI已经绑定
**当前Host Prompt Surface覆盖旧规则：UI已绑定不等于正文可以省略强绑定资产。** 当`adapters/generation/platform_profile.yaml`规定`NAMED_ASSET_MENTION_REQUIRED`时，MUST_BIND / DIRECT_BIND / CONTINUITY_ENTRY等资产仍必须以真实原生`@资产`进入正文；只有平台Profile明确`ui_binding_without_prompt_mention_allowed=true`时才允许UI-only。

```text
保持当前已绑定参考中的主体、空间、材质、综合色与构图关系稳定。
```

### 4.2 Current Generation Profile：强绑定资产必须原生@Mention
只有真实Token/资产显示名已由Reference Runtime / Asset Registry / Target Adapter建立时才可写：

```text
<REAL_NATIVE_TOKEN> 保持已绑定Reference中当前任务所需的可见关系。
```

禁止：
- Token后接文件名；
- Token后接Asset ID/Version；
- Token后接“这是Environment Authority/MUST_BIND”等职责解释；
- Token对应Reference没有合法Capability/Role Route，或沿用已知失败的Literalization路线。

### 4.3 Token尚未建立或强绑定资产未Mention
若任务必须视觉绑定但当前没有真实Token，或Reference Runtime要求的强绑定资产未出现在Prompt：
- Copy Surface状态 = `WITHHELD_PENDING_NATIVE_BINDING`；
- 在代码块外给最短操作者提示，告诉用户需要绑定哪些**人类可理解资源类别**；
- 不伪造Native Token，不写伪输入编号标签，不把本地路径塞进Prompt。

## 5｜Visual Control Reference输入

Final Video在Native Token emission前必须先读取`visual_reference_routing.md`：
- 综合色Card/Crop → 按Capability Route直绑 / Dedicated Channel；`ROLE_SEPARATION=VERIFIED_FAIL`时优先无生成式Color-Only Crop / Dedicated Channel；仅在已观察Literalization、Direct Fail、已证明槽位冲突、用户明确要求，或Role Separation失败且无安全非生成式隔离时转Applied Reference；
- Style Board → Verified Direct / Clean Crop / Applied Reference按Capability选择；
- Storyboard整Sheet/宫格 → Verified Board Direct / Panel Multi-reference / Key Panel / Clean Panel；
- 某一路线已经发生实际泄漏时，不能只加Negative后沿用同一路线。

## 6｜Mandatory Surface Rewrite Pass

候选Prompt必须按顺序执行：
1. `COPY SURFACE EXTRACTION`：只提取白名单执行内容；
2. `FILE/PATH STRIP`：清文件名、扩展名、路径、下载/归档信息；
3. `TASK SHELL STRIP`：清任务说明、输入映射、输出管理和保存位置等操作者壳；
4. `ADMIN STRIP`：清Reference职责、Reuse、Binding、MUST_BIND、Authority、Stage/Gate/Method等；
5. `ROLE DISSOLVE`：把仍有视觉/声音价值的控制结果改写成直接执行句；
6. `NATIVE TOKEN VALIDATION`：仅保留真实Token，并核对所有强绑定资产均已@Mention；
7. `REFERENCE ROUTE CHECK`：所有Video视觉Token必须有Content/Role + Capability Route；
8. `CONSTRAINT STATE CONFIRM`：仅确认上游Hard Conflict=0；Sanitizer不得自行裁决互斥事实；
9. `SEMANTIC DEDUP`：同一事实只保留最佳一次；
10. `SURFACE LINT`：机械扫描下列Forbidden Pattern；
11. `EGRESS REWRITE`：交给`prompt_egress_gate.md`按Image/Video出站语法重写；
12. `SINGLE COPY BLOCK`：最终给生成模型的正文只保留一块Copy Surface；用户可见的结构化镜头执行分析允许位于代码块外。

## 7｜Mechanical Surface Lint（强制，不靠“理解”）

交付前必须生成内部`SURFACE_LINT_REPORT`，以下计数全部为0才算PASS：

- `WINDOWS_PATH_COUNT`：盘符绝对路径样式；
- `POSIX_LOCAL_PATH_COUNT`：`/mnt/`、`/home/`、`/Users/`、临时目录等本地路径；
- `FILE_EXTENSION_COUNT`：`.png/.jpg/.jpeg/.webp/.mp4/.mov/.zip/.md/.txt`等文件后缀；
- `INTERNAL_ASSET_ID_COUNT`：项目内部全大写/下划线资产ID或Master/Crop/Assembly/Authority/Profile命名；
- `VERSION_TAG_COUNT`：资产版本后缀；
- `TASK_SHELL_COUNT`：任务说明、输入映射、输出管理、保存位置等操作者壳；
- `PIPELINE_TERM_COUNT`：MUST_BIND/Authority/Resolver/Registry/Stage/Gate/Capsule/Executor Input Map等；
- `ADMIN_HEADING_COUNT`：Reference职责、Reuse、Binding、资产登记、审核标准等；
- `SELF_CHECK_COUNT`：内部检查/生成后确认/验收说明；
- `QC_CONTRACT_BACKFLOW_COUNT`：QC验收要求、PASS条件、验收清单等QC Contract回流；
- `PROMPT_PREFIX_DUPLICATION_COUNT`：重复的生成调用前缀；
- `DURATION_ECHO_COUNT`：无执行价值的重复时长尾缀；
- `META_NEGATIVE_PROMPT_COUNT`：若平台支持negative prompt请添加等meta说明；
- `STYLE_METHOD_NAME_COUNT`：Style Projection等内部方法名；
- `UNVERIFIED_NATIVE_TOKEN_COUNT`：没有真实绑定记录却出现的@Token；
- `MISSING_REQUIRED_ASSET_MENTION_COUNT`：Reference Runtime要求强绑定但Copy Surface没有对应@资产Mention；
- `UNBOUND_ASSET_MENTION_COUNT`：Prompt出现@Mention但本次Reference Runtime无法回查；
- `TOKEN_OVERANNOTATION_COUNT`：Token后附资产名、版本、文件名、职责长说明；
- `UNROUTED_CONTROL_REFERENCE_TOKEN_COUNT`：Video Token对应Color/Style/Storyboard Reference但没有合法Capability/Role Route，或沿用已知失败路线。

任一`>0`：`SURFACE_SANITIZATION=FAIL`，禁止交付。

> **重要：** 仅写一句“不要出现文件名/路径”不算执行Lint。必须实际检查候选Copy Surface。

## 8｜Prompt长度与说明性语言

Sanitizer同时删除对模型没有执行价值的自我说明：
- “基于以下输入……”如果Reference已经通过UI/Token绑定，则删除；
- “这张图用于后续……”删除；
- “Controller会归档……”删除；
- “请不要重新设计……”若可改写为具体可见保持项，则改写；不能产生可见执行差异的说明直接删除。

目标不是“越短越好”，而是**每句话都能改变生成结果或防止一个真实失败。** 对Stage 05 Seedance任务，按`video_prompt_template.md`执行`PROMPT_LENGTH_CEILING = NONE`；Sanitizer禁止以“已有@图”或“字数过长”为理由删掉时间轴、动作、摄影机、表演、物理、光影综合色、声音或Ending State。

## 9｜Revision / Inpaint

合法模型侧表达优先是：
```text
只修改指定区域：修正手指数量、关节连接和握持关系；区域外人物身份、背景、构图、光线与综合色保持不变。
```

不要写：
- Edit Target的内部文件名；
- Patch Authority的ID；
- 本地蒙版路径；
- “这是Revision v002”。

## 10｜QC例外

Web QC Copy Prompt是**Verifier证据映射**，不是Generation Prompt。它可以按本批实际上传顺序用动态@图号指认Evidence，但该例外不得回流到Stage 03/04/05生成Prompt。


## Current｜Style Projection Preservation Rule
Surface Sanitizer删除的是**内部Style Authority说明**，不是已经改写成直接画面语言的Style Projection。以下属于白名单执行内容，不能因含“画风/风格”而删掉：画种、线稿、色块/阴影方法、人物/材质渲染、综合色与对比组织、项目气质。Sanitization后若只剩抽象Style Tag，标`STYLE_PROJECTION_SANITIZER_OVERSTRIP`并回Compiler。

## 11｜Hard Fail

- `MODEL_FACING_METADATA_LEAK`
- `LOCAL_PATH_LEAK`
- `FILE_NAME_LEAK`
- `TASK_SHELL_LEAK`
- `REFERENCE_ADMIN_TEXT_LEAK`
- `PIPELINE_JARGON_LEAK`
- `INTERNAL_HEADING_LEAK`
- `NATIVE_TOKEN_OVERANNOTATION`
- `PSEUDO_NATIVE_REFERENCE_TOKEN`
- `UNROUTED_CONTROL_REFERENCE_TOKEN`
- `MODEL_FACING_ALLOWLIST_VIOLATION`
- `SURFACE_LINT_NOT_RUN`
- `PROMPT_SURFACE_SANITIZATION_FAIL`

任一未解决 → 禁止交付，返回Compiler重编，不消耗生成额度。

## 12｜回归标准

### 场景资产 + Approved综合色卡
如果UI已经绑定场景参考与Approved综合色卡，Copy Surface只保留直接画面语言；综合色卡本身继续作为视觉Reference，不为了Prompt净化额外生成综合色应用图。示例：

```text
保持当前已绑定参考中的主体、空间、材质与构图关系。综合色与明度遵循已绑定的综合色参考，只取颜色关系，不复制控制图的版式。保持同一视觉绘制语言，输出单一连续画面。
```

### Final Video
同理：内部可以有完整Reference Pack与Binding Plan，但Copy Surface只保留真实镜头执行语言和必要真实Token。
