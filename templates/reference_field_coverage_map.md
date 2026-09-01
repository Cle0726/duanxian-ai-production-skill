# Reference Field Coverage Map（关键可见资产参考覆盖表）

> **用途：** Stage 04 Storyboard与Stage 05 Final Video在真正Resolve @参考图之前，先证明“当前镜头里所有关键可见资产都已经有足够直接的视觉Authority”。
>
> **核心原则：Minimum Sufficient Reference Set（最小充分参考集），不是Minimum Image Count（最少图片数）。**
>
> 无意义Reference要删；但当前镜头里会被清楚看见、会参与动作、会影响身份/结构/空间/连续性的关键资产，一个都不能为了省槽位被静默省略。
> **Stage 02 `Critical Visual Read` 是本表的重要输入。** 导演已经判定某字段“这个Shot必须看清”时，Stage 04/05不能因为Reference精简或景别变化把它降级。

---

## 1｜什么叫 Key Visible Asset（关键可见资产）

满足任意一项，默认列入关键可见资产：
- 明确剧情人物，且脸/服装/身份在当前镜头可读；反复/命名人物通常必须回到正式Character Authority；一次性Montage/功能人物必须先有Stage 02 `SCOPED_CAST_BRIEF`；只要清楚可见，Stage 03必须已有Approved FMH/Minor Human Master覆盖Appearance，Assembly/Previs只补Placement/Pose/Contact；
- 关键道具、武器、乐器、载具、怪物/实体，且会被清楚看到、持握、操作、攻击、特写或承担因果；
- 当前镜头空间关系依赖的Environment Zone / Derived Coverage；
- 会跨镜持续的伤势、破损、湿损、血迹、变身状态；**Pre-Transformation Injury Ref在`TRANSFORMATION_RECOVERY=RECOVERED`后不得继续作为当前Injury Authority。**
- 多人接触/站位关系对画面成立很重要；
- 当前镜头的真实Continuity Entry必须由上一Approved Ending Frame约束；
- 已批准Storyboard / Shot Assembly / Additional Video Conditioning Keyframe中某个字段对当前执行不可替代。
- Stage 02 Detailed Shot Contract明确标为`Critical Visual Read`的脸、眼妆、武器接触、伤势、Prop状态、空间关系、Transformation Silhouette等。

通常不自动列为独立关键资产：
- Deep Background Mass；
- 一次性不可辨认路人；
- 不被清楚看见、没有因果作用的普通背景小物；
- 已经被当前最直接Assembly/Anchor完整承载、且单独上传不会再增加必要控制字段的上游重复图。

---

## 2｜Reference Field Coverage Map

每个Stage 04 Segment / Stage 05 Generation Segment先建立：

```text
| Field | Visible Asset / State | Critical? | Required Visual Authority | Most Direct Approved Ref | Input Mode | Covered? | Notes |
|---|---|---|---|---|---|---|---|
| CHARACTER_IDENTITY | CHR_A | YES | identity/current look | CHR_A_CURRENT | HD_OBJECT_AUTHORITY_IMAGE | YES | recurring/named |
| SCOPED_CHARACTER_APPEARANCE | Nurse_A | YES | one-scene appearance | FMH_NURSE_A | HD_OBJECT_AUTHORITY_IMAGE | YES | SCOPED_CAST / NON_RECURRING; Base Appearance Owner fixed to FMH; Assembly may only cover separate relation/placement/contact fields |
| ENVIRONMENT_VIEW | Opera stage left reverse | YES | current shot geometry | ENV_STAGE_CV_LEFT_REVERSE | HD_OBJECT_AUTHORITY_IMAGE | YES | |
| PROP_STATE | White pendant cracked | YES | current state | PROP_PENDANT_CRACKED | HD_OBJECT_AUTHORITY_IMAGE | YES | |
| PERSONAL_ADORNMENT | recurring signature earring/ring/pin | YES when clearly readable & identity-bearing | current look / AD-01 | CHR_CURRENT or AD01 | HD_OBJECT_AUTHORITY_IMAGE | YES | Current Look sufficient→use it; insufficient+Approved AD-01→AD-01 MUST; insufficient+no AD-01→ADORNMENT_ASSET_GAP |
| TRANSFORMATION_EYE_SIGNATURE | Celia transformed eye motif | YES when eye graphic readable | TE-03 eye/motif canon | TE03_CELIA | HD_OBJECT_AUTHORITY_IMAGE | YES | Primary Eye Signature + Secondary Graphic / Iris detail |
| RELATION_ASSEMBLY | A supports injured B | YES | multi-character relation | ASM_... | HD_SHOT_ASSEMBLY_IMAGE | YES | |
| STORYBOARD_CONTROL | SH12 composition | YES(Stage 05) | camera/blocking | SB_SH12 | CONTROL_IMAGE / CONTROL_CROP / TEXT_CONTROL（按Capability Route） | YES | |
```

