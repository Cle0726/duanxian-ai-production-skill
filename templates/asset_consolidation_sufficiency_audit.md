# Asset Consolidation & Sufficiency Audit（资产合并与充分性审计）

> **用途：** Stage 02在逐Shot完成Coverage / Video Risk / Shot Assembly / Character Requirement分析后，不直接把所有原始需求节点照单全收。先跨Shot聚类、合并、复用、去重并检查静态证据是否足够，再形成最终Episode Asset Requirement Manifest。
>
> **核心原则：** `Discover Need → Route Owner → Consolidate Across Shots → Reuse First → Remove Non-Static Problems → Sufficiency Check → Final Unique Asset Manifest`。数量是分析结果，不是目标配额。

---

## 1｜执行位置与边界

固定位置：

`Detailed Shot Contract → Segment Plan → Coverage / Static Risk / Functional Minor Human / Shot Assembly / Character Requirement → RAW ASSET DEMAND SET → Asset Consolidation & Sufficiency Audit → FINAL Episode Asset Requirement Manifest`

本Audit属于Stage 02的**Production Translation Pass**，不重新导演Shot，也不重新设计Canon。

- 不改变Scene Visual Thesis / Blocking / Axis / Entry/Landing Camera Geometry / Lens Family / Focus Plan / Stabilization / Camera Intent / Shot Relation；需要改变时回Director Core最小Patch；
- 不把Storyboard Grid / Previous Ending Frame算作Stage 03资产；
- 不用“资产少一点”作为牺牲关键Static Evidence的理由；
- 不用“图片便宜”作为无限制造无Shot依据资产的理由；
- Stage 04 Video Conditioning只登记策略/Required Roles，不提前算作已生成正式资产。

---

## 2｜RAW ASSET DEMAND SET

先保留逐Shot分析得到的原始需求，不急着命名成一张张最终图片：

```text
Raw Demand ID：RD__
Triggered By：SC__ / SH__ / SEG__
Need Class：CHARACTER / FUNCTIONAL_MINOR_HUMAN / PERFORMANCE_SUPPORT / NARRATIVE_FX / ENV_MASTER / PROP_MASTER / COVERAGE / PERSISTENT_STATE / SUPPORT_REF / SHOT_ASSEMBLY / COLOR_CONTROL / STAGE04_HD_ANCHOR
Authority Owner：<唯一Owner模块>
Critical Fields：当前必须稳定的视觉字段
Visual State：人物Look / Injury / Prop State / Transformation / Environment Runtime State
Spatial State：Environment View / Zone / Blocking Relation / Contact Geometry
Static-Solvable：YES / NO / PARTIAL
Existing Approved Evidence：<Asset IDs / NONE>
Residual Static Ambiguity：LOW / MED / HIGH
Video Risk If Missing：LOW / MED / HIGH
```

Raw Demand Node可以很多；**Raw数量不等于最终资产数量**。

---

## 3｜跨Shot合并签名（Consolidation Signature）

两个或多个Raw Demand只有在以下关键字段兼容时才允许合并：

```text
Same Authority Owner
+ Same Canon / Parent Master
+ Same Character / Prop / Transformation State
+ Same Environment View Family / Functional Zone（适用时）
+ Same Core Blocking / Relation State（Assembly适用时）
+ Same Critical Visual Fields
+ Same Static Risk Problem
```

### 可以合并的典型情况
- 同一Door-side Environment Coverage能稳定支持SH12 / SH13 / SH18；
- 同一“女主坐沙发、男主站立压迫”的Assembly可服务一组只改变表情/景别、不改变核心空间关系的Shot；
- 同一伤口/破损Persistent State Variant跨多个Shot持续；但若中间发生`TRANSFORMATION_RECOVERY=RECOVERED`，伤势Variant只能覆盖恢复点之前，恢复后不得继续合并/复用；
- 同一复杂握持/扶抱静态几何能支持连续Shot Group，Camera变化不改变关键接触关系。
- 同一个匿名功能人物在同一Scene/Shot Group内年龄段、服装轮廓、清晰度与职责不变时，可共享一个FMH Asset；若核心位置关系由同一Assembly承担，则不再额外复制FMH。

### 不应强行合并
- Screen Direction / Environment View发生实质变化，旧Coverage无法唯一支持；
- Character Look / Injury / Transformation / Prop State已改变；Transformation Recovery导致的Post-Recovery Injury State属于实质状态改变，必须切断旧Injury Variant复用；
- Blocking从“隔着屏障”变为“进入同一动作区”，核心空间关系改变；
- Contact Point / Holder / Support关系改变；
- Critical Read从整体关系转为必须读清新结构面/局部细节；
- 一个需求属于Canon/Coverage，另一个实际属于Support/Assembly，不能为减少数量混Owner。

