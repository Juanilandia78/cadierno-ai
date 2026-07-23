import re


_START_TEMPLATE = "<!-- cadierno:managed:start:{key} -->"
_END_TEMPLATE = "<!-- cadierno:managed:end:{key} -->"


def _block_pattern(key: str) -> re.Pattern:

    start = re.escape(_START_TEMPLATE.format(key=key))
    end = re.escape(_END_TEMPLATE.format(key=key))
    return re.compile(f"{start}.*?{end}", re.DOTALL)


def render_managed_block(key: str, content: str) -> str:

    start = _START_TEMPLATE.format(key=key)
    end = _END_TEMPLATE.format(key=key)
    body = content.strip("\n")
    return f"{start}\n{body}\n{end}"


def upsert_managed_section(existing_text: str, key: str, content: str) -> str:
    """
    Reemplaza el contenido del bloque gestionado `key` dentro de `existing_text`,
    o lo agrega al final si no existe. Todo el resto del texto (incluido
    cualquier contenido manual del usuario) permanece exactamente igual.
    """

    block = render_managed_block(key, content)
    pattern = _block_pattern(key)

    if pattern.search(existing_text):
        return pattern.sub(lambda _match: block, existing_text, count=1)

    if not existing_text.strip():
        return block + "\n"

    trimmed = existing_text.rstrip("\n")
    return f"{trimmed}\n\n{block}\n"


def extract_managed_section(existing_text: str, key: str) -> str | None:

    pattern = _block_pattern(key)
    match = pattern.search(existing_text)

    if not match:
        return None

    start = _START_TEMPLATE.format(key=key)
    end = _END_TEMPLATE.format(key=key)
    inner = match.group(0)[len(start):-len(end)]
    return inner.strip("\n")
