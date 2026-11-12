"""worker_config.py -- worker SSH settings for the infra/ scripts.

The repository is public, so no key path, user or address is committed.
Settings come from the environment first, then from the gitignored
``infra/workers.local.conf`` (template: ``workers.local.conf.example``).
Worker addresses come from the gitignored ``infra/workers.json``.
"""

import os
import sys
from pathlib import Path

INFRA = Path(__file__).resolve().parent
LOCAL_CONF = INFRA / "workers.local.conf"

_DEFAULTS = {"TOKE_WORKER_SSH_USER": "ubuntu"}


def _read_conf(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        values[key.strip()] = val
    return values


def setting(name: str, required: bool = True) -> str:
    """Return a worker setting from the environment or workers.local.conf."""
    val = os.environ.get(name) or _read_conf(LOCAL_CONF).get(name) \
        or _DEFAULTS.get(name, "")
    if not val and required:
        sys.exit(f"ERROR: {name} is not set. Export it, or copy "
                 f"{LOCAL_CONF.name}.example to {LOCAL_CONF.name} and fill it in.")
    return os.path.expandvars(os.path.expanduser(val))


def ssh_key() -> Path:
    return Path(setting("TOKE_WORKER_SSH_KEY"))


def ssh_user() -> str:
    return setting("TOKE_WORKER_SSH_USER")
