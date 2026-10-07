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
