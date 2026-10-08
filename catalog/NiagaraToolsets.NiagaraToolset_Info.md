# NiagaraToolsets.NiagaraToolset_Info

Niagara Toolset for general Niagara information and guidance.

Provides:
- Enum value lookups
- General usage information

Call these functions when you need context about Niagara types.

1 tools.

### `UEnum_Info`

Returns information about a UEnum and all its values.
ALWAYS call this when working with a UEnum type to see valid values.

| arg | type | req | description |
|---|---|---|---|
| `enum` | `ref</Script/CoreUObject.Enum>` | yes | Represents a reference to a UObject or UClass. |

Returns: `string`
