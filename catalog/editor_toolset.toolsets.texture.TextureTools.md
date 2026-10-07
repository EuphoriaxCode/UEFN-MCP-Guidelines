# editor_toolset.toolsets.texture.TextureTools

Provides tools for importing, inspecting, reading, and exporting Texture2D assets.

4 tools.

### `export_png`

Exports a Texture to a PNG file on disk.

        Args:
            texture: The Texture to export.
            file_path: The absolute path of the .png file to write.

| arg | type | req | description |
|---|---|---|---|
| `texture` | `ref</Script/Engine.Texture2D>` | yes | Represents a reference to a UObject or UClass. |
| `file_path` | `string` | yes |  |

### `get_size`

Returns the dimensions of a Texture2D in pixels.

        Args:
            texture: The Texture2D to query.

        Returns:
            A vector x is the width and y is the height, both in pixels.

| arg | type | req | description |
|---|---|---|---|
| `texture` | `ref</Script/Engine.Texture2D>` | yes | Represents a reference to a UObject or UClass. |

Returns: `IntPoint{x:integer, y:integer}`

### `import_file`

Imports an image file from disk as a Texture2D asset.

        Args:
            folder_path: The content-browser folder to create the asset in.
            asset_name: The name of the new asset.
            source_file: The absolute path to the source image file on disk.

        Returns:
            The assets produced by the import (typically a single Texture2D).

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |
| `source_file` | `string` | yes |  |

Returns: `[ref</Script/CoreUObject.Object>]`

### `read_texture`

Reads a Texture and returns it as an image.

        Args:
            texture: The Texture to read.

        Returns:
            A full-resolution image of the texture.

| arg | type | req | description |
|---|---|---|---|
| `texture` | `ref</Script/Engine.Texture2D>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ToolsetImage{mimeType:string, data:string}`
