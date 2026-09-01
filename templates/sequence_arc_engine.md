# Sequence Arc Engine（场景序列弧线引擎） Current Authority

> **用途：** 在Detailed Shot Contract之前，把Scene/Segment看成一个连续的观众体验，而不是一组各自“合理”的镜头。

## 1｜Sequence Contract

```text
Sequence ID：
Selected Directorial Thesis：
Opening Image Function：
Closing Image Function：
Audience Attention Arc：
Knowledge Arc：
Distance Arc：
Perspective / Alignment Arc：
Optical / Focus Arc：<仅当Lens Family、DOF或焦点访问本身推动叙事时填写>
Performance Access Arc：
Viewpoint Arc：<观众的观察位置/角色对齐如何转移；按editorial_grammar_engine.md>
Editorial Rhythm Arc：<Hold / Cut / Contrast如何形成节奏，不等同于平均Shot Length>
Cut Density Arc：
Reaction Economy：
Withhold → Reveal Map：
Visual Motif / Recurrence：
Sound / Silence Arc：<适用时>
```

## 2｜Beat Function Table

| Beat | Audience Knows Before | Attention Owner | What Changes | Show / Withhold | Distance/Perspective/Focus | Performance Access | Cut/Hold Function | End State |
|---|---|---|---|---|---|---|---|---|
| B01 | | | | | | | | |

每个Beat必须增加至少一种东西：知识、权力、空间、情绪、动作状态、期待或对已有信息的重新解释。

如果镜头/Beat只重复已经知道的东西，先问是否应该删除/合并/保持同Shot。

## 3｜Reaction Economy

Reaction Shot不是默认语法。每个Reaction至少回答一种功能：
- 新信息进入角色；
- 关系权力改变；
- 角色隐藏/失败隐藏某种反应；
- 观众需要重新解释前一个动作；
- Reaction本身触发下一个Beat。

若只是“对方说话所以切到听者”，标`REACTION_COVERAGE_REDUNDANCY`。

## 4｜Performance Access Arc

导演明确何时允许观众看清脸：
- `DENIED`：故意不给脸/不给完整反应；
- `PARTIAL`：侧脸、背影、遮挡、距离；
- `OPEN`：允许完整表演读取；
- `INTIMATE`：需要细微眼神/嘴角/呼吸等。

Close-up不是奖励。只有Sequence需要提高Performance Access时才靠近。

## 5｜Cut Density Arc

定义一场戏的切换密度如何变化，而不是均匀切：
- `SUSTAINED`：长时间保持；
- `SPARSE`：少量有意义切换；
- `ACCELERATING`：信息/动作压力上升；
- `FRAGMENTED`：主观失衡/动作冲击；
- `RELEASE`：切换变少或回到更完整空间。

任何密度变化都必须有戏剧原因。

## 5.5｜Editorial Handoff

Sequence Arc锁定后必须交给`editorial_grammar_engine.md`先建立Editorial Intent Draft；Formal Shot Progression确定后再锁`EDITORIAL_PLAN`。`Cut Density Arc`只定义密度趋势，真正的`Viewpoint Role / Cut Trigger / Cut Timing / Transition / Continuity Strategy`由Editorial Authority拥有。不得让Detailed Shot Contract各自独立决定切点，造成局部合理、整体单调。

## 6｜Sequence Hard Fail

- `SEQUENCE_ARC_FLAT_FAIL`：镜头顺序只有景别变化，没有观众体验推进；
- `REACTION_COVERAGE_REDUNDANCY`：反应镜头只是覆盖习惯；
- `CUT_DENSITY_MECHANICAL_FAIL`：一句一切/固定节奏；
- `PERFORMANCE_ACCESS_RANDOM_FAIL`：Close/Wide没有与观众访问角色内心的需求相关；
- `REVEAL_ORDER_FAIL`：重要信息被过早展示或晚到失去意义。
