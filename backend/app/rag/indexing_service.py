class IndexingService:
    def __init__(
            self,
            scanner,
            chunker,
            embedder,
            vector_store_cls,
            repo_summary,
            framework_detector,
            file_prioritizer,
            entrypoint_detector,
    ):
        self.scanner = scanner
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store_cls = vector_store_cls
        self.repo_summary = repo_summary
        self.framework_detector = framework_detector
        self.file_prioritizer = file_prioritizer
        self.entrypoint_detector = entrypoint_detector

    def build_index(self, repo_path: str):
        print("Scanning repository...")
        files = self.scanner(repo_path)
        print(f"Files found: {len(files)}")

        if not files:
            raise RuntimeError("No files found to index.")

        framework = self.framework_detector(repo_path)
        print(f"Detected framework: {framework}")

        entrypoints = self.entrypoint_detector(repo_path, framework)
        print(f"Detected entrypoints: {entrypoints}")

        print("Generating repository summary...")
        summary = self.repo_summary.summarize(files)

        print("Chunking files...")
        chunks = []

        for file in files:
            file_chunks = self.chunker(file)

            weight = self.file_prioritizer(file["path"], framework)

            if file_chunks:
                chunks.extend(file_chunks * weight)

        print(f"Chunks generated: {len(chunks)}")

        if not chunks:
            raise RuntimeError("No chunks generated. Scanner may be filtering too aggressively.")

        chunks = [c for c in chunks if c["content"].strip()]
        texts = [chunk["content"] for chunk in chunks]

        print("Generating embeddings...")
        embeddings = self.embedder.embed(texts)

        print("Building vector store...")
        vector_store = self.vector_store_cls(self.embedder.dimension())

        vector_store.framework = framework
        vector_store.entrypoints = entrypoints
        vector_store.summary = summary

        vector_store.add(embeddings, chunks)

        print("Index built successfully.")

        return vector_store
