# Daily Reward - per-player view: wraps the UMG widgets, lays them out on a Verse canvas
# and choreographs every animation (open, cards stagger-in, hover, claim, popup, close).

using { /Fortnite.com/UI }
using { /UnrealEngine.com/Temporary/UI }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /Verse.org/Simulation }
using { /Verse.org/Colors }
using { /Verse.org/Input/UI }
using { DailyReward.UI }

# What the UI should show right now (computed by the device from the save data).
dr_display<public> := struct:
    CanClaim<public>:logic = false
    NextDay<public>:int = 0
    Streak<public>:int = 0
    RemainingSeconds<public>:int = 0
    AllClaimed<public>:logic = false

# Card widget state indices (FrameSwitch / GlowSwitch / TagSwitch children).
DRStateLocked<public>:int = 0
DRStateToday<public>:int = 1
DRStateClaimed<public>:int = 2

# Screen layout (offsets from screen centre, 1920x1080 reference).
DRCardX<public>:[]float = array{-410.0, -160.0, 90.0, -410.0, -160.0, 90.0, 395.0}
DRCardY<public>:[]float = array{-138.0, -138.0, -138.0, 150.0, 150.0, 150.0, 6.0}

DRCenterSlot<public>(W:widget, X:float, Y:float, Z:type{_X:int where 0 <= _X, _X <= 2147483647}):canvas_slot =
    canvas_slot:
        Widget := W
        Anchors := anchors{Minimum := vector2{X := 0.5, Y := 0.5}, Maximum := vector2{X := 0.5, Y := 0.5}}
        Offsets := margin{Left := X, Top := Y}
        Alignment := vector2{X := 0.5, Y := 0.5}
        SizeToContent := true
        ZOrder := Z

# Transparent clickable area of a fixed size.
DRHitArea<public>(W:float, H:float):color_block =
    color_block{DefaultColor := NamedColors.Black, DefaultOpacity := 0.0, DefaultDesiredSize := vector2{X := W, Y := H}}

DRFullSlot<public>(W:widget, Z:type{_X:int where 0 <= _X, _X <= 2147483647}):canvas_slot =
    canvas_slot:
        Widget := W
        Anchors := anchors{Minimum := vector2{X := 0.0, Y := 0.0}, Maximum := vector2{X := 1.0, Y := 1.0}}
        Offsets := margin{}
        Alignment := vector2{X := 0.0, Y := 0.0}
        SizeToContent := false
        ZOrder := Z

