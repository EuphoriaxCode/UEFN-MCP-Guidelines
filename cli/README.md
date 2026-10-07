# `uefn` — CLI for driving UEFN through its MCP server

Pure-Python (3.9+, no dependencies). Talks to the editor's streamable-HTTP MCP endpoint
(`http://127.0.0.1:8000/mcp`, override with `UEFN_MCP_URL`) and wraps the toolsets in short, scriptable commands.
Built so an AI agent (or you) can work on Scene Graph levels quickly and reproducibly.

```bash
python cli/uefn.py status            # or cli\uefn.cmd status on Windows
```

## Commands
| Command | What it does |
|---|---|
| `status` | toolsets, session/game state, Verse roots, entity count |
| `wait [--timeout s]` | block until the editor's MCP answers (after a launch or crash) |
| `toolsets` / `describe <ts> [tool]` | list toolsets / tools / one tool's schema. Aliases: `entity verse session device editor logs scene asset object material mi texture mesh umg fields mvvm niagara script …` |
| `call <ts> <tool> [json\|@file]` | call any tool; images (viewport captures) are saved to `--image` |
| `script <file.py> [--lib name]` | run a sandbox script (`execute_tool_script`); `--lib` prepends `cli/sandbox/<name>.py` |
| `catalog` | regenerate `catalog/` (every toolset's tools and schemas as Markdown + JSON) |
| `digest [module] [--grep re] [--class c] [--comments]` | compact Verse API from the on-disk digests (works offline) |
| `log [regex] [-n N] [--client]` | tail the editor (or Fortnite client) log, e.g. `uefn log "\[SGLab\]"` |
| `shot [out.png] [--labels]` | capture the editor viewport |
| `cam [--at x,y,z] [--look x,y,z \| --rot p,y,r]` | read/move the editor camera |
| `verse ls\|cat\|grep\|rm\|push\|build` | Verse files; `verse push local.verse [/proj/Dir] --build` |
| `build` | `BuildAll`; prints `BUILD OK` or the diagnostics and exits 1 |
| `session status\|start\|stop\|push\|game-start\|game-stop\|restart` | play-test loop (`restart` = push + restart game) |
| `sg tree [path] [--comps] [--depth n]` | entity tree with short names |
| `sg classes [filter] [--entities]` | component (or entity/prefab) classes |
| `sg comps <path>` / `sg props <path> <comp>` | components of an entity / editable properties of one |
| `sg get\|set <path> <comp> <prop> [value]` | read/write a component property (`value` is JSON or a bare string) |
| `sg add <path> <comp[,comp]>` / `sg rmcomp <path> <comp>` | attach / remove components |
| `sg new <Parent/Name> [--at] [--rot] [--scale] [--comp a,b] [--cls prefab]` | create an entity (transform is LOCAL to the parent) |
| `sg rm <path>` | delete an entity (and its subtree) |
| `sg xf <path> [--at] [--rot] [--scale] [--world]` | read or set transform; local by default |
| `sg apply spec.json [--parent P] [--prune]` | idempotent declarative build (see below) |
| `sg dump <path> [--props]` | export an entity subtree as a spec (round-trips with `apply`) |
| `sg atlas [filter]` | (re)build `catalog/scene-graph/component-atlas.*` |

**Entity paths** use short names (the editor's random `_xxxx_123` suffix is stripped): `Showroom/BackWall`.
A bare name works when it is unique. Full display names and raw `refPath`s also work.
**Component names**: friendly class names (`sphere_light_component`, `LampShowroom-lamp_toggle_component`) or aliases
`cube sphere cylinder cone plane light spot rectlight sun interact text keyframed particles decal camera`.

## Declarative scene specs
```json
{"name": "Arena", "at": [0, 0, 400], "children": [
  {"name": "Floor", "scale": [20, 20, 0.2], "components": {"cube": {}}},
  {"name": "Pillar", "at": [-800, -800, 150], "scale": [0.5, 0.5, 3],
   "repeat": {"count": 4, "step": [533, 0, 0], "name": "Pillar_{i}"},
   "components": {"cylinder": {"CastShadow": false}}},
  {"name": "Lamp", "at": [0, 0, 600], "components": {"light": {"Intensity": 800, "ColorFilter": {"r": 1, "g": 0.3, "b": 0.1}}}}
]}
```
- `at`/`rot`/`scale` are **local** to the parent (rot = pitch, yaw, roll in degrees). `scale` may be a single number.
- `apply` matches existing entities by name under the same parent: updates transform/props, adds missing components,
  creates missing entities. `--prune` deletes children that are not in the spec.
- `repeat` expands one node into `count` siblings (`step` added per index, optional `yaw_step`).

## Notes
- The session id is cached in `%TEMP%/uefn_mcp_sid.txt`; a stale id is refreshed automatically.
- Component classes are cached in `%TEMP%/uefn_component_classes.json` (refreshed on a miss).
- Local↔world math follows Unreal's FRotator/FQuat conventions (`uefncli/xform.py`), verified against editor read-backs.
- Never probe `UI_grid_container_component` with `AddComponent` on a bare entity — it crashes UEFN 42.30.
