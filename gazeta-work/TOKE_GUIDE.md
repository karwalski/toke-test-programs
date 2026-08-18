# toke quick reference (for translating Python → toke)

Module header: `m=name;i=io:std.io;i=s:std.str;` (import math as `i=m:std.math;` if needed).
Functions: `f=fname(p:i64;q:$str):i64{ <expr };`  — `<` returns. Top-level order: m, imports, types, then functions; main LAST.
main: `f=main():i64{ ...; <0 };`

## Bindings / mutation
- `let x=5;` immutable. `let x=mut.5;` mutable — REASSIGN needs mut: `x=x+1;`. Reassigning a non-mut binding = E4070.
- `=` is assignment/binding; `==` is equality (NOT `=`). `!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`, `!`.

## Types: i64, u64, f64, bool, $str.  Int division truncates; `%` = modulo. `x as f64`, `x as i64`, `x as u64` casts.

## Arrays: `@(a;b;c)` (semicolon-separated). Empty typed: `mut.@($str)` / `mut.@($i64)` / `mut.@($f64)`.
- `a.get(i)`, `a.len()`, `a=a.push(x)` (or `a=a+@(x)`), `a=a.set(i;x)`. Nested: `@(@(1;2);@(3;4))`, `g.get(i).get(j)`.

## Strings (s.):
- `s.len(x)`, `s.slice(x;start;end)` (end exclusive), `s.concat(a;b)`, `s.charat(x;i)`.
- `s.split(x;sep)`→[str], `s.fields(x)`→[str] (whitespace runs, drops empties), `s.join(sep;arr)` (SEP FIRST).
- `s.toint(x)`→i64, `s.tofloat(x)`→f64, `s.fromint(n)`→str, `s.fromfloat(x)`→str, `s.format(x;"%.6f")`→str.
- `s.contains/indexof/startswith/endswith/replace/trim/upper/lower`. String `==` works.

## Control: `if(c){...}el{...}`; expression-if `let x=if(c){a}el{b};`. `lp(cond){...}` while; `lp(let i=0;i<n;i=i+1){...}` for; `br` break. `el if(c2){...}` may be rejected — use nested `el{if(...){...}}`.
## Match: `let v=mt call(){$ok:x x;$err:e dflt};`. io: `io.readln()`, `io.eof()`, `io.println(x)`, `io.print(x)`.

## Read all stdin tokens (Gazeta contract = sys.stdin.read().split()):
```
f=readall():$str{ let all=mut.""; lp(1==1){ let ln=io.readln(); all=s.concat(all;s.concat(ln;" ")); if(io.eof()){br} }; <all };
```
then `let toks=s.fields(readall()); let a=s.toint(toks.get(0));` etc.

## Strip-trailing-zeros float format (Python `"%.6f" % x` then rstrip("0").rstrip(".")):
```
f=fmt(x:f64):$str{ let raw=s.format(x;"%.6f"); let n=mut.s.len(raw);
  lp(n>0){ if(s.slice(raw;n-1;n)=="0"){n=n-1}el{br} };
  if(n>0){ if(s.slice(raw;n-1;n)=="."){n=n-1} };
  let r=mut.s.slice(raw;0;n); if(r==""){r="0"}; if(r=="-0"){r="0"}; <r };
```
GOTCHAS: single-uppercase identifiers fail (use lowercase). No `el if` (nest it). Reassign → declare `mut.`. Match the Python's EXACT output (spacing, newlines, number formatting).
