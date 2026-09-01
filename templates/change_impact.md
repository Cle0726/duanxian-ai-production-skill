# Change Impact（变更影响追踪）

> **用途：** 当一个已使用的正式人物/场景/道具资产换版本或发生批准变更时，只找出真正受影响的下游内容，避免“改一张母图 → 整集全部重做”。

## 核心原则

**Change does not mean invalidate everything.** 变更后先查依赖，再按画面是否实际可见、是否影响剧情/连续性决定返工范围。

Change Impact不负责擅自批准新资产。只有用户/现有批准规则确认的新版本，才成为下游正式依据。

## 触发条件

### Asset Authority变化
- APPROVED人物母图被新APPROVED版本替换；
- 场景母图几何/固定结构发生正式修改；
- 道具结构、比例或状态定义修改；
- 某个State Variant被替代；
- 正式资产被标记DEPRECATED；
- Approved Production Support Reference的Parent Authority发生变化，导致其Interaction/State证据可能失真。

### Storyboard / Continuity Authority变化
- 已被下游Video Prompt引用的APPROVED Storyboard换版本或局部Patch后重新批准；
- 已生成Additional Video Conditioning Keyframe所依赖的Approved Storyboard版本改变；
- CONTINUITY_ENTRY使用的Approved Previous Ending Frame改变真实时间点/版本；
- Continuity Snapshot出现正式更正。

### Visual Style / Color Authority变化
- Render Style Authority / Approved Style Evidence发生正式版本变化；
- Cinematic Shot Style Authority发生正式版本变化；
- Global Color DNA / Global Color Card发生正式变化；
- Scene Color Extension Spec / Card发生正式变化；
- 持续性Lighting Variant Reference发生正式变化。

### Music / Performance Authority变化
- 已批准Music Identity / Musical Motion Grammar发生正式版本变化；
- 影响Stage 04/05动作时间结构的Visual Beat Map发生变化；
- Approved TE-03的Primary Eye Signature / Secondary Graphic / Iris Architecture / Periocular Emblem / Formation Sequence / Cross-Core Echo发生正式变更，或Musical Eye Motif Registry中的Reserved Signature被替换。

**只要Authority本身已被下游Snapshot引用，正式换版就触发Dependency Scan；不是只有Stage 03图片资产才触发Change Impact。**

## 依赖扫描范围

按现有项目记录查：

1. Asset Registry；
2. Scene Pack；
3. `Reference Pack Snapshot（参考图包快照）`历史记录：实际资产ID + 版本 + 职责；
4. Episode Workspace；
5. Approved Storyboards；
6. Final Video Prompt / VIDEO_RUNTIME_CORE与Prompt Version；
7. Approved Videos；
8. Previous Ending Frame / Continuity Snapshot；
9. Visual Style / Global Color DNA / Scene Color Extension / Lighting Authority Snapshot；
10. Production Support Reference / Video Conditioning Snapshot；
11. Visual Beat Map / Stage 06 Music Sync Handoff；
12. 尚未进入最终成片的后期段落。


## 依赖数据要求

Change Impact不能只凭“这个Scene里出现过某角色”来猜依赖。若Reference Pack Snapshot同时记录了Approved Archive Path，应优先用Asset ID + Version + Archive Path定位历史文件。优先读取每个Segment被冻结的 `Storyboard Reference Pack Snapshot` 与 `Video Reference Pack Snapshot`。只有Snapshot明确记录使用了旧资产版本，才进入进一步可见性判断。

如果旧内容没有Snapshot，标记为 `REVIEW` 并人工/视觉检查一次；不要因为历史数据缺失就直接把整集标成STALE。

## Dependency Status（依赖状态）

这是下游内容的依赖状态，不替代资产本身的 `WIP / CURRENT / APPROVED / DEPRECATED`：

- `VALID`：变化与该下游无关，可继续使用；
- `REVIEW`：变化可能可见，需要检查，但不自动重做；
- `STALE`：明确依赖旧定义，继续使用会造成错误，需要返工或替换。

## 影响判断

### 例1｜人物围巾结构修改
- 近景清楚看到围巾 → `STALE` 或 `REVIEW`；
- 远景只看到人物轮廓 → 多数可 `VALID`；
- 该镜头人物根本没戴/没显示围巾 → `VALID`。

