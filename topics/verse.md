# Verse (UEFN 42.30) — gotchas and useful APIs

## Compiler errors we hit
| Error | Cause | Fix |
|---|---|---|
| 3506 Unknown member `X` in `WBP_...` | widget editor not opened before fields were added | OpenEditorForAsset, rebuild |
| 3506 Unknown member `Subscribe` in `event(tuple())` | UMG event fields are events | `.Await()` in a loop |
| 3594 Access level private only inside classes | `<private>` on module-level fn | `<internal>` |
| 3588/3532 ambiguous identifier `UI` | local var named like an asset module | rename (`PlayerUI`) |
| 3512 `no_rollback` not allowed in context | calling a non-transactional fn inside `if (...)` | call first, test the option after |
| S88 Expected expression, got ")" | indented archetype as call argument | bind to a name first |
| 3506 Unknown identifier `Back` | qualified `(/Verse.org/Input/UI:)Back` doesn't resolve | `using { /Verse.org/Input/UI }` then `Back` |

## Patterns
- Map set is failable: `if (set M[K] = V) {}`. Same for `weak_map`.
- Persistence: `dr_save := class<final><persistable>:` (immutable fields, defaults) + module-level
  `var Saves:weak_map(player, dr_save) = map{}`. Replace the whole object on update.
- Time: `GetSecondsSinceEpoch()` (real UTC seconds, `<reads>`), `GetSimulationElapsedTime()` for tweens.
- Math: `Floor/Ceil/Round/Int` are `<decides>` (`[ ]`), `Mod[a,b]`, `Quotient[a,b]` too; `Clamp/Min/Max/Lerp/Pow/Sin/Cos`.
- `for (I -> Item : Array)` gives index + value; `for` returns an array.
- Player join/leave: `GetPlayspace().PlayerAddedEvent()/PlayerRemovedEvent()`; also iterate `GetPlayers()` in OnBegin.
- One widget instance per player; one watcher loop per instance; end loops with a `DestroyEvent` race on leave.
- `defer:` runs on normal exit AND cancellation — use it for cleanup.
- `race` cancels losing branches immediately, including a branch that is mid-action.
- `player_ui_slot{InputMode := ui_input_mode.All}` = cursor + no movement; `None` = HUD only.
- Device APIs used: `item_granter_device.GrantItem(agent)`, `trigger_device.Trigger(agent)` / `TriggeredEvent:listenable(?agent)`,
  `button_device.InteractedWithEvent` / `SetInteractionText(message)`, `audio_player_device.Play(agent)`.
- `message` constants need `<localizes>`: `ButtonText<localizes>:message = "Daily Rewards"`.

## Verse UI (native) widgets worth knowing
`canvas` (Slots, AddWidget(slot), RemoveWidget(widget)), `canvas_slot` (Anchors, Offsets, Alignment, SizeToContent, ZOrder, Widget),
`button` (container: Slot, OnClick, HighlightEvent, UnhighlightEvent, TriggeringInputAction),
`color_block` (DefaultColor, DefaultOpacity 0..1, DefaultDesiredSize), `texture_block`, `text_block`, `stack_box`, `overlay`.
UMG user widgets are `widget` subclasses and can go into any Verse slot.
