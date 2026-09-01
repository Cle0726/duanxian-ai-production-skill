# Segment Planner（视频段落规划器）

> **Story Scope Gate：** Segment只能拆自当前`EPISODE SCREENPLAY LOCK`中的Scene/Beat与Stage 02 Detailed Shot Contract；不得直接从小说段落按平台时长切Segment。
> **用途：** 在Stage 02内自动判断哪些Shot应该合成一次AI视频生成，哪些Shot应该拆开。**本Planner位于Stage 02C Production Translation，必须在`DIRECTOR CORE LOCKED`后读取`director_to_ai_execution_boundary.md`与`video_generation_duration_authority.md`；Skill不设置固定单次视频时长上限，实际Director Target由已选Sequence的自然执行判断。只有当前平台能力被可靠提供时才做Duration Mapping。** **调用本Planner前，必须先完成`world_state_continuity_engine.md`的State Diff / Transition Audit，并由`director_architecture_engine.md`锁定Scene Spatial Staging、Axis/Screen Direction、Shot Progression与Detailed Shot Contract。** Segment Plan完成后先读取`previsualization_strategy_router.md`，为每个Segment锁定Shot Storyboard Coverage Contract + Supplemental Previs；之后才形成Raw Asset Demand，经过`asset_consolidation_sufficiency_audit.md`合并/复用/充分性复核得到Final Episode Asset Requirement Manifest，再进入Stage 03；不是直接跳到Stage 04。用户不需要自己决定Segment边界或预演形式。

## 核心定义

- **Shot（镜头）**：两次明确切镜之间连续的一段摄影。
- **Segment（视频段落）**：一次送给AI视频模型生成的完整任务。

一个Segment可以包含一个Shot，也可以包含多个由 `CUT / Match Cut` 分开的Shot。

## 默认原则

优先让一个Segment覆盖一个**完整且可稳定生成的导演单元**：同一空间逻辑、同一视觉主次、可连续执行的Blocking/Camera/动作链。不是机械“一Shot一Segment”或“一个Scene一个Segment”。

## 适合合并到同一Segment的条件

多数条件成立时可以合并：

- 同一Scene、时间连续；
- 人物数量基本稳定；
- 场景空间不发生大跳变；
- 服装/道具状态连续；
- CUT / Match Cut数量有限且明确；
- `Director Target Duration > 0`且由已选Sequence自然需要决定，不为平台时长Padding或Forced Compression；
- 动作和表演可以在同一次生成中连续理解；
- 不需要完全不同的参考图包。

## 应优先拆成多个Segment的情况

出现以下任一高风险条件时优先拆：

- 空间/地点明显改变；
- 时间跳变；
- 角色阵容明显改变；
- 前后需要完全不同的正式参考资产；
- 大规模复杂动作 + 多次切镜 + 多人物同时发生；
- 一个Segment内的动作物理链过长，模型难稳定；
- 同一Segment包含多次换手/拿放/扶持/承重切换/多人接触，Action Feasibility State Table过长或Support关系频繁重构；
- 需要在中间得到稳定尾帧作为下一段连续性锚点；
- 预计一次生成会造成身份、空间、道具或CUT关系漂移。
- Segment内部需要同时维持多个互相冲突的Camera Intent / Axis体系；
- 前后Shot的Focus Owner / Depth Plan / Reference Pack发生大幅变化，合并会让视觉主次不稳定；
- Combat从远距离建立直接跨到Contact/Impact且中间需要独立可读的Initiative Shift；
- Transformation Reveal需要独立Hero Landing或Music Eye / Large Silhouette读点。

## Segment Complexity（段落复杂度）快速判断

可把风险粗分为：

- `LOW`：单Shot、单一动作/表演、人物少、空间稳定；
- `MEDIUM`：2–3 Shot、1–2个明确CUT、人物/道具关系稳定；
- `HIGH`：多人物复杂动作、多次CUT、空间变化或大量状态变化。

