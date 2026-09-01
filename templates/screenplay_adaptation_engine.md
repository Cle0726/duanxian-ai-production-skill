# Screenplay Adaptation Engine｜Stage 01B 小说→影视剧本改编

> **用途：** 把Stage 01A的源文本材料改编为“演员、场景、动作、对白、声音可以执行”的影视剧本草稿。它负责**戏剧化与屏幕化**，但不拥有镜头、摄影、分镜或资产设计权。

## 0｜最高边界
`ADAPT THE STORY FOR SCREEN → DO NOT DIRECT THE CAMERA`

Stage 01B可以改变**表达方式与Scene组织**，不能偷偷改变Locked Canon：
- 可以压缩重复信息；
- 可以把文学心理转成可表演行为、沉默、对白、声音或Subtext；
- 可以把连续同地点/同时间、同一戏剧任务的碎片合并；
- 可以把跨地点/跨时间/戏剧任务明显变化的长段拆Scene；
- 可以口语化/压缩普通对白；
- **不能**无依据新增关键事件、改变人物核心动机、改写世界规则、提前/延后关键Reveal导致剧情意义变化、删除必须保留的Payoff。

## 0.5｜User-provided Final Screenplay Pass-through
若`Source Mode = USER_PROVIDED_FINAL_SCREENPLAY`且用户已明确称其为最终/批准剧本：
- 01B不主动重写Scene结构、对白或事件；
- 只做`PASS_THROUGH_NORMALIZATION`：统一Scene ID/Slugline/Action-Dialogue-Sound结构、标记Entry/Exit Story State，并把发现的Canon/因果问题交01C QC；
- 如果必须改变内容才能消除冲突，停止Pass-through并显式请求Story层裁决，不能把“格式整理”伪装成改编。

## 1｜Adaptation Operations
每一处非直译改编使用下列操作之一并记录Source Anchor：
- `KEEP`：保留；
- `COMPRESS`：压缩重复/说明；
- `MERGE`：合并同一戏剧任务的材料；
- `SPLIT_SCENE`：因时间/地点/戏剧任务变化拆Scene；
- `EXTERNALIZE_INTERNAL`：把心理内容转为可表演行为/沉默/可辨识选择；
- `VISUALIZE`：把说明转成剧中可见事实或行为；
- `AURALIZE`：必要时转成剧情声音/声音缺失；
- `DIALOGUE_ADAPT`：口语化、压缩或将必要信息转为对白；
- `PRESERVE_AS_SUBTEXT`：不强行说出口，保留为表演Subtext；
- `RELOCATE`：仅在不改变Reveal/因果意义时移动信息；
- `DELETE_REDUNDANT`：删除真正重复且无Setup/Payoff/Character功能的材料。

`DELETE / RELOCATE / MERGE / SPLIT`只要触及关键Canon、Reveal、关系转折或Payoff，必须显式证明意义未改变；否则`ADAPTATION_CANON_CONFLICT`。

## 2｜Scene Split / Merge Grammar
正式Scene边界优先依据：
1. 时间连续性；
2. 地点连续性；
3. 当前Scene Dramatic Objective；
4. Obstacle / Tactic / Relationship Turn是否形成新的戏剧单元；
5. 信息Reveal是否需要独立进入/退出状态。

禁止：
- 每个小说段落=一个Scene；
- 每句对白=一个Beat；
- 为后续剪辑方便提前按Shot切Scene；
- 为适配AI视频时长把自然Scene切碎。

## 3｜把“不可见文学信息”变成可演信息
对`INTERNAL_THOUGHT / NARRATION / DESCRIPTIVE_PROSE`逐条裁决：
- 能由行为/选择表达 → `EXTERNALIZE_INTERNAL / VISUALIZE`；
- 必须由语言承载且人物确有说话动机 → `DIALOGUE_ADAPT`；
- 是人物内在驱动力但不应被说出 → `PRESERVE_AS_SUBTEXT`；
- 是世界/剧情必须知道但当前无法安全外化 → 保留为`DIRECTOR_CONTEXT_ONLY`，不得假装观众已经知道；
- 纯文学修辞且不承载剧情/人物/氛围功能 → 可`DELETE_REDUNDANT`。

如果为了“可拍”而捏造新的重大行动或对白意义，标`SCREENPLAY_EXTERNALIZATION_OVERREACH`。

## 4｜Dialogue Adaptation
对白必须：
- 保留必须锁定的关键台词/信息；
- 符合人物当前Objective / Relationship / Knowledge；
- 允许停顿、打断、未说完和Subtext，但不写镜头；
- 避免把本可由行为理解的信息全部口头解释；
- 不为了缩时长让自然语言失真；
- 不把小说叙述直接塞成角色说明台词。

## 5｜Episode Runtime只作为宏观密度约束
本项目单集目标为**15–18分钟**。Stage 01B可以据此检查整集戏剧密度，但：
- 不在此阶段分配Shot秒数；
- 不为达到分钟数Padding；
- 不静默删除Locked Story Facts；
- 若源内容无法在目标时长内合理改编，标`SCREENPLAY_RUNTIME_DENSITY_CONFLICT`，交由用户/Story层裁决，而不是把问题推给Stage 02强行压缩。

## 6｜输出：SCREENPLAY ADAPTATION DRAFT
每个Scene至少包含：
```text
SCENE ID:
INT./EXT. + LOCATION + TIME:
Scene Dramatic Purpose:
Characters Present:
Objective / Obstacle / Turn:

ACTION:
可见、可表演、按因果顺序的动作。

DIALOGUE:
人物名：对白

SOUND / SILENCE（剧情相关时）:

PERFORMANCE SUBTEXT（必要时，非观众直接信息）:

ENTRY STATE:
EXIT / STORY STATE CHANGE:
```

另附内部`ADAPTATION DECISION LEDGER`：
```text
Source Anchor | Operation | Adapted Result | Why | Canon Preserved? | Reveal Preserved?
```

## 7｜Director Authority Firewall
Stage 01B/剧本正文不得出现当前Shot级：
- 景别、Lens、Camera Height/Angle/View；
- Pan/Tilt/Dolly/Zoom/Handheld/Focus；
- CUT / Match Cut / Shot Number；
- 4/6/9格Storyboard指令；
- 画面左/右/前景/中景等具体摄影构图（除非它本身是剧情事实，如“他堵在门口”）；
- Reference / Asset / Prompt / Platform操作。

命中则`SCREENPLAY_DIRECTOR_AUTHORITY_BLEED`，删除导演化内容后再锁剧本。

## 8｜Stage 01B Hard Gates
以下任一未解决，不得进入01C：
- `ADAPTATION_CANON_CONFLICT`
- `SCREENPLAY_EXTERNALIZATION_OVERREACH`
- `SCREENPLAY_SCENE_STRUCTURE_FAIL`
- `SCREENPLAY_EXPOSITION_OVERLOAD`
- `SCREENPLAY_RUNTIME_DENSITY_CONFLICT`
- `SCREENPLAY_DIRECTOR_AUTHORITY_BLEED`

通过后记录：`SCREENPLAY_ADAPTATION_DRAFT_READY = PASS`。
