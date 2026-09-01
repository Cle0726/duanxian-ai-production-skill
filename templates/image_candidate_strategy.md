# Image Candidate Strategy & Video Cost Split（图片候选策略与视频成本分流）

> **用途：** 统一《断弦之歌》静态图片候选数量、候选筛选、深度QC、Revision / Fresh Regen与Video Take预算。当前项目的现实成本结构是：**静态图片生成成本很低，Video Take成本很高**。因此图片阶段允许用多个平行候选换取更高确定性；视频阶段继续严格单Take优先。
>
> 核心原则：**Image generation is candidate-rich; video generation is take-constrained.｜图片宽松探索，视频严格节流。**

---

## 1｜两套预算绝不互相污染

### Static Image Policy
图片阶段的多候选用于降低设计、构图、材质、结构与下游Video失败风险。

### Video Policy
正式Video仍执行Adaptive Take Budget：
- 默认1 Take起步；
- T1/T2不预生成多Take；
- T3/T4也先1 Take，只有上游Gate通过且Failure Diagnosis证明主要剩余问题属于模型随机性时，才允许受限追加。

**图片默认2–4张候选，绝不构成“视频也应该2–4 Take”的理由。**

若图片候选策略被错误套到Video，或Video单Take节流规则反向把所有Stage 03图片强制压成单候选，标记：
`CANDIDATE_POLICY_BLEED_FAIL`

---

## 2｜Planned Image Candidate Count（计划图片候选数）

候选数是当前Job的生产元数据，**不写进模型Prompt正文**；生成平台若支持数量参数，由执行层设置。平台一次只能返回1张时，可分次执行同一Task Contract直到达到计划数。

### I1｜Design-Bearing Canon Master
适用：
- Character / Environment / Prop / Weapon正式Canon Master；
- 首次核心Transformation视觉资产；
- 正式Render Style / Cinematic Shot Style Evidence；
- 正式Global / Scene Color Card；
- 其他一旦批准会被大量下游复用的设计型静态Authority。

默认：
**2 Candidates**

高风险时：
**4 Candidates**

高风险条件包括：
- 本集/本季核心视觉资产；
- 复杂空间或复杂结构；
- 多人/多物体高一致性；
- 重要主道具、Boss空间、首次核心变身；
- 一旦锁错会造成大量Storyboard / Video返工。

### I2｜Derived Coverage / Functional Minor Human / Stage 03 Production Support / Shot Assembly Asset
适用：
- Environment / Prop Derived Coverage；
- 已有Approved Master基础上的必要视角、开合态、局部结构面；
- Stage 03 `PRODUCTION SUPPORT REFERENCE`：复杂Interaction / Contact / Transient State / Entity Action State等低成本高清风险消解图；
- `AD-01 Signature Adornment Detail`：已有Character Master基础上的个人标志装饰高清局部；
- `Functional Minor Human Asset / FMH`：基于Stage 02 `SCOPED_CAST_BRIEF`的范围人物Appearance Reference；
- Stage 03 `SHOT_ASSEMBLY_ASSET`：把已批准人物/场景/道具/状态组装成一张高清静态生产图，用于多人关系、人物进入场景、Montage情境或复杂空间中的稳定同框；
- 已锁设计后的正式静态扩展。

默认：
**2 Candidates**

这不是重新探索设计。Coverage候选必须回指同一Parent Master与Shot Coverage Contract；FMH候选必须回指同一`SCOPED_CAST_BRIEF + Scope`；Support候选必须回指同一Parent Authorities与Video Risk Contract；Assembly候选必须回指同一Parent Character/Environment/Prop Authorities与同一Assembly Brief，不能借机重设计Canon，也不能把Storyboard宫格直接清稿冒充资产。

### I3｜Stage 04 Previs Deliverable / Additional Video Conditioning Keyframe
普通单Component Previs（Hero Frame / Pair / Board / Map / Camera Path等）：
**1 Candidate**

复杂或高风险Previs Component可升级：
**2 Candidates**

`VIDEO_CONDITIONING_KEYFRAME`只在对应`APPROVED PREVIS SET`之后、且Video Risk Matrix/Stage 04判断确有必要时生成：
**默认2 Candidates**

它是同一`APPROVED PREVIS SET` + 同一Approved Authorities下的高清执行锚图，不是第二套Previs/Storyboard或新Canon。

复杂条件包括：
- HYBRID_PREVIS中的高风险Component；
- 多人Blocking；
- 战斗 / 追逐 / 强接触；
- 复杂空间反打；
- 多阶段动作；
- 复杂Camera / 轴线风险；
- 单张Storyboard错误会显著提高Video失败概率。

### I4｜Revision / Local Patch / Inpaint
默认：
**1 Edit Attempt**

因为目标已经明确，先修改真正的`EDIT_TARGET / REVISION_SOURCE_IMAGE`，不为了“保险”同时做多张局部修订。

若一次Revision仍失败：
1. 先Diagnosis；
2. 能继续最小Revision则再1次；
3. 不值得继续修则明确切换`FRESH_REGEN`。

