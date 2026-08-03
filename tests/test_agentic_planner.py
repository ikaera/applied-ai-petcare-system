"""Tests for agentic planner with multi-step reasoning and error logging."""

import pytest
import json
import os
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.agentic_planner import (
    AgenticSchedulePlanner,
    ErrorLogger,
    ReasoningStep,
    PlanningError,
    ReasoningTrace,
    AgenticPlanningResult,
)
from pawpal_system import Task, Pet, Owner


class TestErrorLogger:
    """Tests for error logging."""

    @pytest.fixture
    def logger(self, tmp_path):
        """Create error logger with temp file."""
        log_file = tmp_path / "test_errors.log"
        return ErrorLogger(str(log_file))

    def test_logger_logs_errors(self, logger):
        """Test that logger records errors."""
        error = logger.log_error(
            ReasoningStep.ANALYZE_CONSTRAINTS,
            "TestError",
            "This is a test error",
            {"context": "test"},
        )
        assert error.error_type == "TestError"
        assert len(logger.errors) == 1

    def test_logger_logs_warnings(self, logger):
        """Test that logger records warnings."""
        logger.log_warning("This is a test warning")
        assert len(logger.warnings) == 1

    def test_logger_summary(self, logger):
        """Test that logger generates summary."""
        logger.log_error(
            ReasoningStep.ANALYZE_CONSTRAINTS,
            "Error1",
            "First error",
        )
        logger.log_error(
            ReasoningStep.OPTIMIZE_SCHEDULE,
            "Error2",
            "Second error",
        )
        logger.log_warning("Warning 1")

        summary = logger.get_summary()
        assert summary["total_errors"] == 2
        assert summary["total_warnings"] == 1


class TestReasoningTrace:
    """Tests for reasoning trace recording."""

    def test_trace_creation(self):
        """Test that reasoning traces can be created."""
        trace = ReasoningTrace(
            step=ReasoningStep.ANALYZE_CONSTRAINTS,
            description="Test step",
            findings=["Finding 1", "Finding 2"],
            decisions=["Decision 1"],
            confidence=0.85,
        )
        assert trace.confidence == 0.85
        assert len(trace.findings) == 2

    def test_trace_serialization(self):
        """Test that traces can be serialized to dict."""
        trace = ReasoningTrace(
            step=ReasoningStep.ASSESS_PRIORITIES,
            description="Test",
            findings=["F1"],
            decisions=["D1"],
            confidence=0.9,
        )
        data = trace.to_dict()
        assert data["step"] == "assess_priorities"
        assert data["confidence"] == 0.9