### 例2｜场景门的位置修改
- 镜头构图里明确看到并依赖这扇门 → `STALE`；
- 镜头在完全相反方向、门不可见 → `VALID`；
- 只是远处模糊背景 → `REVIEW`。

### 例3｜道具尺寸改变
- 有人物持握/交互 → 高概率 `STALE`；
- 道具只在极远背景出现且不可辨认 → `REVIEW / VALID`。

### 例4｜Approved Storyboard局部重绘后换v002
- 旧FINAL VIDEO PROMPT已经引用Storyboard v001但尚未生成视频 → `STALE / RECOMPILE`，只重编受影响Shot/动作块；
- Video已经APPROVED且画面实际正确 → 不因Storyboard文档换版自动重做，除非新Storyboard代表Canon/连续性事实也被正式改写；
- 后续Segment引用该Storyboard Exit State → 先检查是否受影响。

### 例5｜Previous Ending Frame时间点改变
- 下一个CONTINUITY_ENTRY Storyboard/Video Prompt引用旧尾帧 → `STALE / CONTINUITY RECHECK`；
- CUT_ENTRY / SCENE_OPENING没有精确尾帧依赖 → 多数`VALID`。

### 例6｜Scene Color Extension改变
- 只改变当前Scene综合色，但对象结构/Storyboard不变 → 已生成但未执行的Storyboard/Video Prompt通常`STALE / RECOMPILE COLOR BLOCK`；
- 已APPROVED视频综合色实际仍符合新Authority → `REVIEW`，不因色卡文档换版自动重做；
- 其他Scene没有引用该Extension → `VALID`；
- Global Color DNA改变时只扫描真正继承该字段且视觉上受影响的下游，不机械全季重做。

### 例7｜Cinematic Shot Style改变
- 当前Storyboard已经锁定具体Camera且画面正确 → 不反向重写Storyboard；新Style Authority只影响未来未锁镜头；
- 尚未锁定Storyboard的Shot grammar明确依赖旧Authority → `STALE / RECOMPILE STORYBOARD GRAMMAR`。

### 例8｜Music Identity / Visual Beat Map改变
- 尚未生成的战斗Video Prompt依赖旧Musical Motion Grammar → `STALE / RECOMPILE MUSIC-MOTION BLOCK`；
- 已批准Video动作不变，但Stage 06尚未配乐 → 更新Music Sync Handoff即可，不重做画面；
- 已批准Video的Protected Sync Point本身被Canon改写 → `REVIEW`，由导演决定是否必须返工。

### 例9｜Production Support / Video Conditioning Frame变化
- Parent Character/Prop/Environment Authority换版，Support图中可见字段被影响 → `STALE / REBUILD SUPPORT`；
- Parent变化不可见于Support负责字段 → `REVIEW / VALID`；
- Approved Storyboard换版后，旧Video Conditioning Frame仍绑定旧构图/Blocking → `STALE / REBUILD CONDITIONING`；
- Video已经APPROVED且实际画面仍正确 → 不因Support/Conditioning文档换版自动重做，仍按实际画面判断。


### 例10｜TE-03 Musical Eye Canon改变
- MCU / CU / ECU Storyboard或尚未生成Video引用旧TE-03，且旧Primary Eye Signature清楚可读 → `STALE / RECOMPILE EYE REFERENCE`；
- 远景眼部不可辨认，仅TF-01整体轮廓有效 → 多数`VALID`；
- 已APPROVED Video实际眼妆仍符合新Canon → `REVIEW`，不因文档换版机械重做；
- Registry Reserved Signature变化导致新旧角色发生撞型 → 只处理受影响角色与尚未生成的下游，不自动重做历史正确视频。

## Prompt / Runtime Stale处理

如果上游Authority变化发生在Video生成前：
- 已生成但未执行的Storyboard Prompt / Final Video Prompt不得继续冒充当前正式Prompt；
- 写`STALE_PROMPT`并调用Prompt Compiler做Minimum Necessary Recompile；
- 只替换受影响Authority、Shot、Color/Lighting、Music Motion、Entry Continuity块，禁止把正确部分全部重写。

如果Video已经APPROVED：
- 文档/模板升级本身不触发重做；
- 只有新的正式Canon/Authority使实际画面错误时才标REVIEW/STALE。

## 输出格式

