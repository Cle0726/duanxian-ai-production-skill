# Personal Creator Cost Efficiency Engine（一人制片成本效率引擎）

> **适用范围：** 《断弦之歌》Stage 02的Production Translation Pass以及Stage 03–05。**不得在Director Judge / Sequence Arc之前参与导演方案选择。** 当前项目的关键现实是：**静态图片生成成本很低，Video Take成本很高**。目标不是压缩图片候选，而是把不确定性尽量用文字、多个低成本静态候选、静态QC与分镜解决，提高Stage 05首轮命中率，把昂贵视频算力集中到真正值得的镜头。图片候选数量读取`image_candidate_strategy.md`。
>
> 核心原则：**Spend cognition before compute.｜先花判断力，再花算力。**

---

## 0｜Director Boundary｜Current

本引擎只优化**如何执行已选导演方案**，不决定“哪种拍法更值得选”。在Director Intelligence阶段：
- 不因为某镜头贵、模型难、Reference缺就淘汰Directorial Option；
- 不因为已有某张资产就偏向对应构图；
- 不把Video稳定性当Actor/DP/Editor Critique理由。

只有Director Judge + Sequence Arc锁定后，本引擎才可以优化Segment拆分、静态参考投资、Candidate预算与Retry策略。若成本/执行限制无法在不伤Director Invariant的前提下解决，返回`AI_EXECUTION_CONSTRAINT_CONFLICT`，不得静默改导演。


## 1｜预算Authority

《断弦之歌》默认按**个人/单人制片预算**运行，而不是商业AI长片团队的高算力模式。

因此：
- 不把“昂贵Video大量生成后海选”当默认质量保证手段；静态图片允许受控候选组与Production Support Reference用于低成本前置消歧；
- 不把每个镜头都按Hero Shot投资；
- 能在Stage 02/03/04解决的问题，不进入Stage 05付费验证；
- Stage 05已有Take失败时，新增Take前先做Temporal Salvage；已经成功的真实时间窗优先保留，不重复付费生成同一已成功内容；
- 能局部Patch解决的正式资产问题，不整张重生；
- 能Trim/Post解决的Video问题，不整段重生；
- 所有**新增正式Authority / VFX Reference / 多机位Environment Set / 额外Video Take**都要回答：**它是否显著降低后续更昂贵的失败概率？** 同一图片Job的2–4张平行Candidate不是新增正式Authority，按Image Candidate Strategy管理。

若答案是否定或不确定，默认不新增。

---

## 2｜Cost Ladder（成本阶梯）

从低成本到高成本依次处理问题：

1. **Text / Logic Fix**：Story / World State / Actor / Combat / Camera逻辑修正；
2. **Static Canon / Coverage / State Fix**：补真正缺失的对象结构、空间方向、持久状态；
3. **Static Production Support Reference**：若复杂Interaction / Contact / Transient State能用一张高清图显著降低Video风险，Stage 03先解决；
4. **Storyboard / Blocking Fix**：构图、空间、动作、Contact、Camera Contract修正；
5. **Additional Video Conditioning Keyframe**：Approved Storyboard后，T3/T4或高风险镜头若低清控制仍可能让Video误读，先生成高清Shot Anchor；
6. **Static Candidate Triage / QC**：对计划内低成本图片候选筛Primary / Backup并完成Deep QC；
7. **Single Video Take**：正式生成1个Take；
8. **Targeted Video Retry**：诊断后局部改Prompt再生成1次；
9. **Selective Video Candidate Budget**：只对高价值且高随机性的镜头增加Take；
10. **Re-plan / Split**：持续失败时拆Segment或改变执行方案。

不得从第1层问题直接跳到昂贵Video重试/多Take层烧算力。静态图片候选属于前置确定性投资，不与Video Take等价。

---

## 3｜Static-First Stop Gate（静态优先停机闸门）

**静态图已经能看见的P0/P1问题，禁止送入Stage 05“看看动起来会不会好”。**

