# Web QC Platform Watermark Exception（网页版QC平台水印豁免）｜V4.3 Method

> **用途：** 允许使用免费额度生成的图片 / Storyboard / Previs / Video Take进入网页版QC时携带指定平台水印，避免把平台商业标记误判为生成失败。
> **适用范围：** 仅Web Asset QC、Web Storyboard / Previs QC、Web Video QC及其External Report导入。
> **不改变：** 生成Prompt、项目美术设计、角色/场景/道具Authority、正式版权/发行要求。

---

## 1｜Profile驱动的默认豁免名单

正式名单从`adapters/web_qc/platform_profile.yaml`读取。当前Profile中`Dola AI`与`豆包AI生成`均为`NEUTRAL_PLATFORM_WATERMARK`。本文件只定义如何处理，不再拥有名单值。

允许识别其正常的大小写、字体、透明度、角标/角落排版差异；只要能够合理确认是上述平台的生成标记，就按本Authority处理。

**禁止泛化：** 这不是“所有水印都允许”。其他未知平台水印、品牌Logo、广告字样、随机生成文字、剧情内不应存在的文字，仍按原QC规则独立判断。

---

## 2｜QC中性规则

当指定水印仅作为平台角标存在，且不遮挡关键验证证据时：

- 不得因此判`FAIL / REVISE`；
- 不得记为P0 / P1 / P2；
- 不得记为文字污染、Logo污染、UI污染、画面不洁、风格漂移或额外物体；
- 不得把去水印写入`Minimum Necessary Change`；
- 不得因为指定水印建议重生成、换平台或额外消耗Take / Candidate；
- 候选比较时不得因为某张图/某个Take带指定水印而降低排名。

允许在报告的非问题备注中写：
`Allowed Platform Watermark Observed: Dola AI / 豆包AI生成`，但默认无需专门报告。

---

## 3｜遮挡关键证据时

如果指定水印实际覆盖了必须验证的关键区域，例如：

- 主要人物眼睛 / 脸部身份；
- 关键手部接触点；
- 武器 / 道具结构；
- 必须读清的Transformation Eye Signature；
- 关键Storyboard Action Contact；
- 必须验证的环境地标 / 出入口；

则：

1. **仍不得把“水印存在”作为P0/P1/P2视觉失败。**
2. 只对被挡住的验证维度标：`EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK`。
3. 若其他帧 / 其他Reference足以验证，则继续正常给Verdict，不要求补证据。
4. 只有该维度确实无法验证时，才允许对该维度给`INSUFFICIENT_EVIDENCE`或请求最小补充证据。
5. 不得因此要求重做已经可验证且正确的其他部分。

---

## 4｜Web QC Copy Prompt必须显式携带

所有Web Asset / Storyboard / Video QC Copy Prompt必须写入一个简短的`【允许的平台水印｜QC豁免】`区块，至少包含：

```text
【允许的平台水印｜QC豁免】
以下免费额度平台水印为QC中性，不得作为P0/P1/P2、文字污染、Logo污染、画面质量失败或返工理由：
- Dola AI
- 豆包AI生成
若指定水印只是角标且不遮挡关键证据，请直接忽略；若实际遮住必须验证的关键区域，只标记EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK，并仅在无法从其他证据完成判断时使用INSUFFICIENT_EVIDENCE。其他未知水印/品牌字样不在此豁免内。
```

不得只把这条写在内部Authority而漏出Copy Prompt，因为网页版Verifier不读取本Skill文件。

---

## 5｜External Report导入归一化

若网页版Verifier仍把`Dola AI`或`豆包AI生成`水印列为P0/P1/P2或Revision Target，本地导入时必须先执行归一化：

- 水印本体问题 → 从Failure List移除；
- 仅因指定水印导致的`REVISE` → 重新判断剩余真实问题；若无其他问题，恢复为可PASS状态；
- 水印遮挡关键证据 → 转写为`EVIDENCE_OCCLUDED_BY_ALLOWED_PLATFORM_WATERMARK`，按证据充分性处理；
- 不得因为外部Verifier误判而额外消耗生成额度。

---

## 6｜边界

本Authority只表示：**这些平台水印不影响当前生产QC。**

它不自动声明这些水印满足未来发行、商业交付、平台上传或版权清洁要求。若项目未来进入正式发布 / 商业母版阶段，应单独执行Delivery Cleanliness / Platform Compliance检查；不得反向用发行要求阻止当前免费额度素材的开发期QC。
