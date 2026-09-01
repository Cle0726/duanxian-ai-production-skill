# Performance Asset Requirement Engine（表演资产需求引擎）

> **Owner：Stage 02需求判定 → Stage 03静态表演Support生产。** 本引擎吸收旧资产圣经中“表情表 / 动作姿态页先于镜头合成”的稳健思想，但不恢复机械六表情、六动作或固定页数。

## 1｜为什么需要单独判定

人物Base Master回答“这个人是谁、长什么样”；白描Storyboard回答“站哪里、什么时候、动作阶段是什么”。二者都不能稳定解决所有**表演形态**问题。

当某个正式Shot的叙事价值高度依赖特殊表情、身体姿态、手势、持握或复杂接触，而且这些问题能够用廉价高清静态图提前消除时，Stage 02必须产生`PERFORMANCE_ASSET_REQUIREMENT_SET`。

## 2｜Authority边界

Performance Support可以拥有：

- `EXPRESSION_SHAPE`：当前情绪下眉眼、嘴角、呼吸状态等可见表演形态；
- `ACTION_POSE_SHAPE`：关键身体重心、肢体折叠、朝向、手势、持握姿态；
- `CONTACT_POSE_SHAPE`：扶抱、递交、压迫、接住、拖拽等关键静态接触关系。

Performance Support**不能拥有**：

- 人物Identity / Face Canon / Hair Canon / Wardrobe Canon；
- Environment Geography；
- Prop结构Canon；
- Camera Motion、速度曲线、完整动作Timing；
- Storyboard Beat顺序。

它必须继承Approved Character Authority或Approved FMH/Minor Human Master。

## 3｜需求类型

- `NONE`：Base Master + Storyboard + Text已足够唯一执行；
- `EXPRESSION_SUPPORT`：特殊/微妙表情是镜头核心信息；
- `ACTION_POSE_SUPPORT`：非中性、容易猜错的身体姿态或持握方式；
- `CONTACT_POSE_SUPPORT`：多人/人-物复杂接触需要高清静态证据；
- `PERFORMANCE_SUPPORT_PACK`：同一人物/Shot Group同时需要表情与姿态/Contact支持。

## 4｜触发条件

典型触发：

- `EXPRESSION_IS_STORY_PAYLOAD`：观众必须从表情读到剧情转折；
- `MICRO_EXPRESSION_CRITICAL`：压抑、认命、怀疑、失声恐慌等不能用通用“惊讶脸”替代；
- `NON_NEUTRAL_POSE`：蹲下平视、扶墙、收紧围巾、异常身体停顿等；
- `COMPLEX_BODY_MECHANICS`：重心、关节、身体扭转容易随机；
- `CONTACT_RELATION`：两人或人-物接触位置重要；
- `PROP_HANDLING`：关键持握/操作方式必须清楚；
- `REPEATED_PERFORMANCE_SHAPE`：同一表演形态在多个Shot复用。

以下不触发静态Support：

- 普通站立/行走/自然说话；
- 单纯动作速度、节奏、惯性、Camera Motion；
- 只有Storyboard Blocking变化、没有额外静态歧义。

## 5｜Stage 03资产类型

- `PERFORMANCE_EXPRESSION_SUPPORT`
- `PERFORMANCE_ACTION_POSE_SUPPORT`
- `PERFORMANCE_CONTACT_POSE_SUPPORT`

推荐默认生成**单帧高清Support**，因为更利于后续Shot Assembly / Execution Frame继承。若为内部资产管理建立多格表情/姿态页可以使用`MULTI_PANEL`，但它不得直接作为Video Primary Visual；若要直接进入Video Reference Pack，优先派生当前Shot单帧Support或让Shot Execution Frame吸收。

## 6｜白描与Performance Support的关系

白描仍然必须先/后按Stage流程完成其Blocking职责：

- 白描：`Blocking / Camera / Action Beat / Timing`；
- Performance Support：`Expression / Pose / Contact static shape`；
- Character/FMH Master：`Identity / Appearance`。

三者不能互相越权。

## 7｜生产与Freeze

Stage 02先生成Requirement；Stage 03在其Parent Character/FMH Authority Approved后生产Support。Freeze前所有非`NONE`且状态为Required的Requirement必须：

- 有对应Approved Support Asset；
- `subject_entity_id`精确匹配人物；
- `media_kind=IMAGE`；
- `authority_role=PERFORMANCE_SUPPORT_AUTHORITY`；
- 不把Support提升成Primary Visual；
- 若是多格页且`direct_input_allowed=true`，必须先拆/派生单帧，避免多Panel语义污染。

失败码：

- `PERFORMANCE_SUPPORT_REQUIRED_MISSING`
- `PERFORMANCE_SUPPORT_ENTITY_MISMATCH`
- `PERFORMANCE_SUPPORT_TYPE_MISMATCH`
- `PERFORMANCE_SUPPORT_AUTHORITY_ROLE_FAIL`
- `PERFORMANCE_SUPPORT_MEDIA_KIND_FAIL`
- `PERFORMANCE_MULTIPANEL_DIRECT_REFERENCE_FORBIDDEN`

## 8｜Stage 05 Reference选择

Performance Support进入完整Asset Library后，是否真正`@`到当前Video Job仍由Reference Resolver决定：

- Shot Execution Frame已经高质量吸收该表演形态 → 可`LINEAGE_ONLY`；
- 当前Primary Visual中表情/姿态仍不清楚或是高风险字段 → 可选对应单帧Performance Support直接Reference；
- 不得为了“资产已经做了”就把所有Performance Support全部上传。
