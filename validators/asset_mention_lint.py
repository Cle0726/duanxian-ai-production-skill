#!/usr/bin/env python3
import argparse, json, re, sys

STRONG_MODES={"MUST_BIND","DIRECT_BIND","EDIT_TARGET","PATCH_DESIGN_REFERENCE","CONTINUITY_ENTRY","PRIMARY_VIEW","SPATIAL_AUTHORITY","COLOR_AUTHORITY","STYLE_AUTHORITY","AUDIO_AUTHORITY","VOICE_AUTHORITY","RHYTHM_AUTHORITY","AMBIENCE_AUTHORITY","MUSIC_AUTHORITY","SFX_AUTHORITY"}

def load_json_or_yaml(path):
    txt=open(path,encoding='utf-8').read()
    try:
        return json.loads(txt)
    except Exception:
        try:
            import yaml
            return yaml.safe_load(txt)
        except Exception as e:
            raise SystemExit(f"Cannot parse runtime file: {e}")

def lint(prompt, runtime):
    issues=[]
    bindings=runtime.get('bindings',[]) or []
    required=[]
    known_tokens=[]
    for b in bindings:
        token=(b.get('native_token') or '').strip()
        name=(b.get('asset_display_name') or '').strip()
        mode=(b.get('binding_mode') or '').upper()
        emit=b.get('emit_on_prompt', mode in STRONG_MODES)
        if token:
            known_tokens.append(token)
        if emit and mode in STRONG_MODES:
            if not token and name:
                token='@'+name.lstrip('@')
            if not token:
                issues.append({'type':'REQUIRED_ASSET_TOKEN_MISSING','asset_id':b.get('asset_id'),'asset_display_name':name or None,'binding_mode':mode})
            else:
                required.append((token,b))
                if token not in prompt:
                    issues.append({'type':'MISSING_REQUIRED_ASSET_MENTION','token':token,'asset_id':b.get('asset_id'),'binding_mode':mode})
    # detect @mentions that cannot be reconciled to current bindings; ignore common timeline/email-like false matches by requiring CJK/word token after @
    mentions=set(re.findall(r'@[\w\-\u4e00-\u9fff]+',prompt))
    valid=set(t for t,_ in required)|set(known_tokens)
    for m in sorted(mentions):
        if m not in valid and not re.fullmatch(r'@图\d+',m):
            issues.append({'type':'UNBOUND_ASSET_MENTION','token':m})
    return {'pass':not issues,'required_mentions':[t for t,_ in required],'issues':issues}

def main():
    ap=argparse.ArgumentParser(description='Validate mandatory @asset mentions against REFERENCE_RUNTIME bindings.')
    ap.add_argument('--prompt',required=True)
    ap.add_argument('--runtime',required=True)
    a=ap.parse_args()
    prompt=open(a.prompt,encoding='utf-8').read()
    runtime=load_json_or_yaml(a.runtime)
    out=lint(prompt,runtime)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
