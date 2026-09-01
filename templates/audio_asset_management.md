# Audio Asset Management｜V4.5.7

> **Owner：AUDIO_ASSET_MANIFEST**。目标是让可复用音频像人物/场景资产一样被登记、复用、版本化，并在需要时稳定`@`；不得临时从文件夹抓音频作为Reference。

## 1｜项目硬规则

- `REFERENCE_VIDEO_POLICY = FORBIDDEN_QUOTA_COST`：任何参考视频不得进入视频生成Job。
- `AUDIO_REFERENCE_POLICY = AUDIO_ASSET_MANIFEST_ONLY`：要作为视频生成参考的音频，必须先登记到`state/audio_asset_manifest.schema.yaml`。
- 音频资产库可以很大；单个Video Job只绑定当前镜头真正需要的最小充分音频集合。
- `@音频资产`只负责其声明的Audio Role，不自动接管人物视觉、场景空间或Storyboard Blocking。

## 2｜Audio Type

- `VOICE_IDENTITY`：角色长期声音身份；绑定`subject_entity_id`。
- `DIALOGUE_TAKE`：已批准对白录音。
- `TEMP_SYNC_DIALOGUE`：只用于口型/Timing，不能回写Voice Canon。
- `SFX / FOLEY / AMBIENCE`：效果、拟音、环境声。
- `MUSIC / DIEGETIC_MUSIC`：配乐或画内音乐。
- `RHYTHM_REFERENCE`：节奏/Timing参考。
- `PERFORMANCE_AUDIO_REFERENCE`：声音表演、呼吸、节奏等参考，不包含Reference Video。

## 3｜稳定@引用

每条可Direct Reference的音频至少记录：
`asset_id → asset_display_name → native_token → audio_type → authority_role → scope → version → fingerprint → binding_status`。

Named-Asset Host示例：
`@艾琳声线母带`、`@剧院环境声_SC03`、`@脚步SFX_木地板`。

只有`status=APPROVED + reference_policy=VIDEO_REFERENCE_ALLOWED + direct_reference_eligible=true + binding_status=READY`的音频才能进入Video Job。

## 4｜Scope与复用

优先复用稳定Audio Asset，不按Shot重复建同一个声音：
- 角色声线：CHARACTER / GLOBAL；
- 环境声：SCENE / LOCATION复用；
- SFX：GLOBAL或Scene Family；
- 对白Take：SHOT / SEQUENCE；
- 音乐：SEQUENCE / EPISODE。

`reuse_key`重复且同时Active时必须报错，避免同一个声音出现多个冲突Authority。

## 5｜Stage 05 Reference Resolver

允许的Audio Reference Role：
`VOICE_IDENTITY / DIALOGUE_CONTENT / TIMING / RHYTHM / AMBIENCE / SFX / MUSIC / PERFORMANCE`。

Resolver只从`AUDIO_ASSET_MANIFEST`挑选；若音频未登记、未批准、Native Binding未Ready，则不得生成伪`@`。

## 6｜Stage 06

Stage 06继续消费同一Audio Manifest进行对白替换、环境声、音乐、SFX与混音；因此Stage 05使用过的音频不会变成不可追踪的临时附件。


## 7｜Binding Closure

- Video Job中的每个`required_bindings[].asset_id`必须真实存在于`ASSET_REGISTRY`；未知Asset不得作为Reference。
- Audio Role只能绑定`media_kind=AUDIO`资产；图片/数据不得伪装成Voice/Music/SFX Reference。
- 音频进入Video Job时，Job自身必须携带与Manifest/Registry一致的Native `@Token`，不能只靠Manifest里“理论上有Token”。
- `scope`必须有对应Owner字段：CHARACTER→subject_entity_id，EPISODE→episode_id，SEQUENCE→sequence_id，SCENE→scene_id，SHOT→shot_id。
- Stage 06继续读取同一`AUDIO_ASSET_MANIFEST + ASSET_REGISTRY`，保证后期使用与Stage 05引用的是同一资产身份。
