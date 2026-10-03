# Lamp showroom (Scene Graph) — work in progress

Goal: six interactive lamps built from **one Scene Graph prefab**, in two rows, three colors, mixed initial states, each toggling
independently, staying aligned when moved/rotated, restoring their initial state each round, and showing prefab edits
propagating while instance overrides are preserved. UEFN 42.30.

**Status: incomplete.** The source lamp, all Verse, a showroom room and the test tooling exist. Blocked on editor-only steps:
the prefab, so also the six instances and the propagation demo, plus the round wiring.

## Lamp structure (becomes `PF_Lamp`)
```
Lamp (root)   transform, lamp_toggle_component      InitiallyOn, LightColor, DebugLabel
├─ Base        cylinder (.2/.2/1.3)                  local (0,0,65)
├─ Bulb        sphere (.45) + sphere_light_component local (0,0,155)  Intensity 200, no shadows
├─ Switch      cube (.2) + lamp_switch_component     local (35,0,45)   prompt "<label> switch: turn ON/OFF"
└─ SwitchLever cube + lamp_state_indicator_component local (50,0,45)   lever +9 cm ON / -9 cm OFF
```
ON = light on in the lamp's color + bulb visible + lever up. OFF = light off + bulb hidden + lever down.
The bulb can't be tinted (basic shapes have no material property in 42.30), so the color is carried by the light.

## Verse ([`verse/`](verse))
| File | Role |
|---|---|
| `lamp_toggle_component.verse` | state + drives every light / bulb mesh / indicator under the root (found by type) |
| `lamp_switch_component.verse` | `basic_interactable_component` subclass with a state-aware prompt |
| `lamp_state_indicator_component.verse` | moves its entity in local space to show on/off |
| `lamp_round_reset_device.verse` | `RoundBeginEvent` → `ResetToInitialState()` on all lamps |
| `lamp_selftest_device.verse` | runtime test: logs all states, toggles only lamps with chosen labels, logs again |

## Tools ([`tools/`](tools)): run from your machine against the editor's MCP server
`mcp.py` / `t.py` (minimal MCP client), `lamp_lib.py` (entity helpers), `rotation_test.py`,
`finish_showroom.py` (places/reuses six `PF_Lamp` instances and applies Red/Green/Blue + ON/OFF overrides), `report_lamps.py`.

## Manual steps (no tool available to the agent)
1. Outliner → right-click the lamp root entity → **Create Prefab** → `LampShowroom/PF_Lamp`, then Build Verse.
2. `lamp_round_reset_device.RoundSettings` → Round Settings device (Details panel).
3. Island Settings: Total Rounds 2, Round Time Limit 1 min (for the round test). Optional: Force Night.

## Verified
- Verse builds clean (5 files).
- Moving and rotating the root: all parts aligned, 0.000 cm error ([output](tools/rotation_test_output.txt), [screenshot](screenshots/rotation_test_yaw45.png)).
- Runtime: initial state applied on session start and re-applied on Stop/Start Game (`[LampShowroom] Lamp reset -> OFF`).
- Runtime: self-test toggled the lamp OFF → ON with no Verse errors. Real player presses of the (original) switch were seen in the log.

## Not yet verified
Prefab and six instances, independence across six lamps, prefab propagation with preserved overrides, multi-round reset,
and a human check of the prompt text and lever in game.
