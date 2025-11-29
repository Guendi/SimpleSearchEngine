# 🔍 SimpleSearchEngine: Mini Text Search Engine

## 🌟 Project Overview

This repository contains a simple, educational implementation of a text **Search Engine** built in Python.

The core functionality revolves around the **Inverted Index**, a fundamental data structure used by professional search engines to efficiently process and retrieve documents based on keyword queries. 

This project serves as a practical demonstration of **Information Retrieval (IR)** concepts and the use of efficient data structures for large-scale text searching.

---

## ✨ Features

* **Inverted Index:** Manages a mapping from tokens (words) to the document IDs they appear in.
* **Document Management:** Methods to seamlessly add (`add_document`) and delete (`delete_document`) text documents.
* **Automatic Indexing:** The index is automatically updated whenever documents are modified or removed.
* **Boolean Search Logic:** The `search` method supports powerful querying:
    * **Implicit AND:** Multiple space-separated terms are treated as `AND` by default (e.g., `dog lazy`).
    * **Explicit AND/OR:** Supports the Boolean operators `AND` (Intersection) and `OR` (Union) in queries (e.g., `fox AND quick`, `cat OR bird`).
* **Tokenization:** Basic text preprocessing is performed (lowercasing, punctuation removal) for clean indexing.

---

## 🛠️ Technology

* **Language:** Python 3.x
* **Key Data Structures:** `dict` (for the Inverted Index and Document Store) and `set` (for fast Boolean set operations).

---

## 📦 Setup and Usage

### Installation

No specific installation is required beyond a Python 3 environment.

### Running the Example

The main script includes an `if __name__ == "__main__":` block that demonstrates the functionality by adding sample documents and allowing for an interactive search.

To run the interactive demo:

```bash
python search_engine.py