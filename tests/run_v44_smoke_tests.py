#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def run(*args,capture=False):
    cmd=[sys.executable,*map(str,args)]; print('$',*map(str,args)); return subprocess.run(cmd,check=True,cwd=ROOT,text=True,capture_output=capture)
def main():
    run(ROOT/'validators/v44_architecture_lint.py','--root',ROOT,'--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/episode_state.schema.yaml',ROOT/'tests/fixtures/episode_state.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/shot_state.schema.yaml',ROOT/'tests/fixtures/shot_state.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/asset_registry.schema.yaml',ROOT/'tests/fixtures/asset_registry.conditioning.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'runtime/video_conditioning_runtime.schema.yaml',ROOT/'tests/fixtures/video_conditioning_runtime.valid.yaml','--json')
    for p in list((ROOT/'state').glob('*.schema.yaml'))+list((ROOT/'runtime').glob('*.schema.yaml')):
        Draft202012Validator.check_schema(yaml.safe_load(p.read_text(encoding='utf-8')))
    for p in list((ROOT/'controller').glob('*.yaml'))+list((ROOT/'adapters').rglob('*.yaml')):
        yaml.safe_load(p.read_text(encoding='utf-8'))
    # mandatory conditioning pass/fail
    run(ROOT/'validators/video_conditioning_lint.py','--runtime',ROOT/'tests/fixtures/video_conditioning_runtime.valid.yaml','--registry',ROOT/'tests/fixtures/asset_registry.conditioning.valid.yaml')
    bad=subprocess.run([sys.executable,str(ROOT/'validators/video_conditioning_lint.py'),'--runtime',str(ROOT/'tests/fixtures/video_conditioning_runtime.invalid_aux_primary.yaml'),'--registry',str(ROOT/'tests/fixtures/asset_registry.conditioning.valid.yaml')],cwd=ROOT,text=True,capture_output=True)
    assert bad.returncode==2 and 'ASSET_ROLE_ESCALATION_FAIL' in bad.stdout
    # @asset surface still enforced
    run(ROOT/'validators/asset_mention_lint.py','--prompt',ROOT/'tests/fixtures/prompt.asset_mentions.valid.txt','--runtime',ROOT/'tests/fixtures/reference_runtime.asset_mentions.valid.yaml')
    missing=subprocess.run([sys.executable,str(ROOT/'validators/asset_mention_lint.py'),'--prompt',str(ROOT/'tests/fixtures/prompt.asset_mentions.missing.txt'),'--runtime',str(ROOT/'tests/fixtures/reference_runtime.asset_mentions.valid.yaml')],cwd=ROOT,text=True,capture_output=True)
    assert missing.returncode==2 and 'MISSING_REQUIRED_ASSET_MENTION' in missing.stdout
    # no direct previs->video route
    wf=yaml.safe_load((ROOT/'controller/workflow_state_machine.yaml').read_text(encoding='utf-8'))
    assert not any(t.get('from')=='APPROVED_PREVIS_SET' and t.get('to')=='VIDEO_GENERATION_READY' for t in wf['transitions'])
    assert any(t.get('to')=='VIDEO_CONDITIONING_IN_PROGRESS' for t in wf['transitions'])
    # temporal shared semantics
    sys.path.insert(0,str(ROOT/'validators')); from temporal_scope import overlap
    assert overlap({'time_scope':'ENTRY'},{'time_scope':'LANDING'}) is False
    # deterministic tools
    fp=run(ROOT/'tools/state_fingerprint.py',ROOT/'tests/fixtures/episode_state.valid.yaml',capture=True).stdout.strip(); assert len(fp)==64
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); src=td/'source.bin'; dst=td/'project/assets/copy.bin'; pr=td/'project'; src.write_bytes(b'duanxian-v44-archive-test')
        rec=json.loads(run(ROOT/'tools/archive_asset.py',src,dst,'--project-root',pr,'--json',capture=True).stdout)
        assert rec['status']=='ARCHIVED' and rec['sha256_verification']=='PASS'
        assert hashlib.sha256(src.read_bytes()).hexdigest()==rec['target_sha256']
    print('V4.4 smoke tests: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
