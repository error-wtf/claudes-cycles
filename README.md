# Claude's Cycles

A **one-prompt replication attempt** of the AI achievement reported by Donald Knuth in his paper *"Claude's Cycles"* (2026), using **Windsurf IDE + Claude Opus 4.6**.

This repository documents our attempt to reproduce — in a single agentic session — the Hamiltonian cycle decomposition for 3D Cayley digraphs on **Z_m³** that Claude originally discovered through 31 guided explorations with Filip Stappers.

## Background: The Original Achievement

In early 2026, **Filip Stappers** fed an open conjecture from Donald Knuth to Claude Opus 4.6 and, over 31 guided explorations (~1 hour), Claude discovered a working construction. Knuth then wrote the formal proof and named the paper after the AI.

> *"A joy it is to learn not only that my conjecture has a nice solution but also to celebrate this dramatic advance in automatic deduction and creative problem solving."*
> — Donald E. Knuth

### Official Reports

- **D.E. Knuth**, *"Claude's Cycles"*, Stanford CS, 2026 — [PDF](https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf)
- **Awesome Agents**: [Knuth Names Paper After Claude That Solved His Math Conjecture](https://awesomeagents.ai/news/knuth-claude-cycles-graph-theory-conjecture/)
- **Boing Boing**: [Donald Knuth says an AI solved a math problem he was stuck on for weeks](https://boingboing.net/2026/03/03/donald-knuth-the-godfather-of-computer-science-says-an-ai-solved-a-math-problem-he-was-stuck-on-for-weeks.html)
- **Hacker News**: [Claude's Cycles \[pdf\]](https://news.ycombinator.com/item?id=47230710)
- **Reddit r/math**: [Claude's Cycles](https://www.reddit.com/r/math/comments/1rjyam6/claudes_cycles/)
- **lhl/claudecycles-revisited**: [Independent cleanroom reproductions](https://github.com/lhl/claudecycles-revisited)

### Credit

**Filip Stappers** was the first to achieve this — he prompted Claude Opus 4.6 with Knuth's exact problem statement and guided it through 31 explorations to discover the construction. Knuth verified and proved the result, naming the paper *"Claude's Cycles"* in honor of both Claude Shannon and the AI.

## This Project

We attempted to replicate the same result in a **single Windsurf agentic session** (one prompt, no restarts) with Claude Opus 4.6. The construction was found, implemented, and verified for all odd m from 3 to 101 — all passing.

## Problem

Given odd m > 2, decompose all 3m³ directed arcs of the Cayley digraph on Z_m³ (with generators e₁=(1,0,0), e₂=(0,1,0), e₃=(0,0,1)) into exactly **3 directed Hamiltonian cycles**.

## Construction

The construction assigns a permutation of {0,1,2} to each vertex (i,j,k), determining which generator each of the three cycles uses at that vertex. Let s = (i+j+k) mod m:

| Condition | Cycle 0 | Cycle 1 | Cycle 2 |
|-----------|---------|---------|--------|
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

27 tests, all pass. Verified for all 50 odd m from 3 to 101.

## Verification Results

| m | Vertices (m³) | Arcs (3m³) | Status |
|---|---------------|------------|--------|
| 3 | 27 | 81 | ✅ |
| 5 | 125 | 375 | ✅ |
| 7 | 343 | 1,029 | ✅ |
| ... | ... | ... | ✅ |
| 101 | 1,030,301 | 3,090,903 | ✅ |

## License

[Anti-Capitalist Software License v1.4](LICENSE) — Copyright (c) 2026 Lino Casu and Claude Opus 4.6

## Authors

- **Lino Casu** ([@error-wtf](https://github.com/error-wtf)) — Prompt, session orchestration
- **Claude Opus 4.6** (Anthropic) — Construction discovery, implementation
- **Windsurf IDE** (Codeium) — Agentic coding environment
