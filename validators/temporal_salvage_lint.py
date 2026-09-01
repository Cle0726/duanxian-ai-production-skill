#!/usr/bin/env python3
import re, sys, json, argparse

STATUS_RE = re.compile(r"Temporal\s+Salvage\s+Status\s*:\s*(FULL_TAKE_USABLE|SALVAGE_AVAILABLE|NO_SALVAGE|INSUFFICIENT_EVIDENCE)", re.I)
DURATION_RE = re.compile(r"Source\s+Duration\s*:\s*(\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?|\d+(?:\.\d+)?\s*s?)", re.I)
RANGE_RE = re.compile(r"(?P<start>\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?)\s*[–—-]\s*(?P<end>\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?)")
CLASS_RE = re.compile(r"\b(CLEAN_KEEP|CONDITIONAL_KEEP|HANDLE_ONLY|REJECT)\b")

def to_seconds(ts):
    ts=ts.strip().lower().rstrip('s').strip()
    if ':' not in ts:
        return float(ts)
    parts=ts.split(':')
    if len(parts)==2:
        return float(parts[0])*60+float(parts[1])
    return float(parts[0])*3600+float(parts[1])*60+float(parts[2])

def lint(text):
    findings=[]
    m=STATUS_RE.search(text)
    status=m.group(1).upper() if m else None
    if not status: findings.append('MISSING_TEMPORAL_SALVAGE_STATUS')
    dm=DURATION_RE.search(text)
    duration=to_seconds(dm.group(1)) if dm else None
    windows=[]
    for line in text.splitlines():
        rm=RANGE_RE.search(line); cm=CLASS_RE.search(line)
        if rm and cm:
            st=to_seconds(rm.group('start')); en=to_seconds(rm.group('end')); cls=cm.group(1).upper()
            windows.append((st,en,cls,line.strip()))
            if en <= st: findings.append('NON_POSITIVE_WINDOW')
            if cls in ('CLEAN_KEEP','CONDITIONAL_KEEP','HANDLE_ONLY'):
                for req in ('VIDEO_USE','AUDIO_USE'):
                    if req not in line: findings.append(f'MISSING_{req}')
                if cls=='CLEAN_KEEP':
                    for req in ('ENTRY','EXIT','Continuity','Director'):
                        if req.lower() not in line.lower():
                            findings.append('CLEAN_KEEP_MISSING_CUT_CONTINUITY_DIRECTOR_FIELDS'); break
                if 'VIDEO_USE: REJECT' in line.upper() and 'AUDIO_USE: AUDIO_ONLY' not in line.upper():
                    findings.append('VIDEO_REJECT_KEEP_WITHOUT_AUDIO_ONLY')
            if cls=='REJECT' and 'AUDIO_USE: AUDIO_ONLY' in line.upper():
                findings.append('AUDIO_ONLY_MISCLASSIFIED_AS_REJECT')
    windows.sort(key=lambda x:x[0])
    for a,b in zip(windows,windows[1:]):
        if b[0] < a[1]-1e-6:
            findings.append('OVERLAPPING_WINDOWS'); break
    if status=='SALVAGE_AVAILABLE' and not any(x[2] in ('CLEAN_KEEP','CONDITIONAL_KEEP','HANDLE_ONLY') for x in windows):
        findings.append('SALVAGE_AVAILABLE_WITHOUT_KEEP_WINDOW')
    if status=='NO_SALVAGE' and any(x[2] in ('CLEAN_KEEP','CONDITIONAL_KEEP','HANDLE_ONLY') for x in windows):
        findings.append('NO_SALVAGE_CONTRADICTS_KEEP_WINDOW')
    # Full-timeline coverage can only be mechanically proven with Source Duration.
    if status in ('SALVAGE_AVAILABLE','NO_SALVAGE'):
        if duration is None:
            findings.append('MISSING_SOURCE_DURATION_FOR_COVERAGE_CHECK')
        elif not windows:
            findings.append('SALVAGE_TIMELINE_COVERAGE_GAP')
        else:
            tol=0.051
            if windows[0][0] > tol: findings.append('SALVAGE_TIMELINE_COVERAGE_GAP')
            if abs(windows[-1][1]-duration) > tol: findings.append('SALVAGE_TIMELINE_COVERAGE_GAP')
            for a,b in zip(windows,windows[1:]):
                if b[0] > a[1]+tol:
                    findings.append('SALVAGE_TIMELINE_COVERAGE_GAP'); break
    # Detect positive auto-approval/ending-authority leakage without flagging explicit prohibitions.
    for raw in text.splitlines():
        line=raw.strip(); low=line.lower()
        if 'salvage_candidate' in low and 'approved_salvage_clip' in low and ('automatic' in low or '自动' in line or '无需批准' in line):
            neg = ('not automatic' in low or '非自动' in line or '不自动' in line or '不得自动' in line or '不能自动' in line or '需批准' in line)
            if not neg: findings.append('SALVAGE_AUTO_APPROVAL')
        if 'salvage_candidate' in low and 'ending frame' in low and ('authority' in low or 'approved' in low):
            neg = ('not ' in low or '不是' in line or '不得' in line or '不能' in line or '无权' in line or '不作为' in line)
            positive_assignment = any(tok in low for tok in ('= yes','= true',': yes',': true','becomes ending frame','is ending frame')) or '升级为ending frame' in low
            if positive_assignment and not neg: findings.append('SALVAGE_ENDING_FRAME_AUTHORITY_BLEED')
    return {'pass':not findings,'status':status,'source_duration':duration,'window_count':len(windows),'findings':sorted(set(findings))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file',nargs='?'); a=ap.parse_args()
    text=open(a.file,'r',encoding='utf-8').read() if a.file else sys.stdin.read()
    out=lint(text); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