### I5｜Fresh Regen
一旦明确放弃当前Candidate并切换`FRESH_REGEN`：
- 回到该资产类别原本的I1 / I2 / I3候选策略；
- 不再把废弃Candidate当生成Primary；
- 仍使用同一个最新Task Contract / Approved Authorities。

---

## 3｜Same Task Contract Rule（同任务合同平行候选）

多候选的意义是**比较执行质量，不是让Canon四处发散**。

同一Candidate Group必须共享：
- Output Target；
- Approved Identity / Structure / Geography；
- Wardrobe / Prop / Transformation Canon；
- Render / Cinematic Style Authority；
- Global / Scene Color Authority；
- Aspect Ratio；
- Shot Coverage Contract；
- 关键Restrictions。

允许变化：
- 随机渲染质量；
- 微小构图自然差异；
- 材质呈现细节；
- 表情/姿态在批准范围内的自然微差；
- 明确标记为`OPEN_DESIGN_RANGE`的尚未锁定设计字段。

禁止：
- 每张候选擅自换脸、换衣、换场景结构；
- 一张写实、一张3D、一张二次元作为“候选”；
- Coverage候选改变Parent Master设计；
- 候选之间使用不同Canon事实却仍放进同一Group。

若需要真正的A/B设计探索，必须显式建立`DESIGN_EXPLORATION_JOB`，不能伪装成普通Production Candidate Group。

---

## 4｜Candidate Triage → Deep QC（先筛后深检）

图片候选默认采用两层检查，不把每一张都做同等昂贵的完整深QC。

### Pass A｜Fast Triage
对同一Group所有候选快速检查P0/P1：
1. Identity / Structure；
2. Canon / Geography / Prop结构；
3. Reference职责是否正确；
4. 明显手部/肢体/对象错误；
   - 若为前景手、叙事手、持物手，必须按`HERO_HAND / FUNCTION_HAND`优先淘汰；
   - 不得以“整体最好看”为理由保留明显手错Primary；
5. 明显前景主脸/五官/关键接触错误；
   - 若为前景主脸、情绪脸或关键接触，必须按`HERO_FACE / FUNCTION_FACE`优先淘汰；
   - 不得以“氛围最好看”为理由保留明显主脸/接触错误Primary；
   - `HERO_FACE / HERO_HAND / FUNCTION_HAND / 关键叙事Contact`的一眼明显错误按Asset QC P0处理，直接REJECT；
6. Style / Color是否越权或严重漂移；
7. 是否存在一眼即可淘汰的生成故障。

输出：
- `PRIMARY QC CANDIDATE`
- `BACKUP CANDIDATE`（如有）
- `REJECTED`

### Pass B｜Deep QC
只对当前`PRIMARY QC CANDIDATE`执行完整Asset / Storyboard QC。

若Primary失败：
1. 先检查Backup是否**已经不存在同一个失败点**；
2. 若Backup明显解决 → Backup升级为Primary，进入Deep QC；
3. 若Backup也有同类问题 → 再决定Revision或Fresh Regen；
4. 不在已有可用Backup时立刻重新生成。

目的：
**用廉价图片候选减少无意义返修，但不降低正式QC标准。**

---

## 5｜Approval / Freeze边界

多候选不会产生多个正式Authority。

只有：
`Candidate Triage推荐 → Deep QC PASS → 用户明确批准`

的那一张，才能：
- 标记APPROVED；
- 进入Registry / Archive；
- 计入Episode Asset Freeze；
- 成为下游Reference Authority。

Backup仍是候选，不因为“第二名也不错”自动进入正式资产池。

---

## 6｜Stage 03 Batch Production

一个Asset Prompt Job可以带`Planned Image Candidate Count`：

```text
Asset ID：ENV-XX
Task：NEW_CANON_MASTER
Candidate Policy：I1
Planned Image Candidate Count：2
High Risk：NO
Candidate Group ID：ENV-XX_CG01
```

批量多个Asset时：
- “每批3–6个Prompt”指不同Asset Job数量；
- 每个Job仍按自己的候选数生成；
- 不把不同Asset的候选互相比；
- Canon Master尚未APPROVED时，不生成依赖它的Derived Coverage。

---

## 7｜Web QC 10图上限

图片候选丰富不取消`adapters/web_qc/platform_profile.yaml`声明的Web QC图片上限（当前Profile=10）。

原则：
- 同一Candidate Group尽量保持同批；
- 先保候选本体 + P0 Authority；
- 次要Authority转TEXT_CONTROL / CONTROL_CROP；
- 仍超限才Multi-Pass；
- 不为了塞Reference拆散一个必须同屏比较的候选组。

高风险4候选不是要求把所有Possible Reference都一起上传。

---

## 8｜Stage 04 Previs特殊规则

