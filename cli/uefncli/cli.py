"""uefn — command line for driving Unreal Editor for Fortnite through its MCP server.

Run `uefn -h` or `uefn <group> -h`. Every command prints JSON or compact text and exits non-zero on error.
"""
import argparse
import base64
import glob
import json
import os
import re
import sys
import time

from . import api, mcp, sg
from .xform import Xf, parse_vec

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIBS = os.path.join(REPO, "cli", "sandbox")
EDITOR_LOG = os.path.join(os.environ.get("LOCALAPPDATA", ""), "UnrealEditorFortnite", "Saved", "Logs", "UnrealEditorFortnite.log")
CLIENT_LOG = os.path.join(os.environ.get("LOCALAPPDATA", ""), "FortniteGame", "Saved", "Logs", "FortniteGame.log")


def out(x):
    if isinstance(x, str):
        print(x)
    else:
        print(json.dumps(x, indent=1, ensure_ascii=False))


def load_args(s):
    if not s:
        return {}
    if s.startswith("@"):
        with open(s[1:], encoding="utf-8") as f:
            return json.load(f)
    return json.loads(s)


# ------------------------------------------------------------------ generic
def c_status(a):
    t0 = time.time()
    names = api.toolset_names(refresh=True)
    r = {"mcp": mcp.URL, "toolsets": len(names), "latency_ms": int((time.time() - t0) * 1000)}
    try:
        r["session"] = api.tool("session", "GetSessionStatus")
        r["game"] = api.tool("session", "GetGameState")
    except Exception as e:
        r["session"] = f"? {e}"
    try:
        r["verse_roots"] = api.tool("verse", "ListFiles", {"path": "", "bRecursive": False})
    except Exception as e:
        r["verse_roots"] = f"? {e}"
    r["entities"] = len(api.tool("entity", "FindEntities", {}))
    out(r)


def c_wait(a):
    """Poll until the MCP server answers and the level's entity list is readable."""
    t0 = time.time()
    while time.time() - t0 < a.timeout:
        try:
            if os.path.exists(mcp.SID_FILE):
                os.remove(mcp.SID_FILE)
            n = len(api.tool("entity", "FindEntities", {}))
            print(f"ready after {time.time() - t0:.0f}s ({n} entities)")
            return
        except Exception:
            time.sleep(a.interval)
    sys.exit(f"timeout after {a.timeout}s")


PERF = {"refPath": "/Script/UnrealEd.Default__EditorPerformanceSettings"}


def c_turbo(a):
    """The editor throttles to ~3 FPS when not focused and serves one MCP call per frame (~333 ms/call).
    Turning bThrottleCPUWhenNotForeground off (in memory only; resets on restart) makes calls ~15 ms."""
    if a.state in ("on", "off"):
        api.tool("object", "set_properties", {"instance": PERF, "values": json.dumps({"bThrottleCPUWhenNotForeground": a.state == "off"})})
    t0 = time.time()
    for _ in range(5):
        api.tool("entity", "FindEntities", {"nameFilter": "__none__"})
    ms = (time.time() - t0) / 5 * 1000
    v = api.tool("object", "get_properties", {"instance": PERF, "properties": ["bThrottleCPUWhenNotForeground"]})
    out({"throttle_when_background": v, "ms_per_call": round(ms, 1)})


def c_toolsets(a):
    out(api.toolset_names(refresh=True))


def c_describe(a):
    d = api.describe(a.toolset)
    if a.tool:
        from .catalog import tool_md
        hits = [t for t in d["tools"] if t["name"].split(".")[-1].lower() == a.tool.lower()]
        out("\n".join(tool_md(t) for t in hits) or f"no tool {a.tool}")
    else:
        for t in sorted(d["tools"], key=lambda t: t["name"]):
            out(f"{t['name'].split('.')[-1]:34s} {t.get('description', '').strip().splitlines()[0][:110]}")