`HIGH` 不等于一定拆，但必须说明为什么仍适合一次生成；否则默认拆分。

## Entry Mode（入场模式）

每个Segment在输出Plan前必须先读取 `segment_entry_modes.md` 并登记：`CONTINUITY_ENTRY / CUT_ENTRY / SCENE_OPENING`。不要再用“上一段尾帧：需要/不需要”作为唯一逻辑。

Entry Mode只决定**视觉接入方式**，不决定世界是否继承。每个Segment同时登记相关`World State Delta / Transition Audit Ref`：
- CONTINUITY_ENTRY：World State + Ending Frame + Continuity Snapshot共同继承；
- CUT_ENTRY：不必复制上一帧构图，但Prop / Injury / Knowledge / Environment Runtime State等仍继承；Injury读取最新Post-Recovery State，不能越过合法Transformation Recovery回滚；
- SCENE_OPENING：不默认用上一Scene尾帧，但绝不清空World State。

## 输出格式

Stage 02完成`DIRECTOR CORE LOCKED`的Detailed Shot Contract后，进入Production Translation Pass并自动追加：

```text
【Segment Plan｜视频段落规划】

SEG-SXX-B01
包含Shot：SH01 / SH02 / SH03
镜头关系：SH01 → CUT → SH02 → Match Cut → SH03
Director Target Duration：约14秒
Duration Rationale：自然完成连续动作链、两个切点与表演落点约需14秒；Skill不因超过历史10秒范围自动拆分
Platform Duration Compatibility：PASS / PENDING
复杂度：MEDIUM
Director Contract Ref：SC__ / SH01-SH03
Shot Progression：WIDE → MEDIUM → TIGHT / 其他
Axis / Screen Direction：<Primary Axis + movement direction>
Critical Visual Read：<本Segment必须真正读到的字段>
Cinematography Summary：<仅写有因的Entry/Landing Camera Geometry、Lens Family、Focus、Stabilization>
Spatial Execution Summary：<按`spatial_execution_translation.md`记录本Segment真正需要的Start Region/Depth/Relation → Motion Target/Path → End Landing；无动态空间风险写N/A>
Camera Intent Summary：<STATIC PRESSURE / SUBJECT FOLLOW / ...>
Cut Motivation / Shot Relation：<每个CUT为什么切、如何连接；无CUT写CONTINUOUS_HOLD>
Dramatic Sensory Cue（适用时）：
Motion Priority：SUBJECT / OPPONENT / CAMERA / ENVIRONMENT / VFX
Action Feasibility Risk：LOW / MEDIUM / HIGH（高风险在Stage 04强制State Table）
合并理由：同一空间、同一人物组合、连续动作链、导演视觉主次兼容、CUT动机明确
Entry Mode：CONTINUITY_ENTRY
World State Transition Ref：<Audit ID / DIRECT_CONTINUITY>
Previous Ending Frame：MUST
结束稳定状态：Character B失去支撑，Character A进入接应动作前的稳定落点
```

若拆分：

```text
SEG-SXX-B02-A｜SH04–SH05｜Director Target约7秒｜PASS
SEG-SXX-B02-B｜SH06–SH07｜Director Target约7秒｜PASS
拆分原因：角色阵容变化 + 动作链过长 + 第二段需要新的参考图包
```

## 与Stage 03 / 04的关系

Segment Plan完成后，先读取`previsualization_strategy_router.md`给每个Segment建立Shot Storyboard Coverage Contract + Supplemental Previs，再形成Raw Asset Demand，并读取`asset_consolidation_sufficiency_audit.md`跨Shot合并/复用/充分性复核；只有Mandatory Shot Storyboard Planning Gate与Final Episode Asset Requirement Manifest均完成并达到`DIRECTOR BREAKDOWN READY`后，才由Stage 03完成整集Episode Asset Pack并通过Freeze Gate。

