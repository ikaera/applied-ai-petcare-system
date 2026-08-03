"""AI Layer: RAG retriever, validation, and planning."""

from .retriever import PetCareRetriever, RetrievalResult
from .validator import RecommendationValidator, ValidationResult

__all__ = [
    "PetCareRetriever",
    "RetrievalResult",
    "RecommendationValidator",
    "ValidationResult",
]
