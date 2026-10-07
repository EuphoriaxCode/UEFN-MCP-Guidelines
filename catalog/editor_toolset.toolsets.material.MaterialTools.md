# editor_toolset.toolsets.material.MaterialTools

Provides tools for creating and editing Material and MaterialFunction assets.

25 tools.

### `add_expression`

Adds a new expression node to a Material or MaterialFunction graph.

        Use list_expression_classes to discover available types.

        Args:
            material_or_function: The Material or MaterialFunction to add the expression to.
            expression_class: The type of expression node to create.
            x: Horizontal position in the graph editor.
            y: Vertical position in the graph editor.

        Returns:
            The newly created MaterialExpression node.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `expression_class` | `ref</Script/CoreUObject.Class>` | yes | Represents a reference to a UObject or UClass. |
| `x` | `integer` |  |  (default `0`) |
| `y` | `integer` |  |  (default `0`) |

Returns: `ref</Script/Engine.MaterialExpression>`

### `connect_expressions`

Connects an expression node's output pin to another expression node's input pin.

        Args:
            from_expression: The expression providing the output value.
            from_output_name: The output pin name. Pass an empty string to use the
                default (first) output.
            to_expression: The expression receiving the input.
            to_input_name: The input pin name to connect to. Use get_expression_input_names
                to discover valid names.

| arg | type | req | description |
|---|---|---|---|
| `from_expression` | `ref</Script/Engine.MaterialExpression>` | yes | Represents a reference to a UObject or UClass. |
| `from_output_name` | `string` | yes |  |
| `to_expression` | `ref</Script/Engine.MaterialExpression>` | yes | Represents a reference to a UObject or UClass. |
| `to_input_name` | `string` | yes |  |

### `connect_to_output`

Connects an expression node's output to one of the material's output properties.

        Args:
            expression: The expression whose output will drive the property.
            output_name: The output pin name. Pass an empty string to use the
                default (first) output.
            material_property: The material output property to connect to.

| arg | type | req | description |
|---|---|---|---|
| `expression` | `ref</Script/Engine.MaterialExpression>` | yes | Represents a reference to a UObject or UClass. |
| `output_name` | `string` | yes |  |
| `material_property` | `MP_EmissiveColor or MP_Opacity or MP_OpacityMask or MP_DiffuseColor or MP_SpecularColor or MP_BaseColor or MP_Metallic or MP_Specular or MP_Roughness or MP_Anisotropy or MP_Normal or MP_Tangent or MP_WorldPositionOffset or MP_WorldDisplacement_DEPRECATED or MP_TessellationMultiplier_DEPRECATED or MP_SubsurfaceColor or MP_CustomData0 or MP_CustomData1 or MP_AmbientOcclusion or MP_Refraction or MP_CustomizedUVs0 or MP_CustomizedUVs1 or MP_CustomizedUVs2 or MP_CustomizedUVs3 or MP_CustomizedUVs4 or MP_CustomizedUVs5 or MP_CustomizedUVs6 or MP_CustomizedUVs7 or MP_PixelDepthOffset or MP_ShadingModel or MP_FrontMaterial or MP_SurfaceThickness or MP_Displacement or MP_MaterialAttributes or MP_CustomOutput or MP_LastCustomizedUVs or MP_NumCustomizedUVs` | yes |  |

### `create_function`

Creates a new empty MaterialFunction asset.

        Args:
            folder_path: The content-browser path to the folder for the new asset.
            asset_name: The name of the new asset.

        Returns:
            The newly created MaterialFunction.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |

Returns: `ref</Script/Engine.MaterialFunction>`

### `create_material`

Creates a new empty Material asset.

        Warning: Each new Material increases shader compile times. Prefer creating
        a MaterialInstance from an existing Material where possible.

        Args:
            folder_path: The content-browser path to the folder for the new asset.
            asset_name: The name of the new asset.

        Returns:
            The newly created Material.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |

Returns: `ref</Script/Engine.Material>`

### `create_parameter_collection`

Creates a new empty MaterialParameterCollection (MPC) asset.

        An MPC holds named Scalar and Vector parameters with default values
        that materials can reference at runtime without recompiling shaders.

        Args:
            folder_path: The content-browser path to the folder for the new asset.
            asset_name: The name of the new asset.

        Returns:
            The newly created MaterialParameterCollection.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |

Returns: `ref</Script/Engine.MaterialParameterCollection>`

### `delete_expression`

Removes an expression node from a Material or MaterialFunction graph.

        Args:
            material_or_function: The Material or MaterialFunction that owns the expression.
            expression: The expression node to remove.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `expression` | `ref</Script/Engine.MaterialExpression>` | yes | Represents a reference to a UObject or UClass. |

### `delete_parameter_group`

Removes a parameter group, ungrouping all parameters that belong to it.

        The parameter expressions themselves are not deleted - only their group assignment
        is cleared.

        Note: triggers an internal recompile; no separate call to recompile/update is needed.

        Args:
            material_or_function: The Material or MaterialFunction to modify.
            group_name: The name of the group to delete.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `group_name` | `string` | yes |  |

