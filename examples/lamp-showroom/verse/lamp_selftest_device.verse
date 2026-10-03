# Lamp showroom: optional runtime self-test.
#
# When RunSelfTest is on, waits for lamps to initialise, logs every lamp's state,
# toggles only the lamps whose DebugLabel starts with one of ToggleLabels, then logs
# every state again. Independence holds if only those lamps changed.

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Fortnite.com/Devices }
using { /UnrealEngine.com/Temporary/Diagnostics }

lamp_selftest_device<public> := class(creative_device):

    @editable
    RunSelfTest<public>:logic = false

    @editable
    ToggleLabels<public>:[]string = array{"A1", "B2"}

    OnBegin<override>()<suspends>:void =
        if (RunSelfTest?):
            Sleep(3.0)
            Report("before")
            if (SimulationEntity := GetSimulationEntity[]):
                for (Lamp : SimulationEntity.FindDescendantComponents(lamp_toggle_component), ShouldToggle[Lamp.DebugLabel]):
                    Lamp.Toggle()
            Report("after")

    ShouldToggle<private>(Label:string)<decides><transacts>:void =
        Matches := for (Prefix : ToggleLabels, StartsWith[Label, Prefix]) {Prefix}
        Matches.Length > 0

    StartsWith<private>(Text:string, Prefix:string)<decides><transacts>:void =
        Prefix.Length <= Text.Length
        Text.Slice[0, Prefix.Length] = Prefix

    Report<private>(Phase:string):void =
        if (SimulationEntity := GetSimulationEntity[]):
            var Line:string = "[LampShowroom] SELFTEST {Phase}:"
            for (Lamp : SimulationEntity.FindDescendantComponents(lamp_toggle_component)):
                State := if (Lamp.IsLampOn[]) then "ON" else "OFF"
                set Line += " {Lamp.DebugLabel}={State}"
            Print(Line)
