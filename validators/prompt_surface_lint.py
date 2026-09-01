#!/usr/bin/env python3
import re, sys, json, argparse

PATTERNS = {
    "WINDOWS_PATH": r"(?i)[A-Z]:\\",
    "POSIX_LOCAL_PATH": r"/(?:mnt|home|Users|tmp)/",
    "FILE_EXTENSION": r"(?i)\.(?:png|jpe?g|webp|gif|mp4|mov|zip|md|txt)\b",
    "TASK_SHELL": r"图片生成任务|视频生成任务|生成任务|任务说明|输入图|输入图片|输入素材|基于以下输入图|图A\b|图B\b|Image A\b|Image B\b|Output Target|输出Target|保存到",
    "SELF_CHECK": r"【?自检】?|生成后确认|审核标准|任一不满足.*重新生成",
    "PIPELINE_JARGON": r"(?i)\bStage\s*0?[1-6]\b|Style Projection|MUST_BIND|Authority|Resolver|Registry|Capsule|Executor Input Map|Semantic Role|Hard Fail|参考职责|视觉权威|综合色权威|人物权威|执行闸门|方法加载|状态机",
    "INTERNAL_ASSET_ID": r"\b(?:ENV|ASM|COLOR|CHAR|PROP|FMH|SHOT|SCENE|VID|STYLE|TF|TE|WP)_[A-Z0-9_]{4,}(?:_v\d+)?\b",
    "VERSION_TAG": r"(?i)(?:^|[_\-])v\d{3,}\b|\bV\d+\.\d+(?:\.\d+)?(?:-BLIND)?\b",
    "META_NEGATIVE": r"(?i)若平台支持\s*negative prompt|if .*supports? negative prompt|negative prompt.*请添加",
    "ADMIN_HEADING": r"【(?:图片生成任务|输入图|必须满足|要求|自检|审核标准|Reference[^】]*)】",
    "BINDING_PACKET": r"(?i)REFERENCE_UPLOAD_BINDING_LIST|NATIVE_BINDING_REQUIRED|MUST_BIND_(?:EXISTING_ASSETS|COLOR_AUTHORITY|STYLE_EVIDENCE)|Executor Binding Packet",
    "QC_CONTRACT_BACKFLOW": r"成片必须满足|QC检查|QC验收|PASS条件|验收清单|必须满足以下验收",
    "PROMPT_PREFIX_DUPLICATION": r"生成视频\s*[:：]\s*生成视频\s*[:：]|生成图片\s*[:：]\s*生成图片\s*[:：]",
    "DURATION_ECHO": r"(?i)(?:\b\d+(?:\.\d+)?s\b\s*[，,、 ]*){3,}",
}

def lint(text):
    findings = {}
    for name, pat in PATTERNS.items():
        matches = list(re.finditer(pat, text, flags=re.M))
        findings[name] = len(matches)
    return findings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='?')
    args = ap.parse_args()
    text = open(args.file, 'r', encoding='utf-8').read() if args.file else sys.stdin.read()
    findings = lint(text)
    ok = all(v == 0 for v in findings.values())
    print(json.dumps({"pass": ok, "findings": findings}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if ok else 2)

if __name__ == '__main__':
    main()
