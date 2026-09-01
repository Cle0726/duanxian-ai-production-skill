#!/usr/bin/env python3
"""Validate Scene Color Authority ownership and adaptive downstream video routing."""
import argparse, json, yaml

FORMAL_APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
SCENE_CARD_TYPES={'SCENE_COLOR_EXTENSION_CARD','SCENE_COLOR_CARD'}
SCENE_BOUND_PREFIXES=('ENVIRONMENT','SHOT_','VIDEO_','STORYBOARD','SCENE_')
SCENE_BOUND_TYPES={'EVENT_NODE_VIEW','RECIPROCAL_COVERAGE','RECIPROCAL_COVERAGE_VIEW','PREDICTIVE_COVERAGE','PREDICTIVE_COVERAGE_VIEW','HD_SHOT_ASSEMBLY_IMAGE','PRIMARY_VISUAL_CONDITIONING','ENVIRONMENT_COVERAGE','PRODUCTION_SUPPORT_REFERENCE','SHOT_ASSEMBLY_ASSET'}
VIDEO_COLOR_MODES={'LINEAGE_ONLY','TEXT_CONTROL','DIRECT_REFERENCE'}

def load(p):
    with open(p,encoding='utf-8') as f: return yaml.safe_load(f)

def is_scene_bound(x):
    t=(x.get('asset_type') or '').upper()
    if t in SCENE_CARD_TYPES: return False
    return bool(x.get('scene_id')) or t.startswith(SCENE_BOUND_PREFIXES) or t in SCENE_BOUND_TYPES or 'ASSEMBLY' in t or 'COVERAGE' in t

def card_scope_mismatch(asset, card):
    problems=[]
    if asset.get('scene_id') and card.get('scene_id') and asset.get('scene_id')!=card.get('scene_id'):
        problems.append(('scene_id',asset.get('scene_id'),card.get('scene_id')))
    if asset.get('location_entity_id') and card.get('location_entity_id') and asset.get('location_entity_id')!=card.get('location_entity_id'):
        problems.append(('location_entity_id',asset.get('location_entity_id'),card.get('location_entity_id')))
    al=asset.get('look_domain'); cl=card.get('look_domain')
    if al not in {None,'NONE','UNKNOWN'} and cl not in {None,'NONE','UNKNOWN'} and al!=cl:
        problems.append(('look_domain',al,cl))
    return problems

def validate_card(assets, cid, consumer=None, named=False):
    issues=[]; c=assets.get(cid)
    if not c:
        return [{'type':'SCENE_COLOR_AUTHORITY_GAP','asset_id':(consumer or {}).get('asset_id'),'color_asset_id':cid,'reason':'MISSING_ASSET'}]
    if c.get('asset_type') not in SCENE_CARD_TYPES or c.get('color_authority_level')!='SCENE_COLOR_CARD':
        issues.append({'type':'SCENE_COLOR_AUTHORITY_WRONG_TYPE','asset_id':(consumer or {}).get('asset_id'),'color_asset_id':cid,'asset_type':c.get('asset_type'),'color_authority_level':c.get('color_authority_level')})
    if c.get('status')!='APPROVED':
        issues.append({'type':'SCENE_COLOR_AUTHORITY_NOT_APPROVED','asset_id':(consumer or {}).get('asset_id'),'color_asset_id':cid,'status':c.get('status')})
    if consumer:
        for field,expected,actual in card_scope_mismatch(consumer,c):
            issues.append({'type':'SCENE_COLOR_SCOPE_MISMATCH','asset_id':consumer.get('asset_id'),'color_asset_id':cid,'field':field,'expected':expected,'actual':actual})
    if named and not (c.get('native_token') or c.get('asset_display_name')):
        issues.append({'type':'SCENE_COLOR_NATIVE_MENTION_MISSING','asset_id':(consumer or {}).get('asset_id'),'color_asset_id':cid})
    return issues

