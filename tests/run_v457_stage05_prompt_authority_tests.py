#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(rel): return (ROOT/rel).read_text(encoding='utf-8')

skill=read('SKILL.md')
refsem=read('templates/execution_reference_semantics.md')
visroute=read('templates/visual_reference_routing.md')
dedup=read('templates/prompt_semantic_deduplication_engine.md')
sanitizer=read('templates/model_facing_prompt_surface_sanitizer.md')
route=read('controller/route_registry.yaml')
lint=read('validators/video_prompt_detail_lint.py')

assert 'Stage 05 Prompt Authority Order' in skill
assert '不拥有Stage 05正文长度、详细度或导演信息裁剪权' in refsem
assert 'REFERENCE ROUTING ≠ PROMPT COMPRESSION' in visroute
assert '不拥有“详细度裁剪”权' in dedup
assert '不得用于缩短Final Video正文' in sanitizer

for key in ['TARGET','ENTRY_STATE','HUMAN_WARDROBE','SCENE_SPACE','PROP_STATE','COMPOSITION','SHOT_SIZE','CAMERA','TIMELINE','SEGMENTED_ACTION','PERFORMANCE','EYELINE','LIMB_OCCUPANCY','PHYSICAL_FEEDBACK','ENV_DYNAMICS','LIGHT_COLOR','SOUND','DIALOGUE_BREATH','ENDING_STATE','NECESSARY_RESTRICTION']:
    assert repr(key) in lint or ("'"+key+"'") in lint, key

stage05=route.split('  STAGE_05_VIDEO:',1)[1].split('  STAGE_05_VIDEO_QC:',1)[0]
character=route.split('  CHARACTER_MASTER:',1)[1].split('  TRANSFORMATION_FIRST_DESIGN:',1)[0]
assert 'validators/video_prompt_detail_lint.py' in stage05
assert 'validators/video_prompt_detail_lint.py' not in character
print('V4.5.7 Stage 05 prompt authority tests: PASS')
