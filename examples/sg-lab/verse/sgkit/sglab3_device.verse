# SGLab 3: players as entities, mesh triggers with players, sweep/overlap deep-dive, enter/exit timing.
#   uefn log "\[SGLab3\]"

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Verse.org/SceneGraph/KeyframedMovement }
using { /Verse.org/SpatialMath }
using { /Verse.org/Colors }
using { /UnrealEngine.com/BasicShapes }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { Meshes }
using { Materials }

sglab3_device<public> := class(creative_device):

    @editable
    Origin<public>:vector3 = vector3{Forward := 2500.0, Left := -2500.0, Up := 450.0}

    var Passed<private>:int = 0
    var Failed<private>:int = 0
    var PadEvents<private>:[]string = array{}
    var GateLog<private>:[]string = array{}

    OnBegin<override>()<suspends>:void =
        Sleep(3.0)
        Print("[SGLab3] ---- start ----")
        if (Sim := GetSimulationEntity[]):
            Root := entity{}
            Sim.AddEntities(array{Root})
            Root.SetGlobalTransform(At(Origin))
            P01_PlayerIsEntity()
            P02_HaloOnPlayer()
            P03_PlayerTrigger(Root)
            P04_SweepDeep(Root)
            P05_GateTiming(Root)
            P06_OverlapVolume(Root)
        Print("[SGLab3] ---- done: {Passed} passed, {Failed} failed ----")

    Report(Id:string, Ok:logic, Name:string, Detail:string):void =
        if (Ok?):
            set Passed += 1
            Print("[SGLab3] {Id} PASS {Name}: {Detail}")
        else:
            set Failed += 1
            Print("[SGLab3] {Id} FAIL {Name}: {Detail}")

    One()<computes>:vector3 = vector3{Forward := 1.0, Left := 1.0, Up := 1.0}
    V(F:float, L:float, U:float)<computes>:vector3 = vector3{Forward := F, Left := L, Up := U}
    At(P:vector3)<transacts>:transform = transform{Translation := P, Rotation := IdentityRotation(), Scale := One()}
    Fmt(P:vector3)<transacts>:string = "({Floor[P.Forward] or 0}, {Floor[P.Left] or 0}, {Floor[P.Up] or 0})"

    Spawn(Parent:entity, Local:vector3, Mesh:component):entity =
        E := Mesh.Entity
        E.AddComponents(array{transform_component{Entity := E}, Mesh})
        Parent.AddEntities(array{E})
        E.SetLocalTransform(At(Local))
        E

    Colored(Parent:entity, Local:vector3, Hue:float):entity =
        E := entity{}
        C := SM_SG_sphere{Entity := E}
        M := M_SG_Color{}
        set M.Color = MakeColorFromHSV(Hue, 1.0, 1.0)
        set M.Glow = 3.0
        set C.Main = M
        Spawn(Parent, Local, C)

    # ---------------------------------------------------------------- players are entities?
    P01_PlayerIsEntity():void =
        var Lines:string = ""
        for (P : GetPlayspace().GetPlayers()):
            G := P.GetGlobalTransform().Translation
            Comps := P.GetComponents()
            Kids := P.GetEntities()
            CharPos := if (C := P.GetFortCharacter[]) then "UE{SGLabCharPos(C)}" else "no char"
            Parent := if (P.GetParent[]) then "has parent" else "no parent"
            set Lines += " entity-global {Fmt(G)} char {CharPos} comps {Comps.Length} children {Kids.Length} {Parent};"
        Report("P01", true, "player as entity", Lines)

    P02_HaloOnPlayer():void =
        var N:int = 0
        for (P : GetPlayspace().GetPlayers()):
            Halo := Colored(P, V(0.0, 0.0, 220.0), 50.0)
            set N += 1
            L := sphere_light_component{Entity := Halo}
            Halo.AddComponents(array{L})
            set L.Intensity = 3000.0
            set L.CastShadows = false
            Print("[SGLab3] halo global {Fmt(Halo.GetGlobalTransform().Translation)}")
        Report("P02", if (N > 0) then true else false, "child entity (glowing sphere + light) parented to the player", "{N} halos; client screenshot should show a gold orb above the head")

    # ---------------------------------------------------------------- player walks into a mesh trigger
    P03_PlayerTrigger(Root:entity)<suspends>:void =
        Pad := Colored(Root, V(0.0, 0.0, -40.0), 120.0)
        Pad.SetLocalTransform(transform{Translation := V(0.0, 0.0, -40.0), Rotation := IdentityRotation(), Scale := V(3.0, 3.0, 0.3)})
        if (PadMesh := Pad.GetComponent[SM_SG_sphere]):
            set PadMesh.Collidable = false
            PadMesh.EntityEnteredEvent.Subscribe(OnPadEnter)
            PadMesh.EntityExitedEvent.Subscribe(OnPadExit)
        Sleep(0.5)
        # teleport every player onto the pad, then away again
        for (P : GetPlayspace().GetPlayers(), C := P.GetFortCharacter[]):
            G := Pad.GetGlobalTransform().Translation
            if (SGLabTeleport[C, G.Forward, -G.Left, G.Up + 60.0, 0.0]) {}
        Sleep(2.0)
        for (P : GetPlayspace().GetPlayers(), C := P.GetFortCharacter[]):
            G := Pad.GetGlobalTransform().Translation
            if (SGLabTeleport[C, G.Forward - 900.0, -G.Left, G.Up + 60.0, 0.0]) {}
        Sleep(1.0)
        var Joined:string = ""
        for (S : PadEvents):
            set Joined += " " + S
        Report("P03", if (PadEvents.Length > 0) then true else false, "mesh EntityEnteredEvent with a player (teleported onto a non-collidable pad)", "{PadEvents.Length} events:{Joined}")

    OnPadEnter(Other:entity):void =
        Kind := if (player[Other]) then "PLAYER" else if (agent[Other]) then "AGENT" else "entity"
        set PadEvents += array{"enter:{Kind}@{GetSimulationElapsedTime()}"}

    OnPadExit(Other:entity):void =
        Kind := if (player[Other]) then "PLAYER" else if (agent[Other]) then "AGENT" else "entity"
        set PadEvents += array{"exit:{Kind}@{GetSimulationElapsedTime()}"}

    # ---------------------------------------------------------------- sweep: what are those distance-0 hits?
    P04_SweepDeep(Root:entity):void =
        Target := Spawn(Root, V(600.0, 0.0, 0.0), cube{Entity := entity{}})
        Probe := Spawn(Root, V(600.0, 0.0, 500.0), cube{Entity := entity{}})
        var Lines:string = ""
        var N:int = 0
        for (Hit : Probe.FindSweepHits(V(0.0, 0.0, -1000.0))):
            set N += 1
            Who := if (Hit.TargetComponent.Entity = Target) then "TARGET" else if (Hit.TargetComponent.Entity = Probe) then "SELF" else "other"
            TPos := Fmt(Hit.TargetComponent.Entity.GetGlobalTransform().Translation)
            set Lines += " [{N}] {Who} at {TPos} d={Hit.SourceHitDistance} move={Fmt(Hit.SourceHitTranslation)} contact={Fmt(Hit.ContactPosition)}"
        Report("P04", true, "FindSweepHits per-hit detail (probe at {Fmt(Probe.GetGlobalTransform().Translation)})", "{N} hits:{Lines}")
        # same sweep with an explicit sphere volume from a transform
        var M:int = 0
        var Lines2:string = ""
        Start := transform{Translation := Probe.GetGlobalTransform().Translation, Rotation := IdentityRotation(), Scale := One()}
        for (Hit : Root.FindSweepHits(V(0.0, 0.0, -1000.0), Start, collision_sphere{Radius := 20.0})):
            set M += 1
            Who := if (Hit.TargetComponent.Entity = Target) then "TARGET" else if (Hit.TargetComponent.Entity = Probe) then "SELF" else "other"
            set Lines2 += " [{M}] {Who} d={Hit.SourceHitDistance} contact={Fmt(Hit.ContactPosition)}"
        Report("P04b", true, "FindSweepHits with a collision_sphere volume", "{M} hits:{Lines2}")

    # ---------------------------------------------------------------- enter/exit flicker timing
    P05_GateTiming(Root:entity)<suspends>:void =
        Gate := Spawn(Root, V(1000.0, 0.0, 0.0), cube{Entity := entity{}})
        if (GateMesh := Gate.GetComponent[cube]):
            set GateMesh.Collidable = false
            GateMesh.EntityEnteredEvent.Subscribe(OnGateEnter)
            GateMesh.EntityExitedEvent.Subscribe(OnGateExit)
        Mover := Spawn(Root, V(1000.0, -400.0, 0.0), cube{Entity := entity{}})
        if (MoverMesh := Mover.GetComponent[cube]):
            set MoverMesh.Collidable = false
        KM := keyframed_movement_component{Entity := Mover}
        Mover.AddComponents(array{KM})
        KM.SetKeyframes(array{keyframed_movement_delta{Transform := At(V(0.0, 800.0, 0.0)), Duration := 2.0, Easing := linear_easing_function{}}},
                        oneshot_keyframed_movement_playback_mode{})
        KM.Play()
        Sleep(3.0)
        var Joined:string = ""
        for (S : GateLog):
            set Joined += " " + S
        Report("P05", true, "enter/exit timeline, both non-collidable", "{GateLog.Length} events:{Joined}")

    OnGateEnter(Other:entity):void =
        set GateLog += array{"in@{GetSimulationElapsedTime()}"}

    OnGateExit(Other:entity):void =
        set GateLog += array{"out@{GetSimulationElapsedTime()}"}

    # ---------------------------------------------------------------- overlap query with a free volume
    P06_OverlapVolume(Root:entity):void =
        A := Spawn(Root, V(1400.0, 0.0, 0.0), cube{Entity := entity{}})
        B := Spawn(Root, V(1400.0, 300.0, 0.0), cube{Entity := entity{}})
        var Near:int = 0
        var Total:int = 0
        Center := transform{Translation := A.GetGlobalTransform().Translation, Rotation := IdentityRotation(), Scale := One()}
        for (Hit : Root.FindOverlapHits(Center, collision_sphere{Radius := 200.0})):
            set Total += 1
            if (Hit.TargetComponent.Entity = A):
                set Near += 1
        var Far:int = 0
        for (Hit : Root.FindOverlapHits(Center, collision_sphere{Radius := 400.0})):
            if (Hit.TargetComponent.Entity = B):
                set Far += 1
        Report("P06", if (Near = 1, Far = 1) then true else false, "FindOverlapHits(transform, collision_sphere)", "r200: {Total} hits, A {Near}; r400: B {Far}")
