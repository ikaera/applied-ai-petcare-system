"""
Simple Flask API for PawPal+ AI system.
Exposes endpoints for task scheduling and AI recommendations.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
from pawpal_system import Owner, Pet, Task
from src.ai.integrator import AISchedulingIntegrator

app = Flask(__name__)
CORS(app)

# Load sample data
def load_sample_data():
    """Load sample owner and pets for demo."""
    owner = Owner("Alex", 480)  # 480 minutes = 8 hours per day
    owner.pets.append(Pet("Mochi", "dog"))
    owner.pets.append(Pet("Luna", "cat"))
    return owner

# Initialize integrator
integrator = AISchedulingIntegrator(retriever_mode="heuristic")

# Global state for demo
demo_owner = load_sample_data()


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "PawPal+ API"})


@app.route("/api/pets", methods=["GET"])
def get_pets():
    """Get all pets for the owner."""
    pets = [
        {"name": pet.name, "species": pet.species}
        for pet in demo_owner.pets
    ]
    return jsonify({"pets": pets})


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks."""
    tasks = []
    for pet in demo_owner.pets:
        for task in pet.tasks:
            tasks.append({
                "id": id(task),
                "pet": pet.name,
                "title": task.title,
                "time": str(task.time),
                "priority": task.priority,
                "completed": task.completed
            })
    return jsonify({"tasks": tasks})


@app.route("/api/tasks", methods=["POST"])
def add_task():
    """Add a new task to a pet."""
    data = request.json
    pet_name = data.get("pet")
    title = data.get("title")
    time = data.get("time")
    priority = data.get("priority", "medium")

    pet = next((p for p in demo_owner.pets if p.name == pet_name), None)
    if not pet:
        return jsonify({"error": f"Pet {pet_name} not found"}), 404

    task = Task(title, time, priority)
    pet.tasks.append(task)

    return jsonify({
        "message": f"Task added for {pet_name}",
        "task": {"title": title, "time": time, "priority": priority}
    }), 201


@app.route("/api/recommend", methods=["POST"])
def get_recommendation():
    """Get AI recommendation for a task (single mode)."""
    data = request.json
    recommendation = data.get("recommendation", "Feed Mochi high-protein kibble")
    pet_name = data.get("pet", "Mochi")
    mode = data.get("mode", "heuristic")  # "heuristic" or "groq"

    # Use integrator with selected mode
    integrator.retriever_mode = mode

    result = integrator.enhance_recommendation(
        recommendation=recommendation,
        pet_name=pet_name,
        context={"age": 3, "activity": "high"}
    )

    return jsonify({
        "mode": mode,
        "recommendation": recommendation,
        "pet": pet_name,
        "validation": result.get("validation", {}),
        "retrieved_docs": result.get("retrieved_docs", []),
        "confidence": result.get("confidence", 0.0)
    })


@app.route("/api/compare", methods=["POST"])
def compare_modes():
    """Compare heuristic vs Groq API modes (A/B testing)."""
    data = request.json
    recommendation = data.get("recommendation", "Feed Mochi high-protein kibble")
    pet_name = data.get("pet", "Mochi")

    # Get results from both modes
    results = {}

    for mode in ["heuristic", "groq"]:
        integrator.retriever_mode = mode
        result = integrator.enhance_recommendation(
            recommendation=recommendation,
            pet_name=pet_name,
            context={"age": 3, "activity": "high"}
        )

        results[mode] = {
            "validation": result.get("validation", {}),
            "retrieved_docs": result.get("retrieved_docs", []),
            "confidence": result.get("confidence", 0.0),
            "metrics": result.get("metrics", {})
        }

    return jsonify({
        "recommendation": recommendation,
        "pet": pet_name,
        "heuristic": results.get("heuristic"),
        "groq": results.get("groq"),
        "comparison": {
            "both_safe": (
                results["heuristic"]["validation"].get("status") == "PASS" and
                results["groq"]["validation"].get("status") == "PASS"
            ),
            "confidence_difference": abs(
                results["heuristic"]["confidence"] -
                results["groq"]["confidence"]
            )
        }
    })


@app.route("/api/plan", methods=["POST"])
def generate_plan():
    """Generate a daily plan with AI enhancements."""
    data = request.json
    date = data.get("date", str(datetime.now().date()))

    # Generate basic plan
    plan = demo_owner.generate_plan(date)

    # Enhance each item with AI validation
    enhanced_plan = []
    for item in plan:
        result = integrator.enhance_recommendation(
            recommendation=item.get("title", ""),
            pet_name=item.get("pet", ""),
            context={}
        )

        enhanced_plan.append({
            **item,
            "validation": result.get("validation", {}),
            "confidence": result.get("confidence", 0.0)
        })

    return jsonify({
        "date": date,
        "plan": enhanced_plan,
        "total_tasks": len(enhanced_plan)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
