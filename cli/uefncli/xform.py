"""UE transform math (FRotator <-> FQuat, compose/inverse) so the CLI can work in local space
while the EntityToolset's Get/SetEntityTransform only speak world space.

Rotator convention = Unreal: pitch around Y, yaw around Z, roll around X, degrees.
"""
import math

D2R = math.pi / 180.0


def rot_to_quat(pitch, yaw, roll):
    sp, cp = math.sin(pitch * D2R / 2), math.cos(pitch * D2R / 2)
    sy, cy = math.sin(yaw * D2R / 2), math.cos(yaw * D2R / 2)
    sr, cr = math.sin(roll * D2R / 2), math.cos(roll * D2R / 2)
    return (cr * sp * sy - sr * cp * cy,
            -cr * sp * cy - sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy)


def _norm_axis(a):
    a = math.fmod(a, 360.0)
    if a > 180:
        a -= 360
    if a < -180:
        a += 360
    return a


def quat_to_rot(q):
    x, y, z, w = q
    sing = z * x - w * y
    yy, yx = 2 * (w * z + x * y), 1 - 2 * (y * y + z * z)
    yaw = math.atan2(yy, yx) / D2R
    if sing < -0.4999995:
        return -90.0, yaw, _norm_axis(-yaw - 2 * math.atan2(x, w) / D2R)
    if sing > 0.4999995:
        return 90.0, yaw, _norm_axis(yaw - 2 * math.atan2(x, w) / D2R)
    pitch = math.asin(2 * sing) / D2R
    roll = math.atan2(-2 * (w * x + y * z), 1 - 2 * (x * x + y * y)) / D2R
    return pitch, yaw, roll


def qmul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def qinv(q):
    return (-q[0], -q[1], -q[2], q[3])


def qrot(q, v):
    x, y, z, w = q
    vx, vy, vz = v
    # t = 2 * cross(q.xyz, v); v' = v + w*t + cross(q.xyz, t)
    tx, ty, tz = 2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx)
    return (vx + w * tx + (y * tz - z * ty), vy + w * ty + (z * tx - x * tz), vz + w * tz + (x * ty - y * tx))


class Xf:
    def __init__(self, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.loc, self.rot, self.scale = tuple(map(float, loc)), tuple(map(float, rot)), tuple(map(float, scale))

    @property
    def q(self):
        return rot_to_quat(*self.rot)

    @classmethod
    def from_json(cls, t):
        l, r, s = t["location"], t["rotation"], t["scale"]
        return cls((l["x"], l["y"], l["z"]), (r["pitch"], r["yaw"], r["roll"]), (s["x"], s["y"], s["z"]))

    def to_json(self):
        r = lambda v: round(v, 4)
        return {"location": dict(zip("xyz", map(r, self.loc))),
                "rotation": dict(zip(("pitch", "yaw", "roll"), map(r, self.rot))),
                "scale": dict(zip("xyz", map(r, self.scale)))}

    def compose(self, local):
        """world = self (parent world) * local"""
        sl = tuple(a * b for a, b in zip(self.scale, local.loc))
        p = qrot(self.q, sl)
        loc = tuple(a + b for a, b in zip(self.loc, p))
        rot = quat_to_rot(qmul(self.q, local.q))
        return Xf(loc, rot, tuple(a * b for a, b in zip(self.scale, local.scale)))

    def relative(self, world):
        """local such that self * local = world"""
        qi = qinv(self.q)
        d = tuple(a - b for a, b in zip(world.loc, self.loc))
        lp = qrot(qi, d)
        lp = tuple(a / b if b else 0.0 for a, b in zip(lp, self.scale))
        rot = quat_to_rot(qmul(qi, world.q))
        return Xf(lp, rot, tuple(a / b if b else 0.0 for a, b in zip(world.scale, self.scale)))

    def __repr__(self):
        f = lambda t: "(" + ", ".join(f"{v:g}" for v in (round(x, 3) for x in t)) + ")"
        return f"at {f(self.loc)} rot {f(self.rot)} scale {f(self.scale)}"


def parse_vec(s, default):
    if s is None:
        return default
    if isinstance(s, (list, tuple)):
        return tuple(float(v) for v in s)
    parts = [float(v) for v in str(s).replace(";", ",").split(",")]
    if len(parts) == 1:
        parts = parts * 3
    return tuple(parts)
