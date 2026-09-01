# Existing Project Migration｜Current Authority

> **用途：** 用当前Skill接管旧Episode时，只迁移仍然有效的项目事实、Approved资产、连续性与当前Next Action。历史版本的执行法规、旧Prompt正文、旧Reference禁令和旧固定时长规则不进入当前运行Authority。

## 0｜Skill Version Delta Audit（版本差量审计）

Workspace必须同时记录：
- `Current Skill Version`：从当前`SKILL.md`入口读取
- `Migration Applied Skill Version`
- `Migration Status`

**不能只看`Migration Status=COMPLETE`。** 只要`Migration Applied Skill Version != Current Skill Version`，即使旧迁移已经COMPLETE，也必须先执行一次轻量`MIGRATION_DELTA_AUDIT`。

差量审计只处理**当前版本可能改变执行结果的运行状态**，不得推翻无关的Approved成果：
1. 保留已APPROVED人物/环境/道具/Previs/Video/真实Ending Frame与有效Continuity；
2. 将尚未执行的旧Generation Prompt / Copy Surface / Runtime Capsule / Digest标STALE并按当前Authority重编；
3. 重算当前Reference Routing / Reference Binding Map / Visual Control Coverage；
4. 清理旧Optional Fallback Job，尤其没有当前`APPLIED_REFERENCE_TRIGGER=VALID`的综合色应用图任务；
5. 若当前Next Action会进入一个**尚未开始Stage 02的新Story Scope**，检查是否存在`EPISODE SCREENPLAY LOCKED`；只有旧Story Lock/小说摘要时标`LEGACY_STORY_LOCK_ONLY_GAP`并补01A→01B→01C；已经完成Stage 02+的既有Scope不因此回滚；
6. 对当前Next Action涉及的Cinematography / Camera / Focus / Audio / Action / Prompt Constraint状态重新跑当前Preflight；
7. 不重做与当前版本差量无关的Stage或Approved资产；
8. 完成后写回`Migration Applied Skill Version = Current Skill Version`、`Migration Delta Audit = PASS`、`Migration Status = COMPLETE`。

`MIGRATION_DELTA_AUDIT`是版本升级的运行缓存失效机制，不是整集重迁移。

## 1｜最高迁移原则

`KEEP VALID RESULTS → INVALIDATE OLD EXECUTION RULES → REBUILD ONLY WHAT CURRENT NEXT ACTION NEEDS`

- 已有明确`APPROVED`人物、环境、道具、综合色、Storyboard/Previs、Video可继承，除非当前Canon/World State/QC已有明确冲突证据。
- 只有`QC PASS`但没有用户批准的资产，不自动升级为APPROVED。
- 不为了版本升级从Stage 01重做整个Episode；从当前真实Next Action继续。
- 旧Prompt文本永远不是新版本的执行Authority，只恢复其中仍有效的Task Intent、Director Decision、World State和已批准视觉事实。

## 2｜旧Prompt与任务队列

旧版生成Prompt、旧Copy Surface、旧本地路径任务壳、旧`@图N`顺序全部标`STALE_EXECUTION_ARTIFACT`，不得继续Patch。

继续生成前必须：
1. 恢复当前Task/Segment目标；
2. 重新建立当前Reference Binding / Visual Routing；
3. Final Video重新建立`VIDEO_EXECUTION_STATE`并运行Constraint / Shot Proof / Readiness；
4. 重新编译当前`FINAL_COPY_SURFACE`。

旧任务队列若仍有`SCENE_COLOR_APPLIED_REFERENCE* / COLOR_GRADE_ANCHOR* / 综合色应用参考图`：没有当前`APPLIED_REFERENCE_TRIGGER=VALID`时标`STALE_OPTIONAL_FALLBACK_JOB`并撤出Mandatory/Next Task。已有Approved色卡按当前`visual_reference_routing.md`直接路由。

## 2.5｜Stage 01 Screenplay Adaptation差量迁移
当前版本新增`01A Source Parse → 01B Screenplay Adaptation → 01C Screenplay Lock`。

迁移原则：
- 已APPROVED Video、已执行完成的Stage 02 Director Contract、已Approved Mandatory Storyboard不会因为新增Screenplay层追溯作废；
- 当前Episode已经有`DIRECTOR CORE LOCKED / DIRECTOR BREAKDOWN READY`或在Stage 03/04/05/06推进，且Story事实未发生变化 → **不从Stage 01重来**；
- 以后如果同Episode出现尚未进入Stage 02的新Scene/Story Scope，或Story级Revision要求重新改编该Scope，而Workspace只有旧`Story Lock / 小说摘要` → 标`LEGACY_STORY_LOCK_ONLY_GAP`，只为该未导演Scope补Stage 01A/B/C；
- 若已有用户批准的正式剧本文件，可登记`USER_PROVIDED_FINAL_SCREENPLAY`，完成Pass-through Parse/QC后建立Screenplay Lock，不重写；
- 旧Stage 02已经锁定但尚未生成Video的Shot，不因为本次新增改编层自动返工；只有明确发现其Director Contract与当前Canon/用户批准剧本冲突时才走Change Impact。

禁止把迁移变成“为了新模板把EP01所有已完成镜头重新写剧本”。

## 3｜Visual-First迁移

历史Reference Routing的已废弃限制不参与当前执行。迁移后统一重新按`visual_reference_routing.md`计算Color / Style / Storyboard的Direct / Panel / Crop / Applied / Text路线，不从旧Prompt或旧任务恢复路由结论。

当前统一读取：
- `visual_reference_routing.md`
- `reference_resolver.md`
- `reference_role_fidelity_isolation.md`

