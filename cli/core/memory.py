from pathlib import Path
from datetime import datetime, timezone
import json


USER_ROOT = Path.home() / ".cadierno-ai"
USER_PROFILE_FILE = USER_ROOT / "profile.json"
USER_PREFERENCES_FILE = USER_ROOT / "preferences.json"
USER_HISTORY_FILE = USER_ROOT / "history.json"

WORKSPACE_DIRNAME = ".cadierno"
WORKSPACE_PROFILE_FILE = "profile.json"
WORKSPACE_PREFERENCES_FILE = "preferences.json"
WORKSPACE_HISTORY_FILE = "history.json"
WORKSPACE_METADATA_FILE = "workspace.json"


def _read_json(path: Path, default):

    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, payload) -> None:

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _workspace_memory_root(project_path: Path) -> Path:
    return project_path / "memory" / WORKSPACE_DIRNAME


def ensure_user_memory() -> None:

    USER_ROOT.mkdir(parents=True, exist_ok=True)

    if not USER_PROFILE_FILE.exists():
        _write_json(
            USER_PROFILE_FILE,
            {
                "name": "",
                "role": "",
                "seniority": "",
                "updated_at": _now_iso(),
            },
        )

    if not USER_PREFERENCES_FILE.exists():
        _write_json(
            USER_PREFERENCES_FILE,
            {
                "communication_style": "professional",
                "updated_at": _now_iso(),
            },
        )

    if not USER_HISTORY_FILE.exists():
        _write_json(USER_HISTORY_FILE, [])


def ensure_workspace_memory(project_path: Path) -> None:

    root = _workspace_memory_root(project_path)
    root.mkdir(parents=True, exist_ok=True)

    profile_path = root / WORKSPACE_PROFILE_FILE
    preferences_path = root / WORKSPACE_PREFERENCES_FILE
    history_path = root / WORKSPACE_HISTORY_FILE
    metadata_path = root / WORKSPACE_METADATA_FILE

    if not profile_path.exists():
        _write_json(
            profile_path,
            {
                "name": "",
                "role": "",
                "seniority": "",
                "updated_at": _now_iso(),
            },
        )

    if not preferences_path.exists():
        _write_json(
            preferences_path,
            {
                "communication_style": "professional",
                "updated_at": _now_iso(),
            },
        )

    if not history_path.exists():
        _write_json(history_path, [])

    if not metadata_path.exists():
        _write_json(
            metadata_path,
            {
                "project_name": project_path.name,
                "project_path": str(project_path),
                "created_at": _now_iso(),
                "last_bootstrap_at": "",
                "last_update_at": "",
            },
        )


def initialize_memory(project_path: Path) -> None:

    ensure_user_memory()
    ensure_workspace_memory(project_path)


def set_style(project_path: Path, style: str, scope: str = "workspace") -> None:

    normalized = style.strip().lower()
    if normalized not in {"argentino", "professional"}:
        raise ValueError("Style inválido. Usar: argentino | professional")

    if scope == "user":
        target = USER_PREFERENCES_FILE
        ensure_user_memory()
    else:
        ensure_workspace_memory(project_path)
        target = _workspace_memory_root(project_path) / WORKSPACE_PREFERENCES_FILE

    prefs = _read_json(target, {})
    prefs["communication_style"] = normalized
    prefs["updated_at"] = _now_iso()
    _write_json(target, prefs)


def update_profile(
    project_path: Path,
    name: str | None = None,
    role: str | None = None,
    seniority: str | None = None,
    scope: str = "workspace",
) -> None:

    if scope == "user":
        target = USER_PROFILE_FILE
        ensure_user_memory()
    else:
        ensure_workspace_memory(project_path)
        target = _workspace_memory_root(project_path) / WORKSPACE_PROFILE_FILE

    profile = _read_json(target, {})

    if name is not None:
        profile["name"] = name
    if role is not None:
        profile["role"] = role
    if seniority is not None:
        profile["seniority"] = seniority

    profile["updated_at"] = _now_iso()
    _write_json(target, profile)


def _append_history(path: Path, event: dict) -> None:

    history = _read_json(path, [])
    history.append(event)
    _write_json(path, history[-500:])


def add_history_event(project_path: Path | None, event_type: str, details: str) -> None:

    ensure_user_memory()

    event = {
        "timestamp": _now_iso(),
        "event": event_type,
        "details": details,
    }

    if project_path is not None:
        event["project"] = str(project_path)
        ensure_workspace_memory(project_path)
        workspace_history = _workspace_memory_root(project_path) / WORKSPACE_HISTORY_FILE
        _append_history(workspace_history, event)

    _append_history(USER_HISTORY_FILE, event)


def mark_workspace_event(project_path: Path, event_name: str) -> None:

    ensure_workspace_memory(project_path)
    metadata_path = _workspace_memory_root(project_path) / WORKSPACE_METADATA_FILE
    metadata = _read_json(metadata_path, {})

    if event_name == "bootstrap":
        metadata["last_bootstrap_at"] = _now_iso()
    elif event_name == "update":
        metadata["last_update_at"] = _now_iso()

    metadata["updated_at"] = _now_iso()
    _write_json(metadata_path, metadata)


def get_effective_style(project_path: Path) -> str:

    ensure_user_memory()
    ensure_workspace_memory(project_path)

    workspace_prefs = _read_json(_workspace_memory_root(project_path) / WORKSPACE_PREFERENCES_FILE, {})
    user_prefs = _read_json(USER_PREFERENCES_FILE, {})

    return workspace_prefs.get("communication_style") or user_prefs.get("communication_style") or "professional"


def get_memory_status(project_path: Path) -> dict:

    ensure_user_memory()
    ensure_workspace_memory(project_path)

    workspace_root = _workspace_memory_root(project_path)

    workspace_profile = _read_json(workspace_root / WORKSPACE_PROFILE_FILE, {})
    workspace_prefs = _read_json(workspace_root / WORKSPACE_PREFERENCES_FILE, {})
    workspace_history = _read_json(workspace_root / WORKSPACE_HISTORY_FILE, [])
    workspace_metadata = _read_json(workspace_root / WORKSPACE_METADATA_FILE, {})

    user_profile = _read_json(USER_PROFILE_FILE, {})
    user_prefs = _read_json(USER_PREFERENCES_FILE, {})
    user_history = _read_json(USER_HISTORY_FILE, [])

    return {
        "project": str(project_path),
        "effective_style": get_effective_style(project_path),
        "workspace": {
            "root": str(workspace_root),
            "profile": workspace_profile,
            "preferences": workspace_prefs,
            "history_count": len(workspace_history),
            "metadata": workspace_metadata,
        },
        "user": {
            "root": str(USER_ROOT),
            "profile": user_profile,
            "preferences": user_prefs,
            "history_count": len(user_history),
        },
    }


def get_history(project_path: Path, scope: str = "workspace", limit: int = 20) -> list[dict]:

    if scope == "user":
        ensure_user_memory()
        history = _read_json(USER_HISTORY_FILE, [])
    else:
        ensure_workspace_memory(project_path)
        history = _read_json(_workspace_memory_root(project_path) / WORKSPACE_HISTORY_FILE, [])

    return history[-max(1, limit):]
