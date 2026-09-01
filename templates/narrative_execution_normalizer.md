# Narrative → Execution Normalizer（导演/文学语言到可执行状态归一器）｜Current Authority

> **目的：** 保留导演层的文学性，但禁止含混诗句直接穿透到视频模型。Final Prompt只写可观察的画面、动作、声音与时间关系。

## 1｜必须归一化的语言
- 抽象心理：“他等着必然会来的惊叫” → 具体等待姿态、视线/不转身、声音环境。
- 诗性省略：“少的是人” → “机械声和雨刷仍在，但没有人开口或惊叫”。
- 模糊镜头：“静止或轻推” → 返回Camera Owner要求唯一决策；Normalizer不能替Camera随机选。
- 泛化声音：“无人声” → 先查Typed Audio State；若Nonverbal Breath=ON，不得输出覆盖它的总禁令。

## 2｜原则
- `Narrative Intent`保留在Director/Sequence内部；
- `Model Execution Language`只保留可观察事实；
- 任何一句如果可能被模型按字面理解成另一个World State，必须改写；
- 不为了“电影感”加入无来源的动作、慢镜、静止、镜头运动。

## 3｜Hard Fail
`POETIC_LITERALIZATION_RISK / ABSTRACT_STATE_LEAK / AMBIGUOUS_OR_BRANCH`未解决 → 不得进入Final Prompt。
