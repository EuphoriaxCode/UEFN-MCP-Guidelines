# editor_toolset.toolsets.asset.AssetTools

Generic, type-agnostic operations on project assets: finding and loading them, managing the
    asset and folder lifecycle, inspecting class, tags, metadata, and dependencies, and reading and
    writing text files on disk.

17 tools.

### `create_folder`

Creates a folder at the specified path.

        Args:
            path: The project relative path at which to create the folder.

        Returns:
            True if the folder could be created or already exists.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes |  |

Returns: `boolean`

### `delete`

Deletes an asset or folder.

        Args:
            path: The current location of the folder or asset.

        Returns:
            True if the delete happened successfully. False otherwise.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes |  |

Returns: `boolean`

### `duplicate`

Makes a copy of a folder or asset.

        Args:
            path: The current location of folder or asset.
            new_path: The location of the copy.

        Returns:
            True if the copy happened successfully. False otherwise.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes |  |
| `new_path` | `string` | yes |  |

Returns: `boolean`

### `exists`

Determines if a folder or asset exists.

        Args:
            path: The path at which an asset or folder might exist.

        Returns:
            True if an asset or folder exists at the path. False otherwise.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes |  |

Returns: `boolean`

### `find_assets`

Searches the project for assets that match specific criteria.

        Args:
            folder_path: The folder to search within. An empty string searches
                         the entire project (/Game/ and all plugin content folders
                         including project plugins and engine plugins).
            name: If set, will only return assets whose name contains this string
                  (case-insensitive).
            asset_type: If set, will only return assets that are of this type.
            recursive: Whether to search subfolders or not.
            tags: If set, will only return assets whose asset registry tags contain
                  all specified key-value pairs with exact value matches.

        Returns:
            A list of full object paths that match the criteria.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` |  |  (default `""`) |
| `name` | `string` |  |  (default `""`) |
| `asset_type` | `ref</Script/CoreUObject.Class>` |  | Represents a reference to a UObject or UClass. (default `null`) |
| `recursive` | `boolean` |  |  (default `true`) |
| `tags` | `object` |  |  (default `null`) |

Returns: `[string]`

### `get_asset_class`

Gets the class of an asset.

        Args:
            asset_path: Content path to the asset.

        Returns:
            The class name of the asset (e.g. 'StaticMesh', 'Material', 'HeroCharacter_C').

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `string`

### `get_asset_tags`

Gets the asset registry tags for an asset.

        Args:
            asset_path: Content path to the asset.

        Returns:
            A dict mapping tag names to their string values.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `object`

### `get_dependencies`

Lists assets that the specified asset depends on.

        Args:
            asset_path: Content path to the asset.

        Returns:
            A list of full object paths for assets that the given asset depends on.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `[string]`

### `get_metadata_tags`

Gets the metadata tags for an asset.

        Args:
            asset_path: Content path to the asset.

        Returns:
            A dict mapping tag names to their string values.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `object`

### `get_referencers`

Lists assets that reference the specified asset.

        Args:
            asset_path: Content path to the asset.

        Returns:
            A list of full object paths for assets that reference the given asset.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `[string]`

### `is_dirty`

Checks whether an asset has unsaved changes.

        Args:
            asset_path: The path to the asset to check.

        Returns:
            True if the asset has unsaved changes, False if it is saved.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `boolean`

### `list_folders`

Lists the folders contained within a folder.

        Args:
            root: The project relative path to the folder to search from.
            recursive: Subfolders will be searched when this is set to true.

        Returns:
            A list of paths to folders

| arg | type | req | description |
|---|---|---|---|
| `root_path` | `string` | yes |  |
| `recursive` | `boolean` |  |  (default `true`) |

Returns: `[string]`

### `load_asset`

Loads an asset from the project.

        Args:
            asset_path: The path to the asset to load.

        Returns:
            The loaded asset.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `ref</Script/CoreUObject.Object>`

### `move`

Moves or renames an asset or folder.

        Args:
            path: The current location of the folder or asset.
            new_path: The new location and/or name.

        Returns:
            True if the rename happened successfully. False otherwise.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes |  |
| `new_path` | `string` | yes |  |

Returns: `boolean`

### `reload_asset`

Reloads an asset from disk, discarding any unsaved in-memory changes.

        Args:
            asset_path: The path to the asset to reload.

        Returns:
            The reloaded asset.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `ref</Script/CoreUObject.Object>`

### `save_assets`

Saves assets to disk.

        Args:
            asset_paths: The paths to the assets to save. Pass an empty list to save
                         all dirty assets.

        Returns:
            True if all assets were saved successfully.

| arg | type | req | description |
|---|---|---|---|
| `asset_paths` | `[string]` | yes |  |

Returns: `boolean`

### `update_metadata_tags`

Sets or removes metadata tags on an asset.

        Args:
            asset_path: Content path to the asset.
            set_tags: Tag names mapped to the values to set.
            remove_tags: Tag names to remove. Removing a tag that does not
                         exist is a no-op.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |
| `set_tags` | `object` |  |  (default `null`) |
| `remove_tags` | `[string]` |  |  (default `null`) |
