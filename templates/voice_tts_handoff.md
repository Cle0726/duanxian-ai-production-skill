# Voice TTS / Dubbing Handoff｜V4.5.7

> **用途：** 把Stage 02/05已经批准的Voice Direction，在Picture Lock之后变成Stage 06可执行的正式配音/TTS交接。它只重新锁真实剪辑时间，不重新发明角色声线、情绪原因或句尾意图。

## 1｜唯一上游

`VOICE_DIRECTION_PLAN → VOICE_PROMPT_HANDOFF → Approved Video/Picture Lock → VOICE_TTS_HANDOFF`

Stage 06不得绕过Voice Direction Plan，只凭“悲伤、愤怒、低沉”等标签重新导演。

## 2｜允许改变的内容

Picture Lock后允许调整：
- Line Start / End；
- Pause Duration；
- Phrase Timing；
- TTS Adapter表达方式（Direct / SSML when supported / Director Note Only）。

## 3｜默认不可改变的表演意图

除非回上游重批Voice Direction，否则必须继承：
- Voice Identity Asset；
- Performance Loudness；
- Pace Curve方向；
- Required Pause Type与原因；
- Required Stress / De-emphasis；
- Pitch / Energy Contour；
- Terminal Intonation；
- Objective / Tactic / Subtext对应的Landing。

## 4｜Picture Lock硬门

每条需要正式配音的Line必须有：
- `line_id`；
- `start_sec < end_sec`；
- 对应Voice Identity；
- 与Plan相同的核心Prosody意图；
- 若有Overlap/Interrupt，必须由源Plan显式授权。

## 5｜禁止

- 不因TTS音色库限制而偷偷换Voice Identity；
- 不因“更有情绪”擅自把FALL改RISE、SOFT改SHOUT；
- 不把Mix Gain/LUFS当Performance Loudness；
- 不把所有Pause机械换成相同毫秒；
- 不让临时Temp Audio成为新的表演Authority。
