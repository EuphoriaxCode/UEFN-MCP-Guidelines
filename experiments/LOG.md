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
  and ✅ **the editor viewport does show it** — but only after the material instances finish compiling (captures right after
  setting were still grey; a capture minutes later shows red/green/blue/gold, `screenshots/vfxdemo_editor.png`). *(corrected in E19)*
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

### E15 ✅ Lab 3 — players as entities, triggers, and the one-tick collision lag
```
P01 PASS player as entity:  entity-global (0, 0, 0) char UE(-246, 771, 486) comps 3 children 0 has parent;
P02 PASS child entity parented to the player: halo global (0, 0, 220)
P03 PASS mesh EntityEnteredEvent with a player (teleported onto a non-collidable pad): enter:entity@1042.396 exit:entity@1042.430
P04 FindSweepHits per-hit detail (probe at (3100,-2500,950)): [1] other at (2500,-2500,410) d=0 move=(-600,0,-500) [2] TARGET d=0 move=(-600,0,-500)
P04b FindSweepHits with a collision_sphere volume: 0 hits
P05 enter/exit timeline (both non-collidable): in×4 @1045.4015, out×4 @1045.4349, in@1046.136, out@1046.737
P06 FAIL FindOverlapHits(transform, collision_sphere): r200: 0 hits; r400: 0 hits
```
- `agent := class(entity)`, `player := class(agent)` — but the **player entity is not spatial** (global transform (0,0,0),
  3 components, has a parent). Children parented to a player stay at world origin; they do NOT follow the character.
