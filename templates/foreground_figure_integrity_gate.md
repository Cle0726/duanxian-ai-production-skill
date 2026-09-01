# Foreground Figure Integrity Gate（前景人物完整性闸门）

> **用途：** 约束Stage 03正式图片资产、Stage 03 Shot Assembly、Stage 04关键Anchor与所有会继续作为Authority被下游引用的高清静态图。只要前景人物的脸、手、肢体、关键接触能被清楚读到，就不能只看“整体氛围”。

## 1｜核心原则
前景人物是最容易一眼暴露AI错误的区域。**当前规则（Current Rule）：** 以下维度是独立硬闸：
1. `Face Integrity`｜脸部与五官完整性；
2. `Hand / Limb Integrity`｜前景手部、腕部、前臂与局部肢体完整性；
3. `Contact Integrity`｜手与衣领/伞柄/门把/身体/他人物体的接触是否真的成立；
4. `Foreground Figure Coherence`｜前景局部关系是否自然，没有融化、拼接、漂浮、复制或局部崩坏。

## 2｜触发条件
命中任一项即必须执行本闸：
- 前景或中近景角色的脸部五官清楚可读；
- 前景可读手部承担情绪、动作或抓握；
- 角色与自身身体、衣领、道具、他人存在关键接触；
- 局部前臂/肩颈/腿部构成明显前景可读结构；
- 该图后续会继续作为Storyboard / Video / QC Authority。

远景群体、深背景模糊人物不按本闸逐脸逐手苛查。

## 3｜Face Integrity（脸部完整性）
### 3.1 Face Priority
- `HERO_FACE`：前景主脸、主情绪脸、对剧情认知至关重要的脸；
- `FUNCTION_FACE`：可读但非绝对主焦点的近景脸；
- `SECONDARY_FACE`：中景可读脸；
- `BACKGROUND_FACE`：远景背景脸。

### 3.2 检查项
- 双眼大小、位置、朝向与视线是否自洽；
- 鼻子、嘴、下巴、耳朵与脸部透视是否同属一个头部结构；
- 眉眼关系、嘴角、鼻梁是否明显错位或塌陷；
- 不要求医学院级写实，但不能出现一眼错误的眼位漂移、嘴鼻错层、耳位离谱、面部融化。

`HERO_FACE`或`FUNCTION_FACE`明显错误 = `FACE_INTEGRITY_FAIL`。

## 4｜Hand / Limb Integrity（手部 / 前景肢体完整性）
执行 `asset_anatomy_integrity_gate.md` 的全部规则，并额外检查：
- 手/前臂与肩线、身体朝向是否一致；
- 当前表演动作是否让局部肢体关系仍然自然；
- 不能因为脸正确就放过前景融化手。

明显错误分别标：`ANATOMY_HAND_FAIL / WRIST_CONNECTION_FAIL / FOREGROUND_LIMB_READ_FAIL`。

## 5｜Contact Integrity（接触完整性）
适用于：摸喉、抓领口、持伞、扶人、贴墙、握门把、拿包带等。

检查：
- 手/物/身体真的接触到同一位置；
- 手指包裹、掌面朝向、受力方向与对象形体相容；
- 没有悬空假接触、穿模、磁吸式黏连、无因融合。

失败码：`CONTACT_INTEGRITY_FAIL`。

## 6｜Foreground Figure Coherence（前景人物局部一致性）
- 前景人物局部不能出现复制块、黏连布料、局部透视断裂；
- 手、脸、脖颈、肩颈、衣领、道具边缘属于同一人物结构；
- 如果单个局部补丁就能修复，优先Local Patch，不为局部错误整图推倒。

失败码：`FOREGROUND_FIGURE_COHERENCE_FAIL`。

## 7｜处置
- Hero / Function级别局部错误一律不得PASS；
- 整体图正确但局部错误：优先Local Patch；
- 若Backup已规避同类问题，Backup优先；
- 只有Primary与Backup都不行时才Fresh Regen。

## 8｜失败码总表
- `FACE_INTEGRITY_FAIL`
- `ANATOMY_HAND_FAIL`
- `WRIST_CONNECTION_FAIL`
- `CONTACT_INTEGRITY_FAIL`
- `FOREGROUND_LIMB_READ_FAIL`
- `FOREGROUND_FIGURE_COHERENCE_FAIL`
- `FIGURE_PRIORITY_UNCHECKED`
