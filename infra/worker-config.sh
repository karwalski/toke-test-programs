# worker-config.sh -- sourced by the infra/ shell scripts.
#
# The repository is public, so no key path, user or address is committed.
# Settings come from the environment first, then from the gitignored
# infra/workers.local.conf (template: workers.local.conf.example).
# Defines TOKE_WORKER_SSH_KEY and TOKE_WORKER_SSH_USER.
# shellcheck shell=bash

_wc_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_wc_env_key="${TOKE_WORKER_SSH_KEY:-}"
_wc_env_user="${TOKE_WORKER_SSH_USER:-}"
if [ -f "$_wc_dir/workers.local.conf" ]; then
    # shellcheck source=/dev/null
    . "$_wc_dir/workers.local.conf"
fi
# The environment wins over the file.
TOKE_WORKER_SSH_KEY="${_wc_env_key:-${TOKE_WORKER_SSH_KEY:-}}"
TOKE_WORKER_SSH_USER="${_wc_env_user:-${TOKE_WORKER_SSH_USER:-ubuntu}}"
# Expand a leading ~ (sourced values are expanded by the shell already;
# quoted ones and environment values may not be).
case "$TOKE_WORKER_SSH_KEY" in
    "~/"*) TOKE_WORKER_SSH_KEY="$HOME/${TOKE_WORKER_SSH_KEY#\~/}" ;;
esac
unset _wc_dir _wc_env_key _wc_env_user

require_worker_ssh_key() {
    if [ -z "$TOKE_WORKER_SSH_KEY" ]; then
        echo "ERROR: TOKE_WORKER_SSH_KEY is not set. Export it, or copy" >&2
        echo "  infra/workers.local.conf.example to infra/workers.local.conf and fill it in." >&2
        exit 2
    fi
}