# ======================================================================= card
# Props: 0 ScaleX, 1 ScaleY, 2 Angle, 3 Flash, 4 CheckSize, 5 Opacity, 6 IconOpacity
dr_card_view<public> := class(dr_anim_target):
    Normal<public>:?WBP_DR_Card = false
    Mega<public>:?WBP_DR_MegaCard = false
    BaseW<public>:float = 250.0
    BaseH<public>:float = 270.0
    CheckNormal<public>:float = 100.0
    CheckBig<public>:float = 230.0

    GetWidget<public>():widget =
        if (C := Normal?):
            C
        else if (M := Mega?):
            M
        else:
            WBP_DR_Card{}

    ApplyProp<override>(Id:int, V:float):void =
        if (C := Normal?):
            if (Id = 0) then set C.CardW = BaseW * V
            else if (Id = 1) then set C.CardH = BaseH * V
            else if (Id = 2) then set C.CardAngle = V
            else if (Id = 3) then set C.Flash = V
            else if (Id = 4) then set C.CheckSize = V
            else if (Id = 5) then set C.CardOpacity = V
            else if (Id = 6) then set C.IconOpacity = V
        else if (M := Mega?):
            if (Id = 0) then set M.CardW = BaseW * V
            else if (Id = 1) then set M.CardH = BaseH * V
            else if (Id = 2) then set M.CardAngle = V
            else if (Id = 3) then set M.Flash = V
            else if (Id = 4) then set M.CheckSize = V
            else if (Id = 5) then set M.CardOpacity = V
            else if (Id = 6) then set M.IconOpacity = V

    SetState<public>(S:int):void =
        if (C := Normal?) then set C.State = S
        else if (M := Mega?) then set M.State = S

    SetDay<public>(Day:int):void =
        if (C := Normal?) then set C.DayIndex = Day

    SetReward<public>(R:dr_reward):void =
        G := DRAmountGlyphs(R.Kind, R.Amount)
        Icon := DRKindIndex(R.Kind)
        if (C := Normal?):
            set C.IconIndex = Icon
            set C.G1 = DRGlyphAt(G, 0)
            set C.G2 = DRGlyphAt(G, 1)
            set C.G3 = DRGlyphAt(G, 2)
            set C.G4 = DRGlyphAt(G, 3)
            set C.G5 = DRGlyphAt(G, 4)
        else if (M := Mega?):
            set M.IconIndex = Icon
            set M.G1 = DRGlyphAt(G, 0)
            set M.G2 = DRGlyphAt(G, 1)
            set M.G3 = DRGlyphAt(G, 2)
            set M.G4 = DRGlyphAt(G, 3)
            set M.G5 = DRGlyphAt(G, 4)

    # Instantly show a state (no animation).
    ShowState<public>(S:int):void =
        SetState(S)
        Snap(3, 0.0)
        Snap(6, if (S = DRStateLocked) then 0.55 else 1.0)
        Snap(4, if (S = DRStateClaimed) then CheckNormal else 0.0)

    PopIn<public>(Delay:float)<suspends>:void =
        Sleep(Delay)
        sync:
            TweenXY(0, 1, 1.0, 0.42, dr_easing.OutBack)
            TweenTo(5, 1.0, 0.12, dr_easing.OutQuad)
            Tween(2, -14.0, 0.0, 0.42, dr_easing.OutBack)

    PopOut<public>(Delay:float)<suspends>:void =
        Sleep(Delay)
        sync:
            TweenXY(0, 1, 0.0, 0.18, dr_easing.InBack)
            TweenTo(5, 0.0, 0.18, dr_easing.InQuad)

    # The big "you claimed it" moment on the card itself.
    ClaimBurst<public>()<suspends>:void =
        TweenXY(0, 1, 0.84, 0.09, dr_easing.InQuad)
        sync:
            TweenXY(0, 1, 1.32, 0.13, dr_easing.OutQuad)
            TweenTo(3, 1.0, 0.1, dr_easing.OutQuad)
        ShowStateKeepFlash()
        sync:
            TweenXY(0, 1, 1.0, 0.6, dr_easing.OutElastic)
            TweenTo(3, 0.0, 0.35, dr_easing.OutQuad)
            Wiggle(2, 10.0)
            block:
                Tween(4, 0.0, CheckBig, 0.11, dr_easing.OutQuad)
                TweenTo(4, CheckNormal, 0.32, dr_easing.OutBack)

    ShowStateKeepFlash<private>():void =
        SetState(DRStateClaimed)
        Snap(6, 1.0)

    # Day becomes claimable while the menu is open.
    Unlock<public>()<suspends>:void =
        SetState(DRStateToday)
        Snap(6, 1.0)
        sync:
            block:
                TweenXY(0, 1, 1.22, 0.12, dr_easing.OutQuad)
                TweenXY(0, 1, 1.0, 0.5, dr_easing.OutElastic)
            Wiggle(2, 8.0)

# ======================================================================= frame
# Props: 0 PanelX, 1 PanelY, 2 PanelOpacity, 3 Backdrop, 4 Rays, 5 TimerOpacity
dr_frame_view<public> := class(dr_anim_target):
    F<public>:WBP_DR_Frame = WBP_DR_Frame{}

    ApplyProp<override>(Id:int, V:float):void =
        if (Id = 0) then set F.PanelW = 1300.0 * V
        else if (Id = 1) then set F.PanelH = 1000.0 * V
        else if (Id = 2) then set F.PanelOpacity = V
        else if (Id = 3) then set F.BackdropOpacity = V
        else if (Id = 4) then set F.RaysOpacity = V
        else if (Id = 5) then set F.TimerOpacity = V

    SetStreak<public>(N:int):void =
        G := DRDigits(Min(N, 999))
        set F.S1 = DRGlyphAt(G, 0)
        set F.S2 = DRGlyphAt(G, 1)
        set F.S3 = DRGlyphAt(G, 2)

    SetTimer<public>(Seconds:int):void =
        G := DRTimerGlyphs(Seconds)
        set F.T1 = DRGlyphAt(G, 0)
        set F.T2 = DRGlyphAt(G, 1)
        set F.T3 = DRGlyphAt(G, 2)
        set F.T4 = DRGlyphAt(G, 3)
        set F.T5 = DRGlyphAt(G, 4)
        set F.T6 = DRGlyphAt(G, 5)
        set F.T7 = DRGlyphAt(G, 6)
        set F.T8 = DRGlyphAt(G, 7)

