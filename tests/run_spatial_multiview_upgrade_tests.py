#!/usr/bin/env python3
from __future__ import annotations
import subprocess, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent
FIX=ROOT/'tests'/'fixtures'/'v457'

def sh(cmd, expect=0):
    r=subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(r.stdout)
    if r.returncode!=expect:
        raise AssertionError(f"command failed {cmd} expected {expect} got {r.returncode}")

def load_yaml(p):
    return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def main():
    # schema parse
    for name in ['minor_human_canon_view_set.schema.yaml','prop_canon_view_set.schema.yaml','environment_visual_anchor_set.schema.yaml','spatial_continuity_state.schema.yaml','shot_boundary_continuity_contract.schema.yaml']:
        assert load_yaml(ROOT/'state'/name)
    # storyboard anonymity
    sh([sys.executable,'validators/storyboard_anonymity_lint.py','--registry',str(FIX/'storyboard_registry.valid.yaml')],0)
    sh([sys.executable,'validators/storyboard_anonymity_lint.py','--registry',str(FIX/'storyboard_registry.invalid.yaml')],2)
    # boundary contract
    sh([sys.executable,'validators/shot_boundary_continuity_lint.py','--contract',str(FIX/'boundary_contract.valid.yaml')],0)
    sh([sys.executable,'validators/shot_boundary_continuity_lint.py','--contract',str(FIX/'boundary_contract.invalid.yaml')],2)
    # view closure
    sh([sys.executable,'validators/view_closure_lint.py','--prop',str(FIX/'prop_view_set.valid.yaml')],0)
    sh([sys.executable,'validators/view_closure_lint.py','--env',str(FIX/'env_anchor_set.valid.yaml')],0)
    # route registry references
    route=(ROOT/'controller'/'route_registry.yaml').read_text(encoding='utf-8')
    for token in ['MINOR_HUMAN_CANON_VIEW_SET','PROP_CANON_VIEW_SET','ENV_VISUAL_ANCHOR_SET','SPATIAL_CONTINUITY_STATE','SHOT_BOUNDARY_CONTINUITY_CONTRACT','validators/storyboard_anonymity_lint.py','validators/shot_boundary_continuity_lint.py']:
        assert token in route, token
    print('ALL SPATIAL/MULTIVIEW UPGRADE TESTS PASSED')

if __name__=='__main__':
    main()
