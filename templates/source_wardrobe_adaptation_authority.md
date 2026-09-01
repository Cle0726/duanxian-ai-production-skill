# Source Wardrobe Adaptation Authority（小说/剧本服装改编权限）

> **核心原则：** **小说锁剧情必要字段；Skill负责人物最终服装美术。**
>
> 普通小说服装描写不是最终Character Design Lock。只有真正影响剧情、身份、连续性或因果的服装事实才拥有硬Authority。

---

## 1｜Source Wardrobe Classification

### `WARDROBE_PLOT_FACT`
服装事实直接参与剧情/因果/连续性。

例：浅色衣料必须让血迹可见；某件制服用于身份识别；衣物内藏关键物；剧情明确换装/伪装；某件衣物损坏/遗失影响后续。

→ 只锁必要字段，其余仍由Skill设计。

### `WARDROBE_SIGNATURE_CUE`
小说反复强调、能帮助人物身份，但并非每个裁片都必须照抄。

→ 保留核心意象/功能，允许重新美术化。

### `WARDROBE_DESCRIPTIVE_CUE`
普通氛围性描述，如“黑裙、灰外套、白衬衫、深色长裤”。

→ Soft Evidence，只提供气质/正式度/综合色倾向，不得直接变成Prompt硬锁。

### `NO_WARDROBE_CONSTRAINT`
小说没有有效服装约束。

→ 完全由Skill Wardrobe设计。

---

## 2｜Authority Order

1. 用户最新明确要求 / Approved Visual Canon；
2. 真正的`WARDROBE_PLOT_FACT`必要字段；
3. 当前Approved Character / LOOK / Closet + World State；
4. Stage 02 Character Costume Dramaturgy（WHY）；
5. Stage 03 Skill Wardrobe Authority：Fashion DNA + Diversity + Body Identity/Presentation + Appeal + Project Wardrobe Canon + Scene Conditions；
6. Signature Cue；
7. Descriptive Cue。

普通小说描写不得压过当前Approved Visual Canon或Skill的正式美术系统。

---

## 3｜Adaptation Rule

例如小说写“凯登穿黑色大衣”。若黑色大衣不承担剧情硬因果，可提取为：
`dark / reserved / outerwear / formal-cold-weather impression`

最终可以由Skill重新决定具体：
- 外套类别；
- 长短；
- 剪裁；
- 内搭；
- 材质；
- 综合色关系；
- Body Presentation；
- Styling。

不得把一句普通 prose description 变成长期角色制服。

---

## 4｜Hard Gates

### `NOVEL_WARDROBE_LITERALISM_FAIL`
普通小说服装描写被错误提升为最终美术硬锁，导致Character Fashion DNA、Diversity或当前Styling失效。

### `STORY_WARDROBE_FACT_LOSS_FAIL`
Skill重新设计时丢失了真正影响剧情/身份/连续性的服装必要字段。

---

## 5｜Existing Approved Look Protection

升级Skill后，既有Approved LOOK不会因为小说原文写法不同而自动失效。只有：
- 用户明确要求重设计；
- Story Plot Fact确实冲突；
- 既有Look发生生产级错误；

才进入最小修订。