```text
【Change Impact｜变更影响】
Changed Asset：CHR_CHARACTER_B_CURRENT
Old：v002
New：v003
Change：围巾结构调整，其余身份/服装不变

Affected:
- EPXX SXX SEG01 Storyboard｜REVIEW｜中景可见变更结构
- EPXX SXX SEG01 Video｜STALE｜近景明确显示被替换的结构
- EPXX SXX SEG02 Video｜VALID｜人物背面远景，结构不可辨认

Next Action：
只返工STALE项；REVIEW先检查，VALID保持不动。
```

## 与Episode Asset Freeze / Workspace关系

- 当前Episode处于`EPISODE ASSET FROZEN`时，正式资产版本变化先更新Episode Asset Pack Snapshot并重新检查Freeze完整性；
- 如果旧APPROVED资产被新APPROVED版本替代且本集需求仍被满足，不需要为了版本号变化把整集Freeze打破，但必须扫描真实依赖；
- 如果关键资产被DEPRECATED且没有有效APPROVED替代，或新增剧情事实证明本集缺一个正式Master，则标记`EPISODE ASSET FREEZE BROKEN`并回Stage 03补齐；
- `STALE`项写回Episode Workspace并生成最小Next Action；
- `REVIEW`只加入检查队列，不自动删除原Approved状态；
- `VALID`不进入返工队列；
- 若修改只影响未来尚未生成内容，只更新未来Reference Pack，不返工过去已正确内容。

## 禁止

- 一个局部版本变化就整集全部作废；
- 没检查画面可见性就批量重做；
- 把“资产版本更新”和“剧情必须回改”混为一谈；
- 为了新版本整洁而重做完全看不出差异的远景。
## Existing Project Migration特殊规则

旧版Skill迁移时，缺少Reference Pack Snapshot不等于STALE。此类历史内容先记`MIGRATION REVIEW`，只在后续生产依赖它、或发现P0/P1冲突时做一次最小复核。已明确APPROVED且画面正确的旧Video不因为模板升级、命名变化或新增字段而重做。`GRANDFATHERED`是迁移处置，不改变原Approval状态。


## Functional Minor Human Change Impact
- `SCOPED_CAST_BRIEF`的年龄段、服装轮廓、匿名边界或Scope发生会影响FMH可见字段的变化 → 对应FMH标`STALE / REBUILD FMH`；
- 只是具体Shot站位/Camera变化而Appearance不变 → FMH保持VALID，改Storyboard/Assembly；
- FMH后续升级为反复/命名人物 → 停止把FMH当长期Authority，建立正式Character Master并做Change Impact。

## Shot Assembly Change Impact
- Parent Character / Environment / Prop / Persistent State Authority发生会影响Assembly可见字段的变化 → 对应`SHOT_ASSEMBLY_ASSET`标`STALE / REBUILD ASSEMBLY`；
- 仅Storyboard构图变化不自动重做Stage 03 Assembly；若变化只影响具体Shot执行，重建受影响Stage 04 Video Conditioning Frame即可；
- Assembly重建后只复查真实依赖它的Storyboard / 未生成Video，不把已正确Approved Video自动作废。


## Personal Adornment Change Impact
- Rotation Pool / Current Active Adornment / Current LOOK Binding变化只影响真实使用该AC的Look / Scene /下游Reference，不扩大成全角色重做；
- 稳定Signature Adornment的形状/位置/材质发生正式变化时，受影响Character Master / Current Look / AD-01与清楚可读的Storyboard/Video Reference必须重新检查；
- 只改变当前Scene不可读的小型装饰，不自动重开全部Identity QC；
- 若装饰从身份配饰升级为剧情因果物件，必须转Prop Authority并执行下游Change Impact。


## V4 Director Intelligence Change Impact

以下变化会先影响Director Intelligence层，而不是直接改Storyboard/Prompt：
- Story/World State/Character Objective或用户明确导演要求改变，且会影响Audience State / Directorial Thesis / Reveal / Alignment → 当前`DIRECTOR_INTELLIGENCE_DECISION_CARD`标`REBUILD REQUIRED`；
- Director Judge改Selected Option或任一Non-Negotiable Invariant → 重跑受影响Sequence Arc，再向Detailed Shot Contract最小传播；
- 实质SYNTHESIS重做后必须完成Targeted Department Re-Critique；
- Approved Geography/Transformation真实设计若只要求非Invariant级Camera微调 → 走Director Spatial Patch；若迫使Invariant改变 → `DIRECTOR_INVARIANT_SPATIAL_CONFLICT`回Director Judge。

