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

    chunks = chunk_text(file_dict["content"])

    return [
        {
            "content": chunk,
            "path": file_dict["path"]
        }
        for chunk in chunks
    ]
