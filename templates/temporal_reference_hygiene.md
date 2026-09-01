# Temporal Reference Hygiene｜V4.5.11

> Pixels own the present. Prompt owns the future. Canon owns the next legal reset.

本模块拥有同一 take 续接边界的 Reference Hygiene 语义。内部 Authority 保持完整，但模型 t=0 输入按模式稀疏化。

- `SEAMLESS_EXTEND`：Verified Ending Anchor 是唯一 model t=0 visual owner；使用 `DELTA_CONTINUATION_PROMPT`；普通 Character/Prop/Environment/Scene Color/Shot Execution 静态图不得同时 Direct Bind。
- `GUIDED_CONTINUATION`：Verified Ending Anchor + real Target Frame；必须证明首尾/endpoint transport 语义；使用 `TRANSITION_PROMPT`。
- `CUT_REPROJECT`：真实 Cut；由 World Spatial State × Camera Topology 重投影；新 Shot Execution Frame 取得 model t=0；使用 `FULL_SHOT_PROMPT`。
- `SCENE_REBASE`：合法重置；Canon/Environment/Color 可重新取得完整视觉权威；递归 pixel lineage 重置。

Internal Conditioning Primary 与 Model t=0 Primary 是两个不同字段。Same-take 不得为了旧 `PRIMARY_VIEW` Gate 把 Shot Execution Frame 再塞进 Provider。

实体需要 Direct Reference 而 Ending Anchor 已有足够可读证据时，用 `TEMPORAL_T0_BAKED`；证据不足则 `TEMPORAL_RESET_REQUIRED`，不得用“尾帧 + 人物母图”硬撞。

Ending Anchor 必须来自 `LOCAL_DECODED_VIDEO` 或 `PLATFORM_EXTRACTED_VERIFIED`，记录源视频 fingerprint、真实 frame hash、递归 snapshot fingerprint、pixel lineage depth 和 degradation debt。Snapshot Gate 必须由独立 validator 产生，捕获工具不能自证。

## Storyboard Approximate Editorial Cut Bridge

当Locked Editorial Plan允许真实切镜时，`CUT_REPROJECT`默认启用`continuity_precision = STORYBOARD_BLOCKING_APPROXIMATE`，而不是把Previous Ending Frame作为Provider直接输入。

此路线固定分权：

- Previous Approved Ending Frame + Continuity Snapshot：只拥有已发生事实、Stage 06剪辑证据和Change Impact；`ending_frame_provider_route = LINEAGE_ONLY / STAGE06_EDIT_REFERENCE_ONLY`。
- Approved Storyboard Exit/Entry：拥有切点两侧的Camera/Blocking/Screen Direction/Depth/Action Phase近似桥接；不得拥有最终人物身份、材质或综合色。
- World Spatial State：拥有人物在场集合、世界Zone/Anchor、朝向、接触、道具Holder与数量等P0事实。
- 新Shot Execution Frame +高清Character/FMH/Environment Authority：拥有下一镜模型`t=0`的最终像素质量。
- Locked Editorial Plan：拥有`MATCH_ON_ACTION / CUT_REFRAME / REACTION_CUT / SPATIAL_REORIENTATION / J-CUT / L-CUT / SOUND_BRIDGE / SHAPE_OR_DIRECTION_MATCH`等过渡语言。

最低桥接字段：

`tracked_entity_set / world_zone_or_anchor / screen_side_or_motion_vector / depth_region / body_orientation / action_phase / held_prop_owner_and_count / transition_language`。

只要这些字段与Approved Storyboard结尾和下一镜入口大致合理，允许关节微角度、手指姿态、衣褶、粒子相位、像素纹理、压缩噪声和轻微综合色在Cut后变化。不得把这种允许变化误判为连续性失败，也不得为追逐逐像素一致而上传会污染下一镜的低清尾帧。

例外：同一摄影机、同一Take或动作接触必须无缝跨生成延续时，仍走`SEAMLESS_EXTEND / GUIDED_CONTINUATION`，Verified Ending Anchor继续是唯一model`t=0`视觉Owner。
