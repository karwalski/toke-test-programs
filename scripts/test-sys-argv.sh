#!/bin/sh
# 136.80: the system-tools programs that used to build a /bin/sh -c command
# line out of an input value (the SYS-102 class) must run their tools
# argv-only. For each one this script (1) does a normal round trip and
# (2) feeds input values holding ; $() backticks spaces and quotes, then
# asserts that nothing they name was executed and that the value reached the
# tool as one literal argument.
#
# Every hostile value carries the same segment, built so that it breaks out
# of each quoting the old programs used -- unquoted, '...' and "..." -- and
# runs `touch M<n>` in the program's working directory ($D):
#     x'$(touch M1)'"$(touch M2)";touch M3;`touch M4` y
# Under /bin/sh -c at least one of M1..M4 appears; argv-only, none does.
#
# usage: scripts/test-sys-argv.sh [ID ...]     (default: all nine)
#   TOKE_BIN  overrides the compiler (default ~/tk/toke/toke)
#   SOL_DIR   overrides the solutions directory, e.g. to run the old
#             programs and watch this script fail
# Builds each program with exactly the grants scripts/cap-manifests.py
# derives from its calls (ADR-0010), never --allow-all.
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TOKE=${TOKE_BIN:-$HOME/tk/toke/toke}
SOL_DIR=${SOL_DIR:-$ROOT/results/solutions/system-tools}
ALL="SYS-045 SYS-077 SYS-085 SYS-087 SYS-097 SYS-098 SYS-104 SYS-113 SYS-120"
IDS=${*:-$ALL}
D=$(mktemp -d) || exit 1
D=$(cd "$D" && pwd -P)
trap 'rm -rf "$D"' EXIT
cd "$D" || exit 1
HS=$(printf '%s' "x'\$(touch M1)'\"\$(touch M2)\";touch M3;\`touch M4\` y")
fail=0
bad() { echo "FAIL $ID: $*"; fail=1; idfail=1; }

# Build $1 into $D/$1.bin with the grants its calls need.
build() {
  python3 - "$ROOT/scripts/cap-manifests.py" "$SOL_DIR/$1/solution.tk" > "$D/$1.toml" <<'EOF' || return 1
import importlib.util, sys
sp = importlib.util.spec_from_file_location("cm", sys.argv[1])
cm = importlib.util.module_from_spec(sp); sp.loader.exec_module(cm)
need, unknown = cm.grants(open(sys.argv[2]).read())
if unknown: sys.exit("unknown gated calls: %s" % unknown)
print(cm.render(need) if need else "")
EOF
  "$TOKE" "$SOL_DIR/$1/solution.tk" --config="$D/$1.toml" --out "$D/$1.bin" > "$D/$1.build.log" 2>&1
}

# Any marker the hostile segment can create, anywhere under $D.
nomarks() {
  m=$(find "$D" -name 'M[0-9]' 2>/dev/null)
  [ -z "$m" ] || { bad "shell injection ran: $(echo "$m" | sed "s|$D/||" | tr '\n' ' ')"; find "$D" -name 'M[0-9]' -exec rm -f {} +; }
}

t045() {  # archive extractor: hostile archive path and destination
  mkdir -p src/sub && echo a > src/a.txt && echo b > src/sub/b.txt
  A="$D/a $HS.tar.gz"; Z="$D/z $HS.zip"
  tar czf "$A" -C src a.txt sub
  (cd src && zip -qr "$Z" a.txt sub)
  for arc in "$A" "$Z"; do
    dest="$D/out $HS"; rm -rf "$dest"
    printf '%s\n%s\n' "$arc" "$dest" | "$B" > out 2>&1
    nomarks
    [ -f "$dest/a.txt" ] && [ -f "$dest/sub/b.txt" ] || bad "not extracted from $(basename "$arc" | cut -c1-6)..."
    grep -Fxq "Done: 2 files extracted to $dest." out || bad "summary line: $(tail -1 out)"
    grep -Fxq "extracted: sub/b.txt" out || bad "listing: $(head -3 out | tr '\n' '|')"
  done
}

t077() {  # script runner: the command is shell by design, the timeout is not
  printf '1\necho hi\n' | "$B" > out 2>&1
  head -1 out | grep -Fxq hi && grep -q '^exit=0 ' out || bad "round trip: $(tr '\n' '|' < out)"
  printf '0.2\nsleep 3\n' | "$B" > out 2>&1
  grep -q '^exit=124 .* TIMEOUT$' out || bad "timeout: $(tr '\n' '|' < out)"
  printf '%s\necho hi\n' "1$HS" | "$B" > out 2>&1
  nomarks
}

