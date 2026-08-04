"""RAG retriever: searches pet care knowledge base for relevant documents.

Supports two modes:
1. Heuristic mode (keyword-based) - fast, no API needed
2. Groq API mode (semantic) - uses LLM for intelligent retrieval
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables for Groq API key
load_dotenv()

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


class GroqEnhancedRetriever(PetCareRetriever):
    """Uses Groq API to intelligently select relevant documents.

    Falls back to heuristic retrieval if API key is missing or API fails.
    """

    def __init__(self, knowledge_base_path: str = "knowledge_base.json", use_api: bool = True):
        """Initialize with knowledge base and optional Groq API."""
        super().__init__(knowledge_base_path)
        self.use_api = use_api and self._has_api_key()
        self.api_key = os.getenv("GROQ_API_KEY")

    def _has_api_key(self) -> bool:
        """Check if Groq API key is available."""
        key = os.getenv("GROQ_API_KEY")
        return key and key != "your_key_here"

    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """Retrieve documents using Groq API or fallback to heuristic."""
        if self.use_api:
            try:
                return self._retrieve_with_groq(query, top_k)
            except Exception as e:
                # Fallback to heuristic if API fails
                print(f"Groq API failed ({str(e)}), falling back to heuristic retrieval")
                return super().retrieve(query, top_k)
        else:
            return super().retrieve(query, top_k)

    def _retrieve_with_groq(self, query: str, top_k: int) -> List[RetrievalResult]:
        """Use Groq API to semantically rank documents."""
        try:
            from groq import Groq
        except ImportError:
            raise ImportError("groq package not installed. Run: pip install groq")

        client = Groq(api_key=self.api_key)

        # Create document index for the API
        doc_list = "\n".join([
            f"{i+1}. [{doc['title']}] {doc['content'][:200]}..."
            for i, doc in enumerate(self.documents)
        ])

        # Use Groq to rank documents
        prompt = f"""You are a pet care expert. Given this query and documents,
select the {min(top_k, len(self.documents))} MOST relevant documents.

Query: {query}

Documents:
{doc_list}

Return ONLY the document numbers (1-indexed) as a comma-separated list, in order of relevance.
Example: 2,5,1

Numbers only, no explanation."""

        response = client.messages.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )

        # Parse response
        try:
            ranks = response.content[0].text.strip()
            indices = [int(x.strip()) - 1 for x in ranks.split(",")]
        except (ValueError, IndexError):
            # Fallback if parsing fails
            return super().retrieve(query, top_k)

        # Return selected documents in ranked order
        results = []
        for idx in indices:
            if 0 <= idx < len(self.documents):
                doc = self.documents[idx]
                # Recalculate heuristic score for consistency
                score = self._calculate_relevance(query, doc)
                results.append(
                    RetrievalResult(
                        document_id=doc["id"],
                        title=doc["title"],
                        content=doc["content"],
                        relevance_score=score
                    )
                )

        return results[:top_k]

    def get_mode(self) -> str:
        """Return current retrieval mode."""
        return "Groq API (with heuristic fallback)" if self.use_api else "Heuristic only"
