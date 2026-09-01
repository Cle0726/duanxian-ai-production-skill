#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(rel): return (ROOT/rel).read_text(encoding='utf-8')

video=read('templates/video_prompt_template.md')
compiler=read('templates/prompt_compiler.md')
dedup=read('templates/prompt_semantic_deduplication_engine.md')
sanitizer=read('templates/model_facing_prompt_surface_sanitizer.md')
egress=read('templates/prompt_egress_gate.md')
skill=read('SKILL.md')
style=read('templates/style_authority_projection_gate.md')
route=read('controller/route_registry.yaml')
refsem=read('templates/execution_reference_semantics.md')
visroute=read('templates/visual_reference_routing.md')
solver=read('templates/prompt_constraint_solver.md')

required=[
 '镜头目标','起始状态','人物外观/服装必要确认','场景空间','道具状态','构图','景别','摄影机','时间轴','逐段动作',
 '表演','视线','肢体占用','物理反馈','环境动态','光影综合色','声音','对白/呼吸','结尾状态','必要负面限制'
]
for term in required:
    assert term in video, f'missing prompt control field: {term}'
assert 'PROMPT_LENGTH_CEILING = NONE' in video and 'PROMPT_LENGTH_CEILING = NONE' in compiler and 'PROMPT_LENGTH_CEILING = NONE' in skill
assert '@当前Shot Execution Frame' in video
assert 'Scene Color Card只在`DIRECT_REFERENCE`模式下额外@' in video
assert 'LINEAGE_ONLY / TEXT_CONTROL / DIRECT_REFERENCE' in video
assert 'Dedup ≠ Short Prompt' in video
assert '镜头执行分析' in sanitizer and '镜头执行分析' in egress
assert '正常Final Video Master Prompt按`video_prompt_template.md`执行`PROMPT_LENGTH_CEILING = NONE`' in dedup
assert '模型Prompt必须短、清楚、无语义复读' not in compiler
assert 'Concise Compile' not in video
assert '只保留1句最关键' not in style
stage05=route.split('  STAGE_05_VIDEO:',1)[1].split('  STAGE_05_VIDEO_QC:',1)[0]
character=route.split('  CHARACTER_MASTER:',1)[1].split('  TRANSFORMATION_FIRST_DESIGN:',1)[0]
assert 'validators/video_prompt_detail_lint.py' in stage05
assert 'validators/video_prompt_detail_lint.py' not in character
assert '视觉Reference已经画清的人物外观、环境固定几何、综合色不重复描述' not in video
assert '已有Approved视觉Reference承担的静态事实（人物长相、环境结构、综合色、构图、画风）默认不在Prompt再次长篇描述' not in refsem
assert 'REFERENCE ROUTING ≠ PROMPT COMPRESSION' in visroute
assert 'REFERENCE_TEXT_SUPPRESSION_CONFLICT' in solver and 'PROMPT_DENSITY_POLICY_CONFLICT' in solver
print('V4.5.7 prompt restoration tests: PASS')