---

## 4｜Reuse First，不重复建设

对每个Consolidated Need依次判断：

1. **EXACT REUSE**：已有Approved资产已完整覆盖Critical Fields → `REUSE`；
2. **PARENT + TEXT ENOUGH**：Master + Geography/Structure/Text Spec已把静态歧义降到足够低 → 不新增图；
3. **SHARED NEW ASSET**：多个Shot共享一个新Coverage / Support / Assembly → 只建一个Asset ID并记录所有Supported Shots；
4. **SHOT-UNIQUE JUSTIFIED**：只有当前Shot需要，且缺失会显著增加昂贵Video风险 → 允许单Shot资产；
5. **NON-STATIC**：速度、时间行为、Camera Motion、动作叠接等不是静态图能解决 → 从Stage 03图片需求移除，路由Stage 04/05；
6. **DEFER TO STAGE 04**：必须等Approved Storyboard精确构图后才能唯一确定 → `VIDEO_CONDITIONING_PLAN / SHOT_EXECUTION_FRAME_PLAN`，不提前建设。

---

## 5｜Asset → Shot Coverage Map

每个最终唯一资产必须记录它服务哪些Shot，避免“一个普通Shot一张新资产”的无意识碎片化：

```text
Asset ID：ASM_SC04_REL_A
Asset Class：SHOT_ASSEMBLY
Parent / Authority：...
Supported Shots：SH21 / SH22 / SH23 / SH24
Supported Segments：SEG_SC04_B01 / B02
Reuse Scope：SINGLE_SHOT / SHOT_GROUP / SCENE / EPISODE
Critical Fields Covered：...
Why Existing Assets Were Insufficient：...
Why This One Asset Is Sufficient：...
```

**Supported Shots多不自动代表好；Supported Shots少也不自动代表浪费。** 关键看是否存在真实共享视觉状态。

---

## 6｜Sufficiency Audit（充分性检查）

完成合并后，反向逐Shot检查一次：

```text
Shot ID
Key Visible Assets
Critical Visual Read
Static-Solvable Risk
Required Authority / Ref
Covered By Final Asset ID(s)
Coverage Status：PASS / GAP / NON_STATIC / STAGE04_DEFERRED
```

判定：
- 静态可解决且当前Final Asset Pool没有足够Authority/Reference → `ASSET_SUFFICIENCY_GAP`；
- 已有资产存在，但Required Critical Fields实际上未被覆盖 → 仍是GAP，不能用“有图”冒充“够用”；
- Shot需要清楚配角/功能性人物但没有`SCOPED_CAST_BRIEF + FMH_ASSET`，或Final Asset Pool没有对应Approved FMH/Minor Human Master → `FUNCTIONAL_MINOR_HUMAN_GAP`；
- Shot被`PERFORMANCE_ASSET_REQUIREMENT_SET`标记为Required，但Final Asset Pool没有对应Approved Performance Support → `PERFORMANCE_SUPPORT_GAP`；
- 剧情FX被`NARRATIVE_FX_ASSET_MANIFEST`标记为`NARRATIVE_FX_REFERENCE`，但Final Asset Pool没有状态覆盖充分的Approved FX资产 → `NARRATIVE_FX_ASSET_GAP`；
- Static-Solvable = NO → 不补图片，明确路由Stage 04/05；
- Stage 04 Deferred必须有具体Shot与Reason，不能成为Stage 02漏分析的垃圾桶。

---

## 7｜Redundancy / Fragmentation Audit（冗余与碎片化检查）

检查以下信号：

- 多张Coverage拥有同一Parent、同一View Family、同一Critical Fields，却没有不同Shot需求理由；
- 多张Assembly的Character Set / Environment / Core Blocking Relation完全相同，只因Shot ID不同而重复；
- Support Ref与Assembly在解决同一个问题，Owner职责重叠；
- 一批普通T1/T2 Shot几乎每个Shot都产生独立静态资产；
- 大量资产`Supported Shots = 1`且`Video Risk If Missing = LOW`；
- 相反，单一Master被要求支撑大量T3/T4复杂空间/接触镜头，却没有Coverage/Support/Assembly。

状态：
- `ASSET_FRAGMENTATION_REVIEW`：偏碎，需要检查，但**不是按数量自动Fail**；
- `ASSET_POOL_THIN_REVIEW`：静态准备可能过薄，需要检查，但**不是按数量自动Fail**；
- `ASSET_REQUIREMENT_DUPLICATION_CONFLICT`：已确认是同一需求的重复建设且无理由，必须合并或说明差异。

