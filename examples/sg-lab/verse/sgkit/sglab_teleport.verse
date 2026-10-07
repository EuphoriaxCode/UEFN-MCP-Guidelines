# Teleport helper kept in its own file: fort_character.TeleportTo only takes the OLD
# /UnrealEngine.com/Temporary/SpatialMath types, and importing that module next to /Verse.org/SpatialMath
# makes `vector3`/`rotation` ambiguous. A qualified `(/UnrealEngine.com/Temporary/SpatialMath:)FromVector3`
# did not resolve without the `using`, so the conversion lives here.

using { /UnrealEngine.com/Temporary/SpatialMath }
using { /Fortnite.com/Characters }

# Teleport to (X forward, Y right, Z up) in Unreal world units, facing YawDegrees.
SGLabTeleport(Char:fort_character, X:float, Y:float, Z:float, YawDegrees:float)<transacts><decides>:void =
    Char.TeleportTo[vector3{X := X, Y := Y, Z := Z}, MakeRotationFromYawPitchRollDegrees(YawDegrees, 0.0, 0.0)]
