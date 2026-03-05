# Claude's Cycles

Implementation of the Hamiltonian cycle decomposition for 3D Cayley digraphs on **Z_m³**, based on Donald Knuth's paper *"Claude's Cycles"* (2026).

## Problem

Given odd m > 2, decompose all 3m³ directed arcs of the Cayley digraph on Z_m³ (with generators e₁=(1,0,0), e₂=(0,1,0), e₃=(0,0,1)) into exactly **3 directed Hamiltonian cycles**.

## Construction

The construction assigns a permutation of {0,1,2} to each vertex (i,j,k), determining which generator each of the three cycles uses at that vertex. Let s = (i+j+k) mod m:

| Condition | Cycle 0 | Cycle 1 | Cycle 2 |
|-----------|---------|---------|---------|
| s = 0, j = m−1 | 0 (+i) | 1 (+j) | 2 (+k) |
| s = 0, j ≠ m−1 | 2 (+k) | 1 (+j) | 0 (+i) |
| s = m−1, i > 0 | 1 (+j) | 2 (+k) | 0 (+i) |
| s = m−1, i = 0 | 2 (+k) | 1 (+j) | 0 (+i) |
| else, i = m−1 | 2 (+k) | 0 (+i) | 1 (+j) |
| else, i ≠ m−1 | 1 (+j) | 0 (+i) | 2 (+k) |

Each row is a permutation of {0,1,2}, guaranteeing arc-disjointness and full coverage. Knuth proved these define three Hamiltonian cycles for all odd m > 2.

## Usage

```python
from claudes_cycles import decompose, verify_decomposition

m = 7  # any odd m > 2
c1, c2, c3 = decompose(m)
result = verify_decomposition(m, (c1, c2, c3))
print(result["valid"])  # True
```

Run the full verification suite:

```bash
python claudes_cycles.py
```

## Tests

```bash
pip install pytest
pytest test_claudes_cycles.py -v
```

Verified for all odd m from 3 to 101 (27 tests, all pass).

## Verification Results

| m | Vertices (m³) | Arcs (3m³) | Status |
|---|---------------|------------|--------|
| 3 | 27 | 81 | ✅ |
| 5 | 125 | 375 | ✅ |
| 7 | 343 | 1,029 | ✅ |
| ... | ... | ... | ✅ |
| 101 | 1,030,301 | 3,090,903 | ✅ |

All 50 odd values from 3 to 101 pass verification.

## Reference

- D.E. Knuth, *"Claude's Cycles"*, Stanford CS, 2026
- [Knuth's homepage](https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf)

## Author

Lino Casu ([@error-wtf](https://github.com/error-wtf))
