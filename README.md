# toke-test-programs

2000+ verified toke application programs across 16 categories.
Each program has: requirement spec, solution, companion file, test harness.

## Repository Structure

```
toke-test-programs/
  schema/
    requirement-template.yaml   # Template for writing new requirements
  categories/
    {category}/
      {id}/
        requirement.yaml        # The program specification
        solution.tk             # The toke source code
        solution.tkc.md         # Companion file (algorithm explanation)
        tests/
          input_01.txt          # Test input
          expected_01.txt       # Expected output
          input_02.txt
          expected_02.txt
        metadata.json           # Auto-generated build/test metadata
```

## Categories

There are 16 categories covering a broad range of real-world application domains:

| Category | Directory |
|----------|-----------|
| Games | `games/` |
| Calculators and Finance | `calculators-finance/` |
| Crypto and Blockchain | `crypto-blockchain/` |
| Messaging | `messaging/` |
| AI Agents | `ai-agents/` |
| Social Media | `social-media/` |
| Manufacturing and ML | `manufacturing-ml/` |
| Data Processing | `data-processing/` |
| Networking and REST | `networking-rest/` |
| Security | `security/` |
| System Tools | `system-tools/` |
| Scientific and Math | `scientific-math/` |
| Media and Content | `media-content/` |
| Education | `education/` |
| Developer Tools | `devtools/` |
| Miscellaneous | `misc/` |

## How to Add a Requirement

1. Choose the appropriate category directory under `categories/`.
2. Copy `schema/requirement-template.yaml` into a new subdirectory named with the program ID (e.g. `categories/games/GAM-001/requirement.yaml`).
3. Fill in all fields. The `id` field uses a 3-letter category prefix and a 3-digit number (e.g. `GAM-001`, `SEC-042`).
4. Add at least two test cases with `input` and `expected_output`.
5. Create corresponding `tests/input_NN.txt` and `tests/expected_NN.txt` files matching the test cases.

## File Layout Per Program

```
categories/{category}/{id}/
  requirement.yaml
  solution.tk
  solution.tkc.md
  tests/
    input_01.txt
    expected_01.txt
    input_02.txt
    expected_02.txt
  metadata.json
```

### requirement.yaml

The program specification. See `schema/requirement-template.yaml` for the full format including fields for difficulty, stdlib modules, input/output formats, test cases, constraints, and companion notes.

### solution.tk

The toke source implementing the requirement. Must compile and pass all test cases.

### solution.tkc.md

The companion file explaining algorithm choice, complexity analysis, and design decisions.

### tests/

Numbered input/output pairs. The test harness pipes `input_NN.txt` to stdin and compares stdout against `expected_NN.txt`.

### metadata.json

Auto-generated file recording build status, test results, compiler version, and timestamps.

## Difficulty Scale

| Level | Description |
|-------|-------------|
| 1 | Trivial - single function, basic I/O |
| 2 | Easy - simple logic, one or two stdlib modules |
| 3 | Medium - moderate complexity, multiple modules |
| 4 | Hard - complex algorithms, concurrency, or state |
| 5 | Expert - system-level, multi-module architecture |
