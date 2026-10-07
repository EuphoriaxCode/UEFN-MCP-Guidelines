# editor_toolset.toolsets.static_mesh.StaticMeshTools

Provides tools for inspecting and modifying static mesh assets.

16 tools.

### `generate_convex_collisions`

Generates convex hull collision shapes for a static mesh.

        Convex hulls provide accurate collision for physics simulation. More hulls
        improve accuracy but increase runtime cost. Replaces any existing collision.

        Args:
            mesh: The static mesh asset to modify.
            hull_count: The number of convex hulls to generate.
            max_hull_verts: The maximum number of vertices per hull.
            hull_precision: Controls the voxel precision of the decomposition.

        Returns:
            True if convex collision was generated successfully.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |
| `hull_count` | `integer` |  |  (default `4`) |
| `max_hull_verts` | `integer` |  |  (default `16`) |
| `hull_precision` | `integer` |  |  (default `100000`) |

Returns: `boolean`

### `generate_lods`

Auto-generates LODs for a static mesh using triangle reduction.

        Each entry in triangle_percents creates one additional LOD. The value is the
        fraction of triangles to keep relative to LOD 0, from just above 0.0 (nearly
        empty) to 1.0 (full detail). For example, [0.5, 0.25] creates LOD1 with 50%
        of the original triangles and LOD2 with 25%.

        Args:
            mesh: The static mesh asset to modify.
            triangle_percents: Triangle retention fraction for each generated LOD.

        Returns:
            The total number of LODs after the operation, including LOD 0.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |
| `triangle_percents` | `[number]` | yes |  |

Returns: `integer`

### `get_bounds`

Returns the local-space bounding box of a static mesh.

        Args:
            mesh: The static mesh asset to query.

        Returns:
            The local-space axis-aligned bounding box.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `Box{min:Vector{x:number, y:number, z:number}, max:Vector{x:number, y:number, z:number}, isValid:boolean}`

### `get_lod_count`

Returns the number of LODs in a static mesh asset.

        Args:
            mesh: The static mesh asset to query.

        Returns:
            The number of LODs.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `integer`

### `get_lod_thresholds`

Returns the screen-size thresholds at which each LOD becomes active.

        Screen size is a ratio of the mesh's screen height to the viewport height. A value
        of 1.0 means the mesh fills the full viewport height; values above 1.0 are valid and
        mean the mesh must appear larger than the viewport before the next LOD activates.
        Each LOD activates when the mesh appears smaller than its threshold.

        Args:
            mesh: The static mesh asset to query.

        Returns:
            A list of screen-size threshold values, one per LOD.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[number]`

### `get_material`

Returns the material assigned to a named slot on a static mesh.

        Args:
            mesh: The static mesh asset to query.
            slot_name: The name of the material slot to query.

        Returns:
            The material assigned to the slot.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |
| `slot_name` | `string` | yes |  |

Returns: `ref</Script/Engine.MaterialInterface>`

### `get_material_slots`

Returns the names of all material slots in a static mesh.

        Material slot names are used when assigning materials to specific parts of
        the mesh. Use these names with get_material and set_material.

        Args:
            mesh: The static mesh asset to query.

        Returns:
            A list of material slot names.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `get_triangle_count`

Returns the number of triangles in a specific LOD of a static mesh.

        Args:
            mesh: The static mesh asset to query.
            lod_index: The LOD index to query. Defaults to 0 (highest quality).

        Returns:
            The number of triangles in the specified LOD.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |
| `lod_index` | `integer` |  |  (default `0`) |

Returns: `integer`

### `get_vertex_count`

Returns the number of vertices in a specific LOD of a static mesh.

        Args:
            mesh: The static mesh asset to query.
            lod_index: The LOD index to query. Defaults to 0 (highest quality).

        Returns:
            The number of vertices in the specified LOD.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |
| `lod_index` | `integer` |  |  (default `0`) |

Returns: `integer`

### `import_file`

Imports a mesh file from disk as a StaticMesh asset.

        Args:
            folder_path: The content-browser folder to create the asset in.
            asset_name: The name of the new asset.
            source_file: The absolute path to the source mesh file on disk.
            import_materials: When True, create Material assets for any materials
                referenced in the file. When False, the imported meshes have no
                materials assigned.
            import_textures: When True, create Texture2D assets for any textures
                referenced by the imported materials. Only effective when
                import_materials is True.
            combine_meshes: When True, all meshes in the file are merged into a
                single StaticMesh. When False, each mesh in the file produces
                its own StaticMesh asset.

        Returns:
            The assets produced by the import. The first entry is the primary
            StaticMesh; additional entries may include extra StaticMeshes (when
            combine_meshes is False) and Material/Texture assets (when the
            corresponding import flags are True).

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |
| `source_file` | `string` | yes |  |
| `import_materials` | `boolean` |  |  (default `false`) |
| `import_textures` | `boolean` |  |  (default `false`) |
| `combine_meshes` | `boolean` |  |  (default `true`) |

Returns: `[ref</Script/CoreUObject.Object>]`

### `is_nanite_enabled`

Returns whether Nanite is enabled for a static mesh.

        Nanite is Unreal's virtualized geometry system that renders highly detailed
        meshes efficiently. It is most beneficial for meshes with many triangles.

        Args:
            mesh: The static mesh asset to query.

        Returns:
            True if Nanite is enabled for this mesh.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `remove_collisions`

Removes all collision shapes from a static mesh.

        Args:
            mesh: The static mesh asset to modify.

        Returns:
            True if all collision shapes were removed.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `remove_lods`

Removes all auto-generated LODs from a static mesh, keeping only LOD 0.

        Args:
            mesh: The static mesh asset to modify.

        Returns:
            True if LODs were removed successfully.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `set_lod_thresholds`

Sets the screen-size thresholds at which each LOD becomes active.

        Screen size is a ratio of the mesh's screen height to the viewport height. A value
        of 1.0 means the mesh fills the full viewport height; values above 1.0 are valid and
        mean the mesh must appear larger than the viewport before the next LOD activates.
        Thresholds must be in strictly descending order (LOD 0 has the largest threshold),
        and there must be exactly one threshold per LOD.

        Args:
            mesh: The static mesh asset to modify.
            thresholds: Screen-size threshold values, one per LOD, in descending order.

        Returns:
            True if the thresholds were applied successfully.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |
| `thresholds` | `[number]` | yes |  |

Returns: `boolean`

### `set_material`

Assigns a material to a named slot on a static mesh asset.

        This affects all instances of the mesh that do not override the slot material.
        Use set_component_material_override to change materials on a single instance.

        Args:
            mesh: The static mesh asset to modify.
            slot_name: The name of the material slot to assign to.
            material: The material to assign.

        Returns:
            True if the material was assigned successfully.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |
| `slot_name` | `string` | yes |  |
| `material` | `ref</Script/Engine.MaterialInterface>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `set_nanite_enabled`

Enables or disables Nanite for a static mesh.

        Changing this setting triggers a mesh rebuild. Nanite is most beneficial for
        high-polygon meshes. Low-polygon meshes may not benefit from Nanite.

        Args:
            mesh: The static mesh asset to modify.
            enabled: True to enable Nanite, False to disable it.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.StaticMesh>` | yes | Represents a reference to a UObject or UClass. |
| `enabled` | `boolean` | yes |  |
