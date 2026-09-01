# Episode Asset Pack First（当集资产包优先）

> **用途：** 正式Production Mode中，Stage 02完成整集导演拆解后，先把本集真正会用到的正式生产资产（空间规划、视觉、综合色、声音身份等）生成/建立、QC、批准并登记；在整集资产冻结前，不进入正式Storyboard生产。

## 核心原则

**先定空间事实，再定视觉资产，再拍分镜，再生成视频。**

正式顺序固定为：

**Stage 02 Director/Shot Relation Planning → Relation Planning Validation → Stage 03A Spatial Canon Build/QC/Approval → Stage 03B Clean Canon + Entity/Event/Relation-driven Visual Asset Build → Asset Consolidation & Sufficiency Audit → Final Episode Asset Requirement Manifest闭环 → Director Spatial Reconciliation → Episode Asset Freeze → Stage 04 Clean Storyboard → Video Conditioning Build/QC/Approval → Stage 05 Video。**

这不是新增Stage。`Episode Asset Freeze Gate`只是Stage 03结束前的生产闸门。

**旧项目迁移例外：** 如果Episode已经用旧版Skill进入Stage 04/05，不要求为了满足本规则把既有成果全部退回Stage 03重做。应读取`existing_project_migration.md`，用现有有效APPROVED资产执行Retroactive Episode Asset Freeze，只补当前后续生产真正缺失的正式资产。

## V4.5.2｜Justified Asset Generation + Cascade Approval

正式资产不是“可能以后有用”的图片收藏。进入Asset Queue前必须记录：
- `WHY_REQUIRED`：为什么现在必须存在；
- `REQUIRED_BY`：Event / Shot / Relation / Continuity / Reuse Requirement；
- `SOURCE_REQUIREMENT_REFS`：上游证据；
- `DOWNSTREAM_USE`：Storyboard / Conditioning / Video / Recurring Set等；
- `Spatial Parent / Visual Parent`（Coverage适用时）。

缺少上述理由的资产默认不进入正式生成队列。

Stage 03采用Cascade Approval：
`Spatial Diagram/Canon → Clean Canon/Key Event View → Coverage → Look → Voice → Final Asset Freeze`。
上游未批准时不得批量生成依赖下游；结构错误优先在最便宜层修正。

## Episode Asset Pack包含什么

只收录剧情/导演/空间关系已经证明“本集确实会使用”的正式可复用生产资产或严格限定Scope资产，包括：

