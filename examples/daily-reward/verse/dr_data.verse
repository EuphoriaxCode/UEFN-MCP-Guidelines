# Daily Reward - reward config, persistent save data and number -> glyph formatting.

using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

# Order matches the IconSwitch / TypeSwitch children in the widgets.
dr_reward_kind<public> := enum:
    Coins
    Cash
    Gems
    Boost
    MysteryGift
    Chest
    MegaChest

DRKindIndex<public>(Kind:dr_reward_kind)<computes>:int =
    case (Kind):
        dr_reward_kind.Coins => 0
        dr_reward_kind.Cash => 1
        dr_reward_kind.Gems => 2
        dr_reward_kind.Boost => 3
        dr_reward_kind.MysteryGift => 4
        dr_reward_kind.Chest => 5
        dr_reward_kind.MegaChest => 6

# One day of the 7-day calendar.
dr_reward<public> := class<concrete>:
    # Which icon/label is shown.
    @editable
    Kind<public>:dr_reward_kind = dr_reward_kind.Coins

    # Number shown on the card (Boost shows it as "x2").
    @editable
    Amount<public>:int = 100

    # Item granters fired for the claiming player (e.g. a granter that gives your tycoon currency).
    @editable
    Granters<public>:[]item_granter_device = array{}

    # How many times each granter is fired.
    @editable
    GrantRepeat<public>:int = 1

    # Triggers fired for the claiming player (hook any device logic: boosts, cosmetics, ...).
    @editable
    Triggers<public>:[]trigger_device = array{}

# Info sent through daily_reward_device.RewardClaimedEvent so your own tycoon code can react.
dr_claim_info<public> := struct:
    Player<public>:player
    DayIndex<public>:int
    Kind<public>:dr_reward_kind
    Amount<public>:int

# ----------------------------------------------------------------- persistence

dr_save<public> := class<final><persistable>:
    LastClaimTime<public>:float = 0.0
    NextDay<public>:int = 0
    Streak<public>:int = 0
    TotalClaims<public>:int = 0

var DRSaveMap<public>:weak_map(player, dr_save) = map{}

# ----------------------------------------------------------------- glyphs
# Glyph indices used by WBP_DR_Glyph: 0-9 digits, then + K M x : . and blank.
DRGlyphPlus<public>:int = 10
DRGlyphK<public>:int = 11
DRGlyphM<public>:int = 12
DRGlyphX<public>:int = 13
DRGlyphColon<public>:int = 14
DRGlyphDot<public>:int = 15
DRGlyphBlank<public>:int = 16

DRDigits<public>(N:int)<transacts>:[]int =
    var Out:[]int = array{}
    var V:int = if (N < 0) then 0 else N
    loop:
        if (D := Mod[V, 10], Q := Quotient[V, 10]):
            set Out = array{D} + Out
            set V = Q
        else:
            break
        if (V = 0):
            break
    Out

DRCompact<internal>(Amount:int, Unit:int, Suffix:int)<transacts>:[]int =
    if (Whole := Quotient[Amount, Unit], Rem := Mod[Amount, Unit], Tenth := Quotient[Rem * 10, Unit]):
        if (Whole < 10, Tenth > 0):
            return DRDigits(Whole) + array{DRGlyphDot} + DRDigits(Tenth) + array{Suffix}
        return DRDigits(Whole) + array{Suffix}
    array{Suffix}

# "+500", "+2.5K", "+10K", "+1.2M", Boost -> "x2"
DRAmountGlyphs<public>(Kind:dr_reward_kind, Amount:int)<transacts>:[]int =
    if (Kind = dr_reward_kind.Boost):
        return array{DRGlyphX} + DRDigits(Amount)
    if (Amount >= 1000000):
        return array{DRGlyphPlus} + DRCompact(Amount, 1000000, DRGlyphM)
    if (Amount >= 1000):
        return array{DRGlyphPlus} + DRCompact(Amount, 1000, DRGlyphK)
    array{DRGlyphPlus} + DRDigits(Amount)

DRTwo<internal>(N:int)<transacts>:[]int =
    array{(if (X := Quotient[N, 10]) then X else 0), (if (X := Mod[N, 10]) then X else 0)}

# HH:MM:SS (hours clamp at 99)
DRTimerGlyphs<public>(Seconds:int)<transacts>:[]int =
    S := Max(Seconds, 0)
    H := Min((if (X := Quotient[S, 3600]) then X else 0), 99)
    M := if (X := Quotient[S, 60], Y := Mod[X, 60]) then Y else 0
    Sec := if (X := Mod[S, 60]) then X else 0
    DRTwo(H) + array{DRGlyphColon} + DRTwo(M) + array{DRGlyphColon} + DRTwo(Sec)

DRGlyphAt<public>(Glyphs:[]int, I:int)<transacts>:int =
    if (G := Glyphs[I]) then G else DRGlyphBlank
