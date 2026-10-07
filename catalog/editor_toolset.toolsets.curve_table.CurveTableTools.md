# editor_toolset.toolsets.curve_table.CurveTableTools

Provides tools for creating and editing CurveTable assets.

10 tools.

### `add_key`

Adds a key to a row.

        Args:
            curve_table: The CurveTable to modify.
            row_name: The name of the row to modify.
            key: The key to add, containing the time and value.

        Returns:
            True if the key was added successfully.

| arg | type | req | description |
|---|---|---|---|
| `curve_table` | `ref</Script/Engine.CurveTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_name` | `string` | yes |  |
| `key` | `SimpleCurveKey{time:number, value:number}` | yes |  |

Returns: `boolean`

### `add_row`

Adds a new row to the curve table with an optional default value.

        Args:
            curve_table: The CurveTable to modify.
            row_name: The name for the new row.
            default_value: The default value returned when sampling outside the key range.

| arg | type | req | description |
|---|---|---|---|
| `curve_table` | `ref</Script/Engine.CurveTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_name` | `string` | yes |  |
| `default_value` | `number` |  |  (default `null`) |

### `create`

Creates a new CurveTable asset.

        Args:
            folder_path: The path to the folder that will contain the asset.
            asset_name: The name of the asset.

        Returns:
            The created CurveTable.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |

Returns: `ref</Script/Engine.CurveTable>`

### `diff`

Returns a unified text diff between two CurveTable assets.

        Args:
            old_asset_path: Content path to the old CurveTable.
            new_asset_path: Content path to the new CurveTable.

        Returns:
            A difflib unified-diff string. Empty when the tables are identical.

| arg | type | req | description |
|---|---|---|---|
| `old_asset_path` | `string` | yes |  |
| `new_asset_path` | `string` | yes |  |

Returns: `string`

### `get_keys`

Returns all keys for a row.

        Args:
            curve_table: The CurveTable to query.
            row_name: The name of the row to query.

        Returns:
            A list of SimpleCurveKey objects for the row.

| arg | type | req | description |
|---|---|---|---|
| `curve_table` | `ref</Script/Engine.CurveTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_name` | `string` | yes |  |

Returns: `[SimpleCurveKey{time:number, value:number}]`

### `import_file`

Imports a file from disk as a CurveTable asset.

        The file's first column is the row name; subsequent columns are sample
        times and values. interp_mode controls how the imported keys are
        interpolated between samples.

        Args:
            folder_path: The content-browser folder to create the asset in.
            asset_name: The name of the new asset.
            source_file: The absolute path to the source file on disk.
            interp_mode: Interpolation mode applied to every imported key.
                Must be RCIM_LINEAR or RCIM_CONSTANT.

        Returns:
            The assets produced by the import (typically a single CurveTable).

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |
| `source_file` | `string` | yes |  |
| `interp_mode` | `RCIM_Linear or RCIM_Constant or RCIM_Cubic or RCIM_None` | yes |  |

Returns: `[ref</Script/CoreUObject.Object>]`

### `list_rows`

Lists the names of all rows in the curve table.

        Args:
            curve_table: The CurveTable to query.

        Returns:
            A list of row names.

| arg | type | req | description |
|---|---|---|---|
| `curve_table` | `ref</Script/Engine.CurveTable>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `remove_row`

Removes a row from the curve table.

        Args:
            curve_table: The CurveTable to modify.
            row_name: The name of the row to remove.

| arg | type | req | description |
|---|---|---|---|
| `curve_table` | `ref</Script/Engine.CurveTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_name` | `string` | yes |  |

### `rename_row`

Renames a row in the curve table.

        Args:
            curve_table: The CurveTable to modify.
            row_name: The current name of the row.
            new_row_name: The new name for the row.

| arg | type | req | description |
|---|---|---|---|
| `curve_table` | `ref</Script/Engine.CurveTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_name` | `string` | yes |  |
| `new_row_name` | `string` | yes |  |

### `set_keys`

Replaces all keys in a row with the provided list.

        Args:
            curve_table: The CurveTable to modify.
            row_name: The name of the row to modify.
            keys: The keys to set in the row.

        Returns:
            True if all keys were set successfully.

| arg | type | req | description |
|---|---|---|---|
| `curve_table` | `ref</Script/Engine.CurveTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_name` | `string` | yes |  |
| `keys` | `[SimpleCurveKey{time:number, value:number}]` | yes |  |

Returns: `boolean`
