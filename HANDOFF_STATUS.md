# V4.5.7 Temporal Reference Hygiene — IMPLEMENTED / LOGIC-CLOSED

## Release status — 2026-08-27

Temporal Reference Hygiene / Adaptive Continuation is now implemented in the executable source tree. The design-handoff text below is retained as historical architecture context; statements saying the Temporal implementation is not present are superseded by this release status.

Validated release facts:

- 37 / 37 `tests/run_*tests.py` suites PASS on the final frozen source tree.
- Temporal adversarial suite covers Ending Anchor provenance, recursive Snapshot lineage, Provider t=0 semantics, T0 sufficiency / reset, `TEMPORAL_T0_BAKED`, internal-conditioning-primary vs model-t0-primary separation, same-take auxiliary visual isolation, cross-artifact fingerprints, downstream Snapshot revalidation, Controller gates, and Failure Router coverage.
- YAML / Python / State+Runtime schema / Architecture / Gate Producer release audit is clean.
- Generic all-round reference capability is explicitly **not** treated as proof of first-frame or endpoint semantics.

---


## Purpose

This package is a **new-session handoff RC**, not a claim that the Temporal Reference Hygiene implementation is already complete.

The executable source tree is based on the last persisted and audited baseline:

- Base package: `skill_v4.5.7_voice_direction_logic_closed_release_20260824.zip`
- Base SHA256: `f1e466236b740acf772fe81ac55bb13908feddb89f2535e7c9cd8f3a5e01be59`

Important: the previous conversation designed and iterated a substantial Temporal Continuation upgrade, but the live worktree from those turns is not present in the current runtime filesystem. Therefore this handoff intentionally preserves the stable baseline and adds the exact engineering specification required to continue safely in a new session. Do **not** assume the Temporal files described below already exist in source code.

## Current production baseline already present

The baseline already includes the V4.5.7 production architecture, including the existing Controller / Schema / Validator / Failure Router / Generation Job flow, Contact Sheet First, Entity Binding, Base Visual Authority, Spatial Continuity / Multiview, Generation Envelope, Adaptive Video Reference Budget, and the Voice Direction / Prosody logic closure.

## Temporal problem being solved

Long-form video continuation by recursively reusing the previous clip's tail frame causes two coupled failure families:

1. **Recursive pixel degradation** — blur, noise, color drift, gamma drift, identity softness, texture collapse.
2. **Authority collision at the generation boundary** — the previous tail frame says “continue exactly from here” while Shot Execution Frame, Character Canon, Environment Master, Scene Color Card, props, and a fully restated prompt simultaneously ask the provider to reconstruct a different t=0.

The key architectural conclusion is:

> Internal production authority should remain complete, but model-facing visual conditioning at t=0 must be sparse and mode-specific.

Equivalent rule:

> Pixels own the present. Prompt owns the future. Canon owns the next legal reset.

## Required continuation modes

`TEMPORAL_ENTRY_PLAN` should distinguish at least:

- `SEAMLESS_EXTEND`
  - Same shot / same take continuation.
  - Previous verified Ending Anchor is the **only model t=0 visual owner**.
  - Use `DELTA_CONTINUATION_PROMPT`.
  - Ordinary static visual direct references are isolated from the provider input.

- `GUIDED_CONTINUATION`
  - Same shot continuation with a real target / endpoint frame.
  - Previous Ending Anchor = start endpoint.
  - Target frame = end endpoint.
  - Use `TRANSITION_PROMPT`.
  - Provider must support real first/last or endpoint semantics; a generic reference slot is not sufficient proof.

- `CUT_REPROJECT`
  - A real editorial cut occurs.
  - Do **not** preserve previous screen-left/screen-right as world truth.
  - Reproject `WORLD_SPATIAL_STATE` through a new `CAMERA_TOPOLOGY_STATE`.
  - New Shot Execution Frame becomes model t=0 primary.
  - Use `FULL_SHOT_PROMPT`.

- `SCENE_REBASE`
  - New scene / legal reset boundary.
  - Canon, Environment Master, Scene Color Authority, and normal visual reference logic may fully reacquire authority.
  - Pixel lineage depth resets.

## Critical distinction: two kinds of “Primary Visual”

The upgrade must explicitly separate:

- **Internal Conditioning Primary** — e.g. a high-quality Shot Execution Frame used by planning, identity QC, blocking QC, spatial checks, future-state reasoning.
- **Model t=0 Primary** — the image or transport mechanism that actually owns the provider's first frame.

For `SEAMLESS_EXTEND`:

