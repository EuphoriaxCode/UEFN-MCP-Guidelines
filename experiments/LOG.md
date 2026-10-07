# Experiment log

Append-only lab notebook. Format: **goal → run → result → lesson**. UEFN 42.30 (`++Fortnite+Release-42.30`) unless noted.
✅ worked · ❌ failed · ⚠️ partially / with caveats · 💥 crashed the editor

---

## 2026-10-07 — session 1: building the CLI

### E01 ✅ MCP surface
- Run: raw `initialize` + `tools/list` against `http://127.0.0.1:8000/mcp`.
- Result: server speaks protocol `2025-11-25`, exposes exactly 3 top-level tools: `list_toolsets`, `describe_toolset`,
  `call_tool`. `resources/list` is empty. Responses are plain JSON (not SSE). Session id via `Mcp-Session-Id` header.
- Lesson: one generic client covers everything; `describe_toolset` returns JSON with full input **and output** schemas.

### E02 ✅ Full toolset catalog
- Run: `uefn catalog` → `catalog/*.md` (+ raw JSON in `catalog/json/`).
- Result: 30 toolsets, ~400 tools. Notables never used before: `EditorAppToolset.SetCameraTransform/FocusOnActors/
  ScreenCoordsToWorld/SetCVarValue/ShowNotification`, `SceneTools.trace_world/create_level/data layers`,
  `StaticMeshTools.import_file/set_material`, `NiagaraToolset_System` (46 tools: create systems/emitters/modules),
  `PhysicsAssetToolset`, `DataTableTools`, `CurveTableTools`, `TextureTools.export_png`, `UMGToolSet.AddUIComponent`.

### E03 ❌ Hidden toolsets
- The editor log registers more toolsets (`PCGToolset`, `CheatsToolset`, `ConfigSettingsToolset`, `AutomationTestToolset`,
  `SourceControlToolset`, `UserDefinedStruct/EnumToolset`, `StateTree`, `GAS*`, `PerfToolset`, `BlueprintTools`…).
- Run: `describe_toolset` and sandbox `execute_tool("PCGToolset.PCGToolset.X")`.
- Result: "not found" / "is not registered" — filtered out for UEFN. Not reachable by any route found.

### E04 ✅ Sandbox errors are catchable
- Run: `execute_tool` of unknown tools inside `try/except` in `execute_tool_script`.
- Result: the `RuntimeError` was caught and the script continued. (Older rule said errors abort scripts even in try/except —
  that is at least not true for "unknown tool / not registered" errors. Re-check for errors raised by real tools.)

### E05 ✅ Scene Graph class inventory
- Run: `uefn sg classes`, `uefn sg classes --entities`.
- Result: **179 component classes** and **1501 entity classes** (1442 are `EntityItems/_Verse.Items-*` — every BR/Creative
  item exists as a Scene Graph entity class!). Components include `keyframed_movement`, `particle_system`, `sound`,
  `text_display` (3D world text), `decal`, cameras, `rigid_body`/`physics`, 10 modular-vehicle parts, Scene-Graph UI
  (`UI_*`), NPC/AI, inventory/items, `tag_component`, `damageable_component`.

