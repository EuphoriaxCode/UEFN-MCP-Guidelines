# editor_toolset.toolsets.scene.SceneTools

Provides tools for working with the currently loaded level, including
    loading levels, placing, replacing, and removing actors, controlling the level camera,
    organizing and hiding actors in the outliner, looking up an OFPA actor's asset path,
    and managing the world's data layers.

28 tools.

### `add_actors_to_data_layer`

Adds actors to a data layer, creating its instance in the current world if
        it has none yet. Actors already in the layer are left unchanged.

        Args:
            actors: The actors to add.
            asset_path: The content path of the data layer asset (e.g. '/Game/DataLayers/Audio').

| arg | type | req | description |
|---|---|---|---|
| `actors` | `[ref</Script/Engine.Actor>]` | yes |  |
| `asset_path` | `string` | yes |  |

### `add_to_scene_from_asset`

Creates a new actor in the scene from an asset.

        Args:
            asset_path: The path to the asset to spawn (e.g. '/Game/Blueprints/MyActor').
            name: The name of the actor instance.
            xform: The transform for the new actor. Parent-local when `parent` is set;
                world-space otherwise.
            parent: If set, the new actor will be a child of this actor. If unset the Actor will
                be a child of the world.
            snap_to_ground: If set to true, will attempt to adjust the actors Z position so that
                the bottom of its bounding box is on the ground.

        Returns:
            The created actor or nothing if creation was unsuccessful.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |
| `name` | `string` | yes |  |
| `xform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` | yes | Represents a 3D transformation with optional location, rotation, and scale. Unset fields mean "identity" when creating objects and "don't change" when modifying existing ones. |
| `parent` | `ref</Script/Engine.Actor>` |  | Represents a reference to a UObject or UClass. (default `null`) |
| `snap_to_ground` | `boolean` |  |  (default `false`) |

Returns: `ref</Script/Engine.Actor>`

### `add_to_scene_from_class`

Creates a new instance of the specified object at the specified transform.

        Args:
            actor_type: The Actor class to instantiate.
            name: The name of the actor instance.
            xform: The transform for the new actor. Parent-local when `parent` is set;
                world-space otherwise.
            parent: If set, the new actor will be a child of this actor. If unset the Actor will
                be a child of the world.
            snap_to_ground: If set to true, will attempt to adjust the actors Z position so that
                the bottom of its bounding box is on the ground.

        Returns:
            The created actor or nothing if creation was unsuccessful.