- Internal Conditioning Primary may still be the Shot Execution Frame.
- Model t=0 Primary must be the verified previous Ending Anchor.
- A Shot Execution Frame must not be silently reintroduced as a second `PRIMARY_VIEW` merely to satisfy an old Generation Job gate.

Required hard failure:

- `TEMPORAL_T0_MULTIPLE_PRIMARY_VISUAL_CONFLICT`

## Continuation Visual Isolation

For same-take continuation, generic provider reference slots cannot be trusted to honor our internal time-scope metadata. Therefore:

### SEAMLESS_EXTEND

Direct visual provider inputs:

- allowed: previous Ending Anchor through a verified t=0 transport
- forbidden by default: Character Canon, FMH Master, Prop Canon, Environment Master, Scene Color Card, Shot Execution Frame, arbitrary static reference images
- audio references may still be allowed where the provider supports them independently

Canon assets remain internal authority / lineage / QC sources, but they are not necessarily sent as direct visual references at the continuation boundary.

### GUIDED_CONTINUATION

Direct visual endpoints:

- previous Ending Anchor
- real Target Frame

Do not also send a large static reference pack unless the provider has an explicitly verified endpoint/reference separation mechanism.

Required conflict failure:

- `TEMPORAL_CONTINUITY_AUXILIARY_VISUAL_REFERENCE_CONFLICT`
- `TEMPORAL_CONTINUITY_DIRECT_COLOR_REFERENCE_CONFLICT`

## Entity Binding versus Temporal Isolation

Existing Entity Binding may conclude that an entity requires `DIRECT_REFERENCE` due to identity, prop, or readability risk. That can conflict with same-take visual isolation.

Do **not** solve this by sending both Tail + Character Master.

Add a `TEMPORAL_T0_SUFFICIENCY_ASSESSMENT` layer:

- If the Ending Anchor already contains sufficiently readable / stable evidence for the required entity:
  - resolve entity mode as `TEMPORAL_T0_BAKED`
  - suppress the auxiliary direct visual reference

- If the Ending Anchor is insufficient:
  - return `TEMPORAL_RESET_REQUIRED`
  - do not force more visual references into the same-take boundary
  - search for a legal reset such as Cut, Reaction, Insert, Occlusion, Match-on-action, significant framing change, or scene boundary

Principle:

> If a seamless continuation can only preserve identity by introducing a competing static visual reference, that generation boundary is probably not a valid seamless boundary.

## Provider transport semantics

An asset token or generic `@reference` must not be assumed to mean “first frame”.

Add a transport contract with explicit verified capability, e.g.:

- `NATIVE_VIDEO_EXTEND`
- `FIRST_FRAME_INPUT`
- `FIRST_LAST_KEYFRAME`
- `TARGET_FRAME_INPUT`
- `NAMED_REFERENCE_WITH_T0_SEMANTICS`
- `ORDERED_REFERENCE_WITH_T0_SEMANTICS`
- `NAMED_ENDPOINT_TARGET`
- `ORDERED_ENDPOINT_TARGET`
- `MANUAL_VERIFIED`

Required fields should include:

- `t0_semantics_verified`
- `capability_evidence_ref`
- for guided continuation, endpoint / target semantics verification

A generic provider reference slot cannot impersonate a verified first-frame or last-frame channel.

## Ending Anchor authenticity and selection

Do not mechanically select the literal final encoded frame.

Build an Ending Anchor from the final tail window using real decodable frame timestamps, balancing:

- proximity to the real end state
- sharpness / identity readability
- artifact avoidance
- motion-state correctness

A candidate several frames before EOF can be better than the final frame if the final frame is blurred or corrupted but the action state is already effectively complete.

Valid provenance modes should include at least:

- `LOCAL_DECODED_VIDEO`
- `PLATFORM_EXTRACTED_VERIFIED`

A user-supplied arbitrary PNG must not be allowed to impersonate a true ending frame without provenance.

For platform-extracted frames, require evidence such as:

- source video fingerprint
- extraction proof reference

Add independent validation so the tool that captures the frame is not also the sole authority declaring itself valid.

Expected validator:

- `validators/continuity_snapshot_lint.py`

It should validate at minimum:

- Ending Anchor exists
- actual hash matches recorded hash
- source video fingerprint is present
- extraction provenance is allowed
- prior snapshot chain is valid when recursive continuation is used
- pixel lineage depth is derived rather than self-declared
- degradation debt values are structurally valid

## Pixel lineage and degradation debt

Recursive generated pixels should carry explicit generation lineage.

Example:

- Canon / source-quality image: depth 0
- first generated tail used as continuation input: depth 1
- next recursive tail: depth 2

The current depth should be derived from the previous continuity snapshot, not supplied manually.

Suggested fields:

