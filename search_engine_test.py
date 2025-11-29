# Import the class to be tested
from search_engine import SimpleSearchEngine


def test_add_document_updates_index():
    # 1. Arrange (Setup)
    engine = SimpleSearchEngine()
    text = "Hello World"

    # 2. Act (Execution)
    doc_id = engine.add_document(text, doc_id=5)

    # 3. Assert (Verification)
    assert doc_id == 5
    assert 'hello' in engine.inverted_index
    assert 5 in engine.inverted_index['hello']


def test_and_search_logic():
    # 1. Arrange (Setup)
    engine = SimpleSearchEngine()
    engine.add_document("Dog and Cat are playing.", doc_id=1)
    engine.add_document("Only the dog is barking.", doc_id=2)

    # 2. Act (Execution)
    results = engine.search("Dog AND Cat")

    # 3. Assert (Verification)
    # Only document 1 should be found.
    assert len(results) == 1
    assert 1 in results
    assert 2 not in results


def test_or_search_logic():
    # 1. Arrange (Setup)
    engine = SimpleSearchEngine()
    engine.add_document("Dog", doc_id=1)
    engine.add_document("Cat", doc_id=2)
    engine.add_document("Bird", doc_id=3)

    # 2. Act (Execution)
    results = engine.search("Dog OR Cat")

    # 3. Assert (Verification)
    # Documents 1 and 2 should be found.
    assert len(results) == 2
    assert 1 in results
    assert 2 in results
    assert 3 not in results