# Video Generation Duration Authority（视频生成时长权限）｜Current Authority

> **用途：** 统一Stage 02 / 04 / 05对“导演上自然需要多久”与“当前实际平台允许怎么生成”的判断。当前规则（Current）：Skill取消固定单次视频时长上限：`SKILL_DURATION_CEILING = NONE`。不再内置10秒Hard Ceiling，不再内置5s/10s合法Slot，也不再把3s或任何其他时长默认判为非法。

## 1｜导演时长与平台能力必须分开

- **Episode Runtime Target（整集成片）**：仍由当前项目/用户目标决定；它不是单次生成上限。
- **Natural Required Duration**：导演判断当前Sequence / Segment自然完成需要多久。
- **Director Target Duration**：Stage 02锁定的实际叙事/表演目标；唯一通用要求是`duration > 0`，Skill不设置固定最大值。
- **Platform Duration Profile**：只有用户、当前平台UI、当前任务或已验证平台配置明确提供时才建立。可为：
  - `UNDECLARED`：当前没有可靠平台时长信息；
  - `FLEXIBLE`：支持自定义/连续时长；
  - `FIXED_SLOTS`：平台提供若干固定档位；
  - `HARD_MAX`：平台明确存在单次最大时长；
  - `FIXED_SLOTS + HARD_MAX`：两者同时存在。
- **Model Generation Slot / Requested Generation Duration**：只有当前平台确实要求选择档位或指定时长时才填写；不得从旧免费额度、历史平台或记忆中硬编码。

**Current Duration Rule：** Skill不设置固定秒数上限或默认生成Slot；实际平台时长能力只在Director Plan锁定后进入Execution Mapping。

## 2｜导演自主定时

固定评估顺序：

**Selected Sequence Arc → Narrative Beat Completion → Dialogue / VO Natural Timing → Actor Performance Readability → Action Physics → Camera Travel → Meaningful Hold → Director Target Duration**

导演应选择：

> **完成当前叙事/表演/动作所需的最短自然充分时长（Shortest Natural Sufficient Duration）。**

不是越短越好，也不是越长越高级。Beat完整、表演可读、动作物理成立、Exit稳定后即可结束。

## 3｜平台能力只在Director Judge之后进入Execution Translation

Director Judge之前，任何“平台最多多少秒 / 有哪些Slot / 哪个时长更容易生成”都不得参与Director Option优劣判断。

只有`DIRECTOR CORE LOCKED`后，Stage 02C才读取当前可靠的`Platform Duration Profile`：

### A. `UNDECLARED`
- 不猜平台档位；
- 不因时长自动拆分；
- 保留Director Target并继续生成平台无关Prompt；
- 若真正执行时平台要求档位，再补做Execution Mapping。

### B. `FLEXIBLE`
- 直接按Director Target申请/设置对应时长；
- 不为凑整秒或档位改导演节奏。

### C. `FIXED_SLOTS`
- 从**当前已验证Slot集合**中选择能完整容纳Director Target且破坏最小的档位；
- 不允许把Slot反写成剧情必须填满的时长；
- 多余尾部只允许稳定、可Trim，不新增剧情动作。

### D. `HARD_MAX`
若Director Target超过**当前平台明确Hard Max**，标记：

`PLATFORM_DURATION_SPLIT_REQUIRED`

然后在不改变Director Invariants的前提下寻找自然边界拆分。这里只是平台执行适配，不是Skill自身时长限制。

## 4｜禁止两种错误

### NO DURATION PADDING｜禁止为了平台时长拖戏
不得因为平台提供更长Slot或默认时长，就加入无信息停顿、重复动作、无因慢动作、Dead Hold或额外CUT来填满。

### NO FORCED TIME COMPRESSION｜禁止为了平台时长压坏表演
不得为了适配平台上限而异常加快对白、删除必要Listener Response、压缩动作物理、加速Camera Travel或删掉关键Hold。

若平台Hard Max确实无法容纳当前Director Target，优先自然拆分；若无损拆分仍会破坏Director Invariants，返回Director Judge处理`AI_EXECUTION_CONSTRAINT_CONFLICT`。

## 5｜平台约束下的自然拆分

只有当前可靠平台Profile确实要求时，才执行`PLATFORM_DURATION_SPLIT_REQUIRED`。优先切分点：
1. Beat Shift / Tactic Shift；
2. 自然CUT / Match Cut；
3. Dialogue Thought Boundary / Listener Meaning Change；
4. 动作完成形成New Stable State；
5. Combat Initiative Shift / Exchange结束；
6. Camera Landing / Reveal完成；
7. 进入/离开空间等天然Transition。

拆分后必须保持World State、人物Objective、服装、伤势、道具、环境破坏、Persistent VFX和Director Invariants连续。

## 6｜Stage 02字段

