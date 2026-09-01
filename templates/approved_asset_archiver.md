# Approved Asset Archiver（已批准资产自动归档器）

> **用途：** 当图片/分镜/尾帧等生产结果已经 `QC PASSED + 用户明确批准 = APPROVED` 后，如果当前AI/运行环境具备真实文件写入能力，就自动命名、创建目录、复制文件并把实际路径写回Registry / Episode Workspace。若没有文件能力，则绝不假装保存成功。

> **V4.3确定性执行：** 有真实本地文件能力时优先调用`tools/archive_asset.py`完成Copy-first、Path Boundary、Size与SHA-256 Postcondition；本文件保留触发条件和语义边界。

> `AD-01 Signature Adornment Detail`按Stage 03 Character Appearance Asset归档，角色职责为`PERSONAL_ADORNMENT_AUTHORITY / DETAIL_AUTHORITY`，跟随角色Registry/Closet，不升级为Prop，除非其职责后来发生剧情因果升级。

## 1｜触发条件

Archiver只在以下条件全部满足后触发：

> `FUNCTIONAL_MINOR_HUMAN_ASSET`批准后使用状态`APPROVED SCOPED FIGURE`，只在登记Scene/Shot Group范围内有效；不升级成长期Character Canon。
> `SHOT_ASSEMBLY_ASSET`批准后使用状态`APPROVED ASSEMBLY`，归档时按Stage 03静态资产处理；它不转成Canon，也不转成Storyboard/Ending Frame。

1. 当前结果已经完成对应QC；
2. 用户已明确批准，状态属于当前资产类型的正式批准类：普通Canon/Storyboard等为`APPROVED`，Functional Minor Human为`APPROVED SCOPED FIGURE`，Production Support为`APPROVED SUPPORT`；Video Conditioning Frame为`APPROVED_VIDEO_CONDITIONING`，Shot Assembly为`APPROVED ASSEMBLY`；
3. Asset Intake已经识别它属于哪个Asset / Episode / Scene / Segment；
4. 已确定规范文件名；
5. 当前运行环境已经解析到可读取的 **Source Path（真实源文件路径）**，或已把聊天/附件中的文件实体 materialize / 挂载为真实本地文件；仅“看得到图片预览、文件卡片、聊天缩略图、文件名或UI引用”不算真实源文件。

**`QC PASSED / WAITING APPROVAL` 不能进入正式approved目录。**

## 2｜Capability Check（文件能力检查）

归档前自动判断当前AI是否真的具备：

- 解析并读取当前候选的真实 Source Path；
- 对 Source Path 执行文件存在检查与大小检查；
- 创建目录；
- 复制/写入文件；
- 对目标文件执行真实存在检查与大小检查；
- 对源文件和目标文件分别计算 SHA-256；
- 验证两个 SHA-256 完全一致；
- 验证最终目标路径位于 Active Project Root 内部。

**缺少以上任何一项，都不能进入 `ARCHIVED`。**

### A. 有文件写入能力

只有完成“真实文件提交协议”全部步骤后，才记录：

```text
Archive Status：ARCHIVED
Active Project Root：<当前项目根目录>
Source Path：<真实存在且可读取的本地源文件路径>
Archive Path：<当前项目根目录内部、真实存在的目标路径>
Archive Filename：<实际文件名>
Source Size：<真实字节数>
Target Size：<真实字节数>
Source SHA-256：<实际计算值>
Target SHA-256：<实际计算值>
SHA-256 Verification：PASS
Archived At：<当前时间，如环境可提供>
```

如果无法真实读取文件并计算这些值，**不得填写占位值，不得写PASS，不得写ARCHIVED**。

### B. 没有文件写入能力 / 文件本体不可访问

不得说“已经保存”。记录：

```text
Archive Status：ARCHIVE PENDING
Active Project Root：<若可确定则记录>
Target Folder：<当前项目根目录内部的建议目录>
Target Filename：<规范文件名>
Reason：当前环境无法解析真实Source Path、无法读取文件本体、无法写入、或无法完成后置验证
Source Path：UNRESOLVED / UNAVAILABLE
SHA-256 Verification：NOT RUN
```

**聊天UI里能看到图片 ≠ 文件系统里能读取图片。** 只有得到可读本地文件路径后才能补做归档。

然后把目标目录和文件名直接给用户即可。

## 2.1｜Physical Archive Commit Protocol（真实文件归档提交协议）

归档必须按以下顺序执行，任何一步失败都立即停止，并保持 `ARCHIVE PENDING`：

### Step 1｜Resolve Source（解析真实源文件）

必须取得真实可读的 `Source Path`。

