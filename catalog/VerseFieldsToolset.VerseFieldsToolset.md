# VerseFieldsToolset.VerseFieldsToolset

Authors Verse fields on a Widget Blueprint and binds widget properties to them via MVVM. Covers
listing, adding, editing, removing, and duplicating fields, plus creating the view binding that
drives a widget property from a field's value.

7 tools.

### `AddVerseField`

Adds a new Verse field (variable) to a Widget Blueprint. The field becomes bindable (FieldNotify) and
is reflected into the widget's generated Verse class. Recompiles the blueprint. Not supported during PIE.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Target widget blueprint. |
| `fieldName` | `string` | yes | Name of the new field. Must be a valid identifier and unique on the blueprint. |
| `spec` | `VerseFieldSpec` | yes | Describes the field to add (type, optional event parameters, default, access, mutability). |

Returns: `boolean`

### `BindWidgetPropertyToVerseField`

Binds a widget property to a Verse field on the same Widget Blueprint (the field is the MVVM SelfContext
source). Creates the view binding and applies the requested mode; recompiles. Not supported during PIE.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Target widget blueprint (must already contain VerseFieldName). |
| `verseFieldName` | `string` | yes | Existing Verse field to read from. |
| `targetWidget` | `ref</Script/UMG.Widget>` | yes | Widget in the tree whose property is written. |
| `widgetPropertyPath` | `string` | yes | Dot-path to the destination property (e.g. "RenderOpacity", "ColorAndOpacity.SpecifiedColor"). Case-sensitive. |
| `mode` | `OneTimeToDestination or OneWayToDestination or TwoWay or OneTimeToSource or OneWayToSource` |  | Binding mode (default OneWayToDestination = Verse field drives the widget; TwoWay for editable write-back). (default `"OneWayToDestination"`) |
| `conversionName` | `string` |  | Optional conversion function name for type mismatches (None = auto). (default `"None"`) |

Returns: `string`

### `DuplicateVerseField`

Duplicates a Verse field under a new name. Recompiles. Not supported during PIE.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Target widget blueprint. |
| `fieldName` | `string` | yes | Name of the existing field to duplicate. |
| `newName` | `string` | yes | Name for the duplicated field. Required: must be non-empty and not already in use on the blueprint. The duplicate is named exactly this; an empty or colliding name fails with a script error. |

Returns: `boolean`

### `EditVerseField`

Edits an existing Verse field (retype/default/access/mutability). Recompiles. Not supported during PIE.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Target widget blueprint. |
| `fieldName` | `string` | yes | Name of the existing field to edit. |
| `spec` | `VerseFieldSpec` | yes | Describes the field's new state (type, optional event parameters, default, access, mutability). |
| `newName` | `string` | yes | When non-empty, renames the field to this name. |

Returns: `boolean`

### `GetSupportedVerseFieldTypes`

Accepted Spec.Type / Spec.EventParameterTypes values. Query this instead of assuming a fixed
list -- it reads from the same place the validation does.

Returns: `VerseFieldSupportedTypes{fieldTypes:[string], eventParameterTypes:[string]}`

### `ListVerseFields`

Lists the Verse-authored fields on a Widget Blueprint.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to inspect. |

Returns: `[VerseFieldInfo]`

### `RemoveVerseField`

Removes a Verse field by name. Recompiles. Not supported during PIE.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Target widget blueprint. |
| `fieldName` | `string` | yes | Name of the field to remove. |

Returns: `boolean`
