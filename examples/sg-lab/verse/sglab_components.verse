# SGLab: helper types for the Scene Graph runtime experiments (sglab_device.verse).

using { /Verse.org/Simulation }
using { /Verse.org/Simulation/Tags }
using { /Verse.org/SceneGraph }
using { /UnrealEngine.com/Temporary/Diagnostics }

# Tags are plain classes deriving from `tag`; subclasses form a hierarchy.
sglab_tag<public> := class(tag){}
sglab_red_tag<public> := class(sglab_tag){}

# A custom scene event; anything implementing `scene_event` can be sent with SendUp/SendDown.
sglab_ping_event<public> := class(scene_event):
    Payload<public>:string = ""

# Counts the scene events it receives. Returns false so propagation continues.
sglab_listener_component<public> := class<final_super>(component):
    var Received<public>:int = 0

    OnReceive<override>(SceneEvent:scene_event):logic =
        if (Ping := sglab_ping_event[SceneEvent]):
            set Received += 1
        false

# Counts PrePhysics ticks and accumulated delta time, to measure the server tick rate.
sglab_tick_counter_component<public> := class<final_super>(component):
    var Ticks<public>:int = 0
    var Elapsed<public>:float = 0.0
    var Subscription<private>:?cancelable = false

    OnBeginSimulation<override>():void =
        (super:)OnBeginSimulation()
        set Subscription = option{TickEvents.PrePhysics.Subscribe(OnTick)}

    OnEndSimulation<override>():void =
        if (S := Subscription?):
            S.Cancel()
        (super:)OnEndSimulation()

    OnTick(DeltaTime:float):void =
        set Ticks += 1
        set Elapsed += DeltaTime
