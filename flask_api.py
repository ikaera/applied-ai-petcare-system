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
                "time": task.scheduled_time,
                "duration": task.duration_minutes,
                "category": task.category,
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
    duration = data.get("duration_minutes", 15)
    priority = data.get("priority", "medium")
    category = data.get("category", "enrichment")
    scheduled_time = data.get("scheduled_time", "09:00")

    pet = next((p for p in demo_owner.pets if p.name == pet_name), None)
    if not pet:
        return jsonify({"error": f"Pet {pet_name} not found"}), 404

    task = Task(title, duration, priority, category, scheduled_time=scheduled_time)
    pet.add_task(task)

    return jsonify({
        "message": f"Task added for {pet_name}",
        "task": {"title": title, "duration": duration, "priority": priority, "category": category}
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

    # Return a mock recommendation result for demo
    return jsonify({
        "mode": mode,
        "recommendation": recommendation,
        "pet": pet_name,
        "validation": {
            "status": "PASS",
            "note": "Recommendation is safe and species-appropriate"
        },
        "retrieved_docs": [
            "Dog Nutrition Basics",
            "Feeding Guidelines by Age"
        ],
        "confidence": 0.95
    })


@app.route("/api/compare", methods=["POST"])
def compare_modes():
    """Compare heuristic vs Groq API modes (A/B testing)."""
    data = request.json
    recommendation = data.get("recommendation", "Feed Mochi high-protein kibble")
    pet_name = data.get("pet", "Mochi")

    # Return mock A/B comparison
    return jsonify({
        "recommendation": recommendation,
        "pet": pet_name,
        "heuristic": {
            "validation": {"status": "PASS", "note": "Keyword match found"},
            "retrieved_docs": ["Dog Nutrition Basics"],
            "confidence": 0.88,
            "metrics": {"docs_retrieved": 1}
        },
        "groq": {
            "validation": {"status": "PASS", "note": "Semantically relevant"},
            "retrieved_docs": ["Dog Nutrition Basics", "Feeding Guidelines"],
            "confidence": 0.95,
            "metrics": {"docs_retrieved": 2}
        },
        "comparison": {
            "both_safe": True,
            "confidence_difference": 0.07
        }
    })


@app.route("/api/plan", methods=["POST"])
def generate_plan():
    """Generate a daily plan with AI enhancements."""
    data = request.json
    date = data.get("date", str(datetime.now().date()))

    # Generate basic plan
    plan = demo_owner.generate_plan(date)

    # Return plan with mock validation
    enhanced_plan = [
        {
            "title": task.title,
            "pet": pet.name,
            "time": task.scheduled_time,
            "duration": task.duration_minutes,
            "category": task.category,
            "validation": {"status": "PASS", "note": "Task is safe"},
            "confidence": 0.95
        }
        for pet in demo_owner.pets
        for task in pet.tasks
    ]

    return jsonify({
        "date": date,
        "plan": enhanced_plan,
        "total_tasks": len(enhanced_plan)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
