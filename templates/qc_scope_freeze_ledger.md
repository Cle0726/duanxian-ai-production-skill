# QC Scope Freeze Ledger（修订复检范围冻结账本）

> **用途：** 当Asset / Storyboard / Video经过一次QC后只返工部分问题，后续复检默认只检查本轮开放的Revision Target，不重复审查已经PASS且未被修改触及的维度。
>
> **核心原则：PASS可以冻结，但不能盲目永久冻结。只有本次修改真正影响到已冻结维度时，才按影响关系最小重开。**

---

## 1｜QC Dimension Status

每个正式验证对象的QC维度只能处于以下状态之一：

- `OPEN`：本轮需要检查；
- `FROZEN_PASS`：此前已PASS，本轮默认不重审；
- `REOPEN_IF_IMPACTED`：此前PASS，但本轮修改可能影响它，需要做Change Surface判断；
- `REOPENED`：确认被本次修改影响，本轮重新检查；
- `N/A`：当前对象不适用。

禁止把`FROZEN_PASS`理解成“以后永远不能检查”。冻结只对**未被修改触及的同一版本链**有效。

---

## 2｜QC Scope Ledger最小字段

```text
QC_SCOPE_LEDGER
Object ID: <Asset / Storyboard / Segment / Video>
Base Version: <v001 / Prompt Version / Take>
Previous QC Source: <WEB_EXTERNAL_VERIFIER / LOCAL_SELF_CHECK>
Previous Verdict: <PASS / REVISE>

FROZEN_PASS:
- Identity
- Structure
- Aspect Ratio

OPEN_REVISION_TARGET:
- Material
- Patch Fidelity

REOPEN_IF_IMPACTED:
- Style
- Continuity

Revision Surface:
- <本次究竟改了哪里、改了什么>

Reopened This Round:
- <真正因修改被重新打开的维度；无则NONE>
```

---

## 3｜Revision Scope判定

收到修订候选后，先回答：

1. 本次Revision Surface是什么？
2. 它是否触及某个`FROZEN_PASS`维度的证据区域或逻辑？
3. 如果不触及，该维度继续冻结；
4. 如果触及，只重开被影响的维度，不把所有QC清零。

### 示例

人物母图上一轮：
- Identity = FROZEN_PASS
- Structure = FROZEN_PASS
- Aspect Ratio = FROZEN_PASS
- Style = OPEN

本轮只修综合色/材质：
- Identity保持冻结；
- Structure保持冻结；
- Aspect Ratio保持冻结；
- Style / Material复检。

若本轮Patch直接修改脸部轮廓：
- Identity必须从`FROZEN_PASS → REOPENED`；
- 其余未受影响维度继续冻结。

---

## 4｜Web QC Evidence Packing联动

网页版Evidence Pack必须根据**本轮开放维度**选择证据，而不是机械重复上一轮所有图。

- 当前复检Render Style → Render Style Anchor从P1升级为P0 Evidence；当前复检Cinematic Shot Style时只上传摄影语法Evidence；综合色复检则按Global/Scene/Shot当前层级选择最直接Color Evidence；
- 当前复检Identity → Character Identity Authority为P0；
- 当前复检Continuity → Ending Frame / Spatial Authority为P0；
- 已冻结Identity且本轮未触及脸/体型 → 不为“保险”额外占10图槽位；
- 但Candidate本身始终需要上传。

`Evidence Priority = function(Current QC Scope)`，不是固定由资产类型决定。

---

## 5｜Multi-Pass与Candidate Group

若单对象P0 Evidence > 10图：

- 每个Pass都重复**完整Candidate Comparison Group**，不得只重复“某一个Candidate”；
- 每个Pass记录：`Object ID / Version / Candidate ID / Batch ID / Pass ID`；
- 文件哈希可取得时记录SHA-256；不可取得时至少记录稳定文件名/上传顺序；
- PASS-A / PASS-B只拆检查维度，不拆候选身份。

最终合并：

`WEB_QC_MERGED_RESULT = all pass results for the same Object + Version + Candidate Group`

任一Reopened P0维度FAIL，则整体不能PASS。

---

## 6｜Local Patch联动

Local Patch完成后默认开放：
- Authorized Change；
- Patch Fidelity；
- Patch Integration；
- Frozen Region Drift。

此前冻结维度只有在Patch实际触及相关区域时才重开。例如：
- 改扳手端部 → Tool Structure重开；综合色若未授权则继续冻结；
- 改人物胸针 → Identity通常不重开；若Patch侵入脸部则Identity重开。

---

## 7｜Storyboard复检

Storyboard Revision可冻结：
- 已确认人物身份；
- 已确认场景几何；
- 已确认Shot数量；
- 已确认Aspect Ratio；

本轮只改某一Panel动作时，只复检：
- 该Panel Action Feasibility（Limb Occupancy / Held Prop Support / Transfer / Preconditions / Exit State）；
- 该Panel Action Physics；
- 与相邻Panel的Continuity；
- 受影响的Performance / Spatial关系。

不得因为一个动作修订把整张Storyboard所有已PASS维度重新审一遍。

---

## 8｜Video复检

Video若执行Minimum Prompt Revision，复检范围必须包含：
- 本次Prompt修改目标；
- 修改可能造成的直接连锁维度；
- Exit State / Continuity（若时序或动作被改）。

没有被改动、且新Take肉眼未出现明显新漂移的已PASS维度可保持冻结；但Video是重新生成的随机输出，Identity / Major Spatial Continuity等P0安全项仍允许做快速Sanity Check，不能完全失明。

---


## 8.1｜Temporal Salvage与Dimension Freeze分离

Video Revision后，旧Take的`CLEAN_KEEP / CONDITIONAL_KEEP / HANDLE_ONLY`时间窗可以继续保留在`SALVAGE_CLIP_REGISTRY`，但它们不等于新Take的QC维度PASS。

- Dimension Freeze回答“哪些质量维度不用重审”；
- Temporal Salvage回答“旧Take哪些真实时间素材值得保留”；
- 新Take仍需自身P0 Sanity Check；
- 旧Take的Salvage Window不会因新Take生成而自动失效；只有Story/Canon/Continuity变更使它不再可用时才由Change Impact标STALE。

禁止用`FROZEN_PASS`伪造Salvage时间窗，也禁止用Salvage Window跳过新Take必要QC。

## 9｜输出到网页版Copy Prompt

修订复检的Copy Prompt必须明确写：

```text
【QC Scope Freeze｜本轮只检查这些】
FROZEN_PASS：Identity / Structure / Aspect Ratio
OPEN_REVISION_TARGET：Style / Material
REOPENED：NONE

除非本轮Revision Surface明显破坏已冻结维度，否则不要重新审查FROZEN_PASS，也不要因为个人审美重新推翻上一轮已冻结结论。
```

---

## 10｜Gate

交付复检包前检查：
- 有Previous QC时是否建立QC Scope Ledger；
- 本轮Revision Surface是否明确；
- Frozen与Open维度是否分开；
- Evidence Pack是否按当前Open Scope选图；
- 任何重开都有具体影响理由；
- Multi-Pass是否保持完整Candidate Group身份。

失败：`QC_SCOPE_UNRESOLVED`，不得直接发给Verifier。
