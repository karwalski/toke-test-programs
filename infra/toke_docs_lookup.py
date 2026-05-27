#!/usr/bin/env python3
"""toke_docs_lookup.py — Reusable toke documentation RAG/lookup module.

Loads toke reference material into a searchable index and provides search
functions for stdlib signatures, grammar rules, and error codes. Designed
for use by worker-generate.py during repair loops.

Usage:
    from toke_docs_lookup import get_context_for_repair, search_stdlib
    context = get_context_for_repair(source, error)
    results = search_stdlib("split")
"""

import json
import os
import re
from pathlib import Path

# --- Paths ---
# When running on workers, docs are in worker-docs/ alongside this file.
# When running locally, fall back to the full repo paths.
_HERE = Path(__file__).resolve().parent
_WORKER_DOCS = _HERE / "worker-docs"

_STDLIB_SIGS_PATH = _WORKER_DOCS / "stdlib-signatures.json"
_ERROR_CODES_PATH = _WORKER_DOCS / "error-codes.json"
_GRAMMAR_PATH = _WORKER_DOCS / "grammar.ebnf"

# Fallback paths for local development
_LOCAL_GRAMMAR = Path(os.environ.get(
    "TOKE_GRAMMAR_PATH",
    str(Path.home() / "tk" / "toke" / "docs" / "spec" / "grammar.ebnf"),
))

# --- Lazy-loaded data ---
_stdlib_sigs: list[dict] | None = None
_error_codes: dict | None = None
_grammar_text: str | None = None


def _load_stdlib() -> list[dict]:
    """Load stdlib function signatures from JSON."""
    global _stdlib_sigs
    if _stdlib_sigs is not None:
        return _stdlib_sigs
    if _STDLIB_SIGS_PATH.exists():
        with open(_STDLIB_SIGS_PATH) as f:
            _stdlib_sigs = json.load(f)
    else:
        _stdlib_sigs = []
    return _stdlib_sigs


def _load_error_codes() -> dict:
    """Load error code explanations from JSON."""
    global _error_codes
    if _error_codes is not None:
        return _error_codes
    if _ERROR_CODES_PATH.exists():
        with open(_ERROR_CODES_PATH) as f:
            _error_codes = json.load(f)
    else:
        _error_codes = {}
    return _error_codes


def _load_grammar() -> str:
    """Load grammar EBNF text."""
    global _grammar_text
    if _grammar_text is not None:
        return _grammar_text
    for path in [_GRAMMAR_PATH, _LOCAL_GRAMMAR]:
        if path.exists():
            _grammar_text = path.read_text()
            return _grammar_text
    _grammar_text = ""
    return _grammar_text


# --- Hardcoded syntax quick-reference ---
SYNTAX_RULES = {
    "keywords": "Keywords (13): m f t i if el lp br let mut as rt mt",
    "module": "Module declaration: m=name; (must be first line, lowercase)",
    "import": "Import: i=alias:std.module; then use alias.func()",
    "function": "Function: f=name(p1:type;p2:type):rettype{body};",
    "return": "Return: < expr; (preferred) or rt expr;",
    "let": "Immutable binding: let x=42;",
    "mut": "Mutable binding: let x=mut.0; then x=x+1; — WITHOUT mut. you CANNOT reassign",
    "if": "Conditional: if(cond){body}el{body} — no 'else', use 'el'",
    "loop": "Loop: lp(let i=0;i<n;i=i+1){body} or lp(cond){body}",
    "match": "Match: mt expr {$Variant:name body; $Variant2:name body}",
    "array": "Array literal: @(1;2;3) — no square brackets. Access: arr.get(idx)",
    "map": "Map literal: @(key1:val1;key2:val2)",
    "struct": "Struct literal: $TypeName{field1:val1;field2:val2}",
    "types": "Types: i64 u64 f64 str bool void byte — use $ prefix in signatures",
    "semicolons": "Semicolons separate ALL statements AND function parameters. NEVER commas.",
    "operators": "Comparison: = (eq) != < > <= >= — Logical: && || ! — Arithmetic: + - * / %",
    "arena": "Arena block: {arena stmts} — scoped memory, values cannot escape",
    "funcref": "Function reference: &funcname",
    "cast": "Type cast: expr as type (e.g. x as i64)",
    "error_union": "Error union: T!ErrType — propagate with ! operator",
    "string_ops": "String building: str.buf() then str.add(buf;s) then str.done(buf)",
    "no_keywords": "NOT toke keywords: return fn func for while else int string var const",
    "no_varnames": "NEVER use i/f/t/m as variable names — they are keywords",
    "no_brackets": "No square brackets — use @(items) for arrays, arr.get(idx) for access",
}


