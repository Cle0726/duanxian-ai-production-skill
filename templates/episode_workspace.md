# Episode Workspace｜V4.3 Structured State Compatibility Guide

> **用途：** V4.3不再把一个不断增长的Markdown Workspace当作唯一机器状态源。本文件保留人类可读说明、旧项目迁移映射与显示建议；正式State使用`state/*.schema.yaml`。

## 1｜State分层

### Hot Episode State
Schema：`state/episode_state.schema.yaml`

只保存当前推进需要的字段：

- Episode ID / Mode / Current Skill Version
- Current Workflow State
- Current Scene / Segment / Shot
- Pending Job / Next Action / Active Route
- Screenplay / Director / Asset Freeze / Storyboard / Video等当前Lock与Approval refs
- Previous Approved Ending Frame ref
- Active Runtime refs + fingerprints
- Open failures / waiting reason

### Shot State
Schema：`state/shot_state.schema.yaml`

保存当前Shot的Director、Continuity、Reference、Storyboard、Video Execution与QC状态，不让Episode State塞入每个Shot的全部细节。

### Asset Registry
Schema：`state/asset_registry.schema.yaml`

保存Asset ID、类型、版本、Authority角色、Approval、文件/内容Fingerprint、依赖与归档状态。

### Approval Record
Schema：`state/approval_record.schema.yaml`

所有需要User Approval的Screenplay/Asset/Storyboard/Video/Master独立记录，不用一句`APPROVED`文字代替证据。

### Continuity Snapshot
Schema：`state/continuity_snapshot.schema.yaml`

Ending Frame与World State连续性单独记录。

## 2｜Lock / Freeze / Approval最小记录

```yaml
artifact_id: EP01_SCREENPLAY
version: 4
fingerprint_type: STRUCTURED_SHA256
fingerprint: "..."
status: LOCKED
source_refs: []
approval_ref: APR_EP01_SCREENPLAY_V4
```

有真实媒体文件时可增加真实文件SHA-256；结构化内容Fingerprint不得标成`FILE_SHA256`。

## 3｜继续制作

用户说“继续”时：

1. 读取Episode Hot State；
2. 如当前任务是Shot级，再读取当前Shot State；
3. 从`controller/workflow_state_machine.yaml`计算Next Action；
4. 从`controller/route_registry.yaml`选择Route；
5. 只加载该Route所需Runtime/Source。

不要为了“保险”把整集Ledger和124个Source Authority重新装入上下文。

## 4｜旧V4.2.x Workspace迁移

迁移时：

- 继承明确存在的Approved成果；
- `QC PASS / WAITING APPROVAL`不能升级为Approved；
- 没有真实版本证据时记录`fingerprint: UNKNOWN`并使依赖Runtime重编译；
- 旧`APPROVED STORYBOARD`映射到`APPROVED_PREVIS_SET`；
- 旧`CURRENT_STATE`字段投影到Episode/Shot State；
- 历史长记录写入Ledger，不复制到Hot State。

详细迁移逻辑仍读取`existing_project_migration.md`。

## 5｜建议项目目录

```text
project/
  state/
    episode_state.yaml
    shots/
      <SHOT_ID>.yaml
    approvals/
    continuity/
    asset_registry.yaml
  runtime/
    story/
    director/
    asset/
    scene/
    reference/
    video/
    qc/
  ledger/
```

Skill包中的`state/`和`runtime/`是Schema，不是项目实际State实例。


## V4.5.3 Compatibility｜Text-only Continuation

兼容Workspace可显示`CONTROLLER_MODE / VISUAL_EVIDENCE_REF / VISUAL_REVIEW_QUEUE`，但机器Source of Truth在`state/episode_state.schema.yaml`与`state/visual_evidence.schema.yaml`。看不到图片的模型不得仅根据Workspace文字把未审图片升级为视觉PASS。