迁移后的默认：
- Approved综合色卡：无真实Direct Fail/Literalization证据时优先Direct Bind；
- Approved Storyboard/4格/6格/9格：按模型能力选择Whole Board / Panel / Key Panel / First-Last / Clean Crop；
- Approved Style Evidence：有合适视觉槽位时优先视觉承担Render Grammar；
- Applied/Clean Reference只在真实失败、槽位或用户明确要求时触发。


## 3.5｜Mandatory Shot Storyboard差量迁移

当前版本硬要求：所有**尚未生成Video**的正式Shot，在Stage 05前都必须有Approved白描Clean Storyboard Panel Coverage，且`STORYBOARD_RENDER_MODE = WHITE_LINE_STORYBOARD_ONLY`。
- 已APPROVED Video：不追溯作废；
- 旧`APPROVED PREVIS SET`只有Hero / Keyframe Pair / Spatial Map / Camera Path / Contact Chain：保留为Supplemental Evidence，但标`LEGACY_PREVIS_BASELINE_GAP`；
- 只为当前尚未生成Video的Shot补白描`CLEAN_STRUCTURAL_STORYBOARD`独立Panel，并由这些Panel确定性拼`CLEAN_STORYBOARD_BOARD`；覆盖全部Shot后再进入Stage 05；
- 旧`Approved Storyboard`若不是白描Clean Panel Baseline，或不能解析到覆盖全部Shot的Board，不能继续视为Stage 05 Gate PASS；彩色/精修旧Board只能作为Supplemental Evidence；
- 旧VCL-0、单Hero直通、Pair直通、Map/Path直通全部废弃。
- 旧`VIDEO_EXECUTION_PLAN`若没有`storyboard_handoff`八字段合同，一律标`REBUILD_REQUIRED`并从Approved Storyboard离图Metadata最小重编；不得仅凭旧Prompt中的泛关键词认定已继承。

## 4｜一次性人物Visual Owner迁移

旧项目中的清楚配角/功能性人物不机械重做主角级完整资产，但必须补登记并复用唯一Base Appearance Owner：
`FMH_ASSET`。

- `TEXT_ONLY`仅限真正深背景且无独立可读职责；
- 已有Approved FMH可直接继承；
- 若旧项目只有Assembly/Previs/Storyboard而没有独立人物母图，迁移时补一张FMH/Minor Human Master；
- 反复/命名/身份连续人物继续使用正式Character Authority。

## 4.5｜Cinematography Grammar差量迁移

旧Approved资产/Previs不会因为新增摄影字段而自动失效。只检查**当前Next Action**：
- 若旧Detailed Shot Contract已经由构图/Reference唯一证明Entry/Landing Camera Geometry/Lens/Focus，登记为`INFERRED_FROM_APPROVED_VISUAL_EVIDENCE`并继续；
- 若Stage 05即将生成且Lens/Focus/Stabilization存在真实歧义，只Patch受影响Shot Contract / Previs，不重做整Scene；
- 旧Prompt中临时追加的“电影感拉焦 / 手持 / 长焦”等没有Stage 02依据的装饰指令一律不继承；
- 已Approved Video不因本次语法补全失效。

## 5｜Duration迁移

任何旧Skill固定秒数上限、固定Slot、默认非法秒数都视为`DEPRECATED_DURATION_PROFILE`。

当前：`SKILL_DURATION_CEILING = NONE`。只有用户、平台UI或当前可靠能力证据提供真实Hard Max/Slot时，才建立新的Platform Duration Profile。旧Workspace保存的历史值不得自动继承。

## 6｜World State / Transformation / Continuity

- 继续继承当前有效World State、伤势、服装、道具、环境破坏、关系与连续性事实；
- 完整合法变身后的普通可恢复伤势按当前Transformation Recovery规则处理；解除变身不恢复旧伤；永久/不可逆状态仍按Canon；
- 旧Ending Frame/Continuity资产可继承，但进入新Video前按当前Reference Routing决定视觉或文字输入方式。

## 7｜Retroactive Episode Asset Freeze

迁移时建立一次追溯式Freeze：
- `VALID APPROVED`：继续使用；
- `WAITING APPROVAL`：等待批准；
- `STALE EXECUTION ARTIFACT`：旧Prompt/旧绑定/旧任务壳，不执行；
- `CURRENT GAP`：只有当前后续生产真正缺的资产/Previs/Authority才补。

完成后直接进入当前真实Next Action，不进行历史版本逐条回放。

## 8｜禁止迁移的内容

以下内容不得从旧版本作为现行规则继承：
- 旧固定视频时长/Slot；
- 旧综合色卡/Style Board/Storyboard全局硬禁；
- 旧Prompt中的文件路径、Asset ID、图A/图B或伪Native Token；
- 旧“为保险预制Applied Reference”任务；
- 已被当前Visual-First、Constraint-First或Prompt Egress Authority取代的流程措辞。


## V4.5.3｜已有资产在Text-only接力时的视觉状态

已有图片没有Current Visual Evidence时，不得因为旧项目曾使用过就自动视为视觉已验证。先登记资产Fingerprint与`visual_evidence_status=MISSING/UNKNOWN`；只有当前任务真正需要复用它时才加入`VISUAL_REVIEW_QUEUE`，无需一次性重审全部图库。


## V4.5.7 Base Authority Override

旧项目中的`SHOT_ASSEMBLY / PREVIS_HUMAN_ANCHOR`不再可作为、共同承担或替代Readable Scoped Cast的Appearance Owner。清楚可见的一次性/配角人物必须补一张Approved FMH/Minor Human Master；正式使用的Environment/Sub-location必须补一张Approved空场景Clean Master。只有深背景不可辨认群众允许TEXT_ONLY。该规则优先于本文旧轻量兼容说明。
