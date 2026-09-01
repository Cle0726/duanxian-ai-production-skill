# Narrative FX Asset Standard（叙事特效资产标准）

> **Owner：非战斗/非纯Transformation的剧情型视觉现象。** Combat VFX仍由`cinematic_combat_vfx_engine.md`拥有，Transformation FX仍由`transformation_asset_standard.md`拥有；本文只处理“失声、异常灯光、特定血滴/悬停、共鸣异常、重复性环境现象”等具有叙事身份的视觉语法。

## 1｜核心原则

不是每个特效都要母图；但**有剧情身份的视觉现象不能每镜重新发明。**

当某个FX满足下列任一条件时，Stage 02应考虑建立`NARRATIVE_FX_ASSET_MANIFEST`：

- 跨多个Shot/Scene重复出现；
- 是观众识别某个异常/规则/线索的视觉标志；
- 状态阶段（开始/发展/完成/余波）必须稳定；
- 与环境材质/光线/物体有特定交互，Video自由猜会破坏设定；
- 单次虽短，但属于剧情关键揭示且形态歧义高。

## 2｜Authority Mode

### `TEXT_GRAMMAR_ONLY`
用于简单、一次性、低歧义效果。只在Prompt/FX Grammar中描述，不建立正式图片Reference。

### `NARRATIVE_FX_REFERENCE`
用于重复、剧情识别、连续性或高歧义现象。Stage 03建立Approved静态Reference/State Sheet。

高风险`SIGNATURE_PHENOMENON / CONTINUITY_STATE`不得用`TEXT_GRAMMAR_ONLY`逃避视觉Authority。

## 3｜资产类型

- `NARRATIVE_FX_REFERENCE`：单一关键状态的高清静态视觉Reference；可在Resolver判定必要时直接作为图片Reference；
- `NARRATIVE_FX_STATE_SHEET`：开始/中间/完成/余波等多状态视觉拆解页，主要用于Canon与下游Execution Frame派生；默认不直接作为Video Primary Visual。

Reference必须是`media_kind=IMAGE`。项目执行策略**禁止Reference Video**，因此Narrative FX不能通过动作参考视频/特效参考视频补齐。

## 4｜可拥有与不可拥有

Narrative FX Authority可以锁：

- 形状/轮廓/层级；
- 材质与综合色倾向；
- 状态节点的可见差异；
- 与环境/物体的静态交互方式；
- 遮挡层级与大致空间深度；
- 是否发光、是否有粒子/纸屑/雾、衰减后的残留形态。

不能锁：

- 完整时间曲线、速度、节拍、Camera Motion；
- 人物Identity；
- Environment Geography；
- Prop主体结构（除非Effect本身就是该主体的状态层）；
- Storyboard动作Beat顺序。

## 5｜状态覆盖

每个需要正式Reference的FX必须声明`required_visual_states[]`，例如：

- `START`
- `DEVELOPING`
- `PEAK`
- `END`
- `AFTERMATH`
- `STATIC`

Asset Registry中的`fx_state_ids`必须覆盖Manifest要求的状态。多状态可以由一个State Sheet覆盖，也可以用多个单帧Reference覆盖。

## 6｜例子

- 全城失声：如果其视觉表现有固定环境反应/物体状态/人物周围表现 → Narrative FX；如果纯粹是“声音消失”且没有稳定可视形态，则保持Audio/Performance/Editorial语义，不凭空造发光罩；
- 路灯异常闪烁：若只是Timing问题，Text Grammar即可；若有固定“逐格熄灭”视觉规则且反复出现，可建立状态Reference；
- 特定悬停血滴：若它承担异常规则线索且形态/空间位置需一致，可建立Narrative FX Reference；
- 普通烟尘、普通雨滴飞溅、普通冲击火花：默认不升级Canon。

## 7｜Freeze硬门

若`authority_mode=NARRATIVE_FX_REFERENCE`，Freeze前必须：

- 至少一个Approved `NARRATIVE_FX_REFERENCE`或`NARRATIVE_FX_STATE_SHEET`；
- Registry中的`narrative_fx_id`与Manifest一致；
- `authority_role=NARRATIVE_FX_AUTHORITY`；
- `media_kind=IMAGE`；
- required states全部覆盖；
- `primary_visual_eligible=false`；
- State Sheet若是`MULTI_PANEL`，默认`direct_input_allowed=false`；需要Video直接参考时由Resolver选择单帧状态Reference或让Shot Execution Frame吸收。

失败码：

- `NARRATIVE_FX_REFERENCE_REQUIRED`
- `NARRATIVE_FX_ASSET_MISSING`
- `NARRATIVE_FX_STATE_COVERAGE_GAP`
- `NARRATIVE_FX_MEDIA_KIND_FAIL`
- `NARRATIVE_FX_AUTHORITY_ROLE_FAIL`
- `NARRATIVE_FX_ENTITY_SCOPE_MISMATCH`
- `NARRATIVE_FX_STATE_SHEET_DIRECT_REFERENCE_FORBIDDEN`

## 8｜与Reference Resolver的关系

Stage 03建立完整FX Authority不代表Stage 05全部直绑。

- 当前Execution Frame已把该FX状态稳定烘焙，且没有额外形态风险 → `LINEAGE_ONLY`；
- FX形态是当前镜头核心且Primary Visual不足以稳定 → 直接绑定当前状态的`NARRATIVE_FX_REFERENCE`；
- State Sheet主要作为生成Execution Frame/静态合成的上游Authority，不默认直接塞给Video。
