# Prompt Egress Gate（最终Prompt出站闸门）｜Current Authority

> **最高原则：** 内部推导再复杂，真正给图片/视频模型的Generation Prompt只能从本Gate出站。任何模板、Capsule、Runtime或Controller都不得直接把“草稿Prompt”交给用户。

## 1｜唯一合法出站链

`VIDEO_EXECUTION_STATE + SPATIAL_EXECUTION_STATE → CONFLICT/PREVIS/READINESS PASS → INTERNAL_DRAFT → STYLE/COLOR/REFERENCE RESOLVE → GENERATION/QC SEPARATION → SURFACE SANITIZER → EGRESS REWRITE → POST-COMPILE CONSTRAINT CLOSURE → MECHANICAL LINT → FINAL_COPY_SURFACE`

- `INTERNAL_DRAFT`永远不是用户可复制Prompt；
- `FINAL_COPY_SURFACE`是唯一允许交付的Generation Prompt；
- 任何QC说明、输入清单、任务壳、文件元数据、内部资产名或流水线方法名都只能存在于内部，不得越过本Gate。

## 2｜FINAL_COPY_SURFACE输出语法

### Image / Asset
只允许：
1. **当前任务强绑定资产的真实@Mention短句**（《断弦之歌》Current Generation Profile下为必填；每个MUST_BIND/DIRECT_BIND资产至少一次）；
2. 1段直接写“生成什么、画面里有什么、状态/构图/空间是什么”的视觉执行语言；
3. 1段直接写项目画风与当前综合色的执行语言；
4. 1句真正必要的画面排除项。

不得出现生产管理栏目标题、输入编号壳、QC验收壳、本地文件元数据、内部资产ID/版本或流水线方法词。

### Video
Stage 05允许在代码块外先显示`镜头执行分析`；真正FINAL_COPY_SURFACE仍只有一个代码块。

Seedance Video Copy Surface必须是详细执行稿，`PROMPT_LENGTH_CEILING = NONE`，不设固定字数区间或最大字符数，并允许使用直接帮助模型理解的执行标题与时间轴标记，例如：
- `镜头目标与时长`
- `起始状态与必要视觉确认`
- `场景空间/构图/摄影机`
- `0–3s / 3–6s ...`
- `光影综合色`
- `对白与声音`
- `结尾状态`
- `必要限制`

这些属于模型执行内容，不属于生产管理标题。不得出现Reference职责表、文件元数据、QC/Stage/Gate说明。

## 3｜Reference表达

- Current Project Default：UI已绑定**不等于**可以省略资产Mention；凡当前Reference Runtime要求强绑定的Approved Asset，必须写真实`@资产名 + 最短可执行保持句`。
- Target Adapter只有明确声明`ui_binding_without_prompt_mention_allowed=true`时，才允许UI-only。
- 平台只支持顺序Token时，使用本次真实Binding Map解析出的`@图N`；不得沿用历史图号。
- Token/Mention未建立：**WITHHOLD Generation Prompt**。先补Native Binding；不得为了给出Prompt而静默删除Reference。

## 4｜Style Projection出站规则

`Style Projection`是内部方法名，**这个词本身不得进入FINAL_COPY_SURFACE**。只允许它求解出来的可见风格语言，例如：

`带动漫影响的二维叙事插画；细而稳定的手绘结构线，受控色块结合柔和绘画阴影；人物与环境保持同一绘画体系，材质以二维概括而非照片纹理表现；综合色丰富但克制，色族集中、选择性显色、对比受控并保持清楚明度层级。`

## 5｜Self-check出站规则

QC与验收条件永远留内部；任何QC流程措辞不得进入Generation Prompt。真正需要防止的高风险项直接改写成一条模型可执行限制。

## 6｜Meta-instruction清理

禁止把“如果平台支持negative prompt，请添加……”交给模型。若排除项确实必要，直接写成当前Prompt的一部分；若不必要则删除。

## 7｜Hard Stop

