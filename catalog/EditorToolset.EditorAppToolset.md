# EditorToolset.EditorAppToolset

Tools for querying and modifying Unreal Editor state: console variables, asset imaging,
actor and asset selection, scene outliner folder selection, viewport camera, content browser
navigation, content browser collections, and Play-In-Editor session control.

37 tools.

### `AddAssetsToCollection`

Adds assets to the specified collection.

| arg | type | req | description |
|---|---|---|---|
| `collection` | `ContentBrowserCollectionInfo{name:string, shareType:Local or Private or Shared}` | yes | The collection to add to. |
| `assetPaths` | `[string]` | yes | The package paths of the assets to add. |

### `CaptureAssetImage`

Renders a thumbnail for the specified asset (e.g. static meshes, skeletal meshes,
skeletons, animations, montages, materials, textures).

| arg | type | req | description |
|---|---|---|---|
| `assetPath` | `string` | yes | The path to the asset, e.g. '/Game/Meshes/SM_Cube'. |

Returns: `ToolsetImage{mimeType:string, data:string}`

### `CaptureEditorImage`

Captures an image of the entire editor application as the user sees it.

Returns: `ToolsetImage{mimeType:string, data:string}`

### `CaptureViewport`

Captures the level viewport with optional annotations.

Annotations rendering overlays a projected 3D world-space grid plus
name + position labels on visible actors. The grid is drawn at a configurable
ground-plane Z and projected through the camera, with coordinate numbers at
intersections (shown in meters). Each labeled actor gets a crosshair at its
projected screen position with a leader-line callout placed to avoid overlap. This
gives a vision-capable agent spatial awareness: it can reference grid
coordinates to direct placement and identify scene contents by label.

| arg | type | req | description |
|---|---|---|---|
| `captureTransform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` |  | Optional pose to capture from. If unset, uses the viewport's current camera. (default `null`) |
| `annotations` | `ViewportAnnotationConfig` |  | Optional annotation overlay configuration. Only use this when you need the information in order to perform spatial actions. (default `null`) |
| `bShowUI` | `boolean` |  | If false (default), editor UI overlays such as transform gizmos and selection outlines are hidden in the captured image. Set true to capture exactly what's on screen, gizmos and all. (default `false`) |

Returns: `ViewportCapture`

### `CreateCollection`

Creates a new static collection.

| arg | type | req | description |
|---|---|---|---|
| `collectionName` | `string` | yes | The name of the new collection. |
| `shareType` | `Local or Private or Shared` | yes | How the collection is shared. |

### `DestroyCollection`

Deletes the specified collection.

| arg | type | req | description |
|---|---|---|---|
| `collection` | `ContentBrowserCollectionInfo{name:string, shareType:Local or Private or Shared}` | yes | The collection to delete. |

### `FocusOnActors`

Repositions the level editor camera to focus on the specified actors.
Cannot be called while PIE is active.

| arg | type | req | description |
|---|---|---|---|
| `actors` | `[ref</Script/Engine.Actor>]` | yes | The actors to focus the level camera on. |

### `GetActiveEditorModes`

Returns the IDs of the currently active editor modes. More than one mode can
be active at once; the default placement mode ("EM_Default") is usually present.

Returns: `[string]`

### `GetAssetThumbnails`

Returns the assets' existing cached thumbnails (the images the Content Browser shows) without
loading or rendering the assets.

On success the result's value holds one image per requested path, in request order; an entry is
an empty image when the asset has no saved thumbnail or its thumbnail could not be decoded. The
call completes with an error instead if any requested path cannot be found.

| arg | type | req | description |
|---|---|---|---|
| `assetPaths` | `[string]` | yes | The asset paths to fetch, e.g. '/Game/Meshes/SM_Cube'. |

Returns: `[ToolsetImage{mimeType:string, data:string}]`

### `GetCVarValue`

Reads the current value of a console variable as its canonical string
representation (e.g. "true"/"false" for bools, "1.5" for floats).

| arg | type | req | description |
|---|---|---|---|
| `name` | `string` | yes | The name of the console variable. |