只有`EPISODE ASSET FROZEN`后，Stage 04 Previsualization / Storyboard才按**Segment**组织，并执行Stage 02已选Previs Mode；不是先做一张超大的Scene宫格再临时切开，也不是每个Segment默认宫格。

Stage 04必须继承Stage 02 Detailed Shot Contract + Shot Storyboard Coverage Contract；先完成Mandatory Board，再执行Supplemental Previs；如果预演需要改变核心Blocking / Distance / Entry/Landing Camera Geometry / Lens Family / Focus Plan / Stabilization / Axis / Camera Intent / Shot Relation，先回Stage 02做最小Director Patch，不允许为了“预演更好看”静默重设计。

每一份正式Previs Deliverable（单帧 / Pair / Board / Map / Camera Path / Hybrid Component）必须明确：

- 服务哪个Segment；
- 包含哪些Shot；
- 哪些Panel属于连续Shot；
- 哪些Panel之间执行CUT / Match Cut；
- Segment的Entry / Exit。

## 与Stage 05的关系

Stage 05默认按已批准Segment Plan写时间轴，并严格继承Entry Mode与Spatial Execution Summary。只有CONTINUITY_ENTRY默认把Previous Ending Frame加入Reference Pack；CUT_ENTRY / SCENE_OPENING不强行加入。若Duration Compatibility Gate、Storyboard QC或视频稳定性证明原计划不合理，允许最小重新拆Segment并回写Episode Workspace；**只要拆分改变了原Approved Storyboard覆盖范围/Shot时间结构，受影响Storyboard必须标STALE并回Stage 04重编，不能只改Stage 05时间轴绕过Storyboard Authority。**
## 当前生成任务约束

当前规则（Current）：`SKILL_DURATION_CEILING = NONE`。先锁真实Director Target Duration；只有当前平台UI / 用户 / 当前任务可靠提供Duration Profile时，才映射固定Slot、Requested Duration或Hard Max。任何历史免费额度Profile都不得自动继承；其他平台能力同样只有明确提供时才采用，不凭空编造。

只有当前可靠平台Profile明确存在Hard Max且Director Target无法容纳时，才执行`PLATFORM_DURATION_SPLIT_REQUIRED`，优先在Beat Shift / Tactic Shift / CUT / Dialogue Thought Boundary / New Stable State / Combat Initiative Shift / Camera Landing处分开；若无损拆分会改变Director Invariants，回Director Judge。



## Cost-Aware Segment Fields
每个Segment记录：
- `Shot Investment Tier`：T1 / T2 / T3 / T4；
- `Max Planned Take Budget`：默认1；仅T3/T4允许在诊断后提高；
- `Cinematography Proof Needed`：YES / NO；
- `Camera Motion Contract Needed`：YES / NO；
- `Shot Storyboard Coverage Plan Status`：PENDING ROUTER / PLANNED / GAP / PASS；
- `Shot Storyboard Coverage Ref`：<SEG Coverage Contract / PENDING>；
- `Mandatory Storyboard Baseline`：CLEAN_STRUCTURAL_STORYBOARD_PANEL_SET / PENDING；`CLEAN_STORYBOARD_BOARD`只记录为确定性Review/Sequence派生物，不作为替代Baseline；
- `Supplemental Previs`：NONE / <Mode>；
- `Director Spatial Complexity`：LOW / MEDIUM / HIGH；
- `Critical Visual Read Risk`：LOW / MEDIUM / HIGH。
- `Location Investment Tier`：若本Segment首次触发场景Coverage需求则记录L1/L2/L3。

这些字段控制生产投资，不进入最终视频模型Prompt正文。


## Current｜>15s额度确认
`SKILL_DURATION_CEILING = NONE`保持不变。Director Target >15s不得因为额度规则自动拆Segment；它只在Stage 05触发`LONG_VIDEO_QUOTA_CONFIRMATION_THRESHOLD = 15s`用户确认。用户确认有额度后按原导演时长执行；用户无额度时再由用户决定是否采用自然Beat拆分/缩短。
