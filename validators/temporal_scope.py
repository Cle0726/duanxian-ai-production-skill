"""Shared temporal-scope semantics for constraint validators."""
from __future__ import annotations

UNIVERSAL_SCOPES={"FULL","FULL_SHOT","ALL","ENTIRE_SHOT","SHOT","GLOBAL"}

def norm(v):
    return str(v or "").strip().upper()

def numeric_interval(c):
    try:
        if c.get("start") is None or c.get("end") is None:
            return None
        return float(c.get("start")), float(c.get("end"))
    except Exception:
        return None

def overlap(a,b):
    ai,bi=numeric_interval(a),numeric_interval(b)
    if ai and bi:
        return max(ai[0],bi[0]) < min(ai[1],bi[1]) or ai==bi
    ta,tb=norm(a.get("time_scope")),norm(b.get("time_scope"))
    if not ta or not tb:
        return True
    if ta in UNIVERSAL_SCOPES or tb in UNIVERSAL_SCOPES:
        return True
    return ta==tb