Returns: `string`

### `GetCameraTransform`

Returns the position and rotation of the level viewport camera.

Returns: `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}`

### `GetCollectionAssets`

Returns the assets in the specified collection.

| arg | type | req | description |
|---|---|---|---|
| `collection` | `ContentBrowserCollectionInfo{name:string, shareType:Local or Private or Shared}` | yes | The collection to query. |

Returns: `[string]`

### `GetContentBrowserPath`

Gets the current path of the active content browser.

Returns: `string`

### `GetOpenAssets`

Gets the list of assets currently open in asset editors.

Returns: `[string]`

### `GetSelectedActors`

Gets the currently selected actors in the level editor.

Returns: `[ref</Script/Engine.Actor>]`

### `GetSelectedAssets`

Gets the list of assets selected in the content browser.

Returns: `[string]`

### `GetSelectedOutlinerFolders`

Gets the folder paths selected across all open scene outliners.

Returns: `[string]`

### `GetShowFlag`

Reads whether a named engine show flag is currently enabled on the active level
editor viewport.

| arg | type | req | description |
|---|---|---|---|
| `flagName` | `string` | yes | The show flag name (see ListShowFlags). |

Returns: `boolean`

### `GetVisibleActors`

Returns all actors in the current level whose bounds intersect the viewport frustum.

Returns: `[ref</Script/Engine.Actor>]`

### `ListCollections`

Lists all collections in the content browser.

Returns: `[ContentBrowserCollectionInfo{name:string, shareType:Local or Private or Shared}]`

### `ListEditorModes`

Lists the IDs of all registered editor modes (e.g. "EM_Default",
"EM_Landscape", "EM_Foliage"), ordered by mode priority.

Returns: `[string]`

### `ListShowFlags`

Lists every engine show flag with its display name and editor group.

Returns: `[ShowFlagInfo{name:string, displayName:string, group:Normal or Advanced or PostProcess or CollisionModes or Developer or Visualize or LightTypes or LightingComponents or LightingFeatures or Lumen or MegaLights or Nanite or Hidden or Transient or Custom}]`

### `OpenEditorForAsset`

Opens an asset editor for the specified asset.

| arg | type | req | description |
|---|---|---|---|
| `assetPath` | `string` | yes | The object path of the asset to open. Bare package paths are also accepted. |

### `RemoveAssetsFromCollection`

Removes assets from the specified collection.

| arg | type | req | description |
|---|---|---|---|
| `collection` | `ContentBrowserCollectionInfo{name:string, shareType:Local or Private or Shared}` | yes | The collection to remove from. |
| `assetPaths` | `[string]` | yes | The package paths of the assets to remove. |

### `ScreenCoordsToWorld`

Finds the world position of the nearest solid object at a given set of normalized view space coords.

| arg | type | req | description |
|---|---|---|---|
| `coords` | `Vector2D{x:number, y:number}` | yes | The normalized screen-space coordinates to trace from. |
| `traceDistance` | `number` |  | The maximum distance to trace within the scene. (default `100000`) |

Returns: `Vector{x:number, y:number, z:number}`

### `SearchCVars`

Finds all console variables that contain a given name.

| arg | type | req | description |
|---|---|---|---|
| `name` | `string` | yes | The partial or full name to search for. |

Returns: `string`

### `SelectActors`

Selects the specified actors in the current scene.

| arg | type | req | description |
|---|---|---|---|
| `actors` | `[ref</Script/Engine.Actor>]` | yes | The actors to select. |

### `SelectAssets`

Selects the specified assets in the content browser.
Completes once the content browser has applied the selection.

| arg | type | req | description |
|---|---|---|---|
| `assetPaths` | `[string]` | yes | The object paths of the assets to select. Bare package paths are also accepted. |

Returns: `null`

### `SelectOutlinerFolders`

Selects the specified folders in every open scene outliner. Replaces the
existing folder selection; non-folder selections (e.g. selected actors)
are preserved.

| arg | type | req | description |
|---|---|---|---|
| `folderPaths` | `[string]` | yes | The folder paths to select. |

