# Paint Blaster — input-driven Scene Graph projectiles

Press **Jump** (or **WeaponPrimary** when a ranged weapon mapping is active) to fire a glowing paint ball from your camera.
The ball is a runtime Scene Graph entity moved by hand every `PostPhysics` tick with `FindSweepHits`; the first entity
it hits that carries one of our kit meshes gets a **new material instance** in the ball's colour, plus a Niagara burst.

| Piece | API |
|---|---|
| Input | `GetPlayerInput[P].GetInputEvents(Jump / WeaponPrimary).TriggerActivationEvent.Subscribe(...)` (non-experimental, publishable) |
| Aim | `fort_character.GetViewLocation/GetViewRotation` → `FromVector3/FromRotation` → `rotation.GetForwardAxis()` (helper `SGLabViewRay`) |
| Projectile | entity + `SM_SG_sphere` (glowing `M_SG_Color`, non-collidable) + `paint_ball_component` (velocity integration + sweep) |
| Paint | `PaintEntity`: `GetComponent[SM_SG_cube/sphere/cylinder/torus/wedge]` → `set Mesh.Main = M_SG_Color{Color := ...}` |
| Impact | `NS_SG_Burst` child entity, removed after 2 s |

Files: [`verse/paintblaster_device.verse`](verse/paintblaster_device.verse) (goes in the project's `SGKit/` folder, next to
the `Meshes/`, `Materials/`, `VFX/` asset folders; uses `SGLabViewRay` from `../sg-lab/verse/sgkit/sglab_teleport.verse`).

## Verified (self-test, no human)
`AutoFire` fires 8 balls from a fixed point at the four KitDemo shapes (editor-placed entities):
```
[Paint] input hooked for a player (Jump + WeaponPrimary)
[Paint] hit at (-423.9, 1650.0, 449.6) painted=yes      # cube's front face (cube centre Left 1600, half-size 50)
[Paint] hit at (-141.7, 1650.1, 444.3) painted=yes      # sphere
[Paint] hit at (141.7, 1650.1, 444.4) painted=yes       # cylinder
[Paint] hit at (431.9, 1615.1, 439.0) painted=yes       # torus ring
... (second volley identical)
[Paint] autofire summary: 8 shots, 8 hits, 8 painted
```

## Human test checklist (not verifiable by the agent — synthetic input doesn't reach the client)
1. Start a session, walk to the coloured shapes south of spawn (KitDemo, Lamps, maze walls are BasicShapes → not paintable).
2. Press **Space** (Jump): a glowing ball should fly from the camera; on impact the shape changes colour + burst.
3. Equip any ranged weapon and press **Left mouse**: should also fire (WeaponPrimary).
4. Editor Output Log: one `[Paint] hit at … painted=yes` line per impact.
