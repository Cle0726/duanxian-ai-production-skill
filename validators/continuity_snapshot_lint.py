#!/usr/bin/env python3
import argparse, json
from temporal_integrity import validate_snapshot_path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('snapshot',nargs='?'); ap.add_argument('--snapshot',dest='snapshot_opt'); a=ap.parse_args()
    p=a.snapshot_opt or a.snapshot
    if not p:
        print(json.dumps({'pass':False,'issues':[{'type':'CONTINUITY_SNAPSHOT_PATH_REQUIRED'}]},ensure_ascii=False,indent=2)); return 2
    out=validate_snapshot_path(p); out.pop('snapshot',None)
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['pass'] else 2
if __name__=='__main__': raise SystemExit(main())
