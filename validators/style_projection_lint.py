#!/usr/bin/env python3
import re, sys, json, argparse

CATEGORIES = {
    "RENDER_FAMILY": [r"二维", r"2D", r"anime[- ]?influenced", r"插画"],
    "LINEWORK_SHADING": [r"手绘.*线", r"linework", r"色块", r"color blocking", r"绘画阴影", r"painterly shading", r"柔和.*阴影"],
    "HUMAN_RENDERING": [r"欧陆.*骨相", r"欧洲.*骨相", r"matte painted skin", r"哑光.*皮肤", r"发束", r"hair"],
    "PALETTE_VALUE": [r"综合色", r"palette", r"色族", r"chroma", r"选择性显色", r"selective saturation", r"对比", r"contrast", r"明度", r"value hierarchy"],
    "ATMOSPHERE": [r"欧陆复古", r"European retro", r"电影化", r"cinematic", r"文学", r"literary", r"忧郁", r"melancholic", r"克制", r"restrained"],
}
CONTINUITY = re.compile(r"保持.*(?:参考|同一|既有).*(?:画风|绘画|渲染|风格)|same (?:visual|render|art) style|style continuity", re.I)

def category_hit(text,pats): return any(re.search(p,text,re.I) for p in pats)

def lint(text,human_required=False,visual_bound=False):
    hits={k:category_hit(text,v) for k,v in CATEGORIES.items()}
    if visual_bound:
        ok=bool(CONTINUITY.search(text))
        return {"pass":ok,"mode":"MINIMAL_VISUAL_BOUND","continuity_sentence":ok,"hits":hits,"missing":[] if ok else ["STYLE_CONTINUITY_SENTENCE"]}
    required=["RENDER_FAMILY","LINEWORK_SHADING","PALETTE_VALUE","ATMOSPHERE"]
    if human_required: required.append("HUMAN_RENDERING")
    missing=[k for k in required if not hits[k]]
    return {"pass":not missing,"mode":"FULL_TEXT","required":required,"hits":hits,"missing":missing}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file',nargs='?'); ap.add_argument('--human-required',action='store_true'); ap.add_argument('--visual-style-evidence-bound',action='store_true')
    a=ap.parse_args(); text=open(a.file,'r',encoding='utf-8').read() if a.file else sys.stdin.read()
    out=lint(text,a.human_required,a.visual_style_evidence_bound); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
