# Prompt Semantic Deduplication Engine（提示词语义去重与单一归属引擎）｜Current Authority

> **Stage 05 Authority Boundary：** 本引擎只拥有“重复事实合并”权，不拥有“详细度裁剪”权。对于Final Video，`video_prompt_template.md`定义的20项执行覆盖与`PROMPT_LENGTH_CEILING = NONE`合同优先。Reference已经绑定、某事实已有视觉证据、Runtime已有摘要，都不能作为删除当前Shot必要文字控制的理由。若去重后缺失任一适用控制项，必须返回Compiler，不能以Dedup PASS交付。

> **用途：** 解决“同一件事在Continuity说一次、Timeline再说一次、Performance/Action/Restrictions又重复一次”的Prompt膨胀。内部规则可以完整分层，但真正交给图片/分镜/视频模型的执行Prompt必须遵守：**One Fact → One Owner → One Best Occurrence。**


## Current｜Dedup ≠ Conflict Solver

本引擎只在`prompt_constraint_solver.md`已经得到`Hard Conflict Count = 0`之后运行。不同Value的互斥事实不能通过“保留最后一句”或“合并措辞”解决。Camera STATIC vs DOLLY、Breath ON vs Human Audio OFF、@图2/@图3争同一Identity Owner等一律先回Constraint Solver。

## 1｜核心原则：分析可以分层，执行不得复读

Skill内部可以分别运行：
- World State；
- Actor Performance；
- Action Feasibility；
- Natural Motion；
- Action Physics；
- Crowd；
- Reference Binding；
- Render / Audio Locks。

但最终模型Prompt不是这些模板的拼接全文。Compiler必须先把结果归并，再输出一份导演执行单。

**默认规则：同一语义事实只允许一个最合适的模型侧落点。**

## 2｜Fact Ownership Map（事实唯一归属）

### Render Style
只负责：二维绘画语言、线稿、脸部概括、皮肤/头发/材质的表现方法。
不得重复人物身份、镜头动作、综合色、画质参考职责。

### Cinematic Shot Style
只负责：项目级摄影语法倾向（景别关系、前中后景、负空间、OTS/Profile/Wide等组织方式）。
不得复述当前Shot已经由Reconciled Director Contract锁定、并由Approved Storyboard具体执行的Camera / Blocking / Composition。

### Color Authority
只负责当前最直接层级：`Global Color DNA / Scene Color Extension / Shot Lighting Variant`。
同一综合色事实只保留一次；Scene Extension已承担当前综合色时不再在后文重复Global色卡职责，临时Shot Lighting只在它实际变化的时间点进入Timeline。

### Reference Binding（内部Owner，不是模型Prompt Block）
内部只负责记录本次输入的Role / Fields / Most Direct与真实绑定。进入模型侧之前必须把字段消解到Subject / Environment / Style-Color / Entry / Camera-Composition / Timeline等真实执行Owner；Asset ID / 文件名 / 输入槽位留在Executor Input Map。
**最终模型正文不保留Reference Pack / Reference Responsibilities章节。**

### Entry State / Continuity
只负责：**t=0已经成立的状态**。
例如：右手当前撑伞、人物站位、门已打开、衣服已湿。
不得提前描述本段将怎样抬手、怎样停步、最后怎样落位。

### Integrated Shot Timeline
是**所有时间变化的唯一主执行区**：
- Camera；
- Trigger；
- Performance；
- Natural Motion；
- Action / Physics；
- Crowd变化；
- Environment response；
- Combat exchange；
- 当前Shot内的Exit变化。

同一个动态事实写进Timeline后，不再在独立Performance / Action / Crowd / Environment段复述。

### Dialogue / Sound
只负责实际声音内容、说话顺序、必要SFX/Ambience/Diegetic Music。
不重复身体表演，除非声音本身就是动作触发点并且Timeline只做最短指代。

### Global Locks
每类只一次：Style/Negative、Reference Fidelity/Render、Audio Boundary。