def search_stdlib(query: str) -> list[dict]:
    """Find matching stdlib function signatures.

    Args:
        query: Search string (e.g. "split", "str.split", "sqrt", "read file")

    Returns:
        List of matching signature dicts with module, function, params, return_type.
    """
    sigs = _load_stdlib()
    query_lower = query.lower().strip()
    query_words = query_lower.split()

    scored = []
    for sig in sigs:
        func_name = sig["function"].lower()
        module = sig["module"].lower()
        score = 0

        # Exact function name match
        if query_lower == func_name:
            score += 100
        # Exact function name after dot (e.g. "split" matches "str.split")
        elif "." in func_name and query_lower == func_name.split(".")[-1]:
            score += 80
        # Query is a prefix of function name
        elif func_name.startswith(query_lower):
            score += 60
        # Function name contains query
        elif query_lower in func_name:
            score += 40
        # Module name contains query
        elif query_lower in module:
            score += 20

        # Multi-word: check if all words appear in function+module
        if score == 0 and len(query_words) > 1:
            combined = f"{module} {func_name} {' '.join(sig.get('params', []))}"
            if all(w in combined for w in query_words):
                score += 30

        # Boost for word overlap with params
        if score > 0:
            param_str = " ".join(sig.get("params", [])).lower()
            for word in query_words:
                if word in param_str:
                    score += 5

        if score > 0:
            scored.append((score, sig))

    scored.sort(key=lambda x: -x[0])
    return [s[1] for s in scored[:10]]


def search_grammar(query: str) -> str:
    """Find relevant grammar rules for a query.

    Args:
        query: Search term (e.g. "loop", "if", "function", "array", "match")

    Returns:
        String containing matching grammar rules and syntax notes.
    """
    grammar = _load_grammar()
    query_lower = query.lower().strip()

    # Map common terms to grammar rule names
    term_map = {
        "loop": ["LoopStmt", "lp"],
        "lp": ["LoopStmt", "lp"],
        "for": ["LoopStmt", "lp"],
        "while": ["LoopStmt", "lp"],
        "if": ["IfStmt", "if", "el"],
        "else": ["IfStmt", "el"],
        "el": ["IfStmt", "el"],
        "function": ["FuncDecl", "ParamList", "ReturnSpec"],
        "func": ["FuncDecl", "ParamList", "ReturnSpec"],
        "fn": ["FuncDecl", "ParamList", "ReturnSpec"],
        "return": ["ReturnStmt"],
        "let": ["BindStmt", "MutBindStmt"],
        "bind": ["BindStmt", "MutBindStmt"],
        "mut": ["MutBindStmt"],
        "mutable": ["MutBindStmt"],
        "match": ["MatchExpr", "MatchArmList", "MatchArm"],
        "mt": ["MatchExpr", "MatchArmList", "MatchArm"],
        "array": ["ArrayLit", "ArrayTypeExpr"],
        "map": ["MapLit", "MapTypeExpr"],
        "struct": ["StructLit", "TypeDecl"],
        "type": ["TypeDecl", "TypeExpr", "ScalarType"],
        "import": ["ImportDecl"],
        "module": ["ModuleDecl"],
        "break": ["BreakStmt"],
        "arena": ["ArenaStmt"],
        "expr": ["Expr", "LogOrExpr", "AddExpr", "MulExpr", "CallExpr"],
        "call": ["CallExpr", "ArgList"],
        "assign": ["AssignStmt"],
        "param": ["ParamList", "Param"],
    }

    # Collect grammar rule names to search for
    search_terms = term_map.get(query_lower, [query])

    results = []

    # Search grammar text for matching rule definitions
    if grammar:
        lines = grammar.split("\n")
        for term in search_terms:
            for i, line in enumerate(lines):
                # Match rule definition lines (e.g. "LoopStmt     = ...")
                if term in line and "=" in line:
                    # Collect the full rule (may span multiple lines)
                    rule_lines = [line]
                    j = i + 1
                    while j < len(lines) and lines[j].strip() and not (
                        lines[j].strip().startswith("(*") or
                        (re.match(r"^[A-Z]\w+\s+=", lines[j]) and "=" in lines[j])
                    ):
                        rule_lines.append(lines[j])
                        j += 1
                    rule_text = "\n".join(rule_lines)
                    if rule_text not in results:
                        results.append(rule_text)

    # Add hardcoded syntax rules
    syntax_matches = []
    for key, rule in SYNTAX_RULES.items():
        if query_lower in key or query_lower in rule.lower():
            syntax_matches.append(rule)

    parts = []
    if results:
        parts.append("Grammar rules:\n" + "\n\n".join(results))
    if syntax_matches:
        parts.append("Syntax notes:\n" + "\n".join(f"- {r}" for r in syntax_matches))

    return "\n\n".join(parts) if parts else f"No grammar rules found for '{query}'"


