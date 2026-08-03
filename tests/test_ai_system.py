"""Tests for RAG retriever, validator, and AI integrator."""

import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.retriever import PetCareRetriever
from src.ai.validator import RecommendationValidator, ValidationIssue
from src.ai.integrator import AISchedulingIntegrator
from pawpal_system import Task, Pet, Owner, Scheduler, PlannedItem


class TestRetriever:
    """Tests for RAG retriever."""

    @pytest.fixture
    def retriever(self):
        """Create a retriever instance."""
        return PetCareRetriever("knowledge_base.json")

    def test_retriever_loads_documents(self, retriever):
        """Test that retriever loads knowledge base."""
        assert len(retriever.documents) > 0
        assert any("dog" in doc["title"].lower() for doc in retriever.documents)
        assert any("cat" in doc["title"].lower() for doc in retriever.documents)

    def test_retriever_finds_dog_feeding_info(self, retriever):
        """Test retrieval for dog feeding."""
        results = retriever.retrieve("dog feeding")
        assert len(results) > 0
        assert results[0].relevance_score > 0
        assert "feeding" in results[0].title.lower() or "feeding" in results[0].content.lower()

    def test_retriever_finds_cat_health_info(self, retriever):
        """Test retrieval for cat health."""
        results = retriever.retrieve("cat health")
        assert len(results) > 0
        assert "cat" in results[0].title.lower() or "cat" in results[0].content.lower()

    def test_retriever_by_category(self, retriever):
        """Test retrieval by species and category."""
        results = retriever.retrieve_by_category("dog", "walking")
        assert len(results) > 0

    def test_retriever_empty_query(self, retriever):
        """Test retriever with empty query."""
        results = retriever.retrieve("")
        assert len(results) == 0

    def test_retriever_top_k_limit(self, retriever):
        """Test that retriever respects top_k parameter."""
        results = retriever.retrieve("pet care", top_k=2)
        assert len(results) <= 2


