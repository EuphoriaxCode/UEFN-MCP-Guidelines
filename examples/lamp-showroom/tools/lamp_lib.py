import json
from t import tool
E="ValkyrieToolset.EntityToolset"
def J(s):
    if s.startswith("ISERROR"): raise RuntimeError(s[:600])
    return json.loads(s)["returnValue"]
def T(x,y,z,s=(1,1,1),yaw=0,pitch=0,roll=0): return {"location":{"x":x,"y":y,"z":z},"rotation":{"pitch":pitch,"yaw":yaw,"roll":roll},"scale":{"x":s[0],"y":s[1],"z":s[2]}}
C={"cube":"/VerseEngineAssets/_Verse/VNI/VerseEngineAssets.BasicShapes_cube",
   "sphere":"/VerseEngineAssets/_Verse/VNI/VerseEngineAssets.BasicShapes_sphere",
   "cylinder":"/VerseEngineAssets/_Verse/VNI/VerseEngineAssets.BasicShapes_cylinder",
   "light":"/EntityFramework/_Verse/VNI/Component.sphere_light_component",
   "interact":"/EntityInteract/_Verse/VNI/EntityInteract.basic_interactable_component",
   "lamp":"/ca93dbca-6f58-4ce8-9bd2-c953b1864acf/_Verse.LampShowroom-lamp_toggle_component",
   "switch":"/ca93dbca-6f58-4ce8-9bd2-c953b1864acf/_Verse.LampShowroom-lamp_switch_component",
   "indicator":"/ca93dbca-6f58-4ce8-9bd2-c953b1864acf/_Verse.LampShowroom-lamp_state_indicator_component"}
ENT={"refPath":"/EntityFramework/_Verse/VNI/Entity.entity"}
def find(name,root=None,rec=True):
    a={"nameFilter":name,"bRecursive":rec}
    if root: a["rootEntity"]=root
    return J(tool(E,"FindEntities",a))
def children(root): return J(tool(E,"FindEntities",{"rootEntity":root,"bRecursive":False}))
def comps(e): return J(tool(E,"GetComponents",{"entity":e}))
def comp(e,prefix):
    for c in comps(e):
        if c["componentName"].startswith(prefix): return c["component"]
def setp(c,p,v): return tool(E,"SetComponentProperty",{"component":c,"propertyName":p,"value":v})
def getp(c,p): return J(tool(E,"GetComponentProperty",{"component":c,"propertyName":p}))
def xf(e): return J(tool(E,"GetEntityTransform",{"entity":e}))
def setxf(e,t): return tool(E,"SetEntityTransform",{"entity":e,"transform":t})
def short(n): return n.split("_")[0]
