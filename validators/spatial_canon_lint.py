#!/usr/bin/env python3
"""Validate SPATIAL_CANON and optionally prove SHOT_RELATION_GRAPH world relations against it."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def dup_ids(items,key):
    seen=set(); dup=[]
    for x in items:
        v=x.get(key)
        if v in seen: dup.append(v)
        seen.add(v)
    return sorted(set(dup))

def lint(spatial, graph=None):
    issues=[]
    locs=spatial.get('locations') or []
    rels=spatial.get('relations') or []
    evs=spatial.get('event_nodes') or []
    routes=spatial.get('character_routes') or []
    diagrams=spatial.get('planning_diagrams') or []
    for key,items in [('location_entity_id',locs),('spatial_relation_id',rels),('event_node_id',evs)]:
        for d in dup_ids(items,key): issues.append({'type':'DUPLICATE_ID','field':key,'id':d})
    loc_by={x.get('location_entity_id'):x for x in locs}
    rel_by={x.get('spatial_relation_id'):x for x in rels}
    anchor_by={}
    for l in locs:
        lid=l.get('location_entity_id')
        if l.get('status')!='LOCKED': issues.append({'type':'SPATIAL_LOCATION_NOT_LOCKED','location_entity_id':lid,'status':l.get('status')})
        for a in l.get('anchors') or []:
            aid=a.get('anchor_id')
            if aid in anchor_by: issues.append({'type':'DUPLICATE_SPATIAL_ANCHOR_ID','anchor_id':aid})
            anchor_by[aid]=(lid,a)
    # Access paths are first-class functional geometry in V4.5.6.
    access_path_by={}
    for l in locs:
        lid=l.get('location_entity_id'); zones=set(l.get('zones') or [])
        for pth in l.get('access_paths') or []:
            pid=pth.get('path_id')
            if pid in access_path_by:
                issues.append({'type':'DUPLICATE_SPATIAL_ACCESS_PATH_ID','access_path_id':pid})
            access_path_by[pid]=(lid,pth)
            for field in ['from_zone_id','to_zone_id']:
                zid=pth.get(field)
                if zid and zid not in zones:
                    issues.append({'type':'SPATIAL_ACCESS_PATH_UNKNOWN_ZONE','access_path_id':pid,'field':field,'zone_id':zid,'location_entity_id':lid})
            for aid in pth.get('via_anchor_ids') or []:
                if aid not in anchor_by:
                    issues.append({'type':'SPATIAL_ACCESS_PATH_UNKNOWN_ANCHOR','access_path_id':pid,'anchor_id':aid})
                elif anchor_by[aid][0]!=lid:
                    issues.append({'type':'SPATIAL_ACCESS_PATH_ANCHOR_OUT_OF_SCOPE','access_path_id':pid,'anchor_id':aid,'location_entity_id':lid})
            if pth.get('passable') is False:
                issues.append({'type':'SPATIAL_ACCESS_PATH_NOT_PASSABLE','access_path_id':pid,'location_entity_id':lid})
    for r in rels:
        rid=r.get('spatial_relation_id')
        if r.get('status')!='LOCKED': issues.append({'type':'SPATIAL_RELATION_NOT_LOCKED','spatial_relation_id':rid,'status':r.get('status')})
        if r.get('from_entity_id') not in loc_by: issues.append({'type':'SPATIAL_RELATION_UNKNOWN_FROM','spatial_relation_id':rid,'entity_id':r.get('from_entity_id')})
        if r.get('to_entity_id') not in loc_by: issues.append({'type':'SPATIAL_RELATION_UNKNOWN_TO','spatial_relation_id':rid,'entity_id':r.get('to_entity_id')})
        fa=r.get('from_anchor_id')
        if fa and fa not in anchor_by: issues.append({'type':'SPATIAL_RELATION_UNKNOWN_ANCHOR','spatial_relation_id':rid,'anchor_id':fa})
        if r.get('relation_kind')=='VISIBLE_FROM':
            if not fa: issues.append({'type':'VISIBLE_FROM_ANCHOR_MISSING','spatial_relation_id':rid})
            elif fa in anchor_by:
                owner,a=anchor_by[fa]
                if owner!=r.get('from_entity_id'):
                    issues.append({'type':'VISIBLE_FROM_ANCHOR_OWNER_MISMATCH','spatial_relation_id':rid,'anchor_id':fa,'owner':owner})
                targets=set(a.get('visible_targets') or [])
                if r.get('to_entity_id') not in targets:
                    issues.append({'type':'SIGHTLINE_TARGET_NOT_DECLARED_ON_ANCHOR','spatial_relation_id':rid,'anchor_id':fa,'target':r.get('to_entity_id')})
    for e in evs:
        if e.get('location_entity_id') not in loc_by: issues.append({'type':'EVENT_NODE_UNKNOWN_LOCATION','event_node_id':e.get('event_node_id')})
        for rid in e.get('required_spatial_relation_ids') or []:
            if rid not in rel_by: issues.append({'type':'EVENT_NODE_UNKNOWN_SPATIAL_RELATION','event_node_id':e.get('event_node_id'),'spatial_relation_id':rid})
    # Character event routes: event-grounded physical paths.
    route_by={}
    event_by={e.get('event_node_id'):e for e in evs}
    for r in routes:
        rid=r.get('route_id')
        if rid in route_by: issues.append({'type':'DUPLICATE_CHARACTER_ROUTE_ID','route_id':rid})
        route_by[rid]=r
        if r.get('status')!='LOCKED': issues.append({'type':'CHARACTER_ROUTE_NOT_LOCKED','route_id':rid,'status':r.get('status')})
        orders=[]
        for n in r.get('nodes') or []:
            orders.append(n.get('order'))
            lid=n.get('location_entity_id')
            if lid not in loc_by: issues.append({'type':'CHARACTER_ROUTE_UNKNOWN_LOCATION','route_id':rid,'location_entity_id':lid})
            aid=n.get('anchor_id')
            if aid and aid not in anchor_by: issues.append({'type':'CHARACTER_ROUTE_UNKNOWN_ANCHOR','route_id':rid,'anchor_id':aid})
            eid=n.get('event_node_id')
            if eid and eid not in event_by: issues.append({'type':'CHARACTER_ROUTE_UNKNOWN_EVENT_NODE','route_id':rid,'event_node_id':eid})
            for srid in n.get('spatial_relation_ids') or []:
                if srid not in rel_by: issues.append({'type':'CHARACTER_ROUTE_UNKNOWN_SPATIAL_RELATION','route_id':rid,'spatial_relation_id':srid})
        if len(orders)!=len(set(orders)): issues.append({'type':'CHARACTER_ROUTE_DUPLICATE_ORDER','route_id':rid})
    for e in evs:
        rid=e.get('character_route_id')
        if rid and rid not in route_by: issues.append({'type':'EVENT_NODE_UNKNOWN_CHARACTER_ROUTE','event_node_id':e.get('event_node_id'),'route_id':rid})
    # Required planning diagrams for reusable sets are structural evidence, not decorative docs.
    dids=set()
    for d in diagrams:
        did=d.get('diagram_id')
        if did in dids: issues.append({'type':'DUPLICATE_SPATIAL_DIAGRAM_ID','diagram_id':did})
        dids.add(did)
        scope=set(d.get('scope_location_ids') or [])
        for lid in scope:
            if lid not in loc_by: issues.append({'type':'SPATIAL_DIAGRAM_UNKNOWN_LOCATION','diagram_id':did,'location_entity_id':lid})
        for rid in d.get('character_route_ids') or []:
            if rid not in route_by: issues.append({'type':'SPATIAL_DIAGRAM_UNKNOWN_CHARACTER_ROUTE','diagram_id':did,'route_id':rid})
        # Renderable diagram geometry must reference real event/zone/anchor facts.
        node_refs={n.get('node_ref') for n in d.get('nodes') or []}
        known_node_refs=set(loc_by)|set(event_by)|set(anchor_by)
        for nr in node_refs:
            if nr not in known_node_refs: issues.append({'type':'SPATIAL_DIAGRAM_UNKNOWN_NODE_REF','diagram_id':did,'node_ref':nr})
        for e in d.get('edges') or []:
            if e.get('from_ref') not in node_refs or e.get('to_ref') not in node_refs:
                issues.append({'type':'SPATIAL_DIAGRAM_EDGE_NODE_MISSING','diagram_id':did,'from_ref':e.get('from_ref'),'to_ref':e.get('to_ref')})
            rel=e.get('relation_id')
            if rel and rel not in rel_by: issues.append({'type':'SPATIAL_DIAGRAM_EDGE_RELATION_MISSING','diagram_id':did,'spatial_relation_id':rel})
        allowed_zones=set()
        for lid in scope:
            allowed_zones.update((loc_by.get(lid) or {}).get('zones') or [])
        for z in d.get('zone_boxes') or []:
            if z.get('zone_id') not in allowed_zones: issues.append({'type':'SPATIAL_DIAGRAM_UNKNOWN_ZONE','diagram_id':did,'zone_id':z.get('zone_id')})
        for ap in d.get('anchor_points') or []:
            aid=ap.get('anchor_id')
            if aid not in anchor_by: issues.append({'type':'SPATIAL_DIAGRAM_UNKNOWN_ANCHOR','diagram_id':did,'anchor_id':aid})
            elif anchor_by[aid][0] not in scope: issues.append({'type':'SPATIAL_DIAGRAM_ANCHOR_OUT_OF_SCOPE','diagram_id':did,'anchor_id':aid})
    for lid,l in loc_by.items():
        if l.get('reuse_tier') not in {'S','A'}: continue
        kind=l.get('location_kind')
        acceptable={'OUTDOOR':{'OUTDOOR_TOPOLOGY','ROUTE_MAP'},'BUILDING':{'BUILDING_FLOOR_PLAN','ROOM_LAYOUT','ZONE_MAP'},'INTERIOR':{'BUILDING_FLOOR_PLAN','ROOM_LAYOUT','ZONE_MAP'},'VEHICLE':{'VEHICLE_LAYOUT'},'MIXED':{'OUTDOOR_TOPOLOGY','BUILDING_FLOOR_PLAN','ROOM_LAYOUT','ZONE_MAP','ROUTE_MAP','VEHICLE_LAYOUT'}}.get(kind,set())
        if not any(d.get('status')=='APPROVED' and lid in (d.get('scope_location_ids') or []) and d.get('diagram_type') in acceptable for d in diagrams):
            issues.append({'type':'REUSABLE_SET_PLANNING_DIAGRAM_MISSING','location_entity_id':lid,'reuse_tier':l.get('reuse_tier'),'location_kind':kind})
    if spatial.get('status')!='LOCKED': issues.append({'type':'SPATIAL_CANON_NOT_LOCKED','status':spatial.get('status')})
    if graph:
        for r in graph.get('relations') or []:
            rid=r.get('relation_id')
            for srid in r.get('spatial_relation_ids') or []:
                if srid not in rel_by:
                    issues.append({'type':'SHOT_RELATION_SPATIAL_PROOF_REF_MISSING','relation_id':rid,'spatial_relation_id':srid})
            # semantic proof: world relation claims must match at least one locked spatial relation
            for wr in r.get('world_relations') or []:
                kind=wr.get('relation_kind')
                candidates=[]
                for sr in rels:
                    if sr.get('status')!='LOCKED': continue
                    if kind=='VISIBLE_FROM' and sr.get('relation_kind')=='VISIBLE_FROM':
                        if sr.get('from_entity_id')==wr.get('from_location_id') and sr.get('to_entity_id')==wr.get('to_location_id'):
                            if not wr.get('sightline_anchor') or sr.get('from_anchor_id')==wr.get('sightline_anchor'): candidates.append(sr)
                    elif kind in {'EXTERIOR_INTERIOR_SAME_ENTITY','SAME_LOCATION_DIFFERENT_LAYER'} and sr.get('relation_kind') in {'EXTERIOR_INTERIOR_SAME_ENTITY','SAME_LOCATION_DIFFERENT_LAYER','INSIDE_SAME_ENTITY','CONTAINS'}:
                        if sr.get('from_entity_id')==wr.get('from_location_id') and sr.get('to_entity_id')==wr.get('to_location_id'): candidates.append(sr)
                    elif kind in {'ADJACENT','CONTAINS'} and sr.get('relation_kind')==kind and sr.get('from_entity_id')==wr.get('from_location_id') and sr.get('to_entity_id')==wr.get('to_location_id'): candidates.append(sr)
                if kind!='UNRELATED' and not candidates:
                    issues.append({'type':'SHOT_RELATION_SPATIAL_CONTRADICTION','relation_id':rid,'relation_kind':kind,'from':wr.get('from_location_id'),'to':wr.get('to_location_id')})
    return {'pass':not issues,'location_count':len(locs),'spatial_relation_count':len(rels),'event_node_count':len(evs),'character_route_count':len(routes),'planning_diagram_count':len(diagrams),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--spatial-canon',required=True); ap.add_argument('--relation-graph'); a=ap.parse_args()
    out=lint(load(a.spatial_canon),load(a.relation_graph) if a.relation_graph else None); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
