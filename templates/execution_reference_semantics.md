# Execution Reference Semantics（执行Reference语义）｜Current Authority

> **核心原则：** 本文件只拥有**Reference绑定、字段职责与原生`@资产`Mention**，不拥有Stage 05正文长度、详细度或导演信息裁剪权。《断弦之歌》当前**视频Reference能力默认采用`MULTIMODAL_ALL_ROUND_REFERENCE`（多模态全能参考）**；这定义底层模型具备多模态职责理解能力；项目实际Video Job只允许文字、图片和音频，参考视频硬禁用。调用表面与能力层分离：当当前Host支持命名资产时，Prompt Surface采用`NAMED_ASSET_MENTION_REQUIRED`。凡当前任务真正参与生成控制的Approved Asset，只要属于MUST_BIND / DIRECT_BIND / EDIT_TARGET / PATCH_DESIGN_REFERENCE / CONTINUITY_ENTRY / AUDIO_AUTHORITY / VOICE_AUTHORITY / RHYTHM_AUTHORITY / AMBIENCE_AUTHORITY / MUSIC_AUTHORITY / SFX_AUTHORITY等强绑定模式，Final Prompt必须显式出现对应平台原生`@资产`Mention。`@Mention`后的局部职责句应简洁，但**整份Final Video Prompt仍必须遵守`video_prompt_template.md + prompt_compiler.md`的详细导演控制合同**。不得因为资产已存在于项目、Runtime或UI中就静默省略，也不得因为Reference已经画清某些静态事实就删除当前Shot执行所需的文字确认。

## 1｜内部保留，模型侧不打印
Asset ID / Version / Path、Why Now、Most Direct、Role表、MUST_BIND、Executor Input Map、Registry、Gate结果都留内部。

## 2｜Reference控制如何进入模型
- Character/Human视觉Owner → 身份、服装、体态连续性；
- Environment → 空间、材质、几何；
- Color Card →综合色/冷暖/饱和度集中/明度层级；
- Style Reference →绘制语言；
- Mandatory Storyboard/Panel →每Shot构图、Blocking、动作状态、时间推进、CUT关系；
- Supplemental Previs →仅其独占的Camera Path / Spatial / Contact / Hero字段；
- Ending/First Frame →入口连续性。

当前《断弦之歌》Generation Profile优先使用**命名资产Mention**：`@<资产显示名> + 最短执行句`。每个当前任务MUST_BIND的Reference都必须在Copy Surface出现一次真实Mention；同一资产不要重复@。只有Target Adapter明确声明`ui_binding_without_prompt_mention_allowed=true`时，才允许仅UI绑定而正文不写Mention。若平台只支持顺序图号，则必须从本次真实Binding Map映射为`@图N`，不得按历史顺序猜测。


## 2B｜Generation Asset Mention Contract

读取`adapters/generation/platform_profile.yaml`。Current Project Default Capability = `MULTIMODAL_ALL_ROUND_REFERENCE`；Named-Asset Host上的Current Prompt Surface = `NAMED_ASSET_MENTION_REQUIRED`。

- `REFERENCE_RUNTIME.bindings[]`中凡`binding_mode`属于强绑定模式且`emit_on_prompt != false`，必须解析出`native_token`；
- 优先使用Registry/Runtime中已经登记的真实`native_token`；若平台以资产显示名作为Mention，则使用`@{asset_display_name}`；
- 每个强绑定资产在FINAL_COPY_SURFACE至少出现一次；缺失 = `MISSING_REQUIRED_ASSET_MENTION`；
- Prompt里出现的每个@Mention必须能回查到本次Reference Runtime Binding；无法回查 = `UNBOUND_ASSET_MENTION`；
- 不能因为“文字已经描述了人物/场景”就删除@资产，文字描述和资产调用不是互相替代关系；
- 不能因为“UI里已经看到这张图”就默认省略Mention，除非当前Target Adapter明确允许；
- 若必须@但Native Token尚未建立，状态=`WITHHELD_PENDING_NATIVE_BINDING`，先补绑定，不允许输出一个看似完整但实际没有调用资产的Prompt。

## 3｜Reference不是正文替代品
Approved视觉Reference负责**稳定与校准**，不负责替代Stage 05的导演文字。Final Video Prompt不需要把资产规格表逐毫米全文翻译，但必须把当前Shot真正影响执行的静态事实自然写进正文：
- 当前可见人物身份、外观/服装中最容易漂且影响动作或识别的部分；
- 当前Scene空间、前中后景、入口/出口、关键Anchor与Blocking关系；
- 当前道具Owner / Holder / Hand / State与接触关系；
- 当前构图、景别、Camera Geometry与Focus；
- 对应Scene Color Authority下本Shot实际光源、冷暖、明暗、主体分离和Lighting变化；
- 运动/时间变化、微表情、表演、声音、物理反馈与Ending State。

**禁止的只是资产行政说明和无意义逐毫米复读，不是详细导演描述。** 若本文件与`video_prompt_template.md / prompt_compiler.md / video_prompt_detail_lint.py`对Stage 05详细度发生冲突，后者优先；本文件只能决定“绑定谁、@谁、Reference负责什么字段”。

## 4｜Control Reference Direct Bind
Color Card / Style Board / Storyboard是否整图直绑，读取`visual_reference_routing.md`的Capability/Risk路线。**不存在按类别一律禁止Token化的规则。**

## 5｜QC例外
WEB_QC_COPY_PROMPT可以按本批上传顺序使用动态`@图1...@图N`做证据映射；该编号是QC Evidence编号。Generation Prompt中的`@资产名`/真实Native Token属于生成资产调用，两者不得混用。

## 6｜Fail
- `REFERENCE_ADMIN_TEXT_LEAK`
- `MODEL_FACING_METADATA_LEAK`
- `NATIVE_TOKEN_OVERANNOTATION`
- `PSEUDO_NATIVE_REFERENCE_TOKEN`
- `REFERENCE_ROLE_SCOPE_VIOLATION`

## 2C｜Multimodal All-Round Reference Contract

`MULTIMODAL_ALL_ROUND_REFERENCE`只表示：**同一次视频生成可以让允许的不同模态Reference承担不同职责，并由Prompt明确指派。项目允许TEXT / IMAGE / AUDIO，禁止REFERENCE VIDEO。** 它不表示任意素材都可靠、不表示Primary Visual万能，也不表示完整资产库必须全部上传。

允许的典型Reference Role：
- Character / FMH Master → 人物身份、脸、发型、服装、体态；
- Environment Master / Visual Anchor → 空间、材质、固定结构、当前Camera方向；
- Prop / Weapon Canon → 关键结构、可见面、交互状态；
- Approved Storyboard Panel / Contact-Sheet-derived Panel → Blocking、构图、动作节点、时间关系；
- Shot Execution Frame → 当前镜头综合色、构图、站位和已烘焙视觉状态；
- Previous Ending Frame → Continuity Entry；
- Motion / Camera Dynamics → Storyboard、Action Key Pose、Camera Path Metadata与文字约束；**不得使用Reference Video**；
- Audio Reference → 声音、节奏、表演Timing（仅当前Provider支持时）。

任何Reference进入Video Job前仍必须经过`Reference Resolver → Minimum Sufficient Reference Set`。Provider实际支持多少张图片、多少段音频、具体格式与大小，必须读取当前Provider Profile；Skill不把单一平台的历史数量限制写成全局能力定义。参考视频数量固定为0。
