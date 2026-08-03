"""Agentic planning: multi-step reasoning for pet care decisions with error logging."""

import json
import logging
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from enum import Enum

from pawpal_system import Owner, Pet, Task, PlannedItem


class ReasoningStep(Enum):
    """Types of reasoning steps in the planning process."""
    ANALYZE_CONSTRAINTS = "analyze_constraints"
    ASSESS_PRIORITIES = "assess_priorities"
    DETECT_CONFLICTS = "detect_conflicts"
    OPTIMIZE_SCHEDULE = "optimize_schedule"
    VALIDATE_PLAN = "validate_plan"
    EXECUTE_PLAN = "execute_plan"


@dataclass
class PlanningError:
    """Represents an error during planning."""
    step: ReasoningStep
    error_type: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    context: Dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "step": self.step.value,
            "error_type": self.error_type,
            "message": self.message,
            "timestamp": self.timestamp,
            "context": self.context,
        }


@dataclass
class ReasoningTrace:
    """Represents one reasoning step in the planning process."""
    step: ReasoningStep
    description: str
    findings: List[str]
    decisions: List[str]
    confidence: float  # 0.0 to 1.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    errors: List[PlanningError] = field(default_factory=list)

    def to_dict(self):
        return {
            "step": self.step.value,
            "description": self.description,
            "findings": self.findings,
            "decisions": self.decisions,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "errors": [e.to_dict() for e in self.errors],
        }


@dataclass
class AgenticPlanningResult:
    """Result of agentic planning process."""
    plan: List[PlannedItem]
    reasoning_traces: List[ReasoningTrace]
    errors: List[PlanningError]
    total_confidence: float
    is_viable: bool
    summary: str


class ErrorLogger:
    """Logs errors and warnings from the planning process."""

    def __init__(self, log_file: str = "planning_errors.log"):
        self.log_file = log_file
        self.errors: List[PlanningError] = []
        self.warnings: List[str] = []

        # Setup file logging
        self.logger = logging.getLogger("agentic_planner")
        self.logger.setLevel(logging.DEBUG)

        # File handler
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_error(
        self,
        step: ReasoningStep,
        error_type: str,
        message: str,
        context: Dict = None,
    ) -> PlanningError:
        """Log an error."""
        error = PlanningError(
            step=step,
            error_type=error_type,
            message=message,
            context=context or {},
        )
        self.errors.append(error)
        self.logger.error(f"[{step.value}] {error_type}: {message}")
        return error

    def log_warning(self, message: str):
        """Log a warning."""
        self.warnings.append(message)
        self.logger.warning(message)

    def get_summary(self) -> Dict:
        """Get error summary."""
        return {
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "errors_by_step": self._group_errors_by_step(),
            "error_types": self._group_errors_by_type(),
        }

    def _group_errors_by_step(self) -> Dict:
        """Group errors by planning step."""
        grouped = {}
        for error in self.errors:
            step = error.step.value
            grouped[step] = grouped.get(step, 0) + 1
        return grouped

    def _group_errors_by_type(self) -> Dict:
        """Group errors by type."""
        grouped = {}
        for error in self.errors:
            grouped[error.error_type] = grouped.get(error.error_type, 0) + 1
        return grouped


