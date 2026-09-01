# Asset Aspect Ratio Authority（图片资产画布比例权威）

> **用途：** Stage 03所有图片资产在写Generation Prompt前先确定画布比例。比例由**资产类型与用途**决定，不能从Style Board、Color Card、Storyboard、Video或最近一次任务继承。
>
> **核心修复：** 《断弦之歌》最终视频/Storyboard Panel是16:9，不代表人物母图也是16:9；Style Board / Color Card自身也不绑定固定比例。人物身份与造型类资产默认采用**9:16竖版**。

## 1｜P0原则：Aspect Ratio Is Asset-Type Authority

任何Stage 03 Prompt必须在正文前部明确写出：

`Canvas / Aspect Ratio：<ratio + orientation + purpose>`

若未写，视为Prompt不完整，不得交付生成。

**禁止比例继承：**
- Render / Cinematic Style Board比例由内容布局决定，只控制各自Style职责，不控制人物画布；
- Storyboard每格16:9，只控制最终镜头构图，不控制人物母图；
- Final Video 16:9，只控制成片，不控制Stage 03资产页；
- Previous Ending Frame、Scene Reference、Approved Character Master的原图比例，都不能自动覆盖当前资产类型的比例。

## 2｜Character Identity / Appearance Assets（人物身份与造型资产）

以下资产只要主体职责是“确认人物是谁 / 长什么样 / 穿什么 / 变身后完整人物结构”，**默认固定9:16竖向高分辨率画布**：

- `DV-01`｜Normal Character Master，2×2人物四视图；
- `DF-01`｜标准正脸；
- `DF-02`｜标准3/4脸；
- `EX-01`｜表情页，默认2×3六宫格；
- `HA-01`｜日常头发结构页；
- `TF-01`｜Transformation Turnaround，2×2变身四视图；
- `TH-01`｜变身头发结构页；
- `TC-01`｜变身礼服结构页。

### 2.1 Prompt Mandatory Phrase

人物母图/人物造型资产Prompt前段必须出现等价正向描述：

```text
9:16 vertical high-resolution character reference sheet,
portrait-oriented canvas
```

中文Prompt至少明确：

> **9:16竖向高分辨率人物资产页 / 人物母图画布。**

这不是建议，而是默认Production Lock。只有用户明确要求其他比例，或该资产在本规则第3节属于专项例外时才改变。

### 2.2 2×2并不等于横版

`DV-01 / TF-01`即使是2×2四格，**整张Sheet仍为9:16竖版**。四格内部根据职责分配脸部与全身空间：
- FRONT FACE / SIDE FACE可以使用较紧的头肩构图；
- FRONT BODY / BACK必须保证完整头顶到鞋底可读；
- 不得为了塞进横版16:9而把全身人物缩得过小、脚部裁切或让左右留白过多。

## 3｜Specialized Character-Related Assets（人物相关专项资产）

以下虽与角色有关，但主体不是“完整人物身份画布”，比例按任务原生结构决定，**不得反向污染人物母图比例**：

- `TE-01~TE-05` Eye Asset：眼部超近特写可用16:9横向或1:1；必须显式标注`EYE DETAIL ASSET`；
- `WP-01` Weapon Master：按道具/武器几何决定，通常16:9横向；
- `PR-01` Character-linked Prop：按Prop Authority决定；
- `AD-01` Signature Adornment Detail：按装饰几何决定，通常1:1或4:3局部高清，不继承人物四视图比例；
- `FMH-01 / Functional Minor Human Asset`：默认9:16竖向高清单人物范围参考；只锁Scoped Appearance，不烘焙最终16:9场景站位。若人物与场景位置关系本身是核心风险，**先保留FMH母图，再额外走`SHOT_ASSEMBLY_ASSET`**，不要把FMH本身做成横版情境图；
- `TS-01` Transformation Timeline：按时序格数量自动决定整页比例；其中单个用于最终视频的关键帧仍按镜头职责16:9；
- `TM-01 / FX-01`：按材质/特效拆解任务决定，不自动9:16，也不自动16:9。
- `PERFORMANCE_EXPRESSION_SUPPORT`：默认4:5或1:1单人物近中景，按表情可读性决定；不继承Final Video比例。
- `PERFORMANCE_ACTION_POSE_SUPPORT / PERFORMANCE_CONTACT_POSE_SUPPORT`：默认4:5或9:16单帧，保证全身/接触关系可读；多人Contact可按关系改为横向，但不机械16:9。
- `NARRATIVE_FX_REFERENCE`：按FX单一状态可读性决定；`NARRATIVE_FX_STATE_SHEET`可使用多格拆解比例，但默认不作为Final Video Direct Reference。

