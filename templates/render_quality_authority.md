# Render Quality Authority（成片画质权限）

> **用途：** 规定Stage 05最终画面的对象结构与细节从哪里来。当前规则统一使用`Approved HD Object Authority`，不再要求每个对象机械回到Parent Master。

## 1｜核心原则

**Control Authority ≠ Object Fidelity Authority。**

最终画面不存在一张“综合画质母图”。每个可见对象只从当前Task最直接的Approved高清对象Authority恢复正式结构与细节：
- 人物：Character / Transformation / 必要Detail Authority；
- 场景：当前Shot匹配的Environment Derived Coverage优先，没有Coverage或Coverage缺Canon字段时才补Canon Master；
- 道具/武器：当前Visible Side / State匹配的Prop / Weapon Coverage优先，必要时补Canon Master；
- 绘画语言：Project Style DNA，必要时Render Style Anchor只作style-only控制；
- 摄影语法：必要时Cinematic Shot Style Anchor提供项目级镜头组织倾向，但不覆盖具体Storyboard；
- 综合色/光色：按Global Color DNA → Scene Color Extension → Shot Lighting Variant选择当前最直接层级；
- Storyboard：Shot / Composition / Action Anchor；
- Ending Frame：起始连续性。

## 2｜Approved HD Object Authority

高清对象Authority进入模型统一标记：`HD_OBJECT_AUTHORITY_IMAGE`。Approved Production Support / Additional Video Conditioning Keyframe使用`HD_PRODUCTION_SUPPORT_IMAGE`：它可以提供当前Shot高分辨率的交互/接触/具体Shot组合证据，但不得覆盖对象Canon。Approved Shot Assembly使用`HD_SHOT_ASSEMBLY_IMAGE`：它可以提供多人关系、人景物组装与空间占位证据，但最终对象结构仍以对应`HD_OBJECT_AUTHORITY_IMAGE`为准。

它可以是：
- Canon Master；
- Derived Coverage；
- Detail Master；
- Transformation/Weapon等专项高清Authority。

选择依据不是“谁更上游”，而是：

`Key Visible Asset Coverage → Task Relevance → Field Directness → Approval → Fidelity → Minimum Sufficient Reference Set`

### 场景示例
当前镜头是舞台左后方反拍，已有Approved Left-Reverse Coverage：
- Left-Reverse Coverage = PRIMARY；
- 正面Canon Master只有Coverage缺固定结构字段时才SUPPORT；
- Coverage足够时正面Canon Master不上传。

### 道具示例
当前镜头是打开怀表的俯拍特写，已有Open-Insert Coverage：
- Open-Insert Coverage = PRIMARY；
- 闭合正面Canon Master不因“正式母图”自动加入。

## 2.1｜HD Production Support不等于新Canon

`HD_PRODUCTION_SUPPORT_IMAGE`可以比低清Storyboard更直接地提供当前Shot的高清接触/组合/短暂状态证据，但它的权限只覆盖Support Contract写明的字段。

- Stage 03 Support：Interaction / Contact / Transient / Entity Action State；限定Scope的Lightweight Interaction Prop / Shot Detail还可承担当前Scene/Shot局部外观证据，但不产生项目级Canon；
- Stage 04 Additional Video Conditioning Keyframe：Approved Storyboard锁定后的Exact Shot Composite；
- Identity / Object Structure / Geography仍由最直接`HD_OBJECT_AUTHORITY_IMAGE`负责；
- Support与对象Authority冲突时，不允许Support“因为更像最终镜头”反向改Canon。

如果Approved Additional Video Conditioning Keyframe已经完整承载当前Shot Composite，只对重复的Composite/Contact字段做视觉去重；Storyboard若仍承担Temporal Beat、Action Sequence或多Panel状态递进，继续保留相应视觉输入。不得用单帧Anchor整资产替代Storyboard。

## 2.2｜HD Shot Assembly不等于对象Canon

`HD_SHOT_ASSEMBLY_IMAGE`可以锁多人关系、人物在空间中的位置、人景物整体同框；一次性`SCOPED_CAST / NON_RECURRING`也必须先使用Approved FMH/Minor Human Master作为Appearance Authority，Assembly只承担关系/同框字段。反复/命名人物身份、关键Prop结构、当前Environment方向如果没有被对应正式Authority清楚锁住，仍必须保留最直接`HD_OBJECT_AUTHORITY_IMAGE`。不能为了减少图片输入让Assembly承担它没有实际承载的字段。

## 3｜Control References

- Storyboard：构图、机位、动作Anchor；
- Ending Frame：起始连续性；
- Render Style Anchor：绘画语言；
- Cinematic Shot Style Anchor：摄影语法，不覆盖具体Storyboard；
- Global/Scene Color Reference：当前综合色；Shot Lighting Variant通常TEXT_CONTROL。

以上控制图都不得成为对象高频细节、分辨率、锐度或最终清晰度来源。

## 4｜Quality Re-Synthesis

若控制参考存在九宫格低细节、截图压缩、运动模糊、草图简化等问题，只继承被授权字段。对象结构与材质重新依据当前`HD_OBJECT_AUTHORITY_IMAGE`合成。

不要通过“忠实复制整张低清控制图”实现连续性或构图。

## 5｜Compiled Render Fidelity Clause

内部仍按本文件的Object Fidelity / Control职责完成Reference解析；最终Copy Surface**不得输出“Render Quality Lock / Reference Pack / Approved Authority / Support / Assembly / Canon”等内部术语**。Compiler只注入一次直接可执行的画面保真句，例如：

```text
保持已绑定角色、场景与关键道具的既定外观、结构、材质和清楚可见的细节；构图或动作参考只用于保持镜头关系，不继承其中的低清、简化、宫格或草图质感。最终画面以完整、稳定、自然融合的高细节重新呈现，不因控制参考的画质而降低成片细节。
```

若当前任务不需要额外保真句，且主体/环境/连续性字段已经完整表达，可由Semantic Dedup省略，不为“有模块”而机械增加标题。

## 6｜Stage 05 Gate

- [ ] 当前关键可见资产Field Coverage完整，未发生`REFERENCE_COVERAGE_GAP / REFERENCE_SLOT_OVERFLOW`；
- [ ] 已通过`REFERENCE_RELEVANCE_FAIL`与`REFERENCE_FIDELITY_FAIL`；
- [ ] 当前关键对象的必要字段都有最直接Approved HD Object Authority或明确TEXT Authority；
- [ ] 当前Shot已有Coverage时，没有无理由把Parent Master重新拉回Primary；
- [ ] Storyboard / Ending Frame / Render Style / Cinematic Shot Style / Color Reference没有承担对象高清细节；
- [ ] 若需要Compiled Render Fidelity Clause，只出现一次且使用直接画面语言；
- [ ] 临时图、失败图、低清宫格、截图没有升级为高清对象Authority。


> 当前项目所有“构图/动作参考”在Video阶段均指静态Storyboard/Key Pose/Ending Frame或结构化Metadata，**不包含参考视频**。
