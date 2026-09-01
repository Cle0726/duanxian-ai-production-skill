# Reference Role & Fidelity Isolation（参考职责与保真隔离）｜Current Authority

> **核心原则：** `Control Reference ≠ Fidelity Source`，但`Control Reference`完全可以是直接Video输入。职责隔离用于防止Reference越权，不用于禁止视觉控制。

## V4.4｜Primary Conditioning层

Reference职责新增一层：`VIDEO_CONDITIONING_IMAGE`。它不取代Identity/Color/Style/Storyboard各自Authority，而是拥有“当前Video Unit最终静态入口画面”的Primary Visual职责。

- Control Reference可以直接上传；
- Fidelity Source可以直接上传；
- 但两者的组合不能自动等价于`VIDEO_CONDITIONING_IMAGE`；
- Whole Storyboard / Design Board / Color Board不得未经Promotion成为Primary Visual；
- Approved Conditioning Frame存在后，其他Reference仍按字段继续Support，不因Primary Frame存在而整包删除。

## 1｜Reference类型
- `HD_OBJECT_AUTHORITY_IMAGE`：Character / Environment / Prop / Detail；
- `HD_PRODUCTION_SUPPORT_IMAGE`：Interaction / Contact / Transient State；
- `HD_PERFORMANCE_SUPPORT_IMAGE`：Expression / Action Pose / Contact Pose；只锁表演静态形态，不拥有Identity/Timing；
- `HD_NARRATIVE_FX_IMAGE`：剧情型FX的形态/状态/静态环境交互；不拥有完整时间曲线；
- `HD_SHOT_ASSEMBLY_IMAGE`：多人、人景物组合、空间占位、Contact；人物Appearance必须来自Character/FMH Base Authority；
- `CONTROL_IMAGE / CONTROL_CROP`：Color / Style / Storyboard / Ending Frame / Camera or composition evidence；
- `TEXT_CONTROL`：视觉Reference无法表达或平台不支持视觉输入的字段。

## 2｜Most Direct Field Owner
每个关键字段只有一个Primary Owner；其他Reference只能Support：
- Identity/Human Appearance → 仅由Character/FMH Base Authority承担；Shot Assembly/Previs Human Anchor只能补Relation/Placement/Pose/Contact，不能承担、共享或替代Appearance Authority；
- Environment Geometry → Environment/Coverage；
- Prop Structure → Prop Authority；
- Color → current Scene Color Authority；
- Render Style →最直接Approved Visual Style Evidence；
- Shot Composition/Blocking/Shot-Cut Sequence → Approved Mandatory Shot Storyboard；
- Supplemental Camera Path/Spatial/Contact Proof → 对应Supplemental Previs；
- Performance Expression/Pose/Contact → Approved Performance Support（适用时）；
- Narrative FX Shape/State → Approved Narrative FX Reference（适用时）；
- Continuity →真实Previous Ending/First Frame。

综合色卡不能重设计人脸；Style Board示例人物不能变成当前角色；Storyboard不能覆盖Character Canon。`CLEAN_STRUCTURAL_STORYBOARD`默认只拥有Shot/Composition/Blocking/Temporal/Cut字段，不拥有最终Render Style、Color、Face Identity或对象细节。这是**字段边界**，不是“不能上传”。

## 3｜Storyboard visual use
Stage 05先确认Approved Mandatory Shot Storyboard覆盖全部Shot，再读取Supplemental Previs；随后，按`MODEL REFERENCE CAPABILITY PROFILE`选择：
- Whole Board direct；
- Panel multi-reference；
- Key Panel selection；
- First/Last frame；
- Clean crop/Anchor fallback。

不再默认“整张宫格不得上传”。

## 4｜Color / Style visual use
- Color Card可直接作为Color Reference；
- Style Board可直接作为Style Reference；
- 是否改变Direct路线只看当前Capability与可核对的Literalization/Content Bleed/槽位/Role Separation证据；Crop优先于生成式Applied，不能用主观“风险/保险”直接制造中间资产。

## 5｜Fidelity Firewall
Control Reference通常不自动控制：最终锐度、对象细节密度、身份结构。高清对象结构仍由Most Direct Object Authority负责。

Final Video若有前景人物，人物与环境必须属于同一绘画系统和同一光照/空间关系；不能把人物像贴纸贴上去。

## 6｜Model-facing projection
内部Role表不打印。平台需要Token时只使用真实Token + 最短职责句；其余字段直接消解到动作/空间/综合色/风格/连续性。

## 7｜Fail
- `REFERENCE_FIDELITY_FAIL`
- `REFERENCE_ROLE_SCOPE_VIOLATION`
- `REFERENCE_OWNER_CONFLICT`
- `REFERENCE_SLOT_OVERFLOW`
- `ENVIRONMENT_INTEGRATION_MISS`
