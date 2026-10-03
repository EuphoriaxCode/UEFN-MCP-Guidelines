# Rotates/moves a lamp root and checks every child against root + R(yaw) * localOffset, then restores it.
import math
from lamp_lib import *
root=find("Lamp_Source")[0]["entity"]
kids={short(k["displayName"]):k["entity"] for k in children(root)}
local={"Base":(0,0,65),"Bulb":(0,0,155),"Switch":(35,0,45),"SwitchLever":(50,0,45)}
def check(rx,ry,rz,yaw):
    setxf(root,T(rx,ry,rz,yaw=yaw))
    ok=True; a=math.radians(yaw)
    for n,(lx,ly,lz) in local.items():
        exp=(rx+lx*math.cos(a)-ly*math.sin(a), ry+lx*math.sin(a)+ly*math.cos(a), rz+lz)
        g=xf(kids[n])["location"]
        err=max(abs(g["x"]-exp[0]),abs(g["y"]-exp[1]),abs(g["z"]-exp[2])); ok&=err<0.5
        print(f"  {n:12s} got ({g['x']:.1f},{g['y']:.1f},{g['z']:.1f}) expected ({exp[0]:.1f},{exp[1]:.1f},{exp[2]:.1f}) err {err:.3f}")
    print("  RESULT", "PASS" if ok else "FAIL")
check(-300,-150,384,45)
check(-500,-300,384,0)
