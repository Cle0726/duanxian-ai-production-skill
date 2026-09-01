#!/usr/bin/env python3
"""Pre-generation hard gate for color authority and video primary-reference binding.

V4.5.7 adaptive video reference budget:
- Scene Color Authority remains mandatory for scene-bound video.
- A direct Scene Color Card image reference is NOT mandatory by default.
- Video defaults to LINEAGE_ONLY when the primary visual already inherits the same
  approved Scene Color Authority.
- DIRECT_COLOR_REFERENCE requires an explicit reason code and a real binding.
- Mandatory clean storyboard panels keep value/light lineage only and never bind
  a color card directly into the image model.
"""
import argparse, json, yaml

GLOBAL_CARD_TYPES={'GLOBAL_COLOR_CARD','BASE_COLOR_CARD'}
SCENE_CARD_TYPES={'SCENE_COLOR_CARD','SCENE_COLOR_EXTENSION_CARD'}
STORYBOARD_TYPES={'STORYBOARD_CLEAN_PANEL','STORYBOARD_CONTACT_SHEET'}
APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
SCENE_REQUIRED_HINTS=('ENVIRONMENT','SHOT_','STORYBOARD','SCENE_','PRODUCTION_SUPPORT','ASSEMBLY')
VIDEO_PRIMARY_ROLES={'PRIMARY_VISUAL_CONDITIONING','VIDEO_FIRST_FRAME','VIDEO_SHOT_EXECUTION_FRAME','SHOT_EXECUTION_FRAME'}
LEGACY_COVERAGE_TYPES={'DERIVED_COVERAGE_VIEW','EVENT_NODE_VIEW','RECIPROCAL_COVERAGE_VIEW','PREDICTIVE_COVERAGE_VIEW','SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW','LOCATION_IDENTITY_VIEW'}
VIDEO_COLOR_MODES={'DIRECT_COLOR_REFERENCE','TEXT_COLOR_CONTROL','LINEAGE_ONLY'}
AUDIO_BINDING_MODES={'AUDIO_AUTHORITY','VOICE_AUTHORITY','RHYTHM_AUTHORITY','AMBIENCE_AUTHORITY','MUSIC_AUTHORITY','SFX_AUTHORITY'}
VIDEO_ALLOWED_DIRECT_MEDIA={'IMAGE','AUDIO'}
DIRECT_COLOR_TRIGGERS={
    'COLOR_DRIFT_OBSERVED','COLOR_NARRATIVE_CRITICAL','MULTISHOT_COLOR_DRIFT_RISK',
    'PRIMARY_VISUAL_COLOR_UNRELIABLE','PROVIDER_DIRECT_COLOR_REQUIRED','USER_REQUIRED','OTHER'
}
LINEAGE_REASONS={'PRIMARY_VISUAL_INHERITS_COLOR','REFERENCE_SLOT_PRESSURE','OTHER','NONE',None}
TEXT_REASONS={'REFERENCE_SLOT_PRESSURE','PROVIDER_DIRECT_COLOR_UNSUPPORTED','OTHER','NONE',None}

def load(p):
    with open(p,encoding='utf-8') as f: return yaml.safe_load(f)


def effective_media_kind(asset):
    """Infer media kind for legacy registry records that predate explicit media_kind.
    Explicit media_kind always wins. Static video-conditioning frames are IMAGE, not reference video.
    """
    mk=asset.get('media_kind')
    if mk: return mk
    at=(asset.get('asset_type') or '').upper(); role=(asset.get('authority_role') or '').upper()
    if any(k in at for k in ('AUDIO','VOICE','DIALOGUE','SFX','FOLEY','AMBIENCE','MUSIC','RHYTHM')) or role in AUDIO_BINDING_MODES:
        return 'AUDIO'
    static_video_frame = any(k in at for k in ('FRAME','SHOT_EXECUTION','CONDITIONING'))
    actual_video = at in {'VIDEO_TAKE','VIDEO_CLIP','REFERENCE_VIDEO'} or at.endswith('_REFERENCE_VIDEO') or ('VIDEO' in at and not static_video_frame)
    if actual_video: return 'VIDEO'
    if (asset.get('video_usage') or {}).get('direct_input_allowed') is not None:
        return 'IMAGE'
    return 'UNKNOWN'

def is_scene_job(j):
    t=(j.get('target_asset_type') or '').upper()
    if t in SCENE_CARD_TYPES: return False
    if j.get('media_kind')=='VIDEO': return True
    return bool(j.get('scene_id')) or t.startswith(SCENE_REQUIRED_HINTS) or 'COVERAGE' in t

