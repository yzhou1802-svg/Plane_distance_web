import math


def _cross(u, v):
    return [
        u[1]*v[2] - u[2]*v[1],
        u[2]*v[0] - u[0]*v[2],
        u[0]*v[1] - u[1]*v[0],
    ]


def _dot(u, v):
    return sum(u[i]*v[i] for i in range(3))


def _vec(p1, p2):
    return [p2[i] - p1[i] for i in range(3)]


def _distance(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)


def _intersect_and_distance(normal, plane_d, point):
    """Find foot of perpendicular from point to plane normal·x = plane_d."""
    n = normal
    p = point
    num = plane_d - _dot(n, p)
    den = _dot(n, n)

    if den == 0:
        return {"status": "degenerate", "distance": None, "intersection": None}

    k = num / den
    intersection = [p[i] + k * n[i] for i in range(3)]
    diff = [intersection[i] - p[i] for i in range(3)]
    dist = _distance(diff)

    if dist < 1e-10:
        return {"status": "on_plane", "distance": 0.0, "intersection": intersection}

    return {"status": "ok", "distance": dist, "intersection": intersection}


def _fmt_equation(n, d):
    parts = []
    labels = ["x", "y", "z"]
    for i, coef in enumerate(n):
        if coef == 0:
            continue
        sign = "+" if coef > 0 and parts else ""
        if parts and coef > 0:
            sign = " + "
        elif parts and coef < 0:
            sign = " - "
            coef = abs(coef)
        else:
            sign = "" if coef > 0 else "-"
            coef = abs(coef)
        coef_str = "" if coef == 1 else (str(int(coef)) if coef == int(coef) else f"{coef:.4g}")
        parts.append(f"{sign}{coef_str}{labels[i]}")
    lhs = "".join(parts) if parts else "0"
    d_str = int(d) if d == int(d) else f"{d:.4g}"
    return f"{lhs} = {d_str}"


def calculate_parameterform(p1, p2, p3, point):
    """
    Plane through p1, p2, p3 in Parameterform.
    Converts to Koordinatenform internally, then computes distance to point.
    """
    v1 = _vec(p1, p2)
    v2 = _vec(p1, p3)
    normal = _cross(v1, v2)

    if _dot(normal, normal) == 0:
        return {"status": "error", "message": "The three points are collinear — they do not define a unique plane."}

    d = _dot(normal, p1)
    result = _intersect_and_distance(normal, d, point)
    result["normal_vector"] = normal
    result["direction_vector_1"] = v1
    result["direction_vector_2"] = v2
    result["koordinatenform"] = _fmt_equation(normal, d)
    return result


def calculate_koordinatenform(a, b, c, d, point):
    """Plane given as ax + by + cz = d."""
    normal = [a, b, c]
    if a == 0 and b == 0 and c == 0:
        return {"status": "error", "message": "The normal vector (a, b, c) is the zero vector — not a valid plane."}

    result = _intersect_and_distance(normal, d, point)
    result["normal_vector"] = normal
    result["koordinatenform"] = _fmt_equation(normal, d)
    return result


def calculate_normaleform(normal, plane_point, point):
    """Plane given in Normaleform: (x - plane_point) · normal = 0."""
    if _dot(normal, normal) == 0:
        return {"status": "error", "message": "The normal vector is the zero vector — not a valid plane."}

    d = _dot(normal, plane_point)
    result = _intersect_and_distance(normal, d, point)
    result["normal_vector"] = normal
    result["koordinatenform"] = _fmt_equation(normal, d)
    return result
