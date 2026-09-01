# Shot Proof Capacity & Motion Budget Gate（镜头证明容量与运动负载闸门）｜Current Authority

> **目的：** 逻辑不冲突也可能生成失败。一个Wide镜头如果同时要求“看清群体惯性 + 司机双手 + 手杖滚动 + 一枚硬币轨迹”，可能超过这个构图真正能证明的信息容量。该Gate在昂贵Video前判断：**当前镜头能否清楚承载这些P0/P1信息，以及同一时间窗的独立运动是否过载。**

## 1｜Critical Read Priority
每个Segment先把可见要求分级：
- `P0 NARRATIVE-ESSENTIAL`：没有它，这段戏意义不成立；
- `P1 IMPORTANT`：强烈希望保留，但可通过别的镜头/声音/静态锚点补；
- `P2 DETAIL`：漂亮或具体，但不值得牺牲首轮稳定性。

精确运动计数（如“必须滚两圈”）默认不得自动成为P0，除非Canon/Director明确赋予叙事意义。

## 2｜Shot Proof Capacity
检查：
- 当前景别/距离是否让每个P0 Critical Read足够大、无遮挡、持续时间足够；
- 微小物件（硬币、戒指、眼部细纹）是否在当前构图有真实Legibility；
- P0事件是否在不同深度/区域互相争夺注意力；
- Entry/Landing Camera Geometry、Lens Family、DOF/Focus Plan与Camera Move是否会进一步降低关键事件可读性；
- 如果一个关键事件只能靠“模型自动帮我们切特写”才能看清，则当前连续镜头Proof不成立。

失败：`SHOT_PROOF_CAPACITY_EXCEEDED / MICRO_OBJECT_LEGIBILITY_FAIL / CRITICAL_READ_COMPETITION / FOCUS_READABILITY_CONFLICT`。

## 3｜Motion Budget（动态预算，不是固定模板）
对每个重叠时间窗统计：
- Primary Action Cluster；
- Independent Secondary Actions；
- Independent Prop Events；
- Dominant Camera Move；
- Exact Timing / Exact Count Constraints；
- Crowd Reaction Layers；
- Audio Events（声音不等于视觉负载，但会增加同步要求）。

默认安全倾向：一个时间窗有**一个主要动作簇 + 至多一个主导Camera行为 + 少量从属动作/环境运动**。不是硬编码数字；复杂镜头可以更高，但必须有Previs Proof。

## 4｜状态
- `PASS`：当前负载可直接进入Video；
- `SIMPLIFY`：删除/降级P2，合并同因果从动作；
- `PREVIS_REWORK`：需要换构图、距离、Anchor或静态证明；
- `SPLIT_REQUIRED`：只有Director允许Cut/Split时采用；
- `BLOCK`：当前设计本身不可稳定执行。

不得因为模型“也许能抽出来”把`PREVIS_REWORK/BLOCK`强行送入Video。

## 5｜SEG03应用
优先级建议由Director/Story决定，不固定写死，但典型分析：
- P0：急刹、群体可信惯性、缺失惊叫但环境机械声继续；
- P1：司机制动、手杖落地、硬币滚动；
- P2：手杖精确滚两圈、硬币必须精确抵某一点、额外扶手微动作。
若同一低机位Wide无法同时证明司机双手和硬币轨迹，必须调整Proof策略，而不是加更多文字。
