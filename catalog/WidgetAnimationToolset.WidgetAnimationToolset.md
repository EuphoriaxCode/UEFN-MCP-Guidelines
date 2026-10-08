# WidgetAnimationToolset.WidgetAnimationToolset

UMG Widget Animation toolset for AI-driven authoring of UWidgetAnimation assets.

UWidgetAnimation extends UMovieSceneSequence, so every SequencerTools /
SequencerKeyframingTools / SequencerConditionTools method that accepts a
UMovieSceneSequence, MovieSceneTrack, MovieSceneSection, or MovieSceneChannel
works on widget animations unmodified. Use this toolset for the UMG-specific
lifecycle and binding work; use the existing Sequencer toolsets for tracks,
sections, and keyframes.

10 tools.

### `AddWidgetToAnimation`

Add a UWidget (or a UPanelSlot with non-null content) as a possessable binding on a
widget animation. Returns a FMovieSceneBindingProxy usable with every SequencerTools
method that takes a binding (add_track_to_binding, etc.).

ObjectToBind must be either:
  - A UWidget inside the Widget Blueprint's tree (typical case: animate a child widget's properties).
  - A UPanelSlot whose Content is non-null (animate slot properties like padding/anchors).

The Widget Blueprint must have a compiled GeneratedClass. The implementation compiles the
blueprint if needed before binding.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Represents a reference to a UObject or UClass. |
| `animation` | `ref</Script/UMG.WidgetAnimation>` | yes | Represents a reference to a UObject or UClass. |
| `objectToBind` | `ref</Script/CoreUObject.Object>` | yes | Represents a reference to a UObject or UClass. |

Returns: `MovieSceneBindingProxy{bindingId:string, sequence:ref</Script/MovieScene.MovieSceneSequence>}`

### `CreateWidgetAnimation`

Create a new UWidgetAnimation on a Widget Blueprint and return its summary.
The empty FWidgetAnimationInfo return signals failure (Animation == nullptr).

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Represents a reference to a UObject or UClass. |
| `animationName` | `string` | yes | Internal asset name. Must not collide with an existing animation. |
| `lengthSeconds` | `number` |  | Initial playback-range length in seconds. Defaults to 1.0s. (default `1`) |

Returns: `WidgetAnimationInfo`

### `FindWidgetAnimation`

Find an animation by internal name. Returns empty info (Animation == nullptr) when not found.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Represents a reference to a UObject or UClass. |
| `animationName` | `string` | yes |  |

Returns: `WidgetAnimationInfo`

### `GetWidgetAnimationBindings`

Get all bindings on a widget animation as FMovieSceneBindingProxy entries.

| arg | type | req | description |
|---|---|---|---|
| `animation` | `ref</Script/UMG.WidgetAnimation>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[MovieSceneBindingProxy{bindingId:string, sequence:ref</Script/MovieScene.MovieSceneSequence>}]`

### `ListWidgetAnimations`

List all animations on a Widget Blueprint.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Represents a reference to a UObject or UClass. |

Returns: `[WidgetAnimationInfo]`

### `RemoveWidgetAnimation`

Remove an animation from a Widget Blueprint.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Represents a reference to a UObject or UClass. |
| `animation` | `ref</Script/UMG.WidgetAnimation>` | yes | Represents a reference to a UObject or UClass. |

Returns: `boolean`

### `RemoveWidgetBinding`

Remove a binding (by GUID) from a widget animation. Removes both the MovieScene possessable and the UMG binding entry.

| arg | type | req | description |
|---|---|---|---|
| `animation` | `ref</Script/UMG.WidgetAnimation>` | yes | Represents a reference to a UObject or UClass. |
| `bindingGuid` | `string` | yes | Globally unique identifier in 8-4-4-4-12 hyphenated form, e.g. "E05FCC13-4D37-9D7A-E238-83859F29AD74". |

Returns: `boolean`

### `RenameWidgetAnimation`

Rename an animation. NewName must not collide with an existing animation on the blueprint.

| arg | type | req | description |
|---|---|---|---|
| `widgetBlueprint` | `ref</Script/UMGEditor.WidgetBlueprint>` | yes | Represents a reference to a UObject or UClass. |
| `animation` | `ref</Script/UMG.WidgetAnimation>` | yes | Represents a reference to a UObject or UClass. |
| `newName` | `string` | yes |  |

Returns: `boolean`

### `SetWidgetAnimationDisplayLabel`

Set the user-facing display label shown in the Animations panel.

| arg | type | req | description |
|---|---|---|---|
| `animation` | `ref</Script/UMG.WidgetAnimation>` | yes | Represents a reference to a UObject or UClass. |
| `displayLabel` | `string` | yes |  |

Returns: `boolean`

### `SetWidgetAnimationLength`

Set the animation playback length in seconds. Updates the MovieScene playback
range to [0, LengthSeconds] in tick resolution. LengthSeconds must be > 0.

| arg | type | req | description |
|---|---|---|---|
| `animation` | `ref</Script/UMG.WidgetAnimation>` | yes | Represents a reference to a UObject or UClass. |
| `lengthSeconds` | `number` | yes |  |

Returns: `boolean`
