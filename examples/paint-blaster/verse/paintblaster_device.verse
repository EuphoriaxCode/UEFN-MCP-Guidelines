# Paint Blaster: press Jump (or WeaponPrimary when the ranged mapping is active) to fire a glowing paint ball.
# The ball is a Scene Graph entity integrated by hand every PostPhysics tick with FindSweepHits; whatever
# custom-mesh entity it hits gets a NEW material instance in the ball's colour, plus a Niagara burst.
#
# Lives in SGKit/ (needs Meshes/, Materials/, VFX/). Helpers SGLabViewRay/SGLabTeleport from sglab_teleport.verse.
#   uefn log "\[Paint\]"

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Verse.org/SpatialMath }
using { /Verse.org/Colors }
using { /Verse.org/Random }
using { /Verse.org/Input }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Input/Character }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { Meshes }
using { Materials }
using { VFX }

# Recolours any of our kit meshes on an entity. Returns true if something was painted.
PaintEntity(E:entity, C:color)<transacts>:logic =
    var Painted:logic = false
    if (M := E.GetComponent[SM_SG_cube]):
        Mat := M_SG_Color{}
        set Mat.Color = C
        set Mat.Glow = 1.0
        set M.Main = Mat
        set Painted = true
    if (M := E.GetComponent[SM_SG_sphere]):
        Mat := M_SG_Color{}
        set Mat.Color = C
        set Mat.Glow = 1.0
        set M.Main = Mat
        set Painted = true
    if (M := E.GetComponent[SM_SG_cylinder]):
        Mat := M_SG_Color{}
        set Mat.Color = C
        set Mat.Glow = 1.0
        set M.Main = Mat
        set Painted = true
    if (M := E.GetComponent[SM_SG_torus]):
        Mat := M_SG_Color{}
        set Mat.Color = C
        set Mat.Glow = 1.0
        set M.Main = Mat
        set Painted = true
    if (M := E.GetComponent[SM_SG_wedge]):
        Mat := M_SG_Color{}
        set Mat.Color = C
        set Mat.Glow = 1.0
        set M.Main = Mat
        set Painted = true
    Painted

paint_ball_component<public> := class<final_super>(component):
    var Velocity<public>:vector3 = vector3{Forward := 0.0, Left := 0.0, Up := 0.0}
    var Paint<public>:color = NamedColors.White
    var Life<public>:float = 3.0
    var Owner<public>:?paintblaster_device = false
    var Sub<private>:?cancelable = false
    var Age<private>:float = 0.0
    var Done<private>:logic = false

    OnBeginSimulation<override>():void =
        (super:)OnBeginSimulation()
        set Sub = option{TickEvents.PostPhysics.Subscribe(OnTick)}

    OnEndSimulation<override>():void =
        if (S := Sub?):
            S.Cancel()
        (super:)OnEndSimulation()

    OnTick(Dt:float):void =
        if (Done?):
            return
        set Age += Dt
        Step := Velocity * Dt
        var Hit:?sweep_hit = false
        for (H : Entity.FindSweepHits(Step), not Hit?, H.TargetComponent.Entity <> Entity):
            set Hit = option{H}
        if (H := Hit?):
            set Done = true
            Target := H.TargetComponent.Entity
            Painted := PaintEntity(Target, Paint)
            if (O := Owner?):
                O.OnBallHit(Entity, H.ContactPosition, Painted)
        else if (Age > Life):
            set Done = true
            Entity.RemoveFromParent()
        else:
            T := Entity.GetGlobalTransform()
            Entity.SetGlobalTransform(transform{Translation := T.Translation + Step, Rotation := T.Rotation, Scale := T.Scale})

