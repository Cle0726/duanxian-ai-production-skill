# Visual Beat Map & Music Sync Handoff（视觉拍点 → Stage 06配乐同步交接）

> **用途：** 把Stage 02/04/05已经设计好的音乐化动作时间结构，可靠交给Stage 06配乐与剪辑。Stage 05仍然NO AUTO BGM；本文件不要求视频模型生成正式BGM。
>
> **核心原则：音乐身份先决定动作时间结构；视频生成后记录真实视觉落点；Stage 06再让正式BGM去配合真实画面，而不是反过来强迫已生成动作追一个不存在的BPM。**

---

## 1｜什么时候必须建立Visual Beat Map

以下情况至少建立一个简版Map：
- Music Identity直接影响战斗动作；
- 休止、切分、延音、对位、渐强/渐弱、反复、终止等是镜头叙事机制；
- 终结技/关键Hit明确依赖“第N拍”或某个停顿；
- 变身、合奏、共鸣断裂等需要音乐与视觉同步；
- 预告/高潮Hero Shot需要Stage 06精准Stinger / Drop / Silence。

普通无音乐机制对白不强制。

---

## 2｜三层时间记录

### A. Planned Visual Beat Map｜Stage 02/04
记录相对结构，不要求先锁BPM：

```text
Beat Map ID: VB-EP01-S04-SEG03-v001
Phrase Start: SH27启动
Protected Sync Point A: 艾莉娅第二次刺击落点
Rest / Hold: 敌人停顿一拍
Major Contact: 第四拍手炮抵近核心
Cadence / Exit: 荆棘解除，角色回到新稳定状态
```

### B. Generated Take Beat Map｜Stage 05 QC后
从实际Take记录真实时间戳：

```text
00:01.20 Phrase Start
00:02.65 Sync A
00:03.40 Rest/Hold Start
00:04.15 Major Contact / Fourth Beat
00:05.70 Cadence / Recovery
```

以实际Approved Video为准，不用计划时间冒充真实时间。

### C. Stage 06 Music Sync Map
Stage 06根据真实画面决定：
- Cue In；
- Phrase Alignment；
- Duck；
- Stinger / Major Hit；
- Silence / Drop；
- Cue Out；
- 必要时音乐自身剪辑/重排/轻微Time-Stretch。

---

## 3｜Protected Visual Sync Point

标记为`PROTECTED_SYNC_POINT`的视觉事件，Picture Lock后不应为了让现成BGM“更顺”而随意移动，除非导演明确允许。

典型：
- 关键Contact；
- 第四拍；
- 武器断裂；
- 圣约断裂；
- 角色第一次变身完成；
- Boss核心破裂；
- 剧情级Silent Beat。

Stage 06优先调整音乐，而不是破坏已经成立的动作因果与打击节奏。

---

## 4｜音乐术语到Stage 06的交接

Stage 05记录的是**可见动作语法**：
- Rest / Hold；
- Sustain；
- Syncopation / Off-beat；
- Counterpoint；
- Crescendo / Diminuendo；
- Repetition / Variation；
- Cadence / Unresolved Closure。

Stage 06把它翻译成音乐选择与编辑：
- Rest不一定等于完全无声，可是BGM可以Drop / Thin / Duck；
- Sustain可延长和声/低音尾部，不要求画面继续发光；
- Syncopation让音乐重音避开常规预期并对齐真实攻击窗口；
- Counterpoint可用不同声部交错，但不能为了理论正确压过对白和SFX；
- Crescendo必须跟动作/风险升级一致，而不是一进战斗就最大；
- Cadence决定Cue Out / Release是否有完成感。

---

## 5｜SFX优先级

关键Contact / Weapon Clash / Core Break的瞬态打击音不得被BGM掩盖。

Stage 06可在`PROTECTED_SYNC_POINT`：
- 短暂Duck BGM；
- 保留Transient + Body + Material + Debris + Tail层；
- 剧情级Impact可使用Post-Impact Vacuum /短暂抽空，但不得滥用。

---

## 6｜Workspace字段

每个适用Segment记录：
- `Visual Beat Map ID / Version`；
- `Planned Beat Map: READY / N/A`；
- `Approved Take Timestamp Map: READY / PENDING / N/A`；
- `Protected Sync Points`；
- `Stage 06 Music Sync Handoff: READY / PENDING / N/A`。

若Video Take换版，旧Timestamp Map自动STALE，必须从新Approved Take重建。

---

## 7｜QC

Stage 06检查：
- BGM重拍/Drop是否错过关键视觉Contact；
- 音乐是否覆盖重要SFX；
- Rest/Hold是否被持续高强度音乐破坏；
- Crescendo是否与风险升级同向；
- 角色Music Identity是否连续；
- 没有为了配乐把已批准视觉动作随意Time-remap到失真。
