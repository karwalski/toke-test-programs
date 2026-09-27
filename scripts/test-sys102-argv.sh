#!/bin/sh
# 136.72: SYS-102 must run openssl argv-only. A passphrase or path holding
# shell metacharacters is data, never a command. Builds the solution with its
# own tkc.toml grants, then (1) round-trips a file, (2) feeds a hostile path
# and a hostile passphrase and asserts nothing they name was executed.
# usage: scripts/test-sys102-argv.sh [solution.tk]   (TOKE_BIN overrides tkc)
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TOKE=${TOKE_BIN:-$HOME/tk/toke/toke}
SOL=${1:-$ROOT/results/solutions/system-tools/SYS-102/solution.tk}
MAN=$ROOT/results/solutions/system-tools/SYS-102/tkc.toml
command -v openssl >/dev/null || { echo "SKIP: openssl not installed"; exit 0; }
D=$(mktemp -d) || exit 1
trap 'rm -rf "$D"' EXIT
"$TOKE" "$SOL" --config="$MAN" --out "$D/b" >"$D/build.log" 2>&1 \
  || { echo "FAIL: build"; cat "$D/build.log"; exit 1; }
fail=0
echo "plain text" > "$D/plain.txt"
printf 'encrypt\n%s\n%s\nmypass\n' "$D/plain.txt" "$D/enc.bin" | "$D/b" >/dev/null 2>&1
printf 'decrypt\n%s\n%s\nmypass\n' "$D/enc.bin" "$D/dec.txt" | "$D/b" >/dev/null 2>&1
cmp -s "$D/plain.txt" "$D/dec.txt" || { echo "FAIL: round trip"; fail=1; }
# Hostile inputs. The path is a real file whose name contains $(...); the
# passphrase ends in '; touch ...'. Under /bin/sh -c either one runs touch
# (in the program's working directory, $D).
cd "$D" || exit 1
HP="$D/p\$(touch MARK_PATH).txt"
echo "hostile name" > "$HP"
printf 'encrypt\n%s\n%s\n%s\n' "$HP" "$D/h.bin" "pw; touch MARK_PASS" > "$D/in"
"$D/b" < "$D/in" > "$D/out" 2>&1
for m in MARK_PATH MARK_PASS; do
  [ -e "$D/$m" ] && { echo "FAIL: shell injection ran 'touch $m'"; fail=1; }
done
[ -s "$D/h.bin" ] || { echo "FAIL: hostile-named input was not encrypted as a literal path"; fail=1; }
printf 'decrypt\n%s\n%s\n%s\n' "$D/h.bin" "$D/h.txt" "pw; touch MARK_PASS" > "$D/in"
"$D/b" < "$D/in" > /dev/null 2>&1
cmp -s "$HP" "$D/h.txt" || { echo "FAIL: hostile passphrase did not round-trip as a literal"; fail=1; }
[ $fail -eq 0 ] && echo "PASS: SYS-102 argv-only (round trip, hostile path, hostile passphrase)"
exit $fail
