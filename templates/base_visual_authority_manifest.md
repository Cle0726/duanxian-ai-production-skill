# Base Visual Authority Manifest｜基础视觉资产管理｜V4.5.7

> **最高原则：** 不因“一次性”而让视频模型临场发明清楚可见的人或正式场景。图片资产数量不是优化目标；**可管理、可复用、可追溯、可冻结**才是目标。

## 1｜两类不可省略的基础母图

### A. Empty Environment Master
任何被Formal Scene / Event Node / Formal Shot实际使用的真实场景或子空间，`Tier S/A/B/C`一律先建立一张**空场景Clean Master**：
- 无可读人物；
- 无临时动作；
- 无一次性剧情状态污染；
- 锁空间身份、材质、综合色、固定家具/结构、基础主光；
- `population_policy=EMPTY_ENVIRONMENT_ONLY`；
- `transient_content_policy=CLEAN_CANON`。

Tier C只豁免复杂Floor Plan/多视角，不豁免这张空场景母图。

### B. Functional Minor Human Master
任何清楚可见、承担构图/动作/因果/见证/对话职责的配角或一次性功能人物，即使只出现一次，也必须先建立一张独立人物母图：
- `asset_type=FUNCTIONAL_MINOR_HUMAN_ASSET`或`MINOR_HUMAN_MASTER`；
- 单人、单帧、干净背景；
- 锁项目画风、年龄/体态、发型轮廓、服装、必要职业识别；
- 不烘焙最终场景站位；
- `subject_entity_id`必须绑定真实人物Entity ID。

真正不可辨认的深背景群众才允许`TEXT_ONLY`；群众总体继续使用`CROWD_ARCHETYPE_SET`，不逐个建母图。

## 2｜Storyboard / Assembly不能替代基础母图

- 匿名白描：只证明Blocking / Camera / Action / Beat；绝不拥有最终人物外观或场景美术Authority。
- Shot Assembly：只证明多人、人景物、Contact、当前Shot组装；不能替代人物母图或空场景母图。
- Rendered Previs/Human Pose Anchor：可补当前姿势/表演/动作节点，但不能成为、共同承担或替代一次性人物Appearance Owner。

## 2.5｜Actor Authority Index（防漏配角）

所有`SPATIAL_CANON.event_nodes.actor_ids`必须进入`actor_authority_index`并分类：
- `CHARACTER_CANON → CHARACTER_AUTHORITY`；
- `MINOR_HUMAN → FMH_ASSET`；
- `CROWD_CLUSTER → CROWD_ARCHETYPE_SET / TEXT_ONLY(仅深背景)`。

这样即使一个配角只出现一个Shot，也不能因为“只出现一次”从资产计划中漏掉。

## 3｜资产多时怎么管理

每一个基础资产都进入`BASE_VISUAL_AUTHORITY_MANIFEST + ASSET_REGISTRY`，按稳定Entity而不是按Shot命名：
- `ENVBASE_<location_entity_id>`：一个Location/Version一个Active空场景母图；
- `FMHBASE_<entity_id>`：一个清楚配角/Scope一个Active人物母图；
- `reuse_key`用于跨Shot/同Scene复用；同一个Entity不得因为换镜头重复建母图；
- 真正设计变化才升Version；镜头角度变化走Coverage/View Set，不复制Master；
- 后续若一次性配角变成反复角色，Promotion到`MINOR_HUMAN_CANON_VIEW_SET`或正式Character Canon，旧母图保留Lineage，不重新随机发明身份。

## 4｜Freeze硬门

Stage 03 Freeze前必须满足：
1. 每个`SPATIAL_CANON.event_node.location_entity_id`都有对应Empty Environment Master；
2. 每个Readable Minor Human都有Functional Minor Human Master；
3. 对应`VISUAL_ASSET_OBLIGATION`均为`FULFILLED + proof_status=PASS`；
4. Manifest没有重复Entity Requirement / reuse_key冲突；
5. Master均为Approved且Entity/Location绑定一致。

Fail：
- `EMPTY_ENVIRONMENT_MASTER_REQUIREMENT_MISSING`
- `EMPTY_ENVIRONMENT_MASTER_CONTAINS_HUMAN`
- `FUNCTIONAL_MINOR_HUMAN_MASTER_ASSET_MISSING`
- `READABLE_MINOR_HUMAN_OWNER_MUST_BE_FMH_ASSET`
- `BASE_VISUAL_DUPLICATE_ENTITY_REQUIREMENT`
- `BASE_VISUAL_REUSE_KEY_COLLISION`
