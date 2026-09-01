# Cinematic Combat & VFX Engine（《断弦之歌》电影级战斗与特效引擎）

> **定位：** 把《断弦之歌》的Music Identity、战术编排、身体/武器物理、共鸣特效、摄影机与声音统一成同一条因果链。它不是“华丽特效词库”，也不是“每个技能套一套爆炸模板”。
>
> **核心命题：** 音乐不是战斗皮肤，而是战斗的时间与运动语法；特效不是贴在动作上的光，而是力量在空间中的可见证据。
>
> 本模板与 `combat_choreography_engine.md` 配合使用：Combat Choreography负责“为什么打、怎么打、谁获得主动权”；本引擎负责“音乐身份怎样进入打法，以及接触、重量、VFX、Camera、SFX怎样被电影化执行”。

---

## 1｜Authority Boundary（权威边界）

优先级：

**Story / World Canon → Approved Character / Transformation / Weapon / Music Identity → Current State → Runtime Derived Combat/VFX**

必须遵守：
- 已明确的曲式、乐器、声部、技能、调性、武器、共鸣代价照Canon执行；
- 未明确的大调/小调、调号、具体作品、作曲家、专业演奏法不得为了“音乐感”擅自定死；
- `DERIVED`的动作/VFX解释只服务当前执行，不能反向改写Canon；
- 《宿命回响》等只可作为参考/致敬来源，不得把其角色、技能名、世界观术语或成品视觉身份写入《断弦之歌》项目Canon；
- Stage 05仍遵守 `NO AUTO BGM`。Music Identity进入动作、镜头、SFX与Stage 06音乐交接，不等于视频模型自动配乐。

---

## 2｜Musical Combat Translation Layer（音乐战斗转译层）

### 2.1 核心链路

**Story / Character Meaning**
→ **Music Identity**
→ **Musical Time Grammar**
→ **Musical Motion Grammar**
→ **Tactical Combat Grammar**
→ **Body / Weapon Mechanics**
→ **Cinematic Impact**
→ **Cinematic VFX**
→ **Camera / SFX**
→ **New Combat State**

禁止跳过中间层，直接从“音乐身份”跳到“某颜色粒子/音符爆炸”。

### 2.2 Musical Time Grammar（音乐时间语法）

根据当前已批准Music Identity与Scene Overlay，按需转译：
- `Tempo Feel`：动作整体速度感，不等于固定BPM；
- `Attack Cadence`：攻击之间的间隔与重音；
- `Rest / Hold`：主动空白、等待、压住一拍；
- `Acceleration / Ritard-like Deceleration`：动作如何加速/放缓；
- `Repetition / Variation`：重复结构是否发生意义变化；
- `Syncopation / Off-beat`：是否利用预期之外的空档或弱拍；
- `Sustain`：力量/控制是否在接触后继续存在；
- `Counterpoint`：多人或攻防两条独立运动如何同时成立并互相咬合；
- `Crescendo / Diminuendo`：动作、压力、VFX、声音如何渐强/渐弱；
- `Cadence / Closure`：攻击段何时真正落地；
- `Unresolved Phrase`：故意不给完整终止感，保留下一动作/叙事悬挂。

这些字段首先控制**时间结构**，不是要求画出乐谱。

### 2.3 Musical Motion Grammar（音乐运动语法）

把时间语法继续翻译为：
- 步法节奏与重心移动；
- Attack Commitment曲线；
- 武器启动/加速/转向/回收方式；
- 防御是硬挡、卸力、等待、截击还是反拍；
- Recovery轻/重/长/短；
- 多人Initiative Handoff；
- 终结技的预期建立与兑现。

**角色音乐身份必须改变“怎么打”，不能只改变颜色。**

### 2.4 Music Symbol Restraint（音乐符号克制）

默认：音乐通过**时间、动作、空间、声音与材质响应**呈现。

五线谱、音符、谱号、调号、休止符等可见符号只有在以下情况使用：
1. Story / World / Approved Asset已确认其真实存在；
2. 该符号承担剧情或机制功能；
3. 它来自武器/瞳孔/噪骸残留/已确认共鸣结构，而不是为了“看起来像音乐”临时贴上。