- Character Asset Requirement Set：本集**反复/命名/后续需要识别连续性**的人物不再只用笼统“Character Master”判断完成。读取`character_asset_requirement_set.md`：主要/反复/可变身人物默认锁`DV-01 + DF-02 + HA-01`，再按真实Shot决定`DF-01 / AD-01 / PR-01`是否Required；同时登记Character Fashion DNA Ref、Character Closet Ref、Adornment Identity与本集Approved LOOK ID。一次性Montage/功能人物若Stage 02标记`SCOPED_CAST / NON_RECURRING`，不强制建立主角级Character Requirement Set；**只要清楚可见就必须Stage 03生成最小FMH人物母图**，TEXT_ONLY仅限真正深背景；Shot Assembly / Previs只能补关系与动作，不能替代Appearance Master；
- Functional Minor Human / Scoped Cast：Stage 02对承担构图/氛围/因果/视线引导/见证职责的一次性人物必须建立`SCOPED_CAST_BRIEF`；只要清楚可见，Visual Owner固定为`FMH_ASSET`并在Stage 03生成最小`FMH_<...>`、QC、用户批准为`APPROVED SCOPED FIGURE`。Shot Assembly / Previs仅作为补充关系/姿态证据。真正深背景无独立职责才允许TEXT_ONLY。不得让Video模型自由脑补；
- Spatial Canon + Environment Clean Canon + 必要Derived Coverage：本集重要/复用地点先锁Topology/Floor Plan/Zone/Door-Window/Sightline/Access，再生成一张正式Clean Hero Master；随后按Event Node、Shot和Shot Relation补最小Reverse / Side / Zone / Clue / Visibility / Location Identity等Coverage；
- Prop / Weapon Canon Master + 必要Derived Coverage：本集关键、反复出现、结构复杂或剧情因果相关道具/武器；先一张正式Hero Master，再按真实Shot需要补最小结构面/状态覆盖；
- Required Performance Support Asset：Stage 02 `PERFORMANCE_ASSET_REQUIREMENT_SET`判定特殊表情、动作姿态或复杂Contact存在静态可解风险时，Stage 03生成`PERFORMANCE_EXPRESSION_SUPPORT / PERFORMANCE_ACTION_POSE_SUPPORT / PERFORMANCE_CONTACT_POSE_SUPPORT`；它继承Character/FMH Identity，只拥有当前表演静态形态，不机械为每个人生产固定六表情/六动作；
- Required Narrative FX Asset：Stage 02 `NARRATIVE_FX_ASSET_MANIFEST`判定剧情型视觉现象需要稳定视觉语法时，Stage 03生成`NARRATIVE_FX_REFERENCE / NARRATIVE_FX_STATE_SHEET`；简单一次性FX保持`TEXT_GRAMMAR_ONLY`，禁止用Reference Video替代；
- Required Production Support Reference：Stage 02 `Video Risk-Driven Static Reference Matrix`证明可用廉价高清静态图显著降低昂贵Video风险的复杂交互/Contact/短暂高风险状态/Entity Action State；它是`APPROVED SUPPORT`，不是新Canon；
- Required Shot Assembly Asset：Stage 02 `Shot Assembly Need Analysis`证明当前集需要一张“人物+场景+道具+状态”的高清静态组装图来稳定多人关系、空间位置或Montage情境；它是`APPROVED ASSEMBLY`，不是Storyboard，也不是新Canon。任何清楚可见的一次性`SCOPED_CAST / NON_RECURRING`都必须先有Approved FMH/Minor Human Master，Assembly只负责继承外观并锁当前组合关系；
- Transformation Master Set：本集实际发生的已确认圣谱者变身所需正式资产；
- 必要Persistent State Variant：会持续跨多个镜头/Segment且结构明显变化的状态；
- 必要Scene Look / Color资产：默认区分`INTERIOR_LOOK / EXTERIOR_LOOK` Domain；每个Scene先有文字Spec，只有反复使用、差异显著、多镜漂移风险高或文字不足时才生成正式可复用Scene Color Extension Card；
- Required Voice Identity Asset：主要/反复角色若项目要求固定声音身份，Episode Asset Freeze前必须已有Approved Voice Master/Reference或明确登记合法例外；随机Video模型音色不能自动成为Canon；
- 必要Lighting Variant Reference：极少数持续跨大量Shot、文字控制反复漂移且已证明值得资产化的照明状态才加入；普通Shot Lighting Variant保持TEXT_CONTROL；
- 已有项目级APPROVED资产可直接引用，不重复生成或复制一份“本集版”。

## 明确不属于Episode Asset Pack

以下不是Stage 03前置资产：

- Storyboard Grid / 宫格分镜；
- 直接从Storyboard宫格放大、清稿或重画后冒充“Shot Assembly Asset”的伪资产；
- Storyboard Sheet / 故事版分镜；
- Previous-Segment Ending Frame / 上一段视频尾帧；
- Video Take；
- 无明确Video Risk Reduced的临时姿势图、测试图、未批准候选；
- 只为“多一张保险图”而产生、没有通过Production Support Reference资格测试的瞬间动作图；
- 轻微湿水、外套开合、少量灰尘、轻血迹等可由连续性和Prompt继承的短期状态。

**Storyboard属于Stage 04；Ending Frame属于Stage 05批准视频之后的连续性产物。**

## Episode Asset Accounting + Provisional Episode Asset Requirement Manifest（整集资产核算与最终需求清单）

Stage 02完成World State Continuity Audit、必要Transition Beat、Scene / Beat / Shot / Segment Plan，并为每个Segment完成`previsualization_strategy_router.md`的Shot Storyboard Coverage Contract + Supplemental Previs Planning及Raw Asset Analysis后，必须先读取`asset_consolidation_sufficiency_audit.md`完成跨Shot合并/复用/充分性检查，再汇总整集，而不是逐Segment边做边发现。Transition Audit新发现的**必要目的地外观 / 入口 / 停车区 / 连接空间 / 剧情关键门区**等正式空间也属于真实需求，必须在此时纳入：


**V4.5.2 Manifest时序：** Stage 02C只能产出`PROVISIONAL_EPISODE_ASSET_MANIFEST`，因为新Location的Topology/Floor Plan/Sightline尚未被验证。`SPATIAL_CANON_LOCKED`后必须重新跑Relation/Asset Obligation Derivation与Consolidation，把空间验证新增/取消的Clue/Visibility/Identity/Event Coverage需求并入，之后才成立`FINAL_EPISODE_ASSET_MANIFEST_READY`并允许进入图片Asset Build。

