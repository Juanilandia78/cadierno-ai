#!/usr/bin/env python3

import argparse

from commands.install import install
from commands.bootstrap import bootstrap
from commands.update import update
from commands.doctor import doctor
from commands.uninstall import uninstall
from commands.memory import (
    assist,
    memory_context,
    memory_history,
    memory_init,
    memory_save,
    memory_search,
    memory_set_profile,
    memory_set_style,
    memory_status,
)

VERSION = "0.2.2"


def main():
    parser = argparse.ArgumentParser(
        prog="cadierno",
        description="Cadierno AI CLI"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"Cadierno AI {VERSION}"
    )

    sub = parser.add_subparsers(dest="command")

    # install
    install_parser = sub.add_parser(
        "install",
        help="Instala Cadierno AI en un proyecto"
    )

    install_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Ruta del proyecto"
    )

    # bootstrap
    bootstrap_parser = sub.add_parser(
        "bootstrap",
        help="Analiza un proyecto"
    )

    bootstrap_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Ruta del proyecto"
    )

    # doctor
    sub.add_parser(
        "doctor",
        help="Diagnostica Cadierno AI"
    )

    # update
    update_parser = sub.add_parser(
        "update",
        help="Actualiza Cadierno AI"
    )

    update_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Ruta del proyecto"
    )

    # uninstall
    uninstall_parser = sub.add_parser(
        "uninstall",
        help="Desinstala Cadierno AI de un proyecto"
    )

    uninstall_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Ruta del proyecto"
    )

    uninstall_parser.add_argument(
        "--purge",
        action="store_true",
        help="Elimina también knowledge/ y memory/"
    )

    # memory
    memory_parser = sub.add_parser(
        "memory",
        help="Gestiona memoria persistente (usuario/workspace/perfil/historial)"
    )

    memory_sub = memory_parser.add_subparsers(dest="memory_command")

    memory_init_parser = memory_sub.add_parser(
        "init",
        help="Inicializa memoria de usuario y workspace"
    )
    memory_init_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")

    memory_status_parser = memory_sub.add_parser(
        "status",
        help="Muestra estado de memoria"
    )
    memory_status_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")

    memory_style_parser = memory_sub.add_parser(
        "style",
        help="Configura estilo de comunicación"
    )
    memory_style_parser.add_argument("style", help="argentino o professional")
    memory_style_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")
    memory_style_parser.add_argument(
        "--scope",
        choices=["workspace", "user"],
        default="workspace",
        help="Alcance de la preferencia"
    )

    memory_profile_parser = memory_sub.add_parser(
        "profile",
        help="Actualiza perfil de desarrollador"
    )
    memory_profile_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")
    memory_profile_parser.add_argument("--name", help="Nombre")
    memory_profile_parser.add_argument("--role", help="Rol")
    memory_profile_parser.add_argument("--seniority", help="Seniority")
    memory_profile_parser.add_argument(
        "--scope",
        choices=["workspace", "user"],
        default="workspace",
        help="Alcance del perfil"
    )

    memory_history_parser = memory_sub.add_parser(
        "history",
        help="Muestra historial de eventos"
    )
    memory_history_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")
    memory_history_parser.add_argument(
        "--scope",
        choices=["workspace", "user"],
        default="workspace",
        help="Alcance del historial"
    )
    memory_history_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Cantidad de eventos a mostrar"
    )

    memory_save_parser = memory_sub.add_parser(
        "save",
        help="Guarda una observación manual en memoria"
    )
    memory_save_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")
    memory_save_parser.add_argument("--title", required=True, help="Título de la observación")
    memory_save_parser.add_argument("--content", required=True, help="Contenido de la observación")
    memory_save_parser.add_argument("--type", default="note", help="Tipo (note, decision, bugfix, etc.)")
    memory_save_parser.add_argument("--tags", help="Tags separados por coma")
    memory_save_parser.add_argument(
        "--scope",
        choices=["workspace", "user"],
        default="workspace",
        help="Alcance de la observación"
    )

    memory_search_parser = memory_sub.add_parser(
        "search",
        help="Busca observaciones en memoria"
    )
    memory_search_parser.add_argument("query", help="Texto a buscar")
    memory_search_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")
    memory_search_parser.add_argument(
        "--scope",
        choices=["workspace", "user"],
        default="workspace",
        help="Alcance de búsqueda"
    )
    memory_search_parser.add_argument("--limit", type=int, default=10, help="Cantidad máxima")

    memory_context_parser = memory_sub.add_parser(
        "context",
        help="Muestra contexto reciente (eventos + observaciones)"
    )
    memory_context_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")
    memory_context_parser.add_argument(
        "--scope",
        choices=["workspace", "user"],
        default="workspace",
        help="Alcance de contexto"
    )
    memory_context_parser.add_argument("--limit", type=int, default=10, help="Cantidad máxima")

    assist_parser = sub.add_parser(
        "assist",
        help="Sugiere workflow y specialists para una tarea"
    )
    assist_parser.add_argument("task", help="Descripción de la tarea")
    assist_parser.add_argument("path", nargs="?", default=".", help="Ruta del proyecto")

    args = parser.parse_args()

    if args.command == "install":
        install(args.path)

    elif args.command == "bootstrap":
        bootstrap(args.path)

    elif args.command == "doctor":
        doctor()

    elif args.command == "update":
        update(args.path)

    elif args.command == "uninstall":
        uninstall(args.path, args.purge)

    elif args.command == "memory":
        if args.memory_command == "init":
            memory_init(args.path)
        elif args.memory_command == "status":
            memory_status(args.path)
        elif args.memory_command == "style":
            memory_set_style(args.path, args.style, args.scope)
        elif args.memory_command == "profile":
            memory_set_profile(args.path, args.name, args.role, args.seniority, args.scope)
        elif args.memory_command == "history":
            memory_history(args.path, args.scope, args.limit)
        elif args.memory_command == "save":
            memory_save(args.path, args.title, args.content, args.type, args.tags, args.scope)
        elif args.memory_command == "search":
            memory_search(args.path, args.query, args.scope, args.limit)
        elif args.memory_command == "context":
            memory_context(args.path, args.scope, args.limit)
        else:
            memory_parser.print_help()

    elif args.command == "assist":
        assist(args.path, args.task)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()