# UMGToolSet.UMGToolSet

UMG widget toolset for AI-driven widget creation and tree manipulation.

IMPORTANT WORKFLOW - for every widget and slot returned by this toolset:
  1. Call ObjectTools.list_properties(widget) to discover exact property names.
  2. Call ObjectTools.get_properties(widget, [...]) with those exact names.
  3. Call ObjectTools.set_properties(widget, {...}) with those exact names.
Property names vary per widget class and CANNOT be guessed - list_properties is required.
Skipping step 1 causes set_properties to silently fail or set wrong properties.

Returns UObject pointers - ToolsetRegistry serializes them as {"refPath": "..."} automatically.
Pass returned Widget, Slot, and Parent pointers directly to ObjectTools or back to this toolset.

21 tools.

### `AddUIComponent`

Adds a UI component of the given class to the named widget.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `widgetName` | `string` | yes | Name of the widget instance to add the component to. |
| `componentClass` | `ref<Class@/Script/UMG.UIComponent>` | yes | The UIComponent subclass to add. |

Returns: `UMGWidgetInfo`

### `AddWidget`

Adds a widget to the tree at the specified position. Returns full widget info including Slot pointer.
When ParentWidget is null and no root exists, the new widget becomes the root of the tree.
Use ObjectTools.list_properties on the returned Widget and Slot to get property names before calling set_properties.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `widgetClass` | `ref<Class@/Script/UMG.Widget>` | yes | The widget class to instantiate. |
| `widgetDisplayName` | `string` | yes | Display name for the new widget instance. |
| `parentWidget` | `ref</Script/UMG.Widget>` |  | The panel widget to add to. Pass null to add to root, or to make this widget the root if the tree is empty. (default `null`) |
| `childIndex` | `integer` |  | Position in parent's child list (0 = first child). -1 (default) appends to end. (default `-1`) |

Returns: `UMGWidgetInfo`

### `CompileWidgetBlueprint`

Compiles a widget blueprint. Returns false with error details if compilation fails.
Errors include missing BindWidget bindings, type mismatches, and graph errors.
Call after all widgets and properties are set. Save separately via AssetTools.save_asset.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to compile. |

Returns: `boolean`

### `CreateWidgetBlueprint`

Creates a new Widget Blueprint asset. Returns the blueprint or nullptr on failure.

| arg | type | req | description |
|---|---|---|---|
| `folderPath` | `string` | yes | Content folder path, e.g. "/Game/UI/Widgets". |
| `assetName` | `string` | yes | Name for the new blueprint asset. |
| `parentClass` | `ref<Class@/Script/UMG.UserWidget>` | yes | The parent UUserWidget class. Get this from GetWidgets Info.ParentClass on the source blueprint. |

Returns: `ref</Script/UMGEditor.WidgetBlueprint>`

### `GetNamedSlots`

Returns available named slots and their content, if any (separate from tree hierarchy).

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to query. |

Returns: `[UMGNamedSlotEntry{slotName:string, hostWidget:ref</Script/UMG.Widget>, contentWidget:ref</Script/UMG.Widget>}]`

### `GetWidgetClassInfo`

Returns the Category, Description and if it's a Panel for a single widget class.
Same per-entry data as ListWidgetClasses, but lets callers query a class they already have
without scanning every UClass. Returns an empty entry if WidgetClass is null.
Can be used to get more information on the class from the Description and Category.

| arg | type | req | description |
|---|---|---|---|
| `widgetClass` | `ref<Class@/Script/UMG.Widget>` | yes | The widget class to inspect. |

Returns: `UMGWidgetClassEntry{widgetClass:ref<Class@/Script/UMG.Widget>, bIsPanel:boolean, category:string, description:string}`

### `GetWidgetDescription`

Full property dump of every widget in the tree.
Each line: [N] Type Name  Prop:Value ...  slot:(SlotProp:Value ...)
N is the 0-based index into result.Widgets -- use result.Widgets[N] to get the widget ref without text parsing.

Same indentation format as GetTaggedWidgetDescription; richer per-widget detail.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The WBP asset. |
| `startWidget` | `ref</Script/UMG.Widget>` |  | nullptr = full tree from root. (default `null`) |
| `maxDepth` | `integer` |  | 1 = no limit; 0 = StartWidget only; N = N levels. (default `-1`) |

Returns: `UMGWidgetDescriptionResult{description:string, widgets:[UMGWidgetInfo]}`

### `GetWidgetTreeDepth`

Returns the maximum depth of the widget tree. Depth: root with no children = 0; root + children = 1; etc.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Represents a reference to a UObject or UClass. |
| `startWidget` | `ref</Script/UMG.Widget>` |  | Represents a reference to a UObject or UClass. (default `null`) |

Returns: `integer`

### `GetWidgets`

Returns blueprint info and all widgets in depth-first order.
Children within each parent are in their panel slot order - this is the hierarchy order shown in the designer.
Info contains ParentClass (pass to CreateWidgetBlueprint) and RootWidgetClass.
Use ObjectTools.list_properties on each returned Widget and Slot to get property names before calling set_properties.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint asset (e.g. "/Game/UI/WBP_MyWidget"), excluding the "_C" suffix. |

Returns: `UMGWidgetTreeInfo{info:UMGWidgetBlueprintInfo, widgets:[UMGWidgetInfo]}`

### `ListWidgetBlueprints`

Lists widget blueprints in a content folder.

| arg | type | req | description |
|---|---|---|---|
| `folderPath` | `string` | yes | Content folder to search, e.g. "/Game/UI". Searches recursively. |

