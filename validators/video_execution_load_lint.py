#!/usr/bin/env python3
import json,sys,argparse

def lint(d):
    issues=[]
    for w in d.get('windows',[]):
        p=int(w.get('primary_action_clusters',0)); sec=int(w.get('independent_secondary_actions',0)); prop=int(w.get('independent_prop_events',0)); cam=int(w.get('dominant_camera_moves',0)); exact=int(w.get('exact_count_constraints',0));
        proof=bool(w.get('previs_proof',False)); critical=w.get('critical_reads',[]); micro=[x for x in critical if x.get('micro_object') and x.get('priority') in ('P0','P1') and not x.get('legibility_proven',False)]
        if cam>1: issues.append({'type':'MULTIPLE_DOMINANT_CAMERA_MOVES','window':w.get('id')})
        if micro: issues.append({'type':'MICRO_OBJECT_LEGIBILITY_FAIL','window':w.get('id'),'reads':[x.get('name') for x in micro]})
        load=p+sec+prop+exact
        if load>=7 and not proof: issues.append({'type':'MOTION_LOAD_OVERLOAD_NO_PROOF','window':w.get('id'),'load':load})
        elif load>=5 and not proof: issues.append({'type':'HIGH_LOAD_PREVIS_REQUIRED','window':w.get('id'),'load':load})
    return {'pass':not issues,'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file',nargs='?'); a=ap.parse_args(); d=json.load(open(a.file,encoding='utf-8')) if a.file else json.load(sys.stdin); out=lint(d); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