| arg | type | req | description |
|---|---|---|---|
| `actor_type` | `ref</Script/CoreUObject.Class>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `xform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` | yes | Represents a 3D transformation with optional location, rotation, and scale. Unset fields mean "identity" when creating objects and "don't change" when modifying existing ones. |
| `parent` | `ref</Script/Engine.Actor>` |  | Represents a reference to a UObject or UClass. (default `null`) |
| `snap_to_ground` | `boolean` |  |  (default `false`) |

Returns: `ref</Script/Engine.Actor>`

### `create_data_layer_asset`

Creates a new Data Layer asset in the content browser.

        A Data Layer asset is reusable across levels; assign it to actors in the
        current world with add_actors_to_data_layer.

        Args:
            asset_path: The content path for the new asset (e.g. '/Game/DataLayers/Audio').
            is_runtime: If True, the layer affects runtime streaming (its actors can be
                loaded and unloaded during play). If False, it is editor-only.

        Returns:
            The created Data Layer asset.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |
| `is_runtime` | `boolean` |  |  (default `true`) |

Returns: `ref</Script/Engine.DataLayerAsset>`

### `create_level`

Creates a new empty level asset and opens it in the editor.

        Args:
            level_path: The content path for the new level asset
                (e.g. '/Game/Maps/MyLevel').
            world_partition: If True, the new level is a partitioned (World
                Partition) world. If False, a regular non-partitioned level.

| arg | type | req | description |
|---|---|---|---|
| `level_path` | `string` | yes |  |
| `world_partition` | `boolean` |  |  (default `false`) |

### `delete_folder`

Deletes a folder from the outliner.

        Actors directly in the folder are moved to the parent folder. Sub-folders and
        their actors are preserved by re-rooting them under the parent. For example,
        deleting 'Lighting' with a sub-folder 'Lighting/Spotlights' leaves 'Spotlights'
        intact under the parent.

        Args:
            folder_path: The folder path to delete (e.g. 'Lighting/Spotlights').

        Returns:
            The number of actors that were moved.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |

Returns: `integer`

### `diff`

Returns a unified text diff between two scene asset packages.

        Args:
            old_scene_path: Content path to the old scene asset.
            new_scene_path: Content path to the new scene asset.

        Returns:
            A difflib unified-diff string. Empty when the scenes are identical.

| arg | type | req | description |
|---|---|---|---|
| `old_scene_path` | `string` | yes |  |
| `new_scene_path` | `string` | yes |  |

Returns: `string`

### `find_actors`

Searches the scene for actors that match specific criteria.

        Args:
            root: If set, will only search this actor and its children. Restricts
                the search to loaded actors.
            name: If set, will only return actors whose label contains this string
                (case-insensitive).
            actor_type: If set, will only return actors that are of this type.
            tag: If set, will only return actors that have this tag. Restricts the
                search to loaded actors.
            bounds: If set, only returns actors whose bounds overlap this world-space AABB.
            collision_channels: If set, bounds checks will use a native physics overlap query
                restricted to these channels. Restricts the search to loaded actors.
            data_layer: If set, only returns actors assigned to the data layer asset
                at this content path (e.g. '/Game/DataLayers/Audio').

        Returns:
            The actor descriptors that match the criteria.

| arg | type | req | description |
|---|---|---|---|
| `root` | `ref</Script/Engine.Actor>` |  | Represents a reference to a UObject or UClass. (default `null`) |
| `name` | `string` |  |  (default `""`) |
| `actor_type` | `ref</Script/CoreUObject.Class>` |  | Represents a reference to a UObject or UClass. (default `null`) |
| `tag` | `string` |  |  (default `""`) |
| `bounds` | `Box{min:Vector{x:number, y:number, z:number}, max:Vector{x:number, y:number, z:number}, isValid:boolean}` |  |  (default `null`) |
| `collision_channels` | `[ObjectTypeQuery1 or ObjectTypeQuery2 or ObjectTypeQuery3 or ObjectTypeQuery4 or ObjectTypeQuery5 or ObjectTypeQuery6 or ObjectTypeQuery7 or ObjectTypeQuery8 or ObjectTypeQuery9 or ObjectTypeQuery10 or ObjectTypeQuery11 or ObjectTypeQuery12 or ObjectTypeQuery13 or ObjectTypeQuery14 or ObjectTypeQuery15 or ObjectTypeQuery16 or ObjectTypeQuery17 or ObjectTypeQuery18 or ObjectTypeQuery19 or ObjectTypeQuery20 or ObjectTypeQuery21 or ObjectTypeQuery22 or ObjectTypeQuery23 or ObjectTypeQuery24 or ObjectTypeQuery25 or ObjectTypeQuery26 or ObjectTypeQuery27 or ObjectTypeQuery28 or ObjectTypeQuery29 or ObjectTypeQuery30 or ObjectTypeQuery31 or ObjectTypeQuery32 or ObjectTypeQuery33 or ObjectTypeQuery34 or ObjectTypeQuery35 or ObjectTypeQuery36 or ObjectTypeQuery37 or ObjectTypeQuery38 or ObjectTypeQuery39 or ObjectTypeQuery40 or ObjectTypeQuery41 or ObjectTypeQuery42 or ObjectTypeQuery43 or ObjectTypeQuery44 or ObjectTypeQuery45 or ObjectTypeQuery46 or ObjectTypeQuery47 or ObjectTypeQuery48 or ObjectTypeQuery49 or ObjectTypeQuery50 or ObjectTypeQuery51 or ObjectTypeQuery52 or ObjectTypeQuery53 or ObjectTypeQuery54 or ObjectTypeQuery55 or ObjectTypeQuery56 or ObjectTypeQuery57 or ObjectTypeQuery58 or ObjectTypeQuery59 or ObjectTypeQuery60 or ObjectTypeQuery61 or ObjectTypeQuery62 or ObjectTypeQuery63 or ObjectTypeQuery64]` | yes |  |
| `data_layer` | `string` |  |  (default `""`) |

Returns: `[ActorDesc]`

### `get_actor_asset_path`

Returns the content path that identifies this actor on disk.

        Args:
            actor: The actor whose path to look up.

        Returns:
            For an actor in a One File Per Actor (OFPA) level, the full object
            path within the per-actor external package (loadable via
            unreal.load_asset). For a regular actor, the containing level's
            package path.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `string`

### `get_actors_in_data_layer`

Returns descriptors for the loaded actors assigned to a data layer.

        Args:
            asset_path: The content path of the data layer asset (e.g. '/Game/DataLayers/Audio').

        Returns:
            The descriptors of the actors in the data layer.

| arg | type | req | description |
|---|---|---|---|
| `asset_path` | `string` | yes |  |

Returns: `[ActorDesc]`

### `get_actors_in_folder`

Returns descriptors for the actors in the specified outliner folder.

        Args:
            folder_path: The folder path to query (e.g. 'Lighting/Spotlights').
            recursive: If True, also includes actors in sub-folders.

        Returns:
            The descriptors of the actors in the specified folder.

| arg | type | req | description |
|---|---|---|---|
| `folder_path` | `string` | yes |  |
| `recursive` | `boolean` |  |  (default `false`) |

Returns: `[ActorDesc]`

### `get_collision_channels`

Returns all available collision channels for use with find_actors.

        Returns:
            A list of all collision channels.

Returns: `[ObjectTypeQuery1 or ObjectTypeQuery2 or ObjectTypeQuery3 or ObjectTypeQuery4 or ObjectTypeQuery5 or ObjectTypeQuery6 or ObjectTypeQuery7 or ObjectTypeQuery8 or ObjectTypeQuery9 or ObjectTypeQuery10 or ObjectTypeQuery11 or ObjectTypeQuery12 or ObjectTypeQuery13 or ObjectTypeQuery14 or ObjectTypeQuery15 or ObjectTypeQuery16 or ObjectTypeQuery17 or ObjectTypeQuery18 or ObjectTypeQuery19 or ObjectTypeQuery20 or ObjectTypeQuery21 or ObjectTypeQuery22 or ObjectTypeQuery23 or ObjectTypeQuery24 or ObjectTypeQuery25 or ObjectTypeQuery26 or ObjectTypeQuery27 or ObjectTypeQuery28 or ObjectTypeQuery29 or ObjectTypeQuery30 or ObjectTypeQuery31 or ObjectTypeQuery32 or ObjectTypeQuery33 or ObjectTypeQuery34 or ObjectTypeQuery35 or ObjectTypeQuery36 or ObjectTypeQuery37 or ObjectTypeQuery38 or ObjectTypeQuery39 or ObjectTypeQuery40 or ObjectTypeQuery41 or ObjectTypeQuery42 or ObjectTypeQuery43 or ObjectTypeQuery44 or ObjectTypeQuery45 or ObjectTypeQuery46 or ObjectTypeQuery47 or ObjectTypeQuery48 or ObjectTypeQuery49 or ObjectTypeQuery50 or ObjectTypeQuery51 or ObjectTypeQuery52 or ObjectTypeQuery53 or ObjectTypeQuery54 or ObjectTypeQuery55 or ObjectTypeQuery56 or ObjectTypeQuery57 or ObjectTypeQuery58 or ObjectTypeQuery59 or ObjectTypeQuery60 or ObjectTypeQuery61 or ObjectTypeQuery62 or ObjectTypeQuery63 or ObjectTypeQuery64]`

### `get_current_level`

Returns the path to the current level asset.

        Returns:
            The name of the loaded level, if any.

Returns: `string`

### `get_data_layers`

Returns the data layer instances in the current world.

        Read or change a layer's state and identity through ObjectTools, e.g. its
        initial_runtime_state, is_initially_visible, is_initially_loaded_in_editor,
        and data_layer_asset properties.

        Returns:
            The data layer instances, or an empty list when the world has none.

Returns: `[ref</Script/Engine.DataLayerInstance>]`

### `get_folders`

Returns all folder paths currently in use in the outliner.

        Includes all intermediate parent paths. For example, if an actor is assigned to
        'Lighting/Spotlights', both 'Lighting' and 'Lighting/Spotlights' are returned.

        Returns:
            A sorted list of unique folder path strings.

Returns: `[string]`

### `is_actor_hidden`

Returns whether the actor is hidden in the editor viewport and outliner.

        Args:
            actor: The actor to query.

        Returns:
            True if the actor is currently hidden in the editor.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `load_actors`

Loads the actors described by the given descriptors into the editor
        and returns them.

        Args:
            actors: The actor descriptors to load.

        Returns:
            The loaded actors, in the order their descriptors were given.

| arg | type | req | description |
|---|---|---|---|
| `actors` | `[ActorDesc]` | yes |  |

Returns: `[ref</Script/Engine.Actor>]`

### `load_level`

Loads a level in the editor.

        Args:
            level_path: The path to the level asset.

| arg | type | req | description |
|---|---|---|---|
| `level_path` | `string` | yes |  |

### `remove_actors_from_data_layer`

Removes actors from a data layer. Actors not in the layer are left unchanged.

        Args:
            actors: The actors to remove.
            asset_path: The content path of the data layer asset (e.g. '/Game/DataLayers/Audio').

| arg | type | req | description |
|---|---|---|---|
| `actors` | `[ref</Script/Engine.Actor>]` | yes |  |
| `asset_path` | `string` | yes |  |

### `remove_from_scene`

Deletes an actor from the scene.

        Args:
            actor: The actor to remove.

        Returns:
            True if the actor was removed.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `rename_folder`

Renames a folder in the outliner.

        Updates the folder path for all actors in the folder and any sub-folders.
        For example, renaming 'Lighting' to 'Lights' also updates actors in
        'Lighting/Spotlights' to 'Lights/Spotlights'. If the new path already
        exists then the affected actors will be merged into it.

        Args:
            old_path: The current folder path (e.g. 'Lighting').
            new_path: The new folder path (e.g. 'Lights').

        Returns:
            The number of actors whose folder path was updated.

| arg | type | req | description |
|---|---|---|---|
| `old_path` | `string` | yes |  |
| `new_path` | `string` | yes |  |

Returns: `integer`

### `replace_actors_with_asset`

Replaces actors in the scene with new actors created from an asset (e.g. a static
        mesh, Blueprint, or particle system), matching the editor's "Replace Selected Actors
        With..." command.

        Preserves each actor's world transform, World Partition identity (actor guid and
        external package), and layers, and reattaches its former parent and children. Does
        not preserve the outliner folder path, tags, or data layer assignments.

        Args:
            actors: The actors to replace.
            asset_path: The content path of the asset to spawn from (e.g. '/Game/Meshes/Rock').
            copy_source_properties: If True and the asset is a Blueprint that shares a native
                parent with a replaced actor's class, copies over that actor's property values.

        Returns:
            The newly created actors, in the order their originals were given.

| arg | type | req | description |
|---|---|---|---|
| `actors` | `[ref</Script/Engine.Actor>]` | yes |  |
| `asset_path` | `string` | yes |  |
| `copy_source_properties` | `boolean` |  |  (default `true`) |

Returns: `[ref</Script/Engine.Actor>]`

### `replace_actors_with_class`

Replaces actors in the scene with new instances of a native Actor class, matching
        the editor's "Replace Selected Actors With..." command.

        Preserves each actor's world transform, World Partition identity (actor guid and
        external package), and layers, and reattaches its former parent and children. Does
        not preserve the outliner folder path, tags, or data layer assignments.

        Args:
            actors: The actors to replace.
            actor_type: The Actor class to create in their place. Must have a registered
                actor factory that can create instances without a source asset (e.g. lights,
                empty actors); asset-backed classes such as StaticMeshActor should use
                replace_actors_with_asset instead.

        Returns:
            The newly created actors, in the order their originals were given.

| arg | type | req | description |
|---|---|---|---|
| `actors` | `[ref</Script/Engine.Actor>]` | yes |  |
| `actor_type` | `ref</Script/CoreUObject.Class>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[ref</Script/Engine.Actor>]`

### `save_actor`

Saves the actor to disk.

        Args:
            actor: The actor to save.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

### `set_actor_folder`

Assigns an actor to the specified folder in the outliner.

        Creates the folder implicitly if it does not already exist. Pass an empty string
        to move the actor to the root of the outliner.

        Args:
            actor: The actor to move.
            folder_path: The folder path to assign (e.g. 'Lighting/Spotlights').
                         Pass an empty string to move the actor to the root.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `folder_path` | `string` | yes |  |

### `set_actor_hidden`

Shows or hides the actor in the editor viewport and outliner.

        This is the same transient, editor-only visibility toggled by the
        outliner's eye icon; it does not affect gameplay visibility and does
        not dirty the level.

        Args:
            actor: The actor to modify.
            hidden: True to hide the actor, False to unhide it.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `hidden` | `boolean` | yes |  |

### `trace_world`

Traces a line through the world and returns the distance to the first hit.

        Args:
            start: The start point of the trace in world space.
            end: The end point of the trace in world space.

        Returns:
            The distance from start to the hit point, or None if nothing was hit.

| arg | type | req | description |
|---|---|---|---|
| `start` | `Vector{x:number, y:number, z:number}` | yes |  |
| `end` | `Vector{x:number, y:number, z:number}` | yes |  |

Returns: `number`

### `unload_actors`

Unloads previously loaded World Partition actors from the editor.

        Args:
            actors: The actor descriptors to unload.

| arg | type | req | description |
|---|---|---|---|
| `actors` | `[ActorDesc]` | yes |  |
