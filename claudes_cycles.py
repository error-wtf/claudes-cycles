"""
Claude's Cycles - Hamiltonian Decomposition of 3D Cayley Digraphs

Based on Donald Knuth's paper 'Claude's Cycles' (2026):
Decompose arcs of Cayley digraph on Z_m^3 with generators
e1=(1,0,0), e2=(0,1,0), e3=(0,0,1) into 3 directed Hamiltonian
cycles, for all odd m > 2.

Construction: Per-vertex permutation based on s = (i+j+k) mod m.

Authors: Lino Casu (error-wtf)
Reference: D.E. Knuth, 'Claude's Cycles', Stanford CS, 2026
"""

from __future__ import annotations
from typing import List, Tuple, Dict, Set

Vertex = Tuple[int, int, int]
GEN_DIFF = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def vertex_perm(i, j, k, m):
    """
    Per-vertex permutation from Knuth's paper for odd m.
    Returns (d0, d1, d2): cycle c uses generator dc.
    0 -> bump i, 1 -> bump j, 2 -> bump k.

    Four cases based on s = (i+j+k) mod m:
    - s == 0:     (0,1,2) if j == m-1, else (2,1,0)
    - s == m-1:   (1,2,0) if i > 0,   else (2,1,0)
    - otherwise:  (2,0,1) if i == m-1, else (1,0,2)
    """
    s = (i + j + k) % m
    if s == 0:
        return (0, 1, 2) if (j == m - 1) else (2, 1, 0)
    elif s == m - 1:
        return (1, 2, 0) if (i > 0) else (2, 1, 0)
    else:
        return (2, 0, 1) if (i == m - 1) else (1, 0, 2)


def build_cycle(m, cycle_idx):
    """Build Hamiltonian cycle number cycle_idx (0, 1, or 2)."""
    assert m % 2 == 1 and m > 2
    n = m ** 3
    f = {}
    for i in range(m):
        for j in range(m):
            for k in range(m):
                f[(i, j, k)] = vertex_perm(i, j, k, m)[cycle_idx]
    pos = (0, 0, 0)
    path = [pos]
    for _ in range(n - 1):
        g = f[pos]
        d = GEN_DIFF[g]
        pos = ((pos[0] + d[0]) % m,
               (pos[1] + d[1]) % m,
               (pos[2] + d[2]) % m)
        path.append(pos)
    return path


def decompose(m):
    """Decompose Z_m^3 Cayley digraph into 3 Hamiltonian cycles."""
    assert m % 2 == 1 and m > 2
    return (build_cycle(m, 0),
            build_cycle(m, 1),
            build_cycle(m, 2))


def get_arcs(path, m):
    """Extract directed arcs (vertex, generator_index) from a cycle."""
    arcs = set()
    n = len(path)
    gens = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for i in range(n):
        src = path[i]
        dst = path[(i + 1) % n]
        diff = ((dst[0] - src[0]) % m,
                (dst[1] - src[1]) % m,
                (dst[2] - src[2]) % m)
        gen = gens.index(diff)
        arcs.add((src, gen))
    return arcs


def verify_decomposition(m, cycles):
    """Verify that cycles form a valid Hamiltonian decomposition."""
    total_vertices = m ** 3
    total_arcs = 3 * total_vertices
    all_vertices = set()
    for i in range(m):
        for j in range(m):
            for k in range(m):
                all_vertices.add((i, j, k))
    all_arcs_expected = set()
    for v in all_vertices:
        for g in range(3):
            all_arcs_expected.add((v, g))

    result = {"m": m, "valid": True, "errors": []}
    all_arcs_found = set()

    for idx, cycle in enumerate(cycles):
        name = "Cycle " + str(idx + 1)
        cycle_set = set(cycle)

        if len(cycle) != total_vertices:
            result["errors"].append(
                name + ": " + str(len(cycle)) +
                " vertices, expected " + str(total_vertices))
            result["valid"] = False

        if cycle_set != all_vertices:
            missing = all_vertices - cycle_set
            if missing:
                result["errors"].append(
                    name + ": missing " + str(len(missing)) +
                    " vertices")
            result["valid"] = False

        try:
            arcs = get_arcs(cycle, m)
            overlap = arcs & all_arcs_found
            if overlap:
                result["errors"].append(
                    name + ": " + str(len(overlap)) +
                    " arcs overlap with previous cycles")
                result["valid"] = False
            all_arcs_found |= arcs
        except (ValueError, IndexError) as e:
            result["errors"].append(name + ": " + str(e))
            result["valid"] = False

    missing = all_arcs_expected - all_arcs_found
    if missing:
        result["errors"].append(
            "Missing " + str(len(missing)) + " arcs")
        result["valid"] = False

    result["arcs_covered"] = len(all_arcs_found)
    result["arcs_expected"] = total_arcs
    return result


if __name__ == "__main__":
    import time

    print("=" * 60)
    print("Claude's Cycles - Hamiltonian Decomposition of Z_m^3")
    print("Based on D.E. Knuth's paper (2026)")
    print("=" * 60)

    hdr = "{:>5} {:>10} {:>10} {:>10} {:>8}".format(
        "m", "vertices", "arcs", "time(ms)", "status")
    print(hdr)
    print("-" * 50)

    for m in range(3, 102, 2):
        t0 = time.perf_counter()
        cycles = decompose(m)
        result = verify_decomposition(m, cycles)
        dt = (time.perf_counter() - t0) * 1000
        status = "PASS" if result["valid"] else "FAIL"
        line = "{:>5} {:>10} {:>10} {:>10.1f} {:>8}".format(
            m, m**3, 3*m**3, dt, status)
        print(line)
        if not result["valid"]:
            for e in result["errors"]:
                print("  ERROR: " + e)
            break

    print("\nDone.")
