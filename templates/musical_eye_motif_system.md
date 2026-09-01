# Musical Eye Motif System（音乐图形化眼部签名系统）

> **用途：** 把《断弦之歌》圣谱者变身眼部定义为全剧核心视觉商标，但避免“字段很多、每处都设计、最后没有一个记忆点”以及“普通眼妆上贴一个♪”两种失败。
>
> **核心原则：** `Few strong graphic decisions first; engineering fields only protect them.`

---

## 1｜P0总纲

所有剧情明确可变身的圣谱者，其`Transformation Eye Signature`必须同时满足：
1. **Base Eye Continuity**：变身前后仍能认出同一个人的基础眼型、眉眼关系与视线气质；
2. **Eye Makeup Presence ≠ NONE**：正式变身态眼妆可MINIMAL / STANDARD / EXPRESSIVE，但不可完全缺席；
3. **Primary Eye Signature = REQUIRED**：只选一个最强、最先被记住的眼部视觉决定；
4. **Secondary Graphic Signature**：MAIN / CORE角色必须有一个次级Graphic Signature；SUPPORT可按需要为NONE；
5. **Periocular Emblem = 0–1**：眼下 / 外眼角 / 颧骨上方 / 太阳穴 / 眉尾附近最多一个辅助纹章，不强迫每人都有；
6. **Musical Origin Trace = REQUIRED**：Primary / Secondary必须能追溯到该角色Music Identity，但最终不要求保持教科书式音符外形；
7. **角色专属**：读取`musical_eye_motif_registry.md`做全项目碰撞；
8. **Beauty Core同源**：眼部与礼服、头发、音乐武器共享同一Music Identity；
9. **远近两级可读**：中景先读到Graphic Silhouette，近景再读到虹膜、材质与细部，不把辨识度全部压在ECU才看见的小符号上。

---

## 2｜三层视觉优先级

### 2.1 Primary Eye Signature｜主眼部签名

**只能有一个主导记忆点。** 可由以下任一通道承担：
- `IRIS_ARCHITECTURE`｜强烈的虹膜拓扑 / 内外环 / 纵向或偏心核心；
- `GRAPHIC_EYELINER`｜远一点仍能改变眼睛外轮廓的图形眼线；
- `EYESHADOW_PLANE`｜大块面、切面、断裂、回环或不对称眼影轮廓；
- `MULTI_ZONE_EYE_GRAPHIC`｜跨上眼、外眼角、下眼尾形成一个整体图形，但仍视为**一个**主签名。

Primary必须能用一句短语记住，例如：
> “双环虹膜 + 纵向裂核”应进一步压缩为主签名“纵裂双环虹膜”；其他结构降为Supporting Field。

### 2.2 Secondary Graphic Signature｜次级图形签名

MAIN / CORE角色再选一个**不同通道**的次级签名，例如：
- 主签名=虹膜结构 → 次签名=红黑锐角眼线；
- 主签名=不对称眼影切面 → 次签名=偏心金属内环；
- 主签名=外眼角谱句形状 → 次签名=下眼缘断奏点列。

Secondary必须支持Primary，不能和Primary争夺视觉中心。

### 2.3 Periocular Emblem｜眼周纹章

最多0–1个，小而明确。位置允许：
`UNDER_EYE / OUTER_EYE / UPPER_CHEEKBONE / TEMPLE / BROW_TAIL`

它可以来自音符、休止、谱号碎片、节拍记号，也可以是从Music Identity衍生的角色Glyph。**它是Accent，不是用来弥补主设计太普通。**

---

## 3｜Musical Translation Spectrum（音乐转译层级）

音乐来源必须存在，但最终视觉允许三种路线：

### `LITERAL_NOTATION`
仍能直接看出音符、谱线、休止、谱号或演奏记号。适合角色主题确实需要“直接记谱感”的设计。

### `DERIVED_MUSICAL_GLYPH`｜推荐核心路线
从音符头/符干/谱线/谱号/演奏记号、乐器结构或节奏图形中拆解、拉伸、重组，形成**属于角色自己的Glyph**。观众能感到音乐来源，但不会像贴标准符号。

### `MUSICAL_GEOMETRY`
音乐已高度抽象成节奏、间隔、回环、断裂、重音、共鸣、声部层次或乐器机械关系。最终不要求肉眼读出标准Notation，但必须有清楚的`Musical Origin Trace`解释“从哪里来、为什么是这个结构”。

**禁止把`MUSICAL_GEOMETRY`理解成任意漂亮幻想纹样。** 如果删除说明后和普通魔法眼妆没有任何结构差异，仍然失败。

---

