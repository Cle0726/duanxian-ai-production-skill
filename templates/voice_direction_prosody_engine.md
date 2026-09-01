# Voice Direction & Prosody Engine（配音导演与语流韵律引擎）｜Current Authority

> **用途：** 把Actor Performance里的Objective / Tactic / Subtext进一步翻译成可执行的声音表演。它不重新发明角色声线，也不负责最终混音；它回答的是：**同一个角色，这一句在此刻该用怎样的音量、语速、停顿、重音、音高走势与句尾语调说出来。**

## 1｜Identity ≠ Performance

声音分两层：

### Stable Voice Identity｜长期声音身份
由`voice_identity_audio_status.md`负责：
- Voice Master / Character ID；
- 年龄感；
- 基础音区 / pitch register；
- 音色 / texture；
- 共鸣倾向；
- 口音 / 发音；
- 基础语速倾向；
- 基础克制/外放程度。

### Line / Beat Voice Direction｜当前台词表演
由本Engine负责：
- Performance Loudness；
- Pace / Pace Curve；
- Thought Phrase / Breath Group；
- Pause Map；
- Stress / De-emphasis Map；
- Pitch / Energy Contour；
- Sentence-final Intonation；
- Voice Texture Deviation；
- Interrupt / Overlap / Listening Response；
- Landing / Carryover。

**禁止：** 因为角色此刻愤怒，就把长期声线换成另一种Voice Identity。

## 2｜固定推导顺序

`Voice Identity → Objective / Tactic / Subtext → Thought Intention → Speech Phrase → Breath Group → Pace Curve → Pause Map → Stress Map → Pitch / Energy Contour → Terminal Intonation → Texture Adjustment → Landing`

不能先写“低沉沙哑、慢速、停顿0.5秒”再硬找情绪理由。

## 3｜Performance Loudness（表演音量）

必须区分：
- `PERFORMANCE_LOUDNESS`：演员此刻说得轻/正常/坚定/提高；
- `MIX_LOUDNESS`：后期把对白在成片里放多响。

前者属于表演，后者属于Stage 06。**耳语不能因为后期响度被拉高，就被误导演成“大声说”。**

推荐内部状态：
- `HUSHED`｜压低到只让近距离对象听见；
- `SOFT`｜轻声；
- `NEUTRAL`｜自然会话；
- `FIRM`｜力度明显但不喊；
- `RAISED`｜提高音量；
- `SHOUT / CALL`｜确有剧情理由的呼喊。

若目标TTS支持数值Gain / dB，可在Target Adapter层映射；未知平台不得伪造精确dB。

## 4｜Pace / Pace Curve（语速与速度曲线）

不要只写“慢/快”。至少判断：
- `Baseline Pace`：角色平时倾向；
- `Line Entry Pace`：开口时比Baseline快/慢多少；
- `Mid-line Shift`：关键词/对方反应后是否加速或减速；
- `Terminal Pace`：句尾是否收短、拖住或突然截断。

可用：`VERY_SLOW / SLOW / BASELINE / QUICK / FAST`，或目标平台支持时映射相对Rate。数值只能由实际TTS平台能力决定，不建立跨平台固定倍率神话。

## 5｜Thought Phrase / Breath Group（思想短语与呼吸组）

台词先按**人物当前思想和意图**分组，而不是按标点机械分组。

每个Speech Phrase至少回答：
- 这组词在完成什么行动？
- 主要信息落在哪个词？
- 是否需要真正换气？
- 下一组词是继续同一思想，还是发生了Meaning Shift？

普通短句不机械插入吸气。真正的Breath Group变化必须来自句长、生理负担、压抑、哭笑、受击或策略变化。

## 6｜Pause Map（停顿节点图）

