#!/bin/zsh

set -euo pipefail

cd "$(dirname "$0")"

port="${1:-8000}"
log_file="${TMPDIR:-/tmp}/timefasss-page-runner.log"

python3 -m http.server "$port" >"$log_file" 2>&1 &
server_pid=$!

cleanup() {
  if kill -0 "$server_pid" >/dev/null 2>&1; then
    kill "$server_pid" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT INT TERM

for _ in {1..50}; do
  if curl -fs "http://127.0.0.1:${port}/page-runner.html" >/dev/null 2>&1; then
    open "http://127.0.0.1:${port}/page-runner.html"
    wait "$server_pid"
    exit $?
  fi
  perl -e 'select(undef, undef, undef, 0.1)'
done

echo "Server did not start on port ${port}."
echo "Check ${log_file} for details."
exit 1