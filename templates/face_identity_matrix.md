# Face Identity Matrix（面部个体识别矩阵）

> **用途：** 把“冷艳、温柔、清冷、成熟”等抽象气质，翻译成可被图片模型执行、可被QC比较的面部结构。避免所有人物收敛为同一张标准美型脸。

## 1｜Face ID字段

正式主要/反复角色至少记录：

1. `Face Outline`｜短椭圆 / 长椭圆 / 柔方 / 倒三角 / 菱形倾向 / 圆中带窄等
2. `Forehead & Hairline`｜额头宽窄、高低、发际线形态
3. `Bizygomatic / Cheek Rhythm`｜颧区宽度与面颊饱满/清瘦程度
4. `Midface Length`｜短 / 中 / 略长
5. `Jaw Architecture`｜柔圆 / 利落 / 略方 / 窄收
6. `Chin`｜短圆 / 尖但克制 / 长窄 / 微方 / 微翘
7. `Nose Signature`｜鼻梁强弱、鼻尖圆/锐、鼻翼视觉宽度
8. `Mouth / Lip Signature`｜唇厚薄、唇峰、嘴宽、嘴角自然趋势
9. `Eye Spacing`｜略近 / 中等 / 略开
10. `Brow-Eye Relationship`｜眉压眼/眉眼开阔、眉峰位置与走势
11. `Resting Expression`｜默认闭口与眼神状态，不等同于当前情绪
12. `Age Read / Maturity`｜年轻、成熟、疲惫、严谨等通过结构与姿态表达，不靠毛孔/摄影皱纹
13. `Distinctive Facial Feature`｜至少1个低夸张但稳定的识别点，例如略长鼻梁、偏宽嘴型、明显唇峰、左眉尾微断、轻微眼下阴影结构等

## 2｜禁止通用美脸默认值

以下组合若被多名核心角色重复使用，应主动打散：
- 小V脸 + 小鼻尖 + 同款大杏眼 + 同款微笑唇；
- 女性一律尖下巴、窄脸、同眼距；
- 男性一律窄长脸、高鼻梁、薄唇、同眉峰；
- 年龄差只靠发色/衣服，不改变中面部、下颌、嘴型与成熟度。

## 3｜Profile Identity（侧脸识别）

SIDE FACE必须定义：
- 额头到鼻根的转折；
- 鼻梁曲线与鼻尖方向；
- 上下唇前后关系；
- 下巴投影；
- 下颌到耳下转折；
- 眼窝与睫毛侧面轮廓。

若SIDE FACE只是把正脸“旋转90度的通用模板”，判`FACE PROFILE GENERIC`。

## 4｜3/4 Face Check

主要/反复角色的`DF-02`必须证明：
- 脸型在3/4角仍然成立；
- 颧区、鼻、嘴、下颌不是模型随机重绘；
- 不因角度变化突然变成另一名角色的标准脸。

## 5｜Collision Gate

与最接近现有角色比较以下非颜色字段：
`Face Outline / Midface / Jaw / Chin / Nose / Mouth / Eye Spacing / Brow-Eye / Resting Expression / Distinctive Feature`

### P0
若同时高度相同：
- Face Outline
- Jaw/Chin
- Eye Spacing/Brow-Eye
- Nose/Mouth中的至少一组

且主要差异只剩发色/发型/服装，判：
`FACE TEMPLATE COLLISION`。

### PASS
- 与最相近角色至少4个非颜色结构字段有清楚差异；
- 遮住头发和服装时仍能用结构性语言区分；
- 差异保持美型，不靠夸张畸变。