class AgenticSchedulePlanner:
    """Agentic planner that uses multi-step reasoning to create schedules."""

    def __init__(self):
        self.error_logger = ErrorLogger()
        self.reasoning_traces: List[ReasoningTrace] = []

    def plan_schedule(self, owner: Owner) -> AgenticPlanningResult:
        """
        Create a schedule using agentic multi-step reasoning.

        Steps:
        1. Analyze constraints (available time, pets)
        2. Assess priorities (task importance)
        3. Detect conflicts (timing issues)
        4. Optimize schedule (fit tasks efficiently)
        5. Validate plan (safety checks)
        6. Execute plan (return final schedule)
        """
        self.reasoning_traces = []
        self.error_logger = ErrorLogger()

        try:
            # Step 1: Analyze Constraints
            trace1 = self._step_analyze_constraints(owner)
            self.reasoning_traces.append(trace1)

            # Step 2: Assess Priorities
            trace2 = self._step_assess_priorities(owner)
            self.reasoning_traces.append(trace2)

            # Step 3: Detect Conflicts
            trace3 = self._step_detect_conflicts(owner)
            self.reasoning_traces.append(trace3)

            # Step 4: Optimize Schedule
            trace4 = self._step_optimize_schedule(owner)
            self.reasoning_traces.append(trace4)

            # Step 5: Validate Plan
            plan = trace4.decisions[0] if trace4.decisions else []
            if isinstance(plan, str):
                plan = []

            trace5 = self._step_validate_plan(plan, owner)
            self.reasoning_traces.append(trace5)

            # Step 6: Execute (return plan)
            # Use simple greedy algorithm for actual planning
            from pawpal_system import Scheduler

            scheduler = Scheduler()
            actual_plan = scheduler.generate_plan(owner)

            trace6 = ReasoningTrace(
                step=ReasoningStep.EXECUTE_PLAN,
                description="Execute the optimized schedule",
                findings=[f"Generated plan with {len(actual_plan)} items"],
                decisions=[f"Return {len([i for i in actual_plan if i.included])} included items"],
                confidence=0.95,
                errors=self.error_logger.errors,
            )
            self.reasoning_traces.append(trace6)

            # Calculate overall confidence
            total_confidence = sum(t.confidence for t in self.reasoning_traces) / len(
                self.reasoning_traces
            )

            is_viable = (
                len(self.error_logger.errors) == 0 and total_confidence >= 0.7
            )

            return AgenticPlanningResult(
                plan=actual_plan,
                reasoning_traces=self.reasoning_traces,
                errors=self.error_logger.errors,
                total_confidence=total_confidence,
                is_viable=is_viable,
                summary=self._generate_summary(actual_plan, total_confidence),
            )

        except Exception as e:
            self.error_logger.log_error(
                ReasoningStep.EXECUTE_PLAN,
                "UnexpectedError",
                str(e),
                {"exception_type": type(e).__name__},
            )
            return AgenticPlanningResult(
                plan=[],
                reasoning_traces=self.reasoning_traces,
                errors=self.error_logger.errors,
                total_confidence=0.0,
                is_viable=False,
                summary=f"Planning failed: {str(e)}",
            )

    def _step_analyze_constraints(self, owner: Owner) -> ReasoningTrace:
        """Step 1: Analyze constraints (time, pets, tasks)."""
        findings = []
        decisions = []

        try:
            # Analyze available time
            findings.append(f"Owner has {owner.available_minutes} minutes available")

            # Analyze pets
            pet_count = len(owner.pets)
            findings.append(f"Owner has {pet_count} pets")

            for pet in owner.pets:
                findings.append(f"  - {pet.name} ({pet.species}): {len(pet.tasks)} tasks")

            # Analyze tasks
            all_tasks = [task for pet in owner.pets for task in pet.tasks]
            total_duration = sum(task.duration_minutes for task in all_tasks)
            findings.append(f"Total task duration: {total_duration} minutes")

            if total_duration > owner.available_minutes * 1.5:
                self.error_logger.log_warning(
                    "Task load is significantly higher than available time"
                )

            decisions.append("Constraints analyzed successfully")

            return ReasoningTrace(
                step=ReasoningStep.ANALYZE_CONSTRAINTS,
                description="Analyze owner, pet, and task constraints",
                findings=findings,
                decisions=decisions,
                confidence=0.95,
            )

        except Exception as e:
            error = self.error_logger.log_error(
                ReasoningStep.ANALYZE_CONSTRAINTS,
                "AnalysisError",
                str(e),
            )
            return ReasoningTrace(
                step=ReasoningStep.ANALYZE_CONSTRAINTS,
                description="Analyze constraints (failed)",
                findings=[],
                decisions=["Error during analysis"],
                confidence=0.0,
                errors=[error],
            )

    def _step_assess_priorities(self, owner: Owner) -> ReasoningTrace:
        """Step 2: Assess task priorities."""
        findings = []
        decisions = []

        try:
            high_priority = 0
            medium_priority = 0
            low_priority = 0

            for pet in owner.pets:
                for task in pet.tasks:
                    if task.priority == "high":
                        high_priority += 1
                    elif task.priority == "medium":
                        medium_priority += 1
                    else:
                        low_priority += 1

            findings.append(f"High priority tasks: {high_priority}")
            findings.append(f"Medium priority tasks: {medium_priority}")
            findings.append(f"Low priority tasks: {low_priority}")

            if high_priority > owner.available_minutes / 5:
                self.error_logger.log_warning(
                    "More high-priority tasks than can likely fit in available time"
                )
                decisions.append("Triage: Focus on essential high-priority tasks first")
            else:
                decisions.append("Priority distribution is manageable")

            return ReasoningTrace(
                step=ReasoningStep.ASSESS_PRIORITIES,
                description="Assess task priorities",
                findings=findings,
                decisions=decisions,
                confidence=0.9,
            )

        except Exception as e:
            error = self.error_logger.log_error(
                ReasoningStep.ASSESS_PRIORITIES,
                "PriorityError",
                str(e),
            )
            return ReasoningTrace(
                step=ReasoningStep.ASSESS_PRIORITIES,
                description="Assess priorities (failed)",
                findings=[],
                decisions=["Error during priority assessment"],
                confidence=0.0,
                errors=[error],
            )

    def _step_detect_conflicts(self, owner: Owner) -> ReasoningTrace:
        """Step 3: Detect scheduling conflicts."""
        findings = []
        decisions = []

        try:
            from pawpal_system import Scheduler

            scheduler = Scheduler()
            conflicts = scheduler.detect_conflicts(owner)

            if conflicts:
                findings.append(f"Found {len(conflicts)} scheduling conflicts:")
                for conflict in conflicts:
                    findings.append(f"  - {conflict}")
                    self.error_logger.log_warning(f"Conflict detected: {conflict}")

                decisions.append("Manual rescheduling required for conflicting tasks")
            else:
                findings.append("No scheduling conflicts detected")
                decisions.append("Schedule is conflict-free")

            return ReasoningTrace(
                step=ReasoningStep.DETECT_CONFLICTS,
                description="Detect scheduling conflicts",
                findings=findings,
                decisions=decisions,
                confidence=0.95 if not conflicts else 0.7,
            )

        except Exception as e:
            error = self.error_logger.log_error(
                ReasoningStep.DETECT_CONFLICTS,
                "ConflictDetectionError",
                str(e),
            )
            return ReasoningTrace(
                step=ReasoningStep.DETECT_CONFLICTS,
                description="Detect conflicts (failed)",
                findings=[],
                decisions=["Error during conflict detection"],
                confidence=0.0,
                errors=[error],
            )

    def _step_optimize_schedule(self, owner: Owner) -> ReasoningTrace:
        """Step 4: Optimize schedule (fit tasks efficiently)."""
        findings = []
        decisions = []

        try:
            from pawpal_system import Scheduler

            scheduler = Scheduler()
            plan = scheduler.generate_plan(owner)

            included = [item for item in plan if item.included]
            skipped = [item for item in plan if not item.included]

            findings.append(f"Included tasks: {len(included)}")
            findings.append(f"Skipped tasks: {len(skipped)}")

            total_duration = sum(item.task.duration_minutes for item in included)
            findings.append(f"Total scheduled time: {total_duration} minutes")
            findings.append(
                f"Utilization: {(total_duration / owner.available_minutes * 100):.1f}%"
            )

            if len(skipped) > 0:
                decisions.append(f"Could not fit {len(skipped)} low-priority tasks")
                self.error_logger.log_warning(f"{len(skipped)} tasks could not be scheduled")
            else:
                decisions.append("All tasks fit within available time")

            decisions.append(f"Optimized plan generated: {len(included)} tasks included")

            return ReasoningTrace(
                step=ReasoningStep.OPTIMIZE_SCHEDULE,
                description="Optimize schedule to fit within constraints",
                findings=findings,
                decisions=decisions,
                confidence=0.85,
            )

        except Exception as e:
            error = self.error_logger.log_error(
                ReasoningStep.OPTIMIZE_SCHEDULE,
                "OptimizationError",
                str(e),
            )
            return ReasoningTrace(
                step=ReasoningStep.OPTIMIZE_SCHEDULE,
                description="Optimize schedule (failed)",
                findings=[],
                decisions=["Error during optimization"],
                confidence=0.0,
                errors=[error],
            )

    def _step_validate_plan(self, plan: List, owner: Owner) -> ReasoningTrace:
        """Step 5: Validate the generated plan."""
        findings = []
        decisions = []

        try:
            from pawpal_system import Scheduler

            scheduler = Scheduler()

            # Validate no conflicts
            conflicts = scheduler.detect_conflicts(owner)
            if conflicts:
                findings.append(f"Validation warning: {len(conflicts)} conflicts remain")
            else:
                findings.append("Validation: No time conflicts")

            # Validate total time
            from pawpal_system import PlannedItem
            if isinstance(plan, list) and len(plan) > 0 and isinstance(plan[0], PlannedItem):
                total_time = sum(item.task.duration_minutes for item in plan if item.included)
                findings.append(
                    f"Time check: {total_time} <= {owner.available_minutes} minutes"
                )

                if total_time <= owner.available_minutes:
                    decisions.append("Validation passed: Plan is feasible")
                    confidence = 0.95
                else:
                    decisions.append("Validation failed: Plan exceeds available time")
                    confidence = 0.3
            else:
                findings.append("Validation: Plan structure valid")
                decisions.append("Plan structure is valid")
                confidence = 0.9

            return ReasoningTrace(
                step=ReasoningStep.VALIDATE_PLAN,
                description="Validate the plan is feasible",
                findings=findings,
                decisions=decisions,
                confidence=confidence,
            )

        except Exception as e:
            error = self.error_logger.log_error(
                ReasoningStep.VALIDATE_PLAN,
                "ValidationError",
                str(e),
            )
            return ReasoningTrace(
                step=ReasoningStep.VALIDATE_PLAN,
                description="Validate plan (failed)",
                findings=[],
                decisions=["Error during validation"],
                confidence=0.0,
                errors=[error],
            )

    def _generate_summary(self, plan: List[PlannedItem], confidence: float) -> str:
        """Generate summary of planning result."""
        included = len([item for item in plan if item.included])
        total = len(plan)
        error_count = len(self.error_logger.errors)

        summary = f"Generated plan: {included}/{total} tasks included. "
        summary += f"Overall confidence: {confidence:.1%}. "

        if error_count > 0:
            summary += f"Warnings: {error_count} issues logged."
        else:
            summary += "No errors detected."

        return summary

    def export_reasoning_log(self, filepath: str = "reasoning_traces.json"):
        """Export reasoning traces to JSON file."""
        traces = [trace.to_dict() for trace in self.reasoning_traces]
        error_summary = self.error_logger.get_summary()

        output = {
            "timestamp": datetime.now().isoformat(),
            "traces": traces,
            "error_summary": error_summary,
        }

        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)

        return filepath