def c_call(a):
    texts, images, err = api.raw(a.toolset, a.tool, load_args(a.args))
    for i, img in enumerate(images):
        p = a.image or f"call_image_{i}.png"
        with open(p, "wb") as f:
            f.write(base64.b64decode(img["data"]))
        print(f"[image saved: {p}]", file=sys.stderr)
    out(api.unwrap(texts) if not a.raw else "\n".join(texts))
    if err:
        sys.exit(1)


def c_script(a):
    src = []
    for lib in a.lib or []:
        p = lib if os.path.exists(lib) else os.path.join(LIBS, lib + ".py")
        with open(p, encoding="utf-8") as f:
            src.append(f.read())
    with open(a.file, encoding="utf-8") as f:
        src.append(f.read())
    r = api.tool("script", "execute_tool_script", {"script": "\n\n".join(src)})
    if isinstance(r, str):
        try:
            r = json.loads(r)
        except ValueError:
            pass
    out(r)


def c_catalog(a):
    from . import catalog
    n = catalog.dump(os.path.join(REPO, "catalog"))
    print(f"{len(n)} toolsets -> catalog/")


def c_digest(a):
    from . import digest
    files = digest_files = digest.digest_files(a.project)
    if not files:
        sys.exit("no digests found")
    out(digest.module_view(a.module or "", digest_files, a.comments, a.grep, a.cls))


# ------------------------------------------------------------------ logs / images
def c_log(a):
    path = CLIENT_LOG if a.client else EDITOR_LOG
    with open(path, encoding="utf-8", errors="replace") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - a.bytes))
        lines = f.read().splitlines()
    if a.pattern:
        rx = re.compile(a.pattern, re.I)
        lines = [l for l in lines if rx.search(l)]
    if a.since:
        lines = [l for l in lines if l[1:20] >= a.since]
    for l in lines[-a.n:]:
        print(l[:a.width])


def _pose(at, look=None, rot=None, cur=None):
    """camera pose from --at + (--look point | --rot p,y,r); missing --at keeps the current camera location."""
    import math
    loc = parse_vec(at, None)
    if loc is None:
        cur = cur or api.tool("editor", "GetCameraTransform")
        loc = (cur["location"]["x"], cur["location"]["y"], cur["location"]["z"])
    if look:
        tx, ty, tz = parse_vec(look, (0, 0, 0))
        dx, dy, dz = tx - loc[0], ty - loc[1], tz - loc[2]
        r = (math.degrees(math.atan2(dz, math.hypot(dx, dy))), math.degrees(math.atan2(dy, dx)), 0.0)
    else:
        r = parse_vec(rot, (0, 0, 0))
    return {"location": dict(zip("xyz", loc)), "rotation": dict(zip(("pitch", "yaw", "roll"), r)),
            "scale": {"x": 1, "y": 1, "z": 1}}


def c_shot(a):
    """Capture from the editor viewport camera, or from an explicit pose (--at/--look) without moving the camera."""
    args = {}
    if a.labels:
        args["annotations"] = {}
    if a.at or a.look:
        args["captureTransform"] = _pose(a.at, a.look, a.rot)
    r, images = api.tool_images("editor", "CaptureViewport", args)
    if not images:
        out(r)
        sys.exit("no image returned")
    with open(a.out, "wb") as f:
        f.write(base64.b64decode(images[0]["data"]))
    print(a.out)


def client_capture(path):
    """Fortnite client window via PrintWindow (works when the window is behind others)."""
    import subprocess
    ps1 = os.path.join(REPO, "scripts", "windows", "capture_fortnite_window.ps1")
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1, "-Out", os.path.abspath(path)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not os.path.exists(path):
        raise RuntimeError("client capture failed: " + (r.stdout + r.stderr)[-400:])
    return path


