# Stale Prompt Artifact Recompile Gate（旧Prompt成品强制重编闸门）｜Current Authority

> **用途：** 防止安装新Skill后继续打开/修改旧版本生成的Prompt文件，从而把旧Task Shell、输入编号壳、本地路径、文件元数据或QC自检外壳带回当前流程。

## 1｜Stale判定
任何现有Prompt Artifact只要满足以下任一条件，就标`STALE_PROMPT_ARTIFACT`：
- 文件正文标记的Skill / Prompt Compiler版本低于当前Skill；
- Prompt正文包含当前版本已禁止的任务壳、路径、内部资产名、Stage/Gate/Authority、自检块；
- Runtime/Capsule版本与当前Skill不一致；
- 旧Prompt是在Surface Sanitizer / Egress Gate引入之前生成；
- 旧Prompt经过多轮“在原文上补一段”式Patch，无法证明Copy Surface是当前规则重新编译的。

## 2｜Stale Prompt不得作为文本母版
`STALE_PROMPT_ARTIFACT`可以帮助恢复“任务意图”，但不得作为当前Prompt的文字底稿。禁止：
- 在旧Prompt原文上删几行再继续；
- 保留旧标题/输入清单，只替换风格段；
- 复制旧Prompt再追加Current Skill Version规则；
- 因为旧Prompt曾经能生成就Grandfather其模型侧格式。

正确做法：
`Recover Task Intent → Re-read Current Authorities → Resolve Current References → Compile Fresh INTERNAL_DRAFT → Surface Sanitizer → Prompt Egress → Fresh FINAL_COPY_SURFACE`

## 3｜版本标记原则
Generation Prompt正文不需要写Skill版本；版本只登记在Workspace / 文件元数据。若旧Prompt正文仍携带任何Skill版本标签，它本身就是强烈Stale信号，必须重新编译而不是继续Patch。

## 4｜Hard Fail
- `STALE_PROMPT_REUSE_FAIL`
- `OLD_PROMPT_PATCH_CHAIN_FAIL`
- `PROMPT_VERSION_MISMATCH`
- `LEGACY_PROMPT_SHELL_SURVIVED`

任一未解决：禁止Generation Prompt出站。

## Current｜Constraint-Proven Fresh Compile
任何Current Skill Version之前的Video Prompt，即使没有路径/资产名泄漏，也没有`VIDEO_EXECUTION_STATE + PROMPT CONFLICT PREFLIGHT + SHOT_PROOF_STATUS + VIDEO_GENERATION_READY`证明，因此不能直接继续Patch。只恢复Task/Director/World State意图，Fresh Recompile后再出站。


## Current｜Legacy Color-Applied Job Invalidation
升级后扫描当前未执行任务队列/Workspace。若存在旧版本生成的`SCENE_COLOR_APPLIED_REFERENCE*`、`COLOR_GRADE_ANCHOR*`或“综合色应用参考图”任务：
- 没有当前`APPLIED_REFERENCE_TRIGGER=VALID` → 标记`STALE_OPTIONAL_FALLBACK_JOB`，从Mandatory/Next Task队列撤下；
- 当前已有Approved Color Card → 直接保留该Card作为综合色视觉Authority；
- 已经生成且Approved的Applied Reference不删除，可作为可选既有资产保留，但不得因为它存在就强制Video使用；
- 不得把旧任务文件名/旧Prompt正文当成当前用户意图继续Patch。
## Current｜Version-Delta Invalidation

当Workspace的`Migration Applied Skill Version != Current Skill Version`时，尚未执行的Generation Prompt、Copy Surface、Reference Routing Snapshot、Reference Binding Map与Runtime Capsule均先标STALE；只恢复有效Task/Director/World State事实并Fresh Recompile。`Migration Status=COMPLETE`不能绕过本条。已APPROVED Video/资产/真实Ending Frame不因此失效。