- `previous_continuity_snapshot_ref`
- `previous_continuity_snapshot_fingerprint`
- `pixel_lineage_depth`
- `lineage_evidence_mode`

Hard failures should prevent:

- manual lineage reset during seamless continuation
- claiming depth 0 while continuing from a generated tail
- depth > 1 without a verifiable previous snapshot

A real Cut/Rebase can legitimately reset recursive pixel lineage.

Track quality debt separately, for example:

- sharpness debt
- chroma / gamma drift debt
- noise debt
- identity debt
- generation depth

Do not automatically perform a visible hard color / quality correction at a same-take seam. Prefer paying this debt at a legal reset or in Stage 06 color matching.

## Color continuity versus color accuracy

For same-take continuation boundary:

- `COLOR_CONTINUITY > COLOR_ACCURACY`
- Previous Ending Anchor's current pixel color state wins at t=0.
- Scene Color Authority remains valid internally but should not normally be added as a direct image reference competing at the seam.

For a true Cut / Scene Rebase:

- `COLOR_ACCURACY` may retake priority.
- Scene Color Authority can be applied normally.

Stage 06 should handle cross-clip color matching / debt repayment where possible.

## Continuity grace window

For seamless continuation, consider a short grace window immediately after t=0 in which the system explicitly avoids visible re-design / re-lighting / re-coloring events.

The grace window should preserve:

- pose momentum
- gaze momentum
- camera velocity
- prop state
- body orientation
- lighting continuity

Canon stabilization after the seam must be subtle and non-eventful, not a visible “correction ramp”.

## Motion Capsule

A single tail frame cannot encode velocity or action direction.

Add an internal `continuity_motion_capsule` derived from recent frames and current state, potentially including:

- last stable pose
- velocity direction
- camera velocity
- body momentum
- gaze velocity
- prop velocity
- action phase
- expected next phase

The model-facing prompt can then describe only the motion delta, rather than re-describing all static facts.

## Overlap continuation

Do not force every segment join to a single exact frame.

Support generation overlap handles so two adjacent clips can share a short motion region. Stage 06 can search the overlap for the best splice based on pose / camera / motion / color similarity and trim duplicates.

Suggested concept:

- `generation_overlap_handle`

This reduces pressure on one tail frame to be simultaneously perfect in composition, motion, color, and quality.

## Camera topology for cuts

A true Cut should not use previous-frame screen position as world-space truth.

Add structured camera topology, e.g.:

- `camera_zone`
- `viewing_direction`
- `axis_side`
- `height_band`
- `lens_family`
- `subject_distance_band`
- `target_anchor`
- `foreground_occlusion`
- `visible_environment_faces`

At minimum, a same-scene Cut should not be considered fully specified with an empty camera topology shell. The previously discussed minimum proof was:

- `camera_zone`
- `viewing_direction`
- `axis_side`
- `target_anchor`

Then compute frame projection from World Spatial State through the new camera state.

## Prompt compilation profiles

Keep the internal `VIDEO_EXECUTION_PLAN` complete. Do not equate internal completeness with provider prompt length.

Required profiles:

### FULL_SHOT_PROMPT

Use for:

- scene opening
- real cut / reprojection
- text-to-video style generation
- canonical restart

May include full subject, environment, camera, lighting, spatial, performance, color, and reference instructions as appropriate.

### TRANSITION_PROMPT

Use for guided start→target continuation.

Focus on:

- motion path
- camera path
- performance transition
- timing
- landing / endpoint

Do not fully re-describe the starting image.

### DELTA_CONTINUATION_PROMPT

Use for seamless extend.

Focus on:

- what changes next
- momentum continuation
- camera continuation
- action phase
- performance / dialogue / sound as needed
- landing

Do not fail merely because the prompt is much shorter than a full-shot prompt.

Internal labels such as `SEAMLESS_EXTEND`, `TEMPORAL_ENTRY_PLAN`, or pipeline gate names should remain internal metadata and should not leak into model-facing prose. Natural-language equivalents are fine.

## Existing rule conflicts that must be audited

When implementing the upgrade, specifically inspect and reconcile:

1. `segment_entry_modes.md`
   - do not require literal internal enum strings in model-facing prompt text

2. `prompt_constraint_solver.md`
   - old `REFERENCE_TEXT_SUPPRESSION_CONFLICT` logic must become entry-mode aware
   - a DELTA continuation intentionally suppresses redundant static restatement

3. `video_prompt_template.md`
   - any old “minimum prompt length” heuristic must not force full static restatement for seamless I2V continuation
   - any unconditional `@Shot Execution Frame` or `@Scene Color Card` rule must be reconciled with adaptive reference budget and Temporal Isolation