推荐Field集合：
- `CHARACTER_IDENTITY / CURRENT_LOOK / PERSONAL_ADORNMENT / SCOPED_CHARACTER_APPEARANCE`
- `TRANSFORMATION / TRANSFORMATION_EYE_SIGNATURE / MUSICAL_EYE_MOTIF / INJURY / PERSISTENT_STATE`
- `ENVIRONMENT_VIEW / GEOGRAPHY`
- `PROP / WEAPON / VEHICLE / ENTITY_STATE`
- `MULTI_CHARACTER_RELATION / SHOT_ASSEMBLY`
- `COMPLEX_CONTACT / INTERACTION`
- `CONTINUITY_ENTRY`
- `STORYBOARD_CONTROL`
- `RENDER_STYLE`
- `SCENE_COLOR / SHOT_LIGHTING`

---

## 3｜Stage 04 Storyboard：关键资产必须先齐

Storyboard生成前：
1. 读取Stage 02 Detailed Shot Contract的`Focus Owner / Critical Visual Read / Shot Size / Screen Occupancy / Depth / Entry/Landing Camera Geometry / Lens Family / Focus Plan / Axis`，先确定导演真正要求看清什么；
2. 枚举当前Segment所有会真正入镜的关键人物；
3. 枚举当前Panel/Shot会清楚看见或操作的关键Prop / Weapon / Entity / Vehicle；
4. Environment使用最匹配当前Camera Side / Zone的Approved Coverage；
5. 若多人关系/人物进入场景容易猜错，使用Approved `SHOT_ASSEMBLY_ASSET`;
6. CONTINUITY_ENTRY才按需加入真实Previous Ending Frame；CUT_ENTRY / SCENE_OPENING不机械加入；
7. 若稳定Signature Adornment在Panel中清楚可读且承担身份识别，必须由当前Character Master或AD-01覆盖；
8. 若变身角色的眼妆/瞳孔在Panel中达到可单独识别程度，或该Beat本身强调眼部启动/眼神/变身完成，则`TRANSFORMATION_EYE_SIGNATURE / MUSICAL_EYE_MOTIF = CRITICAL`，Approved TE-03必须作为Most Direct Eye Authority；
9. Style/Color按Visual-First路由：当前任务已有Approved且相关的Style/Color视觉Authority、平台可接收图片且对应Route未`VERIFIED_FAIL`时，优先视觉绑定；能力`UNKNOWN`不自动降为TEXT_CONTROL。仅当该字段已被更直接视觉Owner完整体现、平台客观不支持视觉输入、或当前任务Scope确实不需要该字段时才省略/文字补充。

**如果一个关键可见资产没有Approved视觉Authority：**
输出 `REFERENCE_COVERAGE_GAP`时：任何Readable Scoped Cast若缺FMH/Minor Human Master，一律回Stage 03补Base Authority并打破Freeze；Stage 04 Previs不得首次发明其Appearance。不得为了继续Storyboard而用纯文字、白描或Assembly硬顶一个本来应该视觉锁定的人物。

---

## 4｜Stage 05 Final Video：镜头里出现的关键资产不能漏

Final Video Reference Pack必须逐项覆盖：
- Stage 02 / Approved Storyboard已经锁定的Critical Visual Read；
- 当前清楚入镜的主要/可识别人物；
- 稳定Signature Adornment若在当前镜头清楚可读并属于人物识别点，必须覆盖`PERSONAL_ADORNMENT`；Current Look足够清楚时不重复加图，Current Look不足且Approved AD-01存在时`AD-01 = MUST / PRIMARY PERSONAL_ADORNMENT_AUTHORITY`，不足且无AD-01则`ADORNMENT_ASSET_GAP`；
- 变身角色若眼妆/瞳孔达到可辨识程度或属于剧情重点，必须覆盖`TRANSFORMATION_EYE_SIGNATURE / MUSICAL_EYE_MOTIF`；
- 当前Shot真正看到的Environment方向；
- 当前会被看清或参与动作的关键道具/武器/载具/怪物；
- 当前持久状态；
- 当前复杂关系/接触（若Assembly / Support / Anchor有必要）；
- Approved Storyboard控制；
- Continuity Entry（适用时）；
- 当前综合色/光色与Render Style（需要图像Evidence时）。

