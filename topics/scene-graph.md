# Scene Graph via MCP (UEFN 42.30)

Learned building an interactive lamp showroom (see [`examples/lamp-showroom`](../examples/lamp-showroom)).
Project needs `"sceneGraph": {"bIsSceneGraphSystemAllowed": true}` in the `.uefnproject` and `EnableSceneGraph` in the `.uplugin`.

## What the EntityToolset can and cannot do
| Can | Cannot |
|---|---|
| `CreateEntity`, `DeleteEntity`, `FindEntities` (tree, name filter) | **create a prefab asset** (no tool; editor-only: Outliner → right-click entity → Create Prefab) |
| `AddComponent` / `RemoveComponent` (incl. your own Verse components right after `BuildAll`) | edit the contents of a prefab asset (only level entities are reachable) |
| `Get/SetComponentProperty` by friendly Verse name, value as JSON string | set a material on basic-shape meshes (no material property exists, editor or Verse) |
| `Get/SetEntityTransform` (world space) | |
| `ListEntityClasses` / `ListComponentClasses` (also lists prefab classes, `bIsPrefab`) | |

## Gotchas (symptom → cause → fix)
- **Children end up at double the offset** → `CreateEntity` with `parentEntity` treats `transform` as the **local** transform,
  while `SetEntityTransform` is **world**. → Pass local offsets to `CreateEntity`, or fix afterwards with `SetEntityTransform` (world).
- **Base entity class isn't listed** by `ListEntityClasses` → use `{"refPath":"/EntityFramework/_Verse/VNI/Entity.entity"}` directly.
- **Light inside a sphere mesh lights nothing** → the mesh blocks it. Set `sphere_light_component.CastShadows = false`
  (and the bulb mesh `CastShadow = false`).
- **Light invisible in the editor screenshot** → daylight. Build a simple roofed room from cube entities, or test at night.
- Editor doesn't run Verse: lights and meshes show their editor defaults, not your `InitiallyOn` state.
- `LevelEntity` can't be saved with `SceneTools.save_actor` ("not an external actor") → `AssetTools.save_assets([])`.

## Class paths that worked
```
entity                      /EntityFramework/_Verse/VNI/Entity.entity
transform_component         /EntityFramework/_Verse/VNI/Entity.transform_component
cube / sphere / cylinder    /VerseEngineAssets/_Verse/VNI/VerseEngineAssets.BasicShapes_cube|sphere|cylinder
sphere_light_component      /EntityFramework/_Verse/VNI/Component.sphere_light_component
basic_interactable_component /EntityInteract/_Verse/VNI/EntityInteract.basic_interactable_component
your Verse component        /<plugin-guid>/_Verse.<Folder>-<component_name>
```
Useful properties: basic-shape mesh `Visible, Collidable, Queryable, CastShadow, HiddenInGame`;
`sphere_light_component` `Intensity (cd), AttenuationRadius, SourceRadius, CastShadows, ColorFilter {"r","g","b"}, Enabled`.
Color JSON for `SetComponentProperty`: `{"r":1.0,"g":0.02,"b":0.02}`.

## Verse patterns for components
- Custom component: `my_component<public> := class<final_super>(component):` with `@editable` fields (`logic`, `color`, `string`…).
- Lifecycle: `OnBeginSimulation` (transactional, subscribe here) → `OnSimulate()<suspends>` → `OnEndSimulation` (cancel subscriptions).
  **Verified:** `OnBeginSimulation` runs again on session start AND on Stop Game → Start Game, so initial state applied there is restored on restart.
  Multi-round behaviour *(unverified)*: use a `round_settings_device.RoundBeginEvent` device as backup.
- Find parts by **type**, not name: `Entity.FindDescendantComponents(light_component)` (includes the entity itself).
  This keeps the prefab layout free to change.
- Find all instances from a device: `GetSimulationEntity[].FindDescendantComponents(my_component)`. No tags or wiring needed.
- Move a part relative to its parent (stays aligned when the root rotates):
  `Entity.SetLocalTransform(transform{Translation := Rest.Translation + Offset, Rotation := Rest.Rotation, Scale := Rest.Scale})`.
- Custom interaction prompt: subclass `basic_interactable_component` (`class<final_super>(basic_interactable_component)`) and
  override `InteractMessage<override>(Agent:agent)<decides><reads>:message`. Build parameterised `<localizes>` messages in
  `OnSimulate` (they are `no_rollback`), bind to a local, then store in `option{}`.
- `light_component.Enable()/Disable()`, `set Light.ColorFilter = ...`, `set Mesh.Visible = ...` all work at runtime.

## Verified move/rotate test
Root yaw 45° + move: every child's world position matched `root + R(yaw) * localOffset` with 0.000 cm error, and each child took
the root's yaw (`GetEntityTransform` read-back). Script: [`examples/lamp-showroom/tools`](../examples/lamp-showroom/tools).