禁止：
- 满屏漂浮随机音符；
- 每个技能都生成魔法五线谱；
- “大调=金色开心 / 小调=蓝色悲伤”的机械映射；
- 只给不同角色换VFX颜色却保持相同运动方式。

---

## 3｜Musical Function → Combat Function（音乐功能转战术功能）

以下是**转译逻辑，不是固定角色技能库**：

- `Rest`：创造短暂行动空白、停止窗口、攻击取消或节奏剥夺；
- `Cadenza / Free Passage`：高技巧、高自由度、速度变化明显的个人爆发段；
- `Sustain / Pedal-like Hold`：控制/压力在动作结束后仍继续作用；
- `Counterpoint`：独立攻防/多人路线同时进行，彼此形成反制或支撑；
- `Repetition`：重演同一动作结构，但第二次必须有信息/战术变化；
- `Diminuendo`：存在感、共鸣、动作幅度或可追踪性逐步下降；
- `Crescendo`：压力/速度/力量逐步积累，不在第一帧直接最大；
- `Syncopation`：在对手预期的“空档”或收招点抢入；
- `Da Capo-like Return`：若Canon支持“从头开始”，优先解释为目标动作/共鸣结构回到Startup，不自动让整个世界、伤势、环境破坏时间倒流；
- `Cadence / Finality`：通过明确落点、重心稳定、空间结果与声音尾音形成终止；
- `Unfinished / Unresolved`：动作可在应当收束处故意留下未闭合路线/未解决压力，但必须有叙事原因。

任何音乐术语进入战斗前都必须回答：**观众不懂术语时，单看动作能不能感受到它？**

---

## 4｜Cinematic Impact Chain（电影级打击链）

重要接触优先使用：

**Intent → Setup → Acceleration → Contact Point Lock → Compression → Micro Hit Hold → Force Propagation → Recoil → Secondary Motion → Environment Proof → Aftermath → New Combat State**

### 4.1 Intent / Setup
- 为什么现在出这一下；
- 身体如何建立发力条件；
- 脚步、髋、肩、手/武器是否按武器结构合理进入线路；
- 全承诺攻击必须有可见Recovery风险。

### 4.2 Contact Point Lock（接触点锁）

必须明确：
- 武器哪一部分；
- 接触目标哪个部位/结构；
- 接触角度；
- Force Direction（力量方向）。

禁止“挥过画面以后目标自己飞走”。

### 4.3 Compression / Micro Hit Hold

重击接触时先出现极短的运动压缩感，再释放力量：
- 不是整段视频冻结；
- 不要求精确毫秒；
- Light Hit可几乎无停顿；
- Medium Hit有短速度压缩；
- Heavy Hit让武器/防御结构明显吃住一瞬；
- Massive Impact可让局部世界像被压住后再展开，但不能每击都用。

### 4.4 Force Propagation（力量传播）

目标反应应尽量沿：

**Contact Point → Nearby Joint / Structure → Torso / Main Mass → Center of Gravity → Foot / Ground / Support**

有合理延迟，而不是全身同帧一起后退。

命中不同位置，反应必须不同：肩、腿、盾、躯干、武器、墙体不能共享同一套击飞动画。

### 4.5 Recoil（反作用）

攻击者也必须承担物理后果：
- 武器回弹/滑开；
- 肩/腕/躯干承受反震；
- 重心需要重新稳定；
- 全承诺攻击产生Recovery窗口。

这属于`Execution Consequence`，不是擅自新增Lore Cost。

---

## 5｜Near Miss Physics（险些命中的物理）

Near Miss不是“攻击没打中所以什么都没发生”。

按攻击尺度可见：
- 头发/衣摆被气流带动；
- 雨滴、雾、尘被切开；
- 身后墙/幕布/地面被攻击路线擦伤；
- 防守者身体为了避开攻击真实改变重心；
- 攻击者因落空进入Recovery或暴露Counter Window。

高质量Near Miss可以比连续命中更紧张。

---

## 6｜Cinematic VFX Causality（电影特效因果链）

每个重要VFX至少内部回答：

