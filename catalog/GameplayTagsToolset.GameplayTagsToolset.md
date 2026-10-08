# GameplayTagsToolset.GameplayTagsToolset

Provides tools for reading and managing gameplay tags in INI tag source files via the project's GameplayTagsManager.

4 tools.

### `FindReferencersByTag`

Returns assets that reference a gameplay tag.

| arg | type | req | description |
|---|---|---|---|
| `tagName` | `string` | yes | The fully-qualified gameplay tag to search for, e.g. "Character.State.Dead". |

Returns: `[string]`

### `GetTagInfo`

Returns detailed information about a specific gameplay tag.

| arg | type | req | description |
|---|---|---|---|
| `tagName` | `string` | yes | The fully-qualified name of the tag, e.g. "Character.State.Dead". |

Returns: `GameplayTagInfo{comment:string, source:string, children:[string]}`

### `ListTags`

Returns gameplay tags registered in the project.

| arg | type | req | description |
|---|---|---|---|
| `parentTag` | `string` | yes | If non-empty, only tags that are descendants of this tag are returned. For example, passing "Character.State" returns "Character.State.Dead", "Character.State.Stunned", etc. Pass an empty string to return all tags. |

Returns: `[string]`

### `ListTagsInSource`

Returns all gameplay tags defined in a specific tag source.

| arg | type | req | description |
|---|---|---|---|
| `tagSource` | `string` | yes | The INI source file name to list tags from, e.g. "MyPluginGameplayTags.ini". |

Returns: `[string]`
