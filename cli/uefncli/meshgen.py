"""Procedural OBJ meshes for building Scene Graph kits (import with StaticMeshTools.import_file).

Units are centimetres, Z up, X forward (Unreal). Every mesh uses ONE material slot named by `mat`
so the generated Verse mesh component exposes a single `@editable var <mat>:material`.
Pivot: 'center' (default) or 'bottom'.
"""
import math


class Obj:
    def __init__(self):
        self.v, self.vt, self.vn, self.f = [], [], [], []

    def vert(self, p, uv, n):
        self.v.append(p)
        self.vt.append(uv)
        self.vn.append(n)
        return len(self.v)

    def tri(self, a, b, c):
        self.f.append((a, b, c))

    def quad(self, a, b, c, d):
        self.tri(a, b, c)
        self.tri(a, c, d)

    def text(self, mat):
        # OBJ is right-handed Y-up by convention; UE's OBJ importer maps (x, y, z)_obj -> (x, -z, y)_ue.
        # We write UE coordinates converted back so the asset lands Z-up, X-forward.
        L = [f"# uefn-cli meshgen", f"mtllib {mat}.mtl", f"o {mat}"]
        for x, y, z in self.v:
            L.append(f"v {x:.4f} {z:.4f} {-y:.4f}")
        for u, w in self.vt:
            L.append(f"vt {u:.5f} {1 - w:.5f}")
        for x, y, z in self.vn:
            L.append(f"vn {x:.5f} {z:.5f} {-y:.5f}")
        L.append(f"usemtl {mat}")
        L.append("s off")
        for a, b, c in self.f:
            L.append(f"f {a}/{a}/{a} {b}/{b}/{b} {c}/{c}/{c}")
        return "\n".join(L) + "\n"


def _norm(v):
    l = math.sqrt(sum(c * c for c in v)) or 1
    return tuple(c / l for c in v)


def box(sx=100, sy=100, sz=100, pivot="center"):
    o = Obj()
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    z0 = 0 if pivot == "center" else hz
    faces = [((1, 0, 0), (0, 1, 0), (0, 0, 1)), ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
             ((0, 1, 0), (-1, 0, 0), (0, 0, 1)), ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
             ((0, 0, 1), (0, 1, 0), (-1, 0, 0)), ((0, 0, -1), (0, 1, 0), (1, 0, 0))]
    for n, u, w in faces:
        c = (n[0] * hx, n[1] * hy, n[2] * hz + z0)
        ext = lambda d: (abs(d[0]) * hx + abs(d[1]) * hy + abs(d[2]) * hz)
        eu, ew = ext(u), ext(w)
        pts = []
        for su, sw, uv in ((-1, -1, (0, 1)), (1, -1, (1, 1)), (1, 1, (1, 0)), (-1, 1, (0, 0))):
            p = tuple(c[i] + u[i] * eu * su + w[i] * ew * sw for i in range(3))
            pts.append(o.vert(p, uv, n))
        # counter-clockwise seen from outside (Unreal front faces are clockwise after the handedness flip)
        o.quad(pts[0], pts[3], pts[2], pts[1])
    return o


def sphere(r=50, seg=32, rings=16, pivot="center"):
    o = Obj()
    z0 = 0 if pivot == "center" else r
    idx = {}
    for i in range(rings + 1):
        th = math.pi * i / rings
        for j in range(seg + 1):
            ph = 2 * math.pi * j / seg
            n = (math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th))
            idx[i, j] = o.vert((n[0] * r, n[1] * r, n[2] * r + z0), (j / seg, i / rings), n)
    for i in range(rings):
        for j in range(seg):
            a, b, c, d = idx[i, j], idx[i, j + 1], idx[i + 1, j + 1], idx[i + 1, j]
            o.quad(a, d, c, b)
    return o


