#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, json, tempfile, yaml
ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable

def run(cmd,expect=0):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if p.returncode!=expect:
        raise AssertionError(f"cmd={cmd}\nreturn={p.returncode}\nstdout={p.stdout}\nstderr={p.stderr}")
    return p

# schemas parse and validate
run([PY,'validators/state_schema_lint.py','runtime/director_runtime.schema.yaml','tests/fixtures/director_runtime.perception.valid.yaml','--json'])
run([PY,'validators/state_schema_lint.py','state/editorial_plan.schema.yaml','tests/fixtures/editorial_plan.valid.yaml','--json'])

# valid perception + editorial plan
p=run([PY,'validators/director_perception_lint.py','--director-runtime','tests/fixtures/director_runtime.perception.valid.yaml','--editorial-plan','tests/fixtures/editorial_plan.valid.yaml'])
out=json.loads(p.stdout)
assert out['pass'] is True and out['error_count']==0

# close-up without information gain/spatial cost + force overload must hard fail
p=run([PY,'validators/director_perception_lint.py','--director-runtime','tests/fixtures/director_runtime.perception.invalid_closeup.yaml'],expect=2)
out=json.loads(p.stdout); kinds={x['type'] for x in out['findings']}
assert 'CLOSEUP_JUSTIFICATION_WEAK' in kinds
assert 'CLOSEUP_SPATIAL_COST_GAP' in kinds
assert 'VISUAL_FORCE_STACK_OVERLOAD' in kinds

# historical bias is warning only; it must never force gratuitous variation
p=run([PY,'validators/director_perception_lint.py','--director-runtime','tests/fixtures/director_runtime.perception.drift_warning.yaml'])
out=json.loads(p.stdout); kinds={x['type'] for x in out['findings']}
assert out['pass'] is True
assert 'SHOT_SCALE_BIAS' in kinds
assert 'CAMERA_ETHICS_BIAS' in kinds
assert 'COMPOSITION_PATTERN_COLLAPSE' in kinds

# causal sequence must resist shuffle
p=run([PY,'validators/editorial_plan_lint.py','--plan','tests/fixtures/editorial_plan.valid.yaml'])
out=json.loads(p.stdout); assert out['pass'] is True
bad=yaml.safe_load((ROOT/'tests/fixtures/editorial_plan.valid.yaml').read_text(encoding='utf-8'))
bad['shuffle_test']={'status':'FAIL','counterfactual_swap_breaks_sequence':False,'dependency_reasons':[],'rationale':'顺序可换'}
with tempfile.TemporaryDirectory() as td:
    bp=Path(td)/'bad.yaml'; bp.write_text(yaml.safe_dump(bad,allow_unicode=True,sort_keys=False),encoding='utf-8')
    p=run([PY,'validators/editorial_plan_lint.py','--plan',str(bp)],expect=2)
    o=json.loads(p.stdout); ks={x['type'] for x in o['findings']}
    assert 'SEQUENCE_SHUFFLE_TEST_FAIL' in ks and 'SEQUENCE_SHUFFLE_TEST_GAP' in ks

# grammar history updater is deterministic state projection, not creative invention
with tempfile.TemporaryDirectory() as td:
    outp=Path(td)/'director.yaml'
    run([PY,'tools/shot_grammar_history.py','--director-runtime','tests/fixtures/director_runtime.perception.valid.yaml','--editorial-plan','tests/fixtures/editorial_plan.valid.yaml','--output',str(outp)])
    d=yaml.safe_load(outp.read_text(encoding='utf-8'))
    ids=[x.get('shot_id') for x in d.get('shot_grammar_history',[])]
    assert {'SH01','SH02','SH03'}.issubset(set(ids))

# control-plane closure
route=yaml.safe_load((ROOT/'controller/route_registry.yaml').read_text(encoding='utf-8'))
wf=yaml.safe_load((ROOT/'controller/workflow_state_machine.yaml').read_text(encoding='utf-8'))
auth=yaml.safe_load((ROOT/'controller/authority_registry.yaml').read_text(encoding='utf-8'))
gpr=yaml.safe_load((ROOT/'controller/gate_producer_registry.yaml').read_text(encoding='utf-8'))
r=route['routes']['STAGE_02B_DIRECTOR_ARCHITECTURE']
assert 'validators/director_perception_lint.py' in r.get('validators',[])
assert 'DIRECTOR_PERCEPTION_PASS' in r.get('produces_fields',[])
t08=next(x for x in wf['transitions'] if x.get('id')=='T08_DIRECTOR_CORE')
assert 'DIRECTOR_PERCEPTION_PASS' in t08.get('requires',[])
assert gpr['producers']['DIRECTOR_PERCEPTION_PASS']['owner']=='validators/director_perception_lint.py'
assert auth['authorities']['camera_ethics_attention_flow']['owner']=='templates/cinematography_grammar.md'
assert auth['authorities']['editorial_information_sequence_logic']['owner']=='templates/editorial_grammar_engine.md'

# source authority tokens must exist
checks={
 'templates/director_intelligence_core.md':['UNRESOLVED_STATE','RELATIONAL_PRESSURE','Creative Drift Telemetry'],
 'templates/cinematography_grammar.md':['Camera Ethics','Attention Flow','Shot Scale Justification','Visual Salience Budget'],
 'templates/editorial_grammar_engine.md':['Sequence Shuffle Test','Editorial Weight','Breathing Function'],
 'templates/prompt_compiler.md':['Style Escalation Policy','Execution Density ≠ Visual Salience Density'],
 'templates/storyboard_prompt_template.md':['Perception Proof Gate','Visual Salience Budget'],
}
for rel,toks in checks.items():
    txt=(ROOT/rel).read_text(encoding='utf-8')
    for tok in toks: assert tok in txt, (rel,tok)

print('DIRECTOR PERCEPTION UPGRADE TESTS PASS')
