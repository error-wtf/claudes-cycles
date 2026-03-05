"""Generate animated GIF of Claude's Cycles for m=3."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np
from PIL import Image
import io
from claudes_cycles import vertex_perm, build_cycle, GEN_DIFF

M = 3
COLORS = ['#FF3366', '#33CC99', '#3388FF']  # red, green, blue
NAMES = ['Cycle 1 (+i dominant)', 'Cycle 2 (+j dominant)', 'Cycle 3 (+k dominant)']
BG = '#0D1117'
GRID_COL = '#30363D'
TEXT_COL = '#E6EDF3'
FRAMES_PER_CYCLE = 28  # 27 edges + 1 pause
TOTAL_FRAMES = 3 * FRAMES_PER_CYCLE + 15  # 3 cycles + final hold


def make_frame(cycle_paths, step, fig, ax):
    """Render one frame of the animation."""
    ax.cla()
    ax.set_facecolor(BG)
    fig.set_facecolor(BG)

    # Grid range
    ax.set_xlim(-0.3, 2.3)
    ax.set_ylim(-0.3, 2.3)
    ax.set_zlim(-0.3, 2.3)
    ax.set_xlabel('i', color=TEXT_COL, fontsize=10)
    ax.set_ylabel('j', color=TEXT_COL, fontsize=10)
    ax.set_zlabel('k', color=TEXT_COL, fontsize=10)
    ax.tick_params(colors=TEXT_COL, labelsize=7)
    for spine in [ax.xaxis, ax.yaxis, ax.zaxis]:
        spine.pane.fill = False
        spine.pane.set_edgecolor(GRID_COL)
        spine._axinfo['grid']['color'] = GRID_COL

    # Draw all 27 vertices as dim dots
    for i in range(M):
        for j in range(M):
            for k in range(M):
                ax.scatter(i, j, k, c=GRID_COL, s=20, alpha=0.4,
                           depthshade=False, zorder=1)

    # Determine which cycle and how many edges to show
    current_cycle = 0
    edges_shown = 0
    remaining = step

    for c in range(3):
        if remaining < FRAMES_PER_CYCLE:
            current_cycle = c
            edges_shown = min(remaining, 27)
            break
        remaining -= FRAMES_PER_CYCLE
        current_cycle = c
        edges_shown = 27
    else:
        # Final hold: show all 3
        current_cycle = 3
        edges_shown = 27

    # Draw completed cycles (thin, semi-transparent)
    for c in range(min(current_cycle, 3)):
        path = cycle_paths[c]
        for e in range(27):
            src = path[e]
            dst = path[(e + 1) % 27]
            xs = [src[0], dst[0]]
            ys = [src[1], dst[1]]
            zs = [src[2], dst[2]]
            # Handle wraparound: skip drawing if distance > 1
            d = sum(abs(dst[a] - src[a]) for a in range(3))
            if d <= 1:
                ax.plot(xs, ys, zs, color=COLORS[c], alpha=0.25,
                        linewidth=1.5, zorder=2)

    # Draw current cycle edges (bright, growing)
    if current_cycle < 3:
        path = cycle_paths[current_cycle]
        col = COLORS[current_cycle]

        # Draw edges
        for e in range(edges_shown):
            src = path[e]
            dst = path[(e + 1) % 27]
            d = sum(abs(dst[a] - src[a]) for a in range(3))
            if d <= 1:
                alpha = 0.4 + 0.6 * (e / max(edges_shown, 1))
                lw = 1.5 + 1.5 * (e / max(edges_shown, 1))
                ax.plot([src[0], dst[0]], [src[1], dst[1]],
                        [src[2], dst[2]], color=col,
                        alpha=min(alpha, 1.0), linewidth=lw, zorder=3)

        # Highlight visited vertices
        for e in range(min(edges_shown + 1, 27)):
            v = path[e]
            s = 50 if e < edges_shown else 90
            ax.scatter(v[0], v[1], v[2], c=col, s=s,
                       alpha=0.9, depthshade=False, zorder=5,
                       edgecolors='white', linewidths=0.3)

        # Bright head
        if edges_shown > 0 and edges_shown <= 27:
            head = path[min(edges_shown, 26)]
            ax.scatter(head[0], head[1], head[2], c='white', s=120,
                       alpha=1.0, depthshade=False, zorder=6,
                       edgecolors=col, linewidths=2)
    else:
        # Final: show all 3 cycles bright
        for c in range(3):
            path = cycle_paths[c]
            col = COLORS[c]
            for e in range(27):
                src = path[e]
                dst = path[(e + 1) % 27]
                d = sum(abs(dst[a] - src[a]) for a in range(3))
                if d <= 1:
                    ax.plot([src[0], dst[0]], [src[1], dst[1]],
                            [src[2], dst[2]], color=col,
                            alpha=0.7, linewidth=2.0, zorder=3)
            for e in range(27):
                v = path[e]
                ax.scatter(v[0], v[1], v[2], c=col, s=35,
                           alpha=0.8, depthshade=False, zorder=5)

    # Title
    if current_cycle < 3:
        title = NAMES[current_cycle]
        title_col = COLORS[current_cycle]
        subtitle = f"Edge {min(edges_shown, 27)}/27"
    else:
        title = "All 3 Hamiltonian Cycles"
        title_col = TEXT_COL
        subtitle = "81 arcs = 3 × 27 (complete decomposition)"

    ax.set_title(f"Claude's Cycles  m=3\n{title}\n{subtitle}",
                 color=title_col, fontsize=11, fontweight='bold',
                 pad=10)

    # Camera angle: slow rotation
    ax.view_init(elev=25, azim=30 + step * 1.2)

    # Render to image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    buf.seek(0)
    return Image.open(buf).copy()


def main():
    print("Building cycles for m=3...")
    paths = [build_cycle(M, c) for c in range(3)]

    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')

    frames = []
    print(f"Rendering {TOTAL_FRAMES} frames...")
    for step in range(TOTAL_FRAMES):
        img = make_frame(paths, step, fig, ax)
        frames.append(img)
        if (step + 1) % 20 == 0:
            print(f"  Frame {step + 1}/{TOTAL_FRAMES}")

    plt.close(fig)

    out = "claudes_cycles.gif"
    print(f"Saving {out}...")
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=120,  # ms per frame
        loop=0,
        optimize=True
    )
    print(f"Done! {out} created ({len(frames)} frames)")


if __name__ == "__main__":
    main()
