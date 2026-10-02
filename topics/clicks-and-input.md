# Clicks, menus and input capture

## What failed (user-tested in a live session)
1. UMG Custom Button `OnButtonClicked` → Verse `event` field → `Widget.Clicked.Await()` : **never fired.**
2. Wrapping the UMG widget itself in a Verse `button` : **still no clicks** — UMG user widgets placed in a Verse canvas
   swallow clicks over their whole area, and the full-screen frame/popup widgets sat above/below everything.

## What works
```verse
DRHitArea(W:float, H:float):color_block =
    color_block{DefaultColor := NamedColors.Black, DefaultOpacity := 0.0, DefaultDesiredSize := vector2{X := W, Y := H}}

ClaimBtn := button{Slot := button_slot{Widget := DRHitArea(470.0, 150.0)}}
# canvas order (later = on top): full-screen frame, backdrop button, panel blocker, cards, UMG button art, hit buttons
ClaimBtn.OnClick().Await()        # or .Subscribe
ClaimBtn.HighlightEvent()         # hover -> animate the UMG art
```
- UMG art for buttons: set its root and inner CustomButton to `HitTestInvisible`.
- Full-screen UMG layers (popup with confetti) → `Root.AddWidget(slot)` while shown, `Root.RemoveWidget(widget)` after.
- Click outside to close: full-screen `button` with a transparent `color_block` (Fill alignment) BELOW the content,
  plus a transparent "panel blocker" button sized like the panel so clicks on the panel don't close.

## Escape / gamepad Back
```verse
using { /Verse.org/Input }
using { /Verse.org/Input/UI }      # Back, MenuNavigationMapping
if (PI := GetPlayerInput[Player]):
    PI.GetInputEvents(Back).TriggerActivationEvent.Subscribe(OnBack)   # payload tuple(player, logic)
# while the menu is open:
PI.AddInputMapping(MenuNavigationMapping)     # remove with RemoveInputMapping on close
set CloseBtn.TriggeringInputAction = option{Back}
```

## Input capture & getting stuck
- `PlayerUI.AddWidget(Root, player_ui_slot{InputMode := ui_input_mode.All})` shows the cursor and blocks movement
  until `RemoveWidget(Root)`.
- Always remove inside a `defer:` in the close function:
```verse
CloseUI()<suspends>:void =
    set IsOpen = false
    defer:
        if (PlayerUI := GetPlayerUI[Player]):
            PlayerUI.RemoveWidget(Root)
    CloseEvent.Signal()
    # ... close animation ...
```
- Bug we shipped once: auto-close timer `race{ CloseEvent.Await(); block{ Sleep(T); CloseUI() } }` — CloseUI signals
  CloseEvent → the race cancels the block mid-close → UI faded but still capturing the mouse. Fix: race only the wait.
- Give players several exits: X, Escape/Back, click outside, idle timeout.
- Don't auto-open capture menus on join unless requested; prefer a world button + a small non-capturing HUD reminder
  (`InputMode := ui_input_mode.None`).
