#!/usr/bin/env python3
from __future__ import annotations
import subprocess,sys,tempfile,json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

def run(*args):
    print('$',*map(str,args)); return subprocess.run([sys.executable,*map(str,args)],check=True,cwd=ROOT,text=True)

def fail_contains(args,needle):
    r=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==2,(r.returncode,r.stdout,r.stderr); assert needle in r.stdout,(needle,r.stdout)

def main():
    run(ROOT/'validators/yaml_duplicate_key_lint.py',ROOT/'controller',ROOT/'state',ROOT/'runtime',ROOT/'adapters',ROOT/'tests/fixtures')
    for lint in ['v44_architecture_lint.py','v45_architecture_lint.py','v451_architecture_lint.py','v452_architecture_lint.py','v453_architecture_lint.py','v454_architecture_lint.py','v455_architecture_lint.py']:
        run(ROOT/'validators'/lint,'--root',ROOT,'--json')
    for p in list((ROOT/'state').glob('*.schema.yaml'))+list((ROOT/'runtime').glob('*.schema.yaml')):
        Draft202012Validator.check_schema(yaml.safe_load(p.read_text(encoding='utf-8')))
    for schema,fixture in [
        ('state/spatial_canon.schema.yaml','tests/fixtures/spatial_canon.realism_wagon.valid.yaml'),
        ('state/realism_contract.schema.yaml','tests/fixtures/realism_contract.wagon.valid.yaml'),
        ('state/asset_registry.schema.yaml','tests/fixtures/asset_registry.realism_wagon.valid.yaml'),
        ('state/visual_evidence.schema.yaml','tests/fixtures/visual_evidence.realism_wagon.valid.yaml')]:
        run(ROOT/'validators/state_schema_lint.py',ROOT/schema,ROOT/fixture,'--json')
    base=[ROOT/'validators/everyday_realism_lint.py','--realism-contract',ROOT/'tests/fixtures/realism_contract.wagon.valid.yaml','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.realism_wagon.valid.yaml']
    run(*base,'--phase','planning')
    run(*base,'--phase','build')
    run(*base,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.valid.yaml','--phase','freeze')
    fail_contains([*base,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.invalid_extra_person.yaml','--phase','freeze'],'CAST_COUNT_MISMATCH')
    fail_contains([*base,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.invalid_wrong_seat.yaml','--phase','freeze'],'CHARACTER_ZONE_ASSIGNMENT_FAIL')
    fail_contains([*base,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.invalid_vehicle_drift.yaml','--phase','freeze'],'VEHICLE_FUNCTIONAL_LAYOUT_DRIFT')
    # If the spatial/realism plan itself was derived rather than explicit Source truth, do not blindly canonize it.
    with tempfile.TemporaryDirectory() as td:
        rc=yaml.safe_load((ROOT/'tests/fixtures/realism_contract.wagon.valid.yaml').read_text(encoding='utf-8'))
        rc['contracts'][0]['source_fact_class']='DERIVED_REALISTIC_RESOLUTION'
        derived=Path(td)/'derived_contract.yaml'; derived.write_text(yaml.safe_dump(rc,allow_unicode=True,sort_keys=False),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ROOT/'validators/everyday_realism_lint.py'),'--realism-contract',str(derived),'--spatial-canon',str(ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml'),'--asset-registry',str(ROOT/'tests/fixtures/asset_registry.realism_wagon.valid.yaml'),'--visual-evidence',str(ROOT/'tests/fixtures/visual_evidence.realism_wagon.invalid_vehicle_drift.yaml'),'--phase','freeze'],cwd=ROOT,text=True,capture_output=True)
        assert r.returncode==2 and 'REALISM_CONTRACT_OR_ASSET_EXECUTION' in r.stdout and 'COMPARE_DERIVED_CONTRACT_WITH_SOURCE_AND_REAL_WORLD_FUNCTION' in r.stdout,(r.returncode,r.stdout,r.stderr)
    fail_contains([*base,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.invalid_missing_realism.yaml','--phase','freeze'],'REALISM_VISUAL_EVIDENCE_FIELDS_MISSING')
    bad_contract=[ROOT/'validators/everyday_realism_lint.py','--realism-contract',ROOT/'tests/fixtures/realism_contract.wagon.invalid_unscoped_exception.yaml','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.realism_wagon.valid.yaml','--phase','planning']
    fail_contains(bad_contract,'REALISM_EXCEPTION_UNSCOPED')
    # Scoped combat exception may waive only human-ergonomic category for this asset.
    ex=[ROOT/'validators/everyday_realism_lint.py','--realism-contract',ROOT/'tests/fixtures/realism_contract.wagon.scoped_combat_exception.yaml','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.realism_wagon.valid.yaml']
    run(*ex,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.exception_human_only.yaml','--phase','freeze')
    fail_contains([*ex,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.invalid_vehicle_drift.yaml','--phase','freeze'],'VEHICLE_FUNCTIONAL_LAYOUT_DRIFT')
    # Vehicle layout is a first-class planning diagram and can be deterministically rendered.
    run(ROOT/'validators/virtual_set_asset_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.realism_wagon.valid.yaml','--phase','spatial')
    run(ROOT/'validators/required_view_realization_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.realism_wagon.valid.yaml','--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.valid.yaml','--phase','freeze')
    # Correct camera view must not bypass its Everyday Realism Contract.
    with tempfile.TemporaryDirectory() as td:
        reg=yaml.safe_load((ROOT/'tests/fixtures/asset_registry.realism_wagon.valid.yaml').read_text(encoding='utf-8'))
        target=next(x for x in reg['assets'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        target['realism_contract_ids']=[]
        bad=Path(td)/'registry.no_realism_binding.yaml'; bad.write_text(yaml.safe_dump(reg,allow_unicode=True,sort_keys=False),encoding='utf-8')
        fail_contains([ROOT/'validators/required_view_realization_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml','--asset-registry',bad,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.valid.yaml','--phase','freeze'],'REQUIRED_VIEW_REALISM_CONTRACT_GAP')
    with tempfile.TemporaryDirectory() as td:
        reg=yaml.safe_load((ROOT/'tests/fixtures/asset_registry.realism_wagon.valid.yaml').read_text(encoding='utf-8'))
        target=next(x for x in reg['assets'] if x['asset_id']=='ASSET_WAGON_REALISM_FORWARD')
        target['realism_qc_status']='FAIL'
        bad=Path(td)/'registry.realism_fail.yaml'; bad.write_text(yaml.safe_dump(reg,allow_unicode=True,sort_keys=False),encoding='utf-8')
        fail_contains([ROOT/'validators/required_view_realization_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml','--asset-registry',bad,'--visual-evidence',ROOT/'tests/fixtures/visual_evidence.realism_wagon.valid.yaml','--phase','freeze'],'REQUIRED_VIEW_REALISM_QC_NOT_PASS')
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'vehicle_layout.svg'
        subprocess.run([sys.executable,str(ROOT/'tools/spatial_diagram_renderer.py'),str(ROOT/'tests/fixtures/spatial_canon.realism_wagon.valid.yaml'),'D_WAGON_VEHICLE_LAYOUT','--output',str(out)],check=True,cwd=ROOT)
        txt=out.read_text(encoding='utf-8'); assert 'VEHICLE_LAYOUT' in txt and 'FRONT PASSENGER' in txt
    print('V4.5.5 smoke tests: PASS')
if __name__=='__main__': raise SystemExit(main())