def search_errors(error_code: str) -> str:
    """Explain what an error means and how to fix it.

    Args:
        error_code: Error code string (e.g. "E4070", "E2002", "e2003")

    Returns:
        Human-readable explanation with fix guidance.
    """
    codes = _load_error_codes()
    code = error_code.upper().strip()

    if code in codes:
        entry = codes[code]
        return (
            f"{code}: {entry['title']}\n"
            f"Stage: {entry['stage']}\n"
            f"Explanation: {entry['explanation']}\n"
            f"Fix: {entry['fix']}"
        )

    # Try partial match (e.g. "4070" -> "E4070")
    if not code.startswith("E") and not code.startswith("W"):
        for prefix in ["E", "W"]:
            candidate = prefix + code
            if candidate in codes:
                entry = codes[candidate]
                return (
                    f"{candidate}: {entry['title']}\n"
                    f"Stage: {entry['stage']}\n"
                    f"Explanation: {entry['explanation']}\n"
                    f"Fix: {entry['fix']}"
                )

    # Return series-level info
    if code and code[0] == "E" and len(code) >= 2:
        series = code[1]
        series_map = {
            "1": "Lexer error — check for invalid characters, bad escape sequences, unterminated strings",
            "2": "Parser error — check for missing semicolons, wrong keywords, unclosed delimiters, declaration order",
            "3": "Name resolution error — check for undeclared identifiers, duplicate declarations, wrong import aliases",
            "4": "Type checker error — check for type mismatches, immutable assignment, non-exhaustive match",
            "5": "Arena error — check for values escaping arena scope",
            "6": "IR lowering error — internal compiler issue",
            "9": "Codegen/internal error — may indicate compiler bug or unsupported feature",
        }
        if series in series_map:
            return f"{code}: Unknown error code in series E{series}xxx\n{series_map[series]}"

    return f"{code}: Unknown error code. Check compiler output for details."


