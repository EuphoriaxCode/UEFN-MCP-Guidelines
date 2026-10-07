# SGLab 4: verify the one-tick collision lag, find a spawn pattern without it, and follow a player.
#   uefn log "\[SGLab4\]"

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Verse.org/SpatialMath }
using { /Verse.org/Colors }
using { /UnrealEngine.com/BasicShapes }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { Meshes }
using { Materials }

# Keeps its entity hovering above one player's character (player entities are not spatial, so follow by hand).
sglab_follow_component<public> := class<final_super>(component):
    var Target<public>:?fort_character = false
    var Offset<public>:vector3 = vector3{Forward := 0.0, Left := 0.0, Up := 230.0}
    var Sub<private>:?cancelable = false
    var Ticks<public>:int = 0

    OnBeginSimulation<override>():void =
        (super:)OnBeginSimulation()
        set Sub = option{TickEvents.PostPhysics.Subscribe(OnTick)}

    OnEndSimulation<override>():void =
        if (S := Sub?):
            S.Cancel()
        (super:)OnEndSimulation()

    OnTick(Dt:float):void =
        if (C := Target?):
            Here := SGLabCharVec(C)
            Entity.SetGlobalTransform(transform{Translation := Here + Offset, Rotation := IdentityRotation(), Scale := vector3{Forward := 1.0, Left := 1.0, Up := 1.0}})
            set Ticks += 1

sglab4_device<public> := class(creative_device):

    @editable
    Origin<public>:vector3 = vector3{Forward := 2500.0, Left := -5000.0, Up := 450.0}

    var Passed<private>:int = 0
    var Failed<private>:int = 0

    OnBegin<override>()<suspends>:void =
        Sleep(4.0)
        Print("[SGLab4] ---- start ----")
        if (Sim := GetSimulationEntity[]):
            Root := entity{}
            Sim.AddEntities(array{Root})
            Root.SetGlobalTransform(At(Origin))
            Q01_LagThenWait(Root)
            Q02_TransformBeforeAdd(Root)
            Q03_SweepAfterWait(Root)
            Q04_FollowPlayer(Root)
        Print("[SGLab4] ---- done: {Passed} passed, {Failed} failed ----")

    Report(Id:string, Ok:logic, Name:string, Detail:string):void =
        if (Ok?):
            set Passed += 1
            Print("[SGLab4] {Id} PASS {Name}: {Detail}")
        else:
            set Failed += 1
            Print("[SGLab4] {Id} FAIL {Name}: {Detail}")

    One()<computes>:vector3 = vector3{Forward := 1.0, Left := 1.0, Up := 1.0}
    V(F:float, L:float, U:float)<computes>:vector3 = vector3{Forward := F, Left := L, Up := U}
    At(P:vector3)<transacts>:transform = transform{Translation := P, Rotation := IdentityRotation(), Scale := One()}
    Fmt(P:vector3)<transacts>:string = "({Floor[P.Forward] or 0}, {Floor[P.Left] or 0}, {Floor[P.Up] or 0})"

    # the usual pattern: add first, then set the local transform
    SpawnAfter(Parent:entity, Local:vector3):entity =
        E := entity{}
        E.AddComponents(array{transform_component{Entity := E}, cube{Entity := E}})
        Parent.AddEntities(array{E})
        E.SetLocalTransform(At(Local))
        E

    # alternative: set the GLOBAL transform before the entity enters the scene
    SpawnBefore(Parent:entity, Local:vector3):entity =
        E := entity{}
        E.AddComponents(array{transform_component{Entity := E}, cube{Entity := E}})
        E.SetGlobalTransform(At(Parent.GetGlobalTransform().Translation + Local))
        Parent.AddEntities(array{E})
        E

    CountAt(Root:entity, Who:entity, Radius:float):int =
        var N:int = 0
        Center := transform{Translation := Who.GetGlobalTransform().Translation, Rotation := IdentityRotation(), Scale := One()}
        for (Hit : Root.FindOverlapHits(Center, collision_sphere{Radius := Radius})):
            if (Hit.TargetComponent.Entity = Who):
                set N += 1
        N

    Q01_LagThenWait(Root:entity)<suspends>:void =
        A := SpawnAfter(Root, V(0.0, 0.0, 0.0))
        B := SpawnAfter(Root, V(400.0, 0.0, 0.0))
        Now := CountAt(Root, B, 60.0)
        Sleep(0.0)
        Next := CountAt(Root, B, 60.0)
        Sleep(0.1)
        Later := CountAt(Root, B, 60.0)
        Report("Q01", if (Next > 0 or Later > 0) then true else false, "overlap query finds a just-moved entity only after a tick",
            "same frame {Now}, after Sleep(0) {Next}, after 0.1 s {Later}")

    Q02_TransformBeforeAdd(Root:entity)<suspends>:void =
        C := SpawnBefore(Root, V(800.0, 0.0, 0.0))
        Now := CountAt(Root, C, 60.0)
        Pos := Fmt(C.GetGlobalTransform().Translation)
        Sleep(0.0)
        Next := CountAt(Root, C, 60.0)
        Report("Q02", if (Now > 0) then true else false, "SetGlobalTransform BEFORE AddEntities avoids the lag",
            "same frame {Now}, after Sleep(0) {Next}, at {Pos}")

    Q03_SweepAfterWait(Root:entity)<suspends>:void =
        Target := SpawnAfter(Root, V(1200.0, 0.0, 0.0))
        Probe := SpawnAfter(Root, V(1200.0, 0.0, 500.0))
        Sleep(0.1)
        var Lines:string = ""
        for (Hit : Probe.FindSweepHits(V(0.0, 0.0, -1000.0))):
            Who := if (Hit.TargetComponent.Entity = Target) then "TARGET" else "other"
            set Lines += " {Who} d={Hit.SourceHitDistance} contact={Fmt(Hit.ContactPosition)} n={Fmt(Hit.ContactNormal * 100.0)}"
        Report("Q03", true, "FindSweepHits after the bodies settled (expect TARGET at d=400)", Lines)

    Q04_FollowPlayer(Root:entity)<suspends>:void =
        var Made:int = 0
        for (P : GetPlayspace().GetPlayers(), C := P.GetFortCharacter[]):
            Orb := entity{}
            Mesh := SM_SG_sphere{Entity := Orb}
            M := M_SG_Color{}
            set M.Color = MakeColorFromHSV(280.0, 1.0, 1.0)
            set M.Glow = 4.0
            set Mesh.Main = M
            Follow := sglab_follow_component{Entity := Orb}
            set Follow.Target = option{C}
            L := sphere_light_component{Entity := Orb}
            Orb.AddComponents(array{transform_component{Entity := Orb}, Mesh, L, Follow})
            set L.Intensity = 2000.0
            set L.CastShadows = false
            Root.AddEntities(array{Orb})
            set Made += 1
            Sleep(1.0)
            Gap := Distance(Orb.GetGlobalTransform().Translation, SGLabCharVec(C) + V(0.0, 0.0, 230.0))
            Report("Q04", if (Gap < 50.0) then true else false, "orb follows the character via TickEvents.PostPhysics",
                "gap {Gap} cm after {Follow.Ticks} ticks")
        if (Made = 0):
            Report("Q04", false, "orb follows the character", "no player with a character")
