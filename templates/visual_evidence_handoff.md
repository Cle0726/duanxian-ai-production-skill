# Visual Evidence Handoff｜多模态→纯文本视觉事实交接 Authority

> **用途：** 《断弦之歌》长期生产允许多模态模型与纯文本LLM轮换。图片像素不是纯文本模型可直接观察的事实；任何已经被多模态模型/人工真正看过的正式视觉资产，都应把可复用观察写入`VISUAL_EVIDENCE`，让后续Text-only Controller安全选择`@资产`、判断缺口和继续生产。

## 1｜核心原则

**See Once → Record Facts → Reuse Safely。**

- Prompt描述、文件名、资产ID、生成意图都不是“图片实际画成什么”的Evidence。
- `VISUAL_EVIDENCE`只记录真正观察到的视觉事实；未知保持UNKNOWN，不允许根据原Prompt补猜。
- Visual Evidence的最高作用是把昂贵的视觉观察从一次对话上下文变成项目持久状态。
- 图片文件变化、Fingerprint不一致时，旧Evidence立即`STALE`；不得继续用于Text-only Reference Resolve。
- Pixel Review前必须先执行`templates/media_review_proxy_protocol.md`：脚本盘点原始文件与Hash，再用不超过1600px的代理图审核；Contact Sheet只能筛选，不能单独签发最终单项PASS。

## 2｜Controller Mode

### MULTIMODAL_ACTIVE
当前模型能真实看图/视频：
- 可以创建新的视觉观察与QC判断；
- 正式图片资产被QC/批准时，应同步写`VISUAL_EVIDENCE`；
- Evidence写入后保存Source Fingerprint、Observed Fact Codes、Issue Codes、Role Assessment与Confidence。

### TEXT_ONLY_CONTINUATION
当前模型不能看图片：
- 可以读取已存在且Fingerprint匹配的`CURRENT VISUAL_EVIDENCE`；
- 可以继续剧本、导演、Spatial Canon、资产需求、Relation、Prompt Compile、State维护和Reference Selection；
- **禁止创建新的视觉PASS，禁止修改observed_visual_facts，禁止根据Prompt/文件名推断图片结果；**
- 使用任何现有Image Asset作为Generation Reference前，必须通过`REFERENCE_VISUAL_EVIDENCE_GATE`；
- 缺Evidence时只阻断该视觉依赖决策，不默认让整个Episode回Stage 01。

## 3｜Visual Fact Record最小字段

每个Current Record至少回答：
- `asset_id + source_fingerprint`：到底观察的是哪一版文件；
- `fact_codes`：真实存在、可复用的视觉事实；
- `issue_codes`：真实观察到的污染/冲突/风险；
- `summary`：供人类阅读的短事实摘要；
- `safe_roles / unsafe_roles`：该图片适合与不适合承担什么Reference职责；
- `primary_visual_eligible / direct_video_eligible`；
- `confidence`。

例如Environment Master若画出了临时顾客，应记录`HAS_UNSCRIPTED_TRANSIENT_PEOPLE`；不能因为原Prompt写“空无一人”而删除这个事实。

## 4｜Reference Resolve规则

Text-only模式选择`@资产`时采用：

`SHOT REQUIRED VISUAL FACTS → CURRENT VISUAL EVIDENCE → ASSET ROLE → MINIMUM SUFFICIENT BINDING`

不是：

`Scene Name → 猜一个同名Asset`。

`REFERENCE_RUNTIME`应记录：
- `required_visual_facts`
- `forbidden_visual_facts`
- 每个Binding的`visual_evidence_ref/status/fact_codes/issue_codes`
- `visual_evidence_coverage`

若Required Fact没有任何Current Evidence覆盖 → `VISUAL_FACT_COVERAGE_GAP`。
若Evidence出现Forbidden/Conflict Fact → `VISUAL_FACT_CONFLICT`。
若Primary Visual的Evidence明确`primary_visual_eligible=false` → `VISUAL_ROLE_EVIDENCE_CONFLICT`。

## 5｜旧资产/未审资产

已有资产没有Visual Evidence时登记为`MISSING / UNVERIFIED`，不能因为过去被使用过就自动升级为Current Evidence。
多模态额度恢复后优先处理`VISUAL_REVIEW_QUEUE`，只补真正阻断当前生产的资产；不要求一次性重看全部项目图库。

## 6｜与Canon的边界

Visual Evidence回答“这张图片实际上画了什么”。
Spatial/Character/Environment Canon回答“项目事实应该是什么”。
两者冲突时不得让旧图片反向篡改Canon；应登记`LEGACY_ASSET_CANON_CONFLICT`并决定Support/Regenerate/Deprecate。

## V4.5.4｜Observed View Role / Camera Axis Evidence

多模态/人工审核Coverage时，Visual Evidence除普通内容事实外，还应尽量写：`Observed View Role`、`camera_origin_zone_id / camera_origin_anchor_id`、`view_target_entity_id / view_target_anchor_id`、`view_direction_code`、`visible_anchor_ids`。

这些字段回答“图片实际上从哪里朝哪里拍、真正看见了什么”。如果Prompt声称FORWARD但Observed Evidence是REVERSE，必须登记真实Observed值并让`REQUIRED_VIEW_REALIZATION_GATE`失败；禁止为了让Registry好看而把Evidence改成Prompt意图。

## V4.5.5｜Observed Everyday Realism

多模态/人工审核人物-场景资产时，Visual Evidence应额外记录`observed.realism`：
- `human_count`与逐角色Count；
- Character `zone_id / functional_position_id / posture / support_surface_id`；
- Environment `environment_kind / specific_type / vehicle_type / driver_zone / passenger_zones / scale / circulation / ingress-egress`；
- Object Affordance；
- 必要Character Pair的距离/Eyeline；
- 八类`category_verdicts`与`overall_verdict`。

Text-only Controller不得从Prompt里的“真实、合理、坐副驾”推断这些Observed字段。若P0/P1现实性字段缺失或UNKNOWN，只阻断该资产的现实性批准并加入Visual Review Queue。


## V4.5.6｜Fine-grained Reality Evidence Precedence

视觉审计不得只写`overall PASS`。若当前资产涉及车辆/功能空间/人物落位，优先保存可验证细节：Vehicle Type、Front Direction、Driver Forward Visibility、Passenger Count、Entry Anchors、Access Paths、人物Zone/Functional Position/Support、必要Eyeline与Mundane Continuity。任何细粒度FAIL优先于Category/Overall PASS。

## V4.5.7｜Platform-scale Identity Readability Evidence

Primary Visual的身份可辨性必须记录目标平台有效尺度Evidence。禁止根据原始分辨率、文件体积（例如19MB）或“放大原图后能看清”写PASS。多人物远景应为每个Required命名人物分别记录`identity_readability_verdict / identity_match_confidence / effective scale / evidence_ref`。平台尺度未知时保持UNKNOWN；UNKNOWN按未证明处理。
