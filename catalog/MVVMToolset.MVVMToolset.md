# MVVMToolset.MVVMToolset

Toolset for authoring ModelViewViewModel (MVVM) data on UMG Widget Blueprints.

The Model-View-ViewModel pattern decouples a UMG widget's presentation (the View)
from the data and logic that drives it (the ViewModel). Bindings wire individual
widget properties to ViewModel properties so the UI reflects state changes
automatically, optionally routing values through conversion functions when the
source and destination types differ, and event bindings forward widget events
(multicast delegates) onto the ViewModel.

This toolset exposes an API to configure WidgetBlueprint's MVVM data:
  - Author ViewModel Blueprints derived from UMVVMViewModelBase and add
    typed properties to them.
  - Discover ViewModels on disk, attach them to a WidgetBlueprint, and list
    the ones currently registered on a widget.
  - Create, list, and remove property-to-property view bindings between
    widgets, ViewModels, and the WidgetBlueprint itself, optionally selecting
    a conversion function when types don't match.
  - Create event bindings from widget multicast delegates to ViewModel
    handlers, and enumerate the events available to bind.
  - Repair MVVM state on a WidgetBlueprint by regenerating its binding graphs
    to match the stored binding data.

15 tools.

### `AddViewModelProperty`

Add a property to an existing ViewModel

| arg | type | req | description |
|---|---|---|---|
| `viewModel` | `ref</Script/Engine.Blueprint>` | yes | ViewModel asset to use. |
| `propertyName` | `string` | yes | Desired name of the new property |
| `propertyType` | `string` | yes | Desired type of the new property. Corresponds with PinType |
| `defaultValue` | `string` | yes | If a default property is desired, string representation of the value |

Returns: `boolean`

### `AddViewModelToWidget`

Adds a ViewModel to the WidgetBlueprint

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |
| `viewModelClass` | `ref<Class@/Script/CoreUObject.Object>` | yes | ViewModel class to use. |

### `CreateViewBinding`

Creates a View Binding from the SourceProperty to the Destination property.
If there is a type mismatch, an existing conversion function will try to be used.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |
| `sourceContext` | `ref</Script/CoreUObject.Object>` | yes | Source object that contains the source property. Can be the following: - UWidget: source property is from a widget in the widget blueprint's widgettree - UClass: source property is from a widget blueprint's ViewModel - Null: source property is from the widget blueprint |
| `sourcePropertyPath` | `string` | yes | Property to read data from. Contains a dot '.' separated path to the reflected property (path.SubField). Case-sensitive |
| `destinationContext` | `ref</Script/CoreUObject.Object>` | yes | Destination object that contains the destination property. Can be the following: - UWidget: destination property is from a widget in the widget blueprint's widgettree - UClass: destination property is from a widget blueprint's ViewModel - Null: destination property is from the widget blueprint |
| `destinationPropertyPath` | `string` | yes | Property to write data to. Contains a dot '.' separated path to the field (path.subfield) |
| `conversionName` | `string` | yes | Optional parameter, name of a conversion function to use if needed. If none is provided, this will be inferred. See ListConversionFunctions |

Returns: `string`

### `CreateViewEventBinding`

Creates a View Event Binding from the EventProperty to the Destination property.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |
| `eventContext` | `ref</Script/CoreUObject.Object>` | yes | Event object that contains the source property. Can be the following: - UWidget: source property is from a widget in the widget blueprint's widgettree - UClass: source property is from a widget blueprint's ViewModel - Null: source property is from the widget blueprint |
| `eventPropertyPath` | `string` | yes | Event property to listen to. Contains a dot '.' separated path to the reflected property (path.SubField). Case-sensitive |
| `destinationContext` | `ref</Script/CoreUObject.Object>` | yes | Destination object that contains the destination property. Can be the following: - UWidget: destination property is from a widget in the widget blueprint's widgettree - UClass: destination property is from a widget blueprint's ViewModel - Null: destination property is from the widget blueprint |
| `destinationPropertyPath` | `string` | yes | Property modify when event is triggered. Contains a dot '.' separated path to the field (path.subfield) |

Returns: `ref</Script/ModelViewViewModelBlueprint.MVVMBlueprintViewEvent>`

### `FixupMVVMData`

Attempts to fixup MVVM data. This function can be called if the MVVM Generated Blueprint graphs like conversion functions report compilation errors.
It regenerates the graphs to ensure parity with view binding data.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to fixup |

### `GetWidgetViewConfig`

Returns the MVVM View configuration.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to read configuration from. |
| `outConfiguration` | `MVVMViewConfig{bInitializeSourcesOnConstruct:boolean, bInitializeBindingsOnConstruct:boolean, bInitializeEventsOnConstruct:boolean, bCreateViewWithoutBindings:boolean}` | yes | Filled with the current view configuration on success. Untouched on failure. |

Returns: `boolean`

### `ListBindableWidgetProperties`

Lists the bindable property paths available on a widget (binding source/destination candidates).
Names aren't filtered by direction -- a read-only property can't be used as a destination and a
write-only one can't be used as a source; CreateViewBinding reports that mismatch if it's tried.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint the widget belongs to |
| `widget` | `ref</Script/UMG.Widget>` | yes | Widget to enumerate bindable properties on |

Returns: `[string]`

### `ListConversionFunctions`

List Available Conversion functions for a WidgetBlueprint that bind a Source Property to a Destination Property

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |

Returns: `[MVVMViewConversionFunctionDescription{conversionFunction:ref</Script/CoreUObject.Function>, conversionNode:ref<Class@/Script/BlueprintGraph.K2Node>}]`

### `ListViewModels`

List all ViewModel under the search path

| arg | type | req | description |
|---|---|---|---|
| `searchPath` | `string` | yes | Mount point search path for ViewModel assets |

Returns: `[ref<Class@/Script/CoreUObject.Object>]`

### `ListWidgetViewBindings`

List all view bindings on the WidgetBlueprint

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |

Returns: `[MVVMBlueprintViewBinding]`

### `ListWidgetViewEvents`

List Available Event Properties for a WidgetBlueprint (i.e. a Multicast Delegate)

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |

Returns: `[string]`

### `ListWidgetViewModels`

List all ViewModel on the WidgetBlueprint

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |

Returns: `[ref<Class@/Script/CoreUObject.Object>]`

### `RemoveWidgetViewBinding`

Removes View Binding on the WidgetBlueprint

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |
| `bindingId` | `string` | yes | Globally unique identifier in 8-4-4-4-12 hyphenated form, e.g. "E05FCC13-4D37-9D7A-E238-83859F29AD74". |

Returns: `boolean`

### `SetBindingMode`

Sets the binding mode (OneTimeToDestination/OneWayToDestination/TwoWay/OneWayToSource) for an existing view binding.
Not supported during PIE.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to use |
| `bindingId` | `string` | yes | The guid of the binding to change |
| `mode` | `OneTimeToDestination or OneWayToDestination or TwoWay or OneTimeToSource or OneWayToSource` | yes | New binding mode to apply |

Returns: `boolean`

### `SetWidgetViewConfig`

Writes the MVVM View configuration on the WidgetBlueprint's View.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | WidgetBlueprint to write configuration to. |
| `configuration` | `MVVMViewConfig{bInitializeSourcesOnConstruct:boolean, bInitializeBindingsOnConstruct:boolean, bInitializeEventsOnConstruct:boolean, bCreateViewWithoutBindings:boolean}` | yes | New view configuration. |

Returns: `boolean`
