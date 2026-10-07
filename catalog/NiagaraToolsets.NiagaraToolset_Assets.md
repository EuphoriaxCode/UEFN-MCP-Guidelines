# NiagaraToolsets.NiagaraToolset_Assets

Niagara Toolset for asset-registry-backed discovery and metadata editing of UNiagaraScript assets.
Read paths use the asset registry only. Write paths load the script and refresh registry tags.

3 tools.

### `FindNiagaraScripts`

Searches for UNiagaraScript assets matching the given filters.

| arg | type | req | description |
|---|---|---|---|
| `folderPath` | `string` | yes | Folder to search within; empty searches the whole project. |
| `name` | `string` | yes | Substring filter on asset name (case-insensitive); empty matches all. |
| `usages` | `[Function or Module or DynamicInput or ParticleSpawnScript or ParticleSpawnScriptInterpolated or ParticleUpdateScript or ParticleEventScript or ParticleSimulationStageScript or ParticleGPUComputeScript or EmitterSpawnScript or EmitterUpdateScript or SystemSpawnScript or SystemUpdateScript]` | yes | Allowed Usage values; empty matches all. |
| `visibilities` | `[Invalid or Unexposed or Library or Hidden]` | yes | Allowed LibraryVisibility values; empty defaults to {Library}. |
| `supportedUsages` | `[Function or Module or DynamicInput or ParticleSpawnScript or ParticleSpawnScriptInterpolated or ParticleUpdateScript or ParticleEventScript or ParticleSimulationStageScript or ParticleGPUComputeScript or EmitterSpawnScript or EmitterUpdateScript or SystemSpawnScript or SystemUpdateScript]` | yes | Restricts results to Module scripts whose supported stack contexts include any of these; empty disables the gate. |
| `bRecursive` | `boolean` | yes | Whether to search subfolders. Ignored when FolderPath is empty. |
| `bIncludeDeprecated` | `boolean` | yes | When false, assets marked deprecated are excluded. |

Returns: `[AssetData{packageName:string, packagePath:string, assetName:string, assetClassPath:TopLevelAssetPath{packageName:string, assetName:string}}]`

### `GetAssetDiscoveryInfo`

Returns the project's configured asset discovery groups.

Returns: `[NiagaraToolsetAssetDiscoveryGroup{description:string, paths:[string]}]`

### `GetNiagaraScriptDigest`

Returns the decoded asset-registry tag metadata for a Niagara script asset.

| arg | type | req | description |
|---|---|---|---|
| `objectPath` | `string` | yes | Full object path of the script (e.g. "/Niagara/Modules/Spawn/Initialize Particle.Initialize Particle"). |

Returns: `NiagaraExt_ScriptDigest`
