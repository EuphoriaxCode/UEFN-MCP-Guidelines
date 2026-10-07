# Bridges between fort_character (old /UnrealEngine.com/Temporary/SpatialMath types) and Scene Graph code
# (/Verse.org/SpatialMath types).
# Verified UEFN 42.30: a qualified name like (/UnrealEngine.com/Temporary/SpatialMath:)FromVector3 only resolves when the
# module is ALSO imported with `using`. With both modules imported, every shared name (vector3, rotation,
# MakeRotationFromYawPitchRollDegrees...) is ambiguous, so qualify those explicitly.

using { /Verse.org/SpatialMath }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /Fortnite.com/Characters }

# Unreal-space position of a character as text (old vector3 has X/Y/Z fields).
SGLabCharPos(Char:fort_character)<transacts>:string =
    P := Char.GetTransform().Translation
    "({Floor[P.X] or 0}, {Floor[P.Y] or 0}, {Floor[P.Z] or 0})"

# Character position as a /Verse.org/SpatialMath vector3 (Forward/Left/Up) for Scene Graph code.
SGLabCharVec(Char:fort_character)<transacts>:(/Verse.org/SpatialMath:)vector3 =
    FromVector3(Char.GetTransform().Translation)

# Teleport to (X forward, Y right, Z up) in Unreal world units, facing YawDegrees.
SGLabTeleport(Char:fort_character, X:float, Y:float, Z:float, YawDegrees:float)<transacts><decides>:void =
    Char.TeleportTo[(/UnrealEngine.com/Temporary/SpatialMath:)vector3{X := X, Y := Y, Z := Z},
                    (/UnrealEngine.com/Temporary/SpatialMath:)MakeRotationFromYawPitchRollDegrees(YawDegrees, 0.0, 0.0)]
