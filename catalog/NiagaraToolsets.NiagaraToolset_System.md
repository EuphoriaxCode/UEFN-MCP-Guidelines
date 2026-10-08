# NiagaraToolsets.NiagaraToolset_System

Niagara Toolset for Niagara System operations.

Provides comprehensive access to Niagara System editing, including:
- System, emitter, and module creation and modification
- Schema discovery for understanding structure
- Topology and Summary inspection for viewing current configuration
- Data access for reading and writing properties
- Dependency rollups via GetSystemDependencies
- Dynamic-input chain traversal via GetDynamicInputChain

This is the primary toolset for working with Niagara Systems in the editor.

46 tools.

### `AddEmitter`

Adds an emitter to a Niagara System.
The new emitter will be based on the template emitter, inheriting its configuration and modules.
Returns the full emitter topology (no input values — call GetEmitterInputValues for values).

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to add the emitter to |
| `templateEmitter` | `ref</Script/Niagara.NiagaraEmitter>` | yes | The emitter asset to use as a template for the new emitter |
| `emitterName` | `string` | yes | Name for the new emitter instance |

Returns: `NiagaraExt_EmitterTopology`

### `AddModule`

Adds a module to a script stack.
The module will be inserted into the specified script's execution stack.
Returns the module topology with all inputs walked (no input values — call GetModuleInputValues for values).

| arg | type | req | description |
|---|---|---|---|
| `moduleLocationRef` | `NiagaraExt_StackItemReference` | yes | Reference specifying where to add the module |
| `moduleAsset` | `ref</Script/Niagara.NiagaraScript>` | yes | The module script asset to add to the stack |

Returns: `NiagaraExt_ModuleTopology`

### `AddRenderer`

Adds a renderer to an emitter.
Creates a new renderer of the specified type and adds it to the emitter's renderer list.
Returns an FNiagaraExt_RendererRef with the new renderer's Index and RendererClass,
usable directly with SetRendererData / GetRendererData without a follow-up topology call.

| arg | type | req | description |
|---|---|---|---|
| `newRendererLocation` | `NiagaraExt_StackItemReference` | yes | Reference specifying which emitter to add the renderer to |
| `rendererClass` | `ref<Class@/Script/Niagara.NiagaraRendererProperties>` | yes | The class of renderer to create (e.g., UNiagaraSpriteRendererProperties) |

Returns: `NiagaraExt_RendererRef{rendererIndex:integer, rendererClass:ref<Class@/Script/Niagara.NiagaraRendererProperties>}`

### `AddSetParameterEntry`

Adds a single parameter to an existing SetParameters module.
The module referenced by ModuleRef must be a SetParameters (UNiagaraNodeAssignment) module.
Use bIsSetParametersModule in the module topology to confirm before calling.

| arg | type | req | description |
|---|---|---|---|
| `moduleRef` | `NiagaraExt_StackItemReference` | yes | Reference to the existing SetParameters module |
| `entry` | `NiagaraExt_SetParameterEntry{variable:NiagaraExt_Variable{name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}, defaultValue:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}}` | yes | The parameter to add (variable name, type, and optional default value) |

Returns: `NiagaraExt_ModuleTopology`

### `AddSetParametersModule`

Adds a SetParameters module to a script stack.
Unlike AddModule which requires a script asset, a SetParameters module dynamically assigns
values to named parameters and generates its own internal script. Use this when you need
to set one or more particle/emitter/system parameters directly in the stack.

| arg | type | req | description |
|---|---|---|---|
| `moduleLocationRef` | `NiagaraExt_StackItemReference` | yes | Reference specifying where to add the module |
| `parameters` | `[NiagaraExt_SetParameterEntry{variable:NiagaraExt_Variable{name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}, defaultValue:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}}]` | yes | Array of parameter entries, each with a variable (name + type) and an optional default value |

Returns: `NiagaraExt_ModuleTopology`

### `AddUserVariables`

Adds or updates user variables on a system.
If a variable with the same name already exists, it will be replaced with the new definition.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to add variables to |
| `variablesToAdd` | `[NiagaraExt_UserVariable{defaultValue:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}, description:string, name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}]` | yes | Array of user variables to add or update |

### `ApplyStackIssueFix`