### E06 ✅ Verse API from on-disk digests
- Digests: `%LOCALAPPDATA%/UnrealEditorFortnite/Saved/VerseProject/<Project>/Digests/BuiltIn/{Verse,UnrealEngine,Fortnite}/*.digest.verse`
  (+ the project's `*-Assets.digest.verse`). Readable without MCP.
- Tool: `uefn digest SceneGraph`, `uefn digest --grep overlap`, `uefn digest --class mesh_component --comments`.
- Saved: `catalog/scene-graph/verse-SceneGraph.txt`.
- Key APIs: `FindDescendantEntities/Components(WithTag)`, `FindOverlapHits`, `FindSweepHits`, `Get/SetGlobalTransform`,
  `Get/SetLocalTransform`, `SetOrigin`, `AddEntities`, `RemoveFromParent`, `AddComponents`, tags (`AddTag/ContainsTag`),
  `SendUp/SendDown(scene_event)` + `OnReceive`, `TickEvents.PrePhysics/PostPhysics`, keyframed movement
  (`SetKeyframes(deltas, oneshot|loop|pingpong)` + events), camera director, `PlaySkeletalAnimation`, `SetPresentableToPlayers`.

### E07 ✅ Custom meshes carry material slots (from older projects' Assets digests)
- Observed in `FindTheBrainrot_Euphoriax-Assets.digest.verse`: every project static mesh becomes
  `<MeshName> := class<final>(mesh_component)` with one `@editable var <SlotName>:material` per material slot, plus
  `<MeshName>_asset:mesh`. Materials become `class(material)` with their parameters as fields.
- `BasicShapes.cube/sphere/...` are `class(mesh_component)` with **no** slots → that's why basic shapes can't be recoloured.
- Lesson: import our own meshes to get recolourable Scene Graph meshes. (Experiment E09 tests the whole pipeline.)

### E08 💥 Component atlas — one component crashes the editor
- Run: `uefn sg atlas` (for every component class: CreateEntity → AddComponent → ListComponentProperties → DeleteEntity).
- Result: 147 classes recorded in `catalog/scene-graph/component-atlas.{json,md}`. Abstract classes are rejected cleanly
  (`light_component`, `sound_component`, `camera_component`, `stackable_component`, `fort_weapon_component`, `AI_sidekick_component`).
  **`AddComponent(UI_grid_container_component)` on a fresh entity crashed UEFN** (EXCEPTION_ACCESS_VIOLATION reading 0x48).
- Lesson: never bulk-add UI_* scene-graph components blindly; the atlas now keeps a `CRASHES` skip list.
  Remaining unprobed: the other `UI_*` widget components, `voice_manager_component`.
- Also: `keyframed_movement_component` has **no** editor-editable properties → keyframes must be set from Verse.
- `text_display_component` editables: `Enabled, Message (message ref), Font, Color, VisibleDistance{minimum,maximum}, FadeInTime, FadeOutTime`.

### E09 ✅ VFX assets become components too
- Observed in `Blindshot-Assets.digest.verse`: a Niagara system asset generates `LaserBeam_Niagara := class<final>(particle_system_component)`.
  So: create a Niagara system (NiagaraToolset_System) → Verse can construct it as a component on any entity.
- No generated `sound_component` subclasses were found in any older project digest (sounds may need a different asset type; open question).

### E10 ✅ 20–40× faster MCP: disable background throttling
- Symptom: every MCP call took exactly **333 ms** (`FindEntities` ×15). Cause: the editor runs ~3 FPS when not the foreground
  app and serves one MCP request per frame.
- Run: `uefn call object set_properties '{"instance":{"refPath":"/Script/UnrealEd.Default__EditorPerformanceSettings"},"values":"{\"bThrottleCPUWhenNotForeground\":false}"}'`
- Result: 333 ms → **8–20 ms** per call. In-memory only (resets on editor restart). Now `uefn turbo on`.
- Lesson: run `uefn turbo on` at the start of every session.

### E11 ⚠️ Shell/tool papercuts
- Git Bash rewrites arguments that start with `/` into Windows paths (`/ca93…` → `C:/Program Files/Git/ca93…`). The CLI now undoes this.
- `VerseToolset.WriteFile` requires `bCreateIfMissing`; `ListFiles` requires `bRecursive`.
- Verse: helper functions called inside `if (...)` / `for (...)` headers must be `<computes>`/`<transacts>` (error 3512);
  a local named `Floor` collides with the built-in `Floor()` (errors 3532/3588).
- `entity{}`, `transform_component{Entity := E}`, `cube{Entity := E}` (BasicShapes), `keyframed_movement_component{Entity := E}`,
  `sphere_light_component{Entity := E}`, custom `class(tag)`, custom `class(scene_event)` all **compile** (runtime results: E12).

### E08b ✅ Atlas finished
- 152 classes recorded. The remaining `UI_*` widget components were deliberately skipped (same family as the crash, and editor-only).

### E12 ✅ Runtime Scene Graph battery — 11/11 PASS (`examples/sg-lab`)
Session started with `uefn session start` (82 s), results via `uefn log "\[SGLab\]"`. Lines verbatim:
```
R01 PASS spawn entity+cube at runtime: global (2500, 0, 450) meshes under root 1
R02 PASS tags + hierarchy query: with base tag 2 (want 2), red 1 (want 1), A has base via subclass: yes
R03 PASS FindOverlapHits: hits 4, of which on B 1
R04 PASS FindSweepHits down 1000: 6 hits; first dist 0 normal (0,0,1) isFloor no
R05 PASS SendDown/SendUp + OnReceive: parent got 2, child got 2 (want 2/2); consumed down=0 up=0
R06 PASS re-parent with AddEntities: GLOBAL kept: before (3900,0,600) after (3900,0,600) local after (0,-500,-150)
R07 PASS spawn 100 cubes in one frame: 100 meshes, sim time delta 0
R08 PASS RemoveFromParent + re-add: no parent, re-added
R09 PASS keyframed movement oneshot (+300 up then +300 left): moved (0, 300, 300)
R10 PASS TickEvents.PrePhysics: 90 ticks in 3.005 s = 29.95 Hz
R11 PASS runtime sphere_light_component: lights under root 1
```
Lessons:
- Runtime construction pattern that works: `E := entity{}; E.AddComponents(array{transform_component{Entity := E}, cube{Entity := E}}); Parent.AddEntities(array{E}); E.SetLocalTransform(...)`.
- Tag queries respect the tag class hierarchy (`FindDescendantEntitiesWithTag(base)` finds subclass tags too).
- `AddEntities` re-parenting **keeps the global transform**.
- Keyframed movement deltas are **cumulative and in parent space** (the 90° yaw of delta 1 did not rotate delta 2).
- Server tick (PrePhysics) = **30 Hz**. Spawning 100 entities fits in one frame.
- Sweep: the first of 6 hits was at distance 0 and not the target cube → investigate (self-hit or initial overlap) in lab 2.
- `Verse Print` from the server shows in the editor log as `LogVerse: : [..]`.

### E13 ✅ Custom mesh pipeline: OBJ → StaticMesh → material → Verse component (editor + runtime)
Script: `experiments/e09_mesh_material.py`, meshes from `cli/uefncli/meshgen.py`.
- **Content root of new projects is `/<plugin-guid>/`**, not `/<ProjectName>/` (create_folder error lists valid roots).
  `sg.content_root()` derives it from `SceneTools.get_current_level`.
- `StaticMeshTools.import_file(import_materials=False)` keeps the OBJ `usemtl` name as the slot (`Main`).
  **Axis mapping: OBJ (x, y, z) → UE (x, −y, z)** (Z stays up, Y mirrored); probe mesh bounds proved it.
  Winding that renders front-facing (UE coords): `cross(b−a, c−a)` points *against* the outward normal. First attempt
  rendered cube/cylinder/torus inside-out and the cylinder lying down; fixed generator → all correct (`screenshots/kitdemo_v2.png`).
- `import_file` **cannot overwrite** ("already exists") → `AssetTools.delete` (check `get_referencers`) then re-import.
- After `BuildAll` each mesh is a component class `SGKit-Meshes-SM_SG_cube` (`/<guid>/_Verse/Assets.SGKit-Meshes-SM_SG_cube`)
  with property `Main` (`Assets_material*`), and the material `M_SG_Color` is a Verse class with `var Color/Glow/Roughness/Metallic`.
- Editor: `SetComponentProperty(Main, <MI asset>)` ❌ "not valid Assets_material". The slot holds an instanced `Assets_material`
  subobject whose only property is `assetForEditor`; `ObjectTools.set_properties(sub, {"assetForEditor": MI})` ✅ sets and reads back,
  but ❌ **the editor viewport keeps rendering the mesh's default material** (tried visibility toggle + move). Editor colour preview: open question.
- **Runtime (Verse) ✅**: `C := SM_SG_cube{Entity := E}; M := M_SG_Color{}; set M.Color = MakeColorFromHSV(30.0*I,1.0,1.0); set C.Main = M`
  → 12 differently coloured cubes; `set M.Color/Glow` every tick animates live (`screenshots/client_lab2.png`).
- **Verse access rule**: asset folders are *internal* modules. Code using `SGKit/Meshes` or `SGKit/Materials` must live in `SGKit/`
  (the parent folder). From `SGLab/` → error 3593 "Invalid access of internal module" + cascades ("expects a value of type false").

### E14 ✅⚠️ Runtime lab 2 (`examples/sg-lab/verse/sgkit/sglab2_device.verse`) — 6/6, two anomalies
```
L01 PASS custom mesh + per-entity material instance: 12 coloured cubes
L02 PASS material animated from TickEvents (hue + glow)
L03 FindSweepHits breakdown: 14 hits, ALL with SourceHitDistance = 0; 13 "other" entities then TARGET
L04 PASS mesh EntityEnteredEvent/ExitedEvent between two entities: entered 17, exited 17   (one pass!)
L05 PASS SetPresentableToPlayers(option{array{}}): readback array of 0; cube invisible in client, sibling sphere visible
L06 PASS spawn 2000 cube entities: spawn sim-time 0 s, then 24.5 Hz over 2 s   (client: "Performance Warning")
```
- **Verse `Left` = Unreal −Y** (verified: teleport to (F, −L, U) put the player in front of the row; hue 0 at Left −660 is on screen-right).
- `fort_character.TeleportTo` resolves to the old `(Temporary vector3, rotation)` overload; a qualified
  `(/UnrealEngine.com/Temporary/SpatialMath:)FromVector3` did **not** resolve without `using` → put the teleport in its own file
  that only uses the old SpatialMath (`sglab_teleport.verse`).
- Open: sweep distances always 0 (and 13 unrelated hits = number of custom cubes in the scene); enter/exit flicker (17 pairs).
- Budget: 2000 static cube entities cost ~20 % server tick (30 → 24.5 Hz).