### `delete_unused_expressions`

Deletes all expression nodes not connected to any material output.

        Useful for cleaning up a material graph after reorganising or after the AI
        has added experimental nodes that were later abandoned.

        Note: triggers no recompile - call recompile() afterwards if needed.

        Args:
            material: The Material to clean up.

| arg | type | req | description |
|---|---|---|---|
| `material` | `ref</Script/Engine.Material>` | yes | Represents a reference to a UObject or UClass. |

### `diff_function`

Returns a unified text diff between two MaterialFunction assets.

        Args:
            old_asset_path: Content path to the old MaterialFunction.
            new_asset_path: Content path to the new MaterialFunction.

        Returns:
            A difflib unified-diff string. Empty when the functions are identical.

| arg | type | req | description |
|---|---|---|---|
| `old_asset_path` | `string` | yes |  |
| `new_asset_path` | `string` | yes |  |

Returns: `string`

### `diff_material`

Returns a unified text diff between two Material assets.

        Args:
            old_asset_path: Content path to the old Material.
            new_asset_path: Content path to the new Material.

        Returns:
            A difflib unified-diff string. Empty when the materials are identical.

| arg | type | req | description |
|---|---|---|---|
| `old_asset_path` | `string` | yes |  |
| `new_asset_path` | `string` | yes |  |

Returns: `string`

### `disconnect_expressions`

Disconnects the input pin of an expression node, removing whatever is connected to it.

        Args:
            to_expression: The expression whose input pin should be disconnected.
            to_input_name: The input pin name to disconnect. Use get_expression_input_names
                to discover valid names. Pass an empty string to disconnect the first input.

| arg | type | req | description |
|---|---|---|---|
| `to_expression` | `ref</Script/Engine.MaterialExpression>` | yes | Represents a reference to a UObject or UClass. |
| `to_input_name` | `string` | yes |  |

### `disconnect_from_output`

Disconnects the expression currently connected to a material output property.

        Args:
            material: The Material to modify.
            material_property: The material output property to disconnect.

| arg | type | req | description |
|---|---|---|---|
| `material` | `ref</Script/Engine.Material>` | yes | Represents a reference to a UObject or UClass. |
| `material_property` | `MP_EmissiveColor or MP_Opacity or MP_OpacityMask or MP_DiffuseColor or MP_SpecularColor or MP_BaseColor or MP_Metallic or MP_Specular or MP_Roughness or MP_Anisotropy or MP_Normal or MP_Tangent or MP_WorldPositionOffset or MP_WorldDisplacement_DEPRECATED or MP_TessellationMultiplier_DEPRECATED or MP_SubsurfaceColor or MP_CustomData0 or MP_CustomData1 or MP_AmbientOcclusion or MP_Refraction or MP_CustomizedUVs0 or MP_CustomizedUVs1 or MP_CustomizedUVs2 or MP_CustomizedUVs3 or MP_CustomizedUVs4 or MP_CustomizedUVs5 or MP_CustomizedUVs6 or MP_CustomizedUVs7 or MP_PixelDepthOffset or MP_ShadingModel or MP_FrontMaterial or MP_SurfaceThickness or MP_Displacement or MP_MaterialAttributes or MP_CustomOutput or MP_LastCustomizedUVs or MP_NumCustomizedUVs` | yes |  |

### `get_expression_input_names`

Returns the names of all input pins on a material expression node.

        Use these names as to_input_name when calling connect_expressions.

        Args:
            expression: The expression node to query.

        Returns:
            The input pin names available on the expression.

| arg | type | req | description |
|---|---|---|---|
| `expression` | `ref</Script/Engine.MaterialExpression>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `get_expression_inputs`

Returns the current wiring of each input pin on a material expression.

        Use after building or modifying a graph to verify the wiring matches
        expectations.

        Args:
            material_or_function: The Material or MaterialFunction that owns the expression.
            expression: The expression whose input wiring to read.

        Returns:
            One entry per input pin, in declaration order matching
            get_expression_input_names. The expression field is None for
            unwired pins.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `expression` | `ref</Script/Engine.MaterialExpression>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[MaterialInputSource{output_name:string, expression:ref</Script/Engine.MaterialExpression>, input_name:string}]`

### `get_expression_output_names`

Returns the names of all output pins on a material expression node.

        Use these names as from_output_name when calling connect_expressions or
        connect_to_output. The empty string represents the default (first) output
        of nodes that expose only an unnamed output.

        Args:
            expression: The expression node to query.

        Returns:
            The output pin names available on the expression.

| arg | type | req | description |
|---|---|---|---|
| `expression` | `ref</Script/Engine.MaterialExpression>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `get_expressions`

