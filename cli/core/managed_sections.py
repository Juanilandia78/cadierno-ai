import re


_DELIMITER_STYLES = {
    "html": ("<!-- cadierno:managed:start:{key} -->", "<!-- cadierno:managed:end:{key} -->"),
    "hash": ("# cadierno:managed:start:{key}", "# cadierno:managed:end:{key}"),
}


def _delimiters(key: str, style: str) -> tuple[str, str]:

    try:
        start_template, end_template = _DELIMITER_STYLES[style]
    except KeyError:
        raise ValueError(f"Estilo de comentario desconocido: {style}") from None

    return start_template.format(key=key), end_template.format(key=key)


def _block_pattern(key: str, style: str) -> re.Pattern:

    start, end = _delimiters(key, style)
    return re.compile(f"{re.escape(start)}.*?{re.escape(end)}", re.DOTALL)


def render_managed_block(key: str, content: str, style: str = "html") -> str:

    start, end = _delimiters(key, style)
    body = content.strip("\n")
    return f"{start}\n{body}\n{end}"


def upsert_managed_section(existing_text: str, key: str, content: str, style: str = "html") -> str:
    """
    Reemplaza el contenido del bloque gestionado `key` dentro de `existing_text`,
    o lo agrega al final si no existe. Todo el resto del texto (incluido
    cualquier contenido manual del usuario) permanece exactamente igual.

    `style` controla la sintaxis de los delimitadores: "html" (comentarios
    `<!-- -->`, para Markdown) o "hash" (comentarios `#`, para .gitignore y
    similares).
    """

    block = render_managed_block(key, content, style)
    pattern = _block_pattern(key, style)

    if pattern.search(existing_text):
        return pattern.sub(lambda _match: block, existing_text, count=1)

    if not existing_text.strip():
        return block + "\n"

    trimmed = existing_text.rstrip("\n")
    return f"{trimmed}\n\n{block}\n"


def extract_managed_section(existing_text: str, key: str, style: str = "html") -> str | None:

    pattern = _block_pattern(key, style)
    match = pattern.search(existing_text)

    if not match:
        return None

    start, end = _delimiters(key, style)
    inner = match.group(0)[len(start):-len(end)]
    return inner.strip("\n")
