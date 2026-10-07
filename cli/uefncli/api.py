"""Toolset-level helpers on top of the MCP meta tools.

    tool("entity", "FindEntities", {...})  -> parsed returnValue (raises ToolError on isError)

Toolset names accept aliases (see ALIASES) or any unique suffix of the full name
("EntityToolset", "scene", "SceneTools").
"""
import json
import os
import re
import tempfile

from . import mcp

ALIASES = {
    "entity": "ValkyrieToolset.EntityToolset",
    "verse": "ValkyrieToolset.VerseToolset",
    "session": "ValkyrieToolset.SessionToolset",
    "device": "ValkyrieToolset.DeviceToolset",
    "python": "ValkyrieToolset.ValkyriePythonToolset",
    "editor": "EditorToolset.EditorAppToolset",
    "logs": "EditorToolset.LogsToolset",
    "umg": "UMGToolSet.UMGToolSet",
    "fields": "VerseFieldsToolset.VerseFieldsToolset",
    "mvvm": "MVVMToolset.MVVMToolset",
    "widgetanim": "WidgetAnimationToolset.WidgetAnimationToolset",
    "tags": "GameplayTagsToolset.GameplayTagsToolset",
    "physics": "PhysicsToolsets.PhysicsAssetToolset",
    "niagara": "NiagaraToolsets.NiagaraToolset_System",
    "niagara_comp": "NiagaraToolsets.NiagaraToolset_Component",
    "niagara_info": "NiagaraToolsets.NiagaraToolset_Info",
    "niagara_assets": "NiagaraToolsets.NiagaraToolset_Assets",
    "actor": "editor_toolset.toolsets.actor.ActorTools",
    "asset": "editor_toolset.toolsets.asset.AssetTools",
    "curve": "editor_toolset.toolsets.curve_table.CurveTableTools",
    "datatable": "editor_toolset.toolsets.data_table.DataTableTools",
    "material": "editor_toolset.toolsets.material.MaterialTools",
    "mi": "editor_toolset.toolsets.material_instance.MaterialInstanceTools",
    "object": "editor_toolset.toolsets.object.ObjectTools",
    "primitive": "editor_toolset.toolsets.primitive.PrimitiveTools",
    "scene": "editor_toolset.toolsets.scene.SceneTools",
    "skel": "editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools",
    "mesh": "editor_toolset.toolsets.static_mesh.StaticMeshTools",
    "script": "editor_toolset.toolsets.programmatic.ProgrammaticToolset",
    "texture": "editor_toolset.toolsets.texture.TextureTools",
}

CACHE = os.path.join(tempfile.gettempdir(), "uefn_toolsets.json")


class ToolError(RuntimeError):
    pass


def toolset_names(refresh=False):
    if not refresh and os.path.exists(CACHE):
        with open(CACHE) as f:
            return json.load(f)
    texts, _, _ = mcp.meta("list_toolsets", {})
    names = re.findall(r"^- ([A-Za-z0-9_.]+):", "\n".join(texts), re.M)
    with open(CACHE, "w") as f:
        json.dump(names, f)
    return names


def resolve(ts):
    """Alias / suffix / full name -> full toolset name. Unknown names pass through (hidden toolsets)."""
    if not ts:
        return ts
    if ts in ALIASES:
        return ALIASES[ts]
    names = toolset_names()
    if ts in names:
        return ts
    low = ts.lower()
    hits = [n for n in names if n.lower().endswith(low) or n.split(".")[-1].lower() == low]
    if len(hits) == 1:
        return hits[0]
    return ts


def raw(ts, name, args=None):
    """Returns (texts, images, is_error) for one toolset tool."""
    p = {"tool_name": name, "arguments": args or {}}
    if ts:
        p["toolset_name"] = resolve(ts)
    return mcp.meta("call_tool", p)


def unwrap(texts):
    s = "\n".join(texts)
    try:
        j = json.loads(s)
    except ValueError:
        return s
    if isinstance(j, dict) and set(j.keys()) == {"returnValue"}:
        return j["returnValue"]
    return j


def tool(ts, name, args=None):
    texts, _, err = raw(ts, name, args)
    if err:
        raise ToolError(f"{resolve(ts)}.{name}: " + "\n".join(texts)[:2000])
    return unwrap(texts)


def tool_images(ts, name, args=None):
    texts, images, err = raw(ts, name, args)
    if err:
        raise ToolError(f"{resolve(ts)}.{name}: " + "\n".join(texts)[:2000])
    return unwrap(texts), images


def describe(ts):
    texts, _, err = mcp.meta("describe_toolset", {"toolset_name": resolve(ts)})
    if err:
        raise ToolError("\n".join(texts))
    return json.loads("\n".join(texts))


def ref(path):
    return {"refPath": path}
