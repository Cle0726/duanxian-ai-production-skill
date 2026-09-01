# Web Multimodal QC Upload Budget（网页版多模态QC上传预算）

> **Method Authority｜用途：** 统一管理《断弦之歌》把图片资产、Storyboard与Video Reference Pack交给网页版多模态模型做独立QC时的实际上传数量、拆包、动态编号和跨批合并。
>
> **V4.3配置Owner：** 当前上传上限与水印Profile由`adapters/web_qc/platform_profile.yaml`唯一拥有。本文件负责Evidence Packing方法；当前Profile值为10张图片。任何Batch Production、Reference Resolver、Candidate Triage或Web QC Handoff都必须读取Profile，不得在其他总控文件维护第二份硬编码。
>
> 这不是新的Stage，也不是生成模型的Reference槽位规则。它只控制**网页版多模态QC提交**。

## 1｜Hard Cap（硬上限）

### 1.1 图片数量

- `WEB_MULTIMODAL_IMAGE_CAP = platform_profile.image_upload_cap`（当前Profile=10）
- 每一个独立Web QC提交中，**实际图片附件总数 ≤ 10**。
- Render/Cinematic Style Board、Color Card、Character Master、Environment Master、Prop/Weapon Master、Previous Ending Frame、Storyboard、Candidate都属于图片，只要实际上传就各占1个图片槽。
- 同一张Authority图如果在B01和B02都需要，它在两个批次中分别各占1个槽。
- 文字Prompt、TEXT-ONLY Authority不占图片槽。

### 1.2 Video QC

Stage 05 Web Video QC按：

`1个当前Video Take + 最多10张参考图片`

组织。这里的10张是**图片参考上限**；Video Take本身不是图片，不占这10张图片预算。

若实际网页UI还存在额外的总附件/文件限制，以用户当前UI能成功上传为准，继续向更小批次拆分；不得为了凑满10张强塞。

### 1.3 Asset / Storyboard QC

Stage 03图片资产QC和Stage 04 Storyboard QC没有Video Take时（包括按Image Candidate Strategy计划生成的2–4张同组候选）：

`Candidates + Authorities + Comparison References ≤ 10 images per batch`

任何一次Copy Prompt里引用的`@图N`都必须和**本批实际上传的≤10张图片**一一对应。

---

## 2｜Web QC Pack不等于Generation Reference Pack

生成模型的Reference Pack和网页版QC Evidence Pack是两个不同对象：

- `GENERATION_REFERENCE_PACK`：为了生成当前资产/Storyboard/Video而选择；受生成模型当前任务输入能力约束。
- `WEB_QC_EVIDENCE_PACK`：为了让网页版验证端判断结果；受本文件`10-image hard cap`约束。

不能因为生成时用了12张图，就直接要求网页版一次上传12张图。

Web QC Evidence Pack必须重新做Evidence Packing：保住当前检查维度真正需要的Authority；其余转TEXT-ONLY、分批验证或在不同Pass中重复Candidate后再合并结论。

---

## 3｜Atomic QC Group（不可拆比较组）

默认把一个正式验证对象视为一个`Atomic QC Group`：

### 图片资产
一个Asset的：
- 当前全部需要二选一/多选一的Candidate；
- 当前P0身份/结构Authority；
- 当前必须对照的Style / Character / Prop / Environment Authority。

### Storyboard
一个Storyboard/Segment的：
- 当前候选Storyboard；
- 必须的Character / Environment / Prop / Previous Ending Frame；
- 必要Render / Cinematic Style Authority。

### Video
一个Video Take的：
- Video Take；
- 当前验证维度需要的Reference Images。

**优先不把同一资产的候选1和候选2拆到不同批次。** 候选比较必须同屏/同批可见时，Candidate组视为不可拆。

如果一个Atomic QC Group连删除CONDITIONAL并TEXT-ONLY化之后仍然超过10张图片，才允许执行`Multi-Pass QC`，而不是随机丢P0 Authority。

---

## 4｜Evidence Priority（证据优先级）

**Evidence Priority由本轮QC Scope决定，不由Reference资产类型永久固定。** 先读取 `qc_scope_freeze_ledger.md`；当前真正开放的验证问题所需Authority自动升级为P0，已经FROZEN_PASS且Revision未触及的维度不为“保险”额外占槽。

装包顺序：