```text
【Episode Asset Accounting｜<EPISODE_ID>】
Raw Demand Nodes：__
Existing Approved Reuse：__
Merged / Shared Across Shots：__ raw nodes → __ unique needs
Removed as Non-Static：__
Deferred Raw Demand Nodes to Stage 04：__
Stage 03 New Unique Assets To Build：__
Projected Stage 03 Freeze Static Asset Pool：__
Stage 04 Video Conditioning Plan：__
Projected Final Episode Static Asset Pool：__
By Class：...

【Final Episode Asset Requirement Manifest｜<EPISODE_ID>】

REUSE / 已有APPROVED：
- CHR_CHARACTER_A_CURRENT_MASTER｜v003
- ENV_SLEEPING_SAND_OLD_CITY_NIGHT｜v002

SPATIAL PLANNING / 空间规划与人物动线：
- TOPO_<LOCATION_GROUP>｜Type=OUTDOOR_TOPOLOGY｜Event Nodes=...｜Character Route=...｜Distance/Slope/Sightline=...｜Status=APPROVED
- FLOOR_<LOCATION>｜Type=BUILDING_FLOOR_PLAN / ROOM_LAYOUT｜Rooms/Zones=...｜Doors/Windows/Stairs=...｜Status=APPROVED
- ROUTE_<ACTOR_GROUP>｜Event Node Chain=...｜Location/Zone/Anchor Sequence=...｜Status=LOCKED

TO BUILD / 本集必须新建Canonical Master：
- CHR_CHARACTER_B_CURRENT_MASTER｜WHY_REQUIRED=...｜REQUIRED_BY=...｜DOWNSTREAM_USE=...
- ENV_OLD_OPERA_BACKSTAGE_MASTER｜WHY_REQUIRED=...｜Spatial Parent=...｜DOWNSTREAM_USE=...
- PROP_TRIFOLD_PROGRAM_MASTER｜WHY_REQUIRED=...｜REQUIRED_BY=...｜DOWNSTREAM_USE=...

CHARACTER REQUIREMENT SET / 主要、反复、可变身人物：
- CHR_CHARACTER_A｜LOOK=LOOK__｜DV-01=REUSE｜DF-02=REUSE｜HA-01=REUSE｜DF-01=NOT_REQUIRED｜AD-01=REQUIRED(reason=MCU/CU + current look insufficient)｜PR-01=NOT_REQUIRED｜Status=INCOMPLETE
- CHR_CHARACTER_B｜LOOK=LOOK__｜DV-01=TO_BUILD｜DF-02=TO_BUILD｜HA-01=TO_BUILD｜DF-01=<REQUIRED/NOT_REQUIRED>｜AD-01=<REQUIRED/NOT_REQUIRED>｜PR-01=<REQUIRED/NOT_REQUIRED>｜Status=INCOMPLETE

FUNCTIONAL MINOR HUMAN / SCOPED CAST：
- SCOPED_<...>｜Triggered By SH__/SEG__｜Function=...｜Distance/Clarity=...｜Visual Owner=TEXT_ONLY / FMH_ASSET｜Required Human Master=NONE / FMH_<...>｜Supplemental Assembly/Previs=OPTIONAL

FMH TO BUILD / 仅当Visual Owner=FMH_ASSET：
- FMH_<...>｜Scope=SCENE/SHOT_GROUP｜Role=SCOPED_CHARACTER_APPEARANCE_AUTHORITY｜Parent=SCOPED_CAST_BRIEF｜Why Text/Assembly Is Insufficient=...

ADORNMENT DETAIL TO BUILD / 仅由Character Requirement Set触发：
- AD-01_<CHARACTER_ID>_<ITEM_ID>｜Triggered By SH__/SEG__｜Why Current Look Is Insufficient=...｜Role=PERSONAL_ADORNMENT_AUTHORITY

EVENT / RELATION / PREDICTIVE COVERAGE TO BUILD：
- ENV_<SET>_CV_EVENT_<NODE>｜Type=ENVIRONMENT_COVERAGE｜Coverage Reason=EVENT_NODE｜WHY_REQUIRED=...｜Spatial Parent=...｜Visual Parent=...｜Triggered By Event=...
- ENV_<SET>_CV_REVERSE_<ANCHOR>｜Type=ENVIRONMENT_COVERAGE｜Coverage Reason=RECIPROCAL｜WHY_REQUIRED=...｜Spatial Parent=...｜Visual Parent=...｜Relation=...
- ENV_<SET>_CV_PRED_<ROLE>｜Type=ENVIRONMENT_COVERAGE｜Coverage Reason=PREDICTIVE｜WHY_REQUIRED=...｜Predicted Shots=...｜Spatial Parent=...｜Visual Parent=...
- PROP_TRIFOLD_PROGRAM_CV_OPEN_INSERT｜Triggered By SH__｜WHY_REQUIRED=...

TRANSFORMATION / 本集实际发生：
- T01 TF-01 / TE-03 / TH-01 / TC-01 / WP-01（按实际镜头需要与Canonical要求）

PERSISTENT STATE VARIANTS：
- ...

PERFORMANCE SUPPORT TO BUILD / 仅由Performance Asset Requirement Set触发：
- PERF_<...>｜Entity=...｜Type=EXPRESSION / ACTION_POSE / CONTACT_POSE｜Triggered By SH__/SEG__｜Why Base Master + Storyboard Is Insufficient=...

NARRATIVE FX TO BUILD / 仅由Narrative FX Asset Manifest触发：
- NFX_<...>｜Authority Mode=NARRATIVE_FX_REFERENCE｜Required States=...｜Triggered By SH__/SC__｜Narrative Role=...｜Why Text Grammar Is Insufficient=...

SUPPORT REF TO BUILD / 仅由Video Risk-Driven Static Reference Matrix触发：
- SUP_<...>｜Type=INTERACTION_GEOMETRY / COMPLEX_CONTACT / TRANSIENT_STATE / ENTITY_ACTION_STATE / LIGHTWEIGHT_INTERACTION_PROP / SHOT_DETAIL｜Triggered By SH__/SEG__｜Video Risk Reduced=...

SHOT ASSEMBLY TO BUILD / 仅由Shot Assembly Need Analysis触发：
- ASM_<...>｜Type=CHARACTER_SCENE_COMPOSITE / CHARACTER_SCENE_PROP_COMPOSITE / MULTI_CHARACTER_RELATION_COMPOSITE / MONTAGE_SITUATION_COMPOSITE / SPATIAL_INTERACTION_COMPOSITE｜Scene/Shot Group=...｜Why Existing Assets Are Not Enough=...

RELATION-DRIVEN ASSET OBLIGATIONS / 必须进入资产核算：
- REL__｜Type=ENVIRONMENT_COVERAGE｜Coverage Reason=CLUE_REVEAL / LOCATION_VISIBILITY / LOCATION_IDENTITY｜Fulfill By=STAGE_03_FREEZE｜Required Visual Fact=...｜Status=...

STAGE 04 VIDEO CONDITIONING PLAN / 只登记策略，不在Stage 03假生成：
- SH__ / VU__｜FIRST_FRAME / FIRST_TARGET / FIRST_LAST / KEY_POSE_CHAIN / CONTACT_CHAIN / CUT_PAIR｜Reason=...｜在Approved Clean Storyboard后建立/Promotion

LOOK / COLOR CONTROL：
- GLOBAL_COLOR_DNA｜REUSE / TEXT AUTHORITY
- INTERIOR_LOOK_<LOCATION/SCENE>｜TEXT / CARD｜Scope=...｜WHY_REQUIRED=...
- EXTERIOR_LOOK_<LOCATION/SCENE>｜TEXT / CARD｜Scope=...｜WHY_REQUIRED=...
- SCENE_COLOR_EXTENSION_<SCENE_ID>｜TO BUILD only if Need=YES｜Parent Global Color DNA｜Scope / Trigger / Why Text Is Insufficient
- SHOT_LIGHTING_VARIANT｜TEXT_CONTROL by default；只有明确升级为可复用Lighting Reference时才进入TO BUILD

VOICE IDENTITY：
- CHR_<ID>_VOICE｜REUSE / TO BUILD / TEMP_SYNC_EXCEPTION｜WHY_REQUIRED=...｜Downstream=Stage 05 Dialogue / Stage 06 Mix

EXCLUDED FROM STAGE 03：
- Storyboard：Stage 04生成
- Ending Frame：Stage 05视频批准后产生
```

