# Asset Anatomy Integrity Gate（图片资产解剖完整性闸门）

> **用途：** 约束Stage 03正式图片资产、Stage 03 Shot Assembly、Stage 04关键Anchor与所有将继续作为Authority被下游引用的高清静态图。

## 1｜为什么单独立闸
很多图片“氛围、构图、风格都对”，但前景可读手部一眼是错的；这种图如果进入Authority，会把错误继续带到Storyboard、Video与QC。**当前规则（Current Rule）：手部/前臂/持物接触是独立硬闸，不再被整体观感掩盖。**

## 2｜必须触发的场景
命中任一项即必须执行本闸：
1. 手部位于前景、中景或清楚可读；
2. 手部承担情绪表演（摸喉、指向、张开、抓紧、触碰自己或他人）；
3. 手部承担Held Prop / Weapon / Umbrella / Door Handle等抓握或支撑；
4. 手部是人物识别、动作因果或构图焦点的一部分；
5. 前臂、手腕、掌面与手指关系可被肉眼读取。

远景群众或模糊深背景手部不按本闸做逐指苛查。

## 3｜检查项
### 3.1 Hand Count / Silhouette
- 手指数是否合理；
- 是否有多指、少指、指头粘连、从错误位置长出额外指枝；
- 整体手型轮廓是否一眼可读。

### 3.2 Palm / Thumb / Finger Chain
- 拇指是否从合理位置连接掌面；
- 掌面朝向与手背朝向是否自洽；
- 指根、第一/第二关节链条是否成立；
- 不要求医学教科书，但不能出现一眼错误的折叠/反转/断裂。

### 3.3 Wrist / Forearm Connection
- 手腕是否接在正确前臂方向；
- 袖口、手腕、掌根过渡是否自然；
- 前臂透视与手部透视是否一致。

### 3.4 Contact / Grip Integrity
- 若在拿伞、扶人、摸喉、按门把、持武器，接触必须真的成立；
- 抓握时手指围绕对象的逻辑要成立；
- 手部不能与道具/身体穿模、融合或悬空假接触。

### 3.5 Narrative Priority
按重要性分级：
- `HERO_HAND`：前景最显眼的手 / 叙事手 / 表演手；
- `FUNCTION_HAND`：持物、支撑、接触成立所需的手；
- `SECONDARY_HAND`：可读但非焦点；
- `BACKGROUND_HAND`：远景群众模糊手。

`HERO_HAND`与`FUNCTION_HAND`出现明显错误 = 直接`ANATOMY_HAND_FAIL`。

## 4｜处置规则
- 若整体图正确，仅局部手部/腕部/接触错误：优先`LOCAL_PATCH`，不要整图重做；
- 若同组Backup不存在该问题，Backup优先升级；
- 若Primary与Backup都有相同类型手错，再Fresh Regen；
- 不得因为“其余都很好看”而放行明显前景手错。

## 5｜失败码
- `ANATOMY_HAND_FAIL`：前景/叙事/持物手存在明显手部解剖错误；
- `HAND_CONTACT_FAIL`：抓握、触碰、支撑或接触不成立；
- `WRIST_CONNECTION_FAIL`：手腕与前臂连接、朝向或透视错误；
- `HAND_PRIORITY_UNCHECKED`：明显可读手没有按Hero/Function/Secondary分类检查。
