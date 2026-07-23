from pathlib import Path
from datetime import datetime, timezone
import json
import os
import sqlite3


WORKSPACE_DIRNAME = ".cadierno"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _user_root() -> Path:
    custom = os.getenv("CADIERNO_USER_MEMORY_DIR", "").strip()
    return Path(custom).expanduser() if custom else Path.home() / ".cadierno-ai"


def _workspace_dirname() -> str:
    value = os.getenv("CADIERNO_WORKSPACE_DIRNAME", "").strip()
    return value or WORKSPACE_DIRNAME


def _workspace_memory_root(project_path: Path) -> Path:
    return project_path / "memory" / _workspace_dirname()


def _user_db_path() -> Path:
    return _user_root() / "brain.db"


def _workspace_db_path(project_path: Path) -> Path:
    return _workspace_memory_root(project_path) / "brain.db"


def _connect(db_path: Path) -> sqlite3.Connection:

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS kv (
            namespace TEXT NOT NULL,
            key TEXT NOT NULL,
            value_json TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY(namespace, key)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scope TEXT NOT NULL,
            project_path TEXT,
            event_type TEXT NOT NULL,
            details TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scope TEXT NOT NULL,
            project_path TEXT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            observation_type TEXT NOT NULL,
            tags_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def _kv_get(conn: sqlite3.Connection, namespace: str, key: str, default):

    row = conn.execute(
        "SELECT value_json FROM kv WHERE namespace = ? AND key = ?",
        (namespace, key),
    ).fetchone()
    if row is None:
        return default
    try:
        return json.loads(row["value_json"])
    except Exception:
        return default


def _kv_set(conn: sqlite3.Connection, namespace: str, key: str, value) -> None:

    conn.execute(
        """
        INSERT INTO kv(namespace, key, value_json, updated_at)
        VALUES(?, ?, ?, ?)
        ON CONFLICT(namespace, key) DO UPDATE SET
            value_json = excluded.value_json,
            updated_at = excluded.updated_at
        """,
        (namespace, key, json.dumps(value, ensure_ascii=True), _now_iso()),
    )
    conn.commit()


def ensure_user_memory() -> None:

    conn = _connect(_user_db_path())
    try:
        if _kv_get(conn, "user", "profile", None) is None:
            _kv_set(conn, "user", "profile", {"name": "", "role": "", "seniority": "", "updated_at": _now_iso()})
        if _kv_get(conn, "user", "preferences", None) is None:
            _kv_set(conn, "user", "preferences", {"communication_style": "professional", "updated_at": _now_iso()})
    finally:
        conn.close()


def ensure_workspace_memory(project_path: Path) -> None:

    conn = _connect(_workspace_db_path(project_path))
    try:
        if _kv_get(conn, "workspace", "profile", None) is None:
            _kv_set(conn, "workspace", "profile", {"name": "", "role": "", "seniority": "", "updated_at": _now_iso()})
        if _kv_get(conn, "workspace", "preferences", None) is None:
            _kv_set(conn, "workspace", "preferences", {"communication_style": "professional", "updated_at": _now_iso()})
        if _kv_get(conn, "workspace", "metadata", None) is None:
            _kv_set(
                conn,
                "workspace",
                "metadata",
                {
                    "project_name": project_path.name,
                    "project_path": str(project_path),
                    "created_at": _now_iso(),
                    "last_bootstrap_at": "",
                    "last_update_at": "",
                },
            )
    finally:
        conn.close()


def initialize_memory(project_path: Path) -> None:

    ensure_user_memory()
    ensure_workspace_memory(project_path)


def set_style(project_path: Path, style: str, scope: str = "workspace") -> None:

    normalized = style.strip().lower()
    if normalized not in {"argentino", "professional"}:
        raise ValueError("Style inválido. Usar: argentino | professional")

    if scope == "user":
        ensure_user_memory()
        conn = _connect(_user_db_path())
        namespace = "user"
    else:
        ensure_workspace_memory(project_path)
        conn = _connect(_workspace_db_path(project_path))
        namespace = "workspace"

    try:
        prefs = _kv_get(conn, namespace, "preferences", {})
        prefs["communication_style"] = normalized
        prefs["updated_at"] = _now_iso()
        _kv_set(conn, namespace, "preferences", prefs)
    finally:
        conn.close()


def update_profile(project_path: Path, name: str | None = None, role: str | None = None, seniority: str | None = None, scope: str = "workspace") -> None:

    if scope == "user":
        ensure_user_memory()
        conn = _connect(_user_db_path())
        namespace = "user"
    else:
        ensure_workspace_memory(project_path)
        conn = _connect(_workspace_db_path(project_path))
        namespace = "workspace"

    try:
        profile = _kv_get(conn, namespace, "profile", {})
        if name is not None:
            profile["name"] = name
        if role is not None:
            profile["role"] = role
        if seniority is not None:
            profile["seniority"] = seniority
        profile["updated_at"] = _now_iso()
        _kv_set(conn, namespace, "profile", profile)
    finally:
        conn.close()


def add_history_event(project_path: Path | None, event_type: str, details: str) -> None:

    ensure_user_memory()
    timestamp = _now_iso()

    user_conn = _connect(_user_db_path())
    try:
        user_conn.execute(
            "INSERT INTO events(scope, project_path, event_type, details, timestamp) VALUES(?, ?, ?, ?, ?)",
            ("user", str(project_path) if project_path else "", event_type, details, timestamp),
        )
        user_conn.commit()
    finally:
        user_conn.close()

    if project_path is not None:
        ensure_workspace_memory(project_path)
        workspace_conn = _connect(_workspace_db_path(project_path))
        try:
            workspace_conn.execute(
                "INSERT INTO events(scope, project_path, event_type, details, timestamp) VALUES(?, ?, ?, ?, ?)",
                ("workspace", str(project_path), event_type, details, timestamp),
            )
            workspace_conn.commit()
        finally:
            workspace_conn.close()


def mark_workspace_event(project_path: Path, event_name: str) -> None:

    ensure_workspace_memory(project_path)
    conn = _connect(_workspace_db_path(project_path))
    try:
        metadata = _kv_get(conn, "workspace", "metadata", {})
        if event_name == "bootstrap":
            metadata["last_bootstrap_at"] = _now_iso()
        elif event_name == "update":
            metadata["last_update_at"] = _now_iso()
        metadata["updated_at"] = _now_iso()
        _kv_set(conn, "workspace", "metadata", metadata)
    finally:
        conn.close()


def set_infra_workspace_metadata(project_path: Path, root: str | None, method: str) -> None:
    """
    Guarda la última detección de workspace de infraestructura (docker-compose,
    monorepo, etc.) para este proyecto. No confundir con el scope de memoria
    "workspace" (que es memoria persistente por-proyecto): esto es información
    sobre la carpeta raíz de infraestructura compartida detectada por bootstrap,
    ver cli/core/workspace.py.
    """

    ensure_workspace_memory(project_path)
    conn = _connect(_workspace_db_path(project_path))
    try:
        metadata = _kv_get(conn, "workspace", "metadata", {})
        metadata["infra_workspace_root"] = root or ""
        metadata["infra_workspace_detection_method"] = method
        metadata["infra_workspace_last_bootstrap_at"] = _now_iso()
        metadata["updated_at"] = _now_iso()
        _kv_set(conn, "workspace", "metadata", metadata)
    finally:
        conn.close()


def get_generated_hash(project_path: Path, relative_file: str) -> str | None:
    """
    Devuelve el hash del contenido que Cadierno generó por última vez para
    `relative_file`, o None si nunca se registró. Se usa para no sobreescribir
    archivos de knowledge/ editados a mano (ver cli/commands/bootstrap.py).
    """

    ensure_workspace_memory(project_path)
    conn = _connect(_workspace_db_path(project_path))
    try:
        hashes = _kv_get(conn, "workspace", "generated_hashes", {})
        return hashes.get(relative_file)
    finally:
        conn.close()


def set_generated_hash(project_path: Path, relative_file: str, content_hash: str) -> None:

    ensure_workspace_memory(project_path)
    conn = _connect(_workspace_db_path(project_path))
    try:
        hashes = _kv_get(conn, "workspace", "generated_hashes", {})
        hashes[relative_file] = content_hash
        _kv_set(conn, "workspace", "generated_hashes", hashes)
    finally:
        conn.close()


def get_effective_style(project_path: Path) -> str:

    ensure_user_memory()
    ensure_workspace_memory(project_path)

    uc = _connect(_user_db_path())
    wc = _connect(_workspace_db_path(project_path))
    try:
        wp = _kv_get(wc, "workspace", "preferences", {})
        up = _kv_get(uc, "user", "preferences", {})
    finally:
        uc.close()
        wc.close()

    return wp.get("communication_style") or up.get("communication_style") or "professional"


def get_memory_status(project_path: Path) -> dict:

    ensure_user_memory()
    ensure_workspace_memory(project_path)

    uc = _connect(_user_db_path())
    wc = _connect(_workspace_db_path(project_path))
    try:
        workspace_profile = _kv_get(wc, "workspace", "profile", {})
        workspace_prefs = _kv_get(wc, "workspace", "preferences", {})
        workspace_metadata = _kv_get(wc, "workspace", "metadata", {})
        user_profile = _kv_get(uc, "user", "profile", {})
        user_prefs = _kv_get(uc, "user", "preferences", {})
        workspace_history_count = int(wc.execute("SELECT COUNT(*) c FROM events").fetchone()["c"])
        user_history_count = int(uc.execute("SELECT COUNT(*) c FROM events").fetchone()["c"])
    finally:
        uc.close()
        wc.close()

    return {
        "project": str(project_path),
        "effective_style": get_effective_style(project_path),
        "workspace": {
            "root": str(_workspace_memory_root(project_path)),
            "profile": workspace_profile,
            "preferences": workspace_prefs,
            "history_count": workspace_history_count,
            "metadata": workspace_metadata,
        },
        "user": {
            "root": str(_user_root()),
            "profile": user_profile,
            "preferences": user_prefs,
            "history_count": user_history_count,
        },
    }


def get_history(project_path: Path, scope: str = "workspace", limit: int = 20) -> list[dict]:

    if scope == "user":
        ensure_user_memory()
        conn = _connect(_user_db_path())
    else:
        ensure_workspace_memory(project_path)
        conn = _connect(_workspace_db_path(project_path))

    try:
        rows = conn.execute(
            "SELECT timestamp, event_type, details, project_path FROM events ORDER BY id DESC LIMIT ?",
            (max(1, limit),),
        ).fetchall()
    finally:
        conn.close()

    return [
        {
            "timestamp": row["timestamp"],
            "event": row["event_type"],
            "details": row["details"],
            "project": row["project_path"],
        }
        for row in reversed(rows)
    ]


def save_observation(project_path: Path, title: str, content: str, observation_type: str = "note", tags: list[str] | None = None, scope: str = "workspace") -> int:

    tags = tags or []
    if scope == "user":
        ensure_user_memory()
        conn = _connect(_user_db_path())
    else:
        ensure_workspace_memory(project_path)
        conn = _connect(_workspace_db_path(project_path))

    try:
        cursor = conn.execute(
            "INSERT INTO observations(scope, project_path, title, content, observation_type, tags_json, created_at) VALUES(?, ?, ?, ?, ?, ?, ?)",
            (scope, str(project_path), title.strip(), content.strip(), observation_type.strip().lower() or "note", json.dumps(tags, ensure_ascii=True), _now_iso()),
        )
        conn.commit()
        return int(cursor.lastrowid)
    finally:
        conn.close()


def search_observations(project_path: Path, query: str, scope: str = "workspace", limit: int = 10) -> list[dict]:

    if scope == "user":
        ensure_user_memory()
        conn = _connect(_user_db_path())
    else:
        ensure_workspace_memory(project_path)
        conn = _connect(_workspace_db_path(project_path))

    try:
        q = f"%{query.strip().lower()}%"
        rows = conn.execute(
            "SELECT id, title, content, observation_type, tags_json, created_at, project_path FROM observations WHERE lower(title) LIKE ? OR lower(content) LIKE ? ORDER BY id DESC LIMIT ?",
            (q, q, max(1, limit)),
        ).fetchall()
    finally:
        conn.close()

    result = []
    for row in rows:
        try:
            tags = json.loads(row["tags_json"])
        except Exception:
            tags = []
        result.append(
            {
                "id": int(row["id"]),
                "title": row["title"],
                "content": row["content"],
                "type": row["observation_type"],
                "tags": tags,
                "created_at": row["created_at"],
                "project": row["project_path"],
            }
        )

    return result


def classify_supervisor_task(task: str) -> dict:

    text = task.strip().lower()

    workflow = "maintenance"
    specialists = ["Architect", "Backend Engineer", "QA Engineer", "Code Reviewer"]
    questions: list[str] = []

    if any(token in text for token in ["mercado pago", "mercadopago", "mp"]):
        workflow = "integration"
        specialists = ["Architect", "Backend Engineer", "Security Engineer", "QA Engineer", "Code Reviewer"]

        if any(token in text for token in ["checkout", "checkout pro", "wallet"]):
            workflow = "new-feature"
            specialists = ["Architect", "Backend Engineer", "QA Engineer", "Code Reviewer"]
        elif any(token in text for token in ["oauth", "auth", "autentic", "login", "cuenta admin"]):
            workflow = "integration"
        elif any(token in text for token in ["suscripcion", "subscription", "plans", "plan"]):
            workflow = "new-feature"
            specialists = ["Architect", "Backend Engineer", "Database Specialist", "QA Engineer", "Code Reviewer"]
        else:
            questions.append("¿Es checkout, OAuth o suscripciones?")

    elif any(token in text for token in ["bug", "error", "fix", "falla", "rompe"]):
        workflow = "bugfix"
        specialists = ["Backend Engineer", "QA Engineer", "Code Reviewer"]
    elif any(token in text for token in ["legacy", "zend", "antiguo", "viejo"]):
        workflow = "legacy"
        specialists = ["Architect", "Backend Engineer", "QA Engineer"]
    elif any(token in text for token in ["nuevo", "feature", "funcionalidad", "crear"]):
        workflow = "new-feature"
        specialists = ["Architect", "Backend Engineer", "Database Specialist", "QA Engineer"]
    elif any(token in text for token in ["refactor", "limpiar", "cleanup", "deuda"]):
        workflow = "refactor"
        specialists = ["Architect", "Backend Engineer", "Code Reviewer"]
    elif any(token in text for token in ["auditar", "audit", "seguridad", "performance"]):
        workflow = "audit"
        specialists = ["Architect", "DevOps Specialist", "Code Reviewer"]
    elif any(token in text for token in ["explicar", "explain", "entender", "comprender"]):
        workflow = "explain-code"
        specialists = ["Documentation Specialist", "Backend Engineer"]

    return {
        "workflow": workflow,
        "specialists": specialists,
        "questions": questions,
    }


def get_recent_context(project_path: Path, scope: str = "workspace", limit: int = 10) -> dict:

    return {
        "scope": scope,
        "events": get_history(project_path, scope=scope, limit=limit),
        "observations": search_observations(project_path, query="", scope=scope, limit=limit),
    }
