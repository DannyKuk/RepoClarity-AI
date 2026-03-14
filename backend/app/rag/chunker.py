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
    """
    Convert a scanned file into chunks with metadata.
    """

    path = file_dict["path"].lower()

    chunks = chunk_text(file_dict["content"])

    chunk_objects = [
        {
            "content": chunk,
            "path": file_dict["path"]
        }
        for chunk in chunks
    ]

    # Prioritize README files by duplicating their chunks
    if "readme" in path or path.endswith(".md"):
        chunk_objects = chunk_objects * 3

    return chunk_objects