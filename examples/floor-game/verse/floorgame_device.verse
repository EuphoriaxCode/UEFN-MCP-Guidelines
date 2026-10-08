# Light Up The Floor — a minigame built entirely from Scene Graph entities at runtime.
#
# * W x H tiles: custom mesh (SM_SG_cube) + their OWN material instance (M_SG_Color).
# * Each tile has an invisible, non-colliding trigger child; the player's character entering it lights the tile:
#   colour by order, glow, and a one-shot Niagara burst (NS_SG_Burst) spawned as a child entity.
# * All tiles lit -> confetti (NS_SG_Confetti) + reset after a pause. An orb with a light follows every player.
# * AutoPlayDemo teleports the first player across the tiles (snake order) to self-test without a human.
#
# Must live in the SGKit/ folder: Meshes/, Materials/ and VFX/ under it are internal asset modules.
#   uefn log "\[Floor\]"

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Verse.org/SceneGraph/KeyframedMovement }
using { /Verse.org/SpatialMath }
using { /Verse.org/Colors }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { Meshes }
using { Materials }
using { VFX }

# Per-tile state lives on a component, so the trigger handler only needs the tile entity.
floor_tile_component<public> := class<final_super>(component):
    var Index<public>:int = 0
    var Lit<public>:logic = false
    var Material<public>:?M_SG_Color = false
    var Game<public>:?floorgame_device = false

    OnTriggerEnter(Other:entity):void =
        if (G := Game?, not Lit?):
            G.LightTile(Self)

