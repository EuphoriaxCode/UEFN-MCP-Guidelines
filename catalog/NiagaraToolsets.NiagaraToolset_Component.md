# NiagaraToolsets.NiagaraToolset_Component

Niagara Toolset for Niagara Component operations.

Use this toolset when working with:
- Niagara Components on actors
- Runtime Niagara system manipulation
- User variable overrides on component instances
- FX-related operations in levels or blueprints

This is the primary toolset for runtime Niagara operations.

4 tools.

### `GetUserVariables`

Returns all user variable values currently set on the component.
This retrieves the current values of all user-exposed parameters that can be overridden at the component level.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Niagara.NiagaraComponent>` | yes | The Niagara component to retrieve user variables from |

Returns: `[NiagaraExt_VariableInst{value:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}, name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}]`

### `GetVariable`

Gets the current value of a specific user variable on the component.
This retrieves the current value of a user-exposed parameter, including any component-level overrides.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Niagara.NiagaraComponent>` | yes | The Niagara component to retrieve the variable from |
| `var` | `NiagaraExt_Variable{name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}` | yes | The variable definition (name and type) to look up |

Returns: `NiagaraExt_VariableInst{value:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}, name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}`

### `SetSystem`

Sets the Niagara System for a component.
Use this instead of setting the Asset property directly to ensure proper initialization.

| arg | type | req | description |
|---|---|---|---|
| `niagaraComponent` | `ref</Script/Niagara.NiagaraComponent>` | yes | The Niagara component to set the system on |
| `system` | `ref</Script/Niagara.NiagaraSystem>` | yes | The Niagara system asset to assign to the component |
| `bResetExistingOverrideParameters` | `boolean` | yes | If true, reset all user variables to system defaults; if false, preserve matching overrides |

### `SetVariable`

Sets the value of a user variable on the component.
This overrides the default value of a user-exposed parameter on a specific component instance.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Niagara.NiagaraComponent>` | yes | The Niagara component to set the variable on |
| `variable` | `NiagaraExt_VariableInst{value:NiagaraToolsetInstancedValue{struct:ref</Script/CoreUObject.ScriptStruct>, value:?}, name:string, type:ToolsetNiagaraTypeDefinition{classStructOrEnum:ref</Script/CoreUObject.Object>}}` | yes | The variable instance containing the name and new value to set |