Applies a Fix-style stack issue fix identified by IssueId and FixId. Link-style fixes are
rejected. The fix is undoable via the editor undo stack. Applying a fix may trigger a
recompile; the result waits for that compile to complete so post-fix state is valid.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to apply the fix to. |
| `issueId` | `string` | yes | IssueId from a prior FNiagaraExt_StackIssue. |
| `fixId` | `string` | yes | FixId from a prior FNiagaraExt_StackIssueFix. |

Returns: `NiagaraToolset_ApplyStackIssueFixResult{applyResult:NiagaraExt_ApplyStackIssueFixResult{bApplied:boolean, appliedFixDescription:string}, postFixIssues:NiagaraExt_StackIssues{numErrors:integer, numWarnings:integer, numInfos:integer, issues:[NiagaraExt_StackIssue]}}`

### `CreateNiagaraSystem`

Creates a new Niagara System asset.
The new system will be based on the template system, inheriting its configuration and emitters.

| arg | type | req | description |
|---|---|---|---|
| `assetName` | `string` | yes | Name of the new asset (without path or extension) |
| `assetPath` | `string` | yes | Directory path where the new asset will be created |
| `templateSystem` | `ref</Script/Niagara.NiagaraSystem>` | yes | Template system to base the new system on (required) |

Returns: `ref</Script/Niagara.NiagaraSystem>`

### `GetAvailableDynamicInputs`

Returns all available Dynamic Input Module assets compatible with the given type.
Dynamic inputs provide procedural value generation for module parameters.

| arg | type | req | description |
|---|---|---|---|
| `type` | `ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}` | yes | The Niagara type definition to find compatible dynamic inputs for |

Returns: `[ref</Script/Niagara.NiagaraScript>]`

### `GetDataInterfaceSchema`

Returns property schema for a specific Data Interface class.
Describes all available properties and their types for the given data interface type.

| arg | type | req | description |
|---|---|---|---|
| `dataInterfaceClass` | `ref<Class@/Script/Niagara.NiagaraDataInterface>` | yes | The data interface class to get the schema for |

Returns: `NiagaraExt_DataInterfaceSchema{dataInterfaceClass:ref<Class@/Script/Niagara.NiagaraDataInterface>, propertySchema:string}`

### `GetDynamicInputChain`

Returns the full recursive chain for a dynamic input: topology metadata and resolved values at every level.
The starting input must have value mode Dynamic; an error is surfaced otherwise.
The schema expands one full level and emits a typed recursion stub at deeper levels;
the wire format recurses to arbitrary depth matching the underlying chain.

| arg | type | req | description |
|---|---|---|---|
| `stackInputRef` | `NiagaraExt_StackItemReference` | yes | Reference to the dynamic input to traverse |

Returns: `NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}`

### `GetDynamicInputSchema`

Returns schema for a dynamic input module in the stack.
Describes the inputs and configuration for a procedural value generator.

| arg | type | req | description |
|---|---|---|---|
| `dynamicInputReference` | `NiagaraExt_StackItemReference` | yes | Reference to the dynamic input to get the schema for |

Returns: `NiagaraExt_DynamicInputSchema{asset:ref</Script/Niagara.NiagaraScript>, inputs:[NiagaraExt_StackInputSchema], outputs:[NiagaraExt_Variable{name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}]}`

### `GetDynamicInputSchemaFromAsset`

Returns schema for a dynamic input asset.
Standalone function that doesn't require a system context - useful for browsing available dynamic inputs.

| arg | type | req | description |
|---|---|---|---|
| `dynamicInputAsset` | `ref</Script/Niagara.NiagaraScript>` | yes | The dynamic input script asset to get the schema for |

Returns: `NiagaraExt_DynamicInputSchema{asset:ref</Script/Niagara.NiagaraScript>, inputs:[NiagaraExt_StackInputSchema], outputs:[NiagaraExt_Variable{name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}]}`

### `GetEmitterData`

Returns emitter property values as a single JSON-string blob in PropertyValues.
The blob contains the full FVersionedNiagaraEmitterData (SimTarget, bLocalSpace, RandomSeed,
FixedBounds, etc.) — fields use C++ PascalCase, must be parsed to read individual values.

For typed access to common metadata (SimTarget, EmitterName, bEnabled, RendererClasses) prefer
GetEmitterSummary — it returns those as named fields directly and avoids a JSON parse step.
Use this endpoint when you need the full property set or a less-common field.

