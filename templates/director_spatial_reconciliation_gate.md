# Director Spatial Reconciliation Gate（导演空间复核闸门）

> **用途：** 解决Stage 02先规划导演关系、Stage 03后才得到正式Environment Geography之间的循环。它不新增Stage，而是在Stage 03内部执行**两次轻量复核**，避免先生成错误Coverage / Shot Assembly再返工。

## 1｜核心原则

Stage 02只锁`Scene Spatial Requirement Draft + Detailed Shot Contract`，不在新场景未批准前虚构门窗、柱体、尺度和可拍位置。

Stage 03使用两次复核：

`Environment Canon Master / Geography Approved → Pass A Geography Precheck → Coverage / Assembly / Support → Pass B Final Reconciliation → Episode Freeze`

---

## 2｜Pass A：Director Geography Precheck（先看真实空间，再做依赖资产）

### Pass A触发时机
每个新Environment的Canon Master + Geography / Blocking Spec批准后，**在依赖该空间的Derived Coverage / Shot Assembly正式生成前**执行。

### Pass A输入
- Approved Environment Canon Master；
- Geography / Blocking Spec；
- Stage 02 Scene Spatial Requirement Draft；
- Axis / Screen Direction / Eyeline Plan；
- 当前Detailed Shot Contracts；
- World State中的关键Prop / Door / Vehicle / Barrier状态。

### 检查
```text
Functional Zone Support
Must-See Relationship Support
Sightline Support
Movement / Combat Lane Support
Camera Feasibility：Entry/Landing Camera Geometry / Path / Stabilization是否有真实空间
Lens / Focus Feasibility：目标前后景关系、Critical Read与Focus Plan是否能成立
Depth Potential
Axis Feasibility
Blocking Start→Change→End Feasibility
Critical Visual Read Feasibility
```

### 结果
- 兼容 → `DIRECTOR GEOGRAPHY PRECHECK PASSED`
- Camera/Blocking需要调整且**不触及Director Invariants** → `DIRECTOR SPATIAL PATCH REQUIRED`，先Patch受影响Shot Contract，再重新计算Coverage / Assembly Need
- 真实Geography迫使核心Blocking/Distance、POV、Reveal、Reaction Give-Deny、关键Hold/Cut或Opening/Closing Function变化 → `DIRECTOR_INVARIANT_SPATIAL_CONFLICT`，返回Director Judge；Stage 03不得自行Patch
- Environment本体无法满足`EPISODE SCREENPLAY LOCK`明确的功能空间 → `ENVIRONMENT_FUNCTIONAL_GEOGRAPHY_CONFLICT`

**P0：未通过Pass A，不得批量生成依赖错误Shot Contract的Coverage / Shot Assembly。**

---

## 3｜Pass B：Final Director Spatial Reconciliation（依赖资产完成后的最终复核）

### Pass B触发时机
本Scene所需Coverage / Shot Assembly / Spatial Support已经Approved后、Episode Freeze前。

### Pass B输入
- Pass A通过后的Detailed Shot Contract；
- Approved Environment Canon Master + Geography；
- Approved Derived Coverage；
- Approved Shot Assembly（若Required）；
- Required Production Support（若承担空间/接触证据）；
- 当前World State / Character Requirement / Prop State。

### 逐Scene检查
```text
Coverage Support：当前Camera Side / Visible Side是否真正有Authority
Assembly Support：多人关系 / 功能位置是否由正确Assembly覆盖
Critical Visual Read Support：关键字段是否会被遮挡或因距离不可读
Depth Support：FG/MG/BG与Overlap/Crop是否仍成立
Cinematography Support：Entry/Landing Camera Geometry、Lens Family、Focus Plan、Stabilization与真实空间兼容
Axis / Screen Direction Support
Blocking Support
Reference Implication Consistency
Segment Dependency Consistency
```

### PASS
所有关键空间/镜头关系兼容：
`DIRECTOR SPATIAL RECONCILED`

