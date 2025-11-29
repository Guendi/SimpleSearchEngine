import re
# Typing imports for better readability
from typing import Dict, Set, List, Optional


class SimpleSearchEngine:
    """
    A simplified search engine that uses an Inverted Index.
    """
    # Constructor

    def __init__(self):
        # Document storage: doc_id -> document text
        self.documents: Dict[int, str] = {}
        # Inverted Index: word -> Set of doc_ids
        self.inverted_index: Dict[str, Set[int]] = {}
        # Counter for the next document ID (optional, if IDs are not managed externally)
        self.next_doc_id: int = 0

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the text: removes punctuation, converts to lowercase, and splits.
        """
        # Removes punctuation and keeps only letters and spaces
        text = re.sub(r'[^a-z\s]', '', text.lower())
        return text.split()

    def add_document(self, text: str, doc_id: Optional[int] = None) -> int:
        """
        Adds a document and updates the Inverted Index.
        Returns the used document ID.
        """

        if doc_id is None:
            doc_id = self.next_doc_id
            self.next_doc_id += 1

        if doc_id in self.documents:
            print(
                f"WARNING: Document with ID {doc_id} already exists. Deleting and re-adding.")
            self.delete_document(doc_id)

        self.documents[doc_id] = text
        # Use a Set for unique words per document
        tokens = set(self._tokenize(text))

        for token in tokens:
            if token not in self.inverted_index:
                self.inverted_index[token] = set()
            self.inverted_index[token].add(doc_id)

        print(f"Document {doc_id} added/updated.")
        return doc_id

    def delete_document(self, doc_id: int) -> bool:
        """
        Deletes a document and removes it from the Inverted Index.
        """
        if doc_id not in self.documents:
            return False

        text = self.documents.pop(doc_id)
        tokens = set(self._tokenize(text))

        for token in tokens:
            if token in self.inverted_index:
                self.inverted_index[token].discard(doc_id)
                # Remove word from index if no documents remain
                if not self.inverted_index[token]:
                    del self.inverted_index[token]

        print(f"Document {doc_id} deleted.")
        return True

    def search(self, query: str) -> Dict[int, str]:
        """
        Searches for documents based on the query (supports AND/OR).
        Returns a map from doc_id to document text.
        """
        query = query.strip().upper()

        if " AND " in query:
            operator = "AND"
            terms = [term.strip().lower() for term in query.split(" AND ")]
        elif " OR " in query:
            operator = "OR"
            terms = [term.strip().lower() for term in query.split(" OR ")]
        else:
            # Default to AND for all space-separated terms
            operator = "AND"
            terms = self._tokenize(query)

        if not terms:
            return {}

        # Initialize the result set with the documents of the first term
        first_term = terms[0]
        result_set: Set[int] = self.inverted_index.get(
            first_term, set()).copy()

        # Perform the set operations based on the operator
        if operator == "AND":
            # Intersection: Documents must contain ALL terms
            for term in terms[1:]:
                doc_ids = self.inverted_index.get(term, set())
                result_set.intersection_update(doc_ids)
        elif operator == "OR":
            # Union: Documents must contain AT LEAST ONE term
            for term in terms[1:]:
                doc_ids = self.inverted_index.get(term, set())
                result_set.update(doc_ids)

        # Collect the found documents
        found_documents: Dict[int, str] = {
            doc_id: self.documents[doc_id]
            for doc_id in result_set
            if doc_id in self.documents
        }

        return found_documents

    def display_index(self):
        """Displays the current Inverted Index."""
        print("\n--- Inverted Index ---")
        for word, doc_ids in sorted(self.inverted_index.items()):
            print(f"'{word}': {sorted(list(doc_ids))}")
        print("----------------------\n")

    def display_documents(self):
        """Displays all stored documents."""
        print("\n--- Document Store ---")
        for doc_id, text in sorted(self.documents.items()):
            print(f"ID {doc_id}: '{text}'")
        print("--------------------------\n")


# --- Example Usage ---
# --- Start Block
if __name__ == "__main__":

    engine = SimpleSearchEngine()

    # 1. Add documents
    doc1_id = engine.add_document(
        "The quick brown fox jumps over the lazy dog.", doc_id=1)
    doc2_id = engine.add_document(
        "A dog and a cat play together in the garden.", doc_id=2)
    doc3_id = engine.add_document(
        "The fox is having a lazy day, but the cat is awake.", doc_id=3)
    doc4_id = engine.add_document(
        "The IPSO school only becomes interesting after the third year.", 4)

    engine.display_documents()
    engine.display_index()

    # --- Test Cases
    # 2. Search queries (Default: implicit AND)
    print("--- Search: 'fox lazy' (Implicit AND) ---")
    results_and = engine.search("fox lazy")
    for doc_id, text in results_and.items():
        print(f"FOUND (AND): ID {doc_id}: {text}")

    print("\n--- Search: 'dog OR cat' (Explicit OR) ---")
    results_or = engine.search("dog OR cat")
    for doc_id, text in results_or.items():
        print(f"FOUND (OR): ID {doc_id}: {text}")

    print("\n--- Search: 'dog AND cat' (Explicit AND) ---")
    results_explicit_and = engine.search("dog AND cat")
    for doc_id, text in results_explicit_and.items():
        print(f"FOUND (Explicit AND): ID {doc_id}: {text}")

    # --- 3. Delete document and check index update
    print("\n*** Deleting Document 1 ***")
    engine.delete_document(doc1_id)
    engine.display_index()

    # --- 4. Search again for deleted document
    print("\n--- Search for 'quick' after deletion ---")
    results_after_delete = engine.search("quick")
    if not results_after_delete:
        print("FOUND: No documents (Correct, because 'quick' was only in Doc 1).")
