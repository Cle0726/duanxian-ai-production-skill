#!/usr/bin/env python3
from __future__ import annotations
import subprocess,sys,tempfile,copy
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'tests/fixtures'

def run(*args):
    r=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,text=True,capture_output=True)
    if r.returncode!=0:
        print(r.stdout); print(r.stderr,file=sys.stderr); raise AssertionError((args,r.returncode))
    return r.stdout

def fail_contains(args,*needles):
    r=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==2,(r.returncode,r.stdout,r.stderr,args)
    for n in needles: assert n in r.stdout,(n,r.stdout)
    return r.stdout

def dump_tmp(td,name,obj):
    p=Path(td)/name; p.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False),encoding='utf-8'); return p

def base_args(rc=None,sp=None,reg=None,ve=None):
    args=[ROOT/'validators/everyday_realism_lint.py','--realism-contract',rc or F/'realism_contract.wagon.v456.valid.yaml','--spatial-canon',sp or F/'spatial_canon.realism_wagon.v456.valid.yaml','--asset-registry',reg or F/'asset_registry.realism_wagon.v456.valid.yaml']
    if ve: args += ['--visual-evidence',ve]
    return args

def main():
    # Static architecture + schema validity.
    run(ROOT/'validators/yaml_duplicate_key_lint.py',ROOT/'controller',ROOT/'state',ROOT/'runtime',ROOT/'adapters',F)
    for lint in ['v44_architecture_lint.py','v45_architecture_lint.py','v451_architecture_lint.py','v452_architecture_lint.py','v453_architecture_lint.py','v454_architecture_lint.py','v455_architecture_lint.py','v456_architecture_lint.py']:
        run(ROOT/'validators'/lint,'--root',ROOT,'--json')
    for p in list((ROOT/'state').glob('*.schema.yaml'))+list((ROOT/'runtime').glob('*.schema.yaml')):
        Draft202012Validator.check_schema(yaml.safe_load(p.read_text(encoding='utf-8')))
    for schema,fixture in [
      ('state/spatial_canon.schema.yaml','spatial_canon.realism_wagon.v456.valid.yaml'),
      ('state/realism_contract.schema.yaml','realism_contract.wagon.v456.valid.yaml'),
      ('state/asset_registry.schema.yaml','asset_registry.realism_wagon.v456.valid.yaml'),
      ('state/visual_evidence.schema.yaml','visual_evidence.realism_wagon.v456.valid.yaml'),
      ('runtime/video_runtime.schema.yaml','video_runtime.realism.v456.valid.yaml'),
      ('runtime/qc_runtime.schema.yaml','qc_runtime.video_realism.v456.valid.yaml')]:
        run(ROOT/'validators/state_schema_lint.py',ROOT/schema,F/fixture,'--json')

    # P0-1: valid reusable VEHICLE + VEHICLE_LAYOUT must not false-fail.
    run(ROOT/'validators/spatial_canon_lint.py','--spatial-canon',F/'spatial_canon.realism_wagon.v456.valid.yaml')

    # Happy lifecycle: DRAFT may pass planning QC, but cannot enter build/freeze until LOCKED.
    with tempfile.TemporaryDirectory() as td:
        rc=yaml.safe_load((F/'realism_contract.wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        for c in rc['contracts']: c['status']='DRAFT'
        p=dump_tmp(td,'draft.yaml',rc)
        run(*base_args(rc=p),'--phase','planning')
        fail_contains([*base_args(rc=p),'--phase','build'],'REALISM_CONTRACT_NOT_LOCKED')

    # Happy V4.5.6 freeze.
    run(*base_args(ve=F/'visual_evidence.realism_wagon.v456.valid.yaml'),'--phase','freeze')

    # P0-2: ordinary image cannot bypass Reality by omitting contract binding.
    with tempfile.TemporaryDirectory() as td:
        reg=yaml.safe_load((F/'asset_registry.realism_wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        a=next(x for x in reg['assets'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        a['realism_contract_ids']=[]
        p=dump_tmp(td,'no_binding.yaml',reg)
        fail_contains([*base_args(reg=p),'--phase','build'],'REALISM_ASSET_CONTRACT_BINDING_MISSING')

    # Missing applicability itself is a hard bypass attempt.
    with tempfile.TemporaryDirectory() as td:
        reg=yaml.safe_load((F/'asset_registry.realism_wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        a=next(x for x in reg['assets'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        a.pop('realism_applicability',None)
        p=dump_tmp(td,'no_applicability.yaml',reg)
        fail_contains([*base_args(reg=p),'--phase','build'],'REALISM_APPLICABILITY_UNDECLARED')

    # P0-3: an asset cannot steal another asset's scoped exception by naming its id.
    with tempfile.TemporaryDirectory() as td:
        rc=yaml.safe_load((F/'realism_contract.wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        event=next(c for c in rc['contracts'] if c['contract_id']=='RC_WAGON_01')
        event['exception_scopes']=[{'exception_id':'EX_COMBAT_OTHER','exception_type':'COMBAT','asset_ids':['SOME_OTHER_ASSET'],'allowed_categories':['HUMAN_ERGONOMICS'],'reason':'REGRESSION scope belongs elsewhere','approval_ref':'APR_EX'}]
        rp=dump_tmp(td,'rc_exception.yaml',rc)
        reg=yaml.safe_load((F/'asset_registry.realism_wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        a=next(x for x in reg['assets'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        a['realism_applicability']='SCOPED_EXCEPTION'; a['realism_exception_ids']=['EX_COMBAT_OTHER']
        regp=dump_tmp(td,'reg_exception.yaml',reg)
        ve=yaml.safe_load((F/'visual_evidence.realism_wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        rec=next(x for x in ve['records'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        rec['observed']['realism']['category_verdicts']['HUMAN_ERGONOMICS']='FAIL'
        vep=dump_tmp(td,'ve_exception.yaml',ve)
        fail_contains([*base_args(rc=rp,reg=regp,ve=vep),'--phase','freeze'],'REALISM_EXCEPTION_SCOPE_MISMATCH','HUMAN_ERGONOMICS_FAIL')

    # P0-6: fine-grained driver visibility FAIL beats a coarse VEHICLE_REALISM PASS.
    with tempfile.TemporaryDirectory() as td:
        ve=yaml.safe_load((F/'visual_evidence.realism_wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        rec=next(x for x in ve['records'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        rec['observed']['realism']['environment']['driver_forward_visibility']='FAIL'
        rec['observed']['realism']['category_verdicts']['VEHICLE_REALISM']='PASS'
        p=dump_tmp(td,'driver_visibility_fail.yaml',ve)
        fail_contains([*base_args(ve=p),'--phase','freeze'],'VEHICLE_DRIVER_FORWARD_VISIBILITY_FAIL','REALISM_SUMMARY_CONTRADICTS_OBSERVATION')

    # Access path contract must point to a real Spatial Canon path.
    with tempfile.TemporaryDirectory() as td:
        rc=yaml.safe_load((F/'realism_contract.wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        next(c for c in rc['contracts'] if c['contract_id']=='RC_WAGON_ENV')['environment_requirements']['required_access_path_ids'].append('GHOST_PATH')
        p=dump_tmp(td,'ghost_path.yaml',rc)
        fail_contains([*base_args(rc=p),'--phase','planning'],'REALISM_REQUIRED_ACCESS_PATH_UNKNOWN')

    # Specialized reality basis cannot claim REFERENCE_REQUIRED without verified provenance.
    with tempfile.TemporaryDirectory() as td:
        rc=yaml.safe_load((F/'realism_contract.wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        c=next(c for c in rc['contracts'] if c['contract_id']=='RC_WAGON_ENV')
        c['reality_basis']={'basis_type':'HISTORICAL_REFERENCE','reference_requirement':'REFERENCE_REQUIRED','verification_status':'PENDING','reference_refs':[],'rationale':'test'}
        p=dump_tmp(td,'basis_missing.yaml',rc)
        fail_contains([*base_args(rc=p),'--phase','planning'],'REALITY_REFERENCE_NOT_VERIFIED','REALITY_REFERENCE_REQUIRED_BUT_MISSING')

    # Stage 04/05 image gates actually execute the same Reality Evidence logic.
    with tempfile.TemporaryDirectory() as td:
        reg=yaml.safe_load((F/'asset_registry.realism_wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        ve=yaml.safe_load((F/'visual_evidence.realism_wagon.v456.valid.yaml').read_text(encoding='utf-8'))
        src=next(x for x in reg['assets'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        srcve=next(x for x in ve['records'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        for stage,phase,aid in [('STORYBOARD','storyboard','ASSET_STORY_REALISM'),('VIDEO_CONDITIONING','conditioning','ASSET_COND_REALISM')]:
            a=copy.deepcopy(src); a['asset_id']=aid; a['fingerprint']='hash-'+aid; a['cascade_stage']=stage; a['status']='QC_PASS_WAITING_APPROVAL'; a['visual_evidence_ref']='VE_'+aid; a['visual_evidence_source_fingerprint']=a['fingerprint']
            rec=copy.deepcopy(srcve); rec['evidence_id']='VE_'+aid; rec['asset_id']=aid; rec['source_fingerprint']=a['fingerprint']
            reg2=copy.deepcopy(reg); reg2['assets'].append(a); ve2=copy.deepcopy(ve); ve2['records'].append(rec)
            rp=dump_tmp(td,f'reg_{phase}.yaml',reg2); vp=dump_tmp(td,f've_{phase}.yaml',ve2)
            run(*base_args(reg=rp,ve=vp),'--phase',phase)
            rec['observed']['realism']['category_verdicts']['HUMAN_ERGONOMICS']='FAIL'; ve2['records'][-1]=rec; vp=dump_tmp(td,f've_{phase}_bad.yaml',ve2)
            fail_contains([*base_args(reg=rp,ve=vp),'--phase',phase],'HUMAN_ERGONOMICS_FAIL')

    # Actual video take requires fingerprint-matched multimodal/human reality evidence.
    run(ROOT/'validators/video_realism_qc_lint.py','--realism-contract',F/'realism_contract.wagon.v456.valid.yaml','--video-runtime',F/'video_runtime.realism.v456.valid.yaml','--qc-runtime',F/'qc_runtime.video_realism.v456.valid.yaml')
    with tempfile.TemporaryDirectory() as td:
        qc=yaml.safe_load((F/'qc_runtime.video_realism.v456.valid.yaml').read_text(encoding='utf-8'))
        qc['video_realism_evidence']['video_take_fingerprint']='stale-video'
        p=dump_tmp(td,'qc_stale.yaml',qc)
        fail_contains([ROOT/'validators/video_realism_qc_lint.py','--realism-contract',F/'realism_contract.wagon.v456.valid.yaml','--video-runtime',F/'video_runtime.realism.v456.valid.yaml','--qc-runtime',p],'VIDEO_REALISM_EVIDENCE_STALE')

    print('V4.5.6 adversarial tests: PASS')

if __name__=='__main__': raise SystemExit(main())
