# Run after PF_Lamp exists: places/reuses six prefab instances and applies per-lamp overrides.
import json
from lamp_lib import *
COLORS={"Red":'{"r":1.0,"g":0.02,"b":0.02}',"Green":'{"r":0.02,"g":1.0,"b":0.05}',"Blue":'{"r":0.05,"g":0.15,"b":1.0}'}
SLOTS=[("A1",-500,-300,"Red",True),("A2",0,-300,"Green",False),("A3",500,-300,"Blue",True),
       ("B1",-500,-800,"Red",False),("B2",0,-800,"Green",True),("B3",500,-800,"Blue",False)]
prefabs=[c for c in J(tool(E,"ListEntityClasses",{"nameFilter":"Lamp"})) if c["bIsPrefab"]]
if not prefabs: raise SystemExit("No lamp prefab class found - create PF_Lamp first and Build Verse.")
cls=prefabs[0]["classPath"]; print("prefab class",cls)
inst=[e for e in J(tool(E,"FindEntities",{"bRecursive":False})) if e["entityClass"]["refPath"]==cls["refPath"]]
def near(x,y):
    for e in inst:
        l=xf(e["entity"])["location"]
        if abs(l["x"]-x)<5 and abs(l["y"]-y)<5: return e["entity"]
for label,x,y,color,on in SLOTS:
    ent=near(x,y)
    if not ent:
        ent=J(tool(E,"CreateEntity",{"entityClass":cls,"name":f"Lamp_{label}","transform":T(x,y,384)}))["entity"]
    lamp=comp(ent,"LampShowroom-lamp_toggle_component")
    print(label, setp(lamp,"InitiallyOn","true" if on else "false"), setp(lamp,"LightColor",COLORS[color]), setp(lamp,"DebugLabel",json.dumps(f"{label} {color}")))
    # editor preview of the configured initial state (runtime Verse applies the same values)
    for k in children(ent):
        if short(k["displayName"])=="Bulb":
            setp(comp(k["entity"],"sphere_light"),"Enabled","true" if on else "false")
            setp(comp(k["entity"],"sphere_light"),"ColorFilter",COLORS[color])
            setp(comp(k["entity"],"BasicShapes_sphere"),"Visible","true" if on else "false")
print(tool("editor_toolset.toolsets.asset.AssetTools","save_assets",{"asset_paths":[]}))
