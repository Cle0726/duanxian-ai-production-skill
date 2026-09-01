# Video Audio Generation Boundary（AI视频声音生成边界）

> **用途：** 本文件是 Stage 05 声音边界的唯一权威来源。它负责“规则是什么”；`video_prompt_template.md` 不再复制完整禁令，只由Prompt Compiler在最终模型Prompt中注入一次短版锁。

## 1｜总原则

**BGM AUTO-GENERATION = FORBIDDEN（禁止自动生成背景配乐）。**

Stage 05只负责生成画面同步真正需要的声音；正式BGM统一留给Stage 06后期。

如果剧情没有明确的画内/剧情内音乐：**`MUSIC = NONE`**。

## 2｜Stage 05允许生成的声音

仅允许以下四类，并且都遵守“必要才写”：

1. `Dialogue / VO`｜对白 / 旁白
   - 只在本段确实需要口型、表演或同步时生成；
   - 声音身份状态由 `voice_identity_audio_status.md` 管理。

2. `Ambience`｜环境声
   - 雨、风、室内空间声、远处车辆等；
   - 只保留对空间感和连续性有帮助的声音。

3. `Foley / SFX`｜拟音 / 音效
   - 脚步、衣料、门、武器碰撞、道具接触、机械运动、攻击触发等；
   - 必须与可见动作、材质和重量对应。

4. `Diegetic / Source Music`｜剧情内音乐 / 画内音乐
   - 只有音乐真实存在于剧情空间、角色理论上能听见时允许；
   - 如角色弹琴、舞台演奏、收音机/唱机、剧情明确的现场歌唱；
   - 不得借“剧情内音乐”名义生成电影配乐。

## 3｜Stage 06职责

Stage 06统一负责：
- 正式BGM选择/制作；
- Music Cue Map；
- Cue In / Build / Duck / Hit / Drop / Cue Out；
- Scene之间音乐连续性；
- Dialogue / Ambience / Foley / SFX / BGM最终混音。

## 4｜Compiled Audio Execution Clause（最终Prompt只注入一次）

Prompt Compiler在需要声音边界时只保留**一个直接执行句**，不输出`Audio Boundary / Stage 05 / Stage 06 / MUSIC = NONE`等内部管理标签：

```text
不要生成背景配乐。只生成本镜头明确需要并与画面同步的对白/旁白、环境声、拟音/音效，以及剧情空间内真实存在的音乐；没有明确的剧情内音乐时保持无配乐。
```

不得再追加第二份英文长列表、第二段“禁止战斗/悬疑/变身音乐”或同义BGM禁令。

## 5｜QC Fail条件

以下任一发生即判 `AUTO-BGM VIOLATION`：
- 需要声音边界时，FINAL VIDEO PROMPT缺少唯一的直接Audio Execution Clause；
- 视频模型自行添加非剧情内音乐；
- 将Music Identity / 战斗节奏 / 变身节奏误解成自动配乐要求；
- 用“氛围音乐”替代Ambience。

如果随机BGM可以在后期干净移除且不伤害对白/环境声，可进入Trim/Post修；若已与对白/环境严重混合无法干净分离，则按声音生成失败处理。


## Current｜Performance Loudness ≠ Mix Loudness

Stage 05可以导演角色是HUSHED / SOFT / NEUTRAL / FIRM / RAISED / SHOUT，但这描述演员表演，不等于最终Gain/LUFS。最终对白在成片里的响度属于Stage 06；不得为了达到混音响度目标把耳语导演成喊话，也不得用后期音量数值代替Prosody。

## Current｜Typed Human-Audio State
Stage 05禁止用一个泛化“无人声 / no human sound”覆盖所有人类来源声音。先在`VIDEO_EXECUTION_STATE.AUDIO_STATE`分别决定：`DIALOGUE / SCREAM / SHOUT / WORD_FORMING_VOCALIZATION / NONVERBAL_BREATH / GASP / FOLEY / AMBIENCE / BGM`。

例如剧情要求“没有惊叫，只有喘气”时，合法状态是`SCREAM=OFF, DIALOGUE=OFF, NONVERBAL_BREATH=ON`；不得再输出`ALL_HUMAN_SOUND=OFF`。父子类别冲突由`prompt_constraint_solver.md`判`AUDIO_ON_OFF_CONFLICT`。

## V4.5.7｜Managed Audio Reference

如果Stage 05需要把既有声音作为生成Reference，必须从`AUDIO_ASSET_MANIFEST`解析Approved Audio Asset并使用真实Native `@音频资产`。禁止临时文件直绑。动作/运镜不得使用Reference Video；只允许Storyboard / Key Pose / Camera Path Metadata / Ending Frame静帧 / 文字控制。