### Task-Specific Restrictions
只负责**尚未被正向执行链解决、且有真实污染路径的残余高风险**。
正向动作已经写清“右手持续撑伞”，默认不再追加“不要让伞悬空”。

## 3｜重复类型

Compiler必须检测：

### `EXACT_DUPLICATE`
同一句或近乎同一句重复。

### `SEMANTIC_DUPLICATE`
不同措辞表达同一事实。
例：
- “右手始终握伞”
- “雨伞全程由右手支撑”
若没有额外信息，只保留一条。

### `CROSS_MODULE_DUPLICATE`
同一动作在Continuity / Timeline / Action / Restrictions跨区重复。

### `NEGATION_MIRROR_DUPLICATE`
已经有明确正向解，又写一条反向禁止。
例：
- 正向：“左手摸喉，右手继续撑伞。”
- 负向：“不要让右手离开伞柄。”
默认删除后者。

### `TIMELINE_SHADOW_DUPLICATE`
Timeline已经精确描述时间行为，后面又用摘要重新说一遍。

### `REFERENCE_ADMIN_LEAK`
Reference Role / Authority / Binding解释没有在Compiler中消解，反而作为行政说明进入Model-Facing Prompt。

### `LOCK_ECHO`
Render / Style / Audio边界在首尾重复。

## 4｜Semantic Canonicalization（语义规范化）

在输出前优先读取`VIDEO_EXECUTION_STATE`；自然语言候选仍需把每条信息内部压成：

```text
FACT_ID
SUBJECT
STATE_OR_ACTION
TIME_SCOPE
OWNER_BLOCK
PRIORITY
UNIQUE_DETAIL
```

如果两条候选具有相同`SUBJECT + STATE_OR_ACTION + TIME_SCOPE`，合并它们的`UNIQUE_DETAIL`，只在Owner Block保留一次。

例：
```text
A: 右手持续握住伞柄。
B: 右手维持雨伞支撑，伞不悬空。
```
归并为：
```text
右手始终维持伞柄支撑。
```
“不悬空”不再重复。

## 5｜Cross-Module Merge（跨模块合并）

如果Performance、Natural Motion、Action Physics描述的是同一连续动作，不拆成三个段落。

内部：
```text
Performance: 注意力内收，开始意识到失声
Natural Motion: 步幅缩短时左臂开始抬起
Physics: 停步后伞面轻微余摆
```
模型侧合并为：
```text
雨声让她的注意力收回自身，步幅不自觉缩短；身体仍带一点前行惯性时左臂已自然抬向喉咙，真正停稳后伞面只轻微余摆一次。
```

**保留因果，删除模块边界。**

## 6｜Final Prompt Assembly顺序

Stage 05最终正文必须覆盖以下执行层；“只保留”指去掉模块行政边界，不代表压缩成短Prompt：

1. `Target / Duration`
2. `Visual Style / Current Color Authority + Shot Lighting`
3. `Entry State + 必要人物外观/服装确认 + Scene/Prop State`
4. `Composition / Shot Size / Camera Geometry / Focus / Stabilization`
5. `Integrated Shot Timeline`（逐段动作、表演、视线、肢体占用、物理、环境动态）
6. `Dialogue / Sound / Visible Breath`（适用时）
7. `Ending State / Continuity Landing`
8. `Render Fidelity / Environment Integration`（适用时）
9. `Task-Specific Restrictions`（有则写；无则省略整个区块）

Reference绑定属于模型正文外的Executor Packet；其有效字段已被消解到Style / Subject / Entry / Camera / Timeline，不占独立章节。

**Current Seedance Rule：** Reference承担视觉稳定，但不替代详细文字控制。正常Final Video Master Prompt按`video_prompt_template.md`执行`PROMPT_LENGTH_CEILING = NONE`；Dedup必须优先保留控制走向的细节，只删除真正重复，不得因达到任意字数阈值主动裁剪。

