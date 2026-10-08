# editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools

Provides tools for inspecting and modifying skeletal mesh assets, including
    the mesh/materials, bone hierarchies, and sockets.

22 tools.

### `add_socket`

Adds a named socket to a skeletal mesh attached to a bone.

        Sockets are named attachment points used to attach weapons, accessories,
        or effects at a consistent position relative to a bone.

        Args:
            mesh: The skeletal mesh asset to modify.
            socket_name: The name to give the new socket.
            bone_name: The name of the bone to attach the socket to.

        Returns:
            The newly created socket.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `socket_name` | `string` | yes |  |
| `bone_name` | `string` | yes |  |

Returns: `ref</Script/Engine.SkeletalMeshSocket>`

### `assign_physics_asset`

Assigns a physics asset to a skeletal mesh.

        The physics asset must be compatible with the mesh's skeleton. Use this
        to swap physics assets or assign one to a mesh that has none.

        Args:
            mesh: The skeletal mesh asset to modify.
            physics_asset: The physics asset to assign.

        Returns:
            True if the physics asset was assigned successfully.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `physics_asset` | `ref</Script/Engine.PhysicsAsset>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `get_bone_children`

Returns the direct children of a bone.

        Args:
            mesh: The skeletal mesh asset to query.
            bone_name: The name of the bone to query.

        Returns:
            A list of direct child bone names, or an empty list for leaf bones.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `bone_name` | `string` | yes |  |

Returns: `[string]`

### `get_bone_names`

Returns the names of all bones in a skeletal mesh in hierarchy order.

        Bone names are used to target specific bones for socket attachment, physics
        constraints, and animation retargeting.

        Args:
            mesh: The skeletal mesh asset to query.

        Returns:
            A list of bone names in skeleton order (root first).

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `get_bone_parent`

Returns the name of a bone's parent, or an empty string for the root bone.

        Args:
            mesh: The skeletal mesh asset to query.
            bone_name: The name of the bone to query.

        Returns:
            The parent bone name, or '' if the bone is the root.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `bone_name` | `string` | yes |  |

Returns: `string`

### `get_bounds`

Returns the local-space bounding volume of a skeletal mesh.

        The bounds represent the reference pose and do not account for animation.

        Args:
            mesh: The skeletal mesh asset to query.

        Returns:
            The local-space bounding volume as a combined box and sphere.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `BoxSphereBounds{origin:Vector{x:number, y:number, z:number}, boxExtent:Vector{x:number, y:number, z:number}, sphereRadius:number}`

### `get_lod_count`

Returns the number of LODs in a skeletal mesh asset.

        Args:
            mesh: The skeletal mesh asset to query.

        Returns:
            The number of LODs.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `integer`

### `get_material`

Returns the material assigned to a named slot on a skeletal mesh.

        Args:
            mesh: The skeletal mesh asset to query.
            slot_name: The name of the material slot to query.

        Returns:
            The material assigned to the slot.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `slot_name` | `string` | yes |  |

Returns: `ref</Script/Engine.MaterialInterface>`

### `get_material_slots`

Returns the names of all material slots in a skeletal mesh.

        Material slot names are used when assigning materials to specific parts of
        the mesh. Use these names with get_material and set_material.

        Args:
            mesh: The skeletal mesh asset to query.

        Returns:
            A list of material slot names.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `get_morph_target_names`

Returns the names of all morph targets on a skeletal mesh.

        Morph targets (blend shapes) are per-vertex offsets used to deform the mesh,
        commonly used for facial expressions and cloth simulation.

        Args:
            mesh: The skeletal mesh asset to query.

        Returns:
            A list of morph target names, or an empty list if none exist.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `get_physics_asset`

Returns the physics asset assigned to a skeletal mesh.

        The physics asset defines the collision bodies and constraints used for
        ragdoll simulation and per-bone physics.

        Args:
            mesh: The skeletal mesh asset to query.

        Returns:
            The physics asset assigned to this mesh.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ref</Script/Engine.PhysicsAsset>`

### `get_section_count`

Returns the number of sections in a specific LOD of a skeletal mesh.

        Sections correspond to individual material slots rendered by a single draw call.
        A mesh may have more sections than material slots if multiple sections share
        the same material.

        Args:
            mesh: The skeletal mesh asset to query.
            lod_index: The LOD index to query. Defaults to 0 (highest quality).

        Returns:
            The number of sections in the specified LOD.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `lod_index` | `integer` |  |  (default `0`) |

Returns: `integer`

### `get_skeleton`