Final Manifest只列**剧情和导演拆解已经支持、且通过Asset Consolidation & Sufficiency Audit后的唯一资产需求**。场景/道具必须先运行`shot_coverage_asset_derivation.md`：Canonical Master与Coverage分开登记，Coverage必须能回指真实Shot；同时运行`functional_minor_human_asset_protocol.md` + `production_support_reference_engine.md` + `shot_assembly_asset_layer.md`，把“匿名功能人物外观”“结构/空间”“持续状态”“复杂交互/Contact”“多人/人景物组装”“Storyboard后Video Conditioning Frame”路由到唯一Owner。不得为了“以后也许有用”提前扩展整季资产、机械360°场景、道具正背侧全套或无意义State Variant/Support Ref。**人物资产按`character_asset_requirement_set.md`执行：主要/反复/可变身角色冻结的是Required Identity Evidence，不再用笼统Character Master标签放行。**

## Stage 03生产方式

Episode Asset Pack可以在同一Cascade层内批量生产，但禁止跨未批准依赖并行越级。正式顺序：

**Planning Diagram / Spatial Canon → 用户批准 → Clean Canon / Key Event View → 用户批准 → Event/Reciprocal/Predictive Coverage → 用户批准 → Character/FMH Performance Support + Narrative FX（适用时）→ Shot Assembly/Production Support → Look/Color → Voice Identity → Final Freeze。**

