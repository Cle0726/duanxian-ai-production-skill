#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, tempfile, yaml

ROOT=Path(__file__).resolve().parents[1]
PYTHON=sys.executable
LEGACY={'DERIVED_COVERAGE_VIEW','EVENT_NODE_VIEW','RECIPROCAL_COVERAGE_VIEW','PREDICTIVE_COVERAGE_VIEW','SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW','LOCATION_IDENTITY_VIEW'}

def run(args, expect=0):
    p=subprocess.run([PYTHON,*map(str,args)],cwd=ROOT,text=True,capture_output=True,timeout=20)
    if p.returncode!=expect:
        print('$',' '.join(map(str,args))); print(p.stdout); print(p.stderr,file=sys.stderr)
        raise SystemExit(f'expected {expect}, got {p.returncode}')
    return p.stdout

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def write(p,obj): Path(p).write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False),encoding='utf-8')

# 1. Active templates cannot create legacy physical coverage types.
for p in (ROOT/'templates').glob('*.md'):
    text=p.read_text(encoding='utf-8')
    bad=sorted(t for t in LEGACY if t in text)
    assert not bad, (p,bad)

# 2. Current generic ENVIRONMENT_COVERAGE remains valid in the Virtual Set gate.
with tempfile.TemporaryDirectory() as td:
    reg=load(ROOT/'tests/fixtures/asset_registry.virtual_set.valid.yaml')
    for a in reg['assets']:
        if a.get('asset_type')=='RECIPROCAL_COVERAGE_VIEW':
            a['asset_type']='ENVIRONMENT_COVERAGE'
            a.setdefault('derivation',{})['coverage_reason_codes']=['RECIPROCAL','REQUIRED_VIEW']
    rp=Path(td)/'registry.yaml'; write(rp,reg)
    run(['validators/state_schema_lint.py','state/asset_registry.schema.yaml',rp,'--json'])
    run(['validators/virtual_set_asset_lint.py','--spatial-canon','tests/fixtures/spatial_canon.virtual_set.valid.yaml','--asset-registry',rp,'--phase','freeze'])

