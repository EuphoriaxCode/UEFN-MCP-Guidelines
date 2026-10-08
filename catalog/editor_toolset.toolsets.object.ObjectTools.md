# editor_toolset.toolsets.object.ObjectTools

Provides tools for inspecting and modifying the properties of
    Unreal Objects and Unreal Classes, including those in Blueprints.
    Also use this toolset to discover available classes and subclasses.

6 tools.

### `get_class`

Returns the class of an Unreal object.

        Args:
            instance: The object instance to query.

        Returns:
            The class of the object.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ref</Script/CoreUObject.Class>`

### `get_properties`

Returns the values of one or more properties on an object.

        Args:
            instance: The the object to query.
            properties: The names of the properties to query.

        Returns:
            A JSON formatted string of the properties and their values.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `properties` | `[string]` | yes |  |

Returns: `string`

### `list_properties`

Returns a list of properties that are on the specified object.

        Args:
            instance: The object to query.

        Returns:
            A list of properties on the object.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |

Returns: `string`

### `reset_properties`

Resets one or more properties on an object to their default values,
        removing any per-instance overrides.

        Args:
            instance: The object with the properties to reset.
            properties: The names of the properties to reset to their defaults.

        Returns:
            True if all properties were reset. False otherwise.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `properties` | `[string]` | yes |  |

Returns: `boolean`

### `search_subclasses`

Finds all subclasses of a given class.

        Args:
            base_class: The class to search subclasses of.
            class_name: Optional case-insensitive substring filter on the class path.

        Returns:
            A list of subclasses matching the filter.

| arg | type | req | description |
|---|---|---|---|
| `base_class` | `ref</Script/CoreUObject.Class>` | yes | Represents a reference to a UObject or UClass. |
| `class_name` | `string` |  |  (default `""`) |

Returns: `[ref<Class@/Script/CoreUObject.Object>]`

### `set_properties`

Sets the values of properties on an object.

        Args:
            instance: The object with the property.
            values: A JSON formatted string of the properties to set and their values.
                For instanced sub-object properties, pass a class path as the instance member.

        Returns:
            True if the property was set. False otherwise.

| arg | type | req | description |
|---|---|---|---|
| `instance` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `values` | `string` | yes |  |

Returns: `boolean`