Returns: `[ref</Script/CoreUObject.Object>]`

### `ListWidgetClasses`

Lists available widget classes, optionally filtered by name substring.

| arg | type | req | description |
|---|---|---|---|
| `filter` | `string` |  | Substring to match against class names. Pass empty string to return all classes. (default `""`) |

Returns: `[UMGWidgetClassEntry{widgetClass:ref<Class@/Script/UMG.Widget>, bIsPanel:boolean, category:string, description:string}]`

### `MoveUIComponent`

Moves a UI component before or after another component on the same widget.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `widgetName` | `string` | yes | Name of the widget instance whose component to move. |
| `componentClassToMove` | `ref<Class@/Script/UMG.UIComponent>` | yes | The UIComponent subclass to reorder. |
| `relativeToComponentClass` | `ref<Class@/Script/UMG.UIComponent>` | yes | The UIComponent subclass to move relative to. |
| `bMoveAfter` | `boolean` | yes | True to place after RelativeToComponentClass, false to place before. |

Returns: `boolean`

### `MoveWidget`

Moves a widget to a new parent panel at the specified position. Returns updated widget info with new Slot.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `widget` | `ref</Script/UMG.Widget>` | yes | The widget to move. |
| `newParent` | `ref</Script/UMG.PanelWidget>` | yes | The destination panel widget. |
| `childIndex` | `integer` |  | Position in new parent's child list (0 = first child). -1 (default) appends to end. (default `-1`) |

Returns: `UMGWidgetInfo`

### `RemoveUIComponent`

Removes a UI component of the given class from the named widget.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `widgetName` | `string` | yes | Name of the widget instance to remove the component from. |
| `componentClass` | `ref<Class@/Script/UMG.UIComponent>` | yes | The UIComponent subclass to remove. |

Returns: `boolean`

### `RemoveWidget`

Removes a widget and its children from the tree.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `widget` | `ref</Script/UMG.Widget>` | yes | The widget to remove (along with its children). |

Returns: `boolean`

### `RenameWidget`

Renames a widget. Returns updated widget info or empty on failure.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `widget` | `ref</Script/UMG.Widget>` | yes | The widget to rename. |
| `newDisplayName` | `string` | yes | The new display name. |

Returns: `UMGWidgetInfo`

### `ReplaceWidgetWithChild`

Replaces a panel widget with its first child, removing the panel from the tree.
The widget to replace must be a UPanelWidget with only one child.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint containing the panel widget. |
| `widgetToReplace` | `ref</Script/UMG.Widget>` | yes | The panel widget to replace with its first child. |

Returns: `boolean`

### `ReplaceWidgetWithNamedSlot`

Replaces a host widget with the content of one of its named slots. The host must implement
INamedSlotInterface (e.g., a UUserWidget exposing named slots). The slot's content widget is
moved up to take the host's place in the tree.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint containing the host widget. |
| `widgetToReplace` | `ref</Script/UMG.Widget>` | yes | The host widget to replace. |
| `namedSlot` | `string` | yes | The slot whose content replaces WidgetToReplace. |

Returns: `boolean`

### `ReplaceWidgetWithTemplate`

Replaces a widget instance in the blueprint's widget tree with a new instance created from a
different template widget class. Preserves references for members that exist on both classes
with a compatible type/signature: bindings, BP graph variable references, animation
bindings, and delegate bindings. Members without a compatible counterpart on the new class
are listed in the returned report; references to those members in the outer blueprint will
become orphaned graph nodes / dangling bindings.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint containing the widget to replace. |
| `widgetToReplace` | `ref</Script/UMG.Widget>` | yes | The widget instance to replace (must be in WidgetBlueprint's tree). |
| `templateClass` | `ref<Class@/Script/UMG.Widget>` | yes | The widget class to create the replacement from. |

Returns: `WidgetReplacementReport`

### `SetNamedSlotContent`

Moves or adds content for a named slot. Use this to set new widget based on WidgetClass or attempt to find a widget in a tree by WidgetName.
Returns full widget info including Slot pointer.
The named slot must already exist. For an inherited slot (HostWidget null) the
slot must be declared by a parent class; otherwise the slot must be one the HostWidget exposes. Fails otherwise.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `slotName` | `string` | yes | Name of the slot to fill (e.g., "content", "header"). |
| `widgetClass` | `ref<Class@/Script/UMG.Widget>` | yes | The widget class to place in the slot. |
| `widgetName` | `string` | yes | Name to find or create the new widget instance with. |
| `hostWidget` | `ref</Script/UMG.Widget>` |  | The widget instance that owns the named slot, or null if it's an inherited namedslot. (default `null`) |

Returns: `UMGWidgetInfo`

### `WrapWidgets`

Wraps one or more widgets in a new panel widget of the specified class.
Only the root-most widgets in the selection are wrapped — children of other selected widgets
are skipped because their parent will be wrapped. Returns info for each newly created wrapper.

Use ObjectTools.list_properties on each returned Widget and Slot to discover property names
before calling set_properties (padding, alignment, anchors, etc. vary per panel class).

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | The widget blueprint to modify. |
| `widgets` | `[ref</Script/UMG.Widget>]` | yes | The widgets to wrap. Must all be in WidgetBlueprint's tree. |
| `wrapperClass` | `ref<Class@/Script/UMG.PanelWidget>` | yes | The panel widget class to wrap with (must be a UPanelWidget subclass). |

Returns: `[UMGWidgetInfo]`
