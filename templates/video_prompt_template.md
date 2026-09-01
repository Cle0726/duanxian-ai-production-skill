# AI漫剧视频提示词模板｜Current Authority｜Prompt Control Restoration

> **最高原则：** `@视觉资产负责稳定，不负责替代导演文字控制。` Final Video Prompt必须同时利用Approved视觉Reference与详细文字执行。Reference锁身份、场景、道具、构图与必要的当前视觉状态；综合色由Scene Color Authority贯穿血缘，是否额外占Direct Reference槽由Reference Budget动态决定。文字必须把镜头如何从起始状态走到结束状态写清楚。
>
> **Seedance Prompt Density Contract：** `PROMPT_LENGTH_CEILING = NONE`。Stage 05 Final Video Master Prompt由当前镜头/Sequence的执行完整性决定，**不设置固定字数区间或最大字符数**；复杂镜头允许超过历史3000中文字级。不得因为存在`@Shot Execution Frame`、可选`@Scene Color Card`、Storyboard或Runtime，就自动压缩成几百字短Prompt。目标平台若存在已验证字符上限，先保留完整Source Master Prompt，再由Target Adapter做受控适配；不得静默删除时间轴、动作、表演、摄影机、物理、声音或结尾状态。
>
> **Dedup ≠ Short Prompt。** 去重只删除同一事实的重复表达、行政解释与无效负面词，不删除对Seedance控制走向有价值的细节。

## 0｜Execution Plan硬前置

在进入任何自然语言Final Prompt前，必须读取并通过`video_execution_plan.md`：

`Approved State → VIDEO EXECUTION PLAN → Conflict/Timing/Camera/Spatial/Body PASS → FROZEN_FOR_COMPILE → Final Prompt`

20项Coverage Map用于证明信息完整，**不要求输出20个彼此割裂的栏目**。最终正文优先按“起始条件 → 连续时间窗 → Ending Landing”组织，让Seedance读到一条连续可执行的导演指令。

## 0.4｜Long Video Quota Gate

`PROMPT_LENGTH_CEILING = NONE`与视频时长额度是两个独立概念。Final Prompt本身不设字数上限；但当当前`VIDEO EXECUTION PLAN.duration_sec > 15`时，必须存在`LONG_VIDEO_QUOTA_CONFIRMATION_PASS`后才能冻结/进入真实Generation Job。未确认额度时可以保留导演计划，但不得擅自提交视频生成。

## 0.5｜Generation Envelope / Editorial Mode Gate

Final Video Prompt必须读取当前`GENERATION_ENVELOPE`，不能由Compiler临时决定是否多机位：
- `ONER`：Exactly one Formal Shot，正文明确`NO CUT`，不随机发明第二机位；
- `SEQUENTIAL_MULTISHOT / TIMED_MULTISHOT / FREESTYLE_BROLL`：必须先通过`MULTISHOT_STORYBOARD_GRID_GATE_PASS`，再按`CUT_CONTRACT[]`逐块编译；
- Multi-shot每次CUT不仅改变景别，还要尊重已锁的`VIEWPOINT_ROLE + CAMERA_CHARACTER + INFORMATION FUNCTION`；
- 只允许在Envelope指定边界切镜，不新增CUT；
- 白描Sequence Board可作为结构辅助Reference，但不得代替每个CUT自己的Primary Visual/Conditioning Authority；
- Multi-shot失败可降级为Single-shot Envelopes + Stage 06 Assembly，Editorial Plan保持不变。

## 1｜内部编译顺序（不复制给模型）

`Director/World State → Mandatory Shot Storyboard → Generation Envelope + Multi-shot Grid Gate → Video Conditioning → Reference Resolve → Typed Execution State + Spatial Execution State → Actor/Action/Physics/Camera/Audio Analysis → Conflict Solver → Shot Proof/Motion Budget → VIDEO EXECUTION ANALYSIS → Detailed Compile → Semantic Dedup → Surface/Egress Rewrite → Post-Compile Closure → Final Lint`

任一Hard Conflict、Storyboard Coverage、Primary Visual Conditioning、Scene Color Authority、关键Reference、Action Feasibility或Video Readiness未通过，不输出正式Video Prompt。

## 2｜用户交付必须包含两部分

### Part A｜镜头执行分析（给用户看，不复制给视频模型）

这不是隐藏思维过程，而是**结构化执行结论**。每个Video Unit至少明确：