允许：
- 用户当前项目里已经存在的本地图片/视频文件；
- 宿主环境明确提供的附件挂载路径；
- 已经 materialize / 下载到本地工作区、且文件系统可读取的文件。

不允许把以下内容当Source Path：
- 聊天消息里的图片预览；
- 缩略图；
- 文件卡片显示名；
- Markdown里的图片引用；
- 仅存在Registry里的旧路径字符串；
- AI自己猜出来的路径。

找不到真实Source Path → `APPROVED / ARCHIVE PENDING`，停止。

### Step 2｜Source Preflight（源文件前置检查）

真实执行：
1. `exists(Source Path) == true`；
2. `is_file(Source Path) == true`；
3. `size(Source Path) > 0`；
4. 文件可读取。

任一失败 → 不复制、不算Hash、不写ARCHIVED。

### Step 3｜Resolve Target（解析目标路径）

- 目标必须位于 Active Project Root 内；
- 先通过Auto Naming得到规范文件名；
- 同名冲突按版本规则处理，不覆盖旧APPROVED。

### Step 4｜Copy-first Commit（真实复制）

创建目标目录并执行真实文件复制。默认**原字节复制**，不得为了归档自动重新编码、重新导出、压缩或改尺寸。

### Step 5｜Filesystem Postcondition（文件系统后置条件）

复制后必须真实检查：
1. `exists(Target Path) == true`；
2. `is_file(Target Path) == true`；
3. `size(Target Path) > 0`；
4. `Source Size == Target Size`。

只创建Registry记录、Markdown记录、目标文件名字符串，**不算完成归档**。

### Step 6｜SHA-256 Verification（真实哈希校验）

必须分别读取真实源文件和真实目标文件的字节并计算：

```text
Source SHA-256 = sha256(Source Path bytes)
Target SHA-256 = sha256(Target Path bytes)
```

只有两者完全一致时：

```text
SHA-256 Verification：PASS
```

否则：

```text
Archive Status：ARCHIVE PENDING
SHA-256 Verification：FAILED
Reason：源文件与归档目标字节不一致
```

不得把文件名、路径字符串、UI图片ID、Registry文本做Hash后冒充“文件SHA-256”。

### Step 7｜Commit Metadata（最后回写元数据）

**只有Step 1–6全部通过后**，才能把Registry / Intake / Workspace从：

```text
APPROVED / ARCHIVE PENDING
```

更新为：

```text
APPROVED / ARCHIVED
```

并写入真实Source Path、Archive Path、文件大小、两份SHA-256与验证结果。

> **No File, No ARCHIVED（没有真实文件，就绝不能标记已归档）。**

## 3｜Copy-first（优先复制）

默认采用**复制**，不是移动：

- 保留原候选/上传文件；
- 把APPROVED版本复制到正式目录；
- 只有用户明确要求“移动/整理并删除原候选”时才执行Move。

避免因为自动归档导致原始候选丢失。

## 4｜Active Project Root（当前项目根目录）

### 4.1 路径优先级（强制）

归档器必须先确定 **Active Project Root（当前正在工作的项目文件夹）**，并按以下优先级解析：

1. **用户在当前会话明确指定的项目目录**；
2. **宿主环境当前打开的项目 / Workspace Root（工作区根目录）**；
3. 若宿主只提供当前工作目录，则使用当前正在执行项目任务的 **Current Working Directory（当前工作目录）**；
4. 只有以上都无法确定时，才进入 `ARCHIVE PENDING`，向用户报告建议目标路径；**不得自行跳到历史目录、其他项目目录或全局默认目录。**

### 4.2 Current Folder First（当前项目文件夹优先）

默认归档位置必须位于 **Active Project Root 内部**。

例如当前用户打开的是：

```text
<ACTIVE_PROJECT_ROOT>/
```

则正式资产只能默认保存到这个目录内部，例如：

```text
<ACTIVE_PROJECT_ROOT>/assets/characters/...
<ACTIVE_PROJECT_ROOT>/episodes/<EPISODE_ID>/...
```

**不得**因为历史Registry、旧Workspace、以前的Archive Path、Skill缓存目录或默认目录存在，就自动把新文件保存到别的文件夹。

### 4.3 禁止越界归档（Path Boundary）

除非用户在当前会话明确要求，否则：

- 不得把文件保存到 Active Project Root 的父目录；
- 不得保存到另一个项目文件夹；
- 不得保存到历史备份目录或非当前Project Root；
- 不得保存到全局 `Downloads` / `Documents` / 临时目录作为正式归档；
- 不得把 Skill 安装目录、缓存目录、Skill ZIP 解压目录当成生产资产目录；
- Registry 中历史 `Archive Path` 只能用于读取旧依赖，**不能反向决定本次新文件的归档根目录**。

