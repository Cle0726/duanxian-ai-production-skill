# Auto Naming（自动文件命名）

> **用途：** 避免长期项目出现“最终版2_真的最终.mp4”。Skill在交付Prompt或批准资产时，同时建议稳定文件名；用户已有命名规则时优先沿用原规则。

> **V4.3确定性执行：** 运行环境可执行Python时，默认命名优先调用`tools/asset_naming.py`；本文件保留命名语义与兼容规则。

## 默认格式（仅在项目没有更高优先级命名规则时）

```text
DSG_<EPISODE_ID>_<SCENE_ID>_<SEGMENT_ID>_SB_v001.png
SUP_<EPISODE_ID>_<SHOT_OR_ASSET>_<TYPE>_v001.png
FMH_<EPISODE_ID>_<SCENE>_<FUNCTION>_v001.png
AD_<CHARACTER_ID>_<SIGNATURE_ADORNMENT>_v001.png
ASM_<EPISODE_ID>_<SCENE_OR_SHOTGROUP>_<TYPE>_v001.png
ANCHOR_<EPISODE_ID>_<SCENE_ID>_<SHOT_ID>_HD_v001.png
DSG_<EPISODE_ID>_<SCENE_ID>_<SEGMENT_ID>_VID_TAKE01.mp4
DSG_<EPISODE_ID>_<SCENE_ID>_<SEGMENT_ID>_VID_TAKE01_SALVAGE_A_<IN>-<OUT>.mp4
DSG_<EPISODE_ID>_<SCENE_ID>_<SEGMENT_ID>_END_v001.png
```

常用标签：

- `SB` = Storyboard（分镜）
- `VID` = Video（视频）
- `TAKE` = 实际发生的第几次生成尝试；默认从TAKE01起步，不表示必须提前生成TAKE02；T3/T4合法候选预算产生后续Take时继续编号
- `END` = Ending Frame（正式连续性尾帧）

- `AD` = Signature Adornment Detail（AD-01，人物个人装饰高清局部）
- `SUP` = Production Support Reference（Stage 03生产辅助参考，APPROVED SUPPORT而非Canon）
- `FMH` = Functional Minor Human Asset（Stage 03范围人物外观参考，APPROVED SCOPED FIGURE而非长期Character Canon）
- `ASM` = Shot Assembly Asset（Stage 03镜头组装资产，APPROVED ASSEMBLY而非Canon/Storyboard）
- `VIDCOND` = Video Conditioning Frame（Stage 04镜头执行图，APPROVED_VIDEO_CONDITIONING而非Canon）
- `APPROVED` = 已批准版本，可在项目习惯允许时加入文件名

## 规则

- 不覆盖用户已有编号体系；
- Scene / Segment ID以Episode Workspace为准；
- 默认从TAKE01起步；只有实际发生可选重试/返工或T3/T4受限候选预算后才出现后续Take编号；
- 若多个Take已经存在，Candidate Triage保留Take编号，便于说明推荐的是哪一个；
- 资产版本继续使用各自Registry版本，不要把Segment Take编号当资产版本。
## 与Approved Asset Archiver联动

Auto Naming在正式归档前运行。正式文件名必须稳定、可追踪，并优先包含已有Asset / Episode / Scene / Segment ID与版本号。

如果目标目录已有同名APPROVED文件，不静默覆盖；按Registry版本规则生成新版本名，或确认是同一文件后避免重复归档。



## Current｜Salvage Clip Naming
Salvage Clip必须保留Source Take与IN/OUT追溯信息。`SALVAGE_A/B/C`只在实际登记多个Window时递增；不要把Salvage编号当新Take编号。候选只登记Registry即可，只有真正导出/采用时才要求实体Clip文件。
