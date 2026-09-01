# Visual Reference Routing & Literalization Risk Manager｜Current Authority

> **最高原则：** `REFERENCE ROUTING ≠ PROMPT COMPRESSION`。综合色卡、Style Board、Storyboard/宫格首先是视觉控制信号，不应被无证据地再生成成另一张控制图；但Reference路由模块**不得据此缩短Stage 05导演正文**。它只决定某张视觉资产应Direct Bind、Split、Crop、Fallback还是不绑定；最终Video文字详细度由`video_prompt_template.md + prompt_compiler.md`唯一决定。
>
> **Current Runtime-Clean Rule：** `UNKNOWN ≠ FAIL ≠ FALLBACK TRIGGER`。Scene-bound Image / Shot Execution仍以Approved Scene Color视觉Authority优先Direct Bind；但Final Video采用**Minimum Sufficient Reference Set**：只要Primary Visual已经继承同一Scene Color Authority且没有综合色风险Trigger，默认`LINEAGE_ONLY`，不机械重复占用色卡Direct Reference槽。不得因为“未知/谨慎/保险”预生成`SCENE_COLOR_APPLIED_REFERENCE`，也不得因为有空槽就自动上传色卡。


## V4.5.7｜All-Round Multimodal Default

《断弦之歌》默认视频Reference能力类为`MULTIMODAL_ALL_ROUND_REFERENCE`：底层模型允许多模态Reference Role分工；本项目有效输入只允许文字、图片、音频，**任何参考视频均禁止**。这里的默认是**项目能力前提**，不是对某个宿主的具体素材数量、版式Literalization可靠性或原生Token语法作保证。

因此本文件仍然保留Capability Evidence：例如Whole Storyboard是否适合Direct、某个平台是否支持独立Audio Reference、实际可输入多少素材，都由当前Provider Profile/实测证据裁决。全能参考与`MINIMUM_SUFFICIENT_REFERENCE_SET`同时成立。

## V4.4｜Primary Visual vs Auxiliary Visual

本文件继续允许Color Card、Style Board、Design Board、Whole Storyboard按Capability直接进入Video。**Direct Bind不是Primary Visual资格。**

Stage 05 Reference Pack先分两层：
1. `PRIMARY_VISUAL_CONDITIONING`：每个Video Unit至少一个，必须是`visual_asset_usage_authority.md`允许且已Approved/Promoted的Shot-specific资产；
2. `AUXILIARY_VISUAL_AUTHORITIES`：Identity / Environment / Design / Color / Style / Storyboard / Continuity等字段级Reference。

Whole Board即使`DIRECT_STORYBOARD_BOARD=VERIFIED_PASS`，也只证明它能作为Director/Temporal视觉控制，不证明它可以取代Primary First/Execution Frame。Design Board、Color Board同理。

## 1｜Field Ownership
每张Reference先登记允许控制的字段：
- `IDENTITY / HUMAN APPEARANCE`
- `ENVIRONMENT / GEOMETRY / MATERIAL`
- `COLOR / VALUE / LIGHT RELATIONSHIP`
- `RENDER STYLE`
- `COMPOSITION / BLOCKING / ACTION STATE`
- `CONTINUITY / FIRST-LAST FRAME`

Direct Bind只授权对应字段，不等于复制Reference全部内容。

## 2｜Capability Evidence
```text
MODEL REFERENCE CAPABILITY PROFILE
IMAGE_REFERENCE_INPUT: VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN
MULTI_IMAGE_REFERENCE: VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN
ROLE_SEPARATION: VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN
DIRECT_COLOR_CARD: VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN
DIRECT_STYLE_BOARD: VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN
DIRECT_STORYBOARD_BOARD: VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN
PANEL_MULTI_REFERENCE: VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN
KNOWN_LITERALIZATION_HISTORY:
- COLOR: NONE / OBSERVED
- STYLE: NONE / OBSERVED
- STORYBOARD_LAYOUT: NONE / OBSERVED
```

不得虚构能力；但也不得把UNKNOWN解释成禁止。