如果计算出的目标路径不在 Active Project Root 内，必须停止真实写入，并记录：

```text
Archive Status：ARCHIVE PENDING
Reason：目标路径越出当前项目根目录，等待用户确认
Proposed Root：<当前Active Project Root>
Proposed Target：<当前项目内部建议路径>
```

### 4.4 无法确定当前项目根目录时

不要自行创建外部 `断弦之歌_Production/` 目录。

只能给出相对路径建议，例如：

```text
./assets/characters/<Character_ID>/approved/
```

并标记 `ARCHIVE PENDING`，直到宿主环境能确认当前项目根目录。

## 5｜默认文件夹结构

### Character / Environment / Prop / Visual Style / Color正式图片资产

以下全部为 **相对于 Active Project Root 的相对路径**：

```text
./
└── assets/
    ├── characters/
    │   └── <Character_ID>/
    │       └── approved/
    ├── environments/
    │   └── <Environment_ID>/
    │       └── approved/
    ├── props/
    │   └── <Prop_ID>/
    │       └── approved/
    ├── visual_style/
    │   ├── render/
    │   │   └── approved/
    │   └── cinematic_shot/
    │       └── approved/
    └── color/
        ├── global/
        │   └── approved/
        ├── scenes/
        │   └── <Scene_or_Location_ID>/approved/
        └── lighting/
            └── <Lighting_ID>/approved/
```

### Storyboard

```text
episodes/
└── <EPISODE_ID>/
    └── S04/
        └── SEG03/
            └── storyboard/
                └── approved/
```

### Ending Frame

```text
episodes/
└── <EPISODE_ID>/
    └── S04/
        └── SEG03/
            └── ending_frame/
                └── approved/
```

### Video（若未来同样调用Archiver）

```text
episodes/
└── <EPISODE_ID>/
    └── S04/
        └── SEG03/
            └── video/
                └── approved/
```

用户已有目录体系时，**优先映射到用户目录**，不要强制改成上面结构。

## 6｜Auto Naming联动

先调用 `Auto Naming（自动命名）`，再归档。

例如：

```text
CHR_CHARACTER_B_CURRENT_MASTER_v001.png
ENV_SCENE_A_MASTER_v003.png
PROP_KEY_A_OPEN_v001.png
STYLE_RENDER_EVIDENCE_v001.png
STYLE_CINEMATIC_SHOT_EVIDENCE_v001.png
COLOR_GLOBAL_DNA_CARD_v001.png
COLOR_SCENE_<SCENE_ID>_EXT_v001.png
SUP_EPXX_SHXX_COMPLEX_CONTACT_v001.png
ANCHOR_EPXX_SXX_SHXX_HD_v001.png
DSG_EPXX_SXX_SEGXX_SB_APPROVED_v002.png
DSG_EPXX_SXX_SEGXX_END_v001.png
```

不得用 `生成图(38).png`、`最终版真的最终.png` 作为正式归档名，除非用户明确要保留原名。

## 7｜Version Collision（同名/版本冲突）

如果目标目录已经存在同名文件：

- 不覆盖APPROVED旧文件；
- 优先按Registry版本规则生成下一版本号；
- 若只是重复归档同一文件，先比对当前记录，避免生成重复副本；
- 无法确认是否同一内容时，不静默覆盖，使用新版本名。

## 8｜Registry / Workspace回写

正式图片资产至少回写：

```text
Asset ID：CHR_CHARACTER_B_CURRENT
Version：v001
Status：APPROVED
Archive Status：ARCHIVED
Archive Filename：CHR_CHARACTER_B_CURRENT_MASTER_v001.png
Archive Path：.../assets/characters/CHR_CHARACTER_B_CURRENT/approved/CHR_CHARACTER_B_CURRENT_MASTER_v001.png
Identity Distinction Card Ref：CHARACTER_IDENTITY_<ID>_v___（主要/反复角色）
Face Identity Ref：...
Hair Identity Ref：...
Base Eye Identity Ref：...
Wardrobe Diversity / Fashion DNA Ref：...
```

主要/反复角色还应把`Identity Distinction Card`的关键字段写回Registry / Runtime Card；可以是Markdown Sidecar或结构化Registry字段，但**不能只存在一次Prompt里然后丢失**。

Storyboard / Ending Frame至少回写Episode Workspace：

```text
SEGXX Approved Storyboard Path：...
SEGXX Approved Ending Frame Path：...
```

