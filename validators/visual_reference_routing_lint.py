#!/usr/bin/env python3
import json, sys, argparse

COLOR_APPLIED_TRIGGERS={"DIRECT_FAIL","LITERALIZATION_OBSERVED","ROLE_SEPARATION_FAIL_NO_SAFE_CROP","SLOT_LIMIT_PROVEN","USER_REQUIRED"}
STYLE_APPLIED_TRIGGERS={"DIRECT_FAIL","LITERALIZATION_OBSERVED","SAMPLE_BLEED_OBSERVED","ROLE_SEPARATION_FAIL_NO_SAFE_CROP","SLOT_LIMIT_PROVEN","USER_REQUIRED"}
TEXT_FALLBACK_REASONS={"PLATFORM_UNSUPPORTED","SLOT_LIMIT_PROVEN","FIELD_FULLY_COVERED_BY_OTHER_VISUAL_OWNER","USER_REQUIRED"}

def lint(data):
    issues=[]
    caps=data.get('capabilities',{})
    platform_accepts_images=bool(data.get('platform_accepts_images',True))
    for r in data.get('references',[]):
        cls=r.get('class','').upper(); route=r.get('route','').upper(); risk=r.get('layout_risk','UNKNOWN').upper(); role=bool(r.get('role_lock',False))
        cap_key={'COLOR':'DIRECT_COLOR_CARD','STYLE':'DIRECT_STYLE_BOARD','STORYBOARD':'DIRECT_STORYBOARD_BOARD'}.get(cls)
        cap=(caps.get(cap_key,'UNKNOWN') if cap_key else 'UNKNOWN').upper()
        hist=str(r.get('literalization_history','NONE')).upper()
        role_sep=str(caps.get('ROLE_SEPARATION','UNKNOWN')).upper()
        sample_hist=str(r.get('sample_bleed_history','NONE')).upper()

        if route=='DIRECT_BIND':
            if not platform_accepts_images:
                issues.append({'type':'DIRECT_BIND_PLATFORM_UNSUPPORTED','reference':r.get('id')})
            if cap=='VERIFIED_FAIL': issues.append({'type':'DIRECT_BIND_CAPABILITY_FAIL','reference':r.get('id')})
            if cls in {'COLOR','STYLE','STORYBOARD'} and not role: issues.append({'type':'DIRECT_BIND_ROLE_LOCK_MISSING','reference':r.get('id')})
            if bool(r.get('requires_role_separation',False)) and role_sep=='VERIFIED_FAIL': issues.append({'type':'DIRECT_BIND_ROLE_SEPARATION_FAIL','reference':r.get('id')})
            if cls=='STORYBOARD' and risk=='HIGH' and cap!='VERIFIED_PASS': issues.append({'type':'HIGH_RISK_BOARD_UNVERIFIED','reference':r.get('id')})

        if route=='APPLIED_REFERENCE' and cls=='COLOR':
            trig=str(r.get('applied_trigger','')).upper()
            if trig not in COLOR_APPLIED_TRIGGERS:
                issues.append({'type':'PREEMPTIVE_APPLIED_REFERENCE','reference':r.get('id'),'trigger':trig or 'NONE'})
                if cap=='UNKNOWN' and hist!='OBSERVED':
                    issues.append({'type':'UNKNOWN_IS_NOT_APPLIED_TRIGGER','reference':r.get('id')})
            else:
                evidence_ok = (
                    (trig=='DIRECT_FAIL' and cap=='VERIFIED_FAIL') or
                    (trig=='LITERALIZATION_OBSERVED' and hist=='OBSERVED') or
                    (trig=='ROLE_SEPARATION_FAIL_NO_SAFE_CROP' and role_sep=='VERIFIED_FAIL' and r.get('non_generative_isolation_available') is False) or
                    (trig=='SLOT_LIMIT_PROVEN' and bool(r.get('slot_limit_proven',data.get('slot_limit_proven',False)))) or
                    (trig=='USER_REQUIRED' and bool(r.get('user_required',data.get('user_required',False))))
                )
                if not evidence_ok:
                    issues.append({'type':'APPLIED_TRIGGER_EVIDENCE_MISMATCH','reference':r.get('id'),'trigger':trig})

        if route=='APPLIED_REFERENCE' and cls=='STYLE':
            trig=str(r.get('applied_trigger','')).upper()
            if trig not in STYLE_APPLIED_TRIGGERS:
                issues.append({'type':'PREEMPTIVE_STYLE_APPLIED_REFERENCE','reference':r.get('id'),'trigger':trig or 'NONE'})
            else:
                evidence_ok = (
                    (trig=='DIRECT_FAIL' and cap=='VERIFIED_FAIL') or
                    (trig=='LITERALIZATION_OBSERVED' and hist=='OBSERVED') or
                    (trig=='SAMPLE_BLEED_OBSERVED' and sample_hist=='OBSERVED') or
                    (trig=='ROLE_SEPARATION_FAIL_NO_SAFE_CROP' and role_sep=='VERIFIED_FAIL' and r.get('non_generative_isolation_available') is False) or
                    (trig=='SLOT_LIMIT_PROVEN' and bool(r.get('slot_limit_proven',data.get('slot_limit_proven',False)))) or
                    (trig=='USER_REQUIRED' and bool(r.get('user_required',data.get('user_required',False))))
                )
                if not evidence_ok:
                    issues.append({'type':'APPLIED_TRIGGER_EVIDENCE_MISMATCH','reference':r.get('id'),'trigger':trig})

        # Visual-First: UNKNOWN alone must not collapse an Approved visual control to text.
        if route=='TEXT_FALLBACK' and cls in {'COLOR','STYLE','STORYBOARD'} and platform_accepts_images and cap!='VERIFIED_FAIL':
            reason=str(r.get('text_fallback_reason','')).upper()
            if reason not in TEXT_FALLBACK_REASONS:
                issues.append({'type':'PREMATURE_TEXT_FALLBACK','reference':r.get('id'),'reason':reason or 'NONE'})

    for h in data.get('humans',[]):
        if h.get('critical_or_readable',False) and h.get('visual_owner','').upper() in {'','TEXT_ONLY','VIDEO_MODEL_GUESS'}:
            issues.append({'type':'HUMAN_VISUAL_AUTHORITY_GAP','human':h.get('id')})
    return {'pass':not issues,'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file',nargs='?'); a=ap.parse_args(); data=json.load(open(a.file,encoding='utf-8')) if a.file else json.load(sys.stdin)
    out=lint(data); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