1. **镜头目标**：这一镜为什么存在，观众应该看到/感受到什么，信息如何推进；
2. **起始状态**：t=0人物、场景、道具、伤势/湿度/服装、正在持续的动作和环境状态；
3. **视觉Reference与@绑定**：Primary Shot Execution Frame为默认主参考；Scene Color Card只在`DIRECT_REFERENCE`模式下额外@；人物/道具/Environment Anchor/Continuity等只按当前风险加入最小充分集合；
4. **人物外观/服装必要确认**：只确认当前镜头最容易漂、且会影响动作/身份识别的可见特征，不重新设计；
5. **场景空间**：前中后景、入口/出口、关键Anchor、人物和道具的相对位置、可行运动路径；
6. **道具状态**：Owner、Holder、哪只手、位置、朝向、开合/破损/湿润等状态与本镜变化；
7. **构图与景别**：主体占画面关系、FG/MG/BG、遮挡、留白、景别和视觉焦点；
8. **摄影机**：机位高度、视角、Lens Family、Focus、Stabilization、开始与结束Camera Geometry、实际运镜；
9. **时间轴**：把整个Video Unit拆成有因果的时间段，不机械均分；
10. **逐段动作**：Preparation → Action → Contact/Transition → Settle/Residual；
11. **表演**：Objective / Tactic / Trigger转成当前景别可见的眼神、表情、姿态、动作节奏和Listener Reaction；
12. **视线**：谁看谁/看哪里，何时转移，是否与Blocking和Cut Motivation一致；
13. **肢体占用**：左右手/脚/身体支撑正在做什么，持物、换手、接触、扶持、承重是否物理可行；
14. **物理反馈**：惯性、重量、碰撞、布料、头发、液体、雨雪、烟雾、道具反作用等；
15. **环境动态**：群众/风/雨/灯/烟/门窗/车辆/背景生命等随时间如何变化；
16. **光影综合色**：对应Scene Color Authority、主光/辅光/环境光、冷暖、明暗、选择性显色和Shot Lighting Variant；
17. **声音**：环境声、Foley、剧情内声音、节奏与画面事件的同步关系；
18. **对白/呼吸**：完整台词、停顿、重音、语速、句尾语调；呼吸只有有剧情/生理原因时才显式导演；
19. **结尾状态**：最后一刻人物/道具/摄影机/环境落在哪里，哪些状态必须传给下一镜；
20. **必要负面限制**：只列当前镜头真实存在且正向描述仍不能充分解决的残余高风险。

分析部分必须来自已锁定Director/World/Storyboard/Runtime，不得在这里重新发明Shot或修改Canon。

## 3｜MODEL-FACING FINAL VIDEO PROMPT结构

### A. @资产绑定

读取`REFERENCE_RUNTIME`与平台Profile。Scene-bound Video至少必须绑定：

- `@当前Shot Execution Frame`：作为Primary Visual Conditioning，锁定当前镜头起始构图、人物/场景/道具关系与可见状态；
- `@对应Scene Color Card`：作为当前Scene Color Authority，锁定综合色、明暗、冷暖和光色关系。

只有当前镜头确实需要额外身份/道具/连续性补强时，再绑定Character/Prop/Ending Frame等Approved Reference。不要为了“保险”堆无关@图。

**基础色卡用于派生Scene Color Card；进入具体Scene Video后，默认不再与Scene Color Card并列成为第二综合色Owner。**

### B. 【镜头目标与时长】

写清：
- 本镜的叙事目标、情绪目标、信息目标；
- 本Video Unit实际目标时长；
- 开头和结尾各自承担什么功能。

### C. 【起始状态与必要视觉确认】

必须写清t=0已经成立的事实：
- 人物位置、朝向、姿态、重心、表情/注意力；
- 当前服装、发型、伤势、湿润/污损等**本镜必须保持一致的可见特征**；
- 场景关键结构、入口/出口、前中后景和固定Anchor；
- 道具由谁持有、哪只手/身体部位承担、状态如何；
- 当前环境状态；
- 起始构图、景别、Camera Geometry与Focus。

视觉Reference已经画清的内容可以避免逐毫米复述，但**不得只写“以@图为准”后省略Seedance理解动作与空间所需的关键事实。**

### D. 【场景空间、构图与摄影机】

根据Detailed Shot Contract具体写：
- Shot Size / Subject Occupancy；
- FG / MG / BG与遮挡关系；
- Axis / Screen Direction / Eyeline；
- Camera Height / Vertical Angle / Subject View；
- Lens Family / Depth of Field / Focus行为；
- Stabilization；
- Camera从Entry到Landing的真实路径、速度、启动/停止点。