# ======================================================================= buttons
# Props: 0 ScaleX, 1 ScaleY, 2 Angle, 3 Opacity
dr_claim_view<public> := class(dr_anim_target):
    B<public>:WBP_DR_ClaimButton = WBP_DR_ClaimButton{}

    ApplyProp<override>(Id:int, V:float):void =
        if (Id = 0) then set B.BtnW = 480.0 * V
        else if (Id = 1) then set B.BtnH = 160.0 * V
        else if (Id = 2) then set B.BtnAngle = V
        else if (Id = 3) then set B.BtnOpacity = V

    SetCanClaim<public>(Can:logic):void =
        set B.BtnState = if (Can?) then 0 else 1

# Props: 0 Scale, 1 Angle, 2 Opacity
dr_close_view<public> := class(dr_anim_target):
    B<public>:WBP_DR_CloseButton = WBP_DR_CloseButton{}

    ApplyProp<override>(Id:int, V:float):void =
        if (Id = 0) then set B.CloseSize = 130.0 * V
        else if (Id = 1) then set B.CloseAngle = V
        else if (Id = 2) then set B.CloseOpacity = V

# ======================================================================= popup
# Props: 0 ScaleX, 1 ScaleY, 2 Opacity, 3 RaysScale, 4 ConfettiOpacity
dr_popup_view<public> := class(dr_anim_target):
    P<public>:WBP_DR_Popup = WBP_DR_Popup{}

    ApplyProp<override>(Id:int, V:float):void =
        if (Id = 0) then set P.PopW = 800.0 * V
        else if (Id = 1) then set P.PopH = 760.0 * V
        else if (Id = 2) then set P.PopOpacity = V
        else if (Id = 3) then set P.RaysSize = 1300.0 * V
        else if (Id = 4) then set P.ConfettiOpacity = V

    Show<public>(R:dr_reward)<suspends>:void =
        Icon := DRKindIndex(R.Kind)
        set P.PopIcon = Icon
        set P.PopType = Icon
        G := DRAmountGlyphs(R.Kind, R.Amount)
        set P.P1 = DRGlyphAt(G, 0)
        set P.P2 = DRGlyphAt(G, 1)
        set P.P3 = DRGlyphAt(G, 2)
        set P.P4 = DRGlyphAt(G, 3)
        set P.P5 = DRGlyphAt(G, 4)
        set P.P6 = DRGlyphAt(G, 5)
        Snap(0, 0.2)
        Snap(1, 0.2)
        Snap(3, 0.0)
        Snap(4, 1.0)
        sync:
            TweenTo(2, 1.0, 0.14, dr_easing.OutQuad)
            TweenXY(0, 1, 1.0, 0.75, dr_easing.OutElastic)
            TweenTo(3, 1.0, 0.55, dr_easing.OutBack)
        Sleep(1.55)
        TweenXY(0, 1, 1.12, 0.12, dr_easing.OutQuad)
        sync:
            TweenXY(0, 1, 0.0, 0.22, dr_easing.InBack)
            TweenTo(2, 0.0, 0.26, dr_easing.InQuad)
            TweenTo(3, 0.0, 0.26, dr_easing.InQuad)

# ======================================================================= HUD reminder
# Props: 0 Scale, 1 Opacity
dr_notify_view<public> := class(dr_anim_target):
    N<public>:WBP_DR_Notify = WBP_DR_Notify{}

    ApplyProp<override>(Id:int, V:float):void =
        if (Id = 0) then set N.NotifySize = 200.0 * V
        else if (Id = 1) then set N.NotifyOpacity = V

