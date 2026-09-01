#!/usr/bin/env python3
import json, sys, argparse, re
from temporal_scope import overlap

AUDIO_PARENT={
  'DIALOGUE':'HUMAN_AUDIO','SCREAM':'HUMAN_AUDIO','SHOUT':'HUMAN_AUDIO',
  'WORD_FORMING_VOCALIZATION':'HUMAN_AUDIO','NONVERBAL_BREATH':'HUMAN_AUDIO','GASP':'HUMAN_AUDIO'
}
HUMAN_AUDIO_PARENTS={'HUMAN_AUDIO','ALL_HUMAN_SOUND','HUMAN_SOUND','ALL_HUMAN_AUDIO'}
CAMERA_MOTION_PREDICATES={'MOTION','CAMERA_MOTION','MOVE','MOVEMENT'}
CAMERA_FOCAL_PREDICATES={'FOCAL_BEHAVIOR','FOCAL_LENGTH_BEHAVIOR'}
CAMERA_GEOMETRY_CHANGE_PREDICATES={'GEOMETRY_CHANGE','CAMERA_GEOMETRY_CHANGE'}
CAMERA_CINEMA_PREDICATES={'CAMERA_HEIGHT','HEIGHT','ENTRY_CAMERA_HEIGHT','ENTRY_VERTICAL_ANGLE','ENTRY_SUBJECT_VIEW','LANDING_CAMERA_HEIGHT','LANDING_VERTICAL_ANGLE','LANDING_SUBJECT_VIEW','VERTICAL_ANGLE','SUBJECT_VIEW','LENS_FAMILY','DEPTH_OF_FIELD','DOF','STABILIZATION','SUPPORT'}
FOCUS_PREDICATES={'FOCUS_PLANE','FOCUS_BEHAVIOR'}
SPATIAL_POSITION_PREDICATES={'HORIZONTAL_REGION','START_HORIZONTAL_REGION','END_HORIZONTAL_REGION','DEPTH_REGION','START_DEPTH','END_DEPTH','ORIENTATION','START_ORIENTATION','END_ORIENTATION'}
SPATIAL_TRAJECTORY_PREDICATES={'MOTION_DIRECTION','MOTION_VECTOR','PATH','MOTION_TARGET'}
SPATIAL_RELATION_PREDICATES={'RELATION','START_RELATION','END_RELATION'}
STABILIZATION_PREDICATES={'STABILIZATION','SUPPORT'}
STATIC_VALUES={'STATIC','LOCKED','HOLD','STILL'}
BODY_STATIC_VALUES=STATIC_VALUES|{'STATIC_BODY'}
MOVING_VALUES={'DOLLY','DOLLY_IN','DOLLY_OUT','PAN','TILT','TRUCK','TRUCK_LEFT','TRUCK_RIGHT','CRANE','PEDESTAL','ARC','ORBIT','FOLLOW','COMPOUND','PUSH_IN','PULL_OUT'}

def norm(v): return str(v).strip().upper()

def ambiguous_value(v):
    s=norm(v)
    return bool(re.search(r'\bOR\b|/OR/|(?:^|\s)或(?:\s|$)|或者|二选一', s, re.I))

def is_on(v): return norm(v) in {'ON','TRUE','1','CONDITIONAL','ALLOWED','ALLOW'}
def is_off(v): return norm(v) in {'OFF','FALSE','0','FORBIDDEN','DISALLOWED','NONE'}