Returns all expression nodes in a Material or MaterialFunction graph.

        Args:
            material_or_function: The Material or MaterialFunction to query.

        Returns:
            All MaterialExpression nodes in the graph.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[ref</Script/Engine.MaterialExpression>]`

### `get_property_input`

Returns the expression and output pin feeding a material output property.

        Use to inspect what drives MP_EmissiveColor, MP_Opacity, MP_BaseColor, etc.

        Args:
            material: The Material to query.
            material_property: The material output property.

        Returns:
            A MaterialInputSource with input_name empty. Its expression field is
            None when the output property is disconnected.

| arg | type | req | description |
|---|---|---|---|
| `material` | `ref</Script/Engine.Material>` | yes | Represents a reference to a UObject or UClass. |
| `material_property` | `MP_EmissiveColor or MP_Opacity or MP_OpacityMask or MP_DiffuseColor or MP_SpecularColor or MP_BaseColor or MP_Metallic or MP_Specular or MP_Roughness or MP_Anisotropy or MP_Normal or MP_Tangent or MP_WorldPositionOffset or MP_WorldDisplacement_DEPRECATED or MP_TessellationMultiplier_DEPRECATED or MP_SubsurfaceColor or MP_CustomData0 or MP_CustomData1 or MP_AmbientOcclusion or MP_Refraction or MP_CustomizedUVs0 or MP_CustomizedUVs1 or MP_CustomizedUVs2 or MP_CustomizedUVs3 or MP_CustomizedUVs4 or MP_CustomizedUVs5 or MP_CustomizedUVs6 or MP_CustomizedUVs7 or MP_PixelDepthOffset or MP_ShadingModel or MP_FrontMaterial or MP_SurfaceThickness or MP_Displacement or MP_MaterialAttributes or MP_CustomOutput or MP_LastCustomizedUVs or MP_NumCustomizedUVs` | yes |  |

Returns: `MaterialInputSource{output_name:string, expression:ref</Script/Engine.MaterialExpression>, input_name:string}`

### `get_referencing_materials`

Returns asset data for all Materials that reference this MaterialFunction.

        Args:
            material_function: The MaterialFunction to query.

        Returns:
            Asset data for each Material that uses this function.

| arg | type | req | description |
|---|---|---|---|
| `material_function` | `ref</Script/Engine.MaterialFunction>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[AssetData{packageName:string, packagePath:string, assetName:string, assetClassPath:TopLevelAssetPath{packageName:string, assetName:string}}]`

### `get_statistics`

Returns compiled shader statistics for a Material or MaterialInstance on
        the current shader platform: instruction counts, texture-sample counts, and
        sampler usage.

        Args:
            material: The Material or MaterialInstance to measure.

        Returns:
            A dict of integer stats: num_pixel_shader_instructions,
            num_vertex_shader_instructions, num_samplers, num_pixel_texture_samples,
            num_vertex_texture_samples, num_virtual_texture_samples, num_uv_scalars,
            num_interpolator_scalars.

| arg | type | req | description |
|---|---|---|---|
| `material` | `ref</Script/Engine.MaterialInterface>` | yes | Represents a reference to a UObject or UClass. |

Returns: `object`

### `layout_expressions`

Automatically arranges all expression nodes in a Material or MaterialFunction graph.

        Args:
            material_or_function: The Material or MaterialFunction whose graph should be tidied.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |

### `list_expression_classes`

Returns MaterialExpression subclasses valid for the given context.

        Use the results with add_expression. Pass a search string to filter by name,
        e.g. 'Multiply' or 'Parameter'.

        Args:
            material_or_function: The Material or MaterialFunction to filter by context.
            search: Optional case-insensitive substring filter on the class path.

        Returns:
            Matching MaterialExpression subclass paths.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `search` | `string` |  |  (default `""`) |

Returns: `[ref<Class@/Script/CoreUObject.Object>]`

### `list_parameter_groups`

Returns the unique parameter group names defined in a Material or MaterialFunction.

        Parameters are organised into groups in the Material Instance editor. This returns
        the distinct set of group names found across all parameter expressions in the graph.
        The empty string represents parameters that have not been assigned to a named group.

        Args:
            material_or_function: The Material or MaterialFunction to query.

        Returns:
            A sorted list of unique group names.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `recompile`

Recompiles a Material or MaterialFunction after edits.

        For Materials, raises if the shader fails to compile. For MaterialFunctions,
        also recompiles any Materials that reference the function.

        Call this once after a set of graph modifications is complete - after adding or
        deleting expressions, making connections, or changing expression properties such as
        parameter names or default values.

        Args:
            material_or_function: The Material or MaterialFunction to recompile.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |

### `rename_parameter_group`

Renames a parameter group across all parameter expressions in a Material or
        MaterialFunction.

        All parameters currently in old_name will be moved to new_name. If new_name
        already exists, the parameters are merged into it.

        Note: triggers an internal recompile; no separate call to recompile/update is needed.

        Args:
            material_or_function: The Material or MaterialFunction to modify.
            old_name: The current name of the group to rename.
            new_name: The new name for the group.

| arg | type | req | description |
|---|---|---|---|
| `material_or_function` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `old_name` | `string` | yes |  |
| `new_name` | `string` | yes |  |
