"""Validation layer: checks AI recommendations for safety and completeness."""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ValidationIssue(Enum):
    """Types of validation issues."""
    MISSING_CONTEXT = "missing_context"
    UNSAFE_RECOMMENDATION = "unsafe_recommendation"
    INSUFFICIENT_INFO = "insufficient_info"
    CONFLICTING_INFO = "conflicting_info"


@dataclass
class ValidationResult:
    """Result of validating a recommendation."""
    is_valid: bool
    confidence_score: float  # 0.0 to 1.0
    issues: List[ValidationIssue]
    explanation: str
    recommendations: List[str]


class RecommendationValidator:
    """Validates AI recommendations for safety and reliability."""

    MEDICAL_KEYWORDS = {
        "medication", "medicine", "drug", "pain", "illness", "disease",
        "sick", "infected", "antibiotics", "prescription", "vet", "doctor"
    }

    SAFE_TASKS = {"walking", "play", "feeding", "grooming", "enrichment", "exercise"}
    POTENTIALLY_UNSAFE = {"medication", "medical", "injury", "emergency"}

    def validate_recommendation(
        self,
        recommendation: str,
        pet_species: str,
        task_category: str,
        supporting_docs: List[str] = None
    ) -> ValidationResult:
        """Validate a task recommendation against safety and completeness criteria."""
        issues = []
        confidence = 1.0

        # Check 1: Does recommendation address medical concerns?
        if any(keyword in recommendation.lower() for keyword in self.MEDICAL_KEYWORDS):
            if not supporting_docs or len(supporting_docs) == 0:
                issues.append(ValidationIssue.MISSING_CONTEXT)
                confidence -= 0.3
            elif not any("vet" in doc.lower() or "veterinarian" in doc.lower() for doc in supporting_docs):
                issues.append(ValidationIssue.INSUFFICIENT_INFO)
                confidence -= 0.2

        # Check 2: Is the recommendation safe for the pet species?
        if not self._is_species_appropriate(recommendation, pet_species):
            issues.append(ValidationIssue.UNSAFE_RECOMMENDATION)
            confidence -= 0.4

        # Check 3: Does recommendation match task category?
        if not self._matches_category(recommendation, task_category):
            issues.append(ValidationIssue.CONFLICTING_INFO)
            confidence -= 0.15

        # Check 4: Is there sufficient detail?
        if len(recommendation.split()) < 5:
            issues.append(ValidationIssue.INSUFFICIENT_INFO)
            confidence -= 0.1

        confidence = max(0.0, min(1.0, confidence))
        is_valid = len(issues) == 0 and confidence >= 0.5

        explanation = self._generate_explanation(is_valid, issues, confidence)
        recommendations = self._generate_recommendations(issues)

        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence,
            issues=issues,
            explanation=explanation,
            recommendations=recommendations
        )

    def _is_species_appropriate(self, recommendation: str, species: str) -> bool:
        """Check if recommendation is appropriate for the pet species."""
        rec_lower = recommendation.lower()
        species_lower = species.lower()

        # Dogs and cats have different care needs
        dog_specific = {"fetch", "walk", "leash", "bark", "pack"}
        cat_specific = {"litter", "climbing", "scratching", "climbing tree"}

        if species_lower.startswith("dog"):
            unsafe_terms = {"toxic to dogs", "dogs cannot", "never give dogs"}
            return not any(term in rec_lower for term in unsafe_terms)
        elif species_lower.startswith("cat"):
            unsafe_terms = {"toxic to cats", "cats cannot", "never give cats"}
            return not any(term in rec_lower for term in unsafe_terms)

        return True

    def _matches_category(self, recommendation: str, category: str) -> bool:
        """Check if recommendation aligns with task category."""
        category_lower = category.lower()
        rec_lower = recommendation.lower()

        category_keywords = {
            "walk": {"walk", "exercise", "outside", "movement"},
            "feeding": {"feed", "food", "meal", "eat", "eating"},
            "meds": {"medication", "medicine", "pill", "dose"},
            "grooming": {"groom", "brush", "bathe", "nail", "clean"},
            "enrichment": {"play", "toy", "puzzle", "engage", "stimulate"}
        }

        if category_lower in category_keywords:
            keywords = category_keywords[category_lower]
            return any(kw in rec_lower for kw in keywords)

        return True

    def _generate_explanation(self, is_valid: bool, issues: List[ValidationIssue], confidence: float) -> str:
        """Generate human-readable explanation of validation result."""
        if is_valid:
            return f"✓ Recommendation passed validation (confidence: {confidence:.1%})"

        issue_names = [issue.value.replace("_", " ") for issue in issues]
        return f"⚠ Recommendation needs review: {', '.join(issue_names)} (confidence: {confidence:.1%})"

    def _generate_recommendations(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate suggestions to improve recommendation."""
        suggestions = []

        if ValidationIssue.MISSING_CONTEXT in issues:
            suggestions.append("Add reference to supporting pet care documentation")

        if ValidationIssue.UNSAFE_RECOMMENDATION in issues:
            suggestions.append("Review for pet species safety. Consult veterinary resources.")

        if ValidationIssue.INSUFFICIENT_INFO in issues:
            suggestions.append("Provide more specific details and context")

        if ValidationIssue.CONFLICTING_INFO in issues:
            suggestions.append("Ensure recommendation aligns with the task type")

        return suggestions
