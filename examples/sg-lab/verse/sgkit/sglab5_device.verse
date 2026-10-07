# SGLab 5: item entities (world + inventory) and Scene Graph cameras.
#   uefn log "\[SGLab5\]"

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Verse.org/SpatialMath }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Items }
using { /UnrealEngine.com/Itemization }
using { /UnrealEngine.com/Temporary/Diagnostics }

sglab5_device<public> := class(creative_device):

    @editable
    Origin<public>:vector3 = vector3{Forward := -2500.0, Left := 0.0, Up := 400.0}

    @editable
    TryCamera<public>:logic = true

    OnBegin<override>()<suspends>:void =
        Sleep(3.0)
        Print("[SGLab5] ---- start ----")
        if (Sim := GetSimulationEntity[]):
            for (P : GetPlayspace().GetPlayers()):
                C01_PlayerComponents(P)
                C02_GiveItem(P)
            C03_WorldItem(Sim)
            if (TryCamera?):
                for (P : GetPlayspace().GetPlayers()):
                    C04_Camera(Sim, P)
        Print("[SGLab5] ---- done ----")

    V(F:float, L:float, U:float)<computes>:vector3 = vector3{Forward := F, Left := L, Up := U}
    One()<computes>:vector3 = vector3{Forward := 1.0, Left := 1.0, Up := 1.0}

    C01_PlayerComponents(P:player):void =
        Invs := for (I : P.FindDescendantComponents(inventory_component)) {I}
        var Items:int = 0
        for (I : Invs):
            set Items += I.GetItems().Length
        Kids := P.GetEntities()
        Print("[SGLab5] C01 player: {P.GetComponents().Length} components, {Kids.Length} child entities, {Invs.Length} inventory components, {Items} items")
        for (K : Kids):
            KInvs := for (I : K.FindDescendantComponents(inventory_component)) {I}
            Print("[SGLab5]   child entity: {K.GetComponents().Length} comps, {KInvs.Length} inventories")

    C02_GiveItem(P:player):void =
        Invs := for (I : P.FindDescendantComponents(inventory_component)) {I}   # generators have no First/indexing
        if (Inv := Invs[0]):
            Apple := Apple_BR_CH1S4_Common{}
            Res := Inv.AddItemDistribute(Apple)
            Ok := if (Res.GetSuccess[]) then "SUCCESS" else "FAILED"
            Errs := if (E := Res.GetError[]) then "{E.Length} errors" else "no errors"
            Print("[SGLab5] C02 AddItemDistribute(Apple) -> {Ok} ({Errs}); apple parent? {if (Apple.GetParent[]) then "yes" else "no"}")
        else:
            Print("[SGLab5] C02 no inventory_component under the player")

    C03_WorldItem(Sim:entity):void =
        Item := Bandage_BR_CH5S1_Common{}
        Item.SetLocalTransform(transform{Translation := Origin + V(600.0, 0.0, 100.0), Rotation := IdentityRotation(), Scale := One()})
        Sim.AddEntities(array{Item})
        Comps := Item.GetComponents()
        Kids := Item.GetEntities()
        Pos := Item.GetGlobalTransform().Translation
        Print("[SGLab5] C03 bandage entity in world: {Comps.Length} components, {Kids.Length} children, at ({Pos.Forward}, {Pos.Left}, {Pos.Up})")

    C04_Camera(Sim:entity, P:player)<suspends>:void =
        Directors := for (D : P.FindDescendantComponents(camera_director_component)) {D}
        Print("[SGLab5] C04 camera directors under player: {Directors.Length}")
        if (Director := Directors[0]):
            CamE := entity{}
            Cam := perspective_camera_component{Entity := CamE}
            CamE.AddComponents(array{transform_component{Entity := CamE}, Cam})
            # high above the floor-game board, looking straight down
            CamE.SetLocalTransform(transform{Translation := Origin + V(0.0, 0.0, 1800.0),
                                             Rotation := MakeRotationFromYawPitchRollDegrees(0.0, -89.0, 0.0), Scale := One()})
            Sim.AddEntities(array{CamE})
            set Cam.FieldOfViewDegrees = 70.0
            if (Handle := Director.AddCamera[Cam, 100]):
                Print("[SGLab5] C04 AddCamera succeeded; holding for 12 s")
                Sleep(12.0)
                Handle.Cancel()
                Print("[SGLab5] C04 camera released")
            else:
                Print("[SGLab5] C04 AddCamera FAILED")
