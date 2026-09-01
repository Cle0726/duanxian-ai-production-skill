# Character Asset Requirement Set（人物资产需求集与冻结规则）

> **用途：** 把人物身份资产从“有一张Character Master就算完成”改成按角色与真实镜头需要判定的Stage 03 Requirement Set。它不要求机械生成所有人物页，而是确保主要/反复/可变身角色在进入Storyboard前，真正需要的脸、发、个人装饰和人物关联关键道具Authority已经齐全。
>
> **核心原则：** `Freeze the required identity evidence, not a vague Character Master label.`

## 1｜适用范围

Stage 02对本集反复/命名/后续需要连续识别的人物建立：

```text
Character Asset Requirement Set｜<CHARACTER_ID>
Current LOOK ID:
REQUIRED BASE:
- DV-01 = REQUIRED / REUSE
- DF-02 = REQUIRED / REUSE
- HA-01 = REQUIRED / REUSE
CONDITIONAL:
- DF-01 = REQUIRED / NOT REQUIRED｜Reason=...
- AD-01 = REQUIRED / NOT REQUIRED｜Reason=...
- PR-01 = REQUIRED / NOT REQUIRED｜Reason=...
TRANSFORMATION (if applicable):
- TF / TE / TH / TC / WP / TS requirements = ...
Status: COMPLETE / INCOMPLETE
```

一次性`SCOPED_CAST / NON_RECURRING`不机械套用主角级完整Requirement Set；只要清楚可见就必须Stage 03建立一张`FMH_ASSET / APPROVED SCOPED FIGURE`作为Base Appearance Authority。SHOT_ASSEMBLY / PREVIS只能补关系与动作；TEXT_ONLY仅限真正深背景且无独立可读职责。

## 2｜默认Identity Lock Set

对主要 / 反复 / 可变身角色，Stage 03默认身份锁定基础为：
- `DV-01`：总身份 + 当前完整Look + FRONT/SIDE/BACK；
- `DF-02`：标准3/4脸，证明Face ID脱离正侧视仍成立；
- `HA-01`：头发结构，锁Far Silhouette / Part-Fringe / Face-framing / Back Mass / End Shape。

`DF-01`不是人人机械生成；当DV-01 FRONT FACE的面部细节不足、后续反复Close-up需要更直接正脸Authority、或Face Identity QC证明正脸容易模板化时才Required。

## 3｜AD-01 Need Test（个人装饰局部资产资格测试）

只有同时满足“存在稳定个人装饰”且下面任一风险成立，才将`AD-01 = REQUIRED`：
- 本集存在MCU / CU / ECU或其他能清楚读出装饰的镜头；
- 装饰是人物重要识别点，换边/换形会明显损害Identity；
- 装饰结构很小，DV-01 / 当前LOOK Authority无法稳定锁定；
- 装饰跨Scene / Episode反复出现，已经证明容易漂移；
- Reference Field Coverage预计会把`PERSONAL_ADORNMENT`判为CRITICAL，但当前Approved人物图不足以承担该字段。

若当前LOOK / DV-01本身已经足够清楚稳定该装饰，则：
`AD-01 = NOT REQUIRED / COVERED BY CURRENT LOOK`。

若该物件承担剧情因果、线索、超自然机制或需要独立结构Canon，则不建AD-01，升级为`PR-01 / Prop Authority`。

## 4｜PR-01 Need Test

当人物关联物件满足以下任一项时可进入`PR-01 / Character-linked Prop Authority`：
- 剧情因果 / 线索 / 机制重要；
- 反复被拿取、操作、特写；
- 需要稳定结构、尺度或状态；
- 仅靠人物母图无法承担其独立Prop字段。

普通装饰不得为了“更正式”机械升级PR-01。

## 5｜Stage 02 → Stage 03 → Freeze

Stage 02必须把每名适用人物的Requirement Set先写入Raw Asset Demand；经`asset_consolidation_sufficiency_audit.md`去重/复用后，再写入Final Episode Asset Requirement Manifest。

Stage 03只有在所有`REQUIRED / TO BUILD`项目都真实生成、QC并用户APPROVED后，该人物才记：
`CHARACTER REQUIREMENT SET = COMPLETE`。

Episode Asset Freeze不能只检查“有Character Master”；必须检查所有人物Requirement Set。

## 6｜Freeze Break

### `CHARACTER_IDENTITY_LOCK_GAP`
主要/反复/可变身人物缺失Stage 02已判Required的DV-01 / DF-02 / HA-01 / DF-01或其他正式身份锁资产。

### `ADORNMENT_ASSET_GAP`
当前Storyboard / Video把`PERSONAL_ADORNMENT`判为CRITICAL，Current Look / DV-01不足以稳定承担，且Stage 03应有的AD-01不存在或未APPROVED。

发现后：
`EPISODE ASSET FREEZE BROKEN(reason=character-identity-lock / adornment-detail)`
→ 回Stage 03只补最小缺口
→ QC + 用户批准
→ Re-Freeze
→ Change Impact只复查真实依赖。

若问题只有Approved Storyboard后才能唯一确定，并且Current Look仍可承担人物Identity，不自动扩大为Character Master重做；先判断是否属于Stage 04 Video Conditioning职责。

## 7｜Reference关系

`AD-01`属于`HD_OBJECT_AUTHORITY_IMAGE / DETAIL_AUTHORITY / PERSONAL_ADORNMENT_AUTHORITY`。

当`PERSONAL_ADORNMENT = CRITICAL`时：
1. 先检查Current Character / Current LOOK Authority是否足够清楚；
2. 足够 → 使用更直接且足够的Current Look，AD-01可OMIT；
3. 不足且已有Approved AD-01 → `AD-01 = MUST / PRIMARY PERSONAL_ADORNMENT_AUTHORITY`；
4. 不足且无AD-01 → `ADORNMENT_ASSET_GAP`，不得让Storyboard / Video重猜。

**Minimum Sufficient不是少图；关键个人装饰清楚可读时必须有正确Authority覆盖。**


## V4.5.7 Base Authority Override

旧项目中的`SHOT_ASSEMBLY / PREVIS_HUMAN_ANCHOR`不再可作为、共同承担或替代Readable Scoped Cast的Appearance Owner。清楚可见的一次性/配角人物必须补一张Approved FMH/Minor Human Master；正式使用的Environment/Sub-location必须补一张Approved空场景Clean Master。只有深背景不可辨认群众允许TEXT_ONLY。该规则优先于本文旧轻量兼容说明。
