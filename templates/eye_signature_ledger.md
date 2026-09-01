# Eye Signature Ledger（角色眼部身份与圣谱者唯一签名台账）

> **用途：** 防止《断弦之歌》角色在基础眼型、眉眼关系、虹膜与变身Graphic Eye上逐渐收敛成“同款眼睛换颜色”。日常人物使用`Base Eye Identity`；圣谱者在此基础上建立少数强记忆点的`Transformation Eye Signature`。
>
> **维护原则：** 自动读取现有角色设定 / Approved资产后填写。资料不足写`UNKNOWN / UNIQUENESS REVIEW PENDING`，不得凭空补造。

## 1｜Base Eye Identity Fields

| Field | 含义 |
|---|---|
| Character ID / Name | 角色 |
| Base Eye Aperture | 眼裂长宽、圆/窄、杏仁/刀锋等 |
| Outer-corner Trend | 平 / 微上挑 / 明显上扬 / 下垂 |
| Upper Lid Geometry | 上眼睑弧线与折线 |
| Lower Lid Geometry | 下眼睑结构 |
| Brow-Eye Relationship | 眉眼距离、眉峰位置、走势 |
| Lash Organization | 睫毛团簇与重点 |
| Iris Scale / Position | 虹膜尺度、露白与位置 |
| Default Gaze | 默认视线气质 |

基础眼部先保证“同一个人”，不因为变身被换成另一种模板眼型。

## 2｜Transformation Eye Signature Fields

| Field | 含义 |
|---|---|
| Eye Makeup Presence | MINIMAL / STANDARD / EXPRESSIVE；正式变身态禁止NONE |
| Primary Eye Signature | 唯一主记忆点 |
| Primary Signature Channel | IRIS_ARCHITECTURE / GRAPHIC_EYELINER / EYESHADOW_PLANE / MULTI_ZONE_EYE_GRAPHIC |
| Secondary Graphic Signature | MAIN/CORE REQUIRED；SUPPORT可NONE |
| Periocular Emblem | 0–1，可NONE |
| Musical Origin Source | Notation / Rhythm / Resonance / Instrument / Voice / Phrase等 |
| Translation Level | LITERAL_NOTATION / DERIVED_MUSICAL_GLYPH / MUSICAL_GEOMETRY |
| Musical Origin Trace | 音乐身份如何变成Graphic |
| Core Pupil Symbol | 角色专属瞳孔核心；必要时可与Primary重合 |
| Iris Architecture | 环、放射、裂纹、偏心、纵核等 |
| Graphic Eyeliner / Shadow Silhouette | 中距离可读的大图形 |
| Eyeshadow Finish | Supporting Material |
| Symmetry Rule | 对称 / 单眼主导 / 刻意缺损 |
| Side-View Makeup Profile | 侧脸可读结构 |
| Material Metaphor | 材质隐喻 |
| Color Family | 辅助综合色，不作为唯一差异 |
| Formation Order | TE-02形成顺序 |
| Cross-Core Echo | 与礼服/发型/武器的呼应 |
| Approved Authority | TE-03 / TF来源 |
| Collision Notes | 与最接近角色的差异 |

## 3｜Visual Priority Rule

设计顺序固定为：
`Base Eye → Primary → Secondary → optional Periocular → Supporting Fields`

不能反过来先填：眼影层数、金粉、谱线、小纹样、下眼符号、睫毛、颜色，再试图从一堆细节里找Primary。

MAIN / CORE角色如果无法在一句话内说出Primary + Secondary，判`EYE_SIGNATURE_OVERDESIGN_FAIL`。

## 4｜Collision Matrix

### Base Eye
与最接近主要角色至少在以下3项形成清楚非颜色差异：
`Aperture / Outer-corner / Lid / Brow-Eye / Lash / Iris Scale / Default Gaze`

### Transformation Eye
重点比较：
`Primary Signature / Primary Channel / Secondary Graphic / Iris Architecture / Graphic Eyeliner-Shadow Silhouette / Symmetry / Side-View / Formation`

P0直接失败：
- Core Pupil完全相同且没有剧情共享机制；
- Primary高度相同，只换颜色；
- 相同虹膜 + 相同外眼角Graphic；
- 标准音符贴在同一位置，只改综合色；
- Periocular Accent被当成唯一差异，主眼部实际上相同；
- 两个角色都拥有很多不同小细节，但缩小后主轮廓仍无法区分。

## 5｜PASS最低条件

- Base Eye至少3项非颜色结构差异；
- Primary Eye Signature无碰撞；
- MAIN/CORE的Secondary Graphic也无高相似；
- Color只是强化识别，不承担主要区别；
- 中距离读主Graphic，近距离读Iris / Accent；
- 音乐来源能追溯，但不强迫最终仍是标准Notation。

## 6｜Approved Authority

TE-03 APPROVED后，Ledger记录与`musical_eye_motif_registry.md`同步。下游不得自由“美化”Primary / Secondary；如果剧情需要真正改变眼部Canon，必须回Stage 03建立新Approved State，而不是Stage 04/05自行发挥。