| arg | type | req | description |
|---|---|---|---|
| `emitterRef` | `NiagaraExt_StackItemReference` | yes | Reference to the emitter to retrieve data from |

Returns: `NiagaraExt_EmitterData{propertyValues:string}`

### `GetEmitterInputValues`

Returns all resolved input values for every module across all four emitter script stacks.
One FNiagaraExt_ModuleInputValues entry per module, each carrying all its resolved input values.
Call this in parallel with GetEmitterTopology to get both structure and values in two passes.

| arg | type | req | description |
|---|---|---|---|
| `emitterRef` | `NiagaraExt_StackItemReference` | yes | Reference to the emitter to retrieve input values from |

Returns: `[NiagaraExt_ModuleInputValues{moduleName:string, inputs:[NiagaraExt_StackInputValueEntry{name:string, value:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}}]}]`

### `GetEmitterSchema`

Returns property schema for Niagara Emitter.
Describes all available properties and their types that can be set on a Niagara Emitter.

Returns: `NiagaraExt_EmitterSchema{propertySchema:string}`

### `GetEmitterSummary`

Returns lightweight emitter metadata: name, enabled state, sim target, renderer classes.
Use this when you only need to check metadata without walking the full emitter structure.

| arg | type | req | description |
|---|---|---|---|
| `emitterRef` | `NiagaraExt_StackItemReference` | yes | Reference to the emitter to summarise. |

Returns: `NiagaraExt_EmitterSummary{emitterName:string, bEnabled:boolean, simTarget:CPUSim or GPUComputeSim, rendererClasses:[ref<Class@/Script/Niagara.NiagaraRendererProperties>]}`

### `GetEmitterTopology`

Returns full emitter topology: four script stacks with all modules and inputs, renderer references.
All fields always populated. The returned topology carries no input values; call GetEmitterInputValues in parallel.
Note: mutation endpoints (AddEmitter, AddModule) also return topology structs — input values require a separate data call.

| arg | type | req | description |
|---|---|---|---|
| `emitterRef` | `NiagaraExt_StackItemReference` | yes | Reference to the emitter to describe. |

Returns: `NiagaraExt_EmitterTopology`

### `GetModuleInputValues`

Returns resolved input values for a single module.
Use when you need values for one specific module without walking the whole emitter.

| arg | type | req | description |
|---|---|---|---|
| `moduleRef` | `NiagaraExt_StackItemReference` | yes | Reference to the module |

Returns: `NiagaraExt_ModuleInputValues{moduleName:string, inputs:[NiagaraExt_StackInputValueEntry{name:string, value:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}}]}`

### `GetModuleSchema`

Returns schema for a module and all its inputs.
Call this after seeing a module in topology to understand what inputs it exposes.

| arg | type | req | description |
|---|---|---|---|
| `moduleReference` | `NiagaraExt_StackItemReference` | yes | Reference to the module to get the schema for |

Returns: `NiagaraExt_ModuleSchema{asset:ref</Script/Niagara.NiagaraScript>, inputs:[NiagaraExt_StackInputSchema], outputs:[NiagaraExt_Variable{name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}]}`

### `GetModuleSchemaFromAsset`

Returns schema for a module asset.
Standalone function that doesn't require a system context - useful for browsing available modules.

| arg | type | req | description |
|---|---|---|---|
| `moduleAsset` | `ref</Script/Niagara.NiagaraScript>` | yes | The module script asset to get the schema for |

Returns: `NiagaraExt_ModuleSchema{asset:ref</Script/Niagara.NiagaraScript>, inputs:[NiagaraExt_StackInputSchema], outputs:[NiagaraExt_Variable{name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}]}`

### `GetModuleTopology`

Returns module topology: metadata and all inputs (name/type/visibility only, no values).
All fields always populated.

| arg | type | req | description |
|---|---|---|---|
| `moduleRef` | `NiagaraExt_StackItemReference` | yes | Reference to the module to describe. |

Returns: `NiagaraExt_ModuleTopology`

### `GetRendererData`

Returns renderer property values.
Retrieves the current values of all configurable renderer properties.

| arg | type | req | description |
|---|---|---|---|
| `rendererRef` | `NiagaraExt_StackItemReference` | yes | Reference to the renderer to retrieve data from |

Returns: `NiagaraExt_RendererData{propertyValues:string}`

