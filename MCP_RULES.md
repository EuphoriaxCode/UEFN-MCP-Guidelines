# MCP_RULES — read this before touching UEFN through `unreal-mcp`

Hard rules learned the expensive way (UEFN 42.30, Oct 2026). Every rule was hit in a real build.
Details + evidence live in `topics/`. **If a rule here conflicts with your instinct, the rule wins.**

## 0. Workflow
- Probe before building: `list_toolsets` → `describe_toolset` → one tiny test → then batch.
- Batch with `ProgrammaticToolset.execute_tool_script` (Python sandbox, only `json, math, re, time, datetime, copy`;
  **no `exec`/`eval`**; `open(path,'r')` only inside `%LOCALAPPDATA%\UnrealEditorFortnite\Saved`). Inline your helper lib in every call.
- Tool names inside `call_tool` are the SHORT names (`ListFiles`, not `ValkyrieToolset.VerseToolset.ListFiles`);
  inside `execute_tool(...)` they are the FULL names.
- A tool error inside `execute_tool` often aborts the script even inside `try/except` → check `exists` first instead of catching.
- `VerseToolset.BuildAll` returns diagnostics; empty list = success. Build after every Verse edit.
- New Verse code → new files, never paste into a user's existing file.

## 1. UMG Widget Blueprints
- Verse fields only reach the Assets digest **after the widget's editor has been opened once** in the session
  (`EditorAppToolset.OpenEditorForAsset`). Otherwise Verse says E3506 "Unknown member". Open it BEFORE adding fields.
- **Text widgets cannot be added** by `AddWidget` (`TextBlock`, `UEFN_TextBlock`, Common text… all rejected).
  → bake static text into PNGs; build numbers from a digit-sprite child widget (glyph switcher, see `topics/umg-widgets.md`).
- A widget name must not equal a Verse field name (`Flash` widget + `Flash` field → error). Suffix widgets (`FlashImg`, `GW1`).
- Bind with `MVVMToolset.CreateViewBinding` / `VerseFields.BindWidgetPropertyToVerseField`. Works: `RenderOpacity`,
  `ActiveWidgetIndex`, `WidthOverride`/`HeightOverride` (SizeBox), child widget Verse fields, `Visibility`.
- **Fails**: struct sub-paths (`RenderTransform.Scale.X`), `SetRenderTransformAngle` (not allowed in UEFN),
  `QueuePlayAnimation*` as binding target. Rotation works via `RenderTransform` + conversion `MakeTransform` (float → Angle pin).
- Conversion/event **pins (`savedPins`) are read-only** through the toolset → no Verse-triggered UMG widget animations.
- A `ScaleBox` whose content is 0-wide on first layout stays broken → **prime glyph rows with a visible value before showing**.
- Overlay + large one-sided padding positions unreliably → place such elements directly in a `CanvasPanel`.

## 2. Clicks & input (most important)
- **UMG Custom Button → Verse `event` field did NOT fire in-game.** Don't rely on it.
- **UMG user widgets in a Verse `canvas` swallow clicks over their whole area**; full-screen ones block everything below.
- ✅ Working pattern: UMG = visuals only (`HitTestInvisible`); click targets = Verse `button{Slot := button_slot{Widget := color_block{DefaultOpacity := 0.0, DefaultDesiredSize := ...}}}`
  placed ON TOP of all UMG widgets in the canvas. Use `OnClick()`, `HighlightEvent()`, `UnhighlightEvent()`.
- Full-screen UMG layers (popups) → `canvas.AddWidget` only while shown, `RemoveWidget` after.
- "Click outside to close": full-screen transparent Verse button + a transparent blocker button over the panel area.
- Escape / gamepad Back: `using {/Verse.org/Input}`, `using {/Verse.org/Input/UI}`;
  `GetPlayerInput[P].GetInputEvents(Back).TriggerActivationEvent.Subscribe(...)` and `AddInputMapping(MenuNavigationMapping)` while open,
  `RemoveInputMapping` on close. Also set `CloseButton.TriggeringInputAction = option{Back}`.
- `player_ui.AddWidget(W, player_ui_slot{InputMode := ui_input_mode.All})` captures the mouse until **RemoveWidget**.
  Put `RemoveWidget` in a `defer:` so a cancelled close can never trap the player.
- **Never auto-open a menu with input capture** unless asked; open via a button device.

## 3. Verse language traps
- `race:` cancels the losing branches — if a branch performs an action that signals the event another branch awaits,
  it cancels ITSELF halfway. Race only the waiting; do the action after the race.
