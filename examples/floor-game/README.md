# Light Up The Floor — a runtime Scene Graph minigame

Built and verified by an agent through the `uefn` CLI in one session (UEFN 42.30). Everything in the game is created by
Verse at runtime from Scene Graph entities — no props, no devices other than the one Verse device.

| Feature | How |
|---|---|
| 5×5 board of tiles | `SM_SG_cube` (our own imported mesh) per tile, each with **its own** `M_SG_Color` material instance |
| Step detection | invisible, non-colliding `SM_SG_cube` trigger child per tile → `EntityEnteredEvent` (fires for the player's character) |
| Tile lights up | `set M.Color = MakeColorFromHSV(...)`, `set M.Glow = 3.0` + a one-shot `NS_SG_Burst` Niagara burst spawned as a child entity and removed after 2 s |
| Win | all lit → 5× `NS_SG_Confetti`, `ROUND n COMPLETE`, board resets after 4 s |
| Decoration | 4 cylinders with `keyframed_movement_component` (ping-pong, +250 cm + 180° yaw) |
| Player orb | glowing sphere + `sphere_light_component` that follows the character (`sglab_follow_component`, PostPhysics tick) |
| Self-test | `AutoPlayDemo` teleports the first player over the tiles in snake order (0.35 s per tile) and logs every event |

## Files
- [`verse/floorgame_device.verse`](verse/floorgame_device.verse) — the game (goes into the project's `SGKit/` folder, next to
  the `Meshes/`, `Materials/`, `VFX/` asset folders; it also uses `sglab_follow_component` and `SGLabTeleport` from
  [`../sg-lab/verse/sgkit`](../sg-lab/verse/sgkit)).
- Assets: meshes from [`cli/uefncli/meshgen.py`](../../cli/uefncli/meshgen.py) imported by
  [`experiments/e09_mesh_material.py`](../../experiments/e09_mesh_material.py); VFX created with `NiagaraToolset_System.CreateNiagaraSystem`
  from engine templates (see `experiments/LOG.md` E19).

## Rebuild from scratch with the CLI
```bash
python -X utf8 experiments/e09_mesh_material.py           # meshes + material + instances
# VFX: see E19 in experiments/LOG.md (CreateNiagaraSystem from /Niagara/DefaultAssets/Templates/...)
python cli/uefn.py verse push "examples/sg-lab/verse/sgkit/*.verse" /<plugin-guid>/SGKit
python cli/uefn.py verse push examples/floor-game/verse/floorgame_device.verse /<plugin-guid>/SGKit --build
python cli/uefn.py device place floorgame_device --at 1500,1800,384
python cli/uefn.py session restart
python cli/uefn.py log "\[Floor\]"
python cli/uefn.py clip --frames 9 --interval 1.3 --dir examples/floor-game/screenshots --prefix run
```

## Verified run (log)
```
[Floor] board ready: 25 tiles
[Floor] autoplay: walking the board
[Floor] tile 0 lit (1/25) … tile 4 lit (5/25), tile 9 … 5, tile 10 … 14, tile 19 … 15, tile 20 … tile 24 lit (25/25)
[Floor] ROUND 1 COMPLETE
[Floor] autoplay done: 25 lit, round 1
[Floor] board reset
```
Each tile fired exactly once, in snake order, ~0.37 s apart (= the teleport interval) → triggers are reliable.
Screens: [`screenshots/run_sheet.jpg`](screenshots/run_sheet.jpg).

## Not verified / next
- A human walking (not teleporting) over the tiles; multiplayer (which player lit a tile — `Other` is not a `player`).
- Better framing for screenshots (a Scene Graph camera, experimental).
