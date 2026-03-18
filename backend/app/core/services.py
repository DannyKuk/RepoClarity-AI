from app.rag.embedder import Embedder
from app.rag.chunker import Chunker
from app.rag.retriever import Retriever
from app.rag.query_engine import QueryEngine
from app.rag.indexing_service import IndexingService
from app.rag.repo_summary import RepoSummarizer
from app.rag.vector_store import VectorStore

from app.repo.scanner import RepositoryScanner
from app.repo.framework_detector import detect_framework
from app.repo.file_prioritizer import get_file_weight
from app.repo.entrypoint_detector import EntrypointDetector
from app.repo.repo_registry import RepoRegistry

from app.llm.ollama_client import OllamaClient


class Services:
    def __init__(self):
        # --- core ---
        self.embedder = Embedder()
        self.chunker = Chunker()
        self.scanner = RepositoryScanner()
        self.registry = RepoRegistry()
        self.entrypoint_detector = EntrypointDetector()

        # --- llm ---
        self.llm = OllamaClient()

        # --- rag ---
        self.retriever = Retriever(self.embedder)

        self.repo_summarizer = RepoSummarizer(self.llm)

        self.vector_store_cls = VectorStore

        self.indexing_service = IndexingService(
            scanner=self.scanner.scan,
            chunker=self.chunker.chunk_file,
            embedder=self.embedder,
            vector_store_cls=self.vector_store_cls,
            repo_summary=self.repo_summarizer,
            framework_detector=detect_framework,
            file_prioritizer=get_file_weight,
            entrypoint_detector=self.entrypoint_detector.detect
        )

        self.query_engine = QueryEngine(
            retriever=self.retriever,
            llm=self.llm,
        )
