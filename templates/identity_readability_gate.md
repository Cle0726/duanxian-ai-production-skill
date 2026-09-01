# Identity Readability Gate｜实际镜头尺度人物身份可辨性硬门 V4.5.7

> **目的：** 本门不重新规定“人物母图是否存在”。Stage 03已经要求清楚可见的命名/功能人物拥有自己的Approved人物视觉Authority。本门只回答一个更下游的问题：**当前Primary Visual在目标平台实际缩放/有效输入尺度下，能不能单独承担这些人物的身份核验。**

## 1｜核心原则

`有高清Primary Visual ≠ 人物身份可读`。

- 原图像素尺寸、文件体积、19MB或更大文件都不是身份可辨性的充分证据；
- 多人物远景必须按**目标平台实际缩放后的有效画面**检查脸部/身份特征是否还能被辨认；
- 若平台实际内部缩放可复现，使用`PLATFORM_ACTUAL_SCALE`；若平台只提供稳定的目标输入Profile，使用同Profile生成`PLATFORM_PROFILE_SIMULATION`预览；
- `ORIGINAL_RESOLUTION_ONLY / FILE_SIZE_ONLY`不得产生PASS；
- 平台尺度未知且无法构造有效预览时，身份结论必须保持`UNKNOWN`，不得根据“原图很大”猜PASS。

## 2｜Hard Fail定义

对于当前Shot中需要身份核验的命名/身份关键人物：

`Primary Visual @ platform-effective scale → identity_readability = FAIL / UNKNOWN`

则记录：

`IDENTITY_READABILITY_FAIL`

发生后：
1. 当前Primary Visual仍可继续承担Composition / Blocking / Spatial State；
2. **它不得继续作为该人物唯一Identity Authority；**
3. 必须二选一：
   - `DIRECT_CHARACTER_IDENTITY_AUTHORITY`：直接绑定该人物Approved Character Master / Current Look / FMH Base Master等真正人物Identity Authority；
   - `REGENERATE_READABLE_PRIMARY`：重新生成身份可辨的高清执行帧，并重新做平台尺度Readability Assessment；
4. 若选择重新生成，在新Primary Visual取得`PASS`之前仍然BLOCKED；
5. 若选择Direct人物Authority，Primary Visual可保留为镜头构图主图，但Reference Pack必须真实包含对应人物资产。

## 3｜多人远景

多人远景不得只检查：
- source width/height；
- JPEG/PNG原始大小；
- 文件MB数；
- “放大原图以后看得见”。

必须检查平台有效缩放后的版本。每个身份关键人物分别记录：
- `entity_id`；
- `visibility_status`；
- 可选的`face_box_at_effective_scale_px`；
- `identity_readability_verdict`；
- `identity_match_confidence`；
- `evidence_ref / reason`。

任何一个Required人物FAIL/UNKNOWN，都不能把整张Primary Visual标成“所有人物身份已烘焙”。

## 4｜Authority边界（不可覆盖）

- **白描Storyboard：** 只控制Blocking / Camera / Action Beat / Timing / Cut。匿名几何人形永远不能补人物Identity；
- **Environment Clean Master / Coverage：** 只控制空间、材质、固定结构与场景方向，永远不能补人物Identity；
- **Shot Assembly：** 可以证明多人关系和人景物组合，但命名人物身份仍继承Character/FMH Authority；
- **Primary Visual：** 只有在平台有效尺度Readability PASS时，才允许对对应人物使用`PRIMARY_VISUAL_BAKED`作为唯一身份视觉依据。

## 5｜Stage 05 Resolver规则

对每个HUMAN Entity Binding：

`Entity → Current Primary Visual → Platform-scale Identity Readability`

- PASS → 可按Minimum Sufficient原则使用`PRIMARY_VISUAL_BAKED`；
- FAIL / UNKNOWN → `PRIMARY_VISUAL_BAKED`非法，必须`DIRECT_REFERENCE`到对应人物Identity Authority，或回Stage 04B重生Primary Visual；
- Storyboard / Environment资产不得作为Identity fallback；
- Direct Binding必须落入真实`Generation Job.required_bindings`，不能只写在Metadata里。

## 6｜Gate输出

- 所有Required人物Primary Visual可读 → `IDENTITY_READABILITY_PASS`；
- 部分不可读但均已Direct Bind人物Authority → `IDENTITY_READABILITY_PASS`，模式=`PRIMARY_PLUS_DIRECT_IDENTITY`；
- 任一不可读/未知人物既没有Direct人物Authority，也没有通过的新Primary Visual → `IDENTITY_READABILITY_FAIL`，禁止进入Video Generation Ready。
## 7｜反绕过补充（Logic Closure）

- `CRITICAL`与`SUPPORT` Human Slot在`AUTO`策略下都属于Readability检查对象；只有真正`AMBIENT`/不可辨背景人物可跳过。
- `PASS`不是自由文本：对于`VISIBLE / PARTIALLY_OCCLUDED`人物，必须有目标平台有效尺度的Face Box记录、有效Scale Evidence，以及至少`MEDIUM` Identity Match Confidence；`LOW / UNKNOWN`不能写PASS。
- `PLATFORM_PROFILE_SIMULATION`必须有Preview Manifest；`PLATFORM_ACTUAL_SCALE`必须有实际Scale Evidence或等价Manifest。
- Direct Identity Fallback必须拥有与当前`entity_id`完全一致的`subject_entity_id`；缺失subject绑定不能视为人物Identity Authority。
- Assessment的`status`必须与计算结果一致：Primary全部可读=`PASS`；Primary不可读但Direct Identity已绑定=`NEEDS_DIRECT_IDENTITY_SUPPORT`；尚未补足=`BLOCKED`；Primary已变更=`STALE`。
- Resolver若要对需要身份检查的人物使用`PRIMARY_VISUAL_BAKED`，必须读取当前有效的`IDENTITY_READABILITY_ASSESSMENT`；漏传Assessment本身就是Fail。
- 无需人物身份核验的纯环境/物件Shot允许`NOT_APPLICABLE`，不得伪造一个人物Assessment来满足流程。
