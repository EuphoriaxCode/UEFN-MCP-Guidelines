# editor_toolset.toolsets.actor.ActorTools

Provides tools for inspecting and modifying actors, including
    their transforms, labels, parent-child relationships, and components.

18 tools.

### `add_component`

Adds a component to an actor instance or blueprint.

        Args:
            owner: The actor blueprint, instance, or SceneComponent to add to.
            component_type: The type of component to add.
            name: The name of the new component.

        Returns:
            The newly added actor component.

| arg | type | req | description |
|---|---|---|---|
| `owner` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |
| `component_type` | `ref</Script/CoreUObject.Class>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |

Returns: `ref</Script/Engine.ActorComponent>`

### `add_tag`

Adds a tag to an actor.

        Args:
            actor: The actor to modify.
            tag: The tag to add.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `tag` | `string` | yes |  |

### `diff`

Returns a unified text diff between two actors.

        Compares the actors' classes, top-level properties, and per-component
        class and top-level properties.

        Args:
            old_actor: The actor whose state is the old side of the diff.
            new_actor: The actor whose state is the new side of the diff.

        Returns:
            A difflib unified-diff string. Empty when the actors are identical.

| arg | type | req | description |
|---|---|---|---|
| `old_actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `new_actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `string`

### `get_actor_bounds`

Returns the bounding box of an actor.

        Args:
            actor: The actor to query.

        Returns:
            The world space bounding box for the actor.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `Box{min:Vector{x:number, y:number, z:number}, max:Vector{x:number, y:number, z:number}, isValid:boolean}`

### `get_actor_transform`

Returns the position, rotation, and scale of an actor.

        Args:
            actor: The actor to query.

        Returns:
            The world space actor transform.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}`

### `get_component_actor`

Returns the actor that owns the specified component.

        Args:
            component: The component to query.

        Returns:
            The actor that owns this component.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Engine.ActorComponent>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ref</Script/Engine.Actor>`

### `get_components`

Returns the components that an actor contains.

        Args:
            actor: The actor to query.
            component_type: If set, will only return components of this type.

        Returns:
            The components in the actor.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `component_type` | `ref</Script/CoreUObject.Class>` |  | Represents a reference to a UObject or UClass. (default `null`) |

Returns: `[ref</Script/Engine.ActorComponent>]`

### `get_label`

Returns the actor's human friendly name as it appears in the editor.

        Args:
            actor: The actor to query.

        Returns:
            The label for the actor.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `string`

### `get_parent_component`

Returns the parent component that this component is attached to, if any.

        Args:
            component: The scene component to query.

        Returns:
            The parent SceneComponent if attached to one, otherwise None.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Engine.SceneComponent>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ref</Script/Engine.SceneComponent>`

### `get_root_component`

Returns the root component of an actor, if any.

        Args:
            actor: The actor to query.

        Returns:
            The actor's root SceneComponent, or None if it has no root component.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `ref</Script/Engine.SceneComponent>`

### `get_tags`

Returns the list of tags on an actor.

        Args:
            actor: The actor to query.

        Returns:
            The tags on the actor as strings.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[string]`

### `has_tag`

Returns whether an actor has a specific tag.

        Args:
            actor: The actor to query.
            tag: The tag to check for.

        Returns:
            True if the actor has the tag, False otherwise.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `tag` | `string` | yes |  |

Returns: `boolean`

### `look_at`

Rotates an actor so its forward vector points at a world-space position.

        Args:
            actor: The actor to rotate.
            target: The world-space position to face.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `target` | `Vector{x:number, y:number, z:number}` | yes |  |

### `remove_component`

Removes a component from an actor instance or blueprint.

        Args:
            component: The component to remove.

        Returns:
            True if the component was successfully removed.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Engine.ActorComponent>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `remove_tag`

Removes a tag from an actor.

        Args:
            actor: The actor to modify.
            tag: The tag to remove.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `tag` | `string` | yes |  |

### `set_actor_transform`

Updates the position, rotation, and/or scale of an actor.

        Args:
            actor: The actor to modify.
            xform: The new transform to apply to this actor.
            worldspace: True means xform is in worldpace. False means relative to parent.
                Has no effect on actors in blueprints, which only have a default
                relative transform.

        Returns:
            True if an id matching the actor was found and it's position was set.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `xform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` | yes | Represents a 3D transformation with optional location, rotation, and scale. Unset fields mean "identity" when creating objects and "don't change" when modifying existing ones. |
| `worldspace` | `boolean` |  |  (default `true`) |

Returns: `boolean`

### `set_label`

Sets the human-friendly name of the actor.

        Args:
            actor: The actor to modify.
            label: The new name for the actor.

        Returns:
            True if the label was updated correctly.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `label` | `string` | yes |  |

Returns: `boolean`

### `set_parent_component`

Sets the parent for the specified scene component.

        For blueprint actors, passing a component as the parent of the root promotes it
        to the scene root, making the current root a child of it. If the current root is a
        DefaultSceneRoot, Unreal will automatically remove it.

        Args:
            component: The scene component to modify.
            parent: The new parent component. None will detach the component from its current parent.

        Returns:
            True if the reparent succeeded.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Engine.SceneComponent>` | yes | Represents a reference to a UObject or UClass. |
| `parent` | `ref</Script/Engine.SceneComponent>` |  | Represents a reference to a UObject or UClass. (default `null`) |

Returns: `boolean`
