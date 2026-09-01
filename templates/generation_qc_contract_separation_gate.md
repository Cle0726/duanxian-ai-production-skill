# Generation / QC Contract Separation Gate（生成契约与质检契约分离闸门）｜Current Authority

> **目的：** 阻止`【成片必须满足】/ 自检 / QC清单`在Final Prompt末尾把Timeline、Audio、Camera、Reference限制重新说一遍，造成冲突与注意力过载。

## 1｜两份Contract
### GENERATION CONTRACT
只包含模型为了生成这一Take必须执行的可观察指令。

### QC CONTRACT
只包含Verifier在真实Take生成后要检查的标准、证据和Verdict字段。

两者可以检查同一事实，但**QC文字不能复制回Generation Prompt**。

## 2｜禁止回流
Final Model Prompt不得出现：
- `成片必须满足 / 自检 / 验收清单 / PASS条件 / QC检查`；
- 为了QC方便再次重复Timeline已有的动作；
- 为了QC方便再次重复Audio开关；
- 为了QC方便再次重复Camera状态。

如果某QC项发现Generation Contract缺了真正必要的执行事实，应回到对应Owner字段补一次，然后重新Conflict Solve；不得在末尾追加“必须满足”。

## 3｜Hard Fail
`QC_CONTRACT_BACKFLOW / ACCEPTANCE_CHECKLIST_IN_PROMPT / QC_ECHO_CONFLICT` → `PROMPT_COMPILATION_BLOCKED`。


## V4.5.3 Visual Evidence Persistence

视觉QC若由多模态模型/人工真实看图得出，结果不仅写PASS/FAIL，还必须把可复用Observed Visual Facts与Source Fingerprint写入`VISUAL_EVIDENCE`。QC Contract描述“应该检查什么”，Visual Evidence记录“这一个文件版本实际看到了什么”；两者不能互相替代。
