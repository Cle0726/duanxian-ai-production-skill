#!/usr/bin/env python3
from __future__ import annotations
import subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent
PYTHON=sys.executable

def run(cmd,expect=0):
    cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print(cp.stdout)
    if cp.stderr: print(cp.stderr)
    if cp.returncode!=expect: raise AssertionError((cmd,cp.returncode,expect))
    return cp

print('SECTION_1_DEFAULT_PROFILE')
run([PYTHON,'validators/all_round_reference_profile_lint.py','--json'])

print('SECTION_2_RUNTIME_SCHEMA_SUPPORT')
with tempfile.TemporaryDirectory() as td:
    src=Path(td)/'src.yaml'; src.write_text('x: 1\n',encoding='utf-8')
    proj=Path(td)/'projection.yaml'
    proj.write_text(yaml.safe_dump({'host_capability':{
        'resolved_profile':'MULTIMODAL_ALL_ROUND_REFERENCE',
        'image_generation':'AVAILABLE','video_generation':'AVAILABLE',
        'reference_transport':'NAMED_ASSET_MENTION',
        'reference_capability_class':'MULTIMODAL_ALL_ROUND_REFERENCE',
        'supported_reference_media':['TEXT','IMAGE','AUDIO'],
        'role_aware_reference_assignment':True}},sort_keys=False),encoding='utf-8')
    out=Path(td)/'runtime.yaml'
    run([PYTHON,'tools/runtime_compiler.py','--runtime-type','GENERATION_RUNTIME','--source',str(src),'--projection',str(proj),'--output',str(out)])
    data=yaml.safe_load(out.read_text(encoding='utf-8'))
    assert data['host_capability']['reference_capability_class']=='MULTIMODAL_ALL_ROUND_REFERENCE'
    assert set(data['host_capability']['supported_reference_media'])=={'TEXT','IMAGE','AUDIO'}
    assert 'VIDEO' not in data['host_capability']['supported_reference_media']

print('SECTION_3_BACKWARD_COMPATIBILITY')
hp=yaml.safe_load((ROOT/'adapters/generation/host_profiles.yaml').read_text(encoding='utf-8'))
assert 'NAMED_ASSET_PLATFORM' in hp['profiles']
assert 'SEEDANCE_NAMED_ASSET_PLATFORM' in hp['profiles']
assert hp['profiles']['SEEDANCE_NAMED_ASSET_PLATFORM']['reference_capability_class']=='MULTIMODAL_ALL_ROUND_REFERENCE'
assert 'VIDEO' not in hp['profiles']['MULTIMODAL_ALL_ROUND_REFERENCE']['supported_reference_media']
assert hp['profiles']['MULTIMODAL_ALL_ROUND_REFERENCE']['reference_video_policy']=='FORBIDDEN_QUOTA_COST'
assert hp['profiles']['MULTIMODAL_ALL_ROUND_REFERENCE']['supports_audio_reference'] is True

print('ALL-ROUND REFERENCE DEFAULT TESTS PASS')
