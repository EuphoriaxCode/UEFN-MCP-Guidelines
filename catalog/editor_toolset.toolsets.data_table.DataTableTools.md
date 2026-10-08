# editor_toolset.toolsets.data_table.DataTableTools

Provides tools for creating and editing DataTable assets.

11 tools.

### `add_rows`

Adds new rows with default values to the data table.

        Args:
            data_table: The DataTable to modify.
            row_names: The names for the new rows.

| arg | type | req | description |
|---|---|---|---|
| `data_table` | `ref</Script/Engine.DataTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_names` | `[string]` | yes |  |

### `create`

Creates a new DataTable asset with the specified column schema.

        Args:
            folder_path: The path to the folder that will contain the asset.
            asset_name: The name of the asset.
            schema: The struct that defines the columns of the table.
                    Must be a subclass of TableRowBase.

        Returns:
            The created DataTable.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |
| `schema` | `ref</Script/CoreUObject.ScriptStruct>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ref</Script/Engine.DataTable>`

### `diff`

Returns a unified text diff between two DataTable assets.

        Args:
            old_asset_path: Content path to the old DataTable.
            new_asset_path: Content path to the new DataTable.

        Returns:
            A difflib unified-diff string. Empty when the tables are identical.

| arg | type | req | description |
|---|---|---|---|
| `old_asset_path` | `string` | yes |  |
| `new_asset_path` | `string` | yes |  |

Returns: `string`

### `get_rows`

Returns the column values for one or more rows as a JSON string.

        Args:
            data_table: The DataTable to query.
            row_names: The names of the rows to retrieve.

        Returns:
            A JSON object mapping each row name to an object of property names and values.

| arg | type | req | description |
|---|---|---|---|
| `data_table` | `ref</Script/Engine.DataTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_names` | `[string]` | yes |  |

Returns: `string`

### `get_schema`

Returns the column schema of the data table as a JSON string.

        Args:
            data_table: The DataTable to query.

        Returns:
            A JSON formatted string mapping column names to their type info.

| arg | type | req | description |
|---|---|---|---|
| `data_table` | `ref</Script/Engine.DataTable>` | yes | Represents a reference to a UObject or UClass. |

Returns: `string`

### `import_file`

Imports a file from disk as a DataTable asset.

        The file's columns must match the property names in schema. Use
        search_row_structs to discover usable schema structs.

        Args:
            folder_path: The content-browser folder to create the asset in.
            asset_name: The name of the new asset.
            source_file: The absolute path to the source file on disk.
            schema: The struct that defines the columns of the table. Must be a
                subclass of TableRowBase.

        Returns:
            The assets produced by the import (typically a single DataTable).

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |
| `source_file` | `string` | yes |  |
| `schema` | `ref</Script/CoreUObject.ScriptStruct>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[ref</Script/CoreUObject.Object>]`

### `list_rows`

Lists the names of all rows in the data table.

        Args:
            data_table: The DataTable to query.

        Returns:
            A list of row names.

| arg | type | req | description |
|---|---|---|---|
| `data_table` | `ref</Script/Engine.DataTable>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `remove_rows`

Removes rows from the data table.

        Args:
            data_table: The DataTable to modify.
            row_names: The names of the rows to remove.

| arg | type | req | description |
|---|---|---|---|
| `data_table` | `ref</Script/Engine.DataTable>` | yes | Represents a reference to a UObject or UClass. |
| `row_names` | `[string]` | yes |  |

### `rename_rows`

Renames one or more rows in the data table.

        Args:
            data_table: The DataTable to modify.
            renames: A mapping of existing row names to their new names.

| arg | type | req | description |
|---|---|---|---|
| `data_table` | `ref</Script/Engine.DataTable>` | yes | Represents a reference to a UObject or UClass. |
| `renames` | `object` | yes |  |

### `search_row_structs`

Finds structs that can be used as a DataTable schema.

        Args:
            struct_name: If set, will filter structs by name using wildcard match.

        Returns:
            A list of structs derived from TableRowBase that match the criteria.

| arg | type | req | description |
|---|---|---|---|
| `struct_name` | `string` |  |  (default `"*"`) |

Returns: `[ref</Script/CoreUObject.ScriptStruct>]`

### `set_rows`

Sets column values for one or more rows.

        Args:
            data_table: The DataTable to modify.
            values: A JSON object mapping row names to objects of camelCase property
                    names and values to update. Only specified properties are updated;
                    others remain unchanged.

| arg | type | req | description |
|---|---|---|---|
| `data_table` | `ref</Script/Engine.DataTable>` | yes | Represents a reference to a UObject or UClass. |
| `values` | `string` | yes |  |