### P0 EVIDENCE｜必须保住
1. 当前待验证的完整Candidate / Storyboard Comparison Group；
2. 当前`OPEN_REVISION_TARGET / REOPENED`直接需要的Authority；
3. Identity开放时：人物/道具身份Master；
4. Structure开放时：武器/道具结构、Environment几何Authority；
5. Continuity开放时：Previous Ending Frame / Approved Storyboard；
6. Render Style / Material开放时：Render Style Anchor /必要材质Authority；Cinematic Shot Style仅在摄影语法开放时加入；
7. 当前核验项明确需要的专项Authority（例如TE眼部、WP武器）。

### P1 EVIDENCE｜容量允许再加
- 当前Scope没有直接要求的综合色/Lighting辅助图；
- 次级细节资产；
- 非当前关键人物；
- 仅用于佐证、不是当前Verdict必要条件的Reference。

例如：若本轮明确只复检Render Style / Material，则Render Style Anchor从通常P1**升级为P0**；若Identity/Structure已FROZEN_PASS且本轮Patch未触及，则对应Authority可不上传。

### TEXT-ONLY FALLBACK｜可文字化
- Project Style DNA；
- Negative / 非照片非3D规则；
- 已稳定的综合色约束；
- Music Identity文字规则；
- Render Quality原则；
- 不需要像素级对照的剧情/机制说明。

`TEXT-ONLY`不是降低Authority，只是不占10张图片槽。

---

## 5｜Automatic Batch Packing（自动拆包算法）

当用户要一次检查多个资产/Storyboard时，Skill自动执行：

1. 先识别可共享的Common Authorities，例如同一个Render Style Anchor；
2. 为每个验证对象建立Atomic QC Group；
3. 计算每组图片数；
4. 按`≤10`把完整Atomic Group装进`B01 / B02 / B03...`；
5. Common Authority在每个需要它的Batch中重复上传并重新计数；
6. 不为了“多塞一个资产”把一个候选组拆开；
7. 每个Batch重新执行Dynamic Numbering，从`@图1`开始连续编号；
8. 每个Batch生成独立、完整、可直接复制的`WEB_QC_UPLOAD_LIST` + `WEB_QC_COPY_PROMPT`；
9. 用户把各批网页版结果贴回后，本地Skill自动合并，不要求用户人工汇总。

### Batch Packing目标

不是追求每批刚好10张，而是：

**最少网页往返 + 不超过10张 + 不破坏同组比较 + 不丢P0证据。**

---

## 6｜Multi-Pass QC（单个对象仍超10张时）

如果**一个**资产/Storyboard/Video所需P0 Evidence本身超过10张，不允许随机删除核心图。改为多个检查Pass：

### PASS-A｜Identity / Structure / Continuity
优先：
- **完整Candidate Comparison Group**；
- Character / Prop / Environment结构Authority；
- Previous Ending Frame / Storyboard等连续性Authority。

### PASS-B｜Style / Material / Detail
重复上传**同一个完整Candidate Comparison Group**，再加入：
- Render / Cinematic Style Board；
- TE / TH / TC / WP专项；
- Color / Lighting；
- 其他必须的细节Authority。

必要时再有PASS-C，但应先尝试删除重复/CONDITIONAL证据。

每个Pass必须绑定相同的`Object ID + Version + Candidate IDs`；文件Hash可取时同时记录SHA-256。不得PASS-A看CAND01、PASS-B却换成另一张未声明候选。

最终本地合并：

`WEB_QC_MERGED_RESULT = PASS-A + PASS-B (+ PASS-C)`

任何一个Pass在本轮开放/重开的P0维度出现Fail，则整体不能PASS。

---

## 7｜Dynamic Numbering Across Batches

`@图N`永远只在**当前Batch**有效：

- B01：`@图1...@图8`
- B02：重新从`@图1...`开始

禁止写：

`B02继续上传@图9～@图16`

因为网页版验证端的实际上传顺序才是编号Authority。

每个Copy Prompt开头必须写清：

`QC Batch: B01 / B02 / ...`

以及：

`只使用本批实际上传的@图1～@图N进行判断；不要引用前一批的@图编号。`

为了降低跨批图片串线，**优先每个Batch使用独立网页验证会话**；若用户选择同一会话继续，也必须在Prompt中声明忽略前批图片编号，只验证当前Batch。

---

## 8｜Stage 03｜WEB_ASSET_QC_BATCH

当Stage 03有多资产候选需要网页版独立验证时：

输出：

