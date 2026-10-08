# ValkyrieToolset.DeviceToolset

AI-callable tools for UEFN Creative devices — classic Blueprint and Verse creative_device. Browse the
project's placeable device catalog, place devices, add or remove event bindings between placed devices,
and read or write a Verse device's settings.

9 tools.

### `AddEventBinding`

Bind a source device's event to a target device's function so the event triggers it (idempotent —
re-binding the same pair is a no-op).

| arg | type | req | description |
|---|---|---|---|
| `sourceDevicePath` | `ref</Script/CoreUObject.Object>` | yes | Object path of an already-placed source device actor (not a catalog asset path). |
| `sourceEvent` | `string` | yes | Event name on the source device. |
| `targetDevicePath` | `ref</Script/CoreUObject.Object>` | yes | Object path of an already-placed target device actor. |
| `targetFunction` | `string` | yes | Function name on the target device. |

### `GetBindingOptions`

Get the source events and target functions a device exposes for binding.

| arg | type | req | description |
|---|---|---|---|
| `devicePath` | `ref</Script/CoreUObject.Object>` | yes | Object path of the device actor. |

Returns: `DeviceBindingOptions{sourceEvents:[string], targetFunctions:[string]}`

### `GetDeviceProperties`

Read named settings from a Verse creative_device.

| arg | type | req | description |
|---|---|---|---|
| `device` | `ref</Script/VerseDevices.ScriptDevice>` | yes | A placed Verse creative_device. |
| `propertyNames` | `[string]` | yes | Setting names. |

Returns: `string`

### `ListDeviceAssets`

List the project's placeable Creative devices — classic (Blueprint) and Verse (creative_device).

| arg | type | req | description |
|---|---|---|---|
| `nameFilter` | `string` |  | Case-insensitive substring matched against each device's asset name. Empty lists all. (default `""`) |

Returns: `[DeviceAssetInfo{displayName:string, assetPath:ref</Script/CoreUObject.Object>, category:string, bIsVerseDevice:boolean}]`

### `ListDeviceProperties`

List a Verse creative_device's editable settings as a JSON property schema, with friendly names.

| arg | type | req | description |
|---|---|---|---|
| `device` | `ref</Script/VerseDevices.ScriptDevice>` | yes | A placed Verse creative_device. |

Returns: `string`

### `ListEventBindings`

List the event bindings currently wired into a device's target functions.

| arg | type | req | description |
|---|---|---|---|
| `devicePath` | `ref</Script/CoreUObject.Object>` | yes | Object path of the device actor. |

Returns: `[DeviceEventBinding{sourceDevicePath:ref</Script/CoreUObject.Object>, sourceEvent:string, targetDevicePath:ref</Script/CoreUObject.Object>, targetFunction:string}]`

### `PlaceDevice`

Place a catalog device (classic or Verse) into the level.

| arg | type | req | description |
|---|---|---|---|
| `assetPath` | `ref</Script/CoreUObject.Object>` | yes | A device asset reference (from the catalog). |
| `transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` | yes | World-space transform to place the device with; scale is applied after spawn. |

Returns: `ref</Script/CoreUObject.Object>`

### `RemoveEventBinding`

Remove an event binding from a source device's event to a target device's function.

| arg | type | req | description |
|---|---|---|---|
| `sourceDevicePath` | `ref</Script/CoreUObject.Object>` | yes | Object path of the source device actor. |
| `sourceEvent` | `string` | yes | Event name on the source device. |
| `targetDevicePath` | `ref</Script/CoreUObject.Object>` | yes | Object path of the target device actor. |
| `targetFunction` | `string` | yes | Function name on the target device. |

### `SetDeviceProperty`

Set one editable setting on a Verse creative_device.

| arg | type | req | description |
|---|---|---|---|
| `device` | `ref</Script/VerseDevices.ScriptDevice>` | yes | A placed Verse creative_device. |
| `propertyName` | `string` | yes | Setting name. |
| `value` | `string` | yes | JSON-encoded value for the setting's type (e.g. 5, true, "text", {"X":1}). |