包括但不限于：
- 人脸/年龄/发型Identity偏移；
- 武器/道具结构模糊、左右反转、接触点不成立；
- 衣服、链条、五金、手指、边缘结构已经出现融化/歧义；
- Environment门窗/入口/走位空间不成立；
- 关键光源方向或阴影已经自相矛盾；
- Storyboard攻击方向、人物倒向、Contact Point、Camera Axis明显错误；
- VFX Reference本身空间几何不成立。

处理顺序：
`STOP → Static Diagnosis → Patch / Replace Candidate / Rebuild Necessary Asset → QC PASS → 才允许视频化`

P2微小绘画差异不触发停机。

---

## 4｜Master Freeze + Local Patch（母图冻结 + 局部补丁）

正式Master一旦APPROVED，默认冻结其未出错区域。

### 4.1 局部错误
若只错：
- 一枚钉帽；
- 一段链条；
- 一个环形端；
- 一只手；
- 一个扣件；
- 小片纹样；
- 局部材质/阴影；

优先：
`Approved Master原图 → Reference Role Resolve → Mask/Local Edit → Patch Composite → 局部QC → 新版本APPROVED`

执行任何Local Patch / Revision前必须读取 `task_bound_reference_binding.md` + `inpaint_local_patch_authority_engine.md`：真正待修改的现有图片（包括QC失败Candidate）绑定为`EDIT_TARGET / REVISION_SOURCE_IMAGE`；Parent Master仅在必要时提供Identity / Structure / Geography Support。若存在用户/项目提供的正确局部图案/结构参考，必须额外绑定为`PATCH_DESIGN_AUTHORITY`，不得用Edit Target自身代替。

不要：
`整张重新生成 → 又发现脸/服装/光线漂移 → 再整张生成`

### 4.2 Patch Provenance
局部修订必须记录：
- Base Master Version；
- EDIT_TARGET；
- PATCH_DESIGN_AUTHORITY（若无则TEXT-ONLY）；
- Patch Region；
- Authorized Change；
- Frozen Regions；
- Result Version。

修订后的新Master仍需QC/用户批准，但**未授权区域不得借修补机会重新设计**。

---

## 5｜Clean Input Principle（干净输入原则）

用于下游Reference的Master首先是**机器可读的设计Authority**，其次才是漂亮展示图。

人物身份/造型Master优先：
- 干净中性背景；
- 单一、柔和、可读的照明；
- 尽量减少剧情雨雾、战斗光、复杂逆光、环境综合色烤入；
- 清楚的轮廓、材质边界、服装结构、武器结构；
- 不用海报式强光把脸/衣服边缘染成后续每个镜头都会继承的错误特征。

Environment Master同样优先可读Geometry与Landmark，再由Scene Runtime / Storyboard / Video决定当前天气、破坏、烟雾与剧情光。

**Clean Input ≠ 无风格。** 仍必须遵守Project Style DNA，只是不把临时场景效果烤进身份Authority。

---

## 6｜Location Investment Tier（场景投资等级）

不是每个Environment都机械制作360°全套视图。

### L1｜Single-View / Low Continuity
适用：
- Establishing Shot；
- 插镜；
- Montage；
- 不发生反打/复杂走位的短场景。

通常一个高质量Master即可。

### L2｜Blocking-Critical
适用：
- 多人对白反打；
- 人物明确从入口走到目标；
- 车辆到达/下车/进门；
- 追逐、战斗、重要Prop移动；
- 同一空间反复跨Segment使用。

需要建立最小必要的：
- 3/4 Master / Reverse / Side之一或数项；
- Entrances / Exits；
- Walkable / Action Space；
- Stable Landmarks；
- Camera-accessible lanes。

### L3｜Hero / Recurrent Set
适用：
- 本季反复使用的核心地点；
- Boss战空间；
- 长时间、多机位、高连续性场景。

才考虑更完整Environment Master Set / Blocking Map。

