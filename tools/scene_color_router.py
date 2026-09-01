#!/usr/bin/env python3
"""Resolve or seed a Scene Color Card from an approved Base/Global Color Card."""
import argparse, json, hashlib, yaml

GLOBAL_TYPES={'GLOBAL_COLOR_CARD','BASE_COLOR_CARD'}
SCENE_TYPES={'SCENE_COLOR_CARD','SCENE_COLOR_EXTENSION_CARD'}

def load(path):
    with open(path,encoding='utf-8') as f: return yaml.safe_load(f)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--registry', required=True)
    ap.add_argument('--base-color-asset-id', required=True)
    ap.add_argument('--scene-id', required=True)
    ap.add_argument('--look-domain', default='MIXED')
    ap.add_argument('--location-entity-id')
    ap.add_argument('--existing-scene-color-asset-id')
    ap.add_argument('--json', action='store_true')
    a=ap.parse_args(); reg=load(a.registry); assets={x.get('asset_id'):x for x in reg.get('assets',[]) if x.get('asset_id')}
    base=assets.get(a.base_color_asset_id)
    if not base or base.get('status')!='APPROVED' or base.get('asset_type') not in GLOBAL_TYPES:
        out={'pass':False,'error':'BASE_COLOR_AUTHORITY_INVALID','base_color_asset_id':a.base_color_asset_id}
        print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
    look=a.look_domain.upper()
    candidates=[]
    for x in assets.values():
        if x.get('asset_type') not in SCENE_TYPES or x.get('status')!='APPROVED': continue
        if x.get('scene_id')!=a.scene_id: continue
        if x.get('look_domain') not in {look,None,'UNKNOWN'}: continue
        if a.location_entity_id and x.get('location_entity_id') not in {a.location_entity_id,None}: continue
        candidates.append(x)
    if a.existing_scene_color_asset_id:
        x=assets.get(a.existing_scene_color_asset_id)
        if not x or x not in candidates:
            out={'pass':False,'error':'EXISTING_SCENE_COLOR_AUTHORITY_INVALID','scene_color_asset_id':a.existing_scene_color_asset_id}
            print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
        candidates=[x]
    if len(candidates)>1:
        out={'pass':False,'error':'AMBIGUOUS_APPROVED_SCENE_COLOR_AUTHORITY','scene_id':a.scene_id,'asset_ids':[x['asset_id'] for x in candidates]}
        print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
    if candidates:
        x=candidates[0]
        out={'pass':True,'required':False,'scene_id':a.scene_id,'look_domain':look,'scene_color_asset_id':x['asset_id'],'reason':'REUSE_APPROVED_SCENE_COLOR_AUTHORITY'}
    else:
        scope=f'{a.scene_id}:{look}'
        suffix=hashlib.sha256(scope.encode()).hexdigest()[:10].upper(); asset_id=f'COLOR-SCENE-{suffix}'
        out={'pass':True,'required':True,'scene_id':a.scene_id,'look_domain':look,'location_entity_id':a.location_entity_id,'target_asset_id':asset_id,'target_asset_type':'SCENE_COLOR_EXTENSION_CARD','route':'SCENE_COLOR_CARD_DERIVATION','derivation_kind':'SCENE_COLOR_FROM_BASE','parent_asset_ids':[a.base_color_asset_id],
             'color_binding':{'required':True,'authority_level':'GLOBAL_COLOR_CARD','color_asset_id':a.base_color_asset_id,'scene_scope':None,'native_token':base.get('native_token'),'binding_status':'BOUND' if (base.get('native_token') or base.get('asset_display_name')) else 'PENDING_NATIVE_BINDING'},
             'required_bindings':[{'asset_id':a.base_color_asset_id,'role':'COLOR_AUTHORITY','binding_mode':'COLOR_AUTHORITY','native_token':base.get('native_token'),'asset_display_name':base.get('asset_display_name')} ]}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else json.dumps(out,ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