---

## 8｜Episode Asset Accounting（整集资产核算）

Stage 02必须输出可解释的核算，而不是只给总数：

```text
【Episode Asset Accounting｜EP__】
Raw Demand Nodes：__
Existing Approved Reuse：__
Merged / Shared Across Shots：__ raw nodes → __ unique needs
Removed as Non-Static：__
Deferred Raw Demand Nodes to Stage 04：__
Stage 03 New Unique Assets To Build：__
Projected Stage 03 Freeze Static Asset Pool：__
Stage 04 Video Conditioning Strategy Plan：__
Projected Final Episode Static Asset Pool（含Stage 04 Video Conditioning Required Frames）：__

By Class：
Character Requirement / Detail：__
Functional Minor Human / Scoped Figure：__
Environment Canon / Coverage：__
Prop / Weapon Canon / Coverage：__
Transformation：__
Persistent State：__
Performance Support：__
Narrative FX：__
Production Support：__
Shot Assembly：__
Scene Color Extension Card（Need=YES only）：__
Stage 04 Additional Video Conditioning Keyframe（conditional projected）：__
Other Authorized Static：__
```

`Projected Stage 03 Freeze Static Asset Pool = Existing Approved Reuse + Stage 03 New Unique Assets To Build`（同一Unique Asset ID只计一次）。

`Projected Final Episode Static Asset Pool = Projected Stage 03 Freeze Static Asset Pool + 当前明确标记Required/Planned的Stage 04 Additional Video Conditioning Keyframe`。Stage 04条件性Anchor若后续Storyboard证明不需要，则从真实Final Pool移除。

所有资产数按**唯一Approved/Planned Asset ID**计数，不把候选图数量算进去；一个Master生成2–4张候选，最终只计1个正式资产。

### 数量解释规则
- **不设置15–18分钟必须达到多少张的硬配额。** 资产量由Scene数量、人物状态、地点、服装、Transformation、复杂Blocking、Contact与Video Risk共同推导；
- 极低或极高数量只触发解释/Review，不直接判错；
- 若总量变化很大，必须能从`Reuse / Merge / New Risk / New Scene / New State`解释变化来源；
- 图片候选数量由`image_candidate_strategy.md`管理，不进入本资产数量核算。

---

## 9｜Stage 02交接状态

Stage 02使用两个内部状态：

1. `DIRECTOR CORE LOCKED`：Scene Intent → World State → Visual Thesis → Spatial / Blocking / Axis / Distance / Shot Progression → Detailed Shot Contract已完成，Director Hard Gates通过；
2. `DIRECTOR BREAKDOWN READY`：在Core Locked之后，Segment + Asset Analysis + Consolidation + Sufficiency Audit + Final Manifest全部完成。

以下任一未解决，不得进入`DIRECTOR BREAKDOWN READY`：
- `ASSET_CONSOLIDATION_NOT_RUN`
- `ASSET_SUFFICIENCY_GAP`
- `ASSET_REQUIREMENT_DUPLICATION_CONFLICT`
- `FUNCTIONAL_MINOR_HUMAN_GAP`
- `PERFORMANCE_SUPPORT_GAP`
- `NARRATIVE_FX_ASSET_GAP`

`ASSET_FRAGMENTATION_REVIEW / ASSET_POOL_THIN_REVIEW`如果检查后确认有合理导演/风险原因，可带解释通过，不因绝对数量阻塞。


## V4.5.7｜Base Authority Asset Consolidation Rule

图片数量本身不是需要压缩的对象。Consolidation只做**同一Entity的重复去重**，不得为了降低资产数删除Base Authority：
- 不同`location_entity_id`各自保留一张Active Empty Environment Master；
- 不同Readable `minor_human entity_id`各自保留一张Active FMH/Minor Human Master；
- 同一Entity跨Shot不得重复生成Master，使用`reuse_key + asset_family_id + version/lineage`复用；
- 摄影方向变化派生Coverage/View Set，不复制Master；
- Shot Assembly/Previs不得被Consolidation误判为可替代Base Master。


## V4.5.7｜Performance / Narrative FX Consolidation

- Performance Support按`entity_id + requirement_type + compatible performance state + supported shots`合并；不同表情语义或不同Contact关系不得为了省图强并。
- Narrative FX按`narrative_fx_id + state coverage + scope`合并；同一剧情现象的State Sheet可覆盖多个Shot，但普通Atmospheric FX不得因“图片便宜”升级成Canon。
- 两类资产都属于“Stage 03库完整性”，但是否进入某个Video Job仍由Reference Resolver决定。