**关键可见资产多，不是删图理由。**
如果凯登、西莉亚、当前舞台反拍、白吊坠和黑色音叉都在镜头里且都清楚可读，它们都必须被Reference Field Coverage Map覆盖。

允许用更高密度Authority减少重复：
- Approved `SHOT_ASSEMBLY_ASSET`可承载多人关系/人景物组合；
- Approved `VIDEO_CONDITIONING_KEYFRAME`可承载具体Shot的高清组合执行；
- 但如果Anchor/Assembly不足以锁某个角色身份或某个道具结构，该对象自己的Approved HD Authority仍必须保留。

---


### 4.1 Transformation Eye Visibility Rule（变身眼妆可读性路由）
- Wide / Full Body且眼部不可辨识：TF-01负责整体Transformation，不机械追加TE-03；
- Medium：如果Primary Eye Signature已经能单独读出，TE-03升级为Critical；否则TF-01可继续承担整体身份；
- MCU / CU / ECU、变身完成、眼部启动、战斗眼神、关键情绪Close-up：TE-03默认`MUST / Most Direct Eye Authority`；
- 已有TE-03时，不允许只靠文字或TF-01重新猜音乐眼妆。

## 5｜Reference Slot Pressure（参考槽位压力）

若平台/工作流存在图像槽位上限，**不得通过静默删除关键资产解决**。

正确顺序：
1. 删除真正重复/无职责Reference；
2. 用最直接Derived Coverage替代“Coverage + 无必要Parent Master”重复组合；
3. 用Approved Shot Assembly / Additional Video Conditioning Keyframe合并多人关系与组合字段；
4. 先对Style / Color / Storyboard做**视觉路由压缩**：Whole Board→关键Panel、重复综合色→唯一Current Color Authority、重复Style证据→Most Direct Visual Style Evidence；只有非Critical、已有其他视觉Owner完整接管，或平台客观不支持视觉输入的剩余字段才可降`TEXT_CONTROL`；**不得仅为省槽位把Required Visual Authority文字化**；
5. 仍然超过可用槽位 → `REFERENCE_SLOT_OVERFLOW`，回Stage 03/04重组Assembly/Anchor，或必要时调整Segment；**禁止继续生成并赌模型自行补关键资产。**

---

## 6｜Hard Gates

### `REFERENCE_COVERAGE_GAP`
任一Critical Field：
- 没有Approved Authority；
- 选中的Reference不能实际覆盖该字段；
- 关键入镜人物/道具/怪物/状态被为了“精简”删除；
- Storyboard或Video正在依赖一个不存在的关键视觉定义。
- Stage 02标记CRITICAL的字段在Stage 04/05被静默降级、景别不足或没有最直接Authority。

→ 禁止交付Storyboard Prompt / FINAL VIDEO PROMPT。

### `REFERENCE_SLOT_OVERFLOW`
所有关键字段都需要视觉Reference，但实际输入槽位无法容纳，并且还没有合法的Assembly / Anchor / TEXT_CONTROL重组方案。

→ 禁止静默删关键图；先重组上游资产或Segment。

### `REFERENCE_REDUNDANCY`
同一字段已经有更直接Primary，另一个Reference没有新增任何必要字段。

→ 删除真正重复项，但不影响其他Critical Field。

---

## 7｜一句话

> **Reference Resolver的目标不是“图片越少越好”，而是“关键资产全覆盖 + 无意义图不占位”；生成Prompt不展示内部资产名。**


## Current Rule｜Functional Minor Human Coverage（Current Rule）
当前Shot若存在匿名但功能明确的人物（路人、见证者、模糊孩子剪影、站台乘客等），必须把它们作为独立Coverage Field登记：`FUNCTIONAL_MINOR_HUMAN / SCOPED_BACKGROUND_WITNESS / ANONYMOUS_PASSERBY`等。只要其承担构图、氛围、因果或反应职责，就不能作为“自动背景杂项”省略。

### Identity Readability Coverage Rule

`CHARACTER_IDENTITY`的Coverage不能只看“Primary Visual里有人”。还必须检查该人物在目标平台有效缩放后的Identity Readability。若Primary Visual FAIL/UNKNOWN，则Field Coverage Map必须把该人物自己的Approved Identity Asset标为`DIRECT / MUST`；Storyboard与Environment不计入Identity覆盖。
