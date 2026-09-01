# Asset Library Completeness Policy（资产库完整性策略）

> **Owner：Stage 02 → Stage 03资产规划与Freeze。** 本策略只定义“资产库应做到多完整”，不定义单次Video Job要上传多少Reference；单次Reference选择仍由`reference_resolver.md`拥有。

## 1｜核心原则

**RICH CANON LIBRARY ≠ LARGE VIDEO REFERENCE PACK。**

《断弦之歌》的静态图片资产生产不设置固定图片数量上限，也不因为Stage 05需要`MINIMUM_SUFFICIENT_REFERENCE_SET`而反向减少Stage 03应有的正式视觉Authority。

- Stage 03目标：在本集真实剧情/镜头需求范围内，建立**可复用、可核验、可追踪血缘的充分视觉Authority库**。
- Stage 05目标：从完整Asset Registry中，为当前Video Generation Job选择**最小充分Reference Pack**。
- “本镜不直接@”不等于“Stage 03不用建”。只要该资产承担正式Identity / Spatial / Prop / Performance / Narrative FX / Persistent State等Authority并被本集真实Shot需要，就必须先完成资产闭环。
- 图片资产多不是失败条件；**无Owner、重复Base Master、版本不清、血缘不明、未批准却被下游引用**才是失败条件。

## 2｜Stage 03 Completeness Domains

Freeze前至少检查以下适用Domain：

1. `BASE_VISUAL_AUTHORITY`：命名/主要人物、清楚配角、正式Environment/Sub-location、关键Prop等基础Authority；
2. `REQUIRED_COVERAGE`：真实Camera / Visible Surface / Event Node要求的Environment/Prop视角；
3. `PERFORMANCE_SUPPORT`：特殊表情、动作姿态、复杂Contact等静态可解的表演风险；
4. `NARRATIVE_FX`：具有剧情身份、重复性、状态连续性或高视觉歧义的叙事特效；
5. `PERSISTENT_STATE / PRODUCTION_SUPPORT / SHOT_ASSEMBLY`：现有Stage 03风险前置资产；
6. `AUDIO_ASSET_MANIFEST`：音频由独立Manifest管理；本策略不把音频数量混入图片Reference Budget。

## 3｜不允许的错误优化

以下均视为`ASSET_LIBRARY_UNDERBUILD`：

- 因为视频@槽位有限，所以Stage 03不建立应有的人物/场景/道具母图；
- 因为当前Primary Visual暂时看起来够用，所以跳过已被Requirement标记的Performance Support或Narrative FX Reference；
- 把白描Storyboard当作人物Identity、最终材质或FX视觉Canon；
- 把空场景母图当人物Identity；
- 为了减少资产数量，把多个不同Entity/Location/Prop错误合并成一个Base Master；
- 以“模型应该能猜”为理由跳过低成本静态图可以明确消除的高风险视觉歧义。

## 4｜同时禁止无理由过量生产

“资产库做足”不等于机械生成固定套装。

- 主要/反复人物可按Character Requirement Set建立高频身份资产；
- 一次性清楚配角必须有Base Master，但表情/动作Support只按真实Shot风险建立；
- Environment / Prop Coverage按真实Camera与Visible Surface需求建立，不机械四视图；
- Narrative FX只有在重复、剧情识别、连续状态或高歧义时升级正式Reference；普通一次性简单效果保留`TEXT_GRAMMAR_ONLY`；
- 不为“以后也许用到”生成无Shot依据的正式资产。

## 5｜Freeze硬门

`ASSET_LIBRARY_COMPLETENESS_PASS`只有在以下条件同时满足时成立：

- Base Visual Authority闭环；
- 所有`STAGE_03_FREEZE`且未被合法Waive的视觉义务已FULFILLED并有Approved Asset；
- 所有Required Performance Asset Requirement已完成；
- 所有要求视觉Reference的Narrative FX已完成；
- Required Asset的Registry记录、Entity/Scope/Authority Role、Approval与Lineage一致；
- 没有用`MINIMUM_SUFFICIENT_REFERENCE_SET`作为缺资产的理由。

该Gate在`EPISODE_ASSET_FROZEN`前必须为PASS；Freeze Broken后重新进入时必须重算。

## 6｜Stage 05边界

资产Freeze通过后，Stage 05继续执行：

`RICH ASSET LIBRARY → Field Coverage → Identity Readability → Reference Resolver → MINIMUM_SUFFICIENT_REFERENCE_SET → Video Job`

因此：**库可以很丰富，单镜发送仍然克制。**

项目策略继续禁止参考视频；动作/运镜不通过Reference Video补齐。