## 4｜Musical Origin Sources（来源不等于最终图标）

可来自但不限于：
- Note / Rest / Staff / Clef / Articulation / Ornament；
- Rhythm / Syncopation / Repetition / Pause / Phrase Break；
- Interval / Counterpoint / Call-and-response；
- Resonance / Harmonic Nodes / Wave / Overtone；
- Instrument Geometry / Key / String / Bow / Reed / Bell / Hammer / Mechanism；
- Voice / Breath / Attack / Sustain / Decay；
- 角色剧情已确认的其他Music Identity机制。

**来源越具体，不代表最终越要字面化。**

---

## 5｜Supporting Fields（支持字段，不得抢主次）

以下仍然记录，但职责变成“稳定复现Primary / Secondary”，而不是每一项都必须独立炫技：
- Eye Makeup Presence / Density；
- Iris Topology / Core Pupil Symbol；
- Eyeshadow Coverage / Geometry / Finish；
- Eyeliner Geometry；
- Lash Organization；
- Symmetry Rule；
- Side-View Makeup Profile；
- Material Metaphor；
- Color Family；
- Formation Sequence；
- Costume / Hair / Weapon Echo。

如果Supporting Fields让眼部出现四五个同等级焦点，判`EYE_SIGNATURE_OVERDESIGN_FAIL`。

---

## 6｜Graphic Readability

### Medium Read
在MCU / CU之外稍远的脸部尺度，至少能读到：
- Primary Eye Signature的外轮廓或综合色块；
- 与普通状态明显不同的Graphic Character。

### Close Read
CU / ECU再读：
- Iris Architecture；
- 精细边界；
- Periocular Emblem（若有）；
- Material / Formation细节。

不能把整套设计建立在“只有ECU才能看到的一枚小音符”。

---

## 7｜Formation（TE-02）

TE-02按视觉优先级形成，不要求每个Supporting Field逐个表演。

优先逻辑：
`Primary Signature emergence → Secondary Graphic lock → optional Periocular Accent → micro-detail settle`

具体顺序由角色Music Identity决定。不同角色不得机械复制同一形成动画。

---

## 8｜Mandatory Canon Fields

每位正式圣谱者至少明确：
- `Base Eye Identity Ref`
- `Eye Makeup Presence`
- `Primary Eye Signature`
- `Primary Signature Channel`
- `Secondary Graphic Signature`（MAIN/CORE REQUIRED；SUPPORT可NONE）
- `Periocular Emblem`（0–1）
- `Musical Origin Source`
- `Translation Level` = LITERAL_NOTATION / DERIVED_MUSICAL_GLYPH / MUSICAL_GEOMETRY
- `Musical Origin Trace`
- `Iris Architecture / Core Pupil`
- `Graphic Eyeliner / Eyeshadow Silhouette`
- `Side-View Read`
- `Formation Sequence`
- `Cross-Core Echo`
- `Registry Collision Result`

---

## 9｜Hard Gates

### `MUSICAL EYE SOURCE LOST`
眼部看起来只是普通时尚/幻想眼妆，Music Identity只存在于说明文字或服装上。

### `MUSICAL EYE STICKER FAIL`
在已经完成的普通眼妆上附加标准音符、谱线贴花，符号没有改变虹膜/眼线/眼影的Graphic Architecture。

### `EYE SIGNATURE COLLISION`
Primary + Secondary组合与其他角色高度相似，只靠颜色、镜像、旋转或小位置变化区分。

### `EYE_SIGNATURE_OVERDESIGN_FAIL`
眼部存在超过3个同等级焦点，Primary不再清楚，细节很多但无法一句话记住。

### `MUSICAL EYE ABSENCE FAIL`
正式变身态完全取消Eye Makeup / Graphic Eye Layer。

### `MUSICAL EYE CANON DRIFT`
TE-03批准后，下游自由改变Primary / Secondary / Iris Architecture / Graphic Silhouette / Periocular Emblem或Formation核心逻辑。

---

## 10｜Registry与Reference

新建/修订圣谱者眼部前必须读取`musical_eye_motif_registry.md`。Registry保留的是**视觉签名所有权**，不是“哪个人占用了哪个标准音符”。

Storyboard / Video中变身眼部达到可单独识别的可读程度时：
- `TRANSFORMATION_EYE_SIGNATURE / MUSICAL_EYE_MOTIF = CRITICAL`；
- Approved TE-03 = Most Direct Eye Authority；
- TF-01负责全身变身身份；TE-03负责精确眼部Canon；
- 不能让视频模型仅凭文字重新发明Primary / Secondary。

详细执行读取`reference_field_coverage_map.md`与`reference_resolver.md`。