paintblaster_device<public> := class(creative_device):

    @editable
    Speed<public>:float = 3000.0

    # Self-test without a human: fire from a fixed spot at the KitDemo shapes every second.
    @editable
    AutoFire<public>:logic = true

    @editable
    AutoFireFrom<public>:vector3 = vector3{Forward := 0.0, Left := 2500.0, Up := 450.0}

    @editable
    AutoFireAt<public>:vector3 = vector3{Forward := -450.0, Left := 1600.0, Up := 444.0}

    var Shots<private>:int = 0
    var Hits<private>:int = 0
    var Painted<private>:int = 0
    var Root<private>:?entity = false

    OnBegin<override>()<suspends>:void =
        if (Sim := GetSimulationEntity[]):
            R := entity{}
            Sim.AddEntities(array{R})
            set Root = option{R}
        for (P : GetPlayspace().GetPlayers()):
            Hook(P)
        GetPlayspace().PlayerAddedEvent().Subscribe(Hook)
        if (AutoFire?):
            Sleep(3.0)
            Targets := array{V(-450.0, 1600.0, 444.0), V(-150.0, 1600.0, 444.0), V(150.0, 1600.0, 444.0), V(450.0, 1600.0, 444.0)}
            for (I := 0..7):
                if (T := Targets[Mod[I, 4] or 0]):
                    Dir := (T - AutoFireFrom).MakeUnitVector()
                    Fire(AutoFireFrom, Dir)
                Sleep(0.8)
            Sleep(2.0)
            Print("[Paint] autofire summary: {Shots} shots, {Hits} hits, {Painted} painted")

    V(F:float, L:float, U:float)<computes>:vector3 = vector3{Forward := F, Left := L, Up := U}

    Hook(P:player):void =
        if (PI := GetPlayerInput[P]):
            PI.GetInputEvents(Jump).TriggerActivationEvent.Subscribe(OnJump)
            PI.GetInputEvents(WeaponPrimary).TriggerActivationEvent.Subscribe(OnPrimary)
            Print("[Paint] input hooked for a player (Jump + WeaponPrimary)")

    OnJump(Event:tuple(player, logic)):void =
        FireFrom(Event(0))

    OnPrimary(Event:tuple(player, logic)):void =
        FireFrom(Event(0))

    FireFrom(P:player):void =
        if (C := P.GetFortCharacter[]):
            Ray := SGLabViewRay(C)
            Fire(Ray(0) + Ray(1) * 150.0, Ray(1))

    Fire(From:vector3, Dir:vector3):void =
        if (R := Root?):
            set Shots += 1
            Hue := GetRandomFloat(0.0, 360.0)
            Paint := MakeColorFromHSV(Hue, 1.0, 1.0)
            Ball := entity{}
            Mesh := SM_SG_sphere{Entity := Ball}
            Mat := M_SG_Color{}
            set Mat.Color = Paint
            set Mat.Glow = 5.0
            set Mesh.Main = Mat
            set Mesh.Collidable = false
            Comp := paint_ball_component{Entity := Ball}
            set Comp.Velocity = Dir * Speed
            set Comp.Paint = Paint
            set Comp.Owner = option{Self}
            Ball.AddComponents(array{transform_component{Entity := Ball}, Mesh, Comp})
            Ball.SetLocalTransform(transform{Translation := From, Rotation := IdentityRotation(), Scale := V(0.25, 0.25, 0.25)})
            R.AddEntities(array{Ball})

    OnBallHit(Ball:entity, At:vector3, DidPaint:logic):void =
        set Hits += 1
        if (DidPaint?):
            set Painted += 1
        if (R := Root?):
            Fx := entity{}
            Fx.AddComponents(array{transform_component{Entity := Fx}, NS_SG_Burst{Entity := Fx}})
            Fx.SetLocalTransform(transform{Translation := At, Rotation := IdentityRotation(), Scale := V(1.0, 1.0, 1.0)})
            R.AddEntities(array{Fx})
            spawn{ Cleanup(Fx, 2.0) }
        Ball.RemoveFromParent()
        Word := if (DidPaint?) then "yes" else "no"
        Print("[Paint] hit at ({At.Forward}, {At.Left}, {At.Up}) painted={Word}")

    Cleanup(E:entity, After:float)<suspends>:void =
        Sleep(After)
        E.RemoveFromParent()
