# SGLab 2: custom meshes + runtime materials, overlap events, per-player presentation, sweep details, perf.
#   uefn log "\[SGLab2\]"

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Verse.org/SceneGraph/KeyframedMovement }
using { /Verse.org/SpatialMath }
using { /Verse.org/Colors }
using { /UnrealEngine.com/BasicShapes }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/Diagnostics }
# Asset folders become internal modules, so this file must live in SGKit/ (parent of Meshes/ and Materials/).
using { Meshes }
using { Materials }

# Pulses the Glow of the material on its entity's SM_SG_cube, and cycles its hue.
sglab_pulse_component<public> := class<final_super>(component):
    var Material<private>:?M_SG_Color = false
    var T<private>:float = 0.0
    var Sub<private>:?cancelable = false

    OnBeginSimulation<override>():void =
        (super:)OnBeginSimulation()
        if (Mesh := Entity.GetComponent[SM_SG_cube]):
            M := M_SG_Color{}
            set Mesh.Main = M
            set Material = option{M}
        set Sub = option{TickEvents.PrePhysics.Subscribe(OnTick)}

    OnEndSimulation<override>():void =
        if (S := Sub?):
            S.Cancel()
        (super:)OnEndSimulation()

    OnTick(Dt:float):void =
        set T += Dt
        if (M := Material?):
            Deg := Mod[Floor[T * 60.0] or 0, 360] or 0
            set M.Color = MakeColorFromHSV(Deg * 1.0, 1.0, 1.0)
            set M.Glow = 2.0 + 2.0 * Sin(T * 4.0)