# ======================================================================= player view
dr_player_view<public> := class:
    Player<public>:player
    Frame<public>:dr_frame_view
    Cards<public>:[]dr_card_view
    Claim<public>:dr_claim_view
    Close<public>:dr_close_view
    Popup<public>:dr_popup_view
    Root<public>:canvas
    # Verse click layers (the UMG art underneath is purely visual)
    ClaimBtn<public>:button
    CloseBtn<public>:button
    BackdropBtn<public>:button
    Notify<public>:dr_notify_view
    NotifyRoot<public>:canvas
    var NotifyShown<public>:logic = false
    BackEvent<public>:event() = event(){}

    var IsOpen<public>:logic = false
    var Busy<public>:logic = false
    var Last<public>:dr_display = dr_display{}
    CloseEvent<public>:event() = event(){}
    DestroyEvent<public>:event() = event(){}

    # Instant update of every visual from a display state.
    ApplyDisplay<public>(D:dr_display, Rewards:[]dr_reward):void =
        set Last = D
        for (I -> Card : Cards):
            if (R := Rewards[I]) then Card.SetReward(R)
            Card.ShowState(StateFor(D, I))
        Frame.SetStreak(D.Streak)
        Frame.SetTimer(D.RemainingSeconds)
        Frame.Snap(5, if (D.CanClaim?) then 0.0 else 1.0)
        Claim.SetCanClaim(D.CanClaim)

    StateFor<public>(D:dr_display, I:int)<transacts>:int =
        if (D.AllClaimed?):
            DRStateClaimed
        else if (I < D.NextDay):
            DRStateClaimed
        else if (I = D.NextDay, D.CanClaim?):
            DRStateToday
        else:
            DRStateLocked

    Open<public>(D:dr_display, Rewards:[]dr_reward)<suspends>:void =
        if (IsOpen?) then return
        set IsOpen = true
        ApplyDisplay(D, Rewards)
        # start poses
        Frame.Snap(0, 0.55)
        Frame.Snap(1, 0.55)
        Frame.Snap(2, 0.0)
        Frame.Snap(3, 0.0)
        Frame.Snap(4, 0.0)
        for (Card : Cards):
            Card.Snap(0, 0.0)
            Card.Snap(1, 0.0)
            Card.Snap(5, 0.0)
        Claim.Snap(0, 0.0)
        Claim.Snap(1, 0.0)
        Claim.Snap(3, 0.0)
        Close.Snap(0, 0.0)
        Close.Snap(2, 0.0)
        Popup.Snap(2, 0.0)
        if (PlayerUI := GetPlayerUI[Player]):
            PlayerUI.AddWidget(Root, player_ui_slot{InputMode := ui_input_mode.All})
        for (I -> Card : Cards):
            spawn{ Card.PopIn(0.16 + 0.055 * (I * 1.0)) }
        sync:
            Frame.TweenTo(3, 1.0, 0.25, dr_easing.OutQuad)
            Frame.TweenTo(4, 1.0, 0.6, dr_easing.OutQuad)
            Frame.TweenTo(2, 1.0, 0.14, dr_easing.OutQuad)
            Frame.TweenXY(0, 1, 1.0, 0.5, dr_easing.OutBack)
            block:
                Sleep(0.5)
                sync:
                    Claim.TweenXY(0, 1, 1.0, 0.7, dr_easing.OutElastic)
                    Claim.TweenTo(3, 1.0, 0.1, dr_easing.OutQuad)
            block:
                Sleep(0.55)
                sync:
                    Close.TweenTo(0, 1.0, 0.4, dr_easing.OutBack)
                    Close.Tween(1, -140.0, 0.0, 0.45, dr_easing.OutBack)
                    Close.TweenTo(2, 1.0, 0.1, dr_easing.OutQuad)
        spawn{ IdleLoop() }

    CloseUI<public>()<suspends>:void =
        if (not IsOpen?) then return
        set IsOpen = false
        # Safety net: the UI (and its mouse/input capture) is ALWAYS removed, even if this
        # close animation gets cancelled halfway.
        defer:
            if (PlayerUI := GetPlayerUI[Player]):
                PlayerUI.RemoveWidget(Root)
        CloseEvent.Signal()
        for (I -> Card : Cards):
            spawn{ Card.PopOut(0.02 * (I * 1.0)) }
        sync:
            Frame.TweenXY(0, 1, 0.6, 0.24, dr_easing.InBack)
            Frame.TweenTo(2, 0.0, 0.24, dr_easing.InQuad)
            Frame.TweenTo(3, 0.0, 0.28, dr_easing.InQuad)
            Frame.TweenTo(4, 0.0, 0.2, dr_easing.InQuad)
            Claim.TweenXY(0, 1, 0.0, 0.18, dr_easing.InBack)
            Close.TweenTo(0, 0.0, 0.18, dr_easing.InBack)
        Sleep(0.05)

    # Full claim choreography; Display = state after the claim.
    PlayClaim<public>(DayIndex:int, Reward:dr_reward, D:dr_display, Rewards:[]dr_reward)<suspends>:void =
        set Busy = true
        spawn{ Claim.Squash(0, 1) }
        if (Card := Cards[DayIndex]):
            Card.ClaimBurst()
        Root.AddWidget(DRFullSlot(Popup.P, 9))
        Popup.Show(Reward)
        Root.RemoveWidget(Popup.P)
        # settle into the "come back tomorrow" state
        set Last = D
        Frame.SetStreak(D.Streak)
        Frame.SetTimer(D.RemainingSeconds)
        Claim.SetCanClaim(D.CanClaim)
        for (I -> C : Cards, StateFor(D, I) = DRStateClaimed, I <> DayIndex):
            C.ShowState(DRStateClaimed)
        sync:
            Frame.TweenTo(5, (if (D.CanClaim?) then 0.0 else 1.0), 0.3, dr_easing.OutQuad)
            Claim.Squash(0, 1)
        set Busy = false

    # The next day became claimable while open (timer hit zero).
    PlayUnlock<public>(D:dr_display)<suspends>:void =
        set Last = D
        Claim.SetCanClaim(D.CanClaim)
        Frame.SetStreak(D.Streak)
        # a new cycle (or broken streak) resets the other cards
        for (I -> C : Cards, I <> D.NextDay):
            C.ShowState(StateFor(D, I))
        sync:
            Frame.TweenTo(5, 0.0, 0.25, dr_easing.OutQuad)
            Claim.Squash(0, 1)
            block:
                if (Card := Cards[D.NextDay]):
                    Card.Unlock()

    # Little life while idle: today's card wiggles, the CLAIM button bounces.
    IdleLoop<private>()<suspends>:void =
        race:
            CloseEvent.Await()
            DestroyEvent.Await()
            loop:
                Sleep(2.6)
                if (not Busy?, Last.CanClaim?, Card := Cards[Last.NextDay]):
                    spawn{ Card.Wiggle(2, 6.0) }
                    spawn{ Claim.Squash(0, 1) }

    ShowNotify<public>()<suspends>:void =
        if (NotifyShown? or IsOpen?) then return
        set NotifyShown = true
        Notify.Snap(0, 0.0)
        Notify.Snap(1, 0.0)
        if (PlayerUI := GetPlayerUI[Player]):
            PlayerUI.AddWidget(NotifyRoot, player_ui_slot{InputMode := ui_input_mode.None})
        sync:
            Notify.TweenTo(0, 1.0, 0.6, dr_easing.OutElastic)
            Notify.TweenTo(1, 1.0, 0.15, dr_easing.OutQuad)

    HideNotify<public>()<suspends>:void =
        if (not NotifyShown?) then return
        set NotifyShown = false
        sync:
            Notify.TweenTo(0, 0.0, 0.18, dr_easing.InBack)
            Notify.TweenTo(1, 0.0, 0.18, dr_easing.InQuad)
        if (not NotifyShown?, PlayerUI := GetPlayerUI[Player]):
            PlayerUI.RemoveWidget(NotifyRoot)

    # Claim pressed while nothing is ready: playful "nope" shake.
    Nope<public>()<suspends>:void =
        sync:
            Claim.Squash(0, 1)
            Claim.Wiggle(2, 7.0)

    # Hover juice for both buttons (runs for the lifetime of the player).
    HoverLoops<public>()<suspends>:void =
        race:
            DestroyEvent.Await()
            loop:
                ClaimBtn.HighlightEvent().Await()
                if (not Busy?):
                    spawn{ Claim.TweenXY(0, 1, 1.08, 0.16, dr_easing.OutBack) }
            loop:
                ClaimBtn.UnhighlightEvent().Await()
                if (not Busy?):
                    spawn{ Claim.TweenXY(0, 1, 1.0, 0.2, dr_easing.OutQuad) }
            loop:
                CloseBtn.HighlightEvent().Await()
                spawn{ Close.TweenTo(0, 1.15, 0.15, dr_easing.OutBack) }
                spawn{ Close.Wiggle(1, 12.0) }
            loop:
                CloseBtn.UnhighlightEvent().Await()
                spawn{ Close.TweenTo(0, 1.0, 0.2, dr_easing.OutQuad) }

