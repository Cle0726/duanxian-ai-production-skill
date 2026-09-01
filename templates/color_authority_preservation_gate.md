# Color Authority Preservation Gate（综合色视觉权威保全）｜Current Authority

> **核心原则：** `APPROVED COLOR AUTHORITY IN SCOPE → PRESERVE IT VISUALLY WHEN USEFUL.`
>
> **Current Rule：** 综合色卡本身是综合色Authority，但**Authority存在 ≠ Final Video必须再次Direct Bind**。Scene-bound Image / Shot Execution优先Direct Bind以烘焙综合色；Final Video默认从已正确综合色的Primary Visual继承，只有明确风险Trigger才额外Direct Bind色卡。Applied Reference仍仅在显式证据触发时按需生成。具体路由读取`visual_reference_routing.md`。

## 1｜何时需要综合色视觉Authority

场景绑定型任务（Environment、Assembly、FMH/一次性人物、Previs、Video、Revision）若已有Approved Scene Color Authority，默认保留它；纯Character Identity Master、纯结构Prop Master或Tiny Local Patch可按Scope不绑定Scene综合色。

V4.5.7项目规则：一个Approved基础色卡作为综合色根；进入新Scene或新Interior/Exterior Look Domain且没有对应Approved Scene Card时，自动执行`Base Color Card → Scene Color Spec → Scene Color Card Generation Job`。这不是Applied Reference预生成。Scene Card批准后，该场景所有Scene-bound图片与Shot Execution持续Direct Bind；Video持续携带同一Authority血缘，但Direct Reference按最小充分集合动态决定。

## 2｜SCENE COLOR AUTHORITY SCAN

```text
Task: ...
Scene Scope: ...
Approved Color Authority: <visual / none>
Color Sensitivity: HIGH / MEDIUM / LOW
Visual Binding Useful: YES / NO
Target Model Reference Capability: ...
Chosen Color Route: LINEAGE_ONLY / TEXT_CONTROL / DIRECT_REFERENCE / DEDICATED_COLOR_CHANNEL / APPLIED_REFERENCE
Role Scope: COLOR + VALUE + LIGHT RELATIONSHIP ONLY
Status: PASS / COLOR_AUTHORITY_GAP
```

## 3｜Visual First, Route Second

如果综合色对当前Shot重要并且平台支持视觉Reference：
- **优先使用最直接的Approved综合色视觉证据；**
- 色卡/综合色Crop可以直接作为Color Reference；
- Prompt只需最短职责锁，不要把综合色卡全文翻译成一大段颜色文字；
- 对Scene-bound Image / Shot Execution，只要Approved Scene Color Card仍是Primary Color Owner，就不能因为“场景图看起来已经有颜色”而静默省掉色卡；**对Final Video则相反：先验证Primary Visual确实继承同一Color Authority，满足时默认LINEAGE_ONLY，不重复占槽。**

只有以下情况才升级为`SCENE_COLOR_APPLIED_REFERENCE / COLOR_GRADE_ANCHOR`：
- 当前目标模型已出现色块/版式直译；
- `ROLE_SEPARATION=VERIFIED_FAIL`且已有无生成式Color-Only Crop / Dedicated Channel仍无法安全隔离所需综合色字段；
- Reference槽位有限，Applied Reference能同时承担环境+综合色并减少冲突；
- 用户/平台工作流明确要求这种执行Reference。

**Applied Reference是工具，不是仪式。**



## V4.5.7｜Scene Color Binding Hard Boundary

- Scene-bound Image Generation：当前Scene Card是`MUST_BIND_COLOR_AUTHORITY`。
- Shot Execution Frame：即使父母图已经综合色正确，也继续绑定当前Scene Card，把最终综合色烘焙进Primary Visual。
- Final Video：`scene_color_authority_id`仍是Hard Requirement，但**Direct Color Reference不是默认Hard Requirement**。默认`LINEAGE_ONLY`；有明确综合色风险Trigger才`DIRECT_REFERENCE`；需要文字强化时可`TEXT_CONTROL`。
- Named Asset平台：图片Prompt必须出现真实`@对应场景色卡`；Video Prompt只有`DIRECT_REFERENCE`模式出现该@。
- Scene-independent Character/Prop/Transformation Master没有Scene Scope时绑定Approved Base/Global Color Card。

失败：`SCENE_COLOR_AUTHORITY_GAP / SCENE_COLOR_BINDING_MISSING / VIDEO_COLOR_BINDING_MISSING / VIDEO_COLOR_REFERENCE_MODE_CONFLICT`。

## Current｜NO PREEMPTIVE APPLIED REFERENCE

`SCENE_COLOR_APPLIED_REFERENCE / COLOR_GRADE_ANCHOR`不得作为Episode Pack或Stage 03的预防性常规资产提前生产。

- Approved Color Card已经存在 → 保留其Authority；Scene-bound Image / Shot Execution无Direct Fail证据时继续Direct；Final Video若Primary Visual已正确继承则默认LINEAGE_ONLY；
- Target Platform/Model仍UNKNOWN → **不因为UNKNOWN强占Video色卡槽，也不生成Applied Reference**；先使用Primary Visual + Authority Lineage，若实测综合色漂移再升级；
- 只有`visual_reference_routing.md`产生有效`APPLIED_REFERENCE_TRIGGER`后，才允许创建Applied Reference Job；
- “怕模型把色块画进去 / 为了保险 / 非剧情参考 / 以前规则要求”均不是合法Trigger。

失败：`PREEMPTIVE_APPLIED_REFERENCE / LEGACY_COLOR_ISOLATION_RULE_REVIVAL`。

## 4｜Color Field Boundary

综合色Reference只控制：
- 色族关系、冷暖分布；
- Chroma concentration / selective saturation；
- Contrast / value hierarchy；
- 环境光色与材质综合色关系。

它不覆盖Character Identity、服装设计、Environment Geometry、Storyboard Camera/Blocking或对象结构。

## 5｜Revision / Rebuild

如果母图内容正确但综合色漂移：直接把Approved综合色Authority作为独立视觉控制即可；不要因为已有母图就假设综合色自然继承，也不要为了综合色强制再造一张Applied Reference。

## 6｜Text Fallback

对Scene-bound Image / Shot Execution，仅当平台没有视觉Reference能力或用户明确选择文字控制时才走Text Fallback。对Final Video，`TEXT_CONTROL`还可在Reference Slot Pressure、Provider不适合Direct Color或Direct颜色图收益低于更关键Identity/Geometry/Continuity Reference时合法使用；它仍必须读取当前Scene Color Authority，不能改写综合色事实。

## 7｜Fail

- `COLOR_AUTHORITY_REUSE_MISS`：已有关键综合色Authority却无理由丢失；
- `COLOR_ROLE_SCOPE_VIOLATION`：色卡越权控制身份/几何/构图；
- `COLOR_REFERENCE_ROUTING_FAIL`：当前平台/历史证据表明Direct Route不稳定却仍沿用；
- `COLOR_REFERENCE_LITERALIZATION_LEAK`：成片真实出现色块/版式污染。

不存在“raw色卡只要直接绑定就自动FAIL”的规则。