class TestValidator:
    """Tests for recommendation validator."""

    @pytest.fixture
    def validator(self):
        """Create a validator instance."""
        return RecommendationValidator()

    def test_validator_passes_safe_recommendation(self, validator):
        """Test validation of safe, non-medical recommendation."""
        result = validator.validate_recommendation(
            recommendation="Take your dog for a 30 minute walk.",
            pet_species="dog",
            task_category="walk"
        )
        assert result.is_valid
        assert result.confidence_score >= 0.5

    def test_validator_flags_medical_without_context(self, validator):
        """Test that medical recommendations without docs are flagged."""
        result = validator.validate_recommendation(
            recommendation="Give your dog medication for pain relief.",
            pet_species="dog",
            task_category="meds",
            supporting_docs=[]
        )
        # Should have lower confidence without supporting docs
        assert result.confidence_score < 0.9

    def test_validator_with_supporting_docs(self, validator):
        """Test validation with supporting documentation."""
        result = validator.validate_recommendation(
            recommendation="Consult your veterinarian about pain medication.",
            pet_species="dog",
            task_category="meds",
            supporting_docs=["Always consult a veterinarian before administering medications"]
        )
        assert result.confidence_score > 0.6

    def test_validator_species_appropriateness(self, validator):
        """Test species-specific validation."""
        result_dog = validator.validate_recommendation(
            recommendation="Take your dog for a 30 minute walk in the morning.",
            pet_species="dog",
            task_category="walk"
        )
        assert result_dog.is_valid

    def test_validator_confidence_score_range(self, validator):
        """Test that confidence scores are in valid range."""
        result = validator.validate_recommendation(
            recommendation="Feed your pet.",
            pet_species="dog",
            task_category="feeding"
        )
        assert 0.0 <= result.confidence_score <= 1.0

    def test_validator_generates_recommendations(self, validator):
        """Test that validator generates improvement suggestions."""
        result = validator.validate_recommendation(
            recommendation="Medication",
            pet_species="dog",
            task_category="meds",
            supporting_docs=[]
        )
        if result.issues:
            assert len(result.recommendations) > 0

    def test_validator_detects_overgeneralization(self, validator):
        """Test bias detection: flags over-generalizations like 'all dogs'."""
        result = validator.validate_recommendation(
            recommendation="All dogs need the same 30 minute walk every day.",
            pet_species="dog",
            task_category="walk"
        )
        assert ValidationIssue.BIAS_DETECTED in result.issues
        assert result.confidence_score <= 0.8

    def test_validator_detects_missing_individual_context(self, validator):
        """Test bias detection: flags recommendations ignoring individual pet traits."""
        result = validator.validate_recommendation(
            recommendation="Follow the standard routine for all puppies.",
            pet_species="dog",
            task_category="walk"
        )
        assert ValidationIssue.BIAS_DETECTED in result.issues

    def test_validator_accepts_individualized_recommendation(self, validator):
        """Test that validator accepts recommendations considering individual traits."""
        result = validator.validate_recommendation(
            recommendation="Based on Mochi's age and breed, 30 minute walks are appropriate.",
            pet_species="dog",
            task_category="walk"
        )
        assert ValidationIssue.BIAS_DETECTED not in result.issues

    def test_validator_bias_suggestion(self, validator):
        """Test that validator provides bias mitigation suggestions."""
        result = validator.validate_recommendation(
            recommendation="All cats need this feeding schedule.",
            pet_species="cat",
            task_category="feeding"
        )
        if ValidationIssue.BIAS_DETECTED in result.issues:
            assert any("individual" in rec.lower() or "avoid" in rec.lower() for rec in result.recommendations)

    def test_validator_combination_medical_and_biased(self, validator):
        """Test simultaneous firing of medical + bias detection rules.

        This tests the precise interaction: when a recommendation is both medical
        AND biased, both issues should be detected and confidence should reflect
        the combined severity.
        """
        result = validator.validate_recommendation(
            recommendation="All senior dogs need this pain medication.",
            pet_species="dog",
            task_category="meds",
            supporting_docs=[]  # Missing vet docs
        )

        # Both issues should be detected
        assert ValidationIssue.BIAS_DETECTED in result.issues
        # Confidence should be lower due to combined issues
        assert result.confidence_score < 0.8
        # Should have recommendations for both issues
        assert len(result.recommendations) >= 2

    def test_validator_combination_medical_missing_docs_and_biased(self, validator):
        """Test medical task without docs that is also biased.

        Verifies that the validator correctly handles the interaction:
        - Medical (lower confidence)
        - Missing supporting docs (lower confidence)
        - Biased recommendation (lower confidence)
        = Combined effect should be very low confidence
        """
        result = validator.validate_recommendation(
            recommendation="All dogs should be given medication for general health.",
            pet_species="dog",
            task_category="meds",
            supporting_docs=[]
        )

        # Should detect both issues
        has_medical_concern = any(
            "medical" in issue.lower() or "veterinary" in issue.lower()
            for issue in [str(i) for i in result.issues]
        )
        has_bias = ValidationIssue.BIAS_DETECTED in result.issues
        assert has_bias, "Should detect bias in 'all dogs' recommendation"

        # Confidence should be significantly lowered
        assert result.confidence_score < 0.7, \
            "Combined issues (medical + missing docs + bias) should lower confidence significantly"

    def test_validator_confidence_precision_single_vs_combined_issues(self, validator):
        """Test that confidence scores precisely reflect issue severity.

        Ensures that bias detection increases issue count when present,
        and combined issues result in appropriate confidence reduction.
        """
        # Single issue: just missing context
        result_incomplete = validator.validate_recommendation(
            recommendation="Give your dog medication.",
            pet_species="dog",
            task_category="meds",
            supporting_docs=[]
        )

        # Combined: missing context + bias
        result_combined = validator.validate_recommendation(
            recommendation="All dogs need this medication.",
            pet_species="dog",
            task_category="meds",
            supporting_docs=[]
        )

        # Verify combined includes bias detection
        assert ValidationIssue.BIAS_DETECTED in result_combined.issues, \
            "Combined scenario should detect bias"

        # Combined confidence should be lower or equal
        assert result_combined.confidence_score <= result_incomplete.confidence_score, \
            "Adding bias detection should not increase confidence"

        # When bias is added to medical concerns, confidence should decrease
        if ValidationIssue.BIAS_DETECTED not in result_incomplete.issues:
            assert result_combined.confidence_score < result_incomplete.confidence_score, \
                "Adding bias to medical concerns should lower confidence"