每个图片Job仍读取`image_candidate_strategy.md`：Master通常2、高风险4；Coverage/Support/Assembly通常2。若Primary失败，先检查Backup是否已经解决同一问题，再决定Revision / Fresh Regen。只有最终APPROVED的一张计入Freeze；Backup候选不进入正式资产池。

**Dependency Stop Rule：** 例如Floor Plan未批准，不得批量生成该房间的正打/反打；Clean Canon未批准，不得用多个角度同时重新发明美术；Character Route矛盾时，不得靠Event View强行补图。

### 综合色与场景的依赖顺序
- Stage 02已经为每个新Scene建立`Scene Color Extension Spec`；
- 若`Scene Color Extension Card Need=YES`，正式Card必须在对应Environment Canon Master之前生成并APPROVED，作为该场景综合色控制；
- 若Need=NO，使用Global Color DNA + Scene文字Spec即可，不为了格式补图；
- Environment Canon Master批准后只复核Material Family与综合色Spec是否一致，不允许用一次随机母图的色偏反过来改写Color Authority；
- 临时Shot Lighting Variant不阻塞Environment Master，也不进入场景永久综合色身份。

可以一次给出一批互不依赖的资产Prompt以节省往返，但存在依赖的资产不得并行越级。例如Scene Color Extension Card尚未批准时，不批量生成依赖它的多个Environment Master/Coverage。“Prompt已经写好”不等于资产已经完成；只有真实APPROVED资产才计入Freeze Gate。

## Director Reconciliation（Stage 03两次复核）

正式Freeze前读取`director_spatial_reconciliation_gate.md`，采用两次复核，避免先做错依赖资产再返工：

### Pass A｜Geography Precheck
新Environment Canon Master + Geography / Blocking Spec一经Approved，**先**把Stage 02 Spatial Requirement / Detailed Shot Contract与真实空间对齐。必须得到`DIRECTOR GEOGRAPHY PRECHECK PASSED`，再生成依赖该空间的Derived Coverage / Shot Assembly。

若Camera/Blocking与真实空间不兼容：先比较当前`Non-Negotiable Directorial Invariants`。不触及Invariant时才允许最小Patch受影响Director Shot并重算Coverage / Assembly Need；若必须改变核心Blocking/Distance、POV、Reveal、Reaction Give-Deny或关键Hold/Cut，标`DIRECTOR_INVARIANT_SPATIAL_CONFLICT`并回Director Judge，不能由Stage 03自行改导演。Environment本体不能满足Story功能空间则`ENVIRONMENT_FUNCTIONAL_GEOGRAPHY_CONFLICT`。

### Pass B｜Final Spatial Reconciliation
Required Coverage / Assembly / Spatial Support完成后再次复核，结果必须为：
`DIRECTOR SPATIAL RECONCILED`。

首次/关键Transformation若Stage 02只有Presentation Requirement Draft，则Stage 03实际Splendor Profile完成后还必须得到`TRANSFORMATION PRESENTATION RECONCILED`。


## Costume Dramaturgy / Body Presentation Reconciliation

对于Stage 02判定为`CLOSET RECOMBINE / NEW LOOK`且服装承担人物/关系/剧情关键读点的主要角色，正式Freeze前必须：
1. Source Wardrobe Classification已完成，普通小说服装描写没有变成硬锁；
2. Costume Dramaturgy Brief已完成；
3. Stage 03实际Approved Look与Dressing Motivation / Self-Presentation / Critical Costume Read一致；
4. Body Identity未漂移，并已登记当前`Body Presentation Mode / Preserved Appeal Hook`；
5. 若关键服装信息在Stage 02镜头中根本不可读，执行最小Director Patch，而不是重新设计整套衣服。

通过状态：`COSTUME_DRAMATURGY_RECONCILED`。普通复用Look、非剧情关键群众不机械阻塞Freeze。


## V4.5.7｜Base Visual Authority Hardening（不可被旧轻量规则覆盖）

图片资产数量不再作为减少Base Authority的理由。Stage 03必须建立并冻结`BASE_VISUAL_AUTHORITY_MANIFEST`：

