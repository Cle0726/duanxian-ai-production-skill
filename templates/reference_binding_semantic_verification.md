# Reference Binding Semantic Verification（视觉参考绑定语义核验）｜Current Authority

> **目的：** 阻止“内部Registry说某张图控制人物，但当前实际绑定到生成器的却是无人环境图”这类高代价错误。无论Reference通过UI图片槽、Attachment顺序、Native Token还是API/Adapter Handle绑定，**接口位置都不自带Semantic Authority**。

## 1｜适用范围
凡Stage 03 / 04 / 05或Revision / Local Patch实际向生成模型绑定一张或多张视觉Reference，在生成前都必须建立当前任务的：

```text
REFERENCE BINDING CONTENT MAP
Binding Handle：UI_SLOT_1 / ATTACHMENT_2 / <REAL_NATIVE_TOKEN> / ADAPTER_REF_A
Binding Mode：UI_SLOT / ATTACHMENT_ORDER / NATIVE_TOKEN / API_HANDLE / OTHER
Expected Fields：STYLE / COLOR / CHARACTER_IDENTITY / ENVIRONMENT / PROP_START_STATE / CONTINUITY / PREVIS_TIMING ...
Actual Visible Evidence：<当前实际绑定图中已经被当前证据确认的可见事实>
Evidence Source：CURRENT VISUAL INSPECTION / CURRENT VERIFIED VISUAL CONTENT RECORD / USER EXPLICIT CURRENT MAPPING / VERIFIED EXTERNAL REPORT
Content-Role Result：PASS / PARTIAL / FAIL / UNVERIFIED
```

**没有正文Native Token不等于可以跳过本核验。** 平台只在UI里选图、拖附件或按上传顺序绑定时，同样要确认“实际绑定的是哪张图、它真的能承担什么字段”。

## 2｜证据与绑定规则
- 文件名、Asset ID、旧Workspace顺序、历史上传顺序、历史Token编号不能单独替代当前Binding Content证据。
- 如果当前Executor明确绑定的是某个Approved资产，且该资产有**当前有效、版本匹配的Verified Visual Content Record**，可复用该视觉事实；不能只凭Registry标签自证画面内容。
- `Expected Fields=CHARACTER_IDENTITY`但Actual Visible Evidence没有该人物 → `REFERENCE_CONTENT_ROLE_CONFLICT`。
- `Expected Fields=PROP_START_STATE`但物件不可辨 → PARTIAL；不能把不可见字段当已锁定。
- 同一Binding可以承担多个真实可见字段，但不能因为“顺带出现”就越权覆盖更直接Authority。
- UI槽位、Attachment选择、上传顺序、Native Token或Adapter Handle任一变化后，旧Content Map自动STALE并重建。
- UI里已绑定Reference但Prompt正文无需Token时，Final Prompt不必打印输入清单；**语义核验仍然必须完成**。

## 3｜Stage路由
- **Stage 03**：人物/环境/综合色/Style/Revision Source等多Reference绑定前核实际内容与职责，避免“图A/图B顺序错但继续生成”。
- **Stage 04**：人物、场景、道具、综合色与Previs Parent绑定前核实际内容；Panel/Board的Temporal字段只能由真实包含该阶段证据的Reference承担。
- **Stage 05**：Final Video Reference Pack的Character / Environment / Prop / Color / Style / Previs / Continuity等全部实际绑定都必须进入本Map，然后才允许Constraint Solver / Readiness判PASS。

## 4｜无法确认时
当前执行端不能可靠确认实际绑定内容时，不得猜。可以使用：
1. 用户对**当前这一批/当前槽位**的明确映射；
2. 与当前绑定资产版本一致的Verified Visual Content Record；
3. 当前视觉检查或外部多模态确认。

三者都不足时：`REFERENCE_BINDING_VISUAL_CONFIRMATION_REQUIRED`，当前生成阻断。

## 5｜Hard Fail
`REFERENCE_BINDING_UNVERIFIED / REFERENCE_CONTENT_ROLE_CONFLICT / REFERENCE_BINDING_STALE_MAP`任一未解决 → `PROMPT_COMPILATION_BLOCKED`。