def get_context_for_repair(source: str, error: str) -> str:
    """Given broken source and compiler error, return relevant docs for repair prompt.

    This is the main entry point for worker-generate.py. It analyzes the error
    and source to determine which documentation is most relevant, then returns
    a string to append to the repair prompt.

    Args:
        source: The broken toke source code
        error: The compiler error output

    Returns:
        String containing relevant documentation context for the repair prompt.
    """
    sections = []

    # 1. Extract and explain error codes
    error_codes_found = re.findall(r"[EW]\d{4}", error.upper())
    if error_codes_found:
        explanations = []
        for code in sorted(set(error_codes_found)):
            explanations.append(search_errors(code))
        sections.append("ERROR CODE REFERENCE:\n" + "\n\n".join(explanations))

    # 2. Detect what grammar constructs are involved
    error_lower = error.lower()
    source_lower = source.lower()
    grammar_queries = set()

    if "immutable" in error_lower or "e4070" in error_lower or "cannot assign" in error_lower:
        grammar_queries.add("mut")
    if "parse" in error_lower or "unexpected" in error_lower or "e2002" in error_lower:
        grammar_queries.add("function")
        # Check what constructs appear in source
        if "lp(" in source_lower or "lp (" in source_lower:
            grammar_queries.add("loop")
        if "if(" in source_lower or "if (" in source_lower:
            grammar_queries.add("if")
        if "mt " in source_lower:
            grammar_queries.add("match")
    if "semicolon" in error_lower or "e2003" in error_lower:
        grammar_queries.add("param")
    if "not declared" in error_lower or "e3011" in error_lower:
        grammar_queries.add("import")
    if "type mismatch" in error_lower or "e4031" in error_lower:
        grammar_queries.add("type")
    if "match" in error_lower or "e4010" in error_lower or "e4011" in error_lower:
        grammar_queries.add("match")
    if "arena" in error_lower or "e5001" in error_lower:
        grammar_queries.add("arena")
    if "array" in error_lower or "@(" in source:
        grammar_queries.add("array")

    if grammar_queries:
        grammar_parts = []
        for q in sorted(grammar_queries):
            result = search_grammar(q)
            if "No grammar rules found" not in result:
                grammar_parts.append(result)
        if grammar_parts:
            sections.append("GRAMMAR REFERENCE:\n" + "\n\n".join(grammar_parts))

    # 3. Find relevant stdlib functions mentioned in source or error
    stdlib_context = _find_relevant_stdlib(source, error)
    if stdlib_context:
        sections.append("STDLIB REFERENCE:\n" + stdlib_context)

    # 4. Add key syntax reminders based on common mistakes
    reminders = _get_syntax_reminders(source, error)
    if reminders:
        sections.append("SYNTAX REMINDERS:\n" + "\n".join(f"- {r}" for r in reminders))

    if not sections:
        # Fallback: provide general syntax reference
        sections.append("GENERAL SYNTAX REFERENCE:\n" + "\n".join(
            f"- {r}" for r in SYNTAX_RULES.values()
        ))

    return "\n\n---\n\n".join(sections)


def _find_relevant_stdlib(source: str, error: str) -> str:
    """Find stdlib functions relevant to the source and error."""
    combined = source + " " + error

    # Extract import aliases and module paths from source
    # Pattern: i=alias:std.module;
    imports = re.findall(r"i\s*=\s*(\w+)\s*:\s*([\w.]+)", source)
    alias_to_module = {alias: module for alias, module in imports}

    # Find function calls in source: alias.func(...)
    calls = re.findall(r"(\w+)\.(\w+)\s*\(", combined)

    relevant_funcs = []
    seen = set()

    for alias, func_name in calls:
        module = alias_to_module.get(alias, "")
        # Search for the function
        search_term = f"{alias}.{func_name}" if not module else func_name
        results = search_stdlib(search_term)
        for sig in results[:3]:
            key = sig["function"]
            if key not in seen:
                seen.add(key)
                params_str = ", ".join(sig["params"])
                relevant_funcs.append(
                    f"  {sig['function']}({params_str}) -> {sig['return_type']}"
                )

    # Also check if error mentions "undefined reference" — may need import help
    if "undefined" in error.lower() or "not declared" in error.lower():
        # Extract identifiers from error that might be function names
        idents = re.findall(r"'(\w+)'", error)
        for ident in idents:
            results = search_stdlib(ident)
            for sig in results[:2]:
                key = sig["function"]
                if key not in seen:
                    seen.add(key)
                    params_str = ", ".join(sig["params"])
                    relevant_funcs.append(
                        f"  {sig['function']}({params_str}) -> {sig['return_type']}  [module: {sig['module']}]"
                    )

    return "\n".join(relevant_funcs) if relevant_funcs else ""