```text
WEB_ASSET_QC_BATCH
Batch: B01
Image Count: 7 / 10

【上传顺序｜示例，实际由本批Resolver动态编号】
1. @图1｜<本轮OPEN Scope真正需要的Authority>
2. @图2｜Asset A CAND01
3. @图3｜Asset A CAND02
4. @图4｜Asset A专项Authority
5. @图5｜Asset B CAND01
6. @图6｜Asset B CAND02
7. @图7｜Asset B专项Authority

> 示例中的@图1不是固定Style职责；若本轮不需要Style，它可以是Identity / Structure / Continuity等其他P0 Evidence。
```

Copy Prompt要求网页版按资产分别返回`WEB_ASSET_QC_RESULT`，不得把两个资产混成一个总Verdict。具体标准模板与导入协议读取 `web_asset_storyboard_qc_handoff.md`；Revision Recheck同时读取 `qc_scope_freeze_ledger.md`。

### Stage 03用户可见交付契约

只要当前流程决定把Asset Candidate交给网页版Verifier，Skill必须直接展示：

1. `WEB_ASSET_QC_BATCH_PLAN`：B01/B02各包含哪些资产；
2. 每批`Image Count: N / 10`；
3. 每批完整上传顺序；
4. 每批一个完整可复制`WEB_ASSET_QC_COPY_PROMPT`。

不得只说“分两批上传”却让用户自己决定哪张放哪批。

Asset Copy Prompt至少动态包含：Project / Batch / 本批@图映射 / 每个Asset的P0与P1核验要求 / Authority职责 / 候选比较要求 / 固定返回格式。

如果B01已经10张，下一资产自动进入B02；不允许输出“再加@图11”。

---

## 9｜Stage 04｜WEB_STORYBOARD_QC_BATCH

Storyboard批量QC同样遵守10图硬上限。

优先保持：
- 当前Storyboard Candidate；
- 当前人物Master；
- Environment Master；
- CONTINUITY_ENTRY的Previous Ending Frame；
- 关键Prop/Weapon；
- 必要Render / Cinematic Style Authority。

多个Segment若共享Authority，可在同一Batch中复用1次Common Authority；但一旦拆到下一Batch，共享Authority若仍需要必须重新上传。

网页版返回每个Segment独立的`WEB_STORYBOARD_QC_RESULT`。具体标准模板与导入协议读取 `web_asset_storyboard_qc_handoff.md`；Revision Recheck同时读取 `qc_scope_freeze_ledger.md`。

### Stage 04用户可见交付契约

使用网页版Storyboard Verifier时，Skill必须直接展示`WEB_STORYBOARD_QC_BATCH_PLAN`、每批`N / 10`图片计数、实际上传顺序和完整Copy Prompt。Copy Prompt至少写明：Storyboard候选、人物/场景/道具/Ending Frame各自Authority、Panel/Shot/Continuity/Action Physics/Performance核验维度与标准返回格式。用户不负责自行删Reference或重新编号。

---

## 10｜Stage 05｜WEB_VIDEO_QC_BATCH

正常情况下，一个Video Take对应一个Web QC Batch：

```text
Video: <SEGMENT_ID>_TAKE01.mp4
Reference Images: N / 10
QC Batch: B01
```

若Video Reference Evidence ≤10：一次完成。

若 >10：
- 先由Evidence Priority删CONDITIONAL / TEXT-ONLY化；
- 仍>10时执行Multi-Pass Video QC；
- 同一个Video Take可在PASS-A / PASS-B重复上传，分别验证不同Authority维度；
- 本地合并报告，不让网页版跨批猜测。

---

## 11｜Cost & Friction Guard（一人制片操作成本保护）

虽然网页版QC不一定直接产生视频生成费，但用户的上传、整理、复制、回贴同样是生产成本。

所以：
- 不因为“上限是10”就每次硬凑10张；
- 不上传本批不需要的旧资产；
- 同批能共享的Authority只上传1次；
- 只有跨Batch才重复必要Common Authority；
- Skill必须自动给出每批上传顺序，不要求用户自己算槽位；
- 用户一次上传结果很多时，Skill主动拆好B01/B02并分别给Copy Prompt。

---

## 12｜QC Gate

任何准备交给网页版多模态验证的包，在交付前必须检查：

- `IMAGE_COUNT <= 10`；
- 所有实际上传图片都有明确职责；
- 所有P0核验项有证据；
- Candidate比较组未被无理由拆散；
- @图编号与本批实际上传顺序一致；
- 跨批时Batch ID明确并重新从@图1编号；
- Copy Prompt不引用本批没有上传的图片；
- 多Pass结果有本地Merge计划。

任一失败：`WEB_QC_PACKET_INVALID`，不得直接交付用户上传。
