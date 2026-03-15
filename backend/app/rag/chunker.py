def chunk_text(text: str, chunk_size: int = 800, overlap: int = 200):
    """
    Split text into overlapping chunks.

    Args:
        text: input text
        chunk_size: max characters per chunk
        overlap: overlap between chunks

    Returns:
        list[str]
    """

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def chunk_file(file_dict):

    path = file_dict["path"].lower()
    chunks = chunk_text(file_dict["content"])

    chunk_objects = [
        {
            "content": chunk,
            "path": file_dict["path"]
        }
        for chunk in chunks
    ]

    weight = 1

    if "readme" in path:
        weight = 4

    elif path.endswith("package.json"):
        weight = 3

    elif "config" in path:
        weight = 3

    elif "main" in path or "app" in path:
        weight = 3

    elif "/pages/" in path or "/components/" in path:
        weight = 2

    return chunk_objects * weight
