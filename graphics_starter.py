"""
COSC3000 - Computer Graphics Project
=====================================
Requirements:
    pip install numpy matplotlib

Usage:
    - Place your .obj file in the 3d_models/ folder
    - Run: python graphics_starter.py
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
OBJ_FILE    = "3d_models/cow.obj"
LIGHT_POINT = np.array([800.0, 400.0, 500.0])


# ─────────────────────────────────────────────
# 1. OBJ LOADER
# ─────────────────────────────────────────────
def load_obj(filepath):
    vertices, faces = [], []
    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == "v":
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif parts[0] == "f":
                idx = [int(p.split("/")[0]) - 1 for p in parts[1:]]
                faces.append(idx)
    return np.array(vertices, dtype=float), faces


# ─────────────────────────────────────────────
# 2. TRANSFORMATION MATRICES
# ─────────────────────────────────────────────
def translation_matrix(tx, ty, tz):
    T = np.eye(4)
    T[0, 3], T[1, 3], T[2, 3] = tx, ty, tz
    return T

def scale_matrix(sx, sy, sz):
    S = np.eye(4)
    S[0, 0], S[1, 1], S[2, 2] = sx, sy, sz
    return S

def rotation_x(angle_deg):
    a = np.radians(angle_deg)
    R = np.eye(4)
    R[1,1], R[1,2] =  np.cos(a), -np.sin(a)
    R[2,1], R[2,2] =  np.sin(a),  np.cos(a)
    return R

def rotation_y(angle_deg):
    a = np.radians(angle_deg)
    R = np.eye(4)
    R[0,0], R[0,2] =  np.cos(a),  np.sin(a)
    R[2,0], R[2,2] = -np.sin(a),  np.cos(a)
    return R

def rotation_z(angle_deg):
    a = np.radians(angle_deg)
    R = np.eye(4)
    R[0,0], R[0,1] =  np.cos(a), -np.sin(a)
    R[1,0], R[1,1] =  np.sin(a),  np.cos(a)
    return R

def shear_matrix(shx=0.0, shy=0.0):
    M = np.eye(4)
    M[0, 2] = shx
    M[1, 2] = shy
    return M

def apply_transform(vertices, matrix):
    ones = np.ones((len(vertices), 1))
    hom  = np.hstack([vertices, ones])
    return (matrix @ hom.T).T[:, :3]


# ─────────────────────────────────────────────
# 3. DOT-PRODUCT FACE COLOURING
# ─────────────────────────────────────────────
def face_normal(verts, face):
    v0, v1, v2 = verts[face[0]], verts[face[1]], verts[face[2]]
    normal = np.cross(v1 - v0, v2 - v0)
    n = np.linalg.norm(normal)
    return normal / n if n > 0 else np.array([0., 0., 1.])

def face_colour(verts, face, light_point):
    centre   = np.mean(verts[face], axis=0)
    to_light = light_point - centre
    to_light = to_light / np.linalg.norm(to_light)
    dot      = np.dot(face_normal(verts, face), to_light)
    t        = (dot + 1) / 2
    return (t, 0.5 * t, 1 - t, 0.7)


# ─────────────────────────────────────────────
# 4. DRAW A SINGLE OBJECT
# ─────────────────────────────────────────────
def draw_object(ax, verts, faces, title="", colour=(0.6, 0.8, 1.0, 0.5),
                light_point=None, elev=20, azim=45, xlim=None, ylim=None, zlim=None):
    polys, colours = [], []
    for face in faces:
        polys.append([verts[i] for i in face])
        colours.append(face_colour(verts, face, light_point)
                       if light_point is not None else colour)

    col = Poly3DCollection(polys, facecolors=colours,
                           edgecolors="black", linewidths=0.2)
    ax.add_collection3d(col)

    # Shared limits keep both subplots in the same frame so changes are visible
    ax.set_xlim(xlim if xlim else (verts[:,0].min(), verts[:,0].max()))
    ax.set_ylim(ylim if ylim else (verts[:,1].min(), verts[:,1].max()))
    ax.set_zlim(zlim if zlim else (verts[:,2].min(), verts[:,2].max()))
    ax.set_xlabel("X", fontsize=7)
    ax.set_ylabel("Y", fontsize=7)
    ax.set_zlabel("Z", fontsize=7)
    ax.tick_params(labelsize=6)
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(title, fontsize=9, pad=20)


# ─────────────────────────────────────────────
# 5. BEFORE / AFTER FIGURE
# ─────────────────────────────────────────────
def plot_before_after(original_verts, faces, transforms):
    """
    One window per transformation.
    Each subplot uses its own natural axis limits so neither model looks distorted.
    Both subplots use the same camera angle so the difference is visually clear.
    """
    ORIGINAL_COLOUR    = (0.75, 0.75, 0.75, 0.5)
    TRANSFORMED_COLOUR = (0.25, 0.60, 1.00, 0.6)
    ELEV, AZIM = 20, 45   # consistent camera angle for all plots

    for i, (label, transformed_verts, description) in enumerate(transforms):
        fig = plt.figure(figsize=(12, 5))
        fig.suptitle(f"{label}  -  {description}", fontsize=12)

        # LEFT: original — auto-scaled to its own bounds
        ax_before = fig.add_subplot(1, 2, 1, projection="3d")
        draw_object(ax_before, original_verts, faces,
                    title="Original", colour=ORIGINAL_COLOUR,
                    elev=ELEV, azim=AZIM)

        # RIGHT: transformed — auto-scaled to its own bounds
        ax_after = fig.add_subplot(1, 2, 2, projection="3d")
        draw_object(ax_after, transformed_verts, faces,
                    title=f"After: {label}", colour=TRANSFORMED_COLOUR,
                    elev=ELEV, azim=AZIM)

        plt.subplots_adjust(top=0.88, wspace=0.1)
        filename = f"transform_{i+1}_{label.replace(' ', '_').replace('+', 'and')}.png"
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"Saved: {filename}")


# ─────────────────────────────────────────────
# 6. DOT-PRODUCT COLOURING FIGURE
# ─────────────────────────────────────────────
def plot_dot_product(verts, faces, light_point):
    fig = plt.figure(figsize=(12, 6))
    fig.suptitle("Dot-Product Face Colouring", fontsize=13)

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    draw_object(ax1, verts, faces, title="No colouring (reference)",
                colour=(0.75, 0.75, 0.75, 0.6))

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    draw_object(ax2, verts, faces,
                title=f"Dot-product colouring\nLight point {light_point}",
                light_point=light_point)
    ax2.scatter(*light_point, color="yellow", s=80, zorder=5, label="Light source")
    ax2.legend(fontsize=8)

    plt.subplots_adjust(top=0.88, wspace=0.1)
    plt.savefig("dot_product_colouring.png", dpi=150, bbox_inches="tight")
    print("Saved: dot_product_colouring.png")


# ─────────────────────────────────────────────
# 7. MAIN
# ─────────────────────────────────────────────
def main():
    verts, faces = load_obj(OBJ_FILE)
    print(f"Loaded: {len(verts)} vertices, {len(faces)} faces")

    # Cow spans roughly 400 units on X/Y, so translate by 300 to make it obvious
    cow_span = verts[:,0].max() - verts[:,0].min()
    translation_amount = cow_span * 0.8   # 80% of the cow's width — clearly visible

    transforms = [
        (
            "Translation",
            apply_transform(verts, translation_matrix(translation_amount, 0, 0)),
            f"+{translation_amount:.0f} units along X axis"
        ),
        (
            "Rotation Y 45deg",
            apply_transform(verts, rotation_y(45)),
            "Rotated 45deg around Y axis"
        ),
        (
            "Translation + Rotation",
            apply_transform(verts, translation_matrix(0, translation_amount, 0) @ rotation_z(30)),
            f"+{translation_amount:.0f} on Y, then 30deg rotation around Z"
        ),
        (
            "Scaling (x2)",
            apply_transform(verts, scale_matrix(2, 2, 2)),
            "Uniform scale by factor 2 — cow is twice the size"
        ),
        (
            "Shape Change",
            apply_transform(verts, shear_matrix(shx=1.5, shy=1.0)),
            "Non-rigid shear: shx=1.5, shy=1.0 — clearly distorts the shape"
        ),
    ]

    plot_before_after(verts, faces, transforms)
    plot_dot_product(verts, faces, LIGHT_POINT)

    plt.show()


if __name__ == "__main__":
    main()