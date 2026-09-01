#!/usr/bin/env python3
from __future__ import annotations
import subprocess,sys,tempfile,hashlib,json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def run(*args,capture=False):
    cmd=[sys.executable,*map(str,args)]; print('$',*map(str,args)); return subprocess.run(cmd,check=True,cwd=ROOT,text=True,capture_output=capture)
def fail_contains(args,needle):
    r=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==2, (r.returncode,r.stdout,r.stderr)
    assert needle in r.stdout, r.stdout

def main():
    run(ROOT/'validators/yaml_duplicate_key_lint.py',ROOT/'controller',ROOT/'state',ROOT/'runtime',ROOT/'adapters',ROOT/'tests/fixtures')
    run(ROOT/'validators/v44_architecture_lint.py','--root',ROOT,'--json')
    run(ROOT/'validators/v45_architecture_lint.py','--root',ROOT,'--json')
    run(ROOT/'validators/v451_architecture_lint.py','--root',ROOT,'--json')
    for p in list((ROOT/'state').glob('*.schema.yaml'))+list((ROOT/'runtime').glob('*.schema.yaml')):
        Draft202012Validator.check_schema(yaml.safe_load(p.read_text(encoding='utf-8')))
    # Spatial canon schema + semantic proof
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/spatial_canon.schema.yaml',ROOT/'tests/fixtures/spatial_canon.clue_reveal.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'runtime/spatial_canon_runtime.schema.yaml',ROOT/'tests/fixtures/spatial_canon_runtime.valid.yaml','--json')
    run(ROOT/'validators/spatial_canon_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.clue_reveal.valid.yaml','--relation-graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml')
    fail_contains([ROOT/'validators/spatial_canon_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.clue_reveal.invalid_missing_sightline.yaml','--relation-graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml'],'SHOT_RELATION_SPATIAL')
    # Relation schemas + phases
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/shot_relation_graph.schema.yaml',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/visual_asset_obligation.schema.yaml',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--json')
    run(ROOT/'validators/shot_relation_asset_obligation_lint.py','--graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--obligations',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--phase','planning')
    run(ROOT/'validators/shot_relation_asset_obligation_lint.py','--graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--obligations',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--phase','freeze','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.clue_reveal.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.clue_reveal.valid.yaml')
    run(ROOT/'validators/shot_relation_asset_obligation_lint.py','--graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--obligations',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--phase','conditioning','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.clue_reveal.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.clue_reveal.valid.yaml','--conditioning-runtime',ROOT/'tests/fixtures/video_conditioning_runtime.clue_reveal.valid.yaml')
    # Fake proof / missing identity / ghost pair must fail
    fail_contains([ROOT/'validators/shot_relation_asset_obligation_lint.py','--graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.invalid_fake_proof.yaml','--obligations',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--phase','planning'],'SOURCE_VISUAL_FACT_MISSING')
    fail_contains([ROOT/'validators/shot_relation_asset_obligation_lint.py','--graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--obligations',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.invalid_missing_identity.yaml','--phase','planning'],'DESTINATION_IDENTITY_ASSET_OBLIGATION_MISSING')
    fail_contains([ROOT/'validators/shot_relation_asset_obligation_lint.py','--graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--obligations',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--phase','conditioning','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.clue_reveal.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.clue_reveal.valid.yaml','--conditioning-runtime',ROOT/'tests/fixtures/video_conditioning_runtime.clue_reveal.invalid_ghost_pair.yaml'],'CUT_PAIR_EXIT_NOT_BOUND_TO_OBLIGATION')
    # Conditioning strategy closure
    run(ROOT/'validators/state_schema_lint.py',ROOT/'runtime/video_conditioning_runtime.schema.yaml',ROOT/'tests/fixtures/video_conditioning_runtime.valid.yaml','--json')
    run(ROOT/'validators/video_conditioning_lint.py','--runtime',ROOT/'tests/fixtures/video_conditioning_runtime.valid.yaml','--registry',ROOT/'tests/fixtures/asset_registry.conditioning.valid.yaml')
    fail_contains([ROOT/'validators/video_conditioning_lint.py','--runtime',ROOT/'tests/fixtures/video_conditioning_runtime.invalid_first_target_missing_target.yaml','--registry',ROOT/'tests/fixtures/asset_registry.conditioning.valid.yaml'],'CONDITIONING_STRATEGY_FRAME_GAP')
    # Clean storyboard contract
    run(ROOT/'validators/clean_storyboard_contract_lint.py','--registry',ROOT/'tests/fixtures/asset_registry.storyboard_clean.valid.yaml')
    fail_contains([ROOT/'validators/clean_storyboard_contract_lint.py','--registry',ROOT/'tests/fixtures/asset_registry.storyboard_clean.invalid_annotated.yaml'],'STORYBOARD_PIXEL_ANNOTATION_FAIL')
    # Grid assembler adds no text; deterministic dimension check.
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); a=td/'a.png'; b=td/'b.png'; out=td/'grid.png'
        Image.new('RGB',(32,18),'white').save(a); Image.new('RGB',(32,18),'black').save(b)
        subprocess.run([sys.executable,str(ROOT/'tools/storyboard_grid_assembler.py'),str(a),str(b),'--output',str(out),'--columns','2','--gap','4'],check=True,cwd=ROOT)
        assert Image.open(out).size==(68,18)
    # Generation @asset mention still enforced.
    run(ROOT/'validators/asset_mention_lint.py','--prompt',ROOT/'tests/fixtures/prompt.asset_mentions.valid.txt','--runtime',ROOT/'tests/fixtures/reference_runtime.asset_mentions.valid.yaml')
    fail_contains([ROOT/'validators/asset_mention_lint.py','--prompt',ROOT/'tests/fixtures/prompt.asset_mentions.missing.txt','--runtime',ROOT/'tests/fixtures/reference_runtime.asset_mentions.valid.yaml'],'MISSING_REQUIRED_ASSET_MENTION')
    print('V4.5.1 smoke tests: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