def cylinder(r=50, h=100, seg=32, pivot="center", r_top=None):
    o = Obj()
    rt = r if r_top is None else r_top
    z_lo = -h / 2 if pivot == "center" else 0
    z_hi = z_lo + h
    slope = (r - rt) / h
    for j in range(seg):
        a0, a1 = 2 * math.pi * j / seg, 2 * math.pi * (j + 1) / seg
        n0 = _norm((math.cos(a0), math.sin(a0), slope))
        n1 = _norm((math.cos(a1), math.sin(a1), slope))
        p = [o.vert((r * math.cos(a0), r * math.sin(a0), z_lo), (j / seg, 1), n0),
             o.vert((r * math.cos(a1), r * math.sin(a1), z_lo), ((j + 1) / seg, 1), n1),
             o.vert((rt * math.cos(a1), rt * math.sin(a1), z_hi), ((j + 1) / seg, 0), n1),
             o.vert((rt * math.cos(a0), rt * math.sin(a0), z_hi), (j / seg, 0), n0)]
        o.quad(p[0], p[3], p[2], p[1])
    for z, rr, n in ((z_hi, rt, (0, 0, 1)), (z_lo, r, (0, 0, -1))):
        if rr <= 0:
            continue
        c = o.vert((0, 0, z), (0.5, 0.5), n)
        for j in range(seg):
            a0, a1 = 2 * math.pi * j / seg, 2 * math.pi * (j + 1) / seg
            p0 = o.vert((rr * math.cos(a0), rr * math.sin(a0), z), (0.5 + 0.5 * math.cos(a0), 0.5 + 0.5 * math.sin(a0)), n)
            p1 = o.vert((rr * math.cos(a1), rr * math.sin(a1), z), (0.5 + 0.5 * math.cos(a1), 0.5 + 0.5 * math.sin(a1)), n)
            if n[2] > 0:
                o.tri(c, p1, p0)
            else:
                o.tri(c, p0, p1)
    return o


def torus(R=50, r=15, seg=48, sides=16):
    o = Obj()
    idx = {}
    for i in range(seg + 1):
        u = 2 * math.pi * i / seg
        for j in range(sides + 1):
            v = 2 * math.pi * j / sides
            n = (math.cos(u) * math.cos(v), math.sin(u) * math.cos(v), math.sin(v))
            p = ((R + r * math.cos(v)) * math.cos(u), (R + r * math.cos(v)) * math.sin(u), r * math.sin(v))
            idx[i, j] = o.vert(p, (i / seg, j / sides), n)
    for i in range(seg):
        for j in range(sides):
            o.quad(idx[i, j], idx[i, j + 1], idx[i + 1, j + 1], idx[i + 1, j])
    return o


def wedge(sx=100, sy=100, sz=100):
    """Ramp: full height at -X, zero at +X; pivot bottom-center."""
    o = Obj()
    hx, hy = sx / 2, sy / 2
    A, B, C, D = (-hx, -hy, 0), (hx, -hy, 0), (hx, hy, 0), (-hx, hy, 0)
    E, F = (-hx, -hy, sz), (-hx, hy, sz)
    def face(pts, uvs):
        n = _norm(_cross(_sub(pts[1], pts[0]), _sub(pts[2], pts[0])))
        ids = [o.vert(p, uv, n) for p, uv in zip(pts, uvs)]
        return ids
    q = face([A, D, C, B], [(0, 0), (0, 1), (1, 1), (1, 0)]); o.quad(*q)      # bottom (normal -Z)
    q = face([A, E, F, D], [(0, 1), (0, 0), (1, 0), (1, 1)]); o.quad(*q)      # back wall (-X)
    q = face([E, B, C, F], [(0, 0), (1, 1), (1, 1), (0, 0)]); o.quad(*q)      # slope
    t = face([A, B, E], [(0, 1), (1, 1), (0, 0)]); o.tri(*t)                   # side -Y
    t = face([D, F, C], [(0, 1), (0, 0), (1, 1)]); o.tri(*t)                   # side +Y
    return o


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


SHAPES = {
    "cube": lambda: box(),
    "cube_bottom": lambda: box(pivot="bottom"),
    "tile": lambda: box(100, 100, 10, pivot="bottom"),
    "beam": lambda: box(100, 10, 10),
    "sphere": lambda: sphere(),
    "cylinder": lambda: cylinder(),
    "cone": lambda: cylinder(r_top=0.0),
    "torus": lambda: torus(),
    "wedge": lambda: wedge(),
}


def write(shape, path, mat="Main"):
    o = SHAPES[shape]()
    with open(path, "w") as f:
        f.write(o.text(mat))
    mtl = path.rsplit("/", 1)[0] + "/" + mat + ".mtl" if "/" in path.replace("\\", "/") else mat + ".mtl"
    with open(path.replace("\\", "/").rsplit("/", 1)[0] + f"/{mat}.mtl", "w") as f:
        f.write(f"newmtl {mat}\nKd 0.8 0.8 0.8\n")
    return len(o.v), len(o.f)