以下变化**默认不使导演卡失效**：
- Reference换图但职责/Canon不变；
- Scene Color Card换成等价Color Crop；
- Prompt语义去重/重编；
- Candidate选择变化但最终Approved视觉事实不变；
- 纯执行Slot/Take预算变化。

只有它们真实改变Scene Meaning / Geography / Character Truth / Director Invariant时才向上重开Director Intelligence。

## Director Architecture Change Impact

当Stage 02 Detailed Shot Contract或Stage 03 Reconciliation发生变化时，按字段最小传播：
- 只改Focus Owner / Critical Read：重算受影响Shot的Reference Coverage + Storyboard；
- 改Blocking / Distance / Depth：重算该Shot/Segment的Assembly/Support/Storyboard，必要时Camera Contract；
- 改Axis / Screen Direction：检查相邻Shot与连续Segment的Screen Side/Eyeline；
- 改Entry/Landing Camera Geometry / Lens Family / Focus Plan / Stabilization：只让受影响Shot的Previs/Video Runtime标STALE；静态Canon资产不自动失效；
- 改Camera Intent / Cut Motivation / Shot Relation：受影响Storyboard标STALE；未受影响资产不失效；
- 改Scene Spatial Requirement导致Environment Geography修改：执行`director_spatial_reconciliation_gate.md`并只传播到真实依赖该Zone/视线/路径的Shot。

不得因为一个Shot的Director Patch让整集所有资产/Storyboard自动STALE。

## Current｜Style Projection Change Impact
当Project Style DNA、Approved Render Style Evidence或作为Style Continuity Source的Parent视觉版本变化：
- 未执行的Stage 03/04/05 Prompt → `STALE / RECOMPILE STYLE PROJECTION`；
- Runtime Digest中的Style Projection Fingerprint → `STALE`；
- 已APPROVED视觉结果只在实际视觉不再符合新Authority时进入REVIEW/Revision，不因版本号机械重做。



## Current｜Stale Prompt Artifact Closure
当Workspace已有旧Prompt文件、旧Compiler版本正文、旧任务壳或“沿旧Prompt继续改”请求时，必须读取`stale_prompt_artifact_gate.md`。旧Prompt只恢复任务意图，不可作为当前文字母版；统一Fresh Recompile后再走Surface Sanitizer + Prompt Egress。


## Current｜Temporal Salvage Change Impact
已登记的Salvage Window绑定Source Take实际时间戳，不因新Take出现而自动失效。只有以下变化需要把相关Clip标`STALE`并复检：Story/World Canon改变、角色/服装/道具Authority变化造成实际画面不再合法、Continuity前后镜变化使Entry/Exit不可接、Director Invariant变化使原Cut不再允许、最终综合色/风格标准发生实质冲突。

Prompt模板升级本身不得自动作废真实可用片段。

## Current｜Director Perception Change Impact

Perception字段变化按Owner最小传播：
- `UNRESOLVED_STATE / RELATIONAL_PRESSURE`改变且会改变观看关系、Reveal或Blocking → 受影响Sequence的Director Perception + Editorial Plan重新验证；不自动重开Story Canon。
- `CAMERA_ETHICS / ATTENTION_FLOW / SHOT_SCALE_JUSTIFICATION / CAMERA_PLACEMENT_JUSTIFICATION`改变 → 只让受影响Formal Shot的Storyboard、Video Conditioning、Execution Plan与未执行Prompt标STALE。
- `VISUAL_FORCE_STACK / VISUAL_SALIENCE_BUDGET`改变但Camera/Blocking不变 → 优先重编受影响Storyboard/Prompt视觉主次，不重建无关资产。
- `INFORMATION_STATE / SEQUENCE_LOGIC / SHUFFLE_TEST`改变 → 重查相邻Edit Points与Sequence Grid；只传播到真正依赖该顺序的下游。
- `SHOT_GRAMMAR_HISTORY / CREATIVE_DRIFT_TELEMETRY`只是派生审美记忆；统计值变化本身**不得**使既有Approved Shot/Video变STALE。

如果Telemetry Warning促成新的导演选择，真正触发Change Impact的是被明确修改的Director/Shot字段，而不是Warning本身。