floorgame_device<public> := class(creative_device):

    @editable
    Origin<public>:vector3 = vector3{Forward := -2500.0, Left := 0.0, Up := 400.0}

    @editable
    GridW<public>:int = 5

    @editable
    GridH<public>:int = 5

    @editable
    TileSize<public>:float = 220.0

    @editable
    AutoPlayDemo<public>:logic = true

    var Tiles<private>:[]floor_tile_component = array{}
    var LitCount<private>:int = 0
    var RoundNo<private>:int = 0
    var Board<private>:?entity = false

    One()<computes>:vector3 = vector3{Forward := 1.0, Left := 1.0, Up := 1.0}
    V(F:float, L:float, U:float)<computes>:vector3 = vector3{Forward := F, Left := L, Up := U}
    Xf(P:vector3, S:vector3)<transacts>:transform = transform{Translation := P, Rotation := IdentityRotation(), Scale := S}

    OnBegin<override>()<suspends>:void =
        if (Sim := GetSimulationEntity[]):
            Root := entity{}
            Root.AddComponents(array{transform_component{Entity := Root}})
            Root.SetLocalTransform(Xf(Origin, One()))
            Sim.AddEntities(array{Root})
            set Board = option{Root}
            BuildBoard(Root)
            BuildPillars(Root)
            for (P : GetPlayspace().GetPlayers()):
                AddOrb(Root, P)
            Print("[Floor] board ready: {Tiles.Length} tiles")
            if (AutoPlayDemo?):
                Sleep(2.0)
                AutoPlay()

    # ------------------------------------------------------------------ building
    BuildBoard(Root:entity):void =
        for (Y := 0..GridH - 1, X := 0..GridW - 1):
            Local := V((X * 1.0 - (GridW - 1) * 0.5) * TileSize, (Y * 1.0 - (GridH - 1) * 0.5) * TileSize, 0.0)
            Tile := entity{}
            Mesh := SM_SG_cube{Entity := Tile}
            M := M_SG_Color{}
            set M.Color = MakeColorFromHSV(220.0, 0.25, 0.35)
            set M.Glow = 0.0
            set M.Roughness = 0.35
            set Mesh.Main = M
            State := floor_tile_component{Entity := Tile}
            set State.Index = Tiles.Length
            set State.Material = option{M}
            set State.Game = option{Self}
            Tile.AddComponents(array{transform_component{Entity := Tile}, Mesh, State})
            Tile.SetLocalTransform(Xf(Local, V(TileSize / 100.0 - 0.1, TileSize / 100.0 - 0.1, 0.2)))
            Root.AddEntities(array{Tile})
            # trigger: invisible, non-colliding box above the tile (children inherit the tile's scale)
            Trigger := entity{}
            TMesh := SM_SG_cube{Entity := Trigger}
            set TMesh.Visible = false
            set TMesh.Collidable = false
            Trigger.AddComponents(array{transform_component{Entity := Trigger}, TMesh})
            Trigger.SetLocalTransform(Xf(V(0.0, 0.0, 600.0), V(0.9, 0.9, 10.0)))
            Tile.AddEntities(array{Trigger})
            TMesh.EntityEnteredEvent.Subscribe(State.OnTriggerEnter)
            set Tiles += array{State}

    BuildPillars(Root:entity):void =
        Half := (GridW * 1.0) * 0.5 * TileSize + 200.0
        for (I := 0..3):
            Sx := if (I = 0 or I = 3) then -1.0 else 1.0
            Sy := if (I < 2) then -1.0 else 1.0
            P := entity{}
            Mesh := SM_SG_cylinder{Entity := P}
            M := M_SG_Color{}
            set M.Color = MakeColorFromHSV(90.0 * I, 0.8, 1.0)
            set M.Glow = 0.2
            set Mesh.Main = M
            KM := keyframed_movement_component{Entity := P}
            P.AddComponents(array{transform_component{Entity := P}, Mesh, KM})
            P.SetLocalTransform(Xf(V(Sx * Half, Sy * Half, 100.0), V(0.6, 0.6, 2.0)))
            Root.AddEntities(array{P})
            KM.SetKeyframes(array{keyframed_movement_delta{
                Transform := transform{Translation := V(0.0, 0.0, 250.0), Rotation := MakeRotationFromYawPitchRollDegrees(180.0, 0.0, 0.0), Scale := One()},
                Duration := 1.2 + 0.3 * I, Easing := ease_in_out_cubic_bezier_easing_function{}}},
                pingpong_keyframed_movement_playback_mode{})
            KM.Play()

    AddOrb(Root:entity, P:player):void =
        if (C := P.GetFortCharacter[]):
            Orb := entity{}
            Mesh := SM_SG_sphere{Entity := Orb}
            M := M_SG_Color{}
            set M.Color = MakeColorFromHSV(45.0, 0.9, 1.0)
            set M.Glow = 6.0
            set Mesh.Main = M
            set Mesh.Collidable = false
            set Mesh.Queryable = false      # don't let the orb trigger tiles
            Follow := sglab_follow_component{Entity := Orb}
            set Follow.Target = option{C}
            L := sphere_light_component{Entity := Orb}
            Orb.AddComponents(array{transform_component{Entity := Orb}, Mesh, L, Follow})
            Orb.SetLocalTransform(Xf(V(0.0, 0.0, 0.0), V(0.3, 0.3, 0.3)))
            set L.Intensity = 1500.0
            set L.CastShadows = false
            Root.AddEntities(array{Orb})

    # ------------------------------------------------------------------ game logic
    LightTile(T:floor_tile_component):void =
        set T.Lit = true
        set LitCount += 1
        if (M := T.Material?):
            Hue := Quotient[LitCount * 360, Max(1, Tiles.Length)] or 0
            set M.Color = MakeColorFromHSV(Hue * 1.0, 1.0, 1.0)
            set M.Glow = 3.0
        SpawnFx(T.Entity, NS_SG_Burst{Entity := entity{}}, 2.0)
        Print("[Floor] tile {T.Index} lit ({LitCount}/{Tiles.Length})")
        if (LitCount = Tiles.Length):
            spawn{ Win() }

    Win()<suspends>:void =
        set RoundNo += 1
        Print("[Floor] ROUND {RoundNo} COMPLETE")
        if (Root := Board?):
            for (I := 0..4):
                SpawnFx(Root, NS_SG_Confetti{Entity := entity{}}, 4.0)
        Sleep(4.0)
        for (T : Tiles):
            set T.Lit = false
            if (M := T.Material?):
                set M.Color = MakeColorFromHSV(220.0, 0.25, 0.35)
                set M.Glow = 0.0
        set LitCount = 0
        Print("[Floor] board reset")

    # one-shot VFX: child entity holding the particle component, removed after Life seconds
    SpawnFx(Parent:entity, Fx:particle_system_component, Life:float):void =
        E := Fx.Entity
        E.AddComponents(array{transform_component{Entity := E}, Fx})
        E.SetLocalTransform(Xf(V(0.0, 0.0, 60.0), One()))
        Parent.AddEntities(array{E})
        spawn{ RemoveLater(E, Life) }

    RemoveLater(E:entity, Life:float)<suspends>:void =
        Sleep(Life)
        E.RemoveFromParent()

    # ------------------------------------------------------------------ self-test
    AutoPlay()<suspends>:void =
        if (Root := Board?, P := GetPlayspace().GetPlayers()[0], C := P.GetFortCharacter[]):
            Print("[Floor] autoplay: walking the board")
            for (Y := 0..GridH - 1, X := 0..GridW - 1):
                Xs := if (Mod[Y, 2] = 0) then X else GridW - 1 - X   # snake order
                G := Root.GetGlobalTransform().Translation
                F := G.Forward + (Xs * 1.0 - (GridW - 1) * 0.5) * TileSize
                L := G.Left + (Y * 1.0 - (GridH - 1) * 0.5) * TileSize
                if (SGLabTeleport[C, F, -L, G.Up + 120.0, 180.0]) {}   # face -X so the camera looks across the board
                Sleep(0.35)
            # overlook: stand off the +X edge, raised, facing the board
            B := Root.GetGlobalTransform().Translation
            if (SGLabTeleport[C, B.Forward + GridW * TileSize * 0.5 + 500.0, -B.Left, B.Up + 400.0, 180.0]) {}
            Sleep(1.0)
            Print("[Floor] autoplay done: {LitCount} lit, round {RoundNo}")