Previs的价值在于提前消除昂贵Video失败，因此：
- 先读取Stage 02 `Shot Storyboard Coverage Contract`；Mandatory Board必须生成，候选数与Panel数按Coverage/Risk决定，不固定4/6/9格；Supplemental Previs按需；
- 普通低风险Previs Component默认1张候选；多人/战斗/复杂Blocking / Camera Path等高风险Component可计划2张；
- `HYBRID_PREVIS`的Component数量与每个Component的Candidate数量是两回事，不能相乘后当作正式资产数；
- 两张候选必须服务同一个Director / Segment / Previs Component Contract；
- Candidate Triage优先比较该Component的Proof Question是否被证明，以及空间、轴线、Blocking、动作逻辑与Video可执行性，而不是单纯哪张更漂亮。

---

## 9｜Revision vs Fresh Regen

### Revision
当前Candidate大部分正确：
`Candidate本身 = EDIT_TARGET / REVISION_SOURCE_IMAGE`
→ 1次定向编辑
→ Revision QC

### Fresh Regen
当前Candidate整体不值得救：
`FRESH_REGEN`
→ 回到对应I1/I2/I3计划候选数
→ 重新建立Candidate Group
→ Triage

禁止：
“嘴上说改这张，但实际只@Master重新生成”。

---

## 10｜Stop / Continue规则

图片生成本身低成本，不采用Video的“第1张合格就必须立即停止所有候选生成”规则。

如果当前Job已经计划2或4张：
- 可以先完成该小组，再统一Triage；
- 不需要因为第1张看起来不错就取消同一小组剩余廉价候选；
- 但也不为了凑数量无限扩大Candidate Group。

正式停止点是：
**已经获得一个可批准的最佳候选，并且继续增加候选不会明显降低下游风险。**

视频仍保持：
**第1个Take通过立即STOP。**

---

## 11｜默认矩阵

| Task | 默认候选 |
|---|---:|
| Design-bearing Canon Master | 2 |
| High-risk Canon Master | 4 |
| Environment / Prop Derived Coverage | 2 |
| Functional Minor Human Asset / FMH | 2 |
| Stage 03 Production Support Reference | 2 |
| Stage 04普通Previs Component | 1 |
| Stage 04复杂/高风险Previs Component | 2 |
| Additional Video Conditioning Keyframe（需要时） | 2 |
| Revision / Inpaint | 1次编辑 |
| Fresh Regen | 回到原Task候选数 |
| Final Video | 1 Take起步 |

用户可以明确覆盖图片候选数量；Video额外Take仍必须服从Failure-before-Compute与Take Budget。

---

## 12｜最终原则

> **Static images buy certainty cheaply; video spends certainty expensively.**

图片阶段允许用少量平行候选把不确定性吃掉；Stage 05不靠昂贵Video抽卡解决本应在图片、分镜和逻辑阶段解决的问题。


## V4.5.2｜VIDEO CONDITIONING CANDIDATE

所有Video Unit至少有一个Primary Conditioning Frame。候选数按风险而不是“是否生成”：
- Promotion已满足全部Shot Contract与Clean QC：0张新图，直接Promotion；
- 普通FIRST_FRAME：默认1个主候选，失败再补；
- FIRST_TARGET / FIRST_LAST：每个Required Role默认1个；
- Contact / Transformation / Key Pose高风险：关键Role可计划2个候选；
- CUT_PAIR：Exit与Entry分别独立QC，再做Pairwise Alignment；不能因为两端各自好看就判关系PASS。

旧“T3/T4才有HD Anchor”的语义废止：复杂度只决定需要多少额外Keyframe，不决定是否存在Primary Conditioning。


## V4.5.2 Virtual Set Candidate Rule
- Planning Diagram重在结构正确，不按美术候选数量竞争；先QC空间事实。
- Event/Reciprocal/Predictive Coverage默认沿用普通Coverage候选策略，但同一Set多视角必须共享Spatial Parent + Visual Parent。
- Predictive Coverage不能为了填满九宫格增加候选；只有已知未来Shot/Relation/高复用机位能够证明`WHY_REQUIRED`时才生成。

## V4.5.4｜Coverage Debt First

Coverage候选不再按“同一场景多出几张总会有用”扩张。先运行`VIEW_ROLE_COVERAGE_MATRIX`：
1. 所有Required View先至少获得1个Candidate；
2. P0/P1 MISSING View优先于任何已覆盖方向的第2/第3轮候选；
3. 每个`view_requirement_id`使用自己的`candidate_budget`（缺省由Validator按4处理，项目可显式设更低）；
4. 某方向超过预算且仍有其它Required View为MISSING → `COVERAGE_BUDGET_STARVES_REQUIRED_VIEW`；
5. 候选只在其对应View Requirement内比较，不能用“14张车厢人物图”声称已经覆盖一个从后排沿纵轴向前看挡风玻璃的FORWARD Requirement。

## V4.5.5｜Realism Debt Before Extra Candidates

候选预算不仅遵守Coverage Debt，也遵守`Realism Debt First`：
- 当前Candidate出现P0现实性错误（人数、座位/Zone、车辆布局、人体穿插、功能空间漂移）时先定位根因并修Generation Spec；
- 不允许在同一错误Contract上盲抽第5/第10张，希望随机变合理；
- Spatial/Realism Contract正确时只重做受影响Candidate；Contract本身错误时先Patch上游再生成；
- 已经证明现实性PASS的其它视角不因局部失败失效。