MakeDRPlayerView<public>(InPlayer:player):dr_player_view =
    Frame := dr_frame_view{}
    Claim := dr_claim_view{}
    Close := dr_close_view{}
    Popup := dr_popup_view{}
    Cards := for (I := 0..6):
        if (I = 6):
            dr_card_view{Mega := option{WBP_DR_MegaCard{}}, BaseW := 350.0, BaseH := 540.0, CheckNormal := 150.0, CheckBig := 320.0}
        else:
            dr_card_view{Normal := option{WBP_DR_Card{}}}
    for (I -> Card : Cards):
        Card.SetDay(I)
    # Never let a ScaleBox'd glyph row start empty (zero-width content breaks its scale).
    set Popup.P.P1 = DRGlyphPlus
    set Popup.P.P2 = 0
    Frame.SetStreak(0)
    Frame.SetTimer(0)
    # Click layers: invisible, fixed-size Verse buttons stacked ON TOP of all UMG art,
    # so no full-screen UMG widget can ever swallow the clicks.
    ClaimBtn := button{Slot := button_slot{Widget := DRHitArea(470.0, 150.0)}}
    CloseBtn := button{Slot := button_slot{Widget := DRHitArea(125.0, 125.0)}}
    BackdropBtn := button{Slot := button_slot{Widget := DRHitArea(16.0, 16.0), HorizontalAlignment := horizontal_alignment.Fill, VerticalAlignment := vertical_alignment.Fill}}
    # absorbs clicks on the panel itself so only clicks NEXT to it close the menu
    PanelBlocker := button{Slot := button_slot{Widget := DRHitArea(1220.0, 820.0)}}
    set CloseBtn.TriggeringInputAction = option{Back}
    var Slots:[]canvas_slot = array{DRFullSlot(Frame.F, 0), DRFullSlot(BackdropBtn, 1), DRCenterSlot(PanelBlocker, 0.0, 30.0, 2)}
    for (I -> Card : Cards, X := DRCardX[I], Y := DRCardY[I]):
        set Slots += array{DRCenterSlot(Card.GetWidget(), X, Y, 3)}
    set Slots += array{
        DRCenterSlot(Claim.B, 0.0, 370.0, 4),
        DRCenterSlot(Close.B, 560.0, -340.0, 5),
        DRCenterSlot(ClaimBtn, 0.0, 370.0, 6),
        DRCenterSlot(CloseBtn, 560.0, -340.0, 7)}
    Notify := dr_notify_view{}
    NotifySlot := canvas_slot:
        Widget := Notify.N
        Anchors := anchors{Minimum := vector2{X := 1.0, Y := 0.42}, Maximum := vector2{X := 1.0, Y := 0.42}}
        Offsets := margin{Left := -30.0}
        Alignment := vector2{X := 1.0, Y := 0.5}
        SizeToContent := true
        ZOrder := 0
    dr_player_view:
        Player := InPlayer
        Frame := Frame
        Cards := Cards
        Claim := Claim
        Close := Close
        Popup := Popup
        Root := canvas{Slots := Slots}
        ClaimBtn := ClaimBtn
        CloseBtn := CloseBtn
        BackdropBtn := BackdropBtn
        Notify := Notify
        NotifyRoot := canvas{Slots := array{NotifySlot}}
