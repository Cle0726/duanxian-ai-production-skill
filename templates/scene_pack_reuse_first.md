# Scene Pack + Reuse First（场景包 + 资产优先复用）｜Current Authority

> **用途：** `EPISODE ASSET FROZEN`后维护Scene级候选调用索引，减少重复检索。Scene Pack**不是最终Reference Pack**，更不是“每段固定上传清单”。

## 1｜Reuse First

先判断：
1. 是否已有APPROVED资产可复用；
2. 当前变化是否只是角度、动作、短期湿水/开合/污损；
3. Environment / Prop当前Shot是否已有匹配Derived Coverage；
4. 只有真正的新身份、新长期造型、新地点、新道具、持久结构变化或真实Coverage Gap才回Stage 03建立新正式资产。

## 2｜Scene Runtime Pack

一个Scene可维护候选资产索引：

```text
SCENE_RUNTIME_PACK｜S04
Style DNA：TEXT AUTHORITY
Color / Lighting：<当前阶段>
Environment Authorities：<Canon Master + 已批准Coverage索引>
Characters：<当前Scene可能出现的Approved Character Authorities>
Scoped Figures / FMH：<当前Scene范围内Approved Scoped Figure Authorities>
Common Props：<Approved Canon/Coverage索引>
```

它回答“这个Scene有哪些可用Authority”，**不回答“当前Segment到底@哪些图”。**

## 3｜Segment Resolve

具体Segment必须执行：

`Scene Runtime Pack + World State Delta + Segment Delta → Task Contract → Key Visible Asset Register / Field Coverage → Eligibility Test → Entry Mode → Storyboard Control → Minimum Sufficient Reference Pack`

因此：
- 本Segment不入镜的人物从Pack中OMIT；
- 当前Camera已有Environment Coverage时优先Coverage；
- 当前Prop可见面已有Coverage时优先Coverage；
- Render/Cinematic Style图像仍按当前Segment职责选择；**Color单独受`color_authority_preservation_gate.md`约束**：当前Scope已有Approved Scene Color Card时，Scene-bound Image / Shot Execution继续视觉绑定；Final Video默认保留Authority血缘而不重复占色卡槽，只有明确综合色风险Trigger才Direct Reference。没有Scene Card但存在Scene-matched Global Color Card且当前Scene明确继承该Baseline时，可作为上游综合色基准；不得机械叠加Global + Scene；
- Approved FMH属于Scene/Shot Group范围Appearance候选；只有当前Segment需要该匿名功能人物时才进入最终Reference Pack，超Scope不得复用；
- Approved Shot Assembly属于Scene级候选关系资产，只有当前Segment确实需要多人/人景物组装关系时才进入最终Reference Pack；
- Approved Storyboard是Stage 05 Control Source，不是Scene基础固定输入；
- Previous Ending Frame只由Entry Mode决定，**不得在Segment Delta里机械 `+ Ending Frame`**。

## 4｜Segment Delta只描述变化

```text
SEGXX Delta
+ Character B进入画面
- Character C离画
+ Prop A从桌面转为Character B左手持有
Environment Runtime：门已打开
Crowd Flow：入口区域密度下降
```

Delta不负责直接指定图片输入；Reference Resolver根据这些变化选择最直接Authority。

## 5｜Cache失效

发生以下情况重新Resolve：
- Approved资产Version变化；
- Scene子空间改变；
- Persistent State改变；
- Change Impact = REVIEW / STALE；
- 新的Derived Coverage / Production Support / Shot Assembly被批准并Re-Freeze。

普通CUT、景别变化、短期Prop状态变化不重建整个Scene Pack。

## 6｜Freeze规则

Scene Pack发现冻结池缺少真正必要的正式资产时：
- 标`EPISODE ASSET FREEZE BROKEN`；
- 若只是当前Shot缺少必要场景/道具结构面，同时标`ASSET_COVERAGE_GAP`；
- 若需要的Stage 03 Production Support缺失，标`VIDEO_RISK_REFERENCE_GAP`并`FREEZE BROKEN(reason=support-reference)`；
- 若需要的清楚配角/功能性小人物缺`SCOPED_CAST_BRIEF`或Approved FMH/Minor Human Master，标`FUNCTIONAL_MINOR_HUMAN_GAP`并`FREEZE BROKEN(reason=functional-minor-human)`；Stage 04 Previs/Assembly不能替代这张人物母图；
- 若人物/场景/道具已有Authority但Required Shot Assembly缺失，标`SHOT_ASSEMBLY_GAP`并`FREEZE BROKEN(reason=shot-assembly)`；
- 回Stage 03只补对应缺口，不重做无关Master；
- APPROVED后更新Asset Pack并重新`EPISODE ASSET FROZEN`；
- 再继续Stage 04/05。

不得用Storyboard或Video Prompt临时发明正式结构绕过Freeze。

## 7｜目标

**Reuse缓存负责效率；Task-Bound Resolver负责当前正确性。**


## V4.5.7 Base Authority Override

旧项目中的`SHOT_ASSEMBLY / PREVIS_HUMAN_ANCHOR`不再可作为、共同承担或替代Readable Scoped Cast的Appearance Owner。清楚可见的一次性/配角人物必须补一张Approved FMH/Minor Human Master；正式使用的Environment/Sub-location必须补一张Approved空场景Clean Master。只有深背景不可辨认群众允许TEXT_ONLY。该规则优先于本文旧轻量兼容说明。