每个有意义停顿标类型，不把沉默当高级感装饰：
- `PRE_LINE_PROCESSING`｜开口前理解/选择；
- `THOUGHT_PAUSE`｜同一句内部思想转向；
- `HESITATION`｜犹豫/回避；
- `LISTENING_PAUSE`｜等待对方反应；
- `IMPACT_PROCESSING`｜被信息击中后的处理延迟；
- `BREATH_PAUSE`｜真实换气；
- `INTERRUPTED`｜被打断；
- `POST_LINE_HOLD`｜说完后有意留白。

需要Lip Sync / precise TTS时可以给具体Duration；若当前平台未知，只给`MICRO / SHORT / MEDIUM / LONG`与剧情理由，不能编造毫秒。

## 7｜Stress / De-emphasis（重音与弱读）

每个关键Speech Phrase优先标：
- `PRIMARY_STRESS`：真正改变意义的词；
- `SECONDARY_STRESS`：次要强调；
- `DE_EMPHASIS`：故意轻过去、回避或不愿承认的词。

**不是所有关键词都加重。** 有时潜台词恰恰来自某个本应重要的词被故意说轻。

## 8｜Pitch / Energy Contour（音高与能量走势）

关注整条语句走势，不只贴“低沉/高亢”标签：
- `LEVEL`｜控制住，不明显起伏；
- `RISING_PRESSURE`｜能量逐步上升；
- `FALLING_ENERGY`｜逐渐失去力度；
- `SPIKE_THEN_CONTROL`｜瞬间泄漏后压回；
- `SUSPENDED`｜保持未解决张力；
- `BREAK / CRACK`｜仅剧情允许时短暂破音/失稳。

Pitch变化必须保持角色Voice Identity，不允许随机换声线。

## 9｜Sentence-final Intonation（句尾语调）

Actor Engine的`OPEN / TIGHT / CUT / OFFER`必须进一步翻译为声音可执行的Terminal Contour：
- `FALL`｜明确落下、结束；
- `RISE`｜真正提问/确认；
- `FALL_RISE`｜保留、含蓄、话没说完；
- `LEVEL`｜悬着，不给情绪落点；
- `CLIPPED`｜突然收断；
- `BREATH_RELEASED`｜力度退去，以气息结束；
- `SUSPENDED`｜故意不给完整终止感。

句号不等于FALL；问号也不等于机械RISE。服从Tactic / Subtext。

## 10｜Texture Adjustment（临时声线质感偏移）

只允许在稳定Voice Identity内做小范围状态变化：
- breathiness ↑ / ↓；
- articulation变清晰/含混；
- consonant attack变硬/软；
- resonance暂时收窄/打开；
- dryness / strain仅在生理或剧情支持时出现。

禁止为了“情绪更强”给每句加沙哑、气声、哭腔。

## 11｜Listening / Interruption / Overlap

多人对白需要声音层面的Active Listening：
- 回答可以抢入、延迟、覆盖前一句尾巴；
- 被打断必须定义断在哪个Thought Phrase；
- Overlap只在关系/权力/紧迫性支持时出现；
- 不把所有对白做成轮流念稿。

## 12｜Voice Direction Card

对白重要Scene/Beat内部至少建立：

```text
VOICE DIRECTION CARD
Character：
Voice Mode / Voice Source：
Objective / Tactic / Subtext：
Baseline Voice Identity：
Performance Loudness：
Pace Curve：
Speech Phrase / Breath Group：
Pause Map：
Stress / De-emphasis：
Pitch / Energy Contour：
Sentence-final Intonation：
Texture Adjustment：
Overlap / Interrupt：
Landing / Carryover：
```

普通一句话不要求填满所有字段，只保留真正改变表演意义的项目。


## 12.5｜Structured Voice Direction Authority（V4.5.7硬闭环）

重要Dialogue/VO不再只停留在Markdown Card。生产态必须建立`VOICE_DIRECTION_PLAN`（`state/voice_direction_plan.schema.yaml`）：

