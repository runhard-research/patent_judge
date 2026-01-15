import re

HEADER_PAT = re.compile(r"(.+?)(について|に関する)")
BODY_TRIGGERS = ["を有する", "を備える", "を含み", "からなり"]
TAIL_PAT = re.compile(r"(装置|システム|方法|プログラム|ハード).*$")

def chunk_claim(text: str):
    chunks = []
    idx = 0

    # HEADER
    m = HEADER_PAT.search(text)
    if m:
        chunks.append({
            "type": "HEADER",
            "text": m.group(0),
            "index": idx
        })
        idx += 1
        rest = text[m.end():]
    else:
        rest = text

    # BODY
    body_parts = [rest]
    for t in BODY_TRIGGERS:
        body_parts = sum([p.split(t) for p in body_parts], [])

    for p in body_parts[:-1]:
        p = p.strip()
        if p:
            chunks.append({
                "type": "BODY",
                "text": p,
                "index": idx
            })
            idx += 1

    # TAIL
    m2 = TAIL_PAT.search(text)
    if m2:
        chunks.append({
            "type": "TAIL",
            "text": m2.group(0),
            "index": idx
        })

    return chunks

