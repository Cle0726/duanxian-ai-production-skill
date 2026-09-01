# Screen Experience & Genre Pressure Engine｜屏幕体验扩展与类型压力引擎｜Current Authority

> **用途：** 解决“剧情事实拍对了，但体验被压扁”的问题。它允许在不新增Canon事实的前提下，为恐怖、悬疑、危机、追逐、怪物首次登场等场景增加必要的Screen Beat、Hold、环境反应、局部Reveal、Negative Space、Reaction与Aftermath。它不拥有世界观改写权，也不允许为了拖时长制造新剧情。
>
> **项目默认：** `PRODUCTION_PRIORITY_PROFILE = QUALITY_FIRST`。Episode Runtime以约20分钟作为**柔性参考**，不是Hard Cap；具体Scene / Sequence / Shot / Segment时长服从体验完成度。

## 0｜核心分权

必须同时区分：

- `CANON BEAT`：会改变Story State / 世界规则 / 人物关键行为结果的事实；只能来自Source / Screenplay Lock。
- `SCREEN EXPERIENCE BEAT`：不改变Canon，只改变观众如何经历已锁定事实；Stage 01B/02可在Source Anchor约束下主动增加。
- `COST / TAKE BUDGET`：决定生成几次、候选几张、是否Retry；**无权删除已批准Screen Experience Beat。**

最高规则：

> **允许增加Screen Beat，不允许增加Canon Beat。**

## 1｜合法 Screen Experience Elaboration

在不改变Locked Story Facts时，可以主动增加：

- 环境先于威胁发生的异常反应；
- Off-screen Sound / Silence / 声音中断；
- 空走廊、门框、窗洞、暗区等Negative Space；
- 人物察觉、寻找、误判、重新确认、看出口、后退、等待；
- 怪物局部肢体、影子、轮廓、反射、足迹、破坏痕迹；
- `FALSE_CLEAR / FALSE_RELIEF`；
- 威胁从远到近的Encroachment；
- Scale Anchor / Environment Proof；
- 攻击后的Result / Consequence / Aftermath；
- 为清楚读懂危险关系所需的Hold。

禁止自行增加：

- 新角色 / 新怪物；
- 新死亡 / 新重伤 / 新关键伤势；
- 新能力 / 新规则 / 新弱点；
- 改变谁赢、谁救谁、谁发现什么关键秘密；
- 提前或延后关键Reveal导致意义变化；
- 与Screenplay Lock冲突的新行动结果。

命中即：`SCREEN_EXPERIENCE_CANON_OVERREACH`。

## 2｜Episode Runtime Policy｜约20分钟，但不以20分钟反向裁剪内容

项目默认：

```text
Episode Runtime Mode = PREFERRED_AROUND_20
Preferred Runtime = 20 min
Soft Review Band = 18–22 min
Hard Runtime Cap = NONE
Over-band Policy = REVIEW_NOT_COMPRESS
Production Priority = QUALITY_FIRST
```

含义：

- 20分钟是包装/节奏参考，不是内容天花板；
- 18–22分钟只是Review Band，超出不自动失败；
- 23、24、25分钟若确实由剧情/体验自然需要，可以保留；
- 若明显过长，先找`TRUE_REDUNDANCY`，再考虑自然拆集；**禁止机械加速对白、删除Threat Build、Reaction、Aftermath或压迫Hold；**
- 若明显偏短，优先检查是否漏掉因果、空间、Reaction、Experience Pressure，不用Dead Hold填时长。

只有用户明确给出`USER_LOCKED_RUNTIME`时，时长才成为Hard Constraint。

## 3｜Experience State ≠ Story State

每个重要Screen Experience Beat同时记录：

```text
Story State Delta：NONE / LOCKED_SOURCE_FACT_ONLY
Experience State IN
Experience Gain
Experience State OUT
```

推荐Experience维度：

