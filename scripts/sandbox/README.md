# Sandbox helper libs

`execute_tool_script` blocks `exec`, so these files are **pasted in front of** each build script (concatenate text).

- `mcp_umglib.py` — `WB('WBP_Name')` builder: creates the WBP, opens its editor (required for Verse fields), `add/img/empty/field/bind/event/glyphs/done`. Collects non-fatal errors in `ERR`.
- `mcp_build_cards.py` — example build script using the lib (day card + mega card).
- `mcp_matlib.py` — material DSL `G('M_Name')` + `make_mi(...)` for material instances.
- `mcp_build_materials.py` — the 7 animated UI materials of the daily-reward example.

Adjust the folder constants (`D`, `F`, `TX`) to your project path (`/<Project>/...`).
Later fixes in the example (Verse hit-area buttons, HitTestInvisible art, primed glyphs) were applied with small one-off
calls — see `../../MCP_RULES.md` and `../../topics/clicks-and-input.md` before reusing the button builders.