1. 每个被正式Event/Shot使用的Location/Sub-location，Tier S/A/B/C全部生成一张空场景Clean Master；
2. 每个清楚可见的Scoped Cast / 一次性配角全部生成一张独立Functional Minor Human Master；
3. Shot Assembly、白描、Rendered Previs只做补充，不得替代上述两种Base Master；
4. 深背景不可辨认群众才允许TEXT_ONLY；
5. 同一个Location/Minor Human依靠`entity_id + reuse_key`跨Shot复用，禁止按Shot重复建Master；
6. Base Master变化用Version/Lineage管理，Camera方向变化用Coverage/View Set管理。

Stage 03 Freeze必须通过`validators/base_visual_authority_lint.py`。

## Episode Asset Freeze Gate（当集资产冻结闸门）

进入正式Stage 04前必须检查：

1. Stage 02已达到`DIRECTOR BREAKDOWN READY`；当前Scene有有效Director Intelligence Decision Card + Sequence Arc；Episode Asset Accounting + Provisional Episode Asset Requirement Manifest完整，Asset Consolidation & Sufficiency Audit已运行且无`ASSET_SUFFICIENCY_GAP / ASSET_REQUIREMENT_DUPLICATION_CONFLICT`，并包含Selected Directorial Thesis / Spatial Requirement / Detailed Shot Contract的Director Ref；
1A. `SPATIAL_CANON_LOCKED`：适用地点的Topology/Floor Plan/Zone/Anchor/Sightline/Access已通过Spatial QC与用户批准；SHOT_RELATION_GRAPH引用的Spatial Relation均能回指真实Locked Spatial Canon；
1B. Final Manifest明确列出所有`fulfill_by=STAGE_03_FREEZE`的Relation-driven Asset Obligation，且非豁免项已有真实Approved fulfillment asset + proof_status=PASS；
1C. Required Outdoor Topology / Floor Plan / Route Map等Planning Diagram已有真实Approved Evidence；Event Node→Spatial Node与Character Event Route已验证；
1D. 所有正式TO BUILD资产都有`WHY_REQUIRED / REQUIRED_BY / DOWNSTREAM_USE`，Coverage含有效Spatial Parent + Visual Parent；不存在无依据“以后也许有用”的图；
2. 新Environment在Canon Master + Geography批准后已先得到`DIRECTOR GEOGRAPHY PRECHECK PASSED`；依赖的Coverage / Assembly在正确Director Contract上生成；最终已得到`DIRECTOR SPATIAL RECONCILED`；首次/关键Transformation适用时同时为`TRANSFORMATION PRESENTATION RECONCILED`；不存在`DIRECTOR SPATIAL PATCH REQUIRED / ENVIRONMENT_FUNCTIONAL_GEOGRAPHY_CONFLICT`；
3. 所有`REUSE`资产仍为有效APPROVED版本；
4. 所有`TO BUILD`关键资产已真实生成、QC并由用户批准；
5. 每个主要/反复/可变身人物都已完成`Character Asset Requirement Set`：默认`DV-01 + DF-02 + HA-01`为有效APPROVED/REUSE；Stage 02判Required的`DF-01 / AD-01 / PR-01`也已真实生成、QC、用户批准；没有`CHARACTER_IDENTITY_LOCK_GAP / ADORNMENT_ASSET_GAP`；
6. 所有Stage 02 `SCOPED_CAST_BRIEF`中清楚可见的人物均已有真实生成、QC、用户批准的`APPROVED SCOPED FIGURE / FUNCTIONAL_MINOR_HUMAN_ASSET`；Shot Assembly / Previs不得作为Appearance Master替代品；仅真正深背景不可辨认群众允许TEXT_ONLY；不存在`VIDEO_MODEL_GUESS`；
7. 人物当前完整Look、Adornment Active State、重要场景、关键道具/武器、必要变身与持久状态没有缺口；
8. Environment / Prop已经运行Shot Coverage Matrix：**每个正式Environment/Sub-location（含Tier C）先有Approved空场景Clean Canon Master**；每个TO BUILD Prop先有Approved Canon Master；所有结构/空间高风险镜头所需Derived Coverage已批准，且每张Coverage都有Parent Master + Triggered Shot；没有机械360°/正背侧全套；
9. `Video Risk-Driven Static Reference Matrix`已运行；所有Owner Stage=03且Required的Production Support Reference已QC + 用户批准，严重跨镜状态没有被临时Support冒充Persistent State；
10. `Shot Assembly Need Analysis`已运行；所有`SHOT_ASSEMBLY_REQUIRED`项目都已有真实生成、QC、用户批准的`APPROVED ASSEMBLY`，且无`SHOT_ASSEMBLY_GAP / SHOT_ASSEMBLY_AUTHORITY_FAIL`；没有从Storyboard宫格放大/清稿冒充Assembly；Stage 04 Video Conditioning只登记策略、不在Stage 03假生成；
11. 没有用Storyboard、尾帧、低清控制图或无资格测试图冒充正式Master/Coverage/Support/Assembly/AD-01；
12. Interior / Exterior Look Domain已经按当前地点冻结；需要正式Scene Color Extension Card的Scene均已APPROVED；不需要图像色卡的Scene已经冻结文字Spec；不存在把Global/旧Scene色卡机械套到新地点的缺口；
12A. Tier S/A Set的Predictive Coverage已按后续真实剧情/机位需求收敛完成；需要的Forward/Reverse/Look-back/Entry/Exit关系视角已批准，不以固定九宫格数量作为完成条件；
12B. 主要/反复角色Required Voice Identity Asset已APPROVED，或已登记合法`TEMP_SYNC/POST_VOICE_REQUIRED`例外；随机生成音色不得计入Voice Canon；
13. 适用的重要新/重组LOOK已完成`COSTUME_DRAMATURGY_RECONCILED`，并登记Body Presentation Mode；不存在`NOVEL_WARDROBE_LITERALISM_FAIL / STORY_WARDROBE_FACT_LOSS_FAIL / BODY_IDENTITY_DRIFT`；
14. 所有将进入Freeze的正式人物/Scoped Figure/Shot Assembly/Support类高清静态图，若存在清楚可读前景脸/手/关键接触，已通过`asset_anatomy_integrity_gate.md` + `foreground_figure_integrity_gate.md`；不存在`ANATOMY_HAND_FAIL / FACE_INTEGRITY_FAIL / CONTACT_INTEGRITY_FAIL / FOREGROUND_LIMB_READ_FAIL / FOREGROUND_FIGURE_COHERENCE_FAIL`；
15. Episode Workspace已记录Director Precheck / Final Reconciliation / Transformation Presentation（适用时）状态，以及Character Requirement Set / Functional Minor Human / Adornment / Coverage / Support / Shot Assembly / Color关系；Freeze Snapshot已准备完成。