class TestAgenticPlanner:
    """Tests for agentic schedule planner."""

    @pytest.fixture
    def planner(self):
        """Create planner instance."""
        return AgenticSchedulePlanner()

    @pytest.fixture
    def sample_owner(self):
        """Create sample owner with pets and tasks."""
        owner = Owner(name="Alex", available_minutes=120)

        mochi = Pet(name="Mochi", species="dog")
        mochi.add_task(Task("Morning walk", 30, "high", "walk"))
        mochi.add_task(Task("Breakfast", 10, "high", "feeding"))
        mochi.add_task(Task("Evening meds", 5, "high", "meds"))

        luna = Pet(name="Luna", species="cat")
        luna.add_task(Task("Feeding", 10, "high", "feeding"))
        luna.add_task(Task("Grooming", 15, "low", "grooming"))

        owner.add_pet(mochi)
        owner.add_pet(luna)

        return owner

    def test_planner_generates_reasoning_traces(self, planner, sample_owner):
        """Test that planner generates reasoning traces for each step."""
        result = planner.plan_schedule(sample_owner)

        assert len(result.reasoning_traces) == 6  # All 6 steps
        assert result.reasoning_traces[0].step == ReasoningStep.ANALYZE_CONSTRAINTS
        assert result.reasoning_traces[1].step == ReasoningStep.ASSESS_PRIORITIES
        assert result.reasoning_traces[2].step == ReasoningStep.DETECT_CONFLICTS
        assert result.reasoning_traces[3].step == ReasoningStep.OPTIMIZE_SCHEDULE
        assert result.reasoning_traces[4].step == ReasoningStep.VALIDATE_PLAN
        assert result.reasoning_traces[5].step == ReasoningStep.EXECUTE_PLAN

    def test_planner_returns_viable_plan(self, planner, sample_owner):
        """Test that planner returns a viable plan."""
        result = planner.plan_schedule(sample_owner)

        assert result.is_viable is True
        assert len(result.plan) > 0
        assert result.total_confidence > 0.5

    def test_planner_confidence_score(self, planner, sample_owner):
        """Test that planner calculates confidence score."""
        result = planner.plan_schedule(sample_owner)

        # Confidence is average of all trace confidences
        assert 0.0 <= result.total_confidence <= 1.0
        assert result.total_confidence > 0.7  # Should be high for valid plan

    def test_planner_handles_overloaded_schedule(self, planner):
        """Test planner with too many tasks."""
        owner = Owner(name="Busy", available_minutes=30)

        pet = Pet(name="Max", species="dog")
        pet.add_task(Task("Walk", 30, "high", "walk"))
        pet.add_task(Task("Feed", 20, "high", "feeding"))
        pet.add_task(Task("Groom", 30, "high", "grooming"))

        owner.add_pet(pet)

        result = planner.plan_schedule(owner)

        # Should have warnings about overload
        assert len(result.reasoning_traces) > 0
        warnings = [t for t in result.reasoning_traces if t.confidence < 0.9]
        assert len(warnings) > 0

    def test_planner_includes_plan_in_result(self, planner, sample_owner):
        """Test that result includes actual plan."""
        result = planner.plan_schedule(sample_owner)

        assert isinstance(result.plan, list)
        assert len(result.plan) > 0

    def test_planner_step_analyze_constraints(self, planner, sample_owner):
        """Test constraint analysis step."""
        trace = planner._step_analyze_constraints(sample_owner)

        assert trace.step == ReasoningStep.ANALYZE_CONSTRAINTS
        assert len(trace.findings) > 0
        assert "available" in trace.findings[0].lower()

    def test_planner_step_assess_priorities(self, planner, sample_owner):
        """Test priority assessment step."""
        trace = planner._step_assess_priorities(sample_owner)

        assert trace.step == ReasoningStep.ASSESS_PRIORITIES
        assert "high priority" in "".join(trace.findings).lower()

    def test_planner_step_detect_conflicts(self, planner, sample_owner):
        """Test conflict detection step."""
        trace = planner._step_detect_conflicts(sample_owner)

        assert trace.step == ReasoningStep.DETECT_CONFLICTS
        assert len(trace.findings) > 0

    def test_error_logger_integration(self, planner, sample_owner):
        """Test that errors are logged during planning."""
        result = planner.plan_schedule(sample_owner)

        # Check error logger captured any issues
        assert isinstance(result.errors, list)
        summary = planner.error_logger.get_summary()
        assert "total_errors" in summary

    def test_reasoning_log_export(self, planner, sample_owner, tmp_path):
        """Test exporting reasoning traces to JSON."""
        result = planner.plan_schedule(sample_owner)

        log_file = tmp_path / "reasoning.json"
        exported = planner.export_reasoning_log(str(log_file))

        assert os.path.exists(exported)
        with open(exported) as f:
            data = json.load(f)
            assert "traces" in data
            assert "error_summary" in data
            assert len(data["traces"]) == 6

    def test_planning_result_summary(self, planner, sample_owner):
        """Test that planning result includes summary."""
        result = planner.plan_schedule(sample_owner)

        assert result.summary is not None
        assert len(result.summary) > 0
        assert "tasks" in result.summary.lower()


class TestIntegrationAgenticPlanner:
    """End-to-end integration tests for agentic planner."""

    def test_full_planning_workflow(self):
        """Test complete agentic planning workflow."""
        # Create planner
        planner = AgenticSchedulePlanner()

        # Create owner with multiple pets
        owner = Owner(name="Jordan", available_minutes=90)

        mochi = Pet(name="Mochi", species="dog")
        mochi.add_task(Task("Morning walk", 30, "high", "walk"))
        mochi.add_task(Task("Evening meds", 5, "high", "meds"))
        mochi.add_task(Task("Breakfast", 10, "high", "feeding"))

        whiskers = Pet(name="Whiskers", species="cat")
        whiskers.add_task(Task("Feeding", 10, "high", "feeding"))
        whiskers.add_task(Task("Grooming", 15, "low", "grooming"))

        owner.add_pet(mochi)
        owner.add_pet(whiskers)

        # Run planning
        result = planner.plan_schedule(owner)

        # Verify results
        assert result.is_viable
        assert len(result.plan) > 0
        assert len(result.reasoning_traces) == 6
        assert result.total_confidence > 0.7

    def test_reasoning_traces_show_progression(self):
        """Test that reasoning traces show logical progression."""
        planner = AgenticSchedulePlanner()

        owner = Owner(name="Test", available_minutes=60)
        pet = Pet(name="Buddy", species="dog")
        pet.add_task(Task("Walk", 30, "high", "walk"))
        pet.add_task(Task("Feed", 10, "high", "feeding"))
        owner.add_pet(pet)

        result = planner.plan_schedule(owner)

        # Traces should progress through planning steps
        steps = [t.step for t in result.reasoning_traces]
        assert ReasoningStep.ANALYZE_CONSTRAINTS in steps
        assert ReasoningStep.ASSESS_PRIORITIES in steps
        assert ReasoningStep.OPTIMIZE_SCHEDULE in steps
        assert ReasoningStep.VALIDATE_PLAN in steps


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