def validate_color_asset(j, assets, cid, expected, issues):
    if not cid:
        issues.append({'type':'GENERATION_COLOR_ASSET_MISSING','generation_job_id':j.get('generation_job_id')}); return
    c=assets.get(cid)
    if not c:
        issues.append({'type':'GENERATION_COLOR_ASSET_UNKNOWN','generation_job_id':j.get('generation_job_id'),'color_asset_id':cid}); return
    expected_types=SCENE_CARD_TYPES if expected=='SCENE_COLOR_CARD' else GLOBAL_CARD_TYPES
    if c.get('asset_type') not in expected_types:
        issues.append({'type':'GENERATION_COLOR_ASSET_WRONG_TYPE','generation_job_id':j.get('generation_job_id'),'color_asset_id':cid,'asset_type':c.get('asset_type')})
    if c.get('status')!='APPROVED':
        issues.append({'type':'GENERATION_COLOR_ASSET_NOT_APPROVED','generation_job_id':j.get('generation_job_id'),'color_asset_id':cid,'status':c.get('status')})
    if expected=='SCENE_COLOR_CARD':
        if j.get('scene_id') and c.get('scene_id') and j.get('scene_id')!=c.get('scene_id'):
            issues.append({'type':'GENERATION_COLOR_SCENE_MISMATCH','generation_job_id':j.get('generation_job_id'),'expected':j.get('scene_id'),'actual':c.get('scene_id')})
        jl=j.get('look_domain'); cl=c.get('look_domain')
        if jl not in {None,'NONE','UNKNOWN'} and cl not in {None,'NONE','UNKNOWN'} and jl!=cl:
            issues.append({'type':'GENERATION_COLOR_LOOK_MISMATCH','generation_job_id':j.get('generation_job_id'),'expected':jl,'actual':cl})

def color_refs(refs, cid):
    return [b for b in refs if b.get('asset_id')==cid and (b.get('role')=='COLOR_AUTHORITY' or b.get('binding_mode')=='COLOR_AUTHORITY')]

def infer_video_color_mode(cb, refs, cid):
    pm=cb.get('projection_mode')
    if pm in VIDEO_COLOR_MODES:
        return pm
    # Legacy compatibility: explicit direct binding means old DIRECT mode.
    if cb.get('required') is True or color_refs(refs,cid):
        return 'DIRECT_COLOR_REFERENCE'
    return 'LINEAGE_ONLY'

