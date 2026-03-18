class Chunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 200):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str):
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)
        step = self.chunk_size - self.overlap

        while start < text_length:
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += step

        return chunks

    def chunk_file(self, file_dict):
        chunks = self.chunk_text(file_dict["content"])

        return [
            {
                "content": chunk,
                "path": file_dict["path"],
            }
            for chunk in chunks
        ]