- UMG event fields are `event(tuple())` → `.Await()` only, no `.Subscribe()`.
- A `<no_rollback>` call cannot sit in a failure context: `X := DoClaim(P)` first, then `if (Day := X?)`.
- `<private>` only inside classes; use `<internal>` at module scope.
- Local var named `UI` clashes with an asset module `UI` → name it `PlayerUI`.
- Archetype `dr_save:` with indented fields cannot be written inline as a call argument — assign to a name first.
- `canvas_slot.ZOrder` is a constrained int type; parameters must be typed `type{_X:int where 0 <= _X, _X <= 2147483647}`.
- No lambdas: pass bound methods, or use an abstract class with an overridable method.

## 4. Materials
- **Custom (HLSL) node compiles but is NOT supported in UEFN** → build graphs from standard nodes.
- UI materials: `materialDomain MD_UI`, `BLEND_Translucent`, `MSM_Unlit`; animate with `Time` (Sine/Cosine use period 1 = Hz).
  Continuous/passive motion belongs in materials (client-side, smooth); Verse field tweens run at server tick (~30 Hz).
- Custom node `inputs` array: when adding elements, resend the existing element unchanged plus the new one.

## 5. Textures
- `TextureTools.import_file` cannot overwrite → import as `_v2`, repoint brushes/MIs, delete the old asset (check `get_referencers`).
- UI texture settings: `TEXTUREGROUP_UI`, `TMGS_NoMipmaps`, `TC_EditorIcon`, `neverStream`, clamp (wrap only for tiling).

## 6. Devices
- `DeviceToolset.SetDeviceProperty` **cannot set device-reference arrays** (`[]button_device` etc.) → the user links them in Details.
- `@editable` arrays of `class<concrete>` with defaults work and show in Details.
- Verse device asset path after build: `/<Project>/_Verse.<Module>-<device_class>`.
- `SetDeviceProperty` also **rejects single device references** (`round_settings_device`: "is not valid round_settings_device") → Details panel.
- `SetDeviceProperty` on a `[]string` must keep the array length (changing length errors "ArrayRemove … ambiguous").
- Island Settings is NOT in `ListDeviceAssets`: place it with `SceneTools.add_to_scene_from_class(actor_type=
  /CreativeCoreDevices/Device_ExperienceSettings_V2_UEFN.Device_ExperienceSettings_V2_UEFN_C)`.
- `ObjectTools.set_properties` on creative devices (Island Settings) returned `false` when `values` was passed as an object *(JSON-string form unverified)*.

## 7. Testing
- `SessionToolset`: `StartSession` (fails if one is active → `PushChanges`), `StartGame`/`StopGame`, `PushChanges(bVerseOnly)`.
- Synthetic mouse/keyboard input (SendInput) is **ignored by the Fortnite client** → add a debug option (e.g. auto-claim)
  to exercise flows; ask the human to test real clicks.
- Screenshot the client with `PrintWindow` (works when occluded): `scripts/windows/capture_fortnite_window.ps1`.
- Verse `Print` from the server is not in the client log; ask the user for the editor Output Log lines.
- Always restore production device settings after testing (test values: short day length, reset on join, auto-claim).
- `StartSession` fails "Validation failed" when the level has no Island Settings device (`UEFNValidation: Error … 0 Island Settings Devices`).
- A failed `StartSession` leaves an **"Unable to Play" modal** in the editor that blocks ALL MCP calls until it's closed.
- `StartSession` can block > 10 min → run it in the background and watch `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Logs\UnrealEditorFortnite.log`
  (`Session -> Channel State`, `LogVerse`). Server-side Verse `Print` DOES appear in that editor log as `LogVerse:`.
- `StopSession` can report `Disconnected` while the toolbar still shows a running game → check `GetSessionStatus` before `StartSession`.

## 8. Scene Graph (details: `topics/scene-graph.md`)
- **No tool creates prefabs** → the human does Outliner → right-click entity → Create Prefab. Plan the work so this is one early step.
- `CreateEntity(parentEntity=…)` takes a **local** transform; `SetEntityTransform` is **world**.
- Basic-shape meshes have **no material property** (editor or Verse) → carry color with lights, or use other meshes.
- Find parts by component type (`FindDescendantComponents`), never by entity name.
- `OnBeginSimulation` re-runs on session start and Stop/Start Game → apply initial state there.

## 9. What the agent cannot do (don't burn time)
- Create/edit prefab assets; link device references; drive the editor UI.
- Computer use can't find the UEFN window by any name ("UEFN", "Unreal Editor for Fortnite", exe name).
- Synthetic Win32 input to the editor gets denied by the agent's permission system → ask the human.
- Python remote execution reports `bRemoteExecution=true` on `239.0.0.1:6766` but never answers; the sandbox has no `unreal` module.