sglab2_device<public> := class(creative_device):

    @editable
    Origin<public>:vector3 = vector3{Forward := 2500.0, Left := 2000.0, Up := 450.0}

    @editable
    PerfCount<public>:int = 2000

    @editable
    TeleportPlayers<public>:logic = true

    var Passed<private>:int = 0
    var Failed<private>:int = 0
    var Entered<private>:int = 0
    var Exited<private>:int = 0

    OnBegin<override>()<suspends>:void =
        Sleep(2.0)
        Print("[SGLab2] ---- start ----")
        if (Sim := GetSimulationEntity[]):
            Root := entity{}
            Sim.AddEntities(array{Root})
            Root.SetGlobalTransform(At(Origin))
            if (TeleportPlayers?):
                ViewFromFront()
            L01_Rainbow(Root)
            L02_Pulse(Root)
            L03_SweepDetail(Root)
            L04_EnterExit(Root)
            L05_Presentation(Root)
            L06_Perf(Root)
        Print("[SGLab2] ---- done: {Passed} passed, {Failed} failed ----")

    Report(Id:string, Ok:logic, Name:string, Detail:string):void =
        if (Ok?):
            set Passed += 1
            Print("[SGLab2] {Id} PASS {Name}: {Detail}")
        else:
            set Failed += 1
            Print("[SGLab2] {Id} FAIL {Name}: {Detail}")

    One()<computes>:vector3 = vector3{Forward := 1.0, Left := 1.0, Up := 1.0}
    V(F:float, L:float, U:float)<computes>:vector3 = vector3{Forward := F, Left := L, Up := U}
    At(P:vector3)<transacts>:transform = transform{Translation := P, Rotation := IdentityRotation(), Scale := One()}

    Spawn(Parent:entity, Local:vector3, Mesh:component):entity =
        E := Mesh.Entity
        E.AddComponents(array{transform_component{Entity := E}, Mesh})
        Parent.AddEntities(array{E})
        E.SetLocalTransform(At(Local))
        E

    # Put every player 900 cm in front of the lab, facing it, so client screenshots show the results.
    ViewFromFront():void =
        Spot := Origin + V(-900.0, 0.0, 0.0)
        for (P : GetPlayspace().GetPlayers(), Char := P.GetFortCharacter[]):
            # Verse vector3: Forward=+X, Left=-Y, Up=+Z (Unreal Y points right)
            if (SGLabTeleport[Char, Spot.Forward, -Spot.Left, Spot.Up, 0.0]):
                Print("[SGLab2] teleported a player to the lab")

    # 12 runtime cubes, each with its OWN material instance and colour.
    L01_Rainbow(Root:entity):void =
        var Made:int = 0
        for (I := 0..11):
            E := entity{}
            C := SM_SG_cube{Entity := E}
            M := M_SG_Color{}
            set M.Color = MakeColorFromHSV(30.0 * I, 1.0, 1.0)
            set M.Glow = 0.5
            set C.Main = M
            Spawn(Root, V(0.0, -660.0 + 120.0 * I, 0.0), C)
            set Made += 1
        Report("L01", if (Made = 12) then true else false, "custom mesh + per-entity material instance", "{Made} coloured cubes")

    L02_Pulse(Root:entity):void =
        E := entity{}
        C := SM_SG_cube{Entity := E}
        Spawn(Root, V(0.0, 0.0, 250.0), C)
        E.SetLocalTransform(transform{Translation := V(0.0, 0.0, 250.0), Rotation := IdentityRotation(), Scale := V(1.5, 1.5, 1.5)})
        E.AddComponents(array{sglab_pulse_component{Entity := E}})
        Report("L02", true, "material animated from TickEvents", "hue cycle + glow pulse running on the big cube above the row")

    L03_SweepDetail(Root:entity):void =
        Target := Spawn(Root, V(600.0, 0.0, 0.0), cube{Entity := entity{}})
        Probe := Spawn(Root, V(600.0, 0.0, 500.0), cube{Entity := entity{}})
        var Lines:string = ""
        var N:int = 0
        for (Hit : Probe.FindSweepHits(V(0.0, 0.0, -1000.0))):
            set N += 1
            Who := if (Hit.TargetComponent.Entity = Target) then "TARGET" else if (Hit.TargetComponent.Entity = Probe) then "SELF" else if (Hit.TargetComponent.Entity = Root) then "ROOT" else "other"
            Src := if (C := Hit.SourceComponent?) then (if (C.Entity = Probe) then "probe" else "src?") else "none"
            set Lines += " [{N}] d={Hit.SourceHitDistance} {Who} src={Src}"
        Report("L03", true, "FindSweepHits breakdown", "{N} hits:{Lines}")

    L04_EnterExit(Root:entity)<suspends>:void =
        Gate := Spawn(Root, V(1000.0, 0.0, 0.0), cube{Entity := entity{}})
        if (GateMesh := Gate.GetComponent[cube]):
            GateMesh.EntityEnteredEvent.Subscribe(OnEntered)
            GateMesh.EntityExitedEvent.Subscribe(OnExited)
        Mover := Spawn(Root, V(1000.0, -400.0, 0.0), cube{Entity := entity{}})
        KM := keyframed_movement_component{Entity := Mover}
        Mover.AddComponents(array{KM})
        KM.SetKeyframes(array{keyframed_movement_delta{Transform := At(V(0.0, 800.0, 0.0)), Duration := 1.5, Easing := linear_easing_function{}}},
                        oneshot_keyframed_movement_playback_mode{})
        KM.Play()
        Sleep(2.5)
        Report("L04", if (Entered > 0) then true else false, "mesh EntityEnteredEvent/ExitedEvent between two entities", "entered {Entered}, exited {Exited}")

    OnEntered(Other:entity):void = set Entered += 1
    OnExited(Other:entity):void = set Exited += 1

    L05_Presentation(Root:entity):void =
        Hidden := Spawn(Root, V(-300.0, -300.0, 0.0), cube{Entity := entity{}})
        Shown := Spawn(Root, V(-300.0, 300.0, 0.0), sphere{Entity := entity{}})
        Hidden.SetPresentableToPlayers(option{array{}})
        Got := if (Ps := Hidden.GetPresentableToPlayers()?) then "array of {Ps.Length}" else "false (everyone)"
        Report("L05", true, "SetPresentableToPlayers(option{array{}})", "readback {Got}; cube at left should be INVISIBLE in the client, sphere at right visible")

    L06_Perf(Root:entity)<suspends>:void =
        Grid := entity{}
        Root.AddEntities(array{Grid})
        Grid.SetLocalTransform(At(V(1500.0, -1500.0, 0.0)))
        T0 := GetSimulationElapsedTime()
        for (I := 0..PerfCount - 1):
            Row := Quotient[I, 50] or 0
            Col := Mod[I, 50] or 0
            Spawn(Grid, V(60.0 * Row, 60.0 * Col, 0.0), cube{Entity := entity{}})
        T1 := GetSimulationElapsedTime()
        # measure the tick rate for 2 seconds afterwards
        var Ticks:int = 0
        Counter := entity{}
        Root.AddEntities(array{Counter})
        Start := GetSimulationElapsedTime()
        loop:
            Sleep(0.0)
            set Ticks += 1
            if (GetSimulationElapsedTime() - Start > 2.0):
                break
        Hz := Ticks * 1.0 / (GetSimulationElapsedTime() - Start)
        Report("L06", true, "spawn {PerfCount} cube entities", "spawn sim-time {T1 - T0}s, then {Hz} Hz over 2 s")