Returns the skeleton asset associated with a skeletal mesh.

        The skeleton defines the bone hierarchy shared across all meshes and
        animations that use it.

        Args:
            mesh: The skeletal mesh asset to query.

        Returns:
            The skeleton asset bound to this mesh.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ref</Script/Engine.Skeleton>`

### `get_socket_bone`

Returns the name of the bone that a socket is attached to.

        Args:
            mesh: The skeletal mesh asset to query.
            socket_name: The name of the socket to query.

        Returns:
            The name of the parent bone.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `socket_name` | `string` | yes |  |

Returns: `string`

### `get_socket_names`

Returns the names of all sockets on a skeletal mesh.

        Sockets are named attachment points parented to bones. They are used to
        attach weapons, accessories, or effects at a consistent location.

        Args:
            mesh: The skeletal mesh asset to query.

        Returns:
            A list of socket names, or an empty list if none exist.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `get_socket_transform`

Returns the local transform of a socket relative to its parent bone.

        Args:
            mesh: The skeletal mesh asset to query.
            socket_name: The name of the socket to query.

        Returns:
            The socket's local transform (translation, rotation, scale).

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `socket_name` | `string` | yes |  |

Returns: `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}`

### `get_vertex_count`

Returns the number of vertices in a specific LOD of a skeletal mesh.

        Args:
            mesh: The skeletal mesh asset to query.
            lod_index: The LOD index to query. Defaults to 0 (highest quality).

        Returns:
            The number of vertices in the specified LOD.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `lod_index` | `integer` |  |  (default `0`) |

Returns: `integer`

### `import_file`

Imports a mesh file from disk as a SkeletalMesh asset.

        The source file must contain a skeleton hierarchy and skinned mesh data.

        Args:
            folder_path: The content-browser folder to create the asset in.
            asset_name: The name of the new asset.
            source_file: The absolute path to the source mesh file on disk.
            skeleton: An existing skeleton to bind the imported mesh to. When
                None, a new Skeleton asset is created alongside the mesh.
            import_materials: When True, create Material assets for any materials
                referenced in the file. When False, the imported mesh has no
                materials assigned.
            import_textures: When True, create Texture2D assets for any textures
                referenced by the imported materials. Only effective when
                import_materials is True.
            import_animations: When True, create AnimSequence assets for any
                animations contained in the file.
            create_physics_asset: When True, create a PhysicsAsset bound to the
                imported mesh's skeleton.

        Returns:
            The assets produced by the import. The first entry is the imported
            SkeletalMesh; additional entries may include a newly created
            Skeleton (when none was supplied), a PhysicsAsset, AnimSequences,
            Materials, and Texture2Ds, depending on which options are enabled.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `asset_name` | `string` | yes |  |
| `source_file` | `string` | yes |  |
| `skeleton` | `ref</Script/Engine.Skeleton>` |  | Represents a reference to a UObject or UClass. (default `null`) |
| `import_materials` | `boolean` |  |  (default `false`) |
| `import_textures` | `boolean` |  |  (default `false`) |
| `import_animations` | `boolean` |  |  (default `false`) |
| `create_physics_asset` | `boolean` |  |  (default `false`) |

Returns: `[ref</Script/CoreUObject.Object>]`

### `remove_socket`

Removes a named socket from a skeletal mesh.

        Args:
            mesh: The skeletal mesh asset to modify.
            socket_name: The name of the socket to remove.

        Returns:
            True if the socket was removed successfully.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `socket_name` | `string` | yes |  |

Returns: `boolean`

### `rename_socket`

Renames a socket on a skeletal mesh.

        Args:
            mesh: The skeletal mesh asset to modify.
            old_name: The current name of the socket.
            new_name: The new name to give the socket.

        Returns:
            True if the socket was renamed successfully.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `old_name` | `string` | yes |  |
| `new_name` | `string` | yes |  |

Returns: `boolean`

### `set_material`

Assigns a material to a named slot on a skeletal mesh asset.

        This affects all instances of the mesh that do not override the slot material.

        Args:
            mesh: The skeletal mesh asset to modify.
            slot_name: The name of the material slot to assign to.
            material: The material to assign.

        Returns:
            True if the material was assigned successfully.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `slot_name` | `string` | yes |  |
| `material` | `ref</Script/Engine.MaterialInterface>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `set_socket_transform`

Sets the local transform of a socket relative to its parent bone.

        Args:
            mesh: The skeletal mesh asset to modify.
            socket_name: The name of the socket to modify.
            transform: The new local transform for the socket.

| arg | type | req | description |
|---|---|---|---|
| `mesh` | `ref</Script/Engine.SkeletalMesh>` | yes | Represents a reference to a UObject or UClass. |
| `socket_name` | `string` | yes |  |
| `transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` | yes | Represents a 3D transformation with optional location, rotation, and scale. Unset fields mean "identity" when creating objects and "don't change" when modifying existing ones. |
