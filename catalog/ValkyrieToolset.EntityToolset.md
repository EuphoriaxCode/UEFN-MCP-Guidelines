# ValkyrieToolset.EntityToolset

Inspects, navigates, and edits the Verse Scene Graph (verse::entity / verse::component
hierarchies) in the current editor level: listing entities and their components and the
classes available to instantiate, creating and deleting entities, attaching and removing
components, reading and writing component properties by their friendly Verse name, and
getting/setting an entity's world transform.

13 tools.

### `AddComponent`

Attach a component to a Verse entity.

| arg | type | req | description |
|---|---|---|---|
| `entity` | `ref</Script/Entity.BaseEntity>` | yes | The target entity. |
| `componentClass` | `ref<Class@/Script/Entity.BaseComponent>` | yes | The component class to attach (a verse::component subclass). |

Returns: `EntityComponentInfo{component:ref</Script/Entity.BaseComponent>, componentName:string, componentClass:ref<Class@/Script/Entity.BaseComponent>}`

### `CreateEntity`

Create a Verse entity in the current editor scene.

| arg | type | req | description |
|---|---|---|---|
| `entityClass` | `ref<Class@/Script/Entity.BaseEntity>` | yes | The entity class to instantiate (a verse::entity subclass). |
| `transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` | yes | World transform for the new entity (a transform component is added for it). |
| `name` | `string` |  | Desired entity name; empty auto-generates one. (default `""`) |
| `parentEntity` | `ref</Script/Entity.BaseEntity>` |  | The entity to create under; omit to create at the persistent level's root. (default `null`) |

Returns: `EntityInfo{entity:ref</Script/Entity.BaseEntity>, displayName:string, entityClass:ref<Class@/Script/Entity.BaseEntity>}`

### `DeleteEntity`

Delete a Verse entity from the current editor scene. Also destroys its child entities and components.

| arg | type | req | description |
|---|---|---|---|
| `entity` | `ref</Script/Entity.BaseEntity>` | yes | The target entity. The level root cannot be deleted. |

### `FindEntities`

Find Verse entities in the current editor scene, optionally scoped and filtered.

| arg | type | req | description |
|---|---|---|---|
| `rootEntity` | `ref</Script/Entity.BaseEntity>` |  | An entity to list under; omit to list from the root of every loaded level. (default `null`) |
| `bRecursive` | `boolean` |  | Whole subtree when true; immediate children when false. (default `true`) |
| `nameFilter` | `string` |  | Case-insensitive substring matched against each entity's friendly name; empty matches all. (default `""`) |

Returns: `[EntityInfo{entity:ref</Script/Entity.BaseEntity>, displayName:string, entityClass:ref<Class@/Script/Entity.BaseEntity>}]`

### `GetComponentProperty`

Read a component's editable property value, by its friendly Verse name.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Entity.BaseComponent>` | yes | The target component. |
| `propertyName` | `string` | yes | The property's friendly Verse name. |

Returns: `string`

### `GetComponents`

List the components attached to a Verse entity.

| arg | type | req | description |
|---|---|---|---|
| `entity` | `ref</Script/Entity.BaseEntity>` | yes | The target entity. |

Returns: `[EntityComponentInfo{component:ref</Script/Entity.BaseComponent>, componentName:string, componentClass:ref<Class@/Script/Entity.BaseComponent>}]`

### `GetEntityTransform`

Get a Verse entity's world transform.

| arg | type | req | description |
|---|---|---|---|
| `entity` | `ref</Script/Entity.BaseEntity>` | yes | The target entity. An entity with no transform component reports its parent's world transform. |

Returns: `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}`

### `ListComponentClasses`

List the concrete Verse component classes that can be attached (verse::component subclasses),
optionally filtered. Covers loaded classes (including a just-built, unsaved Verse class) and
unloaded prefab classes.

| arg | type | req | description |
|---|---|---|---|
| `nameFilter` | `string` |  | Case-insensitive substring matched against each class's friendly name; empty matches all. (default `""`) |

Returns: `[EntityClassInfo{classPath:ref<Class@/Script/CoreUObject.Object>, className:string, bIsPrefab:boolean}]`

### `ListComponentProperties`

List a Verse component's editable properties.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Entity.BaseComponent>` | yes | The target component. |

Returns: `[EntityPropertyInfo{name:string, type:string, value:string, bReadOnly:boolean}]`

### `ListEntityClasses`

List the concrete Verse entity classes that can be instantiated (verse::entity subclasses),
optionally filtered. Covers loaded classes (including a just-built, unsaved Verse class) and
unloaded prefab classes.

| arg | type | req | description |
|---|---|---|---|
| `nameFilter` | `string` |  | Case-insensitive substring matched against each class's friendly name; empty matches all. (default `""`) |

Returns: `[EntityClassInfo{classPath:ref<Class@/Script/CoreUObject.Object>, className:string, bIsPrefab:boolean}]`

### `RemoveComponent`

Remove a component from a Verse entity.

| arg | type | req | description |
|---|---|---|---|
| `entity` | `ref</Script/Entity.BaseEntity>` | yes | The target entity. |
| `componentClass` | `ref<Class@/Script/Entity.BaseComponent>` | yes | The component class to remove (a verse::component subclass). |

### `SetComponentProperty`

Write one property on a component, by its friendly Verse name.

| arg | type | req | description |
|---|---|---|---|
| `component` | `ref</Script/Entity.BaseComponent>` | yes | The target component. |
| `propertyName` | `string` | yes | The property's friendly Verse name. |
| `value` | `string` | yes | The new value, JSON-encoded — e.g. 5, true, "text", {"X":1,"Y":2,"Z":3}. |

### `SetEntityTransform`

Set a Verse entity's world transform (adds a transform component if it has none).

| arg | type | req | description |
|---|---|---|---|
| `entity` | `ref</Script/Entity.BaseEntity>` | yes | The target entity. |
| `transform` | `ToolsetTransform{location:Vector{x:number, y:number, z:number}, rotation:Rotator{pitch:number, yaw:number, roll:number}, scale:Vector{x:number, y:number, z:number}}` | yes | The new world-space transform. |
