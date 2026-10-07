# SGLab: runtime Scene Graph experiments. Place one in the level, start a session, then
#   uefn log "\[SGLab\]"
# Every experiment prints one line: [SGLab] Rxx PASS|FAIL <name>: <details>

using { /Verse.org/Simulation }
using { /Verse.org/Simulation/Tags }
using { /Verse.org/SceneGraph }
using { /Verse.org/SceneGraph/KeyframedMovement }
using { /Verse.org/SpatialMath }
using { /UnrealEngine.com/BasicShapes }
using { /Fortnite.com/Devices }
using { /UnrealEngine.com/Temporary/Diagnostics }

sglab_device<public> := class(creative_device):

    # World position of the lab area (cm, Verse axes: Forward = +X, Left = +Y, Up = +Z).
    @editable
    Origin<public>:vector3 = vector3{Forward := 2500.0, Left := 0.0, Up := 450.0}

    @editable
    SpawnCount<public>:int = 100

    var Passed<private>:int = 0
    var Failed<private>:int = 0

    OnBegin<override>()<suspends>:void =
        Sleep(2.0)
        Print("[SGLab] ---- start ----")
        if (Sim := GetSimulationEntity[]):
            Root := entity{}
            Sim.AddEntities(array{Root})
            Root.SetGlobalTransform(At(Origin))
            R01_Spawn(Root)
            R02_Tags(Root)
            R03_Overlap(Root)
            R04_Sweep(Root)
            R05_SceneEvents(Root)
            R06_Reparent(Root)
            R07_ManySpawn(Root)
            R08_Remove(Root)
            R09_Keyframes(Root)
            R10_TickRate(Root)
            R11_Light(Root)
        else:
            Report("R00", false, "GetSimulationEntity", "no simulation entity")
        Print("[SGLab] ---- done: {Passed} passed, {Failed} failed ----")

    # ------------------------------------------------------------ helpers
    Report(Id:string, Ok:logic, Name:string, Detail:string):void =
        if (Ok?):
            set Passed += 1
            Print("[SGLab] {Id} PASS {Name}: {Detail}")
        else:
            set Failed += 1
            Print("[SGLab] {Id} FAIL {Name}: {Detail}")

    One():vector3 = vector3{Forward := 1.0, Left := 1.0, Up := 1.0}

    At(P:vector3):transform = transform{Translation := P, Rotation := IdentityRotation(), Scale := One()}

    V(F:float, L:float, U:float):vector3 = vector3{Forward := F, Left := L, Up := U}

    # A cube entity under Parent at a LOCAL offset.
    SpawnCube(Parent:entity, Local:vector3):entity =
        E := entity{}
        E.AddComponents(array{transform_component{Entity := E}, cube{Entity := E}})
        Parent.AddEntities(array{E})
        E.SetLocalTransform(At(Local))
        E

    Fmt(P:vector3):string = "({P.Forward}, {P.Left}, {P.Up})"

    # ------------------------------------------------------------ experiments
    R01_Spawn(Root:entity):void =
        E := SpawnCube(Root, V(0.0, 0.0, 0.0))
        G := E.GetGlobalTransform().Translation
        Meshes := for (M : Root.FindDescendantComponents(mesh_component)) {M}
        Ok := if (Distance(G, Origin) < 1.0, Meshes.Length = 1) then true else false
        Report("R01", Ok, "spawn entity+cube at runtime", "global {Fmt(G)} meshes under root {Meshes.Length}")

    R02_Tags(Root:entity):void =
        A := SpawnCube(Root, V(0.0, 300.0, 0.0))
        B := SpawnCube(Root, V(0.0, 600.0, 0.0))
        A.AddTag(sglab_red_tag{})
        B.AddTag(sglab_tag{})
        Base := for (T : Root.FindDescendantEntitiesWithTag(sglab_tag)) {T}
        Red := for (T : Root.FindDescendantEntitiesWithTag(sglab_red_tag)) {T}
        HasA := if (A.ContainsTag[sglab_tag]) then "yes" else "no"
        Ok := if (Base.Length = 2, Red.Length = 1) then true else false
        Report("R02", Ok, "tags + hierarchy query", "with base tag {Base.Length} (want 2), red {Red.Length} (want 1), A has base via subclass: {HasA}")

    R03_Overlap(Root:entity):void =
        A := SpawnCube(Root, V(400.0, 0.0, 0.0))
        B := SpawnCube(Root, V(450.0, 0.0, 0.0))  # cubes are 100 cm: 50 cm overlap
        var Count:int = 0
        var HitsB:int = 0
        for (Hit : A.FindOverlapHits()):
            set Count += 1
            if (Hit.TargetComponent.Entity = B):
                set HitsB += 1
        Ok := if (HitsB > 0) then true else false
        Report("R03", Ok, "FindOverlapHits", "hits {Count}, of which on B {HitsB}")

    R04_Sweep(Root:entity):void =
        Floor := SpawnCube(Root, V(800.0, 0.0, 0.0))
        Probe := SpawnCube(Root, V(800.0, 0.0, 500.0))
        var First:string = "none"
        var N:int = 0
        for (Hit : Probe.FindSweepHits(V(0.0, 0.0, -1000.0))):
            set N += 1
            if (N = 1):
                IsFloor := if (Hit.TargetComponent.Entity = Floor) then "yes" else "no"
                set First = "dist {Hit.SourceHitDistance} normal {Fmt(Hit.ContactNormal)} isFloor {IsFloor}"
        Report("R04", if (N > 0) then true else false, "FindSweepHits down 1000", "{N} hits; first {First}")

    R05_SceneEvents(Root:entity):void =
        Parent := SpawnCube(Root, V(1100.0, 0.0, 0.0))
        Child := SpawnCube(Parent, V(0.0, 0.0, 150.0))
        L1 := sglab_listener_component{Entity := Parent}
        L2 := sglab_listener_component{Entity := Child}
        Parent.AddComponents(array{L1})
        Child.AddComponents(array{L2})
        Down := Parent.SendDown(sglab_ping_event{Payload := "down"})
        Up := Child.SendUp(sglab_ping_event{Payload := "up"})
        Ok := if (L1.Received = 2, L2.Received = 2) then true else false
        DownN := if (Down?) then 1 else 0
        UpN := if (Up?) then 1 else 0
        Report("R05", Ok, "SendDown/SendUp + OnReceive", "parent got {L1.Received}, child got {L2.Received} (want 2/2); consumed down={DownN} up={UpN}")

    R06_Reparent(Root:entity):void =
        P1 := SpawnCube(Root, V(1400.0, 0.0, 0.0))
        P2 := SpawnCube(Root, V(1400.0, 500.0, 300.0))
        C := SpawnCube(P1, V(0.0, 0.0, 150.0))
        Before := C.GetGlobalTransform().Translation
        P2.AddEntities(array{C})
        After := C.GetGlobalTransform().Translation
        LocalAfter := C.GetLocalTransform().Translation
        Kept := if (Distance(Before, After) < 1.0) then "GLOBAL kept" else "LOCAL kept"
        Report("R06", true, "re-parent with AddEntities", "{Kept}: global before {Fmt(Before)} after {Fmt(After)} local after {Fmt(LocalAfter)}")

    R07_ManySpawn(Root:entity):void =
        Grid := entity{}
        Root.AddEntities(array{Grid})
        Grid.SetLocalTransform(At(V(0.0, -1500.0, 0.0)))
        T0 := GetSimulationElapsedTime()
        for (I := 0..SpawnCount - 1):
            Row := Quotient[I, 10] or 0
            Col := Mod[I, 10] or 0
            SpawnCube(Grid, V(150.0 * Row, 150.0 * Col, 0.0))
        N := for (M : Grid.FindDescendantComponents(mesh_component)) {M}
        Report("R07", if (N.Length = SpawnCount) then true else false, "spawn {SpawnCount} cubes in one frame", "{N.Length} meshes, sim time delta {GetSimulationElapsedTime() - T0}")

    R08_Remove(Root:entity):void =
        E := SpawnCube(Root, V(1700.0, 0.0, 0.0))
        E.RemoveFromParent()
        Gone := if (E.GetParent[]) then "still parented" else "no parent"
        Root.AddEntities(array{E})
        Back := if (E.GetParent[]) then "re-added" else "not re-added"
        Report("R08", true, "RemoveFromParent + re-add", "{Gone}, {Back}")

    R09_Keyframes(Root:entity)<suspends>:void =
        E := SpawnCube(Root, V(2000.0, 0.0, 0.0))
        KM := keyframed_movement_component{Entity := E}
        E.AddComponents(array{KM})
        Up := keyframed_movement_delta{
            Transform := transform{Translation := V(0.0, 0.0, 300.0), Rotation := MakeRotationFromYawPitchRollDegrees(90.0, 0.0, 0.0), Scale := One()},
            Duration := 1.0,
            Easing := ease_in_out_cubic_bezier_easing_function{}}
        Side := keyframed_movement_delta{
            Transform := transform{Translation := V(0.0, 300.0, 0.0), Rotation := IdentityRotation(), Scale := One()},
            Duration := 1.0,
            Easing := linear_easing_function{}}
        Start := E.GetGlobalTransform().Translation
        KM.SetKeyframes(array{Up, Side}, oneshot_keyframed_movement_playback_mode{})
        KM.Play()
        race:
            KM.FinishedEvent.Await()
            Sleep(5.0)
        End := E.GetGlobalTransform().Translation
        D := End - Start
        Ok := if (Distance(D, V(0.0, 300.0, 300.0)) < 5.0) then true else false
        Report("R09", Ok, "keyframed movement oneshot (+300 up then +300 left)", "moved {Fmt(D)}")
        # leave one looping for the screenshot
        E2 := SpawnCube(Root, V(2300.0, 0.0, 0.0))
        KM2 := keyframed_movement_component{Entity := E2}
        E2.AddComponents(array{KM2})
        KM2.SetKeyframes(array{Up}, pingpong_keyframed_movement_playback_mode{})
        KM2.Play()

    R10_TickRate(Root:entity)<suspends>:void =
        E := entity{}
        Counter := sglab_tick_counter_component{Entity := E}
        E.AddComponents(array{Counter})
        Root.AddEntities(array{E})
        Sleep(3.0)
        Hz := if (Counter.Elapsed > 0.0) then Counter.Ticks * 1.0 / Counter.Elapsed else 0.0
        Report("R10", if (Counter.Ticks > 0) then true else false, "TickEvents.PrePhysics", "{Counter.Ticks} ticks in {Counter.Elapsed}s = {Hz} Hz")

    R11_Light(Root:entity):void =
        E := SpawnCube(Root, V(2600.0, 0.0, 200.0))
        L := sphere_light_component{Entity := E}
        E.AddComponents(array{L})
        set L.Intensity = 5000.0
        set L.CastShadows = false
        Lights := for (X : Root.FindDescendantComponents(light_component)) {X}
        Report("R11", if (Lights.Length = 1) then true else false, "runtime sphere_light_component", "lights under root {Lights.Length}")
