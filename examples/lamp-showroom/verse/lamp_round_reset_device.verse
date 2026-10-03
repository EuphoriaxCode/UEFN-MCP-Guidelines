# Lamp showroom: restores every lamp's configured initial state when a round begins.
#
# Wire RoundSettings to the level's Round Settings device. Lamps are found through the
# Scene Graph, so new lamp instances need no extra wiring.

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Fortnite.com/Devices }
using { /UnrealEngine.com/Temporary/Diagnostics }

lamp_round_reset_device<public> := class(creative_device):

    @editable
    RoundSettings<public>:round_settings_device = round_settings_device{}

    OnBegin<override>()<suspends>:void =
        RoundSettings.RoundBeginEvent.Subscribe(OnRoundBegin)

    OnRoundBegin<private>():void =
        ResetAllLamps()

    ResetAllLamps<public>():void =
        if (SimulationEntity := GetSimulationEntity[]):
            var Count:int = 0
            for (Lamp : SimulationEntity.FindDescendantComponents(lamp_toggle_component)):
                Lamp.ResetToInitialState()
                set Count += 1
            Print("[LampShowroom] Round begin: reset {Count} lamps")