**不再默认输出独立Performance、Action Feasibility、Action Physics、Crowd、Environment、Motion Grammar复述区。** 这些都是内部编译源，最终在Timeline对应时间点出现一次。

图片/Storyboard Prompt同理：先确定唯一职责，再把重复的画风、身份、构图、负面项合并到各自唯一Owner Block。

## 7｜允许重复的极少例外

只有以下情况可再次出现同一核心实体，但必须带来**新的时间/状态信息**：
- Entry写“右手撑伞”是t=0事实；Timeline后面写“左手接伞→右手释放”是新状态变化，不算重复；
- 同一道具在两个不同Shot发生不同状态变化；
- 高风险身份在Reference Pack定义Authority，Timeline只在真正发生身份/变身状态切换时再次提及；
- QC发现某模型对某一高风险规则持续失败，允许在Task-Specific Restrictions补一条最短残余限制，但必须标记`EVIDENCE_BACKED_REPEAT`，不得复制整段说明。

## 8｜Prompt Compression优先级

只有在**目标平台当前已验证的字符上限**要求生成Adapter版本时，才按以下顺序压缩；Source Master Prompt本身没有长度上限，**不得为了追求短或达到历史字数范围而主动触发本节**：
1. 删除Exact / Semantic Duplicate；
2. 合并Cross-Module同因果链；
3. 删除Negative Mirror；
4. 删除Reference Role / Authority等行政解释，并把仍有执行价值的字段归并到真实执行Owner；
5. 删除对模型无执行价值的内部术语；
6. 精简低风险背景信息；
7. 信息仍过密才拆Shot / Segment。

不得为了缩短Prompt先删：
- 当前Shot必要的人物外观/服装确认；
- 起始Scene/Prop状态、构图与Camera Geometry；
- Integrated Timeline中的动作因果、表演、视线、Limb Occupancy；
- 当前Scene光影/综合色执行；
- Dialogue/Sound/可见呼吸时序；
- Ending State；
- P0身份；
- 真实连续性；
- 关键Action Feasibility；
- 关键微表情/潜台词载体；
- 必要Motion Corridor；
- Contact / Force / Exit。

## 9｜Revision Prompt去重

Minimum Necessary Change时：
- 保留未修改模块的**已编译结果**；
- 只替换Open Revision Target；
- 重新跑Semantic Dedup；
- 不因为“重新输出完整Prompt”而把旧解释、旧负面词、旧故障描述叠加进去。

禁止形成：
```text
旧规则 + 补丁说明 + 再次强调
```
应重新编译成：
```text
当前唯一有效版本
```

## 10｜Hard Gate

FINAL Prompt输出前执行：
```text
[ ] Every fact has one primary owner
[ ] No exact or semantic duplicate across blocks
[ ] Entry contains only start-state facts, not timeline actions
[ ] Integrated Timeline is the only owner of time-varying performance/action/crowd/environment behavior
[ ] Positive solution is not mirrored by redundant negative wording
[ ] Reference roles/admin text are absent from model-facing prompt; their execution fields were dissolved into the correct owner blocks
[ ] Each Global Lock appears once
[ ] Revision did not append old wording on top of new wording
```

失败：`PROMPT_REDUNDANCY_FAIL`。

通过Dedup后仍必须运行`model_facing_prompt_surface_sanitizer.md`，因为“没有重复”不等于“没有内部说明泄漏”。

必须回Compiler重新归并；**不得把重复Prompt交给用户或模型。**

## 11｜核心句

**Rule Sources may repeat concepts for safety; Final Model Prompt may not.**

Skill内部可以多层校验同一个事实，模型侧只接收一次最清楚、最可执行的版本。

## Current｜Style Projection Dedup Boundary
可以把重复的Style句合并成一段，但不得把完整Render Language压成“保持项目统一画风”一句。Dedup后至少保留`style_authority_projection_gate.md`要求的Subject-Aware最小投影。
