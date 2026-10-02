# Daily Reward UI - animation core.
# Easing curves + a cancellable per-property tween system.
# Continuous/passive motion lives in the UI materials (client-side, perfectly smooth);
# this file only drives short one-shot "juice" (pops, squash, wiggles, fades).

using { /Verse.org/Simulation }

dr_easing<public> := enum:
    Linear
    InQuad
    OutQuad
    InOutSine
    InBack
    OutBack
    OutElastic

DRPi<public>:float = 3.14159265

DREase<public>(Ease:dr_easing, T:float)<reads>:float =
    case (Ease):
        dr_easing.Linear => T
        dr_easing.InQuad => T * T
        dr_easing.OutQuad => 1.0 - (1.0 - T) * (1.0 - T)
        dr_easing.InOutSine => 0.5 - 0.5 * Cos(DRPi * T)
        dr_easing.InBack =>
            2.70158 * T * T * T - 1.70158 * T * T
        dr_easing.OutBack =>
            U := T - 1.0
            1.0 + 2.70158 * U * U * U + 1.70158 * U * U
        dr_easing.OutElastic =>
            if (T <= 0.0):
                0.0
            else if (T >= 1.0):
                1.0
            else:
                Pow(2.0, -10.0 * T) * Sin((T * 10.0 - 0.75) * (2.0 * DRPi / 3.0)) + 1.0

# Base class for anything with animatable float properties.
# Every property (Id) has a generation counter: starting a new tween on a property
# silently cancels the previous one, so hover/claim/open animations never fight.
dr_anim_target<public> := class<abstract>:
    var Gens<private>:[int]int = map{}
    var Vals<private>:[int]float = map{}

    # Implemented per widget: write value V into the widget field for property Id.
    ApplyProp<public>(Id:int, V:float):void

    Get<public>(Id:int, Default:float)<transacts>:float =
        if (V := Vals[Id]) then V else Default

    Snap<public>(Id:int, V:float):void =
        Bump(Id)
        Store(Id, V)

    Bump<private>(Id:int):int =
        G := (if (X := Gens[Id]) then X else 0) + 1
        if (set Gens[Id] = G) {}
        G

    Store<private>(Id:int, V:float):void =
        if (set Vals[Id] = V) {}
        ApplyProp(Id, V)

    Tween<public>(Id:int, From:float, To:float, Duration:float, Ease:dr_easing)<suspends>:void =
        MyGen := Bump(Id)
        Start := GetSimulationElapsedTime()
        Store(Id, From)
        loop:
            Sleep(0.0)
            Cur := if (X := Gens[Id]) then X else 0
            if (Cur <> MyGen):
                break
            Elapsed := GetSimulationElapsedTime() - Start
            T := if (Duration > 0.0) then Clamp(Elapsed / Duration, 0.0, 1.0) else 1.0
            Store(Id, From + (To - From) * DREase(Ease, T))
            if (T >= 1.0):
                break

    TweenTo<public>(Id:int, To:float, Duration:float, Ease:dr_easing)<suspends>:void =
        Tween(Id, Get(Id, To), To, Duration, Ease)

    # Uniform scale on two property ids at once (X and Y).
    TweenXY<public>(IdX:int, IdY:int, To:float, Duration:float, Ease:dr_easing)<suspends>:void =
        sync:
            TweenTo(IdX, To, Duration, Ease)
            TweenTo(IdY, To, Duration, Ease)

    # Juicy press: squash wide, then spring back with elastic overshoot.
    Squash<public>(IdX:int, IdY:int)<suspends>:void =
        sync:
            TweenTo(IdX, 1.12, 0.06, dr_easing.OutQuad)
            TweenTo(IdY, 0.86, 0.06, dr_easing.OutQuad)
        sync:
            TweenTo(IdX, 1.0, 0.45, dr_easing.OutElastic)
            TweenTo(IdY, 1.0, 0.45, dr_easing.OutElastic)

    # Cartoon wiggle on an angle property.
    Wiggle<public>(IdAngle:int, Strength:float)<suspends>:void =
        TweenTo(IdAngle, -Strength, 0.07, dr_easing.OutQuad)
        TweenTo(IdAngle, Strength * 0.8, 0.1, dr_easing.InOutSine)
        TweenTo(IdAngle, -Strength * 0.45, 0.09, dr_easing.InOutSine)
        TweenTo(IdAngle, Strength * 0.2, 0.08, dr_easing.InOutSine)
        TweenTo(IdAngle, 0.0, 0.08, dr_easing.OutQuad)