### DIRECTOR PATCH
真实资产合理，但某个Shot关系需要调整：
- 先对照Director Decision Card / Sequence Arc；只在不触及Non-Negotiable Directorial Invariants时允许本地Patch；
- 若触及Invariant，停止本分支并标`DIRECTOR_INVARIANT_SPATIAL_CONFLICT`返回Director Judge；
- 不触及Invariant时只修改受影响Shot Contract；
- 更新对应Segment / Coverage / Static Risk / Assembly分析；
- 未受影响Shot保持有效。

状态：`DIRECTOR SPATIAL PATCH REQUIRED`。

### ASSET PATCH
导演意图合理，但缺真实视觉证据：
- `ASSET_COVERAGE_GAP`
- `SHOT_ASSEMBLY_GAP`
- `VIDEO_RISK_REFERENCE_GAP`

只补最小资产，再运行Pass B。

### ENVIRONMENT CANON CONFLICT
如果Environment本体无法满足`EPISODE SCREENPLAY LOCK`明确要求的功能空间关系：
`ENVIRONMENT_FUNCTIONAL_GEOGRAPHY_CONFLICT`

不得把矛盾留给Storyboard模型。

---

## 4｜Transformation Presentation Reconciliation（适用时）

首次/关键Transformation在Stage 02若尚无Approved Splendor Profile，只能先写`Transformation Presentation Requirement Draft`，不得虚构尚未设计的裙尾、材质或Weapon-Body Silhouette。

Stage 03实际TF / TH / TC / TE / WP完成并形成Approved `Transformation Splendor Profile`后，Freeze前复核：
- Large Silhouette Hook是否有Shot能真正读出；
- Musical Eye Motif所需Shot Size是否满足；
- Material Contrast是否被摄影距离/光线看见；
- Weapon-Body Silhouette是否有有效Hero framing；
- Stage 02原Presentation Draft是否需要根据真实设计做最小Shot Contract Patch；若Patch会改变Director Invariant，必须返回Director Judge，不由Transformation资产反向重导镜头。

通过：`TRANSFORMATION PRESENTATION RECONCILED`。

如果本集没有首次/关键Transformation：`N/A`。

---

## 5｜Freeze Gate

Episode Freeze必须同时满足：
- Required视觉资产齐全；
- 所有新Environment已`DIRECTOR GEOGRAPHY PRECHECK PASSED`，且无未解决`DIRECTOR_INVARIANT_SPATIAL_CONFLICT`；
- 最终状态`DIRECTOR SPATIAL RECONCILED`；
- 首次/关键Transformation适用时`TRANSFORMATION PRESENTATION RECONCILED`。

没有最终复核状态，即使资产都APPROVED，也不能进入正式Storyboard。

## 6｜Change Impact

复核后若只改SH12：
- 只重算SH12所在Segment及其Coverage / Reference / Assembly依赖；
- 不重做整Scene/整Episode；
- 已批准且无依赖的资产不失效。

## 7｜一句话

> **Stage 02先决定戏剧关系；Stage 03一拿到真实空间就先校准，再生产依赖图；资产完成后再做一次最终对齐。这样不是“最后才发现镜头拍不了”。**

## V4.5.5｜Reality Reconciliation Pass

Pass A/B都增加`Everyday Realism`检查：

`Source Facts → Realism Contract → Spatial/Functional Layout → World State → Generated Visual Evidence`。

若现实性失败，先定位Owner：
- Spatial/Vehicle Layout本身不现实且只是Derived → Patch Spatial Canon并重算受影响Coverage；
- Source明确、Spatial/Realism Contract正确而图片错误 → Reject当前Candidate，只重做受影响资产；
- 人物换位/湿度/物件等来源错误 → 回World State最小修正；
- 不同现实解会改变剧情意义 → 返回Director/User，不自动替换Canon。

P0/P1现实性未解决时不得把状态写成`DIRECTOR SPATIAL RECONCILED`。