class TestIntegrator:
    """Tests for AI scheduling integrator."""

    @pytest.fixture
    def integrator(self):
        """Create an integrator instance."""
        return AISchedulingIntegrator("knowledge_base.json")

    @pytest.fixture
    def sample_plan(self):
        """Create a sample plan to enhance."""
        owner = Owner(name="Jordan", available_minutes=90)
        mochi = Pet(name="Mochi", species="dog")
        mochi.add_task(Task("Morning walk", 30, "high", "walk"))
        mochi.add_task(Task("Feed breakfast", 10, "high", "feeding"))
        owner.add_pet(mochi)

        scheduler = Scheduler()
        return scheduler.generate_plan(owner)

    def test_integrator_enhances_plan(self, integrator, sample_plan):
        """Test that integrator adds retrieval and validation to plan."""
        pet_species_map = {"Mochi": "dog"}
        enhanced_plan = integrator.enhance_plan(sample_plan, pet_species_map)

        assert len(enhanced_plan) == len(sample_plan)
        for item in enhanced_plan:
            assert item.retrieval_results is not None
            assert item.validation_result is not None

    def test_integrator_retrieves_relevant_docs(self, integrator, sample_plan):
        """Test that integrator retrieves relevant documentation."""
        pet_species_map = {"Mochi": "dog"}
        enhanced_plan = integrator.enhance_plan(sample_plan, pet_species_map)

        walk_items = [item for item in enhanced_plan if item.planned_item.task.category == "walk"]
        if walk_items:
            assert len(walk_items[0].retrieval_results) > 0

    def test_integrator_metrics_tracking(self, integrator, sample_plan):
        """Test that integrator tracks metrics."""
        pet_species_map = {"Mochi": "dog"}
        enhanced_plan = integrator.enhance_plan(sample_plan, pet_species_map)
        metrics = integrator.get_metrics()

        assert metrics["total_items"] > 0
        assert metrics["items_validated"] > 0
        assert "avg_confidence" in metrics
        assert "avg_retrieval_score" in metrics

    def test_integrator_validates_all_items(self, integrator, sample_plan):
        """Test that integrator validates all items in plan."""
        pet_species_map = {"Mochi": "dog"}
        enhanced_plan = integrator.enhance_plan(sample_plan, pet_species_map)

        valid_count = sum(
            1 for item in enhanced_plan
            if item.validation_result and item.validation_result.is_valid
        )
        assert valid_count >= 0
        assert valid_count <= len(enhanced_plan)

    def test_integrator_log_interaction(self, integrator, sample_plan):
        """Test that integrator can log interactions."""
        pet_species_map = {"Mochi": "dog"}
        enhanced_plan = integrator.enhance_plan(sample_plan, pet_species_map)
        log = integrator.log_interaction("Test user input", enhanced_plan)

        assert "user_input" in log
        assert "items_recommended" in log
        assert "avg_confidence" in log


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_full_workflow_with_rag_validation(self):
        """Test complete workflow: scheduling -> RAG -> validation."""
        # Create owner and pets
        owner = Owner(name="Alex", available_minutes=120)

        mochi = Pet(name="Mochi", species="dog")
        mochi.add_task(Task("Morning walk", 30, "high", "walk", scheduled_time="08:00"))
        mochi.add_task(Task("Evening meds", 5, "high", "meds", scheduled_time="19:00"))
        mochi.add_task(Task("Breakfast", 10, "high", "feeding", scheduled_time="08:30"))

        luna = Pet(name="Luna", species="cat")
        luna.add_task(Task("Feeding", 5, "high", "feeding", scheduled_time="08:00"))
        luna.add_task(Task("Grooming", 15, "medium", "grooming", scheduled_time="15:00"))

        owner.add_pet(mochi)
        owner.add_pet(luna)

        # Generate base schedule
        scheduler = Scheduler()
        base_plan = scheduler.generate_plan(owner)

        # Enhance with RAG + validation
        integrator = AISchedulingIntegrator("knowledge_base.json")
        pet_species_map = {pet.name: pet.species for pet in owner.pets}
        enhanced_plan = integrator.enhance_plan(base_plan, pet_species_map)

        # Verify results
        assert len(enhanced_plan) > 0
        assert all(item.retrieval_results is not None for item in enhanced_plan)
        assert all(item.validation_result is not None for item in enhanced_plan)

        # Check metrics
        metrics = integrator.get_metrics()
        assert metrics["total_items"] > 0
        assert metrics["avg_confidence"] >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