4. `generation_job_binding_lint.py` / `video_generation_job_prompt_lint.py`
   - old requirement for an Asset Registry `PRIMARY_VIEW` must not reintroduce Shot Execution Frame as a second t=0 primary during seamless continuation

5. `entity_binding_reference_resolver.py`
   - high-risk `DIRECT_REFERENCE` must be reconciled through T0 Sufficiency, not by violating visual isolation

6. platform profiles / adapters
   - must distinguish ordinary reference image support from true first-frame / extend / endpoint semantics

## Expected new or modified artifacts

The previous design discussion expected or referenced these additions. A new session should first inspect the baseline and decide exact naming before implementing:

### State / schema

- `state/temporal_entry_plan.schema.yaml`
- `state/temporal_t0_sufficiency_assessment.schema.yaml`
- extensions to `state/generation_job.schema.yaml`
- extensions to continuity snapshot / execution plan schemas as needed

### Tools

- `tools/temporal_entry_planner.py`
- `tools/temporal_t0_sufficiency_builder.py`
- ending anchor / tail-window improvements in `tools/ending_frame_capture.py`
- execution-plan and prompt/job binding propagation

### Validators

- `validators/temporal_entry_plan_lint.py`
- `validators/temporal_t0_sufficiency_lint.py`
- `validators/continuity_snapshot_lint.py`
- transport / model-t0 anti-bypass checks in generation job validators

### Templates / docs

- `templates/temporal_reference_hygiene.md`
- update segment entry, prompt compiler, prompt template, Stage 06 assembly/color matching, reference resolver, and failure diagnosis docs

### Controller wiring

Update as necessary:

- `controller/authority_registry.yaml`
- `controller/route_registry.yaml`
- `controller/gate_producer_registry.yaml`
- `controller/workflow_state_machine.yaml`
- `controller/failure_router.yaml`
- `controller/module_manifest.yaml`

## Failure codes discussed / recommended

At minimum audit or add equivalents for:

- `TAIL_FRAME_QUALITY_DEGRADED`
- `TEMPORAL_PIXEL_LINEAGE_EXCEEDED`
- `TAIL_FRAME_COLOR_AUTHORITY_VIOLATION`
- `CONTINUITY_REBASE_REQUIRED`
- `TEMPORAL_RESET_REQUIRED`
- `TEMPORAL_T0_MULTIPLE_PRIMARY_VISUAL_CONFLICT`
- `TEMPORAL_CONTINUITY_AUXILIARY_VISUAL_REFERENCE_CONFLICT`
- `TEMPORAL_CONTINUITY_DIRECT_COLOR_REFERENCE_CONFLICT`
- transport failures for missing / unverifiable native t=0 token or endpoint capability
- failures for fake ending-frame provenance and forged pixel-lineage state

## Required anti-bypass chain

The implementation should prove the same Temporal decision is bound through:

```text
CONTINUITY_SNAPSHOT
        ↓
TEMPORAL_ENTRY_PLAN
        ↓
TEMPORAL_T0_SUFFICIENCY_ASSESSMENT
        ↓
Entity Binding / Reference Resolver
        ↓
VIDEO_EXECUTION_PLAN
        ↓
Prompt Artifact
        ↓
Generation Job
```

Each downstream artifact should bind the upstream plan fingerprint / strategy strongly enough that a later stage cannot silently switch back to `FULL_SHOT_PROMPT`, re-add a competing static reference, or replace the t=0 transport without invalidation.

## Regression expectations for the next session

Do not claim final release until the implementation is present on disk and the new session has rerun the available test suite.

At minimum rerun:

- Temporal dedicated normal + adversarial tests
- Entity Binding → Video closure
- Adaptive Video Reference Budget
- Generation Envelope
- Spatial / Multiview
- Contact Sheet Storyboard
- Base Visual Authority
- Voice Direction closure
- V4.5.7 Execution Plan
- V4.5.7 Logic Closure
- V4.5.7 Integrity
- Architecture lints
- Gate Producer lint
- YAML parsing / duplicate-key checks
- JSON Schema meta validation
- Python syntax compile
- Failure Router coverage for every emitted code
- secret / cache scan

If a legacy fixture fails only because the new transport / temporal contract is stricter, migrate the fixture. Do not weaken a production gate merely to preserve an obsolete fixture.

## Release discipline

This handoff package is intentionally labeled `handoff_rc`.

Do not push to Git or call it Final until:

1. actual Temporal source changes exist on disk,
2. the full cross-layer anti-bypass chain is verified,
3. regression results are obtained in the new session,
4. the final ZIP is rebuilt from the verified worktree,
5. SHA256 and ZIP integrity are recorded.