**Cause → Source → Formation → Spatial Geometry → Motion → Medium / Environment Interaction → Contact Behavior → Lighting Interaction → Decay → Residue / State Change**

### 6.1 Cause / Source

特效必须有来源：
- 身体共鸣；
- 已确认武器结构；
- 瞳孔/谱核/共鸣腔；
- 环境中的噪骸残留；
- 已确认技能机制。

禁止无动作原因地“突然全身发光”。

### 6.2 Formation

说明特效如何形成：
- 汇聚；
- 拉紧；
- 压缩；
- 扩散；
- 振荡；
- 延迟残留；
- 沿武器/地面/弦线/空气压力建立。

### 6.3 Spatial Geometry

VFX必须生活在场景空间中：
- 有前后深度；
- 受人物/物体遮挡；
- 服从透视与攻击路线；
- 被墙、地面、柱子、敌人结构截断/反射/吸收时有合理变化；
- 不作为永远浮在画面最前层的2D贴纸。

### 6.4 Environment Proof（环境证明）

超自然力量优先通过真实介质显形：
- 雨滴轨迹；
- 雾/烟/尘；
- 水面波纹；
- 幕布/纸张/衣料；
- 灯具/金属件共振；
- 地面碎屑；
- 冰、玻璃、木、石、铁等材质响应。

**环境证明比无意义增加粒子更优先。**

### 6.5 Lighting Interaction

有亮度的VFX必须按需要影响附近材质：
- 手/脸/衣服边缘反光；
- 湿地/金属/玻璃局部反射；
- 距离增加后亮度自然衰减。

禁止VFX很亮但人物和环境完全不受光，也禁止为了“电影感”全屏过曝。

### 6.6 Contact Behavior

VFX命中时优先改变：
- 压力；
- 方向；
- 结构；
- 平衡；
- 速度；
- 共鸣状态；
- 空间控制。

不是所有技能都“爆炸”。音波、低频、弦线、休止、秩序、反复等应有不同接触逻辑。

### 6.7 Decay / Residue

技能结束后不能一帧清空：
- 光衰减；
- 灰尘/雨/碎屑继续运动；
- 衣物/头发晚于主体恢复；
- 表面损伤保留；
- 共鸣残留按Canon衰退；
- World State发生的破坏必须交给 `world_state_continuity_engine.md` 持续记录。

---

## 7｜VFX Identity ≠ Color Swap（特效身份不等于换颜色）

不同圣谱者至少在以下三项中形成明显差异：
- Timing / Cadence；
- Geometry；
- Motion / Decay；
- Environmental Interaction；
- Contact Behavior；
- Sound Texture；
- Weight / Recovery。

如果两个角色只是“同一种光束，一个金色一个蓝色”，判定Music-to-Combat Translation失败。

### 7.1 Signature VFX Grammar Card（标志性战斗特效语法卡）

对跨多Scene/多Episode重复出现、角色识别度高或结构复杂的技能/共鸣效果，可建立可复用`Signature VFX Grammar Card`，至少记录：
- VFX ID / Version / Approval Status；
- Music Identity Ref；
- Cause / Source；
- Base Geometry；
- Motion / Timing；
- Contact Behavior；
- Environment / Medium Interaction；
- Lighting / Emission Range；
- Decay / Residue；
- Impact Scale Range；
- Forbidden Mismatch。

若纯文字Grammar足够稳定，不强制新增图片资产。只有反复生成时确实需要固定形状/材质/层级关系，Stage 02才标记`VFX_REFERENCE_REQUIRED`，Stage 03使用现有资产生产流程建立Approved VFX Reference / Effect Board并进入Episode Asset Pack。**不要为每次普通击打都制造一张VFX母图。**

---

## 8｜Impact Scale（冲击层级）

按剧情需要自动选择，不以“越大越好”为原则：

- `PERSONAL`：主要影响身体/武器；
- `LOCAL`：附近衣物、尘、水、轻物体响应；
- `ENVIRONMENTAL`：地面、墙、窗、灯具等明显响应；
- `STRUCTURAL`：改变场景结构，必须写回World State；
- `NARRATIVE`：直接改变剧情/世界机制，如核心破坏、静默场解除等，只能来自Story/Canon。