### `SetCVarValue`

Sets the value of a console variable. The value is parsed according to
the variable's declared type.

| arg | type | req | description |
|---|---|---|---|
| `name` | `string` | yes | The name of the console variable. |
| `value` | `string` | yes | The new value as a string. |

### `SetCameraTransform`

Sets the position and rotation of the level viewport camera.

| arg | type | req | description |
|---|---|---|---|
| `transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` | yes | The transform to apply to the viewport camera. |

### `SetContentBrowserPath`

Navigates the active content browser to the specified folder path.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes | The internal path to navigate to, e.g. '/Game/Meshes'. |

### `SetEditorMode`

Activates the specified editor mode. Pass "EM_Default" (or an empty string) to
return to the default placement/select mode. Cannot be used during PIE.

| arg | type | req | description |
|---|---|---|---|
| `modeId` | `string` | yes | The editor mode ID to activate (see ListEditorModes). |

### `SetShowFlag`

Toggles a named engine show flag on the active level editor viewport (e.g.
"Navigation", "Collision", "Grid", "Bounds", "Fog", "Landscape", "Volumes").

| arg | type | req | description |
|---|---|---|---|
| `flagName` | `string` | yes | The show flag name (see ListShowFlags). |
| `bEnabled` | `boolean` | yes | Whether to enable or disable the flag. |

### `SetViewportViewMode`

Sets the view mode of the active level editor viewport (e.g. Lit, Unlit,
Wireframe, Lighting-only, complexity visualizations).

| arg | type | req | description |
|---|---|---|---|
| `viewMode` | `VMI_BrushWireframe or VMI_Wireframe or VMI_Unlit or VMI_Lit or VMI_Lit_DetailLighting or VMI_LightingOnly or VMI_LightComplexity or VMI_ShaderComplexity or VMI_LightmapDensity or VMI_LitLightmapDensity or VMI_ReflectionOverride or VMI_VisualizeBuffer or VMI_StationaryLightOverlap or VMI_CollisionPawn or VMI_CollisionVisibility or VMI_LODColoration or VMI_QuadOverdraw or VMI_PrimitiveDistanceAccuracy or VMI_MeshUVDensityAccuracy or VMI_ShaderComplexityWithQuadOverdraw or VMI_HLODColoration or VMI_GroupLODColoration or VMI_MaterialTextureScaleAccuracy or VMI_RequiredTextureResolution or VMI_PathTracing or VMI_RayTracingDebug or VMI_VisualizeNanite or VMI_VisualizeVirtualTexture or VMI_VisualizeLumen or VMI_VisualizeVirtualShadowMap or VMI_VisualizeGPUSkinCache or VMI_VisualizeSubstrate or VMI_VisualizeGroom or VMI_LWCComplexity or VMI_Lit_Wireframe or VMI_VisualizeActorColoration or VMI_ShadowCasters or VMI_Clay or VMI_Zebra or VMI_FrontBackFace or VMI_RandomColor or VMI_VisualizeMegaLights or VMI_StreamingTextureDeficit or VMI_StreamingTextureResidency or VMI_StreamingMeshLODDeficit or VMI_StreamingMeshLODResidency or VMI_FarShadowCasters or VMI_Max or VMI_Unknown` | yes | The view mode to apply. |

### `ShowNotification`

Shows a transient editor notification (Slate toast, bottom-right).

| arg | type | req | description |
|---|---|---|---|
| `message` | `string` | yes | The text to display. |
| `state` | `None or Pending or Success or Fail` |  | The notification's status, which drives its icon. Defaults to None (neutral info, no icon). (default `"None"`) |
| `expireDuration` | `number` |  | Seconds the toast remains on screen before it fades out. Defaults to 1 (FNotificationInfo's own default). (default `1`) |

### `WorldPosToScreenCoords`

Converts a world-space position into normalized screen space based on the editor viewport camera.

| arg | type | req | description |
|---|---|---|---|
| `position` | `Vector{x:number, y:number, z:number}` | yes | The world space position to convert. |

Returns: `Vector2D{x:number, y:number}`
