# Cinematic Spatial Staging Engine（电影化空间调度引擎）

> **用途：** 为Stage 02提供人物距离、景深、屏幕占比、遮挡、轴线与镜头空间的可执行导演规则。它解决“人物都站成一排、距离太安全、空间没有压迫感”的问题。

## 1｜空间不是背景，是戏剧变量

每个重要Beat先问：
- 谁控制空间？
- 谁正在缩短/拉开距离？
- 谁挡住谁的路径或视线？
- 哪个Environment Feature参与关系？
- Beat结束后，人物空间关系和开始相比发生了什么？

## 2｜Screen Occupancy

不要只写Wide / Medium / Close。重要Shot还记录主体相对画面高度/面积的意图，例如：
- `DOMINANT`：主体明显压画面；
- `BALANCED`：主体与环境都可读；
- `SUBORDINATE`：主体被环境/威胁压制。

需要时可用近似比例（如人物高度约70%）帮助执行，但不是全片固定数学规则。

## 3｜Depth Layers

多人Shot优先建立真实前后关系：
- FG可以是肩、武器、门框、链条、家具；
- MG通常承担主要表演/接触；
- BG承担第二人物、出口、威胁或环境因果。

允许重要主体部分出画；“所有资产都完整展示”不是电影化构图目标。

## 4｜Overlap / Occlusion

合法遮挡可增强：
- 距离感；
- 压迫感；
- 主观观察；
- 战斗攻击线；
- 信息延迟。

但Critical Visual Read不能被无理由挡住。

## 5｜Distance Contrast

一个Scene若剧情关系明显变化，至少检查是否需要距离反差：
- 远 → 近；
- 近 → 突然拉开；
- 平行 → 前后错层；
- 隔着屏障 → 共享空间；
- 安全距离 → Weapon Reach / Contact。

不是每场都必须大幅移动；静止本身可以有张力，但必须是有意的。

## 6｜Lens / Perspective Intent

Stage 02不强迫使用具体毫米，只锁摄影效果：
- `DEPTH_EXAGGERATED`｜强化前后尺度差；
- `NATURAL_PERSPECTIVE`｜自然关系；
- `DEPTH_COMPRESSED`｜压缩人物距离、产生拥挤/监视感。

Stage 04再按实际模型能力翻译成可执行Camera/Lens描述。

## 7｜Combat Staging

战斗优先避免：
- 三方等距三角展示；
- 所有人完整全身；
- 敌人永远画面正中像展品；
- Weapon Reach和人物实际距离不一致；
- 接触时Camera退得太远；
- Camera靠近后又遮住接触点。

关键Exchange通常至少有一个Shot让观众清楚读到：
`Attack Line + Defender Relation + Contact/Near Miss + Force Direction`。

## 8｜Transformation Staging

变身Hero状态第一次完整出现时，构图必须让新Silhouette、Material Contrast、Music Eye/Weapon中的关键层级真正可读。若依旧使用普通日常人物同样的安全全身距离和画面权重，判展示失败。

## 9｜Hard Fail

- `STAGING_DISTANCE_FLAT_FAIL`：关键多人镜头同深度/同尺度/均匀间距且无理由；
- `COMBAT_LINEUP_FAIL`：战斗像角色阵容展示；
- `SPATIAL_DOMINANCE_UNREADABLE`：剧情明确谁压迫/保护/主导，但构图完全读不出；
- `CRITICAL_OCCLUSION_FAIL`：遮挡破坏关键视觉信息。


## Current｜Selected Interpretation Boundary
本引擎只为Director Judge已选定的Interpretation求解空间，不自己决定“更有电影感”的替代拍法。若空间求解发现Selected Plan与真实Environment不可兼容，走Director Spatial Reconciliation；如果最小Patch会改变Audience Alignment / Reveal / Core Blocking / POV / Reaction / Key Cut-Hold，必须返回Director Judge，不能由Staging Engine自行换方案。


## Current｜Execution Handoff
本引擎只拥有Stage 02导演空间设计，不直接往Final Video Prompt追加自然语言。Detailed Shot Contract锁定后，Stage 02C必须读取`spatial_execution_translation.md`，只把当前Segment真正需要的动态位置/关系/路径/落点转成`SPATIAL_EXECUTION_STATE`。视觉Reference已经证明的静态空间不重复，动态空间执行不得因Visual-First被整体删掉。

## V4.5.5｜Reality Floor Before Dramatic Geometry

电影化空间调度建立在现实可行性之上。普通剧情先满足“正常人能这样站/坐/交流/通行”，再使用距离、遮挡、前后层和Power Geometry增强戏剧性。

- 人物位置若明显违背功能位置、座位、通道或人体尺度，不得以“更有电影感”解释；
- 低声交流/共同任务等普通行为应有合理距离与Eyeline Access；刻意疏远、戒备、监视等反常距离必须有Director/Behavior Reason；
- Staging不得为了画面均衡把角色从已锁定Driver/Passenger/Bedside/Counter等功能位置挪走；
- 若Director方案只有破坏现实功能才能成立，先走Director Spatial Reconciliation，而不是让Stage 03图片偷偷改空间。

普通现实Hard Fail可增加：`CHARACTER_ZONE_ASSIGNMENT_FAIL / SOCIAL_SPATIAL_IMPLAUSIBILITY / SPACE_CAPACITY_EXCEEDED / HUMAN_SCALE_IMPLAUSIBLE`。