通过后状态：

`EPISODE ASSET FROZEN`

只有这个状态才允许Production Mode进入Stage 04正式Storyboard Prompt。


### Current｜Style Continuity Freeze Check
所有进入Freeze的正式视觉资产必须：
- 有有效Style Projection Fingerprint；
- 实际QC包含Style Match维度；
- 补图/重建/Revision不存在未解决`STYLE_EVIDENCE_BINDING_GAP / STYLE_TAG_ONLY_FAIL`。
## Freeze之后发现遗漏怎么办

如果Stage 04/05发现一个**确实会影响身份、结构、空间、关键状态或昂贵Video执行稳定性**的静态视觉缺口：
如果Stage 04发现Storyboard必须改变Stage 02核心Blocking / Distance / Axis / Camera Intent才能在真实Environment成立，优先判`DIRECTOR SHOT CONTRACT CONFLICT`，回Stage 02 + Director Reconciliation做最小Patch；不要把导演冲突误诊成“Storyboard自由发挥”。


- 不用Storyboard或视频临时“硬撑”过去；
- 标记 `EPISODE ASSET FREEZE BROKEN`；
- 回Stage 03只补这个真实缺口；
- QC + 用户批准后重新执行Freeze Gate；
- 用Change Impact只复查真实依赖该资产的Storyboard / Video，不把整集已经正确的内容全部作废。

如果只是普通角度、姿势、微表情、短期湿水/灰尘/轻血迹等，且现有Authority + Storyboard已把静态歧义降到LOW，不新增图。若Stage 04发现清楚配角/功能性小人物缺少Stage 02 `SCOPED_CAST_BRIEF`或Approved FMH/Minor Human Master，标记`FUNCTIONAL_MINOR_HUMAN_GAP`并`FREEZE BROKEN(reason=functional-minor-human)`，回Stage 03补人物母图；不得在Stage 04用Previs/Assembly首次发明Appearance；若Stage 04发现主要/反复人物缺少Stage 02应有的身份锁页，标记`CHARACTER_IDENTITY_LOCK_GAP`并`FREEZE BROKEN(reason=character-identity-lock)`；若Signature Adornment在当前镜头成为CRITICAL、Current Look不足以锁定且缺AD-01，标记`ADORNMENT_ASSET_GAP`并`FREEZE BROKEN(reason=adornment-detail)`。若Stage 04发现**必须看清此前未覆盖的道具结构面或正式空间方向**，标记`ASSET_COVERAGE_GAP`并回Stage 03补最小Derived Coverage；若发现复杂交互/Contact/短暂高风险状态可被一张高清静态图显著稳定且属于Stage 03 Owner，标记`VIDEO_RISK_REFERENCE_GAP`并`FREEZE BROKEN(reason=support-reference)`后只补最小Support Ref；若发现人物/场景/道具各自都有Authority，但关键多人关系或人景物组装缺少高清静态资产，标记`SHOT_ASSEMBLY_GAP`并`FREEZE BROKEN(reason=shot-assembly)`后只补对应Assembly。若问题必须依赖Approved Storyboard准确构图，则不打破Stage 03 Freeze；Storyboard批准后固定进入`VIDEO_CONDITIONING_IN_PROGRESS`，按策略生成/Promotion First/Target/Last/Contact/Exit/Entry等镜头执行帧。