- `threat_pressure`：0–8；
- `audience_uncertainty`：0–8；
- `perceived_threat_proximity`：UNKNOWN / FAR / MID / NEAR / IMMEDIATE；
- `escape_security`：OPEN / THREATENED / REDUCED / DENIED；
- `character_threat_awareness`：UNAWARE / SUSPECTS / CONFIRMS / TRACKS / SURVIVAL_RESPONSE；
- `scale_understanding`：UNKNOWN / PARTIAL / CLEAR。

**剧情信息增量接近0不等于镜头无功能。** 只要Experience Gain真实存在，该Beat合法。

## 4｜Threat / Horror Coverage Roles

恐怖、危机、怪物场景按需要从下列角色中组织，不要求每场全部使用：

- `NORMALCY`：建立正常基线；
- `OMEN`：异常预兆；
- `OFFSCREEN_THREAT`：威胁存在但不可见；
- `TRACE`：环境证明威胁存在/经过；
- `NEGATIVE_SPACE_HOLD`：观众被迫观察可能出现威胁的空间；
- `PARTIAL_REVEAL`：局部身体/影子/轮廓；
- `FALSE_CLEAR`：角色/观众暂时以为安全；
- `REACTION_WITHHOLD`：给Reaction但继续不给完整答案；
- `SCALE_REVEAL`：用人物/建筑/空间参照建立尺度；
- `ENCROACHMENT`：威胁侵入安全距离；
- `ESCAPE_DENIAL`：出口/可行动空间被压缩；
- `FULL_REVEAL`：完整看见威胁；
- `COMMITMENT`：威胁真正发动行动；
- `CONSEQUENCE`：造成可读结果；
- `AFTERMATH`：让结果存在；
- `FALSE_RELIEF`：短暂释放后重新升压；
- `PAYOFF`：前面建立的压力获得结果。

### Major / Hero Threat

重大怪物首次正式登场、Boss威胁、核心恐怖Scene默认不得直接：

`NORMAL → FULL_REVEAL → ATTACK`

除非Source明确要求突然袭击。通常至少需要2类不同的Pre-Reveal / Pressure Role，或提供`IMMEDIATE_REVEAL_JUSTIFICATION`。

## 5｜Threat Pressure Arc

压力不是一直向上。允许：

`1 → 3 → 2 → 4 → 3 → 6 → 5 → 8`

其中回落可以制造False Clear / False Relief。重要的是每个变化有原因，而不是机械每镜+1。

建议语义：

0 NORMAL｜1 UNEASE｜2 ANOMALY｜3 PRESENCE SUSPECTED｜4 PRESENCE CONFIRMED｜5 ENCROACHMENT｜6 ESCAPE THREATENED｜7 IMMEDIATE DANGER｜8 BREACH / CONTACT

## 6｜Protected Experience Beat

以下Beat一旦由Director锁定，标：

`protected_from_cost_compression = true`

包括：

- Threat Build / Reveal；
- Scale Proof；
- Reaction / Perception Shift；
- Escape Denial；
- Necessary Negative Space / Anticipation Hold；
- Consequence / Aftermath；
- 关键False Clear / False Relief；
- 关键空间重建。

Cost Engine不得以“省一次15s视频 / 减少Segment / 镜头没有新剧情信息”为理由删除、合并或缩短到失效。

## 7｜No Padding Gate

Quality First不等于无限加镜头。新增Screen Experience Beat必须至少产生一个真实`experience_gain`：

`PRESSURE / UNCERTAINTY / PROXIMITY / ESCAPE_DENIAL / PERCEPTION / SCALE / ANTICIPATION / CONSEQUENCE / SPATIAL_ORIENTATION / FALSE_RELIEF`

若没有任何Gain，只是为了拉长时间，判：`SCREEN_EXPERIENCE_PADDING_FAIL`。

## 8｜Stage Integration

### Stage 01B
允许`EXPERIENCE_ELABORATE`操作：只写可见Action / Sound / Silence / Character Response，不写Camera Shot。

