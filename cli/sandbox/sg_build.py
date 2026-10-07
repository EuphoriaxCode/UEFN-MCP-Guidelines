# Sandbox-side Scene Graph builder (runs INSIDE execute_tool_script, so the whole build is one MCP round-trip).
# The CLI prepends this file and appends:  SPEC = <json>; PARENT = <refPath or None>; COMP_CLASSES = {...}
# Only json/math are used. Transforms in the spec are LOCAL; CreateEntity(parentEntity=..) takes local directly.
import json
import math

ET = "ValkyrieToolset.EntityToolset."


def _t(name, args):
    return execute_tool(ET + name, json.dumps(args))


def _rv(r):
    return r["returnValue"] if isinstance(r, dict) and "returnValue" in r else r


def _vec(v, d):
    if v is None:
        return d
    if isinstance(v, (int, float)):
        return [float(v)] * 3
    return [float(x) for x in v]


def _xf(n):
    l = _vec(n.get("at"), [0.0, 0.0, 0.0])
    r = _vec(n.get("rot"), [0.0, 0.0, 0.0])
    s = _vec(n.get("scale"), [1.0, 1.0, 1.0])
    return {"location": {"x": l[0], "y": l[1], "z": l[2]}, "rotation": {"pitch": r[0], "yaw": r[1], "roll": r[2]},
            "scale": {"x": s[0], "y": s[1], "z": s[2]}}


def _expand(nodes):
    out = []
    for n in nodes:
        r = n.get("repeat")
        if not r:
            out.append(n)
            continue
        for i in range(int(r["count"])):
            m = json.loads(json.dumps(n))
            m.pop("repeat")
            m["name"] = r.get("name", n["name"] + "_{i}").replace("{i}", str(i)).replace("{n}", str(i + 1))
            base = _vec(m.get("at"), [0.0, 0.0, 0.0])
            step = _vec(r.get("step"), [0.0, 0.0, 0.0])
            m["at"] = [base[k] + step[k] * i for k in range(3)]
            if "yaw_step" in r:
                rot = _vec(m.get("rot"), [0.0, 0.0, 0.0])
                rot[1] += r["yaw_step"] * i
                m["rot"] = rot
            out.append(m)
    return out


def _js(v):
    return v if isinstance(v, str) and v[:1] in "{[\"" else json.dumps(v)


STATS = {"entities": 0, "components": 0, "props": 0, "errors": []}


def build(nodes, parent_ref):
    for n in _expand(nodes):
        args = {"entityClass": {"refPath": n.get("class", "/EntityFramework/_Verse/VNI/Entity.entity")},
                "name": n["name"], "transform": _xf(n)}
        if parent_ref:
            args["parentEntity"] = {"refPath": parent_ref}
        try:
            ent = _rv(_t("CreateEntity", args))["entity"]
        except Exception as e:
            STATS["errors"].append("create " + n["name"] + ": " + str(e)[:200])
            continue
        STATS["entities"] += 1
        for cname, props in (n.get("components") or {}).items():
            try:
                c = _rv(_t("AddComponent", {"entity": ent, "componentClass": {"refPath": COMP_CLASSES[cname]}}))
                STATS["components"] += 1
            except Exception as e:
                STATS["errors"].append("add " + cname + " on " + n["name"] + ": " + str(e)[:200])
                continue
            for p, v in (props or {}).items():
                try:
                    _t("SetComponentProperty", {"component": c["component"], "propertyName": p, "value": _js(v)})
                    STATS["props"] += 1
                except Exception as e:
                    STATS["errors"].append("set " + n["name"] + "." + cname + "." + p + ": " + str(e)[:200])
        if n.get("children"):
            build(n["children"], ent["refPath"])


def run():
    nodes = SPEC if isinstance(SPEC, list) else [SPEC]
    build(nodes, PARENT)
    STATS["errors"] = STATS["errors"][:30]
    return STATS
