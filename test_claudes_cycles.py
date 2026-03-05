"""Tests for Claude's Cycles Hamiltonian decomposition."""

import pytest
from claudes_cycles import (
    vertex_perm, build_cycle, decompose,
    get_arcs, verify_decomposition, GEN_DIFF
)


class TestVertexPerm:
    """Test the per-vertex permutation function."""

    def test_returns_permutation(self):
        """Each vertex gets a permutation of {0,1,2}."""
        for m in [3, 5, 7]:
            for i in range(m):
                for j in range(m):
                    for k in range(m):
                        d = vertex_perm(i, j, k, m)
                        assert set(d) == {0, 1, 2}, (
                            f"Not a perm at ({i},{j},{k}), m={m}: {d}")

    def test_s0_boundary(self):
        """s=0, j=m-1 gives (0,1,2)."""
        for m in [3, 5, 7]:
            assert vertex_perm(0, m - 1, 1, m) == (0, 1, 2)

    def test_s0_interior(self):
        """s=0, j != m-1 gives (2,1,0)."""
        for m in [5, 7]:
            assert vertex_perm(0, 0, 0, m) == (2, 1, 0)


class TestBuildCycle:
    """Test individual cycle construction."""

    def test_hamiltonian_m3(self):
        for c in range(3):
            path = build_cycle(3, c)
            assert len(path) == 27
            assert len(set(path)) == 27

    def test_hamiltonian_m5(self):
        for c in range(3):
            path = build_cycle(5, c)
            assert len(path) == 125
            assert len(set(path)) == 125

    def test_cycle_closes(self):
        """Last vertex connects back to first."""
        for m in [3, 5, 7]:
            for c in range(3):
                path = build_cycle(m, c)
                n = len(path)
                last = path[-1]
                g = vertex_perm(*last, m)[c]
                d = GEN_DIFF[g]
                nxt = ((last[0]+d[0]) % m,
                       (last[1]+d[1]) % m,
                       (last[2]+d[2]) % m)
                assert nxt == path[0], (
                    f"Cycle {c} doesn't close for m={m}")


class TestDecompose:
    """Test the full 3-cycle decomposition."""

    @pytest.mark.parametrize("m", [3, 5, 7, 9, 11])
    def test_valid_decomposition(self, m):
        cycles = decompose(m)
        result = verify_decomposition(m, cycles)
        assert result["valid"], (
            f"m={m} failed: {result['errors']}")

    @pytest.mark.parametrize("m", [3, 5, 7, 9, 11])
    def test_all_arcs_covered(self, m):
        cycles = decompose(m)
        result = verify_decomposition(m, cycles)
        assert result["arcs_covered"] == result["arcs_expected"]

    @pytest.mark.parametrize("m", [3, 5, 7])
    def test_no_arc_overlap(self, m):
        cycles = decompose(m)
        all_arcs = set()
        for cycle in cycles:
            arcs = get_arcs(cycle, m)
            overlap = arcs & all_arcs
            assert len(overlap) == 0
            all_arcs |= arcs


class TestLargerValues:
    """Test larger m values (slower)."""

    @pytest.mark.parametrize("m", [13, 15, 21, 51, 101])
    def test_valid_decomposition_large(self, m):
        cycles = decompose(m)
        result = verify_decomposition(m, cycles)
        assert result["valid"], (
            f"m={m} failed: {result['errors']}")


class TestEdgeCases:
    """Test edge cases and assertions."""

    def test_even_m_rejected(self):
        with pytest.raises(AssertionError):
            decompose(4)

    def test_m1_rejected(self):
        with pytest.raises(AssertionError):
            decompose(1)

    def test_m2_rejected(self):
        with pytest.raises(AssertionError):
            decompose(2)