### `GetRendererSchema`

Returns property schema for a specific Renderer class.
Describes all available properties and their types for the given renderer type.

| arg | type | req | description |
|---|---|---|---|
| `rendererClass` | `ref<Class@/Script/Niagara.NiagaraRendererProperties>` | yes | The renderer class to get the schema for (e.g., UNiagaraSpriteRendererProperties) |

Returns: `NiagaraExt_RendererSchema{rendererClass:ref<Class@/Script/Niagara.NiagaraRendererProperties>, propertySchema:string}`

### `GetScriptStackInputValues`

Returns all resolved input values for every module in the given script stack.
One FNiagaraExt_ModuleInputValues entry per module.

| arg | type | req | description |
|---|---|---|---|
| `scriptRef` | `NiagaraExt_StackItemReference` | yes | Reference to the script stack |

Returns: `[NiagaraExt_ModuleInputValues{moduleName:string, inputs:[NiagaraExt_StackInputValueEntry{name:string, value:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}}]}]`

### `GetScriptStackTopology`

Returns script stack topology: all modules and their inputs in execution order.
All fields always populated.

| arg | type | req | description |
|---|---|---|---|
| `scriptRef` | `NiagaraExt_StackItemReference` | yes | Reference to the script stack to describe. |

Returns: `NiagaraExt_ScriptStackTopology{scriptName:string, modules:[NiagaraExt_ModuleTopology]}`

### `GetStackInputData`

Returns the value of a stack module input.
Retrieves the current value and configuration for a specific module input parameter.

| arg | type | req | description |
|---|---|---|---|
| `stackInputRef` | `NiagaraExt_StackItemReference` | yes | Reference to the stack input to retrieve data from |

Returns: `NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}`

### `GetStackInputSchema`

Returns schema for a single module input in the stack.
Describes the type, metadata, and configuration options for a specific input parameter.

| arg | type | req | description |
|---|---|---|---|
| `inputReference` | `NiagaraExt_StackItemReference` | yes | Reference to the stack input to get the schema for |

Returns: `NiagaraExt_StackInputSchema`

### `GetStackInputTopology`

Returns stack input topology: name, type, visibility, editability. No value payload.
For the resolved value call GetStackInputData. For a dynamic-input chain call GetDynamicInputChain.

| arg | type | req | description |
|---|---|---|---|
| `stackInputRef` | `NiagaraExt_StackItemReference` | yes | Reference to the stack input to describe. |

Returns: `NiagaraExt_StackInputTopology`

### `GetStackIssues`

Returns all stack issues (errors, warnings, info) from the Niagara module stack, including
dismissed ones. Waits for any in-flight compile to complete before collecting.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to query. |

Returns: `NiagaraExt_StackIssues{numErrors:integer, numWarnings:integer, numInfos:integer, issues:[NiagaraExt_StackIssue]}`

### `GetSystemCompileState`

Returns the current compile state of a Niagara System: aggregate status, per-script compile
events, and summary flags. Waits for any in-flight compile to complete before collecting.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to query. |

Returns: `NiagaraExt_SystemCompileState`

### `GetSystemData`

Returns system property values.
Retrieves the current values of all configurable system-level properties.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to retrieve data from |

Returns: `NiagaraExt_SystemData{propertyValues:string}`

### `GetSystemDependencies`

Returns the four Used* sets (renderers, data interfaces, modules, dynamic inputs)
gathered across all emitters and system scripts.
These sets are not included in topology structs; call this endpoint separately when needed.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to scan |

Returns: `NiagaraExt_SystemDependencies{usedRenderers:[ref<Class@/Script/Niagara.NiagaraRendererProperties>], usedDataInterfaces:[ref<Class@/Script/Niagara.NiagaraDataInterface>], usedModules:[ref</Script/Niagara.NiagaraScript>], usedDynamicInputs:[ref</Script/Niagara.NiagaraScript>]}`

### `GetSystemSchema`

Returns property schema for Niagara System.
Describes all available properties and their types that can be set on a Niagara System.

Returns: `NiagaraExt_SystemSchema{propertySchema:string}`

### `GetSystemSummary`

Returns lightweight system metadata: name, user variables, and one summary entry per emitter.
Use this for first contact with an unfamiliar system. For full structural detail call GetEmitterTopology per emitter.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to summarise. |

