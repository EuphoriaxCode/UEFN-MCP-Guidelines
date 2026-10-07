"""Compact view of the Verse API digests that UEFN writes to disk.

    uefn digest SceneGraph                 # one module, compact signatures
    uefn digest --grep keyframed           # search every digest, show the enclosing class
    uefn digest --class mesh_component     # one class with comments

Digests live in %LOCALAPPDATA%/UnrealEditorFortnite/Saved/VerseProject/<Project>/Digests/BuiltIn/*/*.digest.verse
"""
import glob
import os
import re

ROOT = os.path.join(os.environ.get("LOCALAPPDATA", ""), "UnrealEditorFortnite", "Saved", "VerseProject")
NOISE = re.compile(r"<(native|public|native_callable|override|final|final_super|epic_internal|computes|"
                   r"concrete|castable|unique|abstract|persistable|open|closed|module_scoped_var_weak_map_key)>")


def digest_files(project=None):
    """Project digests exist only while the editor has the project open; VerseProject/FortniteGame/Digests/BuiltIn
    is a persistent copy of the built-in ones (same build), used as a fallback."""
    projects = sorted(glob.glob(os.path.join(ROOT, "*")), key=os.path.getmtime, reverse=True)
    projects = [p for p in projects if os.path.basename(p) != "FortniteGame"]
    if project:
        projects = [p for p in projects if os.path.basename(p).lower() == project.lower()] or projects
    for p in projects:
        files = glob.glob(os.path.join(p, "Digests", "BuiltIn", "*", "*.digest.verse"))
        if len(files) >= 3:
            return sorted(files) + glob.glob(os.path.join(p, "Digests", "*-Assets", "*.digest.verse"))
    return sorted(glob.glob(os.path.join(ROOT, "FortniteGame", "Digests", "BuiltIn", "*", "*.digest.verse")))


def _clean(line):
    s = NOISE.sub("", line.rstrip())
    s = s.replace(" = external {}", "")
    return s


def parse(path):
    """Yields (module_path, indent, kind, text, comment) records."""
    mod_stack = []  # (indent, name)
    comment = []
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("<#") or raw.strip() in ("#>",) or raw.startswith("Copyright"):
            continue
        ind = len(raw) - len(raw.lstrip(" "))
        s = raw.strip()
        if s.startswith("#"):
            c = s.lstrip("#").strip()
            if not (c.startswith("Verse path:") or c.startswith("Module import path:")):
                comment.append(c)
            continue
        if s.startswith("using {") or s.startswith("@available") or s.startswith("@experimental") or s.startswith("@deprecated"):
            if s.startswith("@experimental"):
                comment.append("[experimental]")
            continue
        while mod_stack and mod_stack[-1][0] >= ind:
            mod_stack.pop()
        m = re.match(r"(\w+)<public> := module:", s)
        if m:
            mod_stack.append((ind, m.group(1)))
            comment = []
            continue
        modpath = "/".join(n for _, n in mod_stack)
        kind = "class" if re.search(r":= (class|interface|struct|enum)\b", s) else "member"
        yield modpath, ind, kind, _clean(raw), " ".join(comment)
        comment = []


def module_view(name, files, with_comments=False, grep=None, cls=None):
    out = []
    for f in files:
        cur_class, cur_lines, cur_ind, keep = None, [], 0, False
        recs = list(parse(f))
        blocks = []
        for modpath, ind, kind, text, com in recs:
            if kind == "class" or (kind == "member" and ind <= cur_ind and cur_class is not None):
                if cur_lines:
                    blocks.append(cur_lines)
                cur_class, cur_lines, cur_ind = text, [], ind
                cur_lines.append((modpath, text, com))
                if kind != "class":
                    cur_class = None
                continue
            cur_lines.append((modpath, text, com))
        if cur_lines:
            blocks.append(cur_lines)
        for b in blocks:
            modpath = b[0][0]
            head = b[0][1]
            if name and not (modpath == name or modpath.startswith(name + "/") or modpath.split("/")[-1] == name):
                continue
            if cls and not re.search(r"\b" + re.escape(cls) + r"\b\s*(<[^>]*>)*\s*:=", head):
                continue
            body = "\n".join(t for _, t, _ in b)
            if grep and not re.search(grep, body + " " + " ".join(c for _, _, c in b), re.I):
                continue
            out.append(f"[{os.path.basename(f).split('.')[0]}:{modpath}]")
            for _, t, c in b:
                if with_comments and c:
                    out.append(" " * (len(t) - len(t.lstrip())) + "# " + c[:400])
                out.append(t)
            out.append("")
    return "\n".join(out)
