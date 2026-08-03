"""Integration layer: combines RAG retriever and validator with scheduling."""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from src.ai.retriever import PetCareRetriever, RetrievalResult
from src.ai.validator import RecommendationValidator, ValidationResult
from pawpal_system import Task, PlannedItem


@dataclass
class EnhancedPlannedItem:
    """PlannedItem enriched with RAG retrieval and validation results."""
    planned_item: PlannedItem
    retrieval_results: List[RetrievalResult] = field(default_factory=list)
    validation_result: Optional[ValidationResult] = None

    def get_recommendation_with_context(self) -> str:
        """Generate a recommendation with retrieved context."""
        task = self.planned_item.task
        pet_name = self.planned_item.pet_name

        base = f"{task.title} for {pet_name}"

        if self.retrieval_results:
            doc = self.retrieval_results[0]
            return f"{base}\n  📚 Reference: {doc.title}\n  Details: {doc.content[:150]}..."

        return base

    def get_validation_summary(self) -> str:
        """Get validation result as a string."""
        if not self.validation_result:
            return "✓ No validation needed"

        result = self.validation_result
        status = "✓" if result.is_valid else "⚠"
        return f"{status} {result.explanation}"


class AISchedulingIntegrator:
    """Integrates RAG and validation into the scheduling workflow."""

    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        """Initialize retriever and validator."""
        self.retriever = PetCareRetriever(knowledge_base_path)
        self.validator = RecommendationValidator()
        self.metrics = {
            "total_items": 0,
            "items_validated": 0,
            "valid_items": 0,
            "avg_confidence": 0.0,
            "avg_retrieval_score": 0.0,
        }

    def enhance_plan(
        self,
        plan: List[PlannedItem],
        pet_species_map: Dict[str, str]
    ) -> List[EnhancedPlannedItem]:
        """Enhance a daily plan with RAG retrieval and validation."""
        enhanced_plan = []

        for item in plan:
            # Retrieve relevant documentation
            retrieval_results = self.retriever.retrieve_by_category(
                pet_species_map.get(item.pet_name, "dog"),
                item.task.category
            )

            # Validate recommendation
            supporting_docs = [r.content for r in retrieval_results]
            validation_result = self.validator.validate_recommendation(
                recommendation=f"{item.task.title}: {item.reason}",
                pet_species=pet_species_map.get(item.pet_name, "dog"),
                task_category=item.task.category,
                supporting_docs=supporting_docs
            )

            enhanced_item = EnhancedPlannedItem(
                planned_item=item,
                retrieval_results=retrieval_results,
                validation_result=validation_result
            )

            enhanced_plan.append(enhanced_item)

            # Update metrics
            self.metrics["total_items"] += 1
            self.metrics["items_validated"] += 1
            if validation_result.is_valid:
                self.metrics["valid_items"] += 1
            if retrieval_results:
                self.metrics["avg_retrieval_score"] = (
                    self.metrics["avg_retrieval_score"] * (len(enhanced_plan) - 1) +
                    retrieval_results[0].relevance_score
                ) / len(enhanced_plan)

        # Update average confidence
        if self.metrics["items_validated"] > 0:
            total_confidence = sum(
                item.validation_result.confidence_score
                for item in enhanced_plan
                if item.validation_result
            )
            self.metrics["avg_confidence"] = (
                total_confidence / self.metrics["items_validated"]
            )

        return enhanced_plan

    def get_metrics(self) -> Dict:
        """Get system reliability metrics."""
        metrics = self.metrics.copy()
        if metrics["total_items"] > 0:
            metrics["validation_success_rate"] = (
                metrics["valid_items"] / metrics["items_validated"]
                if metrics["items_validated"] > 0
                else 0.0
            )
        return metrics

    def log_interaction(self, user_input: str, plan: List[EnhancedPlannedItem]) -> Dict:
        """Log an AI interaction for debugging and evaluation."""
        return {
            "user_input": user_input,
            "items_recommended": len(plan),
            "items_valid": sum(1 for item in plan if item.validation_result and item.validation_result.is_valid),
            "avg_confidence": self.metrics.get("avg_confidence", 0.0),
            "avg_retrieval_score": self.metrics.get("avg_retrieval_score", 0.0),
        }