VFX亮度/面积与Impact Scale不必一一对应。低频、休止、控制类能力可以极少发光但影响很大。

---

## 9｜Camera as Witness（摄影机是见证者，不是打击替身）

摄影机首先保证读懂：
- 攻击线；
- 接触点；
- 力量方向；
- 目标位移；
- 新空间关系。

同时继承Stage 02 `Combat Spatial Directing`：
- Engagement Distance Ladder；
- FG / MG / BG层级；
- Contact Read Shot；
- Initiative Shift Visual；
- Camera Intent / Axis / Screen Direction。

**摄影机不承担“把所有人都看全”的义务。** 允许前景武器、肩背、锁链或环境元素切入画面，只要Critical Contact/Threat Read不被遮挡。战斗构图应随距离和主动权变化，不应长期保持等距全身阵容。

Camera Shake只在冲击足以影响观察者时使用，并尽量具有方向性。

禁止：
- 每次命中都随机震屏；
- 用快速推拉/旋转替代真实身体与环境反馈；
- 关键接触时切到看不清的位置；
- 全程手持抖动掩盖动作失败。
- 所有参战者长期同深度、同尺寸、均匀间距，画面像阵容展示；
- 主动权/距离已经改变，但Camera与构图完全没有空间反馈。

有时稳定远景比震屏更能证明巨大重量，因为观众可以完整看到结构被改变。

### Impact Space Reserve（冲击空间预留）

Stage 04构图时，若角色/目标将在某方向被推动、击飞、逼退，应提前给该方向保留画面空间。冲击后构图最好发生真实变化，而不是双方自动回到原位。

---

## 10｜Sound-Impact Handoff（打击声音交接）

Stage 05只生成当前允许的SFX/Foley；Stage 06完成正式声音设计。关键接触可按需拆：
- `Transient`：接触瞬间；
- `Body`：主体重量；
- `Sub / Low-End`：大型/低频冲击的身体感（适量）；
- `Material`：金属/木/石/冰/布等材质声；
- `Debris`：延迟碎屑；
- `Tail / Space`：空间尾音/混响。

声音也允许时间层次，不要求所有层同时出现。

关键剧情级冲击可设计`Post-Impact Vacuum`：强接触后短暂减少声音信息，再由耳鸣/碎屑/环境声恢复；只在真正重要节点使用，不作为每次重击模板。

**BGM不能替代打击声。** Stage 06关键Contact可对BGM做短Ducking，给Transient / Body留空间；Stage 05仍禁止自动BGM。

---

## 11｜Cost Coupling（音乐/技能代价耦合）

《断弦之歌》已确认的圣谱者技能与武器维持存在共鸣代价时，电影表现优先把代价写进：
- 动作精度；
- Recovery；
- 稳定度；
- 乐监握持/节拍纹/听觉/心律相关已确认表现；
- 圣谱者当前已确认的共鸣衰减；
- 武器/VFX稳定度变化（仅Canon支持时）。

禁止为了“强招有代价”自行新增吐血、骨折、寿命百分比、技能冷却等新Canon。

---

## 12｜Combat State Persistence（战斗状态持续）

每个重要Exchange结束后建立`New Combat State`，至少按需要记录：
- Distance / Measure；
- Initiative；
- Facing / Position；
- Weapon State；
- Guard / Recovery State；
- Injury / Cost State；若已触发Transformation Recovery，Injury使用Post-Recovery State，Cost保持独立Authority；
- Environment Damage；
- Persistent VFX / Field；
- Exposed Weakness / Core State。

下一Shot/Segment从这个状态继续。禁止：
- 每个Segment重新摆成起手式；
- 已破坏墙/地面自动恢复；
- 已逼到墙边下一段突然回到八米外；
- 已形成的持续共鸣场无因消失。

与 `world_state_continuity_engine.md` 共用State Diff原则。

---

## 13｜Stage Integration

### Stage 02｜Combat / Music Design Brief