t085() {  # file watcher: hostile watched path; a stub stat logs its argv
  W="$D/w $HS"; echo x > "$W"
  printf '%s\necho triggered\n1\n' "$W" | "$B" > out 2>&1
  nomarks
  [ ! -s out ] || bad "unchanged file reported: $(tr '\n' '|' < out)"
  # A stub `stat` that prints a new mtime on every call forces a change
  # and records each argument on its own line (spawn takes PATH at start).
  mkdir -p fake
  printf '#!/bin/sh\nn=$(cat %s/n 2>/dev/null || echo 0); n=$((n+1)); echo $n > %s/n\nfor a in "$@"; do printf "%%s\\n" "$a" >> %s/argv; done\necho $n\n' "$D" "$D" "$D" > fake/stat
  chmod +x fake/stat
  printf '%s\necho triggered\n1\n' "$W" | PATH="$D/fake:$PATH" "$B" > out 2>&1
  nomarks
  grep -q '^Change detected: ' out && grep -Fxq 'Running: echo triggered' out \
    && grep -Fxq 'Output: triggered' out || bad "change round trip: $(tr '\n' '|' < out)"
  grep -Fxq -- "$W" argv 2>/dev/null || bad "stat did not receive the path as one argument"
  printf '/nonexistent/z\necho x\n1\n' | "$B" > out 2>&1
  grep -Fxq 'ERROR: path not found: /nonexistent/z' out || bad "missing path: $(cat out)"
}

t087() {  # permission fixer: hostile directory and subdirectory names, hostile mode
  P="$D/p $HS"; mkdir -p "$P/s $HS"
  echo 1 > "$P/f $HS"; echo 2 > "$P/s $HS/g"
  chmod 600 "$P/f $HS" "$P/s $HS/g"; chmod 700 "$P" "$P/s $HS"
  printf '%s\n644\n755\nyes\n' "$P" | "$B" > out 2>&1
  nomarks
  grep -Fxq 'Summary: 4 files changed.' out || bad "dry run: $(tail -1 out)"
  [ "$(stat -f %Lp "$P/f $HS")" = 600 ] || bad "dry run changed a mode"
  printf '%s\n\n\nno\n' "$P" | "$B" > out 2>&1
  nomarks
  grep -Fxq 'Summary: 4 files changed.' out || bad "fix: $(tail -1 out)"
  grep -Fxq "chmod 644 $P/f $HS" out || bad "chmod line for the hostile file name"
  for f in "$P/f $HS" "$P/s $HS/g"; do [ "$(stat -f %Lp "$f")" = 644 ] || bad "file mode not 644"; done
  for f in "$P" "$P/s $HS"; do [ "$(stat -f %Lp "$f")" = 755 ] || bad "dir mode not 755"; done
  chmod 600 "$P/f $HS"
  printf '%s\n644;touch M5\n755\nno\n' "$P" | "$B" > out 2>&1
  nomarks
  [ "$(stat -f %Lp "$P/f $HS")" = 600 ] || bad "hostile mode was applied"
}

pidtests() {  # SYS-097/098: a hostile PID, alone and after a live PID
  sleep 30 & SP=$!
  for pid in "$HS" "$SP;touch M3" "$SP \$(touch M1)"; do
    printf '%s\n' "$pid" | "$B" > out 2>&1
    nomarks
    case "$pid" in *';'*) grep -Fxq "ERROR: PID not found: $pid" out || bad "hostile PID not rejected: $(head -1 out)";; esac
  done
  printf '%s\n' "$SP" | "$B" > out 2>&1
  printf '99999999\n' | "$B" > miss 2>&1
  kill "$SP" 2>/dev/null; wait "$SP" 2>/dev/null
  grep -Fxq 'ERROR: PID not found: 99999999' miss || bad "missing PID: $(cat miss)"
}

t097() {  # open-fd lister
  pidtests
  [ -s out ] || bad "no fds listed for a live process"
  grep -q '^txt REG .*sleep$' out || bad "no 'txt REG .../sleep' line: $(head -2 out | tr '\n' '|')"
}

