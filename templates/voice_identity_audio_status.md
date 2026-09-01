# Voice Identity & Audio Status（声音身份与对白音频状态）

> **用途：** 角色声音身份是长期资产，不应等到Stage 05临时决定。V4.5.2要求主要/反复角色在Episode Asset Freeze前解析Required Voice Identity；Stage 05只消费已锁Voice Identity或显式TEMP_SYNC例外。此规则只处理角色声音身份，不改变 `NO AUTO BGM`。


## 0｜Stage 03 Voice Asset Requirement（V4.5.2）

在Episode Asset Manifest中对本集有Dialogue/VO的主要/反复角色运行Voice Requirement：
- 已有Approved Voice Master → `REUSE / FINAL_VOICE`；
- 本项目要求建立正式固定声线且尚无 → `TO BUILD VOICE_IDENTITY_ASSET`，进入Stage 03资产队列；
- 当前只允许临时同步、正式声音确定在Stage 06 → 必须登记`TEMP_SYNC_AUDIO + Voice Replacement Required=YES`，不得把随机模型声音写回Canon。

Asset Freeze检查的是“声音身份有没有明确Authority/例外”，不是强制每个群众都建立Voice Master。

## 1｜三种Voice Mode

### `FINAL_VOICE`
只有项目已有明确批准的 `Approved Voice Master / Voice Reference` 时使用。

要求：
- 当前Dialogue/VO必须绑定该角色正式声音来源；
- 音色、性别表现、年龄感、口音/语言、说话力度保持稳定；
- Stage 06可继续清理混音，但不默认重配演员。

### `TEMP_SYNC_AUDIO`
当本段需要口型/表演同步，但角色**没有Approved Voice Master**时使用。

规则：
- Stage 05生成的对白只用于Timing / Lip Sync / Acting Reference；
- 不得把随机模型音色登记为角色正式声音；
- Workspace必须标记 `Voice Replacement Required = YES`；
- Stage 06统一替换/克隆/配音并重新混音。

这是“需要对白但暂无正式声纹”时的默认模式。

### `NO_DIALOGUE_AUDIO`
当本段没有对白、或决定完全后期配音时使用。

Stage 05不生成Dialogue/VO，只保留需要的Ambience / Foley / SFX / Diegetic Music。

## 2｜Voice Identity字段

如果存在Approved Voice Master，至少记录：
- Character ID；
- Voice Master ID / Version；
- language；
- age impression；
- gender presentation（仅声音表现）；
- timbre / texture；
- speaking pace tendency；
- emotional restraint / intensity；
- pronunciation / accent要求（已确认时）；
- status：APPROVED / DEPRECATED。

未确认的信息不编造。

## 3｜Stage 05 Prompt规则

在【声音 / Audio Generation Boundary】中增加：
- `Voice Mode = FINAL_VOICE / TEMP_SYNC_AUDIO / NO_DIALOGUE_AUDIO`；
- `Voice Source = Approved Voice Master ID / NONE`；
- `Voice Replacement Required = YES / NO`。

`TEMP_SYNC_AUDIO`时必须明确：
> Dialogue audio is temporary sync audio only. Do not treat the generated voice as the character's canonical voice identity. Final voice will be replaced in Stage 06.

## 4｜Stage 06交接

Stage 06优先检查：
- 哪些Segment是FINAL_VOICE；
- 哪些是TEMP_SYNC_AUDIO必须替换；
- 替换后口型/停顿是否仍同步；
- 同一角色跨Segment最终声音是否一致。

## 5｜与BGM规则关系

Voice Mode只决定Dialogue/VO状态。无论哪种Voice Mode，Stage 05仍然：
**BGM边界不在本文件重复定义；统一服从 `video_audio_generation_boundary.md`。**


## Current｜Voice Identity vs Prosody

本文件只锁**长期声音身份**；重要Dialogue/VO的当前台词执行必须建立`VOICE_DIRECTION_PLAN`并遵守`voice_direction_prosody_engine.md`。`VOICE_DIRECTION_PLAN.voice_identity_asset_id`只能指向这里已经Approved的Voice Identity。
- Voice Identity：谁在说、稳定音区/音色/年龄感/口音/基础pace；
- Voice Direction：这一句为何这样说，以及Performance Loudness、Pace Curve、Pause Map、Stress、Terminal Intonation怎样变化。

不得把“当前句低声、加速、句尾截断”写回长期Voice Master；也不得只靠Voice Master就认为这一句已经完成配音导演。

## V4.5.7｜Voice Asset进入统一Audio Manifest

Approved Voice Master / Voice Reference必须同时登记到`AUDIO_ASSET_MANIFEST`。需要在Video Job中直接参考声线时，使用`VOICE_AUTHORITY`绑定模式与对应Native `@音频资产`；未登记或Native Binding未Ready时不得伪造Mention。
