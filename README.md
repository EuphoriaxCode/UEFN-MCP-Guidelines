# UEFN × MCP knowledge base

Lessons, rules and reusable scripts for building in **Unreal Editor for Fortnite (UEFN)** with an AI agent through the
`unreal-mcp` server (Valkyrie / editor toolsets). Every entry was learned in a real build and verified in-game unless marked otherwise.

> **NL:** Dit is een kennisbank voor AI-agents die UEFN via MCP aansturen. Geef bij elke sessie minstens
> [`MCP_RULES.md`](MCP_RULES.md) mee (of laat de agent deze repo eerst lezen), zodat bekende fouten niet opnieuw gemaakt worden.

## How to use with an agent
Start every UEFN/MCP task with something like:
> Read `MCP_RULES.md` from github.com/EuphoriaxCode/UEFN first and follow it. Check `topics/` for the area you touch.

| File | What |
|---|---|
| [`MCP_RULES.md`](MCP_RULES.md) | **Short must-follow checklist** (paste this into the agent's context) |
| [`topics/mcp-toolsets.md`](topics/mcp-toolsets.md) | Which toolset does what, sandbox limits, asset/class paths |
| [`topics/umg-widgets.md`](topics/umg-widgets.md) | Building Widget Blueprints, Verse fields, bindings, glyph numbers |
| [`topics/clicks-and-input.md`](topics/clicks-and-input.md) | Clickable menus that actually work, Escape, never trapping the mouse |
| [`topics/animation.md`](topics/animation.md) | Material-based passive animation + Verse tween engine + choreography |
| [`topics/materials-and-textures.md`](topics/materials-and-textures.md) | UI materials from code, texture import/update, generated art |
| [`topics/verse.md`](topics/verse.md) | Verse compiler errors we hit and the patterns that fix them |
| [`topics/testing.md`](topics/testing.md) | Session loop, screenshots, debug options, what agents can't test |
| [`scripts/sandbox/`](scripts/sandbox) | Helper libs to inline into `execute_tool_script` (UMG builder, material DSL) |
| [`scripts/art/`](scripts/art) | Pillow/numpy SDF art generator (Roblox-style UI) + mockup composer |
| [`scripts/windows/`](scripts/windows) | Capture the Fortnite client window (PrintWindow) |
| [`examples/daily-reward/`](examples/daily-reward) | Complete 7-day Daily Reward UI (Verse + build scripts + screenshots) |

## Contributing a lesson
Add it where it belongs (`topics/*.md`); if it is a "would have saved an hour" rule, also add one line to `MCP_RULES.md`.
Format: **symptom → cause → fix**, plus the UEFN version. Mark untested ideas as *(unverified)*.

Versions: UEFN 42.30 (Fortnite Release-42.30), October 2026.
