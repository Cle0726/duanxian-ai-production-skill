# Media Review Proxy Protocol｜视觉审核代理图硬边界

> 适用：任何图片批次、4K/大尺寸PNG、Storyboard Panel、Contact Sheet、Generation Candidate、Video Conditioning Frame及Ending Frame的视觉审核。

## 1｜固定顺序

视觉审核必须按以下顺序执行，不得从逐张打开原始大图开始：

1. 运行`tools/media_review_proxy_builder.py`，先完成Metadata Inventory；
2. Inventory必须保存文件名、绝对路径、目录结构、宽高、格式、字节数、修改时间与SHA-256；
3. 同一脚本随后生成最长边不超过1600px的JPG/WEBP代理图和审核Contact Sheet；
4. 先用Contact Sheet做批次筛选，再打开候选的单项代理图做视觉判断；
5. 最终单项资产验收必须回到该资产自己的代理图，Contact Sheet只能做Triage，不得单独产生最终PASS；
6. 原始高分辨率文件保留在磁盘，Evidence与报告用绝对路径和Fingerprint引用，不把原图反复嵌入会话。

标准调用：

```powershell
python tools/media_review_proxy_builder.py <image-or-directory> --output <review-package> --max-edge 1600 --format jpg
```

## 2｜禁止行为

- Metadata Inventory完成前，不得调用`view_image`逐张打开原始图片；
- 不得为了“再确认一次”重复读取同一张原始4K/大尺寸PNG；
- 已有Fingerprint匹配代理图时，继续审核必须复用代理图；
- Contact Sheet不得冒充单项资产细节验收，也不得替代最终选中资产的独立代理图复核；
- 代理图不得反向覆盖、改写或降采样原始资产。

只有当代理图不能裁决一个明确的局部细节时，才允许对原图做一次有坐标范围的局部Crop；Crop同样限制最长边不超过1600px，保存路径和源Fingerprint，并在Evidence中写明`proxy_insufficient_reason`。不得重新打开整张原图。

## 3｜Evidence与缓存

- `review_manifest.json`是Source→Proxy→Contact Sheet的Lineage Map；
- 代理复用以Source SHA-256匹配为准，文件名相同但Hash变化时必须重建；
- Visual Evidence的`source_fingerprint`始终绑定原始文件；代理图只作为`review_derivative_ref`；
- 审核记录至少保存`source_absolute_path / source_sha256 / proxy_absolute_path / proxy_sha256 / review_scope / verdict`；
- Contact Sheet审核只允许`SHORTLIST / REJECT_OBVIOUS / NEED_INDIVIDUAL_REVIEW`，不允许单独写`APPROVED_FINAL`。

## 4｜任务完成门

一个图片批次只有在以下条件全部满足时才完成审核：

- Inventory与目录结构已持久化；
- 所有实际打开的审核图最长边不超过1600px；
- Contact Sheet完成批次筛选；
- 每个最终APPROVED资产都已单独打开其代理图验收；
- Evidence回指原始绝对路径、原始SHA-256和实际审核代理图；
- 原始文件未修改。