### Stage 02A/B
把Genre Felt Intent转成`EXPERIENCE_PRESSURE_PLAN`；重大Threat必须显式规划Pressure Arc、Coverage Role与Protected Beat。

### Stage 02C
Segment Planner优先保留Protected Experience Beat。若一个15s Segment只能装下Threat Build的一部分，可以自然拆成多段；**Segment数量不是内容预算。**

### Stage 04
Storyboard必须覆盖每个Protected Beat绑定的Shot；不能因为“剧情已经知道怪物来了”删掉Omen / Negative Space / Scale / Reaction / Aftermath。

### Stage 05
Final Prompt必须继承当前Beat的Pressure State IN→OUT、Threat Coverage Role和Creature Performance；不能只写“怪物出现/逼近”。

## 9｜Hard Fail

- `SCREEN_EXPERIENCE_CANON_OVERREACH`
- `SCREEN_EXPERIENCE_PADDING_FAIL`
- `QUALITY_FIRST_COST_BACKDRIVE_FAIL`
- `THREAT_PRESSURE_PLAN_GAP`
- `THREAT_REVEAL_TOO_IMMEDIATE`
- `PROTECTED_EXPERIENCE_BEAT_DROPPED`
- `EXPERIENCE_STORYBOARD_COVERAGE_GAP`
- `EXPERIENCE_DURATION_FORCED_COMPRESSION`

> **最终原则：** 整集优先完成观众体验，再做成本优化。允许多生成几段15s，只要每一段承担真实导演功能；不允许为了省Segment把恐惧、压迫、危机和后果压成儿童片式“出现→反应→开打”。

---

## Anti-Shortcut / Experience Completeness Gate

`QUALITY_FIRST` 不允许把“字段齐全”当成“体验完整”。Genre Pressure Scene 在 Director Core Freeze 前必须通过 `EXPERIENCE_COMPLETENESS_PASS`。

硬规则：

1. **Protected Beat 不得因 Cost / Quota / Token / 少生成一段视频而删除、缩短或合并。** 成本不是 Compression Justification。
2. 每个 Protected Beat 必须有自己的 `landing_contract`。镜头只有在该 Beat 的观众体验已经可读后才能 Exit；不能为了快切在 Landing 前结束。
3. `planned_scene_duration_seconds` 必须至少容纳导演自己声明为 `KEEP` 的 `duration_need_seconds` 总量。这里没有统一最低秒数，只有当前 Scene 自己声明的自然需要。
4. 多个 Protected Beat 若映射到同一 Shot / Panel，必须显式 `MERGE`，并提供 `experience_equivalence_evidence` 证明合并后每个体验功能仍然完整；否则 `PROTECTED_BEAT_COLLAPSE_UNJUSTIFIED` / `EXPERIENCE_STORYBOARD_PANEL_COLLAPSE`。
5. `experience_coverage_contract` 明确当前场景哪些体验维度 REQUIRED / NOT_APPLICABLE。LOCK 时 Required Dimension 必须都有合法 Beat Owner，形成 **zero Experience Coverage Debt**。
6. Editorial 必须把 Protected Beat 映射成真正的 `experience_state_in → experience_delta → experience_state_out`；仅保留 Shot ID、仅写“很恐怖/很压迫”不算完成。
7. `NEGATIVE_SPACE_HOLD / REACTION_WITHHOLD / FALSE_CLEAR / FALSE_RELIEF / AFTERMATH` 等 Hold Role 必须真的获得 Editorial Hold/Breathing Function，不能一闪而过。
8. Active Creature 在可见 Threat Beat 中必须有逐 Beat 的 `behavior_beat_map`：感知动作、身体动作、目标跟踪变化、环境响应、压力功能和退出触发。重复复制同一段行为描述属于 `CREATURE_BEHAVIOR_TEMPLATE_REPETITION`。

目标不是机械增加镜头数量，而是保证：**只要一个 Beat 被导演判定为承担威胁、恐惧、危机、反应、Reveal、逃生空间或后果，它就必须真正被观众读到。**
