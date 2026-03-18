from app.core.services import Services


def test_services_wiring():
    s = Services()

    # core components exist
    assert s.embedder is not None
    assert s.chunker is not None
    assert s.scanner is not None

    # indexing service wiring
    assert s.indexing_service.embedder is s.embedder
    assert s.indexing_service.chunker == s.chunker.chunk_file
    assert s.indexing_service.scanner == s.scanner.scan

    # query engine wiring
    assert s.query_engine.retriever is s.retriever
    assert s.query_engine.llm is s.llm