# 3. Relation-driven clue/visibility/identity obligations work with generic coverage + reason codes.
with tempfile.TemporaryDirectory() as td:
    ob=load(ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml')
    reg=load(ROOT/'tests/fixtures/asset_registry.clue_reveal.valid.yaml')
    for o in ob['obligations']:
        if o['obligation_type']=='SCENE_CLUE_VIEW':
            o['obligation_type']='ENVIRONMENT_COVERAGE'; o['coverage_reason_codes']=['CLUE_REVEAL','LOCATION_VISIBILITY']
        elif o['obligation_type']=='LOCATION_IDENTITY_VIEW':
            o['obligation_type']='ENVIRONMENT_COVERAGE'; o['coverage_reason_codes']=['LOCATION_IDENTITY']
    for a in reg['assets']:
        if a['asset_type']=='SCENE_CLUE_VIEW':
            a['asset_type']='ENVIRONMENT_COVERAGE'; a.setdefault('derivation',{})['coverage_reason_codes']=['CLUE_REVEAL','LOCATION_VISIBILITY']
        elif a['asset_type']=='LOCATION_IDENTITY_VIEW':
            a['asset_type']='ENVIRONMENT_COVERAGE'; a.setdefault('derivation',{})['coverage_reason_codes']=['LOCATION_IDENTITY']
    op=Path(td)/'obligations.yaml'; rp=Path(td)/'registry.yaml'; write(op,ob); write(rp,reg)
    run(['validators/state_schema_lint.py','state/visual_asset_obligation.schema.yaml',op,'--json'])
    run(['validators/state_schema_lint.py','state/asset_registry.schema.yaml',rp,'--json'])
    run(['validators/shot_relation_asset_obligation_lint.py','--graph','tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--obligations',op,'--phase','freeze','--spatial-canon','tests/fixtures/spatial_canon.clue_reveal.valid.yaml','--asset-registry',rp])

# 4. Compatibility remains: legacy fixtures are readable by migration validators.
run(['validators/virtual_set_asset_lint.py','--spatial-canon','tests/fixtures/spatial_canon.virtual_set.valid.yaml','--asset-registry','tests/fixtures/asset_registry.virtual_set.valid.yaml','--phase','freeze'])
run(['validators/shot_relation_asset_obligation_lint.py','--graph','tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--obligations','tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--phase','freeze','--spatial-canon','tests/fixtures/spatial_canon.clue_reveal.valid.yaml','--asset-registry','tests/fixtures/asset_registry.clue_reveal.valid.yaml'])

# 4B. V4.5.7 production completeness does not treat legacy obligation names as current targets; they must migrate first.
with tempfile.TemporaryDirectory() as td:
    base={'schema_version':1,'skill_version':'4.5.7','episode_id':'EP','environments':[],'minor_humans':[],'actor_authority_index':[],'crowd_archetype_set_refs':[],'status':'FROZEN'}
    perf={'schema_version':1,'skill_version':'4.5.7','episode_id':'EP','requirements':[],'status':'FROZEN'}
    fx={'schema_version':1,'skill_version':'4.5.7','episode_id':'EP','effects':[],'status':'FROZEN'}
    obs={'schema_version':3,'skill_version':'4.5.7','episode_id':'EP','status':'COMPLETE','obligations':[{'obligation_id':'OLD1','trigger_type':'SHOT','shot_ids':['SH1'],'obligation_type':'SCENE_CLUE_VIEW','fulfill_by':'STAGE_03_FREEZE','reason':'legacy','fulfillment_asset_ids':[],'status':'FULFILLED','waiver_policy':'NON_WAIVABLE','proof_status':'PASS'}]}
    reg={'schema_version':7,'skill_version':'4.5.7','assets':[]}
    paths=[]
    for name,obj in [('base',base),('perf',perf),('fx',fx),('obs',obs),('reg',reg)]:
        q=Path(td)/f'{name}.yaml'; write(q,obj); paths.append(q)
    out=run(['validators/asset_library_completeness_lint.py','--base-visual-manifest',paths[0],'--performance-requirements',paths[1],'--narrative-fx-manifest',paths[2],'--obligations',paths[3],'--asset-registry',paths[4],'--phase','freeze'],expect=2)
    assert 'LEGACY_COVERAGE_OBLIGATION_REQUIRES_MIGRATION' in out

# 4C. Compatibility validators accept old-version legacy registries, but the same physical types are rejected once the registry declares 4.5.7.
with tempfile.TemporaryDirectory() as td:
    reg=load(ROOT/'tests/fixtures/asset_registry.virtual_set.valid.yaml'); reg['skill_version']='4.5.7'; rp=Path(td)/'legacy_as_current.yaml'; write(rp,reg)
    out=run(['validators/virtual_set_asset_lint.py','--spatial-canon','tests/fixtures/spatial_canon.virtual_set.valid.yaml','--asset-registry',rp,'--phase','freeze'],expect=2)
    assert 'LEGACY_COVERAGE_ASSET_REQUIRES_MIGRATION' in out

# 5. But a new 4.5.7 Generation Job cannot create a legacy physical coverage type.
with tempfile.TemporaryDirectory() as td:
    job=load(ROOT/'tests/fixtures/v457/generation_job.character.valid.yaml')
    job['skill_version']='4.5.7'; job['target_asset_type']='EVENT_NODE_VIEW'
    jp=Path(td)/'job.yaml'; write(jp,job)
    out=run(['validators/generation_job_binding_lint.py','--job',jp,'--registry','tests/fixtures/v457/asset_registry.lineage_color.valid.yaml','--json'],expect=1)
    assert 'LEGACY_COVERAGE_TYPE_NEW_PRODUCTION' in out

print('V4.5.7 coverage migration tests: PASS')
