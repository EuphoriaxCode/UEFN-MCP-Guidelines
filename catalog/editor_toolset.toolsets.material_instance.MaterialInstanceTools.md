# editor_toolset.toolsets.material_instance.MaterialInstanceTools

Provides tools for creating and modifying MaterialInstanceConstant assets.

14 tools.

### `clear_parameters`

Clears all parameter overrides on a material instance, reverting to parent defaults.

        Args:
            instance: The MaterialInstanceConstant to clear.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |

### `create`

Creates a new MaterialInstanceConstant asset derived from a parent material.

        Material instances expose the parent's parameters without triggering a full
        shader recompile when parameter values change.

        Args:
            folder_path: The content-browser path to the folder for the new asset.
            asset_name: The name of the new asset.
            parent: The parent Material or MaterialInstance to derive from.

        Returns:
            The newly created MaterialInstanceConstant.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |
| `parent` | `ref</Script/Engine.MaterialInterface>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ref</Script/Engine.MaterialInstanceConstant>`

### `diff`

Returns a unified text diff between two MaterialInstanceConstant assets.

        Args:
            old_asset_path: Content path to the old MaterialInstanceConstant.
            new_asset_path: Content path to the new MaterialInstanceConstant.

        Returns:
            A difflib unified-diff string. Empty when the instances are identical.

| arg | type | req | description |
|---|---|---|---|
| `old_asset_path` | `string` | yes |  |
| `new_asset_path` | `string` | yes |  |

Returns: `string`

### `get_scalar_parameter`

Gets the current value of a scalar parameter on a material instance.

        Args:
            instance: The MaterialInstanceConstant to query.
            name: The parameter name.

        Returns:
            The effective scalar (float) value, inheriting from the parent if not overridden.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |

Returns: `number`

### `get_static_switch_parameter`

Gets the value of a static switch parameter on a material instance.

        Note: Overriding static switch parameters triggers a shader recompile.

        Args:
            instance: The MaterialInstanceConstant to query.
            name: The parameter name.

        Returns:
            The effective boolean value, inheriting from the parent if not overridden.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |

Returns: `boolean`

### `get_texture_parameter`

Gets the texture assigned to a texture parameter on a material instance.

        Args:
            instance: The MaterialInstanceConstant to query.
            name: The parameter name.

        Returns:
            The assigned Texture, or None if the parameter is not overridden on this instance.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |

Returns: `ref</Script/Engine.Texture>`

### `get_vector_parameter`

Gets the current value of a vector parameter on a material instance.

        Args:
            instance: The MaterialInstanceConstant to query.
            name: The parameter name.

        Returns:
            The effective value as a LinearColor (RGBA), inheriting from the parent if
            not overridden.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |

Returns: `LinearColor{r:number, g:number, b:number, a:number}`

### `list_parameters`

Returns all parameters exposed by a material or instance, with their names and types.

        Args:
            material: The Material or MaterialInstance to query.

        Returns:
            A list of MaterialParameter entries, each with a name and a type.

| arg | type | req | description |
|---|---|---|---|
| `material` | `ref</Script/Engine.MaterialInterface>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[MaterialParameter{type:Scalar or Vector or Texture or StaticSwitch, name:string}]`

### `set_parameter_override`

Enables or disables a parameter override on a material instance.

        Enabling sets the override to the current effective value. Disabling reverts
        to the parent. For non-static parameter types, disabling also discards the
        prior override value; re-enabling later restores the parent value, not the
        prior override. Static switches and static component masks preserve their
        value across toggle.

        Args:
            instance: The MaterialInstanceConstant to modify.
            name: The parameter name.
            override: True to enable the override, False to clear it.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `override` | `boolean` | yes |  |

### `set_parent`

Changes the parent of a material instance.

        Args:
            instance: The MaterialInstanceConstant to modify.
            parent: The new parent Material or MaterialInstance.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `parent` | `ref</Script/Engine.MaterialInterface>` | yes | Represents a reference to a UObject or UClass. |

### `set_scalar_parameter`

Sets the value of a scalar parameter on a material instance.

        Args:
            instance: The MaterialInstanceConstant to modify.
            name: The parameter name.
            value: The new scalar (float) value.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `value` | `number` | yes |  |

### `set_static_switch_parameter`

Sets the value of a static switch parameter on a material instance.

        Args:
            instance: The MaterialInstanceConstant to modify.
            name: The parameter name.
            value: The new boolean value.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `value` | `boolean` | yes |  |

### `set_texture_parameter`

Assigns a texture to a texture parameter on a material instance.

        Args:
            instance: The MaterialInstanceConstant to modify.
            name: The parameter name.
            value: The Texture asset to assign.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `value` | `ref</Script/Engine.Texture>` | yes | Represents a reference to a UObject or UClass. |

### `set_vector_parameter`

Sets the value of a vector parameter on a material instance.

        Args:
            instance: The MaterialInstanceConstant to modify.
            name: The parameter name.
            value: The new value as a LinearColor (RGBA). Use values in the range 0–1
                for standard colors; values above 1 are valid for HDR and emissive.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/Engine.MaterialInstanceConstant>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `value` | `LinearColor{r:number, g:number, b:number, a:number}` | yes |  |