如果当前环境无法解析真实Source Path、无法真实保存、或无法完成目标存在/大小/SHA-256验证，则Path不得写成假路径，改为 `ARCHIVE PENDING` + Target Folder / Target Filename。`ARCHIVED` 与 `SHA-256 PASS` 只能由真实文件系统检查结果产生。

## 9｜与Asset Intake的完整闭环

```text
用户上传/生成候选
→ Asset Intake识别任务
→ Candidate Triage（图片计划多候选时：Fast Triage → Primary/Backup）
→ Primary Deep QC
→ QC PASSED / WAITING APPROVAL
→ 用户明确批准
→ APPROVED
→ Auto Naming
→ Approved Asset Archiver
→ 解析真实Source Path
→ 源文件exists/is_file/size/readable检查
→ Copy-first真实复制
→ 目标文件exists/is_file/size检查
→ Source / Target SHA-256真实计算并比对
→ 全部PASS后才写 ARCHIVED + 实际路径
→ 下游Reference Resolver优先调用已归档APPROVED文件
```

## 10｜下游调用原则

如果已归档APPROVED版本存在真实路径：

- Reference Resolver优先引用正式归档文件；
- 不继续引用临时候选文件；
- Change Impact使用Asset ID + Version + Archive Path定位历史依赖；
- 归档只是文件管理，不改变人物/场景/道具的设计规则。

## 10.1｜Production Support Archive Boundary

Production Support Reference与Video Conditioning Frame可以归档，但状态必须保持：

`APPROVED SUPPORT`

不得因为进入`approved/`目录就升级为`APPROVED CANON`。

归档至少记录：
- Support / Conditioning Frame ID；
- Stage Owner（03 / 04）；
- Triggered Shot / Segment；
- Parent Authority IDs + Versions；
- Authority Fields；
- Canon Boundary；
- Approved Storyboard Version（Video Conditioning Frame必填）；
- Video Risk Reduced；
- Archive Filename / Path / SHA-256（只有真实文件系统验证通过后）。

Parent Authority或Approved Storyboard换版后，按`change_impact.md`判断该Support/Conditioning Frame是否`STALE`，不得继续无条件作为当前Reference。


## 10.2｜Shot Assembly Archive Boundary

`SHOT_ASSEMBLY_ASSET`批准并归档时状态保持：

`APPROVED ASSEMBLY`

不得因为进入`approved/`目录升级为`APPROVED CANON`或`APPROVED SUPPORT`。归档至少记录Assembly ID、Scene/Shot Group Scope、Parent Authority IDs + Versions、Scoped Cast（若有）、Assembly Authority Fields与Video Risk Reduced。Parent Authority或Scope变化后按`change_impact.md`判断`STALE / REBUILD ASSEMBLY`。

## 11｜禁止

- QC通过但用户没批准就存入`approved/`；
- 没有文件写入能力却声称“已保存”；
- 没有真实Source Path却声称“已归档”；
- 只修改Registry / Intake / Workspace的Markdown就标记ARCHIVED；
- 未检查目标文件真实存在且大小>0就标记ARCHIVED；
- 未对真实源文件和真实目标文件分别计算SHA-256就写`SHA-256 PASS`；
- 对路径字符串、文件名、UI引用或图片ID计算Hash后冒充文件Hash；
- 自动覆盖旧APPROVED版本；
- 因归档而修改图像内容、压缩画质或重新编码，除非用户明确要求；
- 默认删除原候选；
- 把Skill压缩包本身当成长期生产资产目录；
- 未经用户明确允许，把新APPROVED文件写到当前Active Project Root之外；
- 因历史Archive Path存在就把本次归档重定向到旧项目文件夹。


## Current｜Approved Salvage Clip Archive
- `SALVAGE_CANDIDATE`不是APPROVED资产，不进入普通Approved Archive；但其唯一Source Take必须标`PRESERVE SOURCE = TRUE`，不得因Whole-Take REVISE自动删除。
- 当用户/最终剪辑明确采用某Window后，可升级`APPROVED_SALVAGE_CLIP`。若环境具备剪辑/文件能力，按`Source Take + IN/OUT`导出Clip并Copy-first归档；若无导出能力，Registry仍保留Source Path/Take + IN/OUT，标`ARCHIVE PENDING`。
- 归档Salvage Clip必须记录Source Take、IN/OUT、Video/Audio Use、Editorial Function、Approval Source与Source Hash（可取得时）。
- 原始Source Take至少保留到Episode Master锁定；不得用裁出的片段覆盖唯一源文件。
- Salvage Clip只有在其确为最终Segment结尾时才进入Ending Frame候选流程。