- Mesh `EntityEnteredEvent` fires for the player's character, but `Other` is neither `player` nor `agent` (some character entity).
- **Hypothesis (one explanation for all anomalies):** a freshly spawned entity's collision body stays where the entity was added
  (the parent's origin) until the next tick, even after `SetLocalTransform`. Evidence: sweep "move" vector (−600,0,−500) takes the
  probe exactly to the root origin; spawn-time enter/exit bursts; overlap queries at the visual positions find nothing.
  The mover passing through the gate later produced exactly one clean in/out pair → events themselves work. → verified in E16.
- `collision_sphere{Radius := 20.0}` is constructible from Verse and accepted by `FindSweepHits/FindOverlapHits(transform, volume)`.

### E16 ✅ Lab 4 — collision lag confirmed, the clean spawn pattern, following a player
```
Q01 PASS overlap query finds a just-moved entity only after a tick: same frame 0, after Sleep(0) 1, after 0.1 s 1
Q02 PASS SetGlobalTransform BEFORE AddEntities avoids the lag: same frame 1, after Sleep(0) 1, at (5800, -10000, 900)
Q03 PASS FindSweepHits after the bodies settled: TARGET d=400.000000 contact=(3750,-5050,500) n=(0,0,100)
Q04 PASS orb follows the character via TickEvents.PostPhysics: gap 0.000000 cm after 30 ticks
```
- **Confirmed:** after `AddEntities` + `SetLocalTransform` in the same frame, the collision body is still at the parent origin.
  Queries (`FindOverlapHits`, `FindSweepHits`) and enter/exit events see the stale position until the next tick → `Sleep(0.0)`.
- On an entity that is **not yet in the scene**, `SetGlobalTransform` is stored as the **local** transform: setting
  parent+offset then adding under the parent put it at parent+parent+offset (5800,−10000,900). Use `SetLocalTransform`
  before `AddEntities` → body is created at the right place immediately (no lag).
- Sweeps are exact once settled (distance 400 for a 500 cm gap between 100 cm cubes, normal +Up).
- Following a player: player entities aren't spatial → a component that sets `Entity.SetGlobalTransform(char pos + offset)`
  in `TickEvents.PostPhysics` tracks with 0 cm error at the 30 Hz server tick.

### E17 ✅ Prefab classes: instancing + per-instance overrides work; creation still impossible
- Cooked engine prefabs exist only as generated classes (`/EntityFramework/ReplicationTest/Prefab_RepTest_ParentChild.Prefab_RepTest_ParentChild_C`);
  `AssetTools.get_asset_class` says the asset doesn't exist and `ObjectTools.list_properties` on the class/CDO returns nothing.
- `uefn sg new PrefabTest --cls <prefab _C>` → instance with its children (`ChildOne`, `ChildTwo/SubChildThree`; prefab child
  names have no random suffix). `sg dump` reads it back with `"class"`.
- Overrides on an instance all worked: `AddComponent` on a prefab child, moving a child, adding a new child entity.
- ⇒ The only missing step is creating the prefab asset (human: Outliner → Create Prefab). Everything after that is scriptable.

### E18 ❌ 3D text (`text_display_component`) text can't be set by the agent
- `Message` holds an object path to a `Verse_message` (default `/EntityFramework/_Verse/VNI/Component.Default___Root:__verse_0x41502826_EmptyMessage`).
- `SetComponentProperty(Message, "Hello")` → "not a valid object path"; JSON objects are silently ignored.
- Module-level `<localizes>` messages live as subobjects `Default___Root:__verse_0x<hash>_<Name>`; the hash isn't CRC32/FNV/MD5
  of the obvious Verse paths, and `_Root` objects expose no properties → no way found to reference a message object. Open.
- `Font` is an instanced `Assets_font` with `assetForEditor` (same pattern as material slots).

### E19 ✅ Niagara VFX created by tool → Scene Graph components
- `NiagaraToolset_System.CreateNiagaraSystem(assetName, assetPath, templateSystem)` from engine templates
  (`/Niagara/DefaultAssets/Templates/Systems/{FountainLightweight,RadialBurst,SimpleExplosion,MinimalLightweight}`) ✅;
  `AddEmitter(system, templateEmitter=/Niagara/DefaultAssets/Templates/Emitters/ConfettiBurst, emitterName)` ✅ (GPU sprite emitter).
  `GetSystemCompileState` → `UpToDate` (confetti still compiling right after adding the emitter).
- After save + `BuildAll`: component classes `SGKit-VFX-NS_SG_{Fountain,Burst,Explosion,Confetti}`, editables
  `Enabled, AutoPlay, AutoPlayInEditor, TickPostPhysicsInternal`. Placed with `uefn sg apply examples/sg-lab/vfxdemo.json`;
  the fountain + particles render in the editor viewport (`screenshots/vfxdemo_editor.png`).
- Correction to E13: per-instance editor materials via `assetForEditor` DO render once the MI shaders are compiled.

### E20 ✅ Showcase: "Light Up The Floor" (`examples/floor-game`)
- One Verse device builds a 5×5 board of custom-mesh tiles with their own materials, invisible trigger children,
  keyframed pillars, a following orb + light; tiles glow and fire a Niagara burst when stepped on; confetti + reset on win.
- Self-test (teleport snake walk): every tile lit exactly once, in order, ~0.37 s apart; `ROUND 1 COMPLETE`; reset after 4 s.
- Runtime VFX: `NS_SG_Burst{Entity := entity{}}` added as a child entity auto-plays; `RemoveFromParent()` after N s cleans up.
- Editor-placed KitDemo shapes kept their per-instance editor materials in game (red/green/blue/gold) → E13 editor path works end to end.
- Verse traps hit: a field named `Round` collides with built-in `Round()` (3532/3588) — same family as `Floor`;
  a local declared twice in one function (even in sibling scopes) is an error (3532 "ambiguous with ... G").
- `PushChanges(bVerseOnly=true)` while the game runs → "The Refresh command is not currently available"; a full push works
  (CLI `session restart --verse-only` now falls back automatically).
- Verse `Print` lines show on the client HUD in play-tests (top-left), handy for screenshots.

### E21 ✅ CLI fast build + spec prefabs verified live
- `uefn sg build maze12.json` (from `examples/procgen/maze.py 12 12 --seed 7`): **128 entities + 128 components in 5.9 s,
  one `execute_tool_script` round-trip, 0 errors** (`examples/procgen/maze_12x12.png`). ~23 ms per inner tool call —
  not faster than turbo MCP calls, but immune to the 333 ms background throttle.
- Spec prefabs (`examples/spec-prefabs/lamp.json`): `sg stamp` ×3 with overrides (shade material per lamp via
  `{"material": MI}`, red bulb colour on one) → sidecar `lamp.instances.json` records transforms + overrides.
  Edited the template (taller pole, moved bulb/shade, Intensity 300→800, new `Cap` child) → `sg propagate`:
  `created 3, updated 15, instances 3`; read-back: all bulbs at local z 210 with Intensity 800, LampRed's bulb still red,
  all three have `Cap` (`examples/spec-prefabs/lamps_propagated.png`).

### E22 ✅ Scene Graph camera takes over the player view; items as entities (`sglab5_device.verse`)
```
C01 player: 3 components, 0 child entities, 0 inventory components, 0 items
C02 no inventory_component under the player
C03 bandage entity in world: 8 components, 0 children, at (-1900, 0, 500)
C04 camera directors under player: 1
C04 AddCamera succeeded; holding for 12 s  ...  camera released
```
- **Every player has a `camera_director_component`.** `Director.AddCamera[perspective_camera_component, 100]` switched the client
  to our camera (top-down over the floor game, `screenshots/lab5_sheet.jpg`); `Handle.Cancel()` gave the view back.
  Experimental: compiles with **warning 2304** "… is experimental, and its use will prevent you from publishing your project".
- `uefn build` now treats warnings as success (it used to exit 1 on any diagnostic).
- The player entity has **no `inventory_component`** → `inventory_component.AddItem` can't target Fortnite inventories this way (42.30).
- `Bandage_BR_CH5S1_Common{}` (from `/Fortnite.com/Items`) spawns into the world as an entity with 8 components
  (pickup behaviour not yet verified by a human).
- Generators (`FindDescendantComponents` results) have no `.First`/indexing → materialise with `for (X : Gen) {X}` first.

### E23 ✅ Paint Blaster: input hooks + hand-integrated projectiles + runtime repaint (`examples/paint-blaster`)
- Non-experimental input actions available to Verse (`/Fortnite.com/Input/Character`): `Jump, Crouch, Sprint` (TraversalMapping),
  `WeaponPrimary, WeaponSecondary, Reload` (RangedWeaponMapping). `Move` (vector3) and `Interact` are **experimental**.
- Subscribing `GetPlayerInput[P].GetInputEvents(Jump).TriggerActivationEvent` works (log line); real presses need a human.
- Projectile = entity moved each `PostPhysics` tick by `Velocity*Dt`, collision via `Entity.FindSweepHits(Step)` excluding itself.
  AutoFire self-test: **8 shots, 8 hits, 8 painted**; contact points exactly on the targets' front faces.
- Editor-placed entities with kit meshes can be repainted at runtime: `GetComponent[SM_SG_cube]` → `set Mesh.Main = M_SG_Color{}`.
- View ray: `FromRotation(fort_character.GetViewRotation()).GetForwardAxis()` (in the bridge file; type-annotate the
  converted rotation as `(/Verse.org/SpatialMath:)rotation` so `GetForwardAxis` resolves).