## 3｜Color Card Default Route
### 3.1 Image / Shot Execution：Direct Visual First
Scene-bound Image与Shot Execution属于综合色**烘焙阶段**。当前Scene Card已Approved、平台支持图片输入且无已知Direct Fail时，优先`DIRECT_BIND`；这一步把综合色真正投射进高质量Primary Visual。

### 3.2 Final Video：Lineage First, Direct Only When Needed
Final Video先确认：
- `scene_color_authority_id`存在且Approved；
- Primary Shot Execution / First Frame继承同一`scene_color_authority_id`；
- 当前综合色在Primary Visual中已经可见且没有明显漂移。

满足时默认：
`scene_color_reference_mode = LINEAGE_ONLY`，**Scene Color Card不进入Direct Reference Pack，也不占@槽位**。Final Prompt仍从Scene Color Authority写出必要的光色执行事实。

只有以下Trigger之一成立时才升级`DIRECT_REFERENCE / DIRECT_COLOR_REFERENCE`：
- `COLOR_DRIFT_OBSERVED`：同模型/同Scene已有综合色漂移；
- `COLOR_NARRATIVE_CRITICAL`：颜色本身承担剧情识别；
- `MULTISHOT_COLOR_DRIFT_RISK`：同一次Multi-shot换角度时综合色已知不稳定；
- `PRIMARY_VISUAL_COLOR_UNRELIABLE`：当前Primary Visual综合色未充分锁定；
- `PROVIDER_DIRECT_COLOR_REQUIRED`：目标Provider实测需要独立综合色参考；
- `USER_REQUIRED`。

若综合色仍需强化但Direct视觉输入不合适、Provider不支持或Reference Slot Pressure明显，可选择`TEXT_CONTROL / TEXT_COLOR_CONTROL`。

**槽位存在不构成Direct Trigger。** 若当前需要Prop Reverse / Character Identity / Environment Anchor / Previous Ending Frame，而这些字段比综合色更独占，优先把槽位给它们。

### 3.3 Applied Reference只允许证据触发
`SCENE_COLOR_APPLIED_REFERENCE / COLOR_GRADE_ANCHOR`不是普通Stage 03资产，也不是“为了以后Video保险”而提前生产的资产。

只有存在以下**可核对的触发证据**之一才允许生成：
- `DIRECT_COLOR_CARD = VERIFIED_FAIL`；
- `KNOWN_LITERALIZATION_HISTORY.COLOR = OBSERVED`；
- `ROLE_SEPARATION = VERIFIED_FAIL`，并且现有Color Reference无法通过无生成式Color-Only Crop / Dedicated Channel安全隔离所需综合色字段；
- 已证明Reference槽位不足，并且合并环境+综合色是当前最小充分方案；
- 用户明确要求Applied/Color Grade Anchor工作流。

若只是`ROLE_SEPARATION = VERIFIED_FAIL`但可以用已有Color-Only Crop或Dedicated Color Channel解决，**优先非生成式隔离，不生成Applied Reference**。

必须记录：
```text
APPLIED_REFERENCE_TRIGGER
Reason Code: DIRECT_FAIL / LITERALIZATION_OBSERVED / ROLE_SEPARATION_FAIL_NO_SAFE_CROP / SLOT_LIMIT_PROVEN / USER_REQUIRED
Evidence: <真实证据>
Status: VALID / INVALID
```

没有这个Trigger：`PREEMPTIVE_APPLIED_REFERENCE = HARD FAIL`。

## 4｜Style Board
Approved、干净且与当前任务相关的Style Reference，在平台可接收图片、`DIRECT_STYLE_BOARD != VERIFIED_FAIL`且无已观察Sample Bleed / Layout Literalization时优先Direct Bind。若`ROLE_SEPARATION = VERIFIED_FAIL`但Clean Crop / Dedicated Style Channel可完整保留Render Style字段，优先非生成式隔离；只有已观察Bleed/Literalization、已证明槽位冲突、用户明确要求，或`ROLE_SEPARATION=VERIFIED_FAIL`且不存在安全非生成式隔离路线时，才使用生成式Applied Reference。UNKNOWN不自动Fallback。

