#!/usr/bin/env python3

"""
Cadierno Memory MCP-like server (stdio JSON-RPC).

Methods:
- mem_save
- mem_search
- mem_context
- mem_status
"""

from pathlib import Path
import json
import sys

from core.memory import (
    get_memory_status,
    get_recent_context,
    save_observation,
    search_observations,
)


def _result(request_id, payload):
    return {"jsonrpc": "2.0", "id": request_id, "result": payload}


def _error(request_id, code, message):
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _handle(method: str, params: dict):

    project = Path(params.get("project_path", ".")).resolve()

    if method == "mem_save":
        obs_id = save_observation(
            project,
            title=params.get("title", "Sin título"),
            content=params.get("content", ""),
            observation_type=params.get("type", "note"),
            tags=params.get("tags", []),
            scope=params.get("scope", "workspace"),
        )
        return {"id": obs_id}

    if method == "mem_search":
        return {
            "items": search_observations(
                project,
                query=params.get("query", ""),
                scope=params.get("scope", "workspace"),
                limit=int(params.get("limit", 10)),
            )
        }

    if method == "mem_context":
        return get_recent_context(
            project,
            scope=params.get("scope", "workspace"),
            limit=int(params.get("limit", 10)),
        )

    if method == "mem_status":
        return get_memory_status(project)

    raise ValueError(f"Método no soportado: {method}")


def main():

    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue

        try:
            message = json.loads(raw)
            request_id = message.get("id")
            method = message.get("method")
            params = message.get("params", {})

            if not method:
                response = _error(request_id, -32600, "Request inválido")
            else:
                payload = _handle(method, params)
                response = _result(request_id, payload)

        except Exception as exc:
            request_id = None
            try:
                parsed = json.loads(raw)
                request_id = parsed.get("id")
            except Exception:
                pass
            response = _error(request_id, -32000, str(exc))

        sys.stdout.write(json.dumps(response, ensure_ascii=True) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