规则：**Geography before coverage + Shot-triggered coverage + Video-risk sufficiency.** 先建立Environment Canon Master与空间关系，再读取Stage 02 `Environment Shot Coverage Matrix`；只有真实Shot存在正式方向/结构风险且当前Authority仍留下明显静态歧义时增加Reverse/Side/Zone视图，不为“保险”生成完整360°。道具同理。复杂交互/Contact等非结构问题转`production_support_reference_engine.md`，不要把每个动作都做成Coverage。

---

## 7｜Cinematography / Camera Contract（摄影语言与运镜契约）

Camera/Focus本身影响废片风险时，按`cinematography_grammar.md`先锁Entry/Landing Camera Geometry、Lens Family、Focus与Stabilization；非Static或路径存在歧义时再读取`camera_motion_contract.md`锁Path / Speed / Motion Curve / Focal Behavior / Landing。

**不要在成本层复制第二套Camera Schema。** 本引擎只检查：静态Previs是否已经能证明关键机位/焦点/路径，能在Stage 04解决的问题不得留给Video多Take碰运气。简单镜头不机械写满摄影字段。

---

## 8｜Shot Investment Tier（镜头投资等级）

Stage 02为每个Segment标记生产投资等级，用于控制生成次数与QC精度。

### T1｜UTILITY（功能镜头）
例：简单过渡、短插镜、低风险环境建立。
- 默认1 Take；
- 不预生成候选；
- P2问题优先接受/后期处理。

### T2｜STORY（普通叙事镜头）
例：重要对白、人物反应、普通连续动作。
- 默认1 Take；
- QC后若明确可修 → 改Prompt再1 Take；
- 只有接近合格且随机性高时，才可选同Prompt再1次。

### T3｜COMPLEX（复杂镜头）
例：多人动作、复杂Camera、关键Combat Exchange、重要Transformation步骤。
- 仍先生成1 Take；
- Stage 04必须严格验证Stage 02 Director Contract并补Micro-Blocking / Contact / Camera Path；若要改核心Blocking/Distance/Axis则回Stage 02最小Patch；
- 若首Take证明Prompt结构正确但模型随机性成为主要瓶颈，可使用**受限候选预算**，通常总Take不超过3–4个；
- 超过预算前必须重新Diagnosis，不连续抽卡。

### T4｜HERO（英雄镜头）
例：本集最重要的变身、Boss关键Hit、核心揭示、可作为宣传物料的高价值镜头。
- 允许把有限算力集中在这里；
- 先完成严格Static/Storyboard Gate；
- 可在首Take后根据Failure Diagnosis批准额外候选；
- 建议总Take预算通常2–4个，只有用户明确授权或极高价值且已有接近成功证据时才继续增加；
- 不复制商业团队几十次海选规模。

### Budget Rule
**候选预算是上限，不是目标。** 第1个Take已经通过就立即停止。

---

## 9｜Best Take Selection（最佳Take选择）

多个Take已经存在或T3/T4启用受限候选预算时：

1. 先按P0正确性淘汰；
2. 再比Action / Physics / Performance / Camera / Continuity；
3. 再比Ending Frame与后期可修复性；
4. 最后才比纯审美。

一个只有尾部P2问题、可Trim解决的Take，通常优于一个“整体更漂亮但动作因果错”的Take。

Candidate Triage只负责选择，不自动APPROVED。

---

## 10｜Hero Shot Budget Concentration（英雄镜头预算集中）

整集预算不平均分配。

优先高投入：
- 首次/关键变身；
- Boss关键Exchange / Narrative Impact；
- 核心人物情感Close-up；
- 本集结尾Hook；
- 宣发潜力强、可反复复用的关键镜头。

优先低投入：
- 普通Establishing；
- 纯功能Transition；
- 可以剪辑/声音辅助完成的短连接；
- 不承担身份/战斗/情绪关键的信息镜头。

Stage 02可给出：
```text
Investment Tier：T1 / T2 / T3 / T4
Why：一句话说明价值与风险
Max Planned Take Budget：1 / 2 / 3 / 4（按当前情况，不机械填满）
```