如果Camera固定，要明确**固定到什么程度**；如果运动，要明确唯一运动方案，不写互斥“固定或推近”。

### E. 【完整镜头时间轴】

Final Prompt最核心部分。按实际时长拆成连续时间段，例如：

`0.0–2.0s`、`2.0–5.0s`、`5.0–8.5s`……

每一段根据适用内容写清：
- Camera行为；
- 主体位置/朝向/路径；
- Trigger / Perception；
- 逐步身体动作；
- 表演、视线、Listener Reaction；
- Limb Occupancy与道具支撑；
- Contact / Weight Shift / Inertia / Recoil / Settle；
- 环境动态与背景生命；
- 光影变化；
- 对白/声音发生点；
- 该段结束时的Landing State。

时间轴必须表现**因果和过渡**，不能只写一串结果Pose。复杂动作优先写`准备 → 发力/移动 → 接触/反应 → 回弹/稳定 → 新状态`。

### F. 【人物表演、视线与身体执行】

即使相关事实已分布在Timeline中，编译前仍必须完整分析；模型正文可把它们自然融合到Timeline，不需要复制内部字段名。

必须确保：
- 心理变化落成可见行为，不只写“害怕/震惊/悲伤”；
- 眼神变化有对象、有时间点；
- 多人对白存在Active Listening；
- 手、脚、身体支撑与道具使用不冲突；
- 持物手参与新动作时有换手/放下/支撑Bridge；
- 呼吸只有在情绪、疲劳、疼痛、受击、叹气、哽咽等有明确原因时显式可见。

### G. 【物理反馈与环境动态】

按镜头真实需求详细写：
- 起停时的重心与惯性；
- 衣摆、头发、雨水、烟雾、灰尘、纸张、金属、门窗等响应；
- 接触的受力方向、压缩/回弹、道具反馈；
- 环境中的风、雨、灯、群众、车辆、机械、背景运动；
- 动作结束后的Residual Motion与自然衰减。

禁止“人物在动但环境完全冻结”，也禁止为了“有生命感”让所有背景元素同时大幅运动。

### H. 【光影与综合色】

无论Scene Color Card当前是`LINEAGE_ONLY / TEXT_CONTROL / DIRECT_REFERENCE`，文字都要写当前镜头需要Seedance执行的综合色和光线结果：
- 当前Scene综合色关系；
- 主体与环境的综合色分离；
- 主光源方向、强弱、软硬；
- 环境光/反射光；
- Shot Lighting Variant；
- 必要的光影随时间变化。

`@色卡`仅在Direct模式下作为额外稳定锚点；Scene Color Authority本身始终存在。**无论是否直绑色卡，都不是删掉文字光影导演的理由。**

### I. 【对白、声音与呼吸】

有声音时写：
- 完整对白/VO；
- 谁在何时说；
- 从`VOICE_PROMPT_HANDOFF`继承的Performance Loudness / Pace Curve / 有因停顿 / Stress或De-emphasis / Pitch-Energy / Sentence-final Intonation；
- 与嘴型/动作/视线的关系；
- Foley、环境声、剧情内音乐或明确无BGM；
- 钟声、脚步、碰撞、雨声等若承担节奏或剧情意义，必须写清出现顺序、次数/间隔关系与画面同步。

`VOICE_PROMPT_HANDOFF`不得只停留在内部计划：当前Video Unit包含的重要Dialogue/VO必须逐条进入模型正文。若台词存在但Prosody锚点没有进入正文，返回`VOICE_PROMPT_DELIVERY_ANCHOR_MISSING`；若句尾走势丢失，返回`VOICE_PROMPT_TERMINAL_ANCHOR_MISSING`。

### J. 【结尾状态与连续性落点】

明确最后一刻：
- 人物位置/朝向/姿态/表情；
- 道具Holder/Location/State；
- Camera Landing；
- 环境仍在持续的状态；
- 下一镜必须继承的World/Continuity事实。

不能只写“自然结束”。

### K. 【画面保真与必要限制】

保留必要的：
- 人物身份/结构稳定；
- 道具结构与接触准确；
- 人物和环境同一空间、接地/遮挡/反射/景深/边缘光一致；
- 动作连续、无肢体瞬移/身份互换；
- 当前镜头实际证实过的残余高风险限制。

**禁止把通用负面词库机械贴到每个镜头。** 没有人物的镜头不要出现“人物穿插/颈肢胶体/身份互换”等无关限制。

## 3.5｜Integrated Timeline Assembly