Returns: `NiagaraExt_SystemSummary{systemName:string, userVariables:[NiagaraExt_UserVariable{defaultValue:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}, description:string, name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}], emitters:[NiagaraExt_EmitterSummary{emitterName:string, bEnabled:boolean, simTarget:CPUSim or GPUComputeSim, rendererClasses:[ref<Class@/Script/Niagara.NiagaraRendererProperties>]}]}`

### `GetUserVariables`

Returns all user variables defined on the system.
User variables are parameters exposed for external control and can be overridden per component instance.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to retrieve user variables from |

Returns: `NiagaraExt_UserVariables{userVariables:[NiagaraExt_UserVariable{defaultValue:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}, description:string, name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}]}`

### `RemoveEmitter`

Removes an emitter from a system.
Deletes the specified emitter and all its associated scripts, modules, and renderers.

| arg | type | req | description |
|---|---|---|---|
| `emitterToRemove` | `NiagaraExt_StackItemReference` | yes | Reference to the emitter to remove from the system |

### `RemoveModule`

Removes a module from a script stack.
Deletes the specified module and all its inputs from the script's execution stack.

| arg | type | req | description |
|---|---|---|---|
| `moduleToRemove` | `NiagaraExt_StackItemReference` | yes | Reference to the module to remove from the stack |

### `RemoveRenderer`

Removes a renderer from an emitter.
Deletes the specified renderer from the emitter's renderer list.

| arg | type | req | description |
|---|---|---|---|
| `rendererToRemove` | `NiagaraExt_StackItemReference` | yes | Reference to the renderer to remove |

### `RemoveSetParameterEntry`

Removes a parameter from an existing SetParameters module by name.
The module referenced by ModuleRef must be a SetParameters (UNiagaraNodeAssignment) module.
Use bIsSetParametersModule in the module topology to confirm before calling.

| arg | type | req | description |
|---|---|---|---|
| `moduleRef` | `NiagaraExt_StackItemReference` | yes | Reference to the existing SetParameters module |
| `parameterName` | `string` | yes | Name of the parameter to remove |

### `RemoveUserVariables`

Removes user variables from a system.
Deletes the specified user variables from the system's user parameter collection.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to remove variables from |
| `variablesToRemove` | `[NiagaraExt_Variable{name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}]` | yes | Array of variable definitions identifying which variables to remove |

### `SetEmitterData`

Sets property values on a Niagara Emitter.
Applies new values to emitter-level properties based on the provided data structure.

| arg | type | req | description |
|---|---|---|---|
| `emitter` | `NiagaraExt_StackItemReference` | yes | Reference to the emitter to modify |
| `emitterData` | `NiagaraExt_EmitterData{propertyValues:string}` | yes | Data structure containing the property values to set |

### `SetModuleEnabled`

Sets whether a module is enabled.
Disabled modules remain in the stack but don't execute. Current state is visible in module topology.

| arg | type | req | description |
|---|---|---|---|
| `moduleRef` | `NiagaraExt_StackItemReference` | yes | Reference to the module to enable or disable |
| `bEnabled` | `boolean` | yes | True to enable the module, false to disable it |

### `SetRendererData`

Sets property values on a Niagara Renderer.
Applies new values to renderer properties based on the provided data structure.
Payload shape varies with the concrete renderer class; call GetRendererSchema for the
renderer's class to inspect valid properties before writing.

| arg | type | req | description |
|---|---|---|---|
| `renderer` | `NiagaraExt_StackItemReference` | yes | Reference to the renderer to modify |
| `rendererData` | `NiagaraExt_RendererData{propertyValues:string}` | yes | Data structure containing the property values to set |

### `SetStackInputData`

Sets the value of a stack module input and returns the resulting stored value.
Updates the value and configuration for a specific module input parameter.

| arg | type | req | description |
|---|---|---|---|
| `stackInputRef` | `NiagaraExt_StackItemReference` | yes | Reference to the stack input to modify |
| `inputData` | `NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}` | yes | The new value and configuration to apply to the input |

Returns: `NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}`

### `SetSystemData`

Sets property values on a Niagara System.
Applies new values to system-level properties based on the provided data structure.

| arg | type | req | description |
|---|---|---|---|
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara System to modify |
| `systemData` | `NiagaraExt_SystemData{propertyValues:string}` | yes | Data structure containing the property values to set |