t098() {  # namespace lister
  pidtests
  exp=""
  for ns in pid net mnt uts ipc user; do
    v=$(readlink "/proc/$SP/ns/$ns" 2>/dev/null); exp="$exp$ns: ${v:-unavailable}
"
  done
  [ "$(cat out)" = "$(printf '%s' "$exp")" ] || bad "namespaces: $(tr '\n' '|' < out)"
}

t104() {  # git stats: hostile repository path
  R="$D/r $HS"; mkdir -p "$R"
  ( cd "$R" && git init -q && git config user.email t@t && git config user.name t \
    && for i in 1 2 3; do echo "$i" >> a.txt; echo "$i" > "b$i.txt"; git add -A; git commit -qm "c$i"; done \
    && echo 4 >> a.txt && echo y >> b1.txt && git commit -qam c4 ) || { bad "fixture repo"; return; }
  printf '%s\n' "$R" | "$B" > out 2>&1
  nomarks
  # git log puts a blank line between commits; it names no file (136.81)
  top=$(git -C "$R" log --pretty=format: --name-only | grep -v '^$' | LC_ALL=C sort | uniq -c \
        | awk '{c=$1; sub(/^ *[0-9]+ ?/, ""); printf "%4d %s\n", c, $0}' | LC_ALL=C sort -rn | head -5)
  exp=$(printf 'Commits: 4\nContributors: 1\nBranches: 1\nTop files: %s' "$(printf '%s' "$top" | sed '1s/^ *//')")
  [ "$(cat out)" = "$exp" ] || { bad "stats differ from the git reference"; printf '%s\n---\n' "$exp"; cat out; }
  printf '/nonexistent/r\n' | "$B" > out 2>&1
  grep -Fxq 'ERROR: not a git repository: /nonexistent/r' out || bad "missing repo: $(cat out)"
}

t113() {  # directory hash: hostile directory and file names, binary content
  H="$D/h $HS"; mkdir -p "$H/sub"
  echo a > "$H/b.txt"; printf 'x\000y\377z' > "$H/a $HS.bin"; echo q > "$H/sub/C"; echo w > "$H/Z"
  printf '%s\n' "$H" | "$B" > out 2>&1
  nomarks
  ref=$(find "$H" -type f -print0 | LC_ALL=C sort -z | xargs -0 cat | shasum -a 256 | cut -d' ' -f1)
  grep -Fxq "Directory hash: $ref" out || bad "hash $(cat out) != reference $ref"
  mkdir -p "$D/empty"
  printf '%s\n' "$D/empty" | "$B" > out 2>&1
  grep -Fxq 'Directory hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' out || bad "empty dir: $(cat out)"
}

t120() {  # decompressor: hostile input and output paths, every format present
  printf 'hello\nworld\n' > plain
  for tool in gzip bzip2 xz zstd; do
    command -v "$tool" >/dev/null || { echo "  (SYS-120: $tool not installed, skipped)"; continue; }
    I="$D/i $HS.$tool"; O="$D/o $HS.$tool.txt"
    "$tool" -c < plain > "$I"
    printf '%s\n%s\n' "$I" "$O" | "$B" > out 2>&1
    nomarks
    cmp -s plain "$O" || bad "$tool: output file differs"
    grep -Fxq "Decompressed: 12 bytes to $O" out || bad "$tool: $(cat out)"
    printf '%s\n-\n' "$I" | "$B" > out 2>&1
    nomarks
    cmp -s plain out || bad "$tool: stdout differs"
  done
  gzip -c < plain > ./-n.gz      # an operand that looks like an option
  printf -- '-n.gz\n-\n' | "$B" > out 2>&1
  cmp -s plain out || bad "a leading-dash path was taken as an option"
}

for ID in $IDS; do
  idfail=0
  W="$D/$ID.work"; mkdir -p "$W"
  build "$ID" || { bad "build"; cat "$D/$ID.build.log"; continue; }
  B="$D/$ID.bin"
  cd "$W" || exit 1
  D0=$D; D=$W
  case $ID in
    SYS-045) t045;; SYS-077) t077;; SYS-085) t085;; SYS-087) t087;;
    SYS-097) t097;; SYS-098) t098;; SYS-104) t104;; SYS-113) t113;;
    SYS-120) t120;; *) bad "no test for $ID";;
  esac
  D=$D0; cd "$D" || exit 1
  [ $idfail -eq 0 ] && echo "PASS $ID"
done
[ $fail -eq 0 ] && echo "PASS: argv-only ($(echo $IDS | wc -w | tr -d ' ') programs, round trip + hostile input)"
exit $fail
