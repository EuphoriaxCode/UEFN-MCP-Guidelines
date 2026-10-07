# Scene Graph at runtime (Verse) — verified patterns

UEFN 42.30. Every pattern below ran in a live session; evidence IDs point to `experiments/LOG.md`
(labs in [`examples/sg-lab`](../examples/sg-lab)). Editor-side authoring is in [`scene-graph.md`](scene-graph.md).

## Spawning
```verse
using { /Verse.org/SceneGraph }
using { /Verse.org/SpatialMath }
using { /UnrealEngine.com/BasicShapes }

SpawnCube(Parent:entity, Local:transform):entity =
    E := entity{}
    E.AddComponents(array{transform_component{Entity := E}, cube{Entity := E}})
    E.SetLocalTransform(Local)       # BEFORE AddEntities: the collision body is created in the right place (E16)
    Parent.AddEntities(array{E})     # enters the scene: OnAddedToScene -> OnBeginSimulation -> OnSimulate
    E
```
- Root for runtime content: `GetSimulationEntity[]` from a `creative_device` (or `Entity.GetSimulationEntity[]` from a component).
- Components need their entity at construction: `cube{Entity := E}`; then `E.AddComponents(...)` (E12).
- 100 entities in one frame: fine. 2000 cubes: the server drops from 30 → ~24.5 Hz (E14).
- Remove: `E.RemoveFromParent()`; re-add later with `Parent.AddEntities` (E12).

### ⚠️ The one-tick collision lag (E15, E16)
If you `AddEntities` first and `SetLocalTransform` after, the **collision body stays at the parent's origin until the next tick**.
Overlap/sweep queries and `EntityEnteredEvent` see the stale position (sweep distances 0, phantom enter/exit bursts).
- Fix A: set the **local** transform *before* `AddEntities`.
- Fix B: `Sleep(0.0)` before querying.
- Trap: on an entity not yet in the scene, `SetGlobalTransform` is stored as **local** — it ends up offset twice once parented.

## Transforms & axes
- `/Verse.org/SpatialMath` uses `vector3{Forward, Left, Up}`. **Forward = Unreal +X, Left = Unreal −Y, Up = +Z** (E14).
- `GetGlobalTransform/SetGlobalTransform`, `GetLocalTransform/SetLocalTransform` (E12).
- Re-parenting with `NewParent.AddEntities(array{E})` **keeps the global transform** (local is recomputed) (E12).
- Fortnite APIs (`fort_character.GetTransform/TeleportTo`, `creative_device.GetTransform`) still use the old
  `/UnrealEngine.com/Temporary/SpatialMath` (`X/Y/Z`). Convert with `FromVector3`/`FromRotation`/`FromTransform`.
  A qualified `(/Mod:)Name` only resolves when the module is also imported with `using`; importing both SpatialMath
  modules makes `vector3`/`rotation` ambiguous → keep the bridge in its own file
  ([`sglab_teleport.verse`](../examples/sg-lab/verse/sgkit/sglab_teleport.verse)).

## Custom meshes with per-entity materials (E13, E14)
1. Generate/import a mesh (`uefn` meshgen + `StaticMeshTools.import_file`), create a material with parameters, `BuildAll`.
2. The Assets digest now has `SM_X := class<final>(mesh_component){ var <Slot>:material }` and
   `M_X := class(material){ var Color:color; var Glow:float ... }`.
3. Verse (the file must live in the **parent folder of the asset folders** — asset folders are internal modules):
```verse
using { Meshes }       # from SGKit/ where SGKit/Meshes and SGKit/Materials are asset folders
using { Materials }
C := SM_SG_cube{Entity := E}
M := M_SG_Color{}                       # a material INSTANCE owned by this entity
set M.Color = MakeColorFromHSV(30.0 * I, 1.0, 1.0)   # Hue 0..360
set C.Main = M
# later, every tick if you like:
set M.Glow = 2.0 + 2.0 * Sin(T * 4.0)
```
- Live per-entity colour/glow animation from `TickEvents` works (screenshot `examples/sg-lab/screenshots/client_lab2.png`).
- `BasicShapes.*` have no material slot — use your own meshes when you need colour.

## Queries
- `Root.FindDescendantEntitiesWithTag(tag_type)` honours tag subclasses (E12). Tags: `my_tag := class(tag){}`; `E.AddTag(my_tag{})`.
- `E.FindOverlapHits()`, `Root.FindOverlapHits(transform, collision_sphere{Radius := R})` — free volume queries (E15/E16).
- `E.FindSweepHits(Displacement)` returns hits sorted by distance; blocking hit last; distances exact once settled (E16).
- Compare hits with `Hit.TargetComponent.Entity = SomeEntity` (entities are comparable).

## Events & ticking
- `TickEvents.PrePhysics/PostPhysics.Subscribe(OnTick)` in `OnBeginSimulation`, cancel in `OnEndSimulation`. Server tick = **30 Hz** (E12).
- Scene events: `my_event := class(scene_event){...}`; `Parent.SendDown(E)` / `Child.SendUp(E)`; components override
  `OnReceive<override>(SceneEvent:scene_event):logic` (return true to consume). Each listener got both events (E12).
- Mesh triggers: `Mesh.EntityEnteredEvent / EntityExitedEvent` (set `Collidable := false`, keep `Queryable`). One clean
  in/out per pass once the spawn lag is avoided (E15). The **player's character triggers them**, but the `Other` entity is
  neither `player` nor `agent`.

## Keyframed movement (E12)
```verse
KM := keyframed_movement_component{Entity := E}
E.AddComponents(array{KM})
KM.SetKeyframes(array{
    keyframed_movement_delta{Transform := transform{Translation := vector3{Forward := 0.0, Left := 0.0, Up := 300.0},
                                                    Rotation := IdentityRotation(), Scale := vector3{Forward := 1.0, Left := 1.0, Up := 1.0}},
                             Duration := 1.0, Easing := ease_in_out_cubic_bezier_easing_function{}}},
    oneshot_keyframed_movement_playback_mode{})   # or loop_ / pingpong_
KM.Play();  KM.FinishedEvent.Await()
```
- Deltas are **relative and cumulative**, applied in **parent space** (a yaw in delta 1 does not rotate delta 2's translation).
- No editor properties — keyframes only from Verse.

## Players
- `agent := class(entity)`, `player := class(agent)`, but a **player entity is not spatial** (global transform (0,0,0)).
  Children parented to a player stay at the world origin (E15).
- To attach things to a character: a component that sets `Entity.SetGlobalTransform(char pos + offset)` every
  `PostPhysics` tick — 0 cm lag at 30 Hz (E16).
- `fort_character.TeleportTo[old vector3, old rotation]` works for moving players into test positions (E14).

## Per-player visibility (E14)
- `E.SetPresentableToPlayers(option{array{}})` hid an entity from the (only) player while a sibling stayed visible.
  Doc: `false` = everyone, `option{array}` = only those players.

## Lights
- `sphere_light_component{Entity := E}` added at runtime; `set L.Intensity`, `set L.CastShadows`, `Enable()/Disable()`,
  `set L.ColorFilter` (E12, lamp showroom).