def lint(data):
    cons=data.get('constraints',[]); conflicts=[]

    # Single-record ambiguity is itself unsafe for an exclusive hard constraint.
    for a in cons:
        if a.get('exclusive',True) and ambiguous_value(a.get('value','')):
            conflicts.append({'type':'AMBIGUOUS_EXCLUSIVE_VALUE','id':a.get('id'),'value':a.get('value')})
        # Rack/transfer focus is only valid when a real start target, landing target and trigger are declared.
        if norm(a.get('domain',''))=='FOCUS' and norm(a.get('predicate',''))=='FOCUS_BEHAVIOR' and norm(a.get('value','')) in {'RACK','TRANSFER'}:
            start=str(a.get('focus_start_target','')).strip()
            landing=str(a.get('focus_landing_target','')).strip()
            trigger=str(a.get('trigger','')).strip()
            if not start or not landing or not trigger or norm(start)==norm(landing):
                conflicts.append({'type':'FOCUS_STATE_CONFLICT','id':a.get('id'),'reason':'RACK_TRANSFER_REQUIRES_DISTINCT_TARGETS_AND_TRIGGER'})

    for i,a in enumerate(cons):
        for b in cons[i+1:]:
            if not overlap(a,b): continue
            da,db=norm(a.get('domain','')),norm(b.get('domain',''))
            sa,sb=norm(a.get('subject','')),norm(b.get('subject',''))
            pa,pb=norm(a.get('predicate','')),norm(b.get('predicate',''))
            va,vb=norm(a.get('value','')),norm(b.get('value',''))
            pola,polb=norm(a.get('polarity','POSITIVE')),norm(b.get('polarity','POSITIVE'))

            if da==db and sa==sb and pa==pb:
                specialized_value_conflict = (
                    (da=='CAMERA' and pa in CAMERA_CINEMA_PREDICATES) or
                    (da=='FOCUS' and pa in FOCUS_PREDICATES) or
                    (da=='SPATIAL' and pa in (SPATIAL_POSITION_PREDICATES | SPATIAL_TRAJECTORY_PREDICATES | SPATIAL_RELATION_PREDICATES))
                )
                if va!=vb and a.get('exclusive',True) and b.get('exclusive',True) and not specialized_value_conflict:
                    conflicts.append({'type':'VALUE_CONFLICT','a':a.get('id'),'b':b.get('id')})
                if pola!=polb:
                    conflicts.append({'type':'POSITIVE_NEGATIVE_CONFLICT','a':a.get('id'),'b':b.get('id')})

            # Camera motion aliases: STATIC cannot coexist with a moving state in the same time window.
            if da=='CAMERA' and db=='CAMERA' and sa==sb and pa in CAMERA_MOTION_PREDICATES and pb in CAMERA_MOTION_PREDICATES:
                if (va in STATIC_VALUES and vb in MOVING_VALUES) or (vb in STATIC_VALUES and va in MOVING_VALUES):
                    conflicts.append({'type':'CAMERA_STATE_CONFLICT','a':a.get('id'),'b':b.get('id')})

            # STATIC means no focal-length change and no camera-geometry change.
            if da=='CAMERA' and db=='CAMERA' and sa==sb:
                for motion,other in ((a,b),(b,a)):
                    mp=norm(motion.get('predicate','')); mv=norm(motion.get('value',''))
                    op=norm(other.get('predicate','')); ov=norm(other.get('value',''))
                    if mp in CAMERA_MOTION_PREDICATES and mv in BODY_STATIC_VALUES:
                        if mv in STATIC_VALUES and op in CAMERA_FOCAL_PREDICATES and ov in {'ALLOW_ZOOM','ZOOM','ZOOM_IN','ZOOM_OUT','VARIABLE'}:
                            conflicts.append({'type':'CAMERA_STATE_CONFLICT','a':motion.get('id'),'b':other.get('id'),'reason':'STATIC_FORBIDS_FOCAL_CHANGE'})
                        if op in CAMERA_GEOMETRY_CHANGE_PREDICATES and ov not in {'NONE','HOLD','NO_CHANGE','STATIC',''}:
                            conflicts.append({'type':'CAMERA_STATE_CONFLICT','a':motion.get('id'),'b':other.get('id'),'reason':'STATIC_BODY_FORBIDS_GEOMETRY_CHANGE'})

            # Cinematography fixed-state conflicts use their domain-specific type instead of generic VALUE_CONFLICT.
            if da=='CAMERA' and db=='CAMERA' and sa==sb and pa==pb and pa in CAMERA_CINEMA_PREDICATES and va!=vb:
                conflicts.append({'type':'CINEMATOGRAPHY_STATE_CONFLICT','a':a.get('id'),'b':b.get('id')})

            # Focus state conflicts are explicit because focus may live in a separate timeline/domain.
            if da=='FOCUS' and db=='FOCUS' and sa==sb and pa==pb and pa in FOCUS_PREDICATES and va!=vb:
                conflicts.append({'type':'FOCUS_STATE_CONFLICT','a':a.get('id'),'b':b.get('id')})

            # LOCKED_OFF means no physical camera move/rotation in the overlapping time window.
            if da=='CAMERA' and db=='CAMERA' and sa==sb:
                pairs=((a,b),(b,a))
                for stab,motion in pairs:
                    sp=norm(stab.get('predicate','')); sv=norm(stab.get('value',''))
                    mp=norm(motion.get('predicate','')); mv=norm(motion.get('value',''))
                    if sp in STABILIZATION_PREDICATES and sv=='LOCKED_OFF' and mp in CAMERA_MOTION_PREDICATES and mv in MOVING_VALUES:
                        conflicts.append({'type':'LOCKED_OFF_MOTION_CONFLICT','a':stab.get('id'),'b':motion.get('id')})

            # Audio parent/child: broad HUMAN AUDIO OFF conflicts child ON.
            if da=='AUDIO' and db=='AUDIO':
                for parent,child in ((a,b),(b,a)):
                    pp=norm(parent.get('predicate','')); cp=norm(child.get('predicate',''))
                    if pp in HUMAN_AUDIO_PARENTS and is_off(parent.get('value')) and AUDIO_PARENT.get(cp)=='HUMAN_AUDIO' and is_on(child.get('value')):
                        conflicts.append({'type':'AUDIO_ON_OFF_CONFLICT','a':parent.get('id'),'b':child.get('id')})

            # Action-set contract: ACTION_SET can explicitly declare allowed_values.
            if da=='ACTION' and db=='ACTION' and sa==sb:
                for aset,act in ((a,b),(b,a)):
                    if norm(aset.get('predicate')) in {'ACTION_SET','ALLOWED_ACTION_SET'} and norm(act.get('predicate')) in {'ACTION','PRIMARY_ACTION','SECONDARY_ACTION'}:
                        allowed={norm(x) for x in aset.get('allowed_values',[]) if str(x).strip()}
                        if allowed and norm(act.get('value')) not in allowed:
                            conflicts.append({'type':'ACTION_SET_CONFLICT','a':aset.get('id'),'b':act.get('id'),'allowed':sorted(allowed),'actual':act.get('value')})

            # Spatial execution conflicts: same subject/predicate, with target-aware relation checks.
            if da=='SPATIAL' and db=='SPATIAL' and sa==sb:
                ta,tb=norm(a.get('target','')),norm(b.get('target',''))
                if pa==pb and pa in SPATIAL_POSITION_PREDICATES and va!=vb:
                    conflicts.append({'type':'SPATIAL_POSITION_CONFLICT','a':a.get('id'),'b':b.get('id')})
                if pa==pb and pa in SPATIAL_TRAJECTORY_PREDICATES and va!=vb:
                    conflicts.append({'type':'SPATIAL_TRAJECTORY_CONFLICT','a':a.get('id'),'b':b.get('id')})
                if pa==pb and pa in SPATIAL_RELATION_PREDICATES and ta==tb and va!=vb:
                    conflicts.append({'type':'SPATIAL_RELATION_CONFLICT','a':a.get('id'),'b':b.get('id'),'target':a.get('target')})

            # A generic POPULATION predicate may not mix WORLD and FRAME visibility scopes.
            if da==db and sa==sb and pa==pb=='POPULATION':
                sca=norm(a.get('frame_scope') or a.get('scope'))
                scb=norm(b.get('frame_scope') or b.get('scope'))
                if sca and scb and sca!=scb and {'WORLD','FRAME_VISIBLE'} <= {sca,scb}:
                    conflicts.append({'type':'SCOPE_CONFLICT','a':a.get('id'),'b':b.get('id')})

    # If a shot is explicitly STATIC, entry and landing camera geometry must match when both are declared.
    by_subject={}
    for c in cons:
        if norm(c.get('domain',''))!='CAMERA': continue
        by_subject.setdefault(norm(c.get('subject','CAMERA')),[]).append(c)
    geo_pairs=[('ENTRY_CAMERA_HEIGHT','LANDING_CAMERA_HEIGHT'),('ENTRY_VERTICAL_ANGLE','LANDING_VERTICAL_ANGLE'),('ENTRY_SUBJECT_VIEW','LANDING_SUBJECT_VIEW')]
    for subject,items in by_subject.items():
        static_any=any(norm(x.get('predicate','')) in CAMERA_MOTION_PREDICATES and norm(x.get('value','')) in BODY_STATIC_VALUES for x in items)
        if not static_any: continue
        for ep,lp in geo_pairs:
            es=[x for x in items if norm(x.get('predicate',''))==ep]
            ls=[x for x in items if norm(x.get('predicate',''))==lp]
            for e in es:
                for l in ls:
                    if norm(e.get('value','')) != norm(l.get('value','')):
                        conflicts.append({'type':'CAMERA_STATE_CONFLICT','a':e.get('id'),'b':l.get('id'),'reason':'STATIC_ENTRY_LANDING_GEOMETRY_MISMATCH'})

    # Easy canonical spatial endpoint checks. Complex geography remains semantic-solver work.
    by_spatial={}
    for c in cons:
        if norm(c.get('domain',''))!='SPATIAL': continue
        by_spatial.setdefault(norm(c.get('subject','')),[]).append(c)
    for subject,items in by_spatial.items():
        def vals(pred): return [norm(x.get('value','')) for x in items if norm(x.get('predicate',''))==pred]
        starts=vals('START_HORIZONTAL_REGION'); ends=vals('END_HORIZONTAL_REGION'); dirs=vals('MOTION_DIRECTION')+vals('MOTION_VECTOR')
        if starts and ends and dirs:
            s,e=starts[-1],ends[-1]
            for d in dirs:
                if d in {'LEFT_TO_RIGHT','RIGHTWARD'} and s in {'RIGHT','EDGE_RIGHT'} and e in {'LEFT','EDGE_LEFT'}:
                    conflicts.append({'type':'SPATIAL_TRAJECTORY_CONFLICT','subject':subject,'reason':'RIGHTWARD_WITH_REVERSED_ENDPOINTS'})
                if d in {'RIGHT_TO_LEFT','LEFTWARD'} and s in {'LEFT','EDGE_LEFT'} and e in {'RIGHT','EDGE_RIGHT'}:
                    conflicts.append({'type':'SPATIAL_TRAJECTORY_CONFLICT','subject':subject,'reason':'LEFTWARD_WITH_REVERSED_ENDPOINTS'})
        sdepth=vals('START_DEPTH'); edepth=vals('END_DEPTH')
        if sdepth and edepth and dirs:
            sd,ed=sdepth[-1],edepth[-1]
            for d in dirs:
                if d=='FG_TO_BG' and sd=='BG' and ed=='FG':
                    conflicts.append({'type':'SPATIAL_TRAJECTORY_CONFLICT','subject':subject,'reason':'FG_TO_BG_WITH_REVERSED_DEPTH_ENDPOINTS'})
                if d=='BG_TO_FG' and sd=='FG' and ed=='BG':
                    conflicts.append({'type':'SPATIAL_TRAJECTORY_CONFLICT','subject':subject,'reason':'BG_TO_FG_WITH_REVERSED_DEPTH_ENDPOINTS'})

    # Reference binding content-role verification. Supports UI slots, attachments, native tokens and adapter handles.
    def binding_handle(r):
        return r.get('binding_handle') or r.get('token') or r.get('ui_slot') or r.get('handle') or r.get('attachment_index') or '<UNSPECIFIED_BINDING>'

    for r in data.get('references',[]):
        h=binding_handle(r)
        if not r.get('verified',False):
            conflicts.append({'type':'REFERENCE_BINDING_UNVERIFIED','binding':h})
            continue
        exp=set(map(norm,r.get('expected_fields',[]))); actual=set(map(norm,r.get('actual_fields',[])))
        missing=sorted(exp-actual)
        if missing:
            conflicts.append({'type':'REFERENCE_CONTENT_ROLE_CONFLICT','binding':h,'missing':missing})

    # Reference owner conflicts across any binding mode.
    owners={}
    for r in data.get('references',[]):
        h=binding_handle(r)
        for f in map(norm,r.get('owned_fields',[])):
            owners.setdefault(f,[]).append(h)
    for f,handles in owners.items():
        uniq=sorted(set(map(str,handles)))
        if len(uniq)>1 and f in set(map(norm,data.get('exclusive_reference_fields',[]))):
            conflicts.append({'type':'REFERENCE_OWNER_CONFLICT','field':f,'bindings':uniq})

    # Event order assertions. Fields represent actual resolved time values.
    for x in data.get('state_order_assertions',[]):
        if 'must_end_before' in x and 'must_start_after' in x:
            if float(x.get('must_end_before',0)) > float(x.get('must_start_after',0)):
                conflicts.append({'type':'STATE_ORDER_CONFLICT','id':x.get('id')})

    # Deduplicate exact conflict records.
    uniq=[]; seen=set()
    for c in conflicts:
        key=json.dumps(c,ensure_ascii=False,sort_keys=True)
        if key not in seen:
            seen.add(key); uniq.append(c)
    return {'pass':not uniq,'conflicts':uniq,'hard_conflict_count':len(uniq)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file',nargs='?'); a=ap.parse_args()
    data=json.load(open(a.file,encoding='utf-8')) if a.file else json.load(sys.stdin)
    out=lint(data); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
