# PhysicsToolsets.PhysicsAssetToolset

Provides tools for creating and managing Physics Assets.

17 tools.

### `AddBody`

Adds a new empty body for the given bone.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `boneName` | `string` | yes | The name of the bone to add a body for. |

### `AddConstraint`

Adds a new constraint between two bodies. Both bodies must already exist.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `bone1Name` | `string` | yes | Name of the child bone. |
| `bone2Name` | `string` | yes | Name of the parent bone. |

### `CreateFromMesh`

Creates a physics asset from a skeletal mesh, auto-generating collision bodies for
each bone. The asset is placed in the same folder as the mesh with the suffix
"_PhysicsAsset".

| arg | type | req | description |
|---|---|---|---|
| `meshPath` | `string` | yes | Content-browser path to the skeletal mesh, e.g. '/Game/Characters/SKM_Hero'. |
| `bAssignToMesh` | `boolean` | yes | If true, assigns the new physics asset to the mesh. |

Returns: `ref</Script/Engine.PhysicsAsset>`

### `GetBodyMassScale`

Returns the mass-scale multiplier for the given body.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to query. |
| `boneName` | `string` | yes | The name of the bone whose body to query. |

Returns: `number`

### `GetBodyNames`

Returns the bone name for each rigid body in a physics asset.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to query. |

Returns: `[string]`

### `GetBodyPhysicsMode`

Returns the physics simulation mode for the given body.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to query. |
| `boneName` | `string` | yes | The name of the bone whose body to query. |

Returns: `Default or Kinematic or Simulated`

### `GetBodyShapes`

Returns all collision shapes assigned to a body.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to query. |
| `boneName` | `string` | yes | The name of the bone whose body shapes to retrieve. |

Returns: `[PhysicsShapeInfo]`

### `GetConstraints`

Returns all constraints in the physics asset with their current angular limits.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to query. |

Returns: `[PhysicsConstraintInfo]`

### `RemoveBody`

Removes the body for the given bone along with any constraints that reference it.
Raises a script error if PhysicsAsset is null or no body exists for BoneName.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `boneName` | `string` | yes | The name of the bone whose body to remove. |

### `RemoveConstraint`

Removes the constraint between two bodies.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `bone1Name` | `string` | yes | Name of the child bone. |
| `bone2Name` | `string` | yes | Name of the parent bone. |

### `RemoveShape`

Removes a collision primitive from a body by name.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `boneName` | `string` | yes | The name of the bone whose body to modify. |
| `shapeName` | `string` | yes | The name of the shape to remove. |

### `SetBodyMassScale`

Sets the mass-scale multiplier for the given body.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `boneName` | `string` | yes | The name of the bone whose body to modify. |
| `massScale` | `number` | yes | Multiplier applied to the computed mass. Must be greater than zero. |

### `SetBodyPhysicsMode`

Sets the physics simulation mode for the given body.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `boneName` | `string` | yes | The name of the bone whose body to modify. |
| `mode` | `Default or Kinematic or Simulated` | yes | The desired simulation mode. |

### `SetBox`

Adds or replaces a box collision primitive on a body.
If any shape with the given name already exists on the body it is removed first.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `boneName` | `string` | yes | The name of the bone whose body to modify. |
| `shapeName` | `string` | yes | A name that uniquely identifies this shape on the body. |
| `center` | `Vector{x:number, y:number, z:number}` | yes | Center of the box in bone-local space (cm). |
| `rotation` | `Rotator{pitch:number, yaw:number, roll:number}` | yes | Orientation of the box in bone-local space. |
| `extentX` | `number` | yes | Full extent along local X (cm). Must be greater than zero. |
| `extentY` | `number` | yes | Full extent along local Y (cm). Must be greater than zero. |
| `extentZ` | `number` | yes | Full extent along local Z (cm). Must be greater than zero. |

### `SetCapsule`

Adds or replaces a capsule collision primitive on a body.
If any shape with the given name already exists on the body it is removed first.
The capsule's long axis is its local Z after applying Rotation.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `boneName` | `string` | yes | The name of the bone whose body to modify. |
| `shapeName` | `string` | yes | A name that uniquely identifies this shape on the body. |
| `center` | `Vector{x:number, y:number, z:number}` | yes | Center of the capsule in bone-local space (cm). |
| `rotation` | `Rotator{pitch:number, yaw:number, roll:number}` | yes | Orientation of the capsule in bone-local space. |
| `radius` | `number` | yes | Radius of the capsule end-caps (cm). Must be greater than zero. |
| `length` | `number` | yes | Length of the cylindrical section (cm). Must be non-negative. Total capsule height = Length + 2 * Radius. |

### `SetConstraintLimits`

Updates the angular limits for an existing constraint.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `info` | `PhysicsConstraintInfo` | yes | Constraint descriptor. Bone1Name and Bone2Name identify the constraint. |

### `SetSphere`

Adds or replaces a sphere collision primitive on a body.
If any shape with the given name already exists on the body it is removed first.

| arg | type | req | description |
|---|---|---|---|
| `physicsAsset` | `ref</Script/Engine.PhysicsAsset>` | yes | The physics asset to modify. |
| `boneName` | `string` | yes | The name of the bone whose body to modify. |
| `shapeName` | `string` | yes | A name that uniquely identifies this shape on the body. |
| `center` | `Vector{x:number, y:number, z:number}` | yes | Center of the sphere in bone-local space (cm). |
| `radius` | `number` | yes | Radius of the sphere (cm). Must be greater than zero. |
