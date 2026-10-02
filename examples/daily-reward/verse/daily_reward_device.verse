# Daily Reward device - drop it in the level, fill the 7 rewards, done.
#
#  - 7-day streak calendar (day 7 = MEGA chest), resets if a day is missed
#  - persistent per player (survives leaving / rejoining)
#  - opens via buttons / triggers / Verse (OpenFor); optional auto-open on join
#  - closes via the X, Escape (gamepad Back), clicking next to the panel, or an idle timeout
#  - small bouncing HUD reminder while a reward is waiting
#  - grants rewards through item granters and/or triggers, and signals RewardClaimedEvent
#    so your tycoon code can add cash, start a boost, etc.
#  - set SecondsPerDay to e.g. 20 to test the whole cycle quickly

using { /Fortnite.com/Devices }
using { /Fortnite.com/Playspaces }
using { /Verse.org/Simulation }
using { /Verse.org/Input }
using { /Verse.org/Input/UI }
using { /UnrealEngine.com/Temporary/Diagnostics }

daily_reward_device<public> := class(creative_device):

    # Day 1..7. Day 7 is shown on the big MEGA card.
    @editable
    Rewards<public>:[]dr_reward = array:
        dr_reward{Kind := dr_reward_kind.Coins, Amount := 500}
        dr_reward{Kind := dr_reward_kind.Cash, Amount := 1000}
        dr_reward{Kind := dr_reward_kind.Gems, Amount := 5}
        dr_reward{Kind := dr_reward_kind.Coins, Amount := 2500}
        dr_reward{Kind := dr_reward_kind.Boost, Amount := 2}
        dr_reward{Kind := dr_reward_kind.Gems, Amount := 10}
        dr_reward{Kind := dr_reward_kind.MegaChest, Amount := 10000}

    # Length of one "day" in seconds. 86400 = real day. Use ~20 to test.
    @editable
    SecondsPerDay<public>:float = 86400.0

    # The streak resets to day 1 when the player waits this many days (or more) between claims.
    @editable
    StreakResetAfterDays<public>:float = 2.0

    # Open the menu automatically shortly after joining when a reward is ready (off = only via buttons).
    @editable
    AutoOpenOnJoin<public>:logic = false

    # Show a small bouncing gift on the HUD while a reward is ready to claim.
    @editable
    ShowReadyReminder<public>:logic = true

    # Close the menu automatically after this many seconds (0 = never).
    @editable
    AutoCloseAfter<public>:float = 90.0

    # Text shown on the Open Buttons.
    ButtonText<localizes>:message = "Daily Rewards"

    @editable
    AutoOpenDelay<public>:float = 2.5

    # Any of these open the menu for the interacting player.
    @editable
    OpenButtons<public>:[]button_device = array{}

    @editable
    OpenTriggers<public>:[]trigger_device = array{}

    # Optional sounds (Audio Player devices).
    @editable
    OpenSounds<public>:[]audio_player_device = array{}

    @editable
    ClaimSounds<public>:[]audio_player_device = array{}

    # TESTING ONLY: wipes every player's daily-reward progress when they join.
    @editable
    ResetProgressOnJoin<public>:logic = false

    # TESTING ONLY: when > 0, the menu claims by itself this many seconds after a reward is ready.
    @editable
    DebugAutoClaimAfter<public>:float = 0.0

    # Await this from your own Verse to react to claims (add tycoon cash, start boosts, ...).
    RewardClaimedEvent<public>:event(dr_claim_info) = event(dr_claim_info){}

    var Views<private>:[player]dr_player_view = map{}

    OnBegin<override>()<suspends>:void =
        for (Player : GetPlayspace().GetPlayers()):
            OnPlayerAdded(Player)
        GetPlayspace().PlayerAddedEvent().Subscribe(OnPlayerAdded)
        GetPlayspace().PlayerRemovedEvent().Subscribe(OnPlayerRemoved)
        for (B : OpenButtons):
            B.SetInteractionText(ButtonText)
            B.InteractedWithEvent.Subscribe(OnOpenRequest)
        for (T : OpenTriggers):
            T.TriggeredEvent.Subscribe(OnOpenTrigger)

    # ---------------------------------------------------------------- public API

    # Open the daily reward menu for a player (e.g. from your own HUD button logic).
    OpenFor<public>(Player:player):void =
        if (View := Views[Player]):
            spawn{ OpenView(View) }

    # ---------------------------------------------------------------- players

    OnPlayerAdded<private>(Player:player):void =
        if (Views[Player]):
            return
        if (ResetProgressOnJoin?):
            SetSave(Player, dr_save{})
        View := MakeDRPlayerView(Player)
        if (set Views[Player] = View) {}
        spawn{ View.HoverLoops() }
        spawn{ WatchClaim(View) }
        spawn{ WatchClose(View) }
        spawn{ TimerLoop(View) }
        if (PlayerInput := GetPlayerInput[Player]):
            PlayerInput.GetInputEvents(Back).TriggerActivationEvent.Subscribe(OnBackPressed)
        if (DebugAutoClaimAfter > 0.0):
            spawn{ DebugAutoClaim(View) }
        if (AutoOpenOnJoin?):
            spawn{ AutoOpen(View) }

    OnPlayerRemoved<private>(Player:player):void =
        if (View := Views[Player]):
            View.DestroyEvent.Signal()
            var NewViews:[player]dr_player_view = map{}
            for (Key -> Value : Views, Key <> Player):
                if (set NewViews[Key] = Value) {}
            set Views = NewViews

    OnBackPressed<private>(Payload:tuple(player, logic)):void =
        if (View := Views[Payload(0)], View.IsOpen?):
            View.BackEvent.Signal()

    OnOpenRequest<private>(Agent:agent):void =
        if (Player := player[Agent]):
            OpenFor(Player)

    OnOpenTrigger<private>(MaybeAgent:?agent):void =
        if (Agent := MaybeAgent?, Player := player[Agent]):
            OpenFor(Player)

    AutoOpen<private>(View:dr_player_view)<suspends>:void =
        Sleep(AutoOpenDelay)
        if (ComputeDisplay(View.Player).CanClaim?):
            OpenView(View)

    OpenView<private>(View:dr_player_view)<suspends>:void =
        if (View.IsOpen?):
            return
        for (S : OpenSounds):
            S.Play(View.Player)
        if (PlayerInput := GetPlayerInput[View.Player]):
            PlayerInput.AddInputMapping(MenuNavigationMapping)
        spawn{ View.HideNotify() }
        View.Open(ComputeDisplay(View.Player), Rewards)
        if (AutoCloseAfter > 0.0):
            spawn{ AutoCloseTimer(View) }

    CloseView<private>(View:dr_player_view)<suspends>:void =
        # never cut a claim animation in half
        loop:
            if (not View.Busy?) then break
            Sleep(0.1)
        if (PlayerInput := GetPlayerInput[View.Player]):
            PlayerInput.RemoveInputMapping(MenuNavigationMapping)
        View.CloseUI()

    AutoCloseTimer<private>(View:dr_player_view)<suspends>:void =
        # Only the WAITING is raced. The close itself must run outside the race: CloseUI signals
        # CloseEvent, which would otherwise cancel the close halfway (UI faded but still on screen,
        # mouse captured, player stuck).
        TimedOut := race:
            block:
                View.CloseEvent.Await()
                false
            block:
                View.DestroyEvent.Await()
                false
            block:
                Sleep(AutoCloseAfter)
                true
        if (TimedOut?, View.IsOpen?):
            Print("[DailyReward] auto-close")
            CloseView(View)

    # ---------------------------------------------------------------- loops

    WatchClaim<private>(View:dr_player_view)<suspends>:void =
        race:
            View.DestroyEvent.Await()
            loop:
                View.ClaimBtn.OnClick().Await()
                Print("[DailyReward] CLAIM clicked")
                if (View.IsOpen?, not View.Busy?):
                    if (ComputeDisplay(View.Player).CanClaim?):
                        ClaimFlow(View)
                    else:
                        View.Nope()

    WatchClose<private>(View:dr_player_view)<suspends>:void =
        race:
            View.DestroyEvent.Await()
            loop:
                race:
                    View.CloseBtn.OnClick().Await()
                    View.BackdropBtn.OnClick().Await()
                    View.BackEvent.Await()
                Print("[DailyReward] close requested")
                if (View.IsOpen?):
                    View.Close.TweenTo(0, 0.82, 0.07, dr_easing.OutQuad)
                    CloseView(View)

    # Keeps the countdown ticking and unlocks the next day live while the menu is open.
    TimerLoop<private>(View:dr_player_view)<suspends>:void =
        race:
            View.DestroyEvent.Await()
            loop:
                Sleep(0.25)
                if (ShowReadyReminder?, not View.IsOpen?):
                    if (ComputeDisplay(View.Player).CanClaim?):
                        if (not View.NotifyShown?) then spawn{ View.ShowNotify() }
                    else if (View.NotifyShown?):
                        spawn{ View.HideNotify() }
                if (View.IsOpen?, not View.Busy?):
                    D := ComputeDisplay(View.Player)
                    if (D.CanClaim?, not View.Last.CanClaim?):
                        View.PlayUnlock(D)
                    else:
                        View.Frame.SetTimer(D.RemainingSeconds)

    DebugAutoClaim<private>(View:dr_player_view)<suspends>:void =
        race:
            View.DestroyEvent.Await()
            loop:
                Sleep(DebugAutoClaimAfter)
                if (View.IsOpen?, not View.Busy?, View.Last.CanClaim?):
                    Print("[DailyReward] debug auto-claim")
                    ClaimFlow(View)

    ClaimFlow<private>(View:dr_player_view)<suspends>:void =
        MaybeDay := DoClaim(View.Player)
        if (Day := MaybeDay?, Reward := Rewards[Day]):
            for (S : ClaimSounds):
                S.Play(View.Player)
            View.PlayClaim(Day, Reward, ComputeDisplay(View.Player), Rewards)

    # ---------------------------------------------------------------- logic

    Now<private>()<transacts>:float = GetSecondsSinceEpoch()

    GetSave<private>(Player:player)<transacts>:dr_save =
        if (S := DRSaveMap[Player]) then S else dr_save{}

    SetSave<private>(Player:player, S:dr_save):void =
        if (set DRSaveMap[Player] = S) {}

    NumDays<private>()<transacts>:int = Min(Rewards.Length, 7)

    ComputeDisplay<public>(Player:player)<transacts>:dr_display =
        S := GetSave(Player)
        Elapsed := Now() - S.LastClaimTime
        Never := if (S.TotalClaims = 0) then true else false
        CanClaim := if (Never?) then true else if (Elapsed >= SecondsPerDay) then true else false
        Broken := if (not Never?, Elapsed >= SecondsPerDay * StreakResetAfterDays) then true else false
        Next := if (Broken?) then 0 else S.NextDay
        Streak := if (Broken?) then 0 else S.Streak
        Remaining := if (CanClaim?) then 0 else (if (R := Ceil[SecondsPerDay - Elapsed]) then R else 0)
        AllClaimed := if (not CanClaim?, not Never?, Next = 0) then true else false
        dr_display:
            CanClaim := CanClaim
            NextDay := Next
            Streak := Streak
            RemainingSeconds := Remaining
            AllClaimed := AllClaimed

    # Applies the claim (save + grant + event). Returns the claimed day index.
    DoClaim<private>(Player:player):?int =
        D := ComputeDisplay(Player)
        if (not D.CanClaim?):
            return false
        Day := D.NextDay
        Reward := if (R := Rewards[Day]) then R else dr_reward{}
        Days := Max(NumDays(), 1)
        Old := GetSave(Player)
        NewSave := dr_save:
            LastClaimTime := Now()
            NextDay := if (N := Mod[Day + 1, Days]) then N else 0
            Streak := D.Streak + 1
            TotalClaims := Old.TotalClaims + 1
        SetSave(Player, NewSave)
        Grant(Player, Reward)
        RewardClaimedEvent.Signal(dr_claim_info{Player := Player, DayIndex := Day, Kind := Reward.Kind, Amount := Reward.Amount})
        Print("[DailyReward] claimed day {Day + 1}")
        option{Day}

    Grant<private>(Player:player, Reward:dr_reward):void =
        for (G : Reward.Granters, I := 1..Max(Reward.GrantRepeat, 1)):
            G.GrantItem(Player)
        for (T : Reward.Triggers):
            T.Trigger(Player)