若一个任务同时要求“完整人物 + 武器”，但主要目的是人物身份/造型建档，仍以**9:16人物画布**为主；武器只做比例展示，不能为了横向放武器把人物母图改成16:9。

## 4｜Non-Character Asset Defaults（非人物资产默认）

- `RENDER STYLE BOARD / CINEMATIC SHOT STYLE BOARD`：**版式比例由证据布局决定**，4:3 / 16:9 / 竖版信息板均可；比例不是Style Authority；
- `GLOBAL COLOR CARD / SCENE COLOR EXTENSION CARD`：按信息密度与排版决定，可横可竖；不得把色卡比例传播给场景/视频；
- `Environment Canon Master`：默认16:9横向；Derived Coverage不得因为“Master Set完整”机械补视图，必须按`shot_coverage_asset_derivation.md`由真实Shot需要触发；
- `SHOT_ASSEMBLY_ASSET`：默认**16:9横向高清单帧资产图**，因为职责是稳定最终视频画面中的人物-场景-道具关系；这个16:9来自Assembly资产用途本身，**不是继承Storyboard宫格**。若特殊构图确有理由可改变比例，但必须在Assembly Contract中说明；
- `Storyboard Panel`：每格最终16:9；整张Storyboard Sheet比例由宫格布局自动决定；
- `Final Video`：16:9，除非用户明确指定其他成片比例；
- `Prop / Weapon`：优先按结构可读性决定；长横向道具通常16:9，竖长道具可用9:16，不机械套视频比例。

## 5｜Reference Authority Isolation（参考比例隔离）

Reference只继承它被授权的职责：
- Render / Cinematic Style Board → 各自Style职责；**不继承其4:3 / 16:9 / 竖版画布**；
- Global / Scene Color Card → Color only；**不继承其版式比例**；
- Character Master → Identity / Outfit / Proportion；若当前任务是新的9:16人物资产，按本Authority重排画布，不把旧图比例当身份；
- Environment / Storyboard / Ending Frame → Space / Composition / Continuity only；不能把16:9带进Character Master Prompt。

推荐在人物Prompt中显式写：

> 使用Render Style reference，仅迁移二维绘画语言与表现方法；**不继承该参考图的画布比例/版式，也不把该板自身的像素细节当人物资产标准。本任务输出严格9:16竖向人物资产页。**

## 6｜Stage 03 Preflight（生成前比例检查）

交付任何Stage 03 Prompt前检查：
1. Asset Type是什么？
2. 本任务主要职责是人物身份/造型，还是眼睛/武器/特效/场景？
3. `Canvas / Aspect Ratio`是否显式写入Prompt？
4. 人物身份/造型类是否为9:16？
5. 是否错误继承Style Board / Color Card / Storyboard / Video的画布比例？
6. 若当前是`FMH`，是否默认9:16范围人物Appearance Reference，并避免把最终场景站位烘焙进FMH？
7. 若当前是`SHOT_ASSEMBLY_ASSET`，是否默认16:9高清单帧且比例来自Assembly用途，而不是Storyboard继承？
8. 若使用例外比例，是否能从资产职责解释，而不是因为“项目常用16:9”？

任一失败：`ASPECT RATIO AUTHORITY FAIL`，先修Prompt，不进入候选生成。

## 7｜QC

人物身份/造型类候选必须检查：
- 整张画布是否真实9:16竖版；
- 2×2人物页有没有被模型做成16:9横版；
- 全身格是否完整头顶到鞋底，比例足够大；
- 脸部格是否仍有足够像素看清身份；
- Style Board / Color Card版式有没有污染人物Asset Layout；
- 若专项资产采用16:9/1:1，是否确实属于第3节例外，而非人物母图误用。


## V4.5.2｜Video Conditioning / Clean Storyboard
- `CLEAN_STORYBOARD_PANEL`：每Panel采用最终成片比例，当前项目默认16:9；
- `VIDEO_FIRST_FRAME / VIDEO_TARGET_FRAME / VIDEO_LAST_FRAME / VIDEO_KEY_POSE / VIDEO_CONTACT_FRAME / VIDEO_CUT_EXIT_FRAME / VIDEO_CUT_ENTRY_FRAME`：必须与对应Video Unit最终画幅一致，当前项目默认16:9；
- Topology / Floor Plan等Planning Diagram不承担成片画幅Authority，可按可读性选择横/竖布局。