出现以下任一项即不允许交付：
- `TASK_SHELL_LEAK`
- `LOCAL_PATH_LEAK`
- `FILE_NAME_LEAK`
- `INTERNAL_ASSET_ID_LEAK`
- `PIPELINE_JARGON_LEAK`
- `SELF_CHECK_LEAK`
- `META_PROMPT_INSTRUCTION_LEAK`
- `STYLE_METHOD_NAME_LEAK`
- `EGRESS_LINT_FAIL`

## 8｜Copy Surface形态示例（抽象）

合法Copy Surface只展示**任务本身的执行内容**，不携带任何项目管理外壳。结构应保持为：

```text
<真实@资产Mention。>

<镜头目标、起始人物/环境/道具状态、构图与摄影机。>

<按实际时长写完整分段Timeline：动作、表演、视线、肢体占用、物理、环境动态、Camera与声音。>

<当前镜头光影综合色、对白/声音、Ending State。>

<只保留当前真实必要的排除项。>
```

示例只说明表面结构，不提供任何可被其他场景误继承的具体人物、地点、道具或综合色内容。

## 9｜Stale Prompt Artifact
若存在旧版本Prompt文件/草稿，出站前必须先读取`stale_prompt_artifact_gate.md`。旧Prompt只能恢复任务意图，不能作为文字母版继续Patch；必须Fresh Recompile。

## Current｜Binding Packet Visibility Canonical Rule

`REFERENCE_UPLOAD_BINDING_LIST / MUST_BIND_* / NATIVE_BINDING_REQUIRED / Executor Binding Packet`全部属于**内部执行证据**，不是Generation Copy Surface内容。
- 已有强绑定Approved Asset：最终Prompt必须出现其真实`@资产`Mention + 最短执行句；
- 尚无真实Native Mention但用户必须手动操作：代码块外最多一句最短绑定提示，不显示内部Asset ID、Role、Path或版本；
- 未完成必要绑定：阻断Executable Prompt，不能用“把Binding List打印出来”或直接省略@资产代替绑定；
- 任何模块出现“生成交付同时给Binding List / 输出REFERENCE_UPLOAD_BINDING_LIST”的旧指令，均由本规则覆盖并视为`BINDING_PACKET_VISIBILITY_CONFLICT`。

## Current｜Style Projection Mechanical Lint
当当前任务触发`style_authority_projection_gate.md`且运行环境支持脚本时，除了`prompt_surface_lint.py`外，还必须按`STYLE PROJECTION CARD`模式运行`validators/style_projection_lint.py`：若`Visual Style Evidence Binding = BOUND`且Reference Content/Role验证通过，使用`--visual-style-evidence-bound`进入`MINIMAL_VISUAL_BOUND`，只要求一条明确的Style Continuity句，不得反向强迫Prompt重写完整Render Core；只有`NOT_AVAILABLE / PLATFORM_UNSUPPORTED`时使用FULL Text模式，环境/道具/Video至少覆盖Render Family、Linework/Shading、Palette/Value、Atmosphere，清楚人物为核心时再加Human Rendering。`STYLE_TAG_ONLY_FAIL / STYLE_RENDER_LANGUAGE_COLLAPSE`只在文字是唯一Style Control且仍缺执行绘制语法时成立。

## Current｜Video Constraint Egress Requirement
Video任务只有在`PROMPT CONFLICT PREFLIGHT: Hard Conflict Count = 0`、`SHOT_PROOF_STATUS=PASS`、`MOTION_LOAD_STATUS!=OVERLOAD`、`GENERATION_QC_SEPARATION=PASS`和`VIDEO_GENERATION_READY`成立后，才允许进入本Gate。Egress Rewrite完成后还必须运行`post_compile_constraint_closure.md`；只有`POST_COMPILE_CONSTRAINT_CLOSURE=PASS`才形成Final Copy Surface。Egress不负责现场解决冲突；发现冲突必须丢弃Candidate、退回Resolved Typed State Fresh Compile，而不是删一句/补一句凑PASS。

QC验收清单、PASS条件和内部检查语句均属于QC Contract，不允许出站。
