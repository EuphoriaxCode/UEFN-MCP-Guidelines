# Lamp showroom: the interaction on a lamp's switch cube.
#
# A basic_interactable_component whose prompt names the lamp and the action the
# switch will perform, read from the lamp_toggle_component on the parent entity.

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }

lamp_switch_component<public> := class<final_super>(basic_interactable_component):

    TurnOnMessage<localizes>(Label:string):message = "{Label} switch: turn ON"
    TurnOffMessage<localizes>(Label:string):message = "{Label} switch: turn OFF"

    var MaybeOnPrompt<private>:?message = false
    var MaybeOffPrompt<private>:?message = false

    # Prompts are built here because localized messages cannot be created in a transactional context.
    OnSimulate<override>()<suspends>:void =
        Label := if (Lamp := Entity.GetParent[].GetComponent[lamp_toggle_component]) then Lamp.DebugLabel else "Lamp"
        OnPrompt := TurnOnMessage(Label)
        OffPrompt := TurnOffMessage(Label)
        set MaybeOnPrompt = option{OnPrompt}
        set MaybeOffPrompt = option{OffPrompt}

    InteractMessage<override>(Agent:agent)<decides><reads>:message =
        Lamp := Entity.GetParent[].GetComponent[lamp_toggle_component]
        if (Lamp.IsLampOn[]) then MaybeOffPrompt? else MaybeOnPrompt?