def validate_video_color_binding(j, assets, cb, refs, named, issues):
    cid=cb.get('color_asset_id')
    if cb.get('authority_level')!='SCENE_COLOR_CARD':
        issues.append({'type':'GENERATION_COLOR_AUTHORITY_LEVEL_MISMATCH','generation_job_id':j.get('generation_job_id'),'expected':'SCENE_COLOR_CARD','actual':cb.get('authority_level')})
    validate_color_asset(j,assets,cid,'SCENE_COLOR_CARD',issues)
    mode=infer_video_color_mode(cb,refs,cid)
    reason=cb.get('reference_reason_code')
    matches=color_refs(refs,cid)

    if mode=='DIRECT_COLOR_REFERENCE':
        if cb.get('required') is not True:
            issues.append({'type':'VIDEO_COLOR_DIRECT_REFERENCE_REQUIRED_FLAG_MISMATCH','generation_job_id':j.get('generation_job_id')})
        if not matches:
            issues.append({'type':'GENERATION_COLOR_REFERENCE_BINDING_MISSING','generation_job_id':j.get('generation_job_id'),'color_asset_id':cid})
        if reason not in DIRECT_COLOR_TRIGGERS:
            issues.append({'type':'VIDEO_COLOR_DIRECT_REFERENCE_TRIGGER_MISSING','generation_job_id':j.get('generation_job_id'),'reason_code':reason})
        if named and matches and not any(b.get('native_token') or b.get('asset_display_name') for b in matches):
            issues.append({'type':'GENERATION_COLOR_NATIVE_MENTION_MISSING','generation_job_id':j.get('generation_job_id'),'color_asset_id':cid})
    elif mode in {'LINEAGE_ONLY','TEXT_COLOR_CONTROL'}:
        if cb.get('required') is not False:
            issues.append({'type':'VIDEO_COLOR_NON_DIRECT_REQUIRED_FLAG_MISMATCH','generation_job_id':j.get('generation_job_id'),'mode':mode})
        if matches:
            issues.append({'type':'VIDEO_COLOR_REFERENCE_MODE_CONFLICT','generation_job_id':j.get('generation_job_id'),'mode':mode,'color_asset_id':cid})
        if cb.get('binding_status') not in {'NOT_REQUIRED','UNKNOWN',None}:
            issues.append({'type':'VIDEO_COLOR_NON_DIRECT_BINDING_STATUS_CONFLICT','generation_job_id':j.get('generation_job_id'),'mode':mode,'binding_status':cb.get('binding_status')})
        if mode=='LINEAGE_ONLY' and reason not in LINEAGE_REASONS:
            issues.append({'type':'VIDEO_COLOR_REFERENCE_REASON_CONFLICT','generation_job_id':j.get('generation_job_id'),'mode':mode,'reason_code':reason})
        if mode=='TEXT_COLOR_CONTROL' and reason not in TEXT_REASONS:
            issues.append({'type':'VIDEO_COLOR_REFERENCE_REASON_CONFLICT','generation_job_id':j.get('generation_job_id'),'mode':mode,'reason_code':reason})
    else:
        issues.append({'type':'VIDEO_COLOR_REFERENCE_MODE_INVALID','generation_job_id':j.get('generation_job_id'),'mode':mode})
    return mode

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--job',required=True); ap.add_argument('--registry',required=True); ap.add_argument('--named-mention-mode',action='store_true'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    j=load(a.job); reg=load(a.registry); assets={x.get('asset_id'):x for x in reg.get('assets',[]) if x.get('asset_id')}; issues=[]
    kind=j.get('media_kind'); target=(j.get('target_asset_type') or '').upper(); cb=j.get('color_binding') or {}; refs=j.get('required_bindings') or []
    if target=='STORYBOARD_CLEAN_SEQUENCE_BOARD':
        issues.append({'type':'DETERMINISTIC_STORYBOARD_BOARD_CANNOT_BE_GENERATION_JOB','generation_job_id':j.get('generation_job_id')})
    if j.get('skill_version') in {'4.5.7','4.5.11'} and target in LEGACY_COVERAGE_TYPES:
        issues.append({'type':'LEGACY_COVERAGE_TYPE_NEW_PRODUCTION','generation_job_id':j.get('generation_job_id'),'target_asset_type':target,'required_type':'ENVIRONMENT_COVERAGE'})
    if kind not in {'IMAGE','VIDEO'}:
        issues.append({'type':'GENERATION_JOB_MEDIA_KIND_UNSUPPORTED','media_kind':kind})

    bootstrap=(kind=='IMAGE' and target in GLOBAL_CARD_TYPES)
    storyboard=(kind=='IMAGE' and target in STORYBOARD_TYPES)
    expected='SCENE_COLOR_CARD' if is_scene_job(j) else 'GLOBAL_COLOR_CARD'
    if target in SCENE_CARD_TYPES: expected='GLOBAL_COLOR_CARD'

    if storyboard:
        if cb.get('required') is not False:
            issues.append({'type':'STORYBOARD_DIRECT_COLOR_BINDING_MUST_BE_DISABLED','generation_job_id':j.get('generation_job_id')})
        if cb.get('authority_level')!='SCENE_COLOR_CARD':
            issues.append({'type':'STORYBOARD_VALUE_LINEAGE_AUTHORITY_MISMATCH','generation_job_id':j.get('generation_job_id'),'actual':cb.get('authority_level')})
        if cb.get('projection_mode')!='VALUE_LIGHTING_LINEAGE_ONLY':
            issues.append({'type':'STORYBOARD_COLOR_PROJECTION_MODE_INVALID','generation_job_id':j.get('generation_job_id'),'actual':cb.get('projection_mode')})
        if cb.get('binding_status')!='NOT_REQUIRED':
            issues.append({'type':'STORYBOARD_COLOR_BINDING_STATUS_INVALID','generation_job_id':j.get('generation_job_id'),'actual':cb.get('binding_status')})
        cid=cb.get('color_asset_id'); validate_color_asset(j,assets,cid,'SCENE_COLOR_CARD',issues)
        if color_refs(refs,cid):
            issues.append({'type':'STORYBOARD_DIRECT_COLOR_REFERENCE_FORBIDDEN','generation_job_id':j.get('generation_job_id'),'color_asset_id':cid})
    elif kind=='VIDEO':
        validate_video_color_binding(j,assets,cb,refs,a.named_mention_mode,issues)
    elif not bootstrap:
        if cb.get('required') is not True:
            issues.append({'type':'GENERATION_COLOR_BINDING_NOT_REQUIRED','generation_job_id':j.get('generation_job_id')})
        if cb.get('authority_level')!=expected:
            issues.append({'type':'GENERATION_COLOR_AUTHORITY_LEVEL_MISMATCH','generation_job_id':j.get('generation_job_id'),'expected':expected,'actual':cb.get('authority_level')})
        if cb.get('projection_mode') not in {None,'DIRECT_COLOR_REFERENCE'}:
            issues.append({'type':'GENERATION_COLOR_PROJECTION_MODE_MISMATCH','generation_job_id':j.get('generation_job_id'),'expected':'DIRECT_COLOR_REFERENCE','actual':cb.get('projection_mode')})
        cid=cb.get('color_asset_id'); validate_color_asset(j,assets,cid,expected,issues)
        if cid:
            matches=color_refs(refs,cid)
            if not matches:
                issues.append({'type':'GENERATION_COLOR_REFERENCE_BINDING_MISSING','generation_job_id':j.get('generation_job_id'),'color_asset_id':cid})
            elif a.named_mention_mode and not any(b.get('native_token') or b.get('asset_display_name') for b in matches):
                issues.append({'type':'GENERATION_COLOR_NATIVE_MENTION_MISSING','generation_job_id':j.get('generation_job_id'),'color_asset_id':cid})

    if kind=='VIDEO':
        seen_binding_assets=set()
        for b in refs:
            aid=b.get('asset_id'); ax=assets.get(aid); mode=b.get('binding_mode'); role=b.get('role')
            if aid in seen_binding_assets:
                issues.append({'type':'GENERATION_REQUIRED_BINDING_DUPLICATE_ASSET','generation_job_id':j.get('generation_job_id'),'asset_id':aid})
            seen_binding_assets.add(aid)
            if not ax:
                issues.append({'type':'GENERATION_REQUIRED_BINDING_ASSET_UNKNOWN','generation_job_id':j.get('generation_job_id'),'asset_id':aid})
                continue
            mk=effective_media_kind(ax)
            vu=ax.get('video_usage') or {}
            if vu.get('direct_input_allowed') is False:
                issues.append({'type':'VIDEO_REFERENCE_DIRECT_INPUT_NOT_ALLOWED','generation_job_id':j.get('generation_job_id'),'asset_id':aid,'asset_type':ax.get('asset_type')})
            if mk=='VIDEO':
                issues.append({'type':'REFERENCE_VIDEO_FORBIDDEN','generation_job_id':j.get('generation_job_id'),'asset_id':ax.get('asset_id'),'reason':'FORBIDDEN_QUOTA_COST'})
            elif mk not in VIDEO_ALLOWED_DIRECT_MEDIA:
                issues.append({'type':'VIDEO_REFERENCE_MEDIA_KIND_FORBIDDEN','generation_job_id':j.get('generation_job_id'),'asset_id':aid,'media_kind':mk,'allowed':sorted(VIDEO_ALLOWED_DIRECT_MEDIA)})
            audio_declared=(mode in AUDIO_BINDING_MODES or role in AUDIO_BINDING_MODES)
            if audio_declared and mk!='AUDIO':
                issues.append({'type':'AUDIO_REFERENCE_ASSET_KIND_MISMATCH','generation_job_id':j.get('generation_job_id'),'asset_id':aid,'media_kind':mk,'binding_mode':mode,'role':role})
            if mk=='AUDIO' and not audio_declared:
                issues.append({'type':'AUDIO_REFERENCE_ROLE_UNDECLARED','generation_job_id':j.get('generation_job_id'),'asset_id':aid,'binding_mode':mode,'role':role})
        for key in ('video_unit_id','prompt_ref','prompt_fingerprint','execution_plan_ref','execution_plan_fingerprint','prompt_artifact_ref'):
            if not j.get(key): issues.append({'type':'VIDEO_GENERATION_PROMPT_PLAN_BINDING_MISSING','generation_job_id':j.get('generation_job_id'),'field':key})
        if not j.get('scene_id'):
            issues.append({'type':'VIDEO_GENERATION_SCENE_SCOPE_MISSING','generation_job_id':j.get('generation_job_id')})
        temporal=j.get('temporal_binding') or {}
        same=temporal.get('entry_mode') in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}
        prim=[b for b in refs if b.get('binding_mode')=='PRIMARY_VIEW' or b.get('role') in VIDEO_PRIMARY_ROLES]
        # Same-take temporal continuation has an exclusive t=0 owner. For cut/rebase
        # jobs, Jimeng all-round profiles may omit a redundant baked composite when
        # independent high-fidelity field owners and storyboard control are bound.
        provider_routed_omit=(not same and j.get('host_profile') in {'JIMENG_SEEDANCE_2_0_OMNI','JIMENG_SEEDANCE_2_5_30S'} and not prim)
        if same:
            if prim: issues.append({'type':'TEMPORAL_T0_MULTIPLE_PRIMARY_VISUAL_CONFLICT','generation_job_id':j.get('generation_job_id'),'asset_ids':[b.get('asset_id') for b in prim]})
            tr=temporal.get('provider_transport') or {}
            if tr.get('t0_semantics_verified') is not True or tr.get('transport_type')=='GENERIC_REFERENCE' or not tr.get('capability_evidence_ref'):
                issues.append({'type':'TEMPORAL_PROVIDER_T0_TRANSPORT_UNVERIFIED','generation_job_id':j.get('generation_job_id')})
            if not temporal.get('continuity_snapshot_ref') or not temporal.get('continuity_snapshot_fingerprint'):
                issues.append({'type':'TEMPORAL_CONTINUITY_SNAPSHOT_BINDING_MISSING','generation_job_id':j.get('generation_job_id')})
            for b in refs:
                ax=assets.get(b.get('asset_id')); mk=effective_media_kind(ax or {})
                if mk=='IMAGE': issues.append({'type':'TEMPORAL_CONTINUITY_AUXILIARY_VISUAL_REFERENCE_CONFLICT','generation_job_id':j.get('generation_job_id'),'asset_id':b.get('asset_id')})
            if infer_video_color_mode(cb,refs,cb.get('color_asset_id'))=='DIRECT_COLOR_REFERENCE': issues.append({'type':'TEMPORAL_CONTINUITY_DIRECT_COLOR_REFERENCE_CONFLICT','generation_job_id':j.get('generation_job_id')})
        elif not prim and not provider_routed_omit:
            issues.append({'type':'VIDEO_PRIMARY_VISUAL_BINDING_MISSING','generation_job_id':j.get('generation_job_id')})
            issues.append({'type':'VIDEO_PRIMARY_VISUAL_BINDING_MISSING','generation_job_id':j.get('generation_job_id')})
        if provider_routed_omit:
            roles={str(b.get('role') or '').upper() for b in refs}
            if 'EMPTY_ENVIRONMENT_MASTER' not in roles:
                issues.append({'type':'PROVIDER_ROUTED_EMPTY_ENVIRONMENT_BINDING_MISSING','generation_job_id':j.get('generation_job_id')})
            if 'CURRENT_SHOT_STORYBOARD_TEMPORAL_CONTROL' not in roles:
                issues.append({'type':'PROVIDER_ROUTED_STORYBOARD_BINDING_MISSING','generation_job_id':j.get('generation_job_id')})
            if 'CHARACTER_MASTER' not in roles:
                issues.append({'type':'PROVIDER_ROUTED_CHARACTER_MASTER_BINDING_MISSING','generation_job_id':j.get('generation_job_id')})
        for b in prim:
            ax=assets.get(b.get('asset_id'))
            if not ax:
                issues.append({'type':'VIDEO_PRIMARY_VISUAL_ASSET_UNKNOWN','generation_job_id':j.get('generation_job_id'),'asset_id':b.get('asset_id')}); continue
            if ax.get('status') not in APPROVED:
                issues.append({'type':'VIDEO_PRIMARY_VISUAL_NOT_APPROVED','generation_job_id':j.get('generation_job_id'),'asset_id':ax.get('asset_id'),'status':ax.get('status')})
            vu=ax.get('video_usage') or {}
            if not (vu.get('direct_input_allowed') and vu.get('primary_visual_eligible')):
                issues.append({'type':'VIDEO_PRIMARY_VISUAL_NOT_ELIGIBLE','generation_job_id':j.get('generation_job_id'),'asset_id':ax.get('asset_id')})
            if cb.get('color_asset_id') and ax.get('scene_color_authority_id')!=cb.get('color_asset_id'):
                issues.append({'type':'VIDEO_PRIMARY_VISUAL_COLOR_MISMATCH','generation_job_id':j.get('generation_job_id'),'asset_id':ax.get('asset_id'),'expected_color_asset_id':cb.get('color_asset_id'),'actual_color_asset_id':ax.get('scene_color_authority_id')})
    out={'pass':not issues,'issues':issues}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out)
    return 1 if issues else 0
if __name__=='__main__': raise SystemExit(main())
