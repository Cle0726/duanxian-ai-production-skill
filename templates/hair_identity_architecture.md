# Hair Identity Architecture（发型身份架构）

> **用途：** 防止新人物都被生成成“同款长发/同款刘海/同款发梢渐变”。发型必须同时在远景剪影、中景结构、近景发束三个尺度上拥有角色身份。

## 0｜时代豁免与流量审美授权

- 发型**不跟随服装的20世纪70–90年代复古限制**：现代流行发型全部可用（大波浪、龙须刘海、狼尾、空气刘海、高颅顶、编发盘发、层次长发等），复古服装 + 现代感发型是漫剧通行做法；
- 成年角色的发型可以承担第一眼吸引力（Appeal Hook），发型设计按短剧流量审美执行：允许飘逸长发、精致刘海、明显卷度、发量感、光泽、发饰与高识别度轮廓；
- 未成年角色发型只走可爱/辨识度路线；
- 发型风格的多样性本身是流量资产：全员同款“大波浪长发+渐变”依然判 `HAIR TEMPLATE COLLISION`（第3节规则不变）。

## 1｜三层Hair ID

### A. Far Silhouette｜远景轮廓
记录：
- Crown Height / Top Volume｜头顶高度与蓬度
- Overall Width｜整体横向宽度
- Weight Distribution｜上重/下重/侧重
- Side Projection｜两侧是否离脸扩张
- Back Mass｜后脑圆度/长度/束点
- Overall Length & End Landmark｜发尾落点

### B. Mid Structure｜中景结构
记录：
- Hairline / Part｜发际线与分缝
- Fringe Grammar｜刘海：幕帘/切分/斜向/短碎/无刘海/不对称等
- Temple / Cheek Framing｜鬓角、脸旁发如何包脸或离脸
- Ear Visibility｜耳朵常露/半露/被遮
- Side Volume｜侧面体积
- Tie / Braid / Pin / Gathering Point｜束发/编发/固定点（如有）
- Back Architecture｜后发分层/束状/整片/尾部结构
- End Shape｜齐切/羽化/破碎/内扣/外翻/波浪/尖束
- Asymmetry Rule｜是否存在稳定不对称

### C. Near Texture｜近景质感
记录：
- Clump Grammar｜大束、窄束、羽毛束、厚块、丝带状等
- Curl Grammar｜直 / C弯 / S弯 / 松波 / 局部折线
- Surface Character｜哑光、柔亮、厚重、轻薄、干爽等
- Edge Strands｜边缘细丝密度
- Motion Weight｜摆动偏轻/偏重/带回弹/拖尾

## 2｜Hair Silhouette Fingerprint

每个正式角色必须能用一句**不提颜色**的话描述其发型剪影。

例如合格描述应该是：
> 高额头偏侧分，头顶低蓬，双侧脸旁发短而离脸，后发在颈后形成厚重长束，发尾轻微外翻。

不合格：
> 很漂亮的长发，微卷，有层次。

## 3｜Anti-Template Gate

任意两名核心角色，不应同时共享以下4项中的3项：
- 同一Part / Fringe Grammar；
- 同一Face-framing；
- 同一Back Mass / Length Silhouette；
- 同一End Shape / Texture Grammar。

若只通过换发色、换发饰区分，判：
`HAIR TEMPLATE COLLISION`。

## 4｜Four-View要求

### FRONT FACE
- 分缝/刘海/脸旁发必须完整可读；
- 不能让长发角色全部出现同款中分/空气刘海。

### SIDE FACE
- 必须证明后脑体积、耳前发、鬓角、发尾侧视关系；
- 发型结构不能在侧面塌成通用光滑头套。

### FRONT BODY
- 头发与肩、胸、外套/礼服的落点关系要正确；
- 长发不能随机穿过肩线或衣领。

### BACK
- 必须显示真正后发架构、束点、分层、发尾；
- 不能只是“大片同色长发盖住背部”。

## 5｜Transformation Hair

可变身角色必须继承Normal Hair ID：
- 发际线与Face-framing身份保留；
- 可以重组束发、舒展大束、增加角色专属发饰或共鸣渐变；
- 变身后发型允许在长度、体积、造型、光泽与运动张力上明显增强（编发/盘发展开、发束舒展、光泽提升、造型张力增强），变身发型可比日常更惊艳、更具传播力；
- 变身后仍应从剪影认出原角色；
- 不允许所有圣谱者统一“发量变多 + 发梢渐变 + 长发飘散”。

变身TH-01必须额外记录：
`Preserved Normal Hair ID / Transformation Structural Change / Gradient Boundary / New Tie-Ornament / Motion Weight / Collision Notes`。
