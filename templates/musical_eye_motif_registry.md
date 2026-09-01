# Musical Eye Motif Registry（圣谱者音乐眼部签名注册表）

> **用途：** 项目级维护所有圣谱者的Eye Graphic Ownership，避免角色增加后退化成“大家都有音符、只是颜色和位置不同”。
>
> **核心原则：** `Reserve the graphic signature, not the notation symbol.`

---

## 1｜Registry Fields

| Field | 含义 |
|---|---|
| Character ID / Name | 角色 |
| Character Tier | MAIN / CORE / SUPPORT |
| Status | PLANNED / TF CANDIDATE / TE-03 APPROVED / DEPRECATED |
| Music Identity Ref | 当前Music Identity Card |
| Primary Eye Signature | 唯一主眼部记忆点 |
| Primary Signature Channel | IRIS_ARCHITECTURE / GRAPHIC_EYELINER / EYESHADOW_PLANE / MULTI_ZONE_EYE_GRAPHIC |
| Secondary Graphic Signature | MAIN/CORE必填；SUPPORT可NONE |
| Periocular Emblem | 0–1个眼周Accent，可NONE |
| Musical Origin Source | Notation / Rhythm / Resonance / Instrument / Voice / Phrase / 其他音乐机制 |
| Translation Level | LITERAL_NOTATION / DERIVED_MUSICAL_GLYPH / MUSICAL_GEOMETRY |
| Musical Origin Trace | 从Music Identity到最终Graphic的可解释路径 |
| Iris Architecture | 虹膜拓扑 / 内外环 / 核心关系 |
| Core Pupil Symbol | 若有，角色唯一；可与Primary重合 |
| Graphic Eyeliner / Shadow Silhouette | 中距离可读的眼周大图形 |
| Symmetry Rule | 对称 / 单眼主导 / 刻意缺损 |
| Side-View Read | 侧脸仍可识别什么 |
| Material Language | 谱墨 / 金属粉 / 玻璃层 / 丝绒雾面 / 光刻等 |
| Formation Order | TE-02形成顺序 |
| Costume / Hair / Weapon Echo | Cross-Core Echo |
| Reserved Signature | `Primary + Secondary + Channel + major geometry`组合 |
| Collision Notes | 与最接近角色的差异 |
| Approved Authority | TE-03 / TF-01版本 |

---

## 2｜角色等级

### MAIN
- Primary必须能一句话记住；
- Secondary必须来自不同视觉通道；
- Periocular Emblem按需要0–1，不为了“更复杂”强加；
- Cross-Core Echo至少在Costume / Hair / Weapon中形成2处强回应；
- 推荐优先考虑`DERIVED_MUSICAL_GLYPH`或高识别`MUSICAL_GEOMETRY`，避免标准符号贴脸。

### CORE
- Primary + Secondary必须清楚；
- 至少与Costume或Weapon形成一个强Echo；
- 完整执行Collision Check。

### SUPPORT
- Primary必须清楚；
- Secondary / Periocular可NONE；
- 允许更简洁，但不得复制MAIN/CORE的Reserved Signature。

---

## 3｜音乐来源规则

Registry不再规定“每人必须占用一个真实Notation Anchor”。音乐身份可以通过：
- 标准Notation；
- 从Notation拆解出的角色Glyph；
- Rhythm / Phrase / Resonance的图形结构；
- Instrument / Voice mechanics；
- 其他项目Canon音乐机制

进入眼部。

如果使用标准音符/谱号，必须说明它为什么属于该角色，而不是因为“音乐角色就贴音符”。

---

## 4｜Collision Rules

### P0 Collision
出现任一项即失败：
- 相同Primary Eye Signature只换综合色；
- 相同Primary Channel + 近似大轮廓 + 近似Secondary，只镜像/旋转/缩放；
- 相同Iris Architecture + 相同Graphic Eyeliner Silhouette；
- 新角色复用MAIN/CORE Reserved Signature；
- 两个角色都靠同一标准Notation贴在同一眼周位置，仅改颜色。

状态：`MUSICAL EYE REGISTRY COLLISION`。

### 可接受的Source复用
多个角色可以同属NOTE / STAFF / RHYTHM / RESONANCE等来源，但最终至少在以下3项形成清楚差异：
- Primary Signature Channel；
- Primary Geometry；
- Secondary Graphic；
- Iris Architecture；
- Symmetry；
- Side-View Read；
- Material Language；
- Formation Order。

---

## 5｜设计前检查

1. 读取已有Approved TE-03 / Registry；
2. 确定Character Tier；
3. 从Music Identity先提出**Primary候选**，不是先填满所有眼妆字段；
4. 只在Primary成立后设计Secondary与可选Periocular；
5. 做全项目Collision；
6. Candidate阶段临时Reserve；
7. TE-03批准后升级为`APPROVED RESERVED SIGNATURE`。

如果Primary不能一句话说明，或必须靠五六个小细节才能成立，返回设计阶段做减法。

---

## 6｜下游继承

TE-03批准后，以下字段不可自由漂移：
- Primary Eye Signature；
- Primary Signature Channel；
- Secondary Graphic Signature；
- Periocular Emblem（若有）；
- Iris Architecture / Core Pupil；
- Graphic Eyeliner / Shadow Silhouette；
- Side-View Read；
- Formation核心顺序；
- Cross-Core Echo。

Storyboard / Video若眼部可读，应优先调用TE-03，不靠文字重新解释。
