# Candidate Triage（候选自动筛选）

> **用途：** Stage 03/04按`image_candidate_strategy.md`计划产生多个图片/Storyboard候选时，或Stage 05合法存在多个Video Take时，Skill替用户比较并推荐最佳候选。**图片多候选是主动生产策略；Video多Take不是。** Video候选预算仍由`personal_creator_cost_efficiency_engine.md`控制，普通T1/T2始终1 Take起步。

## 核心原则

**先按生产正确性筛，再按美观度排序。**

“最好看”但身份、空间、动作、连续性或前景主脸/手/关键接触存在明显硬伤的候选，不应排第一。HERO/FUNCTION级明显解剖/接触错误直接淘汰，不进入“审美更好所以Primary”的比较。

## 适用对象

- Character / Environment / Prop候选资产；
- Storyboard候选；
- Video Take候选；
- Ending Frame候选。

## 图片候选默认流程

图片计划候选组不是“每张都先做完整深QC”，而是：

1. Asset Intake确认同一Job / Candidate Group；
2. `FAST TRIAGE`：所有候选先做P0/P1快速筛除；
3. 选出`PRIMARY QC CANDIDATE`与`BACKUP CANDIDATE`；
4. 只对Primary执行完整Deep QC；
5. Primary失败时，先检查Backup是否已不存在同一失败点；若是，Backup升级Primary进入Deep QC；
6. Backup也失败，才进入Revision / Fresh Regen。

只有最终`QC PASS + 用户明确批准`的一张进入APPROVED / Freeze。

## 图片候选评分顺序

优先检查：

1. Identity / Structure（身份或结构是否正确）；
2. Foreground Figure Integrity：HERO/FUNCTION级脸、手、腕部、关键接触无明显硬伤；
3. Continuity（连续性）；
4. Composition / Action（构图和动作）；
5. Style（画风）；
6. Detail / Finish（细节与完成度）；
7. Aesthetic Preference（审美偏好）。

## Video Take评分顺序（Best Take Selection）

优先检查：

1. 人物身份与造型稳定；
2. 动作 / Physics正确；
3. Camera / CUT / Timing正确；
4. 场景与道具稳定；
5. 表演是否达到Beat目标；
6. 是否能提供高质量Ending Frame；
7. 综合色和整体观感。

## 输出格式

### 图片 / Storyboard
```text
【Candidate Triage｜图片候选筛选】

Primary：CAND02 ★★★★★
原因：
- P0身份/结构正确
- 当前Task Contract执行最完整
- 构图/材质/画风最稳定

Backup：CAND01 ★★★★☆
主要问题：一个P1局部可修，但整体方向成立

Rejected：CAND03
原因：结构漂移 / 空间错误 / Canon冲突

Next：CAND02 → Deep QC
```

### Video Candidate Recommendation
```text
【Best Take Selection】

Primary：TAKE02 ★★★★★
Backup：TAKE01 ★★★★☆
Next：TAKE02 → Video QC
```

## 自动批准边界

Skill可以明确“推荐哪个”，但除非用户已授权自动采用最佳候选，正式 `APPROVED` 仍遵守项目现有批准规则。

## 返工节省原则

### Images / Storyboard
Primary Deep QC失败时，先看Backup是否已经规避同一P0/P1问题；有更好的现成Backup时先切Backup，不急着Revision或Fresh Regen。若Primary大部分正确且Backup也没有更优解，再对Primary做最小Revision。

### Video Rework
如果一个Take只有末尾小问题，而另一个整体动作都错，优先判断是否能通过Trim / Post Fix / 更好Ending Frame解决，而不是为了轻微瑕疵重生整段。

## Asset Intake入口

用户上传多个候选时，先由Asset Intake确认这些候选属于同一个Job，再进行横向比较。图片/Storyboard的计划候选数读取`image_candidate_strategy.md`；多候选必须共享同一Task Contract，不允许用“候选”名义让Canon、身份、场景几何或Style分叉。视频候选比较只处理已经存在或按T3/T4受限预算合法产生的多个Take，不得反向变成“每个Prompt固定先生成多个Take”的生产要求。不同Segment、不同资产任务不得混成同一候选组。

连续性比较时使用 `Continuity Priority`：P0问题优先淘汰；P2自然差异不能把本来更好的候选降为失败项。


## Stop / Continue

### Images
如果当前Image Job已经计划2或4张，可完成该小组后统一Triage；不采用“第1张看起来不错就立即取消剩余廉价候选”的Video规则。获得可批准Primary后，不再无上限扩大Candidate Group。

### Video Stop Rule
第一个Take已经通过QC时立即停止继续生成。Take上限是成本保护线，不是必须用满的配额。


## Current｜Temporal Salvage Across Takes
如果已经合法存在多个Video Take，但没有一个Whole Take完整PASS，不得只比较“哪个整体分高”。先导入每个Take的`TEMPORAL_SALVAGE_MAP`，判断是否存在互补`CLEAN_KEEP / CONDITIONAL_KEEP`窗口。

只有同时满足Identity / Axis / Action Entry-Exit / Lighting / Style / Audio Continuity与Director允许Cut时，Stage 06才可组合不同Take；否则继续按Best Whole Take + Failure Diagnosis处理。

多Take存在Salvage潜力不能反向成为“以后每次都先生成多个Take”的理由。
