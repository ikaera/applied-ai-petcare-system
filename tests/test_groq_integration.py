"""Integration tests for Groq API mode retrieval."""

import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.retriever import PetCareRetriever, GroqEnhancedRetriever
from src.ai.integrator import AISchedulingIntegrator
from pawpal_system import Task, Pet, Owner, Scheduler


class TestGroqEnhancedRetriever:
    """Tests for GroqEnhancedRetriever with API fallback."""

    @pytest.fixture
    def heuristic_retriever(self):
        """Create heuristic-only retriever."""
        return PetCareRetriever("knowledge_base.json")

    @pytest.fixture
    def groq_retriever(self):
        """Create Groq retriever (API disabled if key missing)."""
        return GroqEnhancedRetriever("knowledge_base.json", use_api=False)

    @pytest.fixture
    def groq_api_retriever(self):
        """Create Groq retriever with API enabled."""
        return GroqEnhancedRetriever("knowledge_base.json", use_api=True)

    def test_groq_retriever_fallback_to_heuristic(self, groq_retriever):
        """Test that Groq retriever falls back to heuristic when API unavailable."""
        results = groq_retriever.retrieve("dog exercise")
        assert len(results) > 0
        assert all(hasattr(r, 'title') for r in results)
        assert all(0 <= r.relevance_score <= 1.0 for r in results)

    def test_groq_mode_returns_valid_results(self, groq_api_retriever):
        """Test that Groq mode returns properly formatted results."""
        results = groq_api_retriever.retrieve("cat feeding schedule", top_k=3)
        assert len(results) <= 3
        for result in results:
            assert hasattr(result, 'document_id')
            assert hasattr(result, 'title')
            assert hasattr(result, 'content')
            assert 0 <= result.relevance_score <= 1.0

    def test_groq_retriever_get_mode(self, groq_retriever, groq_api_retriever):
        """Test retriever mode reporting."""
        assert "Heuristic only" in groq_retriever.get_mode()
        assert "Groq API" in groq_api_retriever.get_mode() or "Heuristic" in groq_api_retriever.get_mode()

    def test_groq_and_heuristic_return_same_format(self, heuristic_retriever, groq_retriever):
        """Test that both retriever types return consistent format."""
        query = "dog health care"
        heuristic_results = heuristic_retriever.retrieve(query, top_k=3)
        groq_results = groq_retriever.retrieve(query, top_k=3)

        # Both should return same type of objects
        assert type(heuristic_results) == type(groq_results)

        # Each result should have same attributes
        for h_result, g_result in zip(heuristic_results, groq_results):
            assert hasattr(h_result, 'title') and hasattr(g_result, 'title')
            assert hasattr(h_result, 'content') and hasattr(g_result, 'content')
            assert hasattr(h_result, 'relevance_score') and hasattr(g_result, 'relevance_score')


class TestDualModeIntegration:
    """Tests for dual-mode scheduling integration."""

    @pytest.fixture
    def test_owner(self):
        """Create test owner with pets."""
        owner = Owner(name="TestOwner", available_minutes=120)

        dog = Pet(name="TestDog", species="dog")
        dog.add_task(Task("Walk", 30, "high", "walk"))
        dog.add_task(Task("Feed", 10, "high", "feeding"))

        cat = Pet(name="TestCat", species="cat")
        cat.add_task(Task("Feed", 5, "high", "feeding"))
        cat.add_task(Task("Groom", 15, "medium", "grooming"))

        owner.add_pet(dog)
        owner.add_pet(cat)
        return owner

    def test_integrator_heuristic_mode(self, test_owner):
        """Test integrator in heuristic mode."""
        scheduler = Scheduler()
        base_plan = scheduler.generate_plan(test_owner)

        integrator = AISchedulingIntegrator(
            knowledge_base_path="knowledge_base.json",
            retriever_mode="heuristic"
        )

        pet_species_map = {pet.name: pet.species for pet in test_owner.pets}
        enhanced_plan = integrator.enhance_plan(base_plan, pet_species_map)

        assert len(enhanced_plan) == len(base_plan)
        assert all(hasattr(item, 'retrieval_results') for item in enhanced_plan)
        assert integrator.get_retriever_mode() == "Heuristic (keyword-based)"

    def test_integrator_groq_mode(self, test_owner):
        """Test integrator in Groq mode (with fallback)."""
        scheduler = Scheduler()
        base_plan = scheduler.generate_plan(test_owner)

        integrator = AISchedulingIntegrator(
            knowledge_base_path="knowledge_base.json",
            retriever_mode="groq"
        )

        pet_species_map = {pet.name: pet.species for pet in test_owner.pets}
        enhanced_plan = integrator.enhance_plan(base_plan, pet_species_map)

        assert len(enhanced_plan) == len(base_plan)
        assert all(hasattr(item, 'validation_result') for item in enhanced_plan)
        mode = integrator.get_retriever_mode()
        assert "Groq" in mode or "Heuristic" in mode

    def test_integrator_metrics_include_mode(self, test_owner):
        """Test that metrics include retriever mode information."""
        scheduler = Scheduler()
        base_plan = scheduler.generate_plan(test_owner)

        integrator = AISchedulingIntegrator(
            knowledge_base_path="knowledge_base.json",
            retriever_mode="heuristic"
        )

        pet_species_map = {pet.name: pet.species for pet in test_owner.pets}
        integrator.enhance_plan(base_plan, pet_species_map)

        metrics = integrator.get_metrics()
        assert "retriever_mode" in metrics
        assert metrics["retriever_mode"] == "Heuristic (keyword-based)"

    def test_both_modes_preserve_validation(self, test_owner):
        """Test that both modes apply validation correctly."""
        scheduler = Scheduler()
        base_plan = scheduler.generate_plan(test_owner)
        pet_species_map = {pet.name: pet.species for pet in test_owner.pets}

        results = {}
        for mode in ["heuristic", "groq"]:
            integrator = AISchedulingIntegrator(
                knowledge_base_path="knowledge_base.json",
                retriever_mode=mode
            )
            enhanced = integrator.enhance_plan(base_plan, pet_species_map)
            results[mode] = enhanced

        # Both modes should validate all items
        for mode in ["heuristic", "groq"]:
            assert all(item.validation_result is not None
                      for item in results[mode]
                      if item.planned_item.included)


class TestGroqFallback:
    """Tests for API fallback behavior."""

    def test_groq_fallback_on_no_key(self):
        """Test fallback when API key is missing."""
        # Create retriever with API enabled but no key
        retriever = GroqEnhancedRetriever("knowledge_base.json", use_api=True)

        # Should still work (fallback to heuristic)
        results = retriever.retrieve("dog health", top_k=3)
        assert len(results) > 0

    def test_groq_explicit_heuristic_mode(self):
        """Test explicit heuristic-only mode."""
        retriever = GroqEnhancedRetriever("knowledge_base.json", use_api=False)

        results = retriever.retrieve("pet training", top_k=3)
        assert len(results) > 0
        assert retriever.get_mode() == "Heuristic only"

    def test_groq_retriever_top_k_respected(self):
        """Test that top_k limit is respected in both modes."""
        heuristic = PetCareRetriever("knowledge_base.json")
        groq = GroqEnhancedRetriever("knowledge_base.json", use_api=False)

        for top_k in [1, 2, 3, 5]:
            h_results = heuristic.retrieve("dog exercise", top_k=top_k)
            g_results = groq.retrieve("dog exercise", top_k=top_k)

            assert len(h_results) <= top_k
            assert len(g_results) <= top_k


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