---

## 11｜Failure-before-Compute Rule（重生成前诊断）

每一次额外Video Take之前必须能回答：
0. 当前Take是否已经完成`TEMPORAL_SALVAGE_MAP`，有没有可以直接保留的时间窗？

- 当前失败属于Prompt可控问题还是模型随机性？
- 能否用Trim/Post解决？
- 能否通过局部Prompt修改解决？
- 是否来自错误Master / Storyboard / World State / Camera Contract？
- 额外Take相比回上游修改，哪一个更便宜且成功率更高？

不能回答时，**不默认继续生成。**

---

## 12｜不吸收的高预算做法

即使外部AI电影项目采用，也不自动进入《断弦之歌》默认流程：
- 每镜头十几/几十次生成海选；
- 为所有地点建立完整360°资产；
- 为普通VFX机械制作Reference；
- 为一个局部错误重生整张Master；
- 只用“字数本身”当质量指标；**但Stage 05必须遵守`PROMPT_LENGTH_CEILING = NONE`与完整控制项Contract，不能借成本优化压成短Prompt，也不能用历史3000字级作为裁剪线。**
- 用大量随机Camera Shake / 爆闪掩盖物理问题；
- 在Actor Prompt中反复要求可见胸腔呼吸来“增加生命感”。

原则：**学习方法，不复制预算规模。**

---

## 13｜Stage Integration

### Stage 02
- 标记Location Investment Tier；
- 标记Shot Investment Tier；
- Hero Shot只挑真正重要的少数镜头；
- 把空间/Camera/Combat风险尽量前置解决；
- 运行Video Risk-Driven Static Reference Matrix，把静态可解的高风险歧义路由到Coverage / Persistent State / Stage 03 Support / Stage 04 Additional Video Conditioning Keyframe。

### Stage 03
- 读取`image_candidate_strategy.md`：Design-bearing Master默认2张，高风险可4张，Environment / Prop Coverage与Stage 03 Production Support默认2张；先Triage再Deep QC；
- 执行Static-First Stop Gate；
- Master Freeze + Local Patch；
- Clean Input；
- Environment / Prop执行Master First：先一张Canonical Master + Text Spec；
- 只生成由Stage 02真实Shot证明需要的Environment / Prop Derived Coverage；
- 对Stage 02标记Required且Static-Solvable的复杂Interaction / Contact / Transient State生成Production Support Reference；
- 只生成下游确实需要的VFX Reference。

### Stage 04
- Stage 04普通Previs Component默认1张；多人/战斗/复杂Blocking / Camera Path等高风险Component可按Image Candidate Strategy计划2张并先Triage；
- T3/T4镜头强化Blocking、Contact、Cinematography Grammar与Camera Motion Contract；
- 检查是否能用最合适的Previs形式提前消除一次视频失败；
- 对被标记`ADDITIONAL_CONDITIONING_KEYFRAME_REQUIRED`的高风险镜头，在`APPROVED PREVIS SET`后先生成/批准高清Shot Support Anchor，再进入Video。

### Stage 05
- 默认从1 Take开始；
- 额外Take必须服从Investment Tier + Failure Diagnosis；
- T3/T4可以有受限候选预算，但不连续盲抽；
- 先Select Best Take，再决定是否真需要新生成。

---

## 14｜最终判断句

每当系统准备新增一个**正式Authority/Reference**、一个Video Take或一次昂贵重生成时，先问：

> **“这个花费是在解决已经知道的问题，还是在赌模型随机给我一个更好的结果？”**

如果主要是后者，默认停止并回到更便宜的上游层解决。

## Current｜No Financial Calculator Boundary
本Skill继续把“Video生成应谨慎、静态可先解决风险”作为生产原则，其中`video_generation_readiness_gate.md`是**技术就绪闸门**，不计算货币金额、总成片成本或预算预测。是否Ready只取决于冲突、Reference、Proof、Motion Load与执行完整性。