除Music / Impact设计外，必须与`director_architecture_engine.md`同步建立Engagement Distance Ladder、Spatial Dominance、Attack/Defense Lane、Depth Strategy、Contact Read Shot与Initiative Shift Visual；这些是导演Authority，不留到Storyboard临场决定。

战斗Scene在原Combat Design Brief基础上，按需增加：
- `Music Identity Ref`；
- `Musical Time Grammar`；
- `Musical Tactical Function`；
- `Impact Scale Target`；
- `VFX Physical Principle`；
- `VFX Reference Need`：TEXT_GRAMMAR_ONLY / VFX_REFERENCE_REQUIRED；
- `Key Contact / Payoff`；
- `Sound-Impact Handoff`；
- `Persistent Combat / Environment State`。

Stage 02不写满逐招动作，只确定本场音乐与战斗的“语法”。

### Stage 03｜Signature VFX Reference（仅需要时）

若Stage 02标记`VFX_REFERENCE_REQUIRED`，才建立可复用Effect Reference / VFX Grammar Board，锁定Source、Geometry、Material/Light Interaction、Contact与Decay。其职责只是固定标志性VFX身份，不取代角色/武器/环境Master，也不预画具体Storyboard构图。

### Stage 04｜Storyboard

Storyboard继承Stage 02空间导演。若候选把Combat变成同深度全身展示，直接`COMBAT_LINEUP_FAIL`，不以“人物都看清了”作为通过理由。

重要战斗Panel除Combat Exchange外，应读出：
- 音乐时间结构（Hold / Acceleration / Sustain / Off-beat等）；
- Contact Point与Force Direction；
- 为冲击预留的空间；
- VFX来源/几何/环境介质；
- Impact前后的构图差异；
- Aftermath与下一Combat State。

### Stage 05｜FINAL VIDEO PROMPT

不要把“Crescendo / Counterpoint / Syncopation”等术语单独丢给模型。Compiler优先翻译成可见执行：

**Current State → Intent → Body/Weapon Setup → Musical Timing → Contact / Near Miss → Impact Physics → VFX Cause/Space/Environment → Recoil/Aftermath → New Combat State**

模型Prompt避免泛化：
- “cinematic impact”；
- “epic VFX”；
- “powerful explosion”；
- “beautiful musical particles”；
- “dramatic camera shake”。

除非后面已经说明它们具体怎么发生。

### Stage 06｜Post

正式完成：
- 角色/场景Music Cue；
- Combat SFX分层；
- Contact瞬态与低频；
- BGM Duck / Silence / Re-entry；
- VFX声纹与角色Music Identity的一致性。

---

## 14｜QC Failure Signs（失败征兆）

出现任一项需要诊断：
- 战斗音乐元素只剩漂浮音符、五线谱、换色Glow；
- Music Identity没有改变步法、攻击节奏、Recovery或战术；
- 每个角色技能都是不同颜色的光炮/爆炸；
- 武器未真正运动，特效却先独立飞出；
- 命中接触点不清楚，目标无因飞走；
- 所有命中都同一种Camera Shake；
- Heavy Hit没有Compression / Force Transfer / Recoil；
- Near Miss没有任何空间/环境后果；
- VFX没有遮挡、透视、环境或光照互动，像画面贴纸；
- 大招第一帧即全屏最大，没有Anticipation/Build；
- 技能结束后一帧环境恢复干净；
- 战斗每个Segment重新起手，距离/破坏/持续场无因重置；
- “Da Capo/反复”等时间类效果擅自把整个世界倒流；
- 为了音乐感擅自新增曲名、调性或专业设定；
- Stage 05把Music Identity误编成自动BGM。

---

## 15｜One-Line Rule（总规则）

**让音乐决定力量怎样发生，让物理证明力量真的发生，让VFX证明这种力量属于谁，让战场状态证明这一击改变了什么。**

## V4.5.7｜Narrative FX Boundary

Combat技能/打击的VFX Grammar仍由本文拥有；非战斗、非纯Transformation且承担剧情规则/线索/环境异常身份的视觉现象，转交`narrative_fx_asset_standard.md`。同一个效果只能有一个Primary Authority：Combat VFX、Transformation FX、Narrative FX三者不得重复建Canon。
