# Lamp showroom: a part that moves to show the lamp's on/off state (the switch lever).
#
# Offsets are applied to the entity's LocalTransform, so the indicator stays aligned
# however the lamp root is moved or rotated.

using { /Verse.org/Simulation }
using { /Verse.org/SceneGraph }
using { /Verse.org/SpatialMath }

lamp_state_indicator_component<public> := class<final_super>(component):

    @editable
    OnOffset<public>:vector3 = vector3{Left := 0.0, Up := 9.0, Forward := 0.0}

    @editable
    OffOffset<public>:vector3 = vector3{Left := 0.0, Up := -9.0, Forward := 0.0}

    var MaybeRestTransform<private>:?transform = false

    ShowState<public>(On:logic):void =
        Rest := MaybeRestTransform? or CaptureRest()
        Offset := if (On?) then OnOffset else OffOffset
        Entity.SetLocalTransform(transform{Translation := Rest.Translation + Offset, Rotation := Rest.Rotation, Scale := Rest.Scale})

    CaptureRest<private>():transform =
        Rest := Entity.GetLocalTransform()
        set MaybeRestTransform = option{Rest}
        Rest
