# toke-test-programs

**2,065 real-world application requirements for the [toke](https://github.com/karwalski/toke) programming language, with automated generation, testing, and verification.**

This repository serves three purposes:

1. **Prove toke works for real applications** — not hello-world demos, but REST APIs, crypto tools, ML pipelines, games, financial calculators, and more
2. **Build a verified training corpus** — every generated program is compile-tested and functionally verified, producing high-quality training data for toke code generation models
3. **Invite contributions** — anyone can add requirements, generate solutions, or verify existing ones

## Categories

```
categories/
  games/               130 programs — card games, puzzles, simulations
  calculators-finance/  130 programs — mortgage, tax, statistics, matrices
  crypto-blockchain/    135 programs — hashing, wallets, Merkle trees, tokens
  messaging/            135 programs — encryption, pub/sub, rate limiting
  ai-agents/            140 programs — tool calling, RAG, classification
  social-media/         150 programs — REST APIs, feeds, auth, moderation
  manufacturing-ml/     135 programs — SPC, defect detection, regression
  data-processing/      130 programs — CSV/JSON parsing, ETL, sorting
  networking-rest/      200 programs — HTTP servers + clients, WebSocket, SSE
  security/             130 programs — scanners, RBAC, intrusion detection
  system-tools/         130 programs — file watcher, cron, backup, monitoring
  scientific-math/      130 programs — algorithms, graph theory, numerical methods
  media-content/        130 programs — markdown, SEO, readability scoring
  education/            130 programs — quiz engine, SRS, grade calculators
  devtools/             130 programs — linters, test runners, code complexity
```

**Total: 2,065 program requirements** across 15 categories.

## Each Program Includes

```
categories/{category}/{id}/
  requirement.yaml       # What to build (description, I/O format, test cases)
  solution.tk            # Working toke source code
  solution.tkc.md        # Companion file (algorithm docs, complexity analysis)
  solution.stripped.tk    # String-stripped version (for model training)
  toke_api_original.tk   # Initial model output (before repair)
  repair_pairs/          # Error-fix training pairs from repair loop
  meta.json              # Generation metadata (repair count, warnings, etc.)
```

## Why This Matters

toke is a programming language designed for token-efficient AI code generation. These programs demonstrate that toke can express real-world applications across every major domain — not just toy examples.

Every program is:
- **Compiled** — passes `tkc --check` (zero errors)
- **Tested** — runs with test inputs and produces expected outputs
- **Documented** — companion files explain the algorithm and design
- **Training-ready** — string-stripped versions feed directly into model training

## Using the Test Harness

```bash
# Test a single program
./scripts/test-runner.sh categories/games/GAM-001/

# Test all programs
./scripts/run-all.sh

# Validate requirement uniqueness and diversity
python3 scripts/validate-uniqueness.py
```

## Contributing Programs

We welcome toke programs from the community. The more verified working code exists, the better toke models become.

1. Pick an unimplemented requirement from any `requirements.yaml`
2. Write a solution in toke (`solution.tk`)
3. Ensure it compiles: `tkc --check solution.tk`
4. Verify it passes the test cases
5. Submit a PR

Or add new requirements — follow the format in `schema/requirement-template.yaml`.

### Contributing to Model Training

Every verified toke program contributes to the next generation of toke code models. Programs that compile correctly and produce expected output are particularly valuable. If you generate toke code (via the [API](https://api.tokelang.dev), [Ollama](https://ollama.com/karwalski/toke), or by hand), consider submitting it here with test cases.

## Automated Generation

The `infra/` directory contains scripts for automated program generation at scale using AI (Claude + toke API). Workers generate, compile, test, and repair programs in parallel. See `infra/README.md` for details.

## Difficulty Scale

| Level | Description |
|-------|-------------|
| 1 | Trivial — single function, basic I/O |
| 2 | Easy — simple logic, one or two stdlib modules |
| 3 | Medium — moderate complexity, multiple modules |
| 4 | Hard — complex algorithms, concurrency, or state |
| 5 | Expert — system-level, multi-module architecture |

## Links

- [toke language](https://github.com/karwalski/toke) — compiler, spec, stdlib
- [tokelang.dev](https://tokelang.dev) — website and documentation
- [API](https://api.tokelang.dev) — free tier for toke code generation
- [VS Code extension](https://marketplace.visualstudio.com/items?itemName=tokelang.toke-language) — syntax highlighting and LSP
- [Ollama model](https://ollama.com/karwalski/toke) — run locally
- [HuggingFace model](https://huggingface.co/karwalski/toke) — fine-tuned weights
- [Research whitepaper](https://github.com/karwalski/toke/blob/main/docs/whitepaper/toke-research-language.md) — methodology and results

## License

MIT