`Trigger / Meaning Appraisal → Objective → Tactic → Subtext → Affect Result → Performance Loudness → Pace Curve → Pause / Stress → Pitch/Energy → Terminal Intonation → Body-Voice Coupling`。

其中：
- 情绪标签只是结果描述，不能替代`trigger_event / meaning_appraisal / objective / tactic / subtext`；
- `IMPORTANT / CRITICAL`台词至少必须有完整Pace Curve、Terminal Intonation，并额外存在Pause / Stress /非LEVEL Contour / Texture / Interaction中的一个真实执行维度；
- `voice_identity_asset_id`只引用Approved Voice Identity，不允许Prosody临时换声线；
- 白描/视频表演中的可见行为必须通过`body_voice_coupling.visual_behavior_anchor`与同一Trigger相连。

Stage 05先运行`tools/voice_direction_prompt_compiler.py`生成`VOICE_PROMPT_HANDOFF`，再由`validators/voice_prompt_handoff_lint.py`确认台词、说话者与Prosody自然语言锚点真实进入Final Video Prompt。 没有Dialogue的Video Unit也必须生成`status=NOT_REQUIRED`的空Handoff，避免Gate靠“文件缺失”猜是否适用。

Stage 06在Picture Lock后由`tools/voice_tts_handoff_builder.py`生成`VOICE_TTS_HANDOFF`，并用`validators/voice_tts_handoff_lint.py`确认只调整真实时间，不改写原表演意图。 没有正式配音需求的Episode/Unit同样显式输出`NOT_REQUIRED`，而不是省略Artifact。

## 13｜Stage 05编译

FINAL VIDEO PROMPT / TTS Handoff只输出当前模型真正能执行的最小声音指令：
- 角色声线身份；
- 相对音量；
- 语速/速度变化；
- 必要停顿节点；
- 重音/弱读；
- 句尾走势；
- 必要的气声/失稳；
- 与画面Trigger的时间关系。

如果视频模型的声音控制很弱，不把二十个Prosody字段全部塞进去；保留导演Card，并在Stage 06正式TTS/配音时执行。

## 14｜Stage 06正式配音 / TTS

Stage 06读取`VOICE_DIRECTION_PLAN + VOICE_TTS_HANDOFF`与实际Picture Lock：
- 根据真实剪辑重新锁Pause Duration与Phrase Timing；
- TEMP_SYNC_AUDIO替换时继承原表演意图，不机械复刻随机临时声线；
- TTS支持SSML / prosody标签时再由Target Adapter映射；
- 不支持的控制项保留为配音导演说明。

最终混音响度与演员表演音量分开处理。

## 15｜Hard Fail

- `VOICE_PROSODY_UNDERDIRECTED`：重要对白只有情绪词，没有Pace/Pause/Stress/Terminal等可执行声音方向；
- `PAUSE_DECORATION_FAIL`：停顿没有理解/选择/倾听/换气/冲击等原因；
- `TERMINAL_INTONATION_FAIL`：句尾语调与Tactic/Subtext冲突；
- `VOICE_IDENTITY_DRIFT`：Prosody指令改变了角色长期声线身份；
- `PERFORMANCE_MIX_LOUDNESS_CONFLATION`：把表演轻重与后期Gain/LUFS混为一谈；
- `DIALOGUE_TURN_TAKING_MECHANICAL`：多人对白机械轮流念稿，无Listening/Interrupt/Overlap逻辑。

未解决重要对白Hard Fail → 不得交付正式Voice/TTS执行单。


## V4.5.7｜Sequence-level VO / Video Unit Scope

对白通常绑定`shot_id`；跨Shot旁白/VO允许直接绑定`video_unit_id`。Stage 05要求每条需要声音执行的Line在`pre_video`前至少有`shot_id`或`video_unit_id`之一。Prompt Compiler优先服从显式`video_unit_id`，否则按当前Video Unit的Shot Set选择，避免跨镜旁白因为没有单一Shot ID而被静默漏掉。
