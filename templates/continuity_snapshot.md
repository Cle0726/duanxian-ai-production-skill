# Continuity Snapshot｜V4.5.11

> **用途：** 定义连续性快照的语义。机器字段以`state/continuity_snapshot.schema.yaml`为准。

## Authority关系

正式Continuity Snapshot只能在真实`APPROVED VIDEO`之后建立。Previous Ending Frame必须来自真实Approved Video的稳定Ending Frame；Storyboard尾格、计划Exit、生成前Keyframe或Inpaint替代图不得冒充。

## 必须记录

- Episode / Scene / Segment / Shot
- Source Approved Video ID / Version / Fingerprint
- Ending Frame ID / File Hash（真实文件可用时）
- Actor positions / facing / pose / held props
- Wardrobe / injury / contamination / transformation state
- Environment runtime state
- Prop/weapon location and ownership
- Ongoing action / task / motion state
- Knowledge / relationship delta（只记录会影响下一段执行的部分）
- Camera-side/screen-direction facts needed by next continuity entry
- Created/approved timestamps（环境可提供时）

## 不要记录

- 与下一段无关的完整剧情摘要；
- 未在真实视频中出现的计划状态；
- 被后续Approved Evidence推翻的旧视觉猜测；
- 把Storyboard设计值伪装成视频已实现事实。

## 写回

Snapshot写入后，下一`CONTINUITY_ENTRY`只消费当前任务需要的Delta。若Approved Video被替换，新Snapshot版本必须使依赖它的Storyboard/Video Runtime失效并运行Change Impact。

## V4.5.11｜Ending Frame提取与Provider上传分离

Approved Video仍必须提取真实Ending Frame并写Snapshot；这是事实链与Stage 06剪辑证据，不代表下一Video Job必须Direct Upload该帧。

- 真正像素级同镜续接：`SEAMLESS_EXTEND / GUIDED_CONTINUATION`，Ending Anchor可成为唯一model`t=0`视觉Owner。
- Locked Editorial Plan允许切镜：默认`CUT_REPROJECT + STORYBOARD_BLOCKING_APPROXIMATE`。Ending Frame仅`LINEAGE_ONLY / STAGE06_EDIT_REFERENCE_ONLY`；下一镜由Approved Storyboard Exit/Entry、World Spatial State、高清对象/环境Authority与新Shot Execution Frame建立。
- Cut Bridge只从Snapshot提取剧情P0：人物在场集合、世界Zone/Anchor、深度、朝向、动作Phase、关键接触、道具Holder与数量、必要Screen Direction。不得把尾帧的低清、压缩纹理、偶发综合色、微姿态或局部错误继承为下一镜最终像素。
- Storyboard尾格仍不能冒充“真实视频已发生”；它只在Cut Bridge中拥有计划中的空间占位与剪辑入口/出口几何。

## V4.5.7｜World Spatial State / Frame Projection / Motion Phase（新增）

连续性快照不再只记录宽泛“人物位置”，而要分三层：
1. `world_spatial_state`：人物/关键道具在真实空间中的`zone / anchor_relation / distance / orientation / contact`；
2. `frame_projection_state`：当前Approved Ending Frame里的人物`LEFT/CENTER/RIGHT`、`FG/MG/BG`、screen direction与可见遮挡；
3. `motion_phase_state`：动作/姿态正进行到哪一步，例如`REACH_60_PERCENT / SIT_SETTLE / WALK_STOP / DOOR_OPENING`。

下一个`CONTINUITY_ENTRY`必须优先继承World Spatial State，再根据新机位重新投影Frame Position。**画面左右不是世界事实。** 反打时允许LEFT/RIGHT变化，但不允许人物无因瞬移、换手、断开接触或跳过动作阶段。
