# UMG widgets + Verse fields

## Lifecycle that works
1. `CreateWidgetBlueprint(folderPath, assetName, parentClass=/Script/UMG.UserWidget)`
2. `OpenEditorForAsset(path)` ← **do this before adding fields** (otherwise fields never reach Verse; E3506).
3. `AddWidget` tree (first widget without parent = root).
4. `set_properties` on widget and on returned `slot` (property names via `list_properties`).
5. `AddVerseField` (spec: type, defaultValue, visibility "Public", writeAccess "", bIsVar).
6. `CreateViewBinding(sourceContext=None, sourcePropertyPath=<field>, destinationContext=<widget>, destinationPropertyPath=<prop>, conversionName="")`.
7. `CompileWidgetBlueprint`, `save_assets`, `VerseToolset.BuildAll`, check digest:
   `ReadFile("/<owner>@fortnite.com/<Project> (<Project>/Assets)/<Project>-Assets.digest.verse")`.

Verse sees: `var Field<public>:float = external {}` and events as `Field<public>:event(tuple()) = external {}`.
Module path follows folders: asset in `/Proj/DailyReward/UI/` → `using { DailyReward.UI }` from `/Proj/DailyReward/*.verse`.

## Palette limits
- AddWidget accepts: CanvasPanel, Overlay, SizeBox, ScaleBox, StackBox, WrapBox, GridPanel, UniformGridPanel, ScrollBox,
  WidgetSwitcher, Image, NamedSlot, CustomButton, project user widgets.
- Rejected: every text widget, preset buttons, ProgressBar/Slider are absent.

## Bindable destinations (verified)
| Want | Destination | Notes |
|---|---|---|
| opacity | `RenderOpacity` | float |
| state / which child | WidgetSwitcher `ActiveWidgetIndex` | int; switcher desired size = active child |
| scale | SizeBox `WidthOverride` + `HeightOverride` → child `ScaleBox(Stretch=Fill)` → fixed-size design SizeBox | non-uniform = squash & stretch |
| rotation | `RenderTransform` with conversion `MakeTransform` | float binds to Angle pin; Scale pin defaults (1,1) |
| child widget field | nested WBP's Verse field name (e.g. `G`) | parent field → child field works |
| visibility | `Visibility` with `Conv_BoolToSlateVisibility` | or just use RenderOpacity |
| NOT | `RenderTransform.Scale.X`, `SetRenderTransformAngle`, `QueuePlayAnimationForward` | compile errors |

Event bindings: `CreateViewEventBinding(eventContext=<CustomButton>, eventPropertyPath="OnButtonClicked", destinationContext=None, destinationPropertyPath=<event field>)` compiles,
but **did not fire in-game** in our test → use Verse buttons for clicks (`clicks-and-input.md`).
Only `OnButtonClicked/OnButtonHighlight/OnButtonUnhighlight` are valid Custom Button event sources.

## Numbers without text widgets (glyph sprites)
`WBP_DR_Glyph`: root WidgetSwitcher with 17 children (0-9, +, K, M, x, :, ., blank SizeBox 0-wide), field `G:int` → `ActiveWidgetIndex`.
Parent: StackBox of glyph instances (negative slot padding for tight kerning) inside a `ScaleBox(ScaleToFit)` inside a fixed SizeBox;
parent fields `G1..Gn` bound to each child's `G`. Format numbers in Verse (`DRAmountGlyphs`, `DRTimerGlyphs` in the example).
**Prime the row with a visible glyph before first display** — an all-blank row (0 width) breaks the ScaleBox permanently.

## Layout tips
- Animated element = container SizeBox (fixed, larger than max overshoot) → Overlay → animated SizeBox (bound W/H) centered.
  Overlay clamps children to its size; CanvasPanel does not.
- CustomButton default style is `NoDrawType` (transparent) — fine as a container.
- Set purely decorative widgets to `HitTestInvisible`.
- Name collisions: widget names are blueprint variables; never reuse a field name for a widget.
