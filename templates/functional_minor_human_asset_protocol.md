# Functional Minor Human / Supporting Cast Visual Authority Protocol｜Current Authority

> **用途：** 所有清楚可见的配角、一次性功能人物在进入Storyboard/Video执行前，先拥有独立、可管理的人物视觉母图，避免视频模型现场发明画风、服装和体态。
>
> **最高原则：** `READABLE SUPPORTING / MINOR HUMAN → STANDALONE HUMAN MASTER BEFORE STAGE 04.`

## 1｜Visual Owner现在只有三类

- `EXISTING_CHARACTER_AUTHORITY`：命名/反复/需跨Scene识别的人物，走正式Character Canon；
- `FMH_ASSET`：一次性或轻量配角，但只要在画面里清楚可见，就必须建立独立`FUNCTIONAL_MINOR_HUMAN_ASSET / MINOR_HUMAN_MASTER`；
- `TEXT_ONLY`：仅限真正深背景、不可辨认、无独立动作/叙事/构图职责的人群存在。

`SHOT_ASSEMBLY`和`PREVIS_HUMAN_ANCHOR`不再是Appearance Owner：它们可以补组合关系、姿态、Contact和动作节点，但不能替代配角人物母图。

`VIDEO_MODEL_GUESS`永远不是Readable Human合法Owner。

## 2｜Human Visual Need Test

满足任一项就视为`READABLE`，必须有独立人物母图：
1. 当前Beat的叙事主体、动作因果主体、情绪见证主体；
2. 中景/近景/清楚全身/明确背影或侧影；
3. 与主角发生对话、递交、接触、追逐、战斗、引导；
4. 服装、年龄、体态、职业轮廓会影响可信度；
5. 后续Shot需要确认还是同一个人；
6. 项目画风一致性不能可靠靠纯文字维持。

只有上述均不成立、且人物不可辨认时，才允许`TEXT_ONLY`。

## 3｜一次性人物也先做一张母图

一次性护士、售票员、保安、路人见证者、临时工作人员等，只要清楚可见：

`SCOPED_CAST_BRIEF → FMH_ASSET → QC → USER APPROVAL → BASE VISUAL AUTHORITY FROZEN`

最小人物母图锁：
- Function / Narrative Role；
- Age / Body / Gender Read（必要时）；
- Wardrobe /职业识别；
- Hair / Head Silhouette；
- 项目统一画风；
- Scoped Identity Boundary。

它是独立人物图，不包含最终场景，不承担最终Blocking。

## 4｜什么时候升级多视角

一张母图是Base Authority，不代表永远够：
- 只出现一次、单一方向可读 → 一张FMH Master即可；
- 跨多个Shot、反打、背面、动作连续性明显 → 升级`MINOR_HUMAN_CANON_VIEW_SET`；
- 后续跨Scene反复出现、具名、身份重要 → Promotion到正式Character Canon。

`MINOR_HUMAN_CANON_VIEW_SET`默认最小候选：`FRONT_OR_3Q / REVERSE_OR_3Q / BODY_SILHOUETTE`，实际按摄影需求补，不机械六视图。

## 5｜群众

- Featured Individual / 可读群众个体 → 视为Minor Human，必须人物母图；
- 普通Crowd → `CROWD_ARCHETYPE_SET`，锁少量群体原型；
- Deep Background Mass → Cluster / Density / Flow，可TEXT_ONLY。

不要求给每一个不可识别群众建立独立人物母图。

## 6｜Storyboard / Previs边界

白描Contact Sheet和Clean Panel只画匿名几何人形。它们负责：
- Blocking；
- Camera / Shot Relation；
- Pose / Action Beat；
- World Position / Screen Projection；
- Entity Slot H_A/H_B/H_C。

它们绝不负责建立配角最终脸、发型、服装或画风。

Rendered Human Pose Anchor可以补复杂姿态，但其身份和Look必须继承已经Approved的FMH/Character Master。

## 7｜Stage 03 Freeze

每一个Stage 02被判为Readable的Scoped Cast都必须在`BASE_VISUAL_AUTHORITY_MANIFEST`中登记：
- stable `entity_id`；
- `reuse_key`；
- `obligation_id=FUNCTIONAL_MINOR_HUMAN_MASTER`；
- `human_master_asset_id`；
- Scope / Promotion State。

Stage 03未生成、未QC、未用户批准 → `FUNCTIONAL_MINOR_HUMAN_MASTER_ASSET_MISSING` / `HUMAN_VISUAL_AUTHORITY_GAP` → 不允许进入Stage 04。

## 8｜Fail

- `HUMAN_VISUAL_AUTHORITY_GAP`
- `FUNCTIONAL_MINOR_HUMAN_MASTER_ASSET_MISSING`
- `READABLE_MINOR_HUMAN_OWNER_MUST_BE_FMH_ASSET`
- `FUNCTIONAL_MINOR_IDENTITY_CONTAMINATION`
- `FUNCTIONAL_MINOR_PLACEMENT_DRIFT`
- `HUMAN_STYLE_FAMILY_DRIFT`
- `BASE_VISUAL_DUPLICATE_ENTITY_REQUIREMENT`