def c_clip(a):
    """N client frames every --interval seconds; with Pillow installed also a contact sheet."""
    os.makedirs(a.dir, exist_ok=True)
    frames = []
    for i in range(a.frames):
        t0 = time.time()
        frames.append(client_capture(os.path.join(a.dir, f"{a.prefix}_{i:02d}.png")))
        time.sleep(max(0.0, a.interval - (time.time() - t0)))
    print("\n".join(frames))
    try:
        from PIL import Image
    except ImportError:
        return
    ims = [Image.open(f).convert("RGB") for f in frames]
    w = 640
    h = int(ims[0].height * w / ims[0].width)
    cols = min(a.cols, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    out_p = os.path.join(a.dir, f"{a.prefix}_sheet.jpg")
    sheet.save(out_p, quality=85)
    print(out_p)


def c_cam(a):
    if a.at is None and a.look is None:
        out(api.tool("editor", "GetCameraTransform"))
        return
    out(api.tool("editor", "SetCameraTransform", {"transform": _pose(a.at, a.look, a.rot)}))


# ------------------------------------------------------------------ verse
def project_root():
    roots = api.tool("verse", "ListFiles", {"path": "", "bRecursive": False})
    for r in roots if isinstance(roots, list) else []:
        p = r if isinstance(r, str) else r.get("path", "")
        if "(" not in p:
            return p.rstrip("/")
    return None


def c_verse(a):
    if a.op == "ls":
        out(api.tool("verse", "ListFiles", {"path": a.path or "", "bRecursive": bool(a.dest)}))
    elif a.op == "cat":
        out(api.tool("verse", "ReadFile", {"path": a.path}))
    elif a.op == "grep":
        out(api.tool("verse", "Grep", {"pattern": a.path, "path": a.dest or ""}))
    elif a.op == "rm":
        out(api.tool("verse", "Delete", {"path": a.path, "bRecursive": False}))
    elif a.op == "push":  # local file(s) -> project path
        files = sorted(glob.glob(a.path)) if any(ch in a.path for ch in "*?") else [a.path]
        dest = a.dest or project_root()
        for lf in files:
            with open(lf, encoding="utf-8") as f:
                content = f.read()
            target = dest.rstrip("/") + "/" + os.path.basename(lf) if not dest.endswith(".verse") else dest
            api.tool("verse", "WriteFile", {"path": target, "content": content, "bCreateIfMissing": True})
            print("wrote", target)
        if a.build:
            return c_build(a)
    elif a.op == "build":
        return c_build(a)


def c_build(a):
    t0 = time.time()
    r = api.tool("verse", "BuildAll", {})
    diags = r if isinstance(r, list) else r
    if not diags:
        print(f"BUILD OK ({time.time() - t0:.1f}s)")
        return
    if isinstance(diags, list):
        for d in diags:
            sp = d.get("span", {})
            f = d.get("filePath", "").rsplit("/", 1)[-1]
            print(f"{d.get('severity', '?')[0]} {f}:{sp.get('startLine', -1) + 1}:{sp.get('startCharacter', -1) + 1} "
                  f"[{d.get('code')}] {d.get('message', '')[:300]}")
    else:
        out(diags)
    sys.exit(1)


# ------------------------------------------------------------------ devices
def _device_ref(name):
    """placed Verse device by label substring (e.g. 'sglab2') -> ref"""
    if name.startswith("/"):
        return {"refPath": name}
    acts = api.tool("scene", "find_actors", {"collision_channels": []})
    hits = [x for x in acts if name.lower() in (x.get("label") or "").lower()]
    if len(hits) != 1:
        raise KeyError(f"device '{name}': {len(hits)} matches " + str([h.get('label') for h in hits][:8]))
    return {"refPath": hits[0]["actorPath"]}


def c_device(a):
    if a.op == "ls":  # catalog (placeable assets)
        for d in api.tool("device", "ListDeviceAssets", {"nameFilter": a.target or ""}):
            print(f"{d['displayName']:60s} {'verse ' if d['bIsVerseDevice'] else 'device'} {d['assetPath']['refPath']}")
    elif a.op == "placed":
        for x in api.tool("scene", "find_actors", {"collision_channels": []}):
            cls = x["class"]["refPath"]
            if "Device" in cls or "VerseDevice" in cls:
                if not a.target or a.target.lower() in (x.get("label") or "").lower():
                    print(f"{x.get('label', ''):45s} {cls.split('.')[-1]:40s} {x['actorPath']}")
    elif a.op == "place":
        assets = api.tool("device", "ListDeviceAssets", {"nameFilter": a.target})
        exact = [d for d in assets if d["displayName"].lower().endswith(a.target.lower())] or assets
        if not exact:
            sys.exit(f"no device asset matching {a.target}")
        xf = Xf(parse_vec(a.at, (0, 0, 384)), parse_vec(a.rot, (0, 0, 0)), parse_vec(a.scale, (1, 1, 1)))
        out(api.tool("device", "PlaceDevice", {"assetPath": exact[0]["assetPath"], "transform": xf.to_json()}))
    elif a.op == "props":
        out(api.tool("device", "ListDeviceProperties", {"device": _device_ref(a.target)}))
    elif a.op == "get":
        out(api.tool("device", "GetDeviceProperties", {"device": _device_ref(a.target), "propertyNames": a.prop.split(",")}))
    elif a.op == "set":
        out(api.tool("device", "SetDeviceProperty", {"device": _device_ref(a.target), "propertyName": a.prop,
                                                     "value": sg.jval(a.value)}))


# ------------------------------------------------------------------ session
def c_session(a):
    S = "session"
    if a.op == "status":
        out({"session": api.tool(S, "GetSessionStatus"), "game": api.tool(S, "GetGameState")})
    elif a.op == "start":
        out(api.tool(S, "StartSession"))
    elif a.op == "stop":
        out(api.tool(S, "StopSession"))
    elif a.op == "push":
        out(api.tool(S, "PushChanges", {"bVerseOnly": a.verse_only}))
    elif a.op == "game-start":
        out(api.tool(S, "StartGame"))
    elif a.op == "game-stop":
        out(api.tool(S, "StopGame"))
    elif a.op == "restart":  # push + restart the round, the common edit loop
        if api.tool(S, "GetSessionStatus") != "Connected":
            out(api.tool(S, "StartSession"))
        else:
            try:
                out(api.tool(S, "PushChanges", {"bVerseOnly": a.verse_only}))
            except api.ToolError as e:  # "The Refresh command is not currently available" for Verse-only pushes
                if not a.verse_only:
                    raise
                print(f"verse-only push refused ({str(e)[-80:]}); doing a full push", file=sys.stderr)
                out(api.tool(S, "PushChanges", {"bVerseOnly": False}))
        if api.tool(S, "GetGameState") == "Running":
            api.tool(S, "StopGame")
        for _ in range(120):
            st = api.tool(S, "GetGameState")
            if st == "CanStart":
                break
            time.sleep(1)
        out(api.tool(S, "StartGame"))


# ------------------------------------------------------------------ scene graph
def _tree_lines(scene, ref, depth, comps, maxdepth):
    lines = []
    for k in sorted(scene.children(ref), key=lambda e: e["displayName"]):
        name = sg.short(k["displayName"])
        cls = k["entityClass"]["refPath"].split(".")[-1]
        extra = f" <{cls}>" if cls != "entity" else ""
        if comps:
            try:
                cs = [c["componentName"] for c in sg.comps(k) if not c["componentName"].startswith("transform_component")]
            except api.ToolError:
                cs = ["<gone>"]
            extra += "  [" + ", ".join(cs) + "]" if cs else ""
        lines.append("  " * depth + name + extra)
        if maxdepth is None or depth + 1 < maxdepth:
            lines += _tree_lines(scene, k["entity"]["refPath"], depth + 1, comps, maxdepth)
    return lines


def sg_build_fast(spec, parent_ref=None):
    names = set()

    def walk(nodes):
        for n in nodes if isinstance(nodes, list) else [nodes]:
            names.update((n.get("components") or {}).keys())
            walk(n.get("children") or [])
    walk(spec)
    classes = {n: sg.comp_class(n) for n in names}
    with open(os.path.join(LIBS, "sg_build.py"), encoding="utf-8") as f:
        lib = f.read()
    script = (lib + "\n\nSPEC = json.loads(" + repr(json.dumps(spec)) + ")\nPARENT = " + repr(parent_ref) +
              "\nCOMP_CLASSES = json.loads(" + repr(json.dumps(classes)) + ")\n")
    t0 = time.time()
    r = api.tool("script", "execute_tool_script", {"script": script})
    if isinstance(r, str):
        try:
            r = json.loads(r)
        except ValueError:
            pass
    if isinstance(r, dict):
        r["seconds"] = round(time.time() - t0, 2)
    return r


def c_sg(a):
    scene = sg.Scene()
    op = a.op
    if op == "tree":
        root = scene.resolve(a.target)["entity"]["refPath"] if a.target else None
        lines = _tree_lines(scene, root, 0, a.comps, a.depth)
        print("\n".join(lines) or "(no entities)")
    elif op == "classes":
        cls = sg.component_classes(refresh=True) if not a.entities else api.tool("entity", "ListEntityClasses", {"nameFilter": a.target or ""})
        for c in cls:
            if a.target and a.target.lower() not in c["className"].lower():
                continue
            print(f"{c['className']:60s} {c['classPath']['refPath']}{'  (prefab)' if c['bIsPrefab'] else ''}")
    elif op == "comps":
        e = scene.resolve(a.target)
        for c in sg.comps(e):
            print(f"{c['componentName']:50s} {c['componentClass']['refPath']}")
    elif op == "props":
        e = scene.resolve(a.target)
        c = sg.find_comp(e, a.comp)
        if not c:
            sys.exit(f"no component {a.comp} on {a.target}")
        for p in api.tool("entity", "ListComponentProperties", {"component": c["component"]}):
            print(f"{p['name']:32s} {p['type']:28s} {p['value'][:100]}{'  (ro)' if p.get('bReadOnly') else ''}")
    elif op == "get":
        c = sg.find_comp(scene.resolve(a.target), a.comp)
        out(sg.get_prop(c, a.prop))
    elif op == "set":
        c = sg.find_comp(scene.resolve(a.target), a.comp)
        out(sg.set_prop(c, a.prop, a.value))
    elif op == "add":
        e = scene.resolve(a.target)
        for name in a.comp.split(","):
            r = sg.add_comp(e, name)
            print("added", r["componentName"])
    elif op == "rmcomp":
        e = scene.resolve(a.target)
        out(api.tool("entity", "RemoveComponent", {"entity": e["entity"], "componentClass": {"refPath": sg.comp_class(a.comp)}}))
    elif op == "new":
        parent = None
        name = a.target
        if "/" in a.target:
            ppath, name = a.target.rsplit("/", 1)
            parent = scene.resolve(ppath)
        xf = Xf(parse_vec(a.at, (0, 0, 0)), parse_vec(a.rot, (0, 0, 0)), parse_vec(a.scale, (1, 1, 1)))
        r = sg.create(name, parent, xf, a.cls)
        print("created", r["displayName"])
        if a.comp:
            e = {"entity": r["entity"]}
            for cn in a.comp.split(","):
                print("  +", sg.add_comp(e, cn)["componentName"])
    elif op == "rm":
        e = scene.resolve(a.target)
        out(api.tool("entity", "DeleteEntity", {"entity": e["entity"]}))
    elif op == "xf":
        e = scene.resolve(a.target)
        if a.at is None and a.rot is None and a.scale is None:
            print("world", sg.world(e))
            print("local", sg.local(scene, e))
            return
        cur = sg.world(e) if a.world else sg.local(scene, e)
        nx = Xf(parse_vec(a.at, cur.loc), parse_vec(a.rot, cur.rot), parse_vec(a.scale, cur.scale))
        (sg.set_world(e, nx) if a.world else sg.set_local(scene, e, nx))
        print("world", sg.world(e))
    elif op == "stamp":  # sg stamp template.json Parent/Name --at .. --set Bulb.light.Intensity=400
        ov = {}
        for s_ in a.set or []:
            rel, comp, prop, v = sg.parse_override(s_)
            ov.setdefault(rel, {}).setdefault(comp, {})[prop] = v
        st = sg.stamp(a.target, a.comp, parse_vec(a.at, None), parse_vec(a.rot, None),
                      parse_vec(a.scale, None) if a.scale else None, ov)
        out(st)
    elif op == "propagate":
        out(sg.propagate(a.target, a.prune))
    elif op == "build":  # create-only, whole spec in ONE sandbox call (fast path for big generated scenes)
        spec = load_args("@" + a.target) if not a.target.lstrip().startswith(("{", "[")) else json.loads(a.target)
        out(sg_build_fast(spec, scene.resolve(a.parent)["entity"]["refPath"] if a.parent else None))
    elif op == "apply":
        spec = load_args("@" + a.target)
        st = sg.apply(spec, a.parent, a.prune, scene=scene)
        out(st)
    elif op == "dump":
        e = scene.resolve(a.target)
        out(sg.dump(scene, e, a.props))
    elif op == "atlas":
        from . import atlas
        p = os.path.join(REPO, "catalog", "scene-graph", "component-atlas.json")
        d = atlas.build(p, a.target or "")
        with open(p.replace(".json", ".md"), "w", encoding="utf-8") as f:
            f.write(atlas.to_markdown(d))


def main(argv=None):
    p = argparse.ArgumentParser(prog="uefn", description="Drive UEFN through its MCP server.")
    s = p.add_subparsers(dest="cmd", required=True)

    s.add_parser("status", help="server/session/project summary").set_defaults(f=c_status)
    x = s.add_parser("wait", help="block until the editor's MCP server is up (e.g. after a crash/restart)")
    x.add_argument("--timeout", type=float, default=1800); x.add_argument("--interval", type=float, default=5)
    x.set_defaults(f=c_wait)
    x = s.add_parser("turbo", help="on = stop the background 3 FPS throttle (~20x faster MCP calls, until restart)")
    x.add_argument("state", nargs="?", choices=["on", "off"]); x.set_defaults(f=c_turbo)
    s.add_parser("toolsets", help="list toolsets").set_defaults(f=c_toolsets)
    x = s.add_parser("describe", help="list tools of a toolset, or one tool's schema")
    x.add_argument("toolset"); x.add_argument("tool", nargs="?"); x.set_defaults(f=c_describe)
    x = s.add_parser("call", help="call any tool: uefn call entity FindEntities '{\"nameFilter\":\"Lamp\"}'")
    x.add_argument("toolset"); x.add_argument("tool"); x.add_argument("args", nargs="?", help="JSON or @file.json")
    x.add_argument("--raw", action="store_true"); x.add_argument("--image", help="save returned image here")
    x.set_defaults(f=c_call)
    x = s.add_parser("script", help="run a sandbox script (execute_tool_script); --lib prepends cli/sandbox/<lib>.py")
    x.add_argument("file"); x.add_argument("--lib", action="append"); x.set_defaults(f=c_script)
    s.add_parser("catalog", help="regenerate catalog/ from the live server").set_defaults(f=c_catalog)
    x = s.add_parser("digest", help="compact Verse API from the on-disk digests")
    x.add_argument("module", nargs="?", help="e.g. SceneGraph, Devices, SceneGraph/KeyframedMovement")
    x.add_argument("--grep"); x.add_argument("--class", dest="cls"); x.add_argument("--comments", action="store_true")
    x.add_argument("--project"); x.set_defaults(f=c_digest)

    x = s.add_parser("log", help="tail the editor (or --client) log with a regex filter")
    x.add_argument("pattern", nargs="?"); x.add_argument("-n", type=int, default=40)
    x.add_argument("--client", action="store_true"); x.add_argument("--bytes", type=int, default=4_000_000)
    x.add_argument("--since", help="timestamp prefix like 2026.10.07-19.00"); x.add_argument("--width", type=int, default=400)
    x.set_defaults(f=c_log)
    x = s.add_parser("shot", help="capture the editor viewport to a PNG")
    x.add_argument("out", nargs="?", default="viewport.png"); x.add_argument("--labels", action="store_true")
    x.add_argument("--at", help="capture from x,y,z (camera not moved)"); x.add_argument("--look", help="aim at x,y,z")
    x.add_argument("--rot", help="or explicit pitch,yaw,roll")
    x.set_defaults(f=c_shot)
    x = s.add_parser("clip", help="burst-capture the Fortnite client window (+ contact sheet)")
    x.add_argument("--frames", type=int, default=6); x.add_argument("--interval", type=float, default=1.0)
    x.add_argument("--dir", default="clip"); x.add_argument("--prefix", default="frame"); x.add_argument("--cols", type=int, default=3)
    x.set_defaults(f=c_clip)
    x = s.add_parser("cam", help="get/set the editor camera; --look x,y,z aims at a point")
    x.add_argument("--at"); x.add_argument("--rot"); x.add_argument("--look")
    x.set_defaults(f=c_cam)

    x = s.add_parser("verse", help="ls|cat|grep|rm|push|build Verse files")
    x.add_argument("op", choices=["ls", "cat", "grep", "rm", "push", "build"]); x.add_argument("path", nargs="?")
    x.add_argument("dest", nargs="?"); x.add_argument("--build", action="store_true"); x.set_defaults(f=c_verse)
    s.add_parser("build", help="BuildAll Verse; exit 1 with diagnostics on failure").set_defaults(f=c_build)

    x = s.add_parser("device", help="ls [filter] | placed [label] | place <asset> --at | props|get|set <label> [prop] [value]")
    x.add_argument("op", choices=["ls", "placed", "place", "props", "get", "set"]); x.add_argument("target", nargs="?")
    x.add_argument("prop", nargs="?"); x.add_argument("value", nargs="?")
    x.add_argument("--at"); x.add_argument("--rot"); x.add_argument("--scale"); x.set_defaults(f=c_device)

    x = s.add_parser("session", help="status|start|stop|push|game-start|game-stop|restart")
    x.add_argument("op", choices=["status", "start", "stop", "push", "game-start", "game-stop", "restart"])
    x.add_argument("--verse-only", action="store_true"); x.set_defaults(f=c_session)

    x = s.add_parser("sg", help="Scene Graph: tree|classes|comps|props|get|set|add|rmcomp|new|rm|xf|apply|dump|atlas|stamp|propagate")
    x.add_argument("op", choices=["tree", "classes", "comps", "props", "get", "set", "add", "rmcomp", "new", "rm", "xf",
                                  "apply", "dump", "atlas", "stamp", "propagate", "build"])
    x.add_argument("target", nargs="?", help="entity path (Showroom/BackWall), class filter, or spec file")
    x.add_argument("comp", nargs="?"); x.add_argument("prop", nargs="?"); x.add_argument("value", nargs="?")
    x.add_argument("--comps", action="store_true", help="tree: show components")
    x.add_argument("--depth", type=int); x.add_argument("--entities", action="store_true", help="classes: entity classes")
    x.add_argument("--at"); x.add_argument("--rot"); x.add_argument("--scale")
    x.add_argument("--world", action="store_true", help="xf: values are world space (default local)")
    x.add_argument("--comp", dest="comp_opt"); x.add_argument("--cls", help="new: entity class refPath (e.g. a prefab)")
    x.add_argument("--parent", help="apply: parent entity path"); x.add_argument("--prune", action="store_true")
    x.add_argument("--props", action="store_true", help="dump: include property values")
    x.add_argument("--set", action="append", help="stamp: override Child/Path.component.Property=json (root: .comp.Prop=..)")
    x.set_defaults(f=c_sg)

    # Git Bash (MSYS) rewrites arguments that start with "/" into Windows paths: undo that for Verse/asset paths.
    argv = [re.sub(r"^[A-Za-z]:/Program Files/Git(?=/)", "", s) for s in (argv if argv is not None else sys.argv[1:])]
    a = p.parse_args(argv)
    if getattr(a, "comp_opt", None):
        a.comp = a.comp_opt
    try:
        a.f(a)
    except (api.ToolError, mcp.McpError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