def infer_mode(u, matches):
    mode=u.get('scene_color_reference_mode')
    if mode in VIDEO_COLOR_MODES: return mode, False
    return ('DIRECT_REFERENCE' if matches else 'LINEAGE_ONLY'), True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--registry',required=True); ap.add_argument('--conditioning-runtime'); ap.add_argument('--named-mention-mode',action='store_true'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    reg=load(a.registry); assets={x.get('asset_id'):x for x in reg.get('assets',[]) if x.get('asset_id')}; issues=[]
    # Scene-bound IMAGE assets must still carry a valid Scene Color Authority lineage.
    for x in assets.values():
        if x.get('media_kind')!='IMAGE' or not is_scene_bound(x): continue
        if x.get('status') not in FORMAL_APPROVED|{'QC_PASS_WAITING_APPROVAL'}: continue
        cid=x.get('scene_color_authority_id')
        if not cid:
            issues.append({'type':'SCENE_COLOR_BINDING_MISSING','asset_id':x.get('asset_id')}); continue
        issues.extend(validate_card(assets,cid,x,a.named_mention_mode))
    if a.conditioning_runtime:
        rt=load(a.conditioning_runtime)
        for u in rt.get('video_units',[]):
            uid=u.get('video_unit_id'); cid=u.get('scene_color_authority_id')
            if not cid:
                issues.append({'type':'VIDEO_COLOR_BINDING_MISSING','video_unit_id':uid}); continue
            # Authority must exist regardless of whether it consumes a direct slot.
            issues.extend([{**z,'video_unit_id':uid} for z in validate_card(assets,cid,None,False)])
            refs=u.get('required_reference_bindings',[]) or []
            matches=[z for z in refs if z.get('asset_id')==cid and z.get('role')=='COLOR_AUTHORITY']
            mode,legacy=infer_mode(u,matches)
            if mode not in VIDEO_COLOR_MODES:
                issues.append({'type':'VIDEO_COLOR_REFERENCE_MODE_INVALID','video_unit_id':uid,'mode':mode}); continue
            if not legacy and not u.get('scene_color_reference_reason'):
                issues.append({'type':'VIDEO_COLOR_REFERENCE_REASON_MISSING','video_unit_id':uid,'mode':mode})
            if mode=='DIRECT_REFERENCE':
                if not matches:
                    issues.append({'type':'VIDEO_COLOR_BINDING_MISSING','video_unit_id':uid,'color_asset_id':cid,'mode':mode})
                elif not any(z.get('binding_status')=='BOUND' for z in matches):
                    issues.append({'type':'VIDEO_COLOR_BINDING_NOT_BOUND','video_unit_id':uid,'color_asset_id':cid})
                elif a.named_mention_mode and not any(z.get('native_token') for z in matches):
                    issues.append({'type':'SCENE_COLOR_NATIVE_MENTION_MISSING','video_unit_id':uid,'color_asset_id':cid})
            else:
                if matches:
                    issues.append({'type':'VIDEO_COLOR_REFERENCE_MODE_CONFLICT','video_unit_id':uid,'mode':mode,'color_asset_id':cid})
            budget=u.get('reference_budget') or {}
            selected=budget.get('selected_direct_reference_ids') or []
            if mode!='DIRECT_REFERENCE' and cid in selected:
                issues.append({'type':'VIDEO_COLOR_REFERENCE_BUDGET_CONFLICT','video_unit_id':uid,'mode':mode,'color_asset_id':cid})
            # Primary Visual must inherit the same Scene Color Authority as the video unit.
            for p in u.get('primary_assets',[]) or []:
                aid=p.get('asset_id'); ax=assets.get(aid)
                if not ax:
                    issues.append({'type':'VIDEO_PRIMARY_ASSET_MISSING','video_unit_id':uid,'asset_id':aid}); continue
                if ax.get('scene_color_authority_id')!=cid:
                    issues.append({'type':'VIDEO_PRIMARY_COLOR_LINEAGE_MISMATCH','video_unit_id':uid,'asset_id':aid,'expected_color_asset_id':cid,'actual_color_asset_id':ax.get('scene_color_authority_id')})
                else:
                    for field,expected,actual in card_scope_mismatch(ax,assets.get(cid) or {}):
                        issues.append({'type':'VIDEO_PRIMARY_COLOR_SCOPE_MISMATCH','video_unit_id':uid,'asset_id':aid,'field':field,'expected':expected,'actual':actual})
    out={'pass':not issues,'issues':issues}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out)
    return 1 if issues else 0
if __name__=='__main__': raise SystemExit(main())