## 5｜Storyboard / 4格 / 6格 / 9格
Storyboard是正式视觉控制，不因宫格身份退成纯文字。路由按版式风险与Capability决定：
- `DIRECT_STORYBOARD_BOARD = VERIFIED_PASS`且整板关系有控制价值 → Whole Board Direct；
- `DIRECT_STORYBOARD_BOARD = UNKNOWN`、平台可接收普通图片、无已知Storyboard Layout Literalization，且`Layout Risk = LOW / MEDIUM` → 允许先Whole Board Direct + 最短Role Lock；UNKNOWN本身不是禁用理由；
- `Layout Risk = HIGH`且Whole Board能力仍UNKNOWN → 优先`PANEL_SPLIT / KEY_PANEL_SELECTION / FIRST_LAST_FRAME`，继续保留视觉控制，不降TEXT；
- 已验证Whole Board失败或已真实发生宫格/边框直译 → Clean Panel / Execution Anchor；
- 槽位有限 → 选Information Gain最高的关键Panel/首尾帧。

Fallback只升级失败的版式路线，不否定Storyboard本身的视觉Authority。

## 6｜Routing Manifest
```text
REFERENCE ROUTING MANIFEST
Reference Class: COLOR / STYLE / STORYBOARD / IDENTITY / ENVIRONMENT
Authorized Fields: ...
Capability Evidence: VERIFIED_PASS / VERIFIED_FAIL / UNKNOWN
Literalization History: NONE / OBSERVED
Chosen Route: DIRECT_BIND / DEDICATED_CHANNEL / PANEL_SPLIT / KEY_PANEL_SELECTION / CLEAN_CROP / APPLIED_REFERENCE / TEXT_FALLBACK
Applied Reference Trigger: <none or explicit trigger>
Role Lock: <最短一句>
Status: PASS / REROUTE_REQUIRED
```

## 7｜Escalation
Image / Shot Execution：`DIRECT_BIND → short Role Lock → PANEL/CROP → APPLIED/CLEAN REFERENCE`。Final Video Color：`LINEAGE_ONLY → TEXT_CONTROL or DIRECT_REFERENCE（按Trigger） → Crop/Dedicated/Applied（仅失败证据触发）`。

只有`VERIFIED_FAIL`、已观察Leak/Literalization、已证明槽位冲突、明确综合色风险或用户要求等可核对依据才升级Final Video综合色Direct输入；`ROLE_SEPARATION=VERIFIED_FAIL`优先无生成式Crop/Dedicated Channel。UNKNOWN/谨慎/保险不能触发Applied，也不能成为“色卡有空位就上传”的理由。

## 8｜QC
QC看实际成片是否出现色块、格线、无关样例人物或Storyboard布局。没有实际Leak就不能因为Reference类别判失败。


## Current｜Mandatory Storyboard Routing
`APPROVED MANDATORY SHOT STORYBOARD`先作为Stage 05视觉控制候选。`CLEAN_STRUCTURAL_STORYBOARD`只声明Shot/Composition/Blocking/Temporal/Cut职责，不承担Render Style/Color/Identity；按Capability选择Whole Board / Panel / Key Panel / Clean Panel。若Whole Board造成版式或白描风格直译，先改变Board/Panel路由并保留独占Shot字段，不能因此撤销Mandatory Storyboard Gate或退回“无分镜直出Video”。

## V4.5.7｜Scene Color Authority Routing

当前项目进入新Scene/Look Domain时先由`scene_color_card_auto_derivation.md`建立对应Scene Card。此后：
- Scene-bound图片：Scene Card = mandatory `COLOR_AUTHORITY`，Direct Visual First；
- Shot Execution Frame：Scene Card继续Direct Bind，把综合色烘焙进Primary Visual；
- Video：Scene Card仍是mandatory **Authority/Lineage**，但Direct Reference默认为`LINEAGE_ONLY`；只有明确Trigger才升级`DIRECT_REFERENCE`；
- Named Mention平台：图片/Shot Execution的Direct Color必须真实`@对应Scene Card`；Video仅在Direct模式出现该@。

Global Base Card是Scene Card的Parent，不在Scene Card已生效后与其平权重复绑定。Applied Reference仍只在已证明需要时生成。
