"""RAG retriever: searches pet care knowledge base for relevant documents."""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class RetrievalResult:
    """Represents a retrieved document with relevance score."""
    document_id: str
    title: str
    content: str
    relevance_score: float


class PetCareRetriever:
    """Retrieves relevant pet care information based on user queries."""

    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        """Load the knowledge base from file."""
        self.documents = []
        self.load_knowledge_base(knowledge_base_path)

    def load_knowledge_base(self, path: str) -> None:
        """Load documents from knowledge base JSON file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Knowledge base not found at {path}")

        with open(path, "r") as f:
            data = json.load(f)
            self.documents = data.get("documents", [])

    def _calculate_relevance(self, query: str, document: Dict) -> float:
        """Calculate relevance score based on keyword overlap (0.0 to 1.0)."""
        query_words = set(query.lower().split())
        doc_text = (document.get("title", "") + " " + document.get("content", "")).lower()
        doc_words = set(doc_text.split())

        # Remove common stop words
        stop_words = {"the", "a", "an", "and", "or", "is", "are", "in", "on", "at", "to", "for"}
        query_words -= stop_words

        if not query_words:
            return 0.0

        # Calculate overlap ratio
        overlap = len(query_words & doc_words)
        relevance = overlap / len(query_words)
        return min(relevance, 1.0)

    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """Retrieve top-k most relevant documents for a query."""
        if not query.strip():
            return []

        scored_docs = []
        for doc in self.documents:
            score = self._calculate_relevance(query, doc)
            if score > 0:
                scored_docs.append((doc, score))

        # Sort by relevance score (descending)
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        # Return top-k results
        results = []
        for doc, score in scored_docs[:top_k]:
            results.append(
                RetrievalResult(
                    document_id=doc["id"],
                    title=doc["title"],
                    content=doc["content"],
                    relevance_score=score
                )
            )

        return results

    def retrieve_by_category(self, species: str, category: str) -> List[RetrievalResult]:
        """Retrieve documents relevant to a specific pet species and task category."""
        query = f"{species} {category}"
        return self.retrieve(query, top_k=5)