Final Prompt的篇幅重点放在Execution Windows。每个时间窗尽量沿同一因果顺序表达：

`Trigger → Perception/微表情 → Preparation/动作 → Eyeline/Limb/Prop → Physics/Environment Response → Camera Read → Sound → Local Landing`

- 不把“表演”“物理”“Camera”“声音”各写一份脱离时间的说明书；
- Camera每个时间窗优先一个Dominant Move，写清Start / Trigger / Path / Speed / Landing；
- 人物表演优先写变化顺序而非情绪标签；
- 身体动作写Preparation、重心、接触、Recovery和Residual Motion；
- 关键Read需要Hold时必须在时间窗内留出真实时长；
- 如果执行计划证明当前时长塞不下，拆Shot/Segment，不靠压缩文字假装可执行。

## 3.8｜Multi-shot Model-facing CUT BLOCK规则

当`FORMAT_MODE != ONER`时，Integrated Timeline必须改为明确的CUT Block序列，而不是把不同机位动作混成一段连续运镜：

```text
FORMAT MODE = <mode>
Exact CUT count = N；cuts only at specified boundaries.

CUT 1 [time optional]
Narrative Function → Camera Start/Character/Path/End → Action → Performance → Information → Exit Trigger

HARD/MATCH/SMASH/... CUT on <locked trigger>

CUT 2 ...
```

规则：
- 每个CUT只保留一个Dominant Camera Idea；
- 每个CUT使用自己Formal Shot的Primary Visual与Storyboard Panel证据；
- `TIMED_MULTISHOT`的各段时长总和必须等于Envelope时长；
- Sequential模式没有强制秒点时，不凭空添加假时间；
- 不写“快速切换多个角度”这种开放式指令；
- CUT数量、顺序、Camera Character、Narrative Function必须与Envelope完全一致。

## 4｜无固定字符上限的完整控制规则

1. **不设置固定字数目标区间或最大字符数**；Prompt长度只由当前镜头所需的时间轴、动作、表演、空间、摄影机、物理、声音和Ending State完整性决定；
2. 字数只计算模型可执行正文，不计算Part A分析、内部State、QC或Binding说明；
3. 不为凑字数重复同义句，新增文字必须承担具体控制职责；
4. 如果Prompt低于2500字，Compiler必须检查是不是丢了：起始状态、空间、道具、Camera、Timeline、表演、视线、肢体、物理、环境、光影综合色、声音、Ending State中的适用项；
5. 如果超过3000字，优先删**重复表达和低价值背景修辞**，不能优先删时间轴、动作因果、Camera、Action Feasibility、声音时序或Ending State；
6. 若目标平台有经过验证的字符上限，完整Master仍保存在运行时/Workspace，再生成平台适配版；不得把平台适配版反写成新的Source Authority。

## 5｜Storyboard / Previs必须参与编译

每一个正式Shot进入Stage 05前都必须有Approved白描Clean Structural Storyboard Panel Set；如果当前Generation Envelope不是ONER，还必须额外有由这些Panel按CUT顺序确定性拼出的Approved白描Sequence Board，且`STORYBOARD_RENDER_MODE = WHITE_LINE_STORYBOARD_ONLY`。Final Prompt编译时必须从Storyboard继承：
- 构图；
- Blocking；
- Cut/No-Cut语义；
- 视线；
- Camera方向；
- 关键动作节点；
- 起始/落点关系。

Storyboard不是可选“参考一下”；它是Final Video Prompt的导演证据之一。Primary Shot Execution Frame负责最终静态执行画面，Storyboard负责时间/构图/Blocking证据，两者职责不同。

**白描分镜文字交接硬要求：** Storyboard图片像素内禁止文字与箭头，因此Storyboard阶段保存在离图Metadata中的`Camera Motion / Timing / Cut-NoCut / Action Beat / Performance / Eyeline / Shot Relation / Landing`必须先写入`VIDEO_EXECUTION_PLAN.storyboard_handoff`，再在本节编译成Final Video Prompt里的可执行自然语言。每个`REQUIRED`项都携带一个`prompt_anchor`；`storyboard_to_video_prompt_handoff_lint.py`会逐项确认该Anchor真实出现在最终正文。只出现“摄影机/时间轴/表演”等同类关键词不算继承。任何字段只停留在Metadata/Plan、没有进入视频提示词，统一报`STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP`并返回Compiler。

## 6｜Semantic Dedup边界

允许删除：
- 完全相同事实的重复句；
- Reference/Authority/Gate等行政解释；
- 同一正向规则的负面镜像；
- 与当前镜头无关的通用负面词。

不得因“去重”删除：
- 必要的人物外观/服装确认；
- 起始空间与道具状态；
- 摄影机执行；
- 时间轴；
- 表演与视线；
- Limb Occupancy / Action Feasibility；
- 物理反馈；
- 环境动态；
- 光影综合色执行；
- 声音/对白/呼吸；
- Ending State。

## 7｜Generation / QC Separation

Final Prompt不写QC Checklist、PASS条件或内部检查语言。Detailed Prompt是**生成控制**，不是QC说明。实际Take生成后再独立执行Video QC。

## 8｜Post-Compile Closure

最终候选经Semantic Dedup、Surface Sanitizer与Egress Rewrite后，必须用`post_compile_constraint_closure.md`反向核对Resolved State。Final Prompt不得出现新约束、漏掉MODEL_TEXT必要事实、重新制造Camera/Audio/Action/Spatial矛盾或互斥分支。

## 9｜COMBAT条件执行合同（仅真实打斗/追逐近身冲突Video Unit启用）

当当前Video Unit被Director/Combat Engine判定为`COMBAT`，上面的20项通用控制**全部继续有效**，并额外要求Final Video Prompt把本Segment可见、可执行的战斗因果写清。不得用“动作激烈”“快速交锋”“自然打斗”等抽象词代替。

至少覆盖：

1. **Combat Objective / Micro-objective**：这一小段到底是压制、试探、保护、拖延、撤离、逼出破绽还是完成关键命中；
2. **Engagement Distance**：Entry → Threat → Weapon Reach/有效攻击距离 → Contact/Near Miss → Exit的距离如何真实变化，禁止瞬移进攻；
3. **Read → Decision**：人物先看见/听见什么威胁，如何判断来势，再选择格挡、闪避、拨挡、截击、后撤、侧移或反击；
4. **Attack / Defense Exchange**：进攻与防御必须形成因果交换，不写双方各自动作的平行清单；
5. **Attack Lane / Escape Lane**：攻击线、闪避路径、撤离线和场景障碍必须与当前空间、站位和轴线兼容；
6. **Contact Point / Near Miss**：命中、格挡或险些命中的具体位置与时间点必须可读；
7. **Force Direction**：接触后的力量方向如何从接触点传到身体质量、重心和支撑点；
8. **Recoil / Recovery**：攻击者与受击/防御者的反冲、回弹、收招、暴露窗口和动作余势；
9. **Initiative Shift**：谁在逼迫谁回应，主动权何时、因为什么发生交换；
10. **Combat Camera Read**：摄影机必须让关键攻击方向、接触点、距离压缩/释放和主动权变化可读，不允许运镜遮掉动作因果；
11. **Exit Combat State**：本Segment结束时双方距离、朝向、重心、武器/道具状态、主动权与下一轮攻防入口必须稳定可承接。

**战斗表演仍受Actor Performance约束。** 战斗中的眼神、微表情、呼吸、迟疑、疼痛、疲劳和关系反应必须挂在`Read → Decision → Commitment → Contact/Near Miss → Recovery`的因果链上，不能为了动作密度把人物变成扑克脸。

**复杂战斗不要硬塞。** 若一个Video Unit无法同时清楚证明距离、攻防、接触、受力、表演和Camera，应按Combat Exchange拆Segment，而不是删掉这些控制项。

## Current｜Prompt Artifact Binding Hard Gate

Source Master Prompt通过Detail/Combat/Conflict/Surface检查后，必须先持久化为`VIDEO_PROMPT_ARTIFACT`，记录真实`prompt_ref + prompt_fingerprint + execution_plan_fingerprint`。Video Job只能执行这一个已冻结版本；模型后续任何自然语言改写都会改变Fingerprint并使旧Job失效，禁止“看起来差不多”继续生成。

## V4.5.7｜Entity Binding → Blocking/Action Final Surface

最终正文必须把每个Storyboard Human Slot反编译为真实人物，并至少写清：
`人物身份/对应@资产（若Direct） + 世界站位 + 画面投影 + 身体朝向 + 当前姿态 + 当前动作阶段 + 交互对象/持物（适用时）`。

示例语义（仅示意结构，不固定措辞）：
`@角色A站在控制台左侧中景，身体朝向角色B，右臂向前伸出，动作处于递交中段；角色B位于其右侧半步，转身面向A，抬手准备接取。`

禁止输出内部`H_A/H_B/...`。匿名白描只提供几何证据，最终视频模型收到的必须是明确可执行的人物站位与动作自然语言。
