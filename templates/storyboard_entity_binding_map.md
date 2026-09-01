# Storyboard Entity Binding Map｜V4.5.7

离图Slot映射Authority。白描像素匿名，但H_A/H_B/P_A/E_A等内部Slot必须稳定绑定真实Entity ID、Approved视觉Authority候选与Panel级站位/动作状态。Slot ID不得进入图片像素或最终模型Prompt。

## Identity Readability Policy

Human slots additionally carry an identity-readability policy:
- `REQUIRED`: always run platform-scale identity readability;
- `AUTO`: default. `CRITICAL` and `SUPPORT` humans are checked; `AMBIENT` humans are not unless explicitly promoted;
- `NOT_REQUIRED`: allowed only when the human is intentionally non-identifiable/deep background and must not be used as a named-character identity source.

A clear named person must never be downgraded to `SUPPORT` merely to bypass identity QC.
