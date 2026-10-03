# Lamp showroom: on/off behaviour for one lamp.
#
# Attach to the ROOT entity of the lamp prefab. Parts are found by component type,
# so the prefab layout stays free to change:
#   * every light_component under the root is coloured and switched,
#   * every mesh_component on an entity that also holds a light (the bulb) is shown only while lit,
#   * every lamp_state_indicator_component under the root (the switch lever) moves to its on/off pose,
#   * every interactable_component under the root toggles the lamp when used.

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Verse.org/Colors }
using { /UnrealEngine.com/Temporary/Diagnostics }

lamp_toggle_component<public> := class<final_super>(component):

    # State applied when the lamp enters the scene and whenever a new round begins.
    @editable
    InitiallyOn<public>:logic = false

    # Colour pushed to every light under this lamp.
    @editable
    LightColor<public>:color = NamedColors.White

    # Shown in the switch prompt and in log lines so playtests identify which lamp changed.
    @editable
    DebugLabel<public>:string = "Lamp"

    var IsOn<private>:logic = false
    var Subscriptions<private>:[]cancelable = array{}

    OnBeginSimulation<override>():void =
        (super:)OnBeginSimulation()
        for (Interactable : Entity.FindDescendantComponents(interactable_component)):
            set Subscriptions += array{Interactable.SucceededEvent.Subscribe(OnInteracted)}
        ResetToInitialState()

    OnEndSimulation<override>():void =
        for (Subscription : Subscriptions):
            Subscription.Cancel()
        set Subscriptions = array{}
        (super:)OnEndSimulation()

    # Restores the configured initial state. Called on simulation start and by lamp_round_reset_device.
    ResetToInitialState<public>():void =
        SetOn(InitiallyOn)
        Print("[LampShowroom] {DebugLabel} reset -> {StateText()}")

    Toggle<public>():void =
        SetOn(if (IsOn?) then false else true)
        Print("[LampShowroom] {DebugLabel} toggled -> {StateText()}")

    IsLampOn<public>()<decides><reads>:void = IsOn?

    SetOn<public>(NewState:logic):void =
        set IsOn = NewState
        for (Light : Entity.FindDescendantComponents(light_component)):
            set Light.ColorFilter = LightColor
            if (NewState?) then Light.Enable() else Light.Disable()
            for (BulbMesh : Light.Entity.FindDescendantComponents(mesh_component), BulbMesh.Entity = Light.Entity):
                set BulbMesh.Visible = NewState
        for (Indicator : Entity.FindDescendantComponents(lamp_state_indicator_component)):
            Indicator.ShowState(NewState)

    OnInteracted<private>(Agent:agent):void = Toggle()

    StateText<private>()<transacts>:string = if (IsOn?) then "ON" else "OFF"
