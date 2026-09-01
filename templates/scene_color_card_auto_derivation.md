# Scene Color Card Auto Derivation｜V4.5.7

> **用户生产规则：** 一个Approved基础色卡作为项目综合色根。进入新场景或新的Interior/Exterior Look Domain时，Controller自行派生并生成对应Scene Color Card；之后该场景的图片持续直接继承/绑定这张色卡，Video持续保留其Authority血缘，但Direct Reference按最小充分Reference Budget动态决定。

## 1｜自动触发

满足任一条件且当前Scope没有Approved Scene Color Card时，自动创建`SCENE_COLOR_EXTENSION_CARD` Generation Job：
- `scene_id`切换到新场景；
- 同一Location从`EXTERIOR_LOOK ↔ INTERIOR_LOOK`切换；
- 日夜/季节/长期材质环境发生足以形成新Look Domain的持久变化；
- 用户明确要求该Scene另有综合色身份。

同一场景的普通Shot Lighting变化不重复新建Scene Card；临时雷光、火光、灯灭等仍作为Shot Lighting Variant。

## 2｜派生来源

Scene Card必须以Approved `GLOBAL_COLOR_CARD / BASE_COLOR_CARD`为Parent，继承Color DNA的综合色组织关系，只派生当前场景需要变化的：环境基底、材质综合色、主辅光冷暖、综合色密度、局部Accent、肤色保护关系。

`derivation_kind = SCENE_COLOR_FROM_BASE`

不得复制基础色卡中的示例人物、示例空间、排版或色块布局为场景内容。

## 3｜自动生成顺序

`Detect Scene Scope → Derive Scene Color Spec → Create Color Generation Job → @Base Color Card / Native Bind → Generate Scene Color Card → Candidate QC → Approval → Register Scene Color Authority → Release dependent image jobs`

场景母图、Coverage、Assembly、Storyboard执行图、Shot Execution Frame在该Scene Card批准之前不得跳过综合色依赖。

## 4｜持续绑定

一旦Scene Card Approved：
- 当前场景所有Scene-bound图片生成：`MUST_BIND_COLOR_AUTHORITY = Scene Card`；
- 当前场景所有Shot Execution Frame：继续绑定同一Scene Card；
- 当前场景Video Job：必须记录同一`scene_color_authority_id`，并检查Primary Visual确实继承该综合色Authority；默认`projection_mode = LINEAGE_ONLY`，不机械追加色卡视觉Reference；
- 当出现`COLOR_DRIFT_OBSERVED / COLOR_NARRATIVE_CRITICAL / MULTISHOT_COLOR_DRIFT_RISK / PRIMARY_VISUAL_COLOR_UNRELIABLE / PROVIDER_DIRECT_COLOR_REQUIRED / USER_REQUIRED`等明确Trigger时，才升级`DIRECT_COLOR_REFERENCE`；槽位压力或Provider不支持Direct Color时可用`TEXT_COLOR_CONTROL`；
- Named Mention平台：图片Direct Color任务始终使用真实`@对应场景色卡`；Video只有`DIRECT_COLOR_REFERENCE`模式才输出该@；Tool-native平台保持同一语义。

## 5｜禁止

- 换场景后继续机械使用上一场景Scene Card；
- 只有文字Scene Spec却把已存在的Scene Card静默省略；
- Video阶段因为不直绑色卡就丢失`scene_color_authority_id`或让Primary Visual与Scene Color Authority血缘不一致；
- 同时把Global + Scene +多个Lighting Card全塞入Prompt求保险；Scene Card生效后Global默认退到Parent Authority。
