# unreal-mcp toolsets (UEFN 42.30)

`list_toolsets` returned these. Call tools with `call_tool(tool_name=<short name>, toolset_name=<toolset>)`.

| Toolset | Use it for | Notes |
|---|---|---|
| `ValkyrieToolset.VerseToolset` | ReadFile / WriteFile / Replace / Grep / ListFiles / Delete / **BuildAll** | Paths are Verse paths: `/<Project>/Folder/file.verse`. `ListFiles("")` shows roots. BuildAll returns diagnostics (empty = OK). |
| `ValkyrieToolset.DeviceToolset` | ListDeviceAssets, PlaceDevice, Get/SetDeviceProperty, ListDeviceProperties, Add/RemoveEventBinding | Can't set device-reference arrays. |
| `ValkyrieToolset.SessionToolset` | StartSession, StopSession, StartGame, StopGame, PushChanges, GetSessionStatus, GetGameState, GetClientLogEntries | GetClientLogEntries often says "no client log"; read `%LOCALAPPDATA%\FortniteGame\Saved\Logs\FortniteGame.log` instead. |
| `ValkyrieToolset.EntityToolset` | Create/Delete/FindEntities, Add/RemoveComponent, Get/SetComponentProperty, Get/SetEntityTransform, ListEntity/ComponentClasses | **No prefab tools.** `CreateEntity` child transform = local. See `topics/scene-graph.md`. |
| `ValkyrieToolset.ValkyriePythonToolset` | Enable Python (needed for the editor_toolset.* toolsets) | |
| `UMGToolSet.UMGToolSet` | CreateWidgetBlueprint, AddWidget, MoveWidget, RemoveWidget, GetWidgets, GetWidgetDescription, CompileWidgetBlueprint, ListWidgetClasses | Use ObjectTools.list_properties to learn property names. |
| `VerseFieldsToolset.VerseFieldsToolset` | AddVerseField, EditVerseField, ListVerseFields, BindWidgetPropertyToVerseField, GetSupportedVerseFieldTypes | Types: bool int float string message color color_alpha texture material event. |
| `MVVMToolset.MVVMToolset` | CreateViewBinding (with conversionName), CreateViewEventBinding, ListWidgetViewBindings, RemoveWidgetViewBinding, ListConversionFunctions, ListBindableWidgetProperties | |
| `WidgetAnimationToolset.WidgetAnimationToolset` | Create/List widget animations, AddWidgetToAnimation | Keys need Sequencer tools; triggering from Verse is not possible (pins). |
| `editor_toolset.toolsets.material.MaterialTools` | create_material, add_expression, connect_expressions, connect_to_output, recompile, get_statistics, layout_expressions | |
| `editor_toolset.toolsets.material_instance.MaterialInstanceTools` | create, set_texture/scalar/vector_parameter | |
| `editor_toolset.toolsets.texture.TextureTools` | import_file (no overwrite), get_size, read_texture | |
| `editor_toolset.toolsets.asset.AssetTools` | find_assets, exists, delete, save_assets, get_referencers | `save_assets([])` saves all dirty. |
| `editor_toolset.toolsets.object.ObjectTools` | list/get/set_properties, search_subclasses, get_class | `set_properties` takes a JSON **string**. |
| `editor_toolset.toolsets.scene.SceneTools` | find_actors (`collision_channels` required, may be `[]`), remove_from_scene, add_to_scene_from_asset, add_to_scene_from_class (`actor_type`, `name`, `xform`), trace_world, save_actor | `save_actor` fails for `LevelEntity` → `save_assets([])`. |
| `EditorToolset.EditorAppToolset` | OpenEditorForAsset, CaptureViewport (with actor labels), CaptureEditorImage, CaptureAssetImage | CaptureAssetImage doesn't support widget blueprints. |
| `EditorToolset.LogsToolset` | GetLogEntries(category, pattern, maxEntries) | Output can be huge; always pass a pattern + small maxEntries. |
| `editor_toolset.toolsets.programmatic.ProgrammaticToolset` | execute_tool_script | See sandbox rules below. |

## Sandbox (`execute_tool_script`)
- Script must define `run()` returning a dict. Call tools with `execute_tool("<full.tool.name>", json.dumps(args))`.
- Allowed imports: `json, math, re, time, datetime, copy`. No `exec`, no `eval`.
- `open(path, 'r')` (mode is required) only works under `%LOCALAPPDATA%\UnrealEditorFortnite\Saved` (and the Fortnite install).
  Since `exec` is blocked, you still have to inline helper libraries into each script.
- `time.sleep` works (use it to poll `GetGameState`).
- Large tool outputs get spilled to a file by the client; parse them with a local Python helper.

## Asset/class paths that worked
- Widget classes: `/Script/UMG.CanvasPanel|Overlay|SizeBox|ScaleBox|StackBox|WidgetSwitcher|Image`,
  Custom Button `/Script/UIFramework.UIFrameworkCustomButtonWidget`, nested widget `/<Project>/Path/WBP_X.WBP_X_C`.
- Material expressions: `/Script/Engine.MaterialExpression<Name>` (Time, TextureCoordinate, Rotator, Sine, Cosine,
  Frac, Abs, Saturate, ComponentMask, AppendVector, LinearInterpolate, Power, Max, ScalarParameter, VectorParameter,
  TextureSampleParameter2D, Constant).
- Button device asset: `/CreativeCoreDevices/SetupAssets/PID_Device_Button.PID_Device_Button`.
- Round Settings: `/CreativeCoreDevices/SetupAssets/PID_CP_Devices_RoundSettings_V2.PID_CP_Devices_RoundSettings_V2`.
- Island Settings (class, not in device catalog): `/CreativeCoreDevices/Device_ExperienceSettings_V2_UEFN.Device_ExperienceSettings_V2_UEFN_C`.
- Scene Graph class paths: see `topics/scene-graph.md`.

## Calling the server without an MCP client
The editor serves streamable-HTTP MCP at `http://127.0.0.1:8000/mcp`: POST `initialize`, keep the `Mcp-Session-Id` header,
then `tools/call` → `call_tool {toolset_name, tool_name, arguments}`. Minimal client: `examples/lamp-showroom/tools/mcp.py`.
`CaptureViewport` / `CaptureEditorImage` return the PNG as a separate `image` content item (not inside the JSON text).