```text
Director Target Duration：__s
Duration Rationale：<为什么自然需要这些时间>
Platform Duration Profile：UNDECLARED / FLEXIBLE / FIXED_SLOTS / HARD_MAX / FIXED_SLOTS+HARD_MAX
Verified Platform Duration Capability：<仅有可靠信息时填写>
Execution Duration Mapping：<DIRECT / SLOT __ / SPLIT / PENDING PLATFORM MAPPING>
Platform Duration Compatibility：PASS / PENDING / PLATFORM_DURATION_SPLIT_REQUIRED / AI_EXECUTION_CONSTRAINT_CONFLICT
```

**禁止写死任何平台档位，除非当前任务已经可靠确认。**

## 7｜Stage 04

Previs服务Stage 02锁定的Director Target Duration：
- Panel / Keyframe数量由信息增量决定，不按秒数机械平均；
- 不存在Skill级固定秒数上限；
- 如果Storyboard证明原Director Target不足以容纳自然表演/Camera/动作，执行`DURATION_REPLAN`回Stage 02更新Target；
- 如果只是当前平台Hard Max不够，由02C/05做Platform Mapping，不通过删表演解决。

## 8｜Stage 05 Duration Compatibility Gate

FINAL VIDEO PROMPT前检查：

1. `Director Target Duration > 0`；
2. Director Target与Approved Sequence / Previs一致；
3. 若`Platform Duration Profile = UNDECLARED`，不得虚构Slot或Hard Max；
4. 若平台能力已明确，Execution Duration Mapping与真实平台能力兼容；
5. 不存在Duration Padding / Forced Compression；
6. 若当前平台Hard Max要求拆分，拆分不破坏Director Invariants。

失败状态：
- `INVALID_DIRECTOR_DURATION`：Target <= 0或与Approved结构自相矛盾；
- `PLATFORM_DURATION_PROFILE_FABRICATION`：凭空编造平台时长能力；
- `PLATFORM_DURATION_CONFLICT`：已知平台能力与当前执行映射冲突；
- `PLATFORM_DURATION_SPLIT_REQUIRED`：已知平台Hard Max需要拆分；
- `AI_EXECUTION_CONSTRAINT_CONFLICT`：任何拆法都会伤害Director Invariants，需要回Director Judge。

**不存在“因为>10秒就禁止输出Prompt”的Skill级规则。**


## 8.5｜15s User Quota Confirmation Gate（额度确认，不是时长上限）

`LONG_VIDEO_QUOTA_CONFIRMATION_THRESHOLD = 15s`。该阈值**不是**Skill时长上限，也不是自动拆Segment条件。

- `Director Target Duration <= 15s`：无需额度提问，自动通过该Gate；
- `Director Target Duration > 15s`：在`VIDEO EXECUTION PLAN`冻结并进入真实Video Generation Job之前，必须向用户提问：
  > **“这个视频单次计划时长为 X 秒，超过15秒。你当前有足够的视频生成额度吗？”**
- 用户明确回答有额度：记录`question_asked=true / user_response=HAS_QUOTA / confirmed_by=USER / confirmation_ref`，允许继续；
- 用户尚未回答：停在`WAITING_USER_QUOTA_CONFIRMATION`，不得启动真实Video Generation Job；
- 用户明确没有额度：不得擅自生成，也不得仅因为>15s自动拆分；应向用户说明并询问是否要按自然Beat拆分、缩短或改用其他执行方案。

**禁止把15秒误写为Hard Max。** 20s、30s或更长的Director Target仍然合法，只多一个用户额度确认步骤。

## 9｜对白 / 表演 / 战斗 / Camera

- Dialogue / Performance：按自然思想单元、语流和反应完成，不按固定秒数截断。
- Combat：按Micro-objective / Exchange可读性组织；是否拆分由戏剧结构与当前平台能力共同决定，不按固定10秒切。
- Camera：Camera Path按真实可读速度完成；不要为适配固定秒数使用不可能的Camera Speed。
- 长镜头：只要导演成立、当前执行平台允许，就可以超过历史10秒范围；Skill不主动截断。

## 10｜QC通过标准

Duration PASS要求：
- Director Target来自叙事/表演/动作/Camera需要；
- Skill未施加固定最大秒数；
- 平台时长能力只使用当前可靠信息；
- 无Padding / Forced Compression；
- 平台若有限制，Execution Mapping正确且不静默伤害Director Invariants。

> **当前Duration原则：导演决定自然时长；平台只决定如何执行。Skill本身不规定固定视频秒数上限。**

## Current｜Narrative Duration / Generation Duration / Trim Handle Separation
Duration内部必须分开：
- `NARRATIVE_DURATION`：真实叙事与表演需要的时长；
- `GENERATION_DURATION`：当前平台实际生成时长/Slot（若平台有要求）；
- `TRIM_HANDLE_DURATION`：Generation比Narrative多出的纯剪辑余量。

Trim Handle**不是新的Narrative Beat**，不得为了填尾巴新增动作、声音事件或复杂Camera规则。若平台固定15s而叙事13s，Timeline的叙事事件在13s结束；剩余2s只继承End State并允许与既有世界一致的自然微动。禁止为了Trim Handle制造“第六Beat”。
