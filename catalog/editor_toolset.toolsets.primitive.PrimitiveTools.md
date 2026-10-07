# editor_toolset.toolsets.primitive.PrimitiveTools

Provides tools for adding primitive geometry components to actors.

4 tools.

### `add_cone`

Adds a cone-shaped StaticMeshComponent to an actor.

        Args:
            actor: The actor to add the component to.
            name: The name of the new component.
            radius: The radius of the cone base.
            height: The height of the cone.
            local_transform: The transform of the component relative to the actor.

        Returns:
            The new StaticMeshComponent.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `radius` | `number` |  |  (default `50`) |
| `height` | `number` |  |  (default `100`) |
| `local_transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` |  | Represents a 3D transformation with optional location, rotation, and scale. Unset fields mean "identity" when creating objects and "don't change" when modifying existing ones. (default `null`) |

Returns: `ref</Script/Engine.StaticMeshComponent>`

### `add_cube`

Adds a cube-shaped StaticMeshComponent to an actor.

        Args:
            actor: The actor to add the component to.
            name: The name of the new component.
            dimensions: The x, y, and z size of the cube.
            local_transform: The transform of the component relative to the actor.

        Returns:
            The new StaticMeshComponent.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `dimensions` | `Vector{x:number, y:number, z:number}` |  |  (default `{"x": 100, "y": 100, "z": 100}`) |
| `local_transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` |  | Represents a 3D transformation with optional location, rotation, and scale. Unset fields mean "identity" when creating objects and "don't change" when modifying existing ones. (default `null`) |

Returns: `ref</Script/Engine.StaticMeshComponent>`

### `add_cylinder`

Adds a cylinder-shaped StaticMeshComponent to an actor.

        Args:
            actor: The actor to add the component to.
            name: The name of the new component.
            radius: The radius of the cylinder.
            height: The height of the cylinder.
            local_transform: The transform of the component relative to the actor.

        Returns:
            The new StaticMeshComponent.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `radius` | `number` |  |  (default `50`) |
| `height` | `number` |  |  (default `100`) |
| `local_transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` |  | Represents a 3D transformation with optional location, rotation, and scale. Unset fields mean "identity" when creating objects and "don't change" when modifying existing ones. (default `null`) |

Returns: `ref</Script/Engine.StaticMeshComponent>`

### `add_sphere`

Adds a sphere-shaped StaticMeshComponent to an actor.

        Args:
            actor: The actor to add the component to.
            name: The name of the new component.
            radius: The radius of the sphere.
            local_transform: The transform of the component relative to the actor.

        Returns:
            The new StaticMeshComponent.

| arg | type | req | description |
|---|---|---|---|
| `actor` | `ref</Script/Engine.Actor>` | yes | Represents a reference to a UObject or UClass. |
| `name` | `string` | yes |  |
| `radius` | `number` |  |  (default `50`) |
| `local_transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` |  | Represents a 3D transformation with optional location, rotation, and scale. Unset fields mean "identity" when creating objects and "don't change" when modifying existing ones. (default `null`) |

Returns: `ref</Script/Engine.StaticMeshComponent>`
