#!/usr/bin/env python3
"""worker-companion.py — Generate .tkc.md companion documentation for toke solutions.

Takes a solution.tk file path as input, calls Claude to generate verbose
companion documentation, and saves as solution.tkc.md alongside the source.

Usage:
    python3 worker-companion.py /path/to/solution.tk
"""

import os
import sys
from pathlib import Path

import requests

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

COMPANION_PROMPT = """You are a toke language documentation expert. Generate a detailed companion
documentation file (.tkc.md) for the following toke program.

The companion file should include:
1. **Overview** — What the program does in 2-3 sentences
2. **Architecture** — How the code is structured (modules, functions, data flow)
3. **Key Concepts** — Toke language features demonstrated (type system, stdlib usage, etc.)
4. **Line-by-Line Notes** — Brief explanation of non-obvious sections
5. **Test Coverage** — What the test cases verify
6. **Complexity** — Time/space complexity if applicable
7. **Potential Improvements** — What could be enhanced

Format as clean Markdown. Be thorough but concise.

SOURCE CODE:
```toke
{source}
```

Generate the companion documentation now:"""


def generate_companion(source_path: Path) -> str | None:
    """Call Claude to generate companion documentation."""
    source = source_path.read_text()

    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "PLACEHOLDER":
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return None

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": COMPANION_PROMPT.format(source=source),
                    }
                ],
            },
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]
    except Exception as e:
        print(f"ERROR: Companion generation failed: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: worker-companion.py <solution.tk>", file=sys.stderr)
        sys.exit(1)

    source_path = Path(sys.argv[1])
    if not source_path.exists():
        print(f"ERROR: {source_path} not found", file=sys.stderr)
        sys.exit(1)

    companion_text = generate_companion(source_path)
    if companion_text:
        output_path = source_path.with_suffix(".tkc.md")
        output_path.write_text(companion_text)
        print(f"Companion saved: {output_path}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
