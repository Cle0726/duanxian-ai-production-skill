# Load on Demand｜V4.3 Compatibility Entry

> **状态：** 兼容文件。V4.3不再在本Markdown维护第二份完整Route表。

## 唯一Route Authority

当前任务的MUST LOAD / Runtime / Conditional Source / Forbidden Context统一读取：

`controller/route_registry.yaml`

如果本文件与`route_registry.yaml`存在差异，**以`route_registry.yaml`为准**。

## 执行规则

1. 先从`controller/workflow_state_machine.yaml`得到Next Action与Route ID。
2. 读取Route声明的Runtime。
3. Runtime有效时，不回读对应完整Source Authority。
4. Runtime不存在、STALE、字段不足、Source版本变化、冲突或QC失败时，只回读Route声明的`source_if_missing_or_stale / compile_runtime_from_source / conditional_source`。
5. `execute_with`表示每次该任务执行阶段需要的Compiler/Surface/Gate，不意味着这些文件拥有领域Canon。
6. Stage 02A的`forbidden_context`是Context Isolation Policy：Director Judge前禁止Cost、现有资产便利度、Reference Slot、Platform Duration参与导演方案选择。
7. 不允许通过关键词搜索把未被当前Route声明的历史/Deprecated内容提升为Authority。

## Compatibility

旧文档或Workspace若写“读取`load_on_demand_controller.md`”，V4.3解释为：**读取本兼容入口，然后执行`controller/route_registry.yaml`。**