def _get_syntax_reminders(source: str, error: str) -> list[str]:
    """Generate targeted syntax reminders based on common mistakes."""
    reminders = []
    error_lower = error.lower()
    source_lower = source.lower()

    # Mutable variable issues
    if "immutable" in error_lower or "e4070" in error_lower or "cannot assign" in error_lower:
        reminders.append(
            "MUTABLE: let x=mut.0; (integers), let s=mut.\"\"; (strings), "
            "let f=mut.0.0; (floats), let a=mut.@(); (arrays)"
        )
        reminders.append(
            "EVERY variable that gets reassigned (x=x+1, x=newval) MUST be declared with mut."
        )

    # Comma vs semicolon
    if "," in source:
        reminders.append(
            "SEMICOLONS not commas: f=name(a:i64;b:str):i64{...} and @(1;2;3) not @(1,2,3)"
        )

    # Common keyword mistakes
    if "return" in source_lower and "< " not in source:
        reminders.append("RETURN: use '< expr' not 'return expr'. 'return' is not a toke keyword.")
    if "else" in source_lower and "el" not in source_lower:
        reminders.append("ELSE: use 'el' not 'else'. el{...} after if(...){...}.")
    if re.search(r"\bfor\b", source_lower):
        reminders.append("FOR LOOP: use 'lp' not 'for'. lp(init;cond;step){body}.")
    if re.search(r"\bfn\b", source_lower) or re.search(r"\bfunc\b", source_lower):
        reminders.append("FUNCTION: use 'f=' not 'fn'/'func'. f=name(params):rettype{body};")

    # Parse errors — general guidance
    if "e2002" in error_lower or "unexpected" in error_lower:
        reminders.append("Check for: commas (use ;), wrong keywords, missing semicolons between statements.")

    # Semicolon issues
    if "e2003" in error_lower or "semicolon" in error_lower:
        reminders.append("Semicolons between ALL statements. Omit only before } or EOF.")
        reminders.append("Function params separated by ; not , : f=name(a:i64;b:str):rettype{...}")

    # Undeclared identifiers
    if "e3011" in error_lower or "not declared" in error_lower:
        reminders.append(
            "Use import ALIAS to call stdlib: i=s:std.str; then s.split() not str.split()"
        )
        reminders.append(
            "Don't use i/f/t/m as variable names — they are keywords."
        )

    # Array-related
    if "[" in source and "@(" not in source:
        reminders.append("NO square brackets: use @(1;2;3) for arrays, arr.get(idx) for access.")

    # Type issues
    if "e4031" in error_lower or "type mismatch" in error_lower:
        reminders.append("Cast with 'as': (x as i64), (n as f64). Check i64 vs f64 in operations.")

    return reminders


def format_signature(sig: dict) -> str:
    """Format a stdlib signature dict as a human-readable string."""
    params_str = ", ".join(sig.get("params", []))
    return f"{sig['function']}({params_str}) -> {sig['return_type']}"


# --- CLI for testing ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 toke_docs_lookup.py stdlib <query>")
        print("  python3 toke_docs_lookup.py grammar <query>")
        print("  python3 toke_docs_lookup.py error <code>")
        print("  python3 toke_docs_lookup.py repair <source> <error>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "stdlib" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        results = search_stdlib(query)
        for sig in results:
            print(format_signature(sig))

    elif cmd == "grammar" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        print(search_grammar(query))

    elif cmd == "error" and len(sys.argv) >= 3:
        code = sys.argv[2]
        print(search_errors(code))

    elif cmd == "repair" and len(sys.argv) >= 4:
        source = sys.argv[2]
        error = sys.argv[3]
        print(get_context_for_repair(source, error))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