## Scene Pack在新流程中的位置

Scene Pack仍然保留，但角色发生变化：

- **以前：** Scene Pack可能边做Scene边发现/新建资产；
- **现在：** Scene Pack只是从已经冻结的Episode Asset Pack里抽取“本Scene常用资产集合”。

它负责复用和缩短Reference Pack，**没有权限绕过Episode Asset Freeze让某个Scene提前进入Storyboard。**

## Stage 04 / 05的调用方式

资产冻结后，每个Segment按实际需要：

`Spatial Canon + Episode Asset Pack（冻结资产池） → Scene Pack → Reference Resolver → Clean Storyboard → Approved Previs → Video Conditioning Build/QC/Approval → VIDEO_CONDITIONING_READY → Video`

对于`CONTINUITY_ENTRY`：正式Storyboard默认等待上一Segment真实APPROVED Ending Frame后再生成，以真实连续性输入为准；不再用计划Exit/尾格冒充正式尾帧提前生产。

`CUT_ENTRY / SCENE_OPENING`没有上一尾帧依赖，可在Episode Asset Freeze后按导演计划直接进入Storyboard。


## Color Authority Preservation in Asset Pack（Current Rule）
当`Scene Color Extension Card Need=YES`且Card已APPROVED后，所有属于该Scene Scope的场景绑定型后续资产必须在Job Contract中记录`Color Authority Owner`，并在场景绑定资产生产时实际保留Scene Color Authority。Stage 03/04/05均优先保留综合色视觉Authority；Stage 05可按平台能力直接绑定Scene Card/Color Crop；只有当前路由产生有效`APPLIED_REFERENCE_TRIGGER`时才使用Applied Reference。不能无理由退成纯文字，也不能忽略目标模型已有失败证据。纯Character Identity Master与合法Tiny Local Patch按Gate例外处理。

## Current｜Color Reference Planning Closure
Episode Asset Pack不得因为Scene Color Card存在就预排`SCENE_COLOR_APPLIED_REFERENCE`。默认资产就是Approved Color Card本身。Applied Reference只能在后续具体目标模型路由产生有效`APPLIED_REFERENCE_TRIGGER`后按需生成。

## V4.5.4｜Required View Fulfillment进入Final Episode Asset Manifest

Final Manifest必须对每个`view_requirement_id`记录：触发Event/Shot/Relation、Location、Camera Origin、Optical Axis、Must See、Candidate Budget、Candidate Asset IDs、最终Selected Fulfillment Asset、Visual Evidence状态。

`REQUIRED_ASSETS_COMPLETE`不再只问“这个场景有没有图”，而要问“本集所有Required View是否都有APPROVED且视觉验真的Fulfillment”。任一P0/P1 View缺失时Asset Pack不得Freeze。

## V4.5.5｜Realism Contract进入Final Episode Asset Manifest

Final Episode Asset Manifest对普通人物-场景资产增加`REALISM_CONTRACT`依赖。每个需要现实性证明的TO BUILD资产至少可追溯：
`Why Required → Scene/Event/Shot → Spatial Parent → Realism Contract → Asset → Current Visual Evidence`。

Freeze时，Required View完整但现实性FAIL仍视为Asset Pack不完整；不得用“已经有这个方向的图”覆盖人物数量/Zone/Vehicle Layout/人体支撑/普通连续性缺口。

## V4.5.7｜Rich Library Completeness

Stage 03遵循`asset_library_completeness_policy.md`：**资产库做足，单镜引用做精。**

- Stage 03不设置固定图片数量上限；数量由本集真实Requirement决定；
- `MINIMUM_SUFFICIENT_REFERENCE_SET`只属于Stage 05单个Generation Job，不得反向变成`MINIMUM_SUFFICIENT_ASSET_LIBRARY`；
- Freeze前新增硬门`ASSET_LIBRARY_COMPLETENESS_PASS`，同时检查Base Visual、Required Coverage、Performance Support、Narrative FX及其它Stage 03未豁免义务；
- Asset多时依靠`entity_id / reuse_key / asset_family_id / lineage / version / approval_ref`管理，禁止按Shot重复造Base Master。
