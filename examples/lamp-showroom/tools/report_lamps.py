# Prints every lamp instance with its hierarchy, overrides and prefab-driven values.
import json
from lamp_lib import *
for e in J(tool(E,"FindEntities",{"bRecursive":False})):
    if "Lamp" not in e["displayName"]: continue
    ent=e["entity"]; t=xf(ent)
    lamp=comp(ent,"LampShowroom-lamp_toggle_component")
    vals={p:getp(lamp,p) for p in ("DebugLabel","InitiallyOn","LightColor")} if lamp else {}
    print(f'{e["displayName"]}  class={e["entityClass"]["refPath"].split(".")[-1]}  at {t["location"]} yaw {t["rotation"]["yaw"]}')
    print("   lamp_toggle_component", json.dumps(vals))
    for k in children(ent):
        n=short(k["displayName"]); cs=[c["componentName"] for c in comps(k["entity"])]
        extra=""
        if n=="Base": extra=" scale="+json.dumps(xf(k["entity"])["scale"])
        if n=="Bulb": extra=" Intensity="+str(getp(comp(k["entity"],"sphere_light"),"Intensity"))
        print(f"   ├─ {n:12s} {cs}{extra}")
