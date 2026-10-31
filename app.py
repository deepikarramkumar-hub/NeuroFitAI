from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("neurofit.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                goal TEXT NOT NULL,
                experience TEXT NOT NULL,
                equipment TEXT NOT NULL,
                minutes INTEGER NOT NULL,
                workout_days INTEGER NOT NULL,
                recovery_days INTEGER NOT NULL,
                focus TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

def build_plan(data):
    goal = data["goal"]
    experience = data["experience"]
    equipment = data["equipment"]
    minutes = data["minutes"]
    days = data["workout_days"]
    focus = data["focus"]

    if goal == "weight_loss":
        workout = ["5-minute warm-up walk", "20 minutes brisk walking or low-impact cardio",
                   "10 minutes bodyweight squats and wall push-ups", "5-minute cool-down"]
        diet = ["Breakfast: oats with fruit or idli with sambar",
                "Lunch: rice or chapati with vegetables and dal",
                "Snack: fruit, buttermilk or a handful of nuts",
                "Dinner: chapati with vegetables or a balanced home-cooked meal"]
    elif goal == "muscle_gain":
        workout = ["5-minute warm-up", "3 sets of squats", "3 sets of push-ups (wall or knee version if needed)",
                   "3 sets of glute bridges", "5-minute cool-down"]
        diet = ["Breakfast: eggs or paneer with whole-grain food",
                "Lunch: rice or chapati with dal, vegetables and a protein source",
                "Snack: milk, curd, fruit or roasted chana",
                "Dinner: balanced meal with protein and vegetables"]
    elif goal == "general_fitness":
        workout = ["5-minute warm-up", "10 minutes brisk walking or marching",
                   "10 minutes squats, wall push-ups and gentle core exercises", "5-minute cool-down"]
        diet = ["Breakfast: idli, dosa or oats with a protein source",
                "Lunch: balanced plate with grains, vegetables and protein",
                "Snack: fruit or nuts", "Dinner: vegetables with dal, paneer, eggs or another protein source"]
    else:
        workout = ["5-minute gentle warm-up", "10 minutes comfortable walking",
                   "10 minutes gentle mobility and stretching", "5-minute cool-down"]
        diet = ["Choose regular, balanced home-cooked meals",
                "Include vegetables and a protein source in meals",
                "Drink water regularly", "Avoid skipping meals; adjust food choices to your needs"]

    if experience == "beginner":
        level_note = "Beginner: start gently, use comfortable repetitions and take breaks whenever needed."
    elif experience == "intermediate":
        level_note = "Intermediate: use controlled movements and increase repetitions gradually."
    else:
        level_note = "Advanced: maintain good technique and adjust intensity to your recovery."

    if equipment == "none":
        equipment_note = "All suggested exercises can be done without gym equipment."
    elif equipment == "home":
        equipment_note = "Use available home equipment only when you know how to use it safely."
    else:
        equipment_note = "Gym equipment is optional; choose machines and weights you can control safely."

    return {
        "workout_title": f"{days}-day weekly fitness outline",
        "workout": workout,
        "diet": diet,
        "level_note": level_note,
        "equipment_note": equipment_note,
        "duration_note": f"Your daily target is about {minutes} minutes. Shorten or split the session if needed.",
        "focus_note": f"Focus area: {focus.replace('_', ' ').title()}",
        "weekly_note": f"Plan for {days} workout days and {data['recovery_days']} recovery days each week."
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/plan", methods=["POST"])
def create_plan():
    data = request.get_json(silent=True) or {}
    required = ["name", "goal", "experience", "equipment", "minutes",
                "workout_days", "recovery_days", "focus"]
    if any(key not in data for key in required):
        return jsonify({"error": "Please complete all fields."}), 400

    try:
        data["minutes"] = int(data["minutes"])
        data["workout_days"] = int(data["workout_days"])
        data["recovery_days"] = int(data["recovery_days"])
    except (TypeError, ValueError):
        return jsonify({"error": "Please enter valid numbers."}), 400

    if not data["name"].strip() or not (10 <= data["minutes"] <= 180):
        return jsonify({"error": "Enter your name and choose 10–180 minutes."}), 400
    if not (1 <= data["workout_days"] <= 7) or not (0 <= data["recovery_days"] <= 7):
        return jsonify({"error": "Choose valid weekly workout and recovery days."}), 400

    plan = build_plan(data)
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO plans (name, goal, experience, equipment, minutes,
            workout_days, recovery_days, focus, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data["name"].strip(), data["goal"], data["experience"], data["equipment"],
              data["minutes"], data["workout_days"], data["recovery_days"], data["focus"],
              datetime.now().isoformat(timespec="seconds")))
        plan["plan_id"] = cursor.lastrowid

    return jsonify({"plan": plan, "message": "Your fitness plan is ready!"})

@app.route("/api/history")
def history():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, name, goal, created_at FROM plans ORDER BY id DESC LIMIT 10"
        ).fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "").lower().strip()
    if not message:
        return jsonify({"reply": "Please type a question."})
    if any(word in message for word in ["diet", "food", "eat", "meal"]):
        reply = "Try to include vegetables, fruit, whole grains and a protein source in balanced meals. Choose foods that suit your needs and budget."
    elif any(word in message for word in ["workout", "exercise", "training", "gym"]):
        reply = "Start with a gentle warm-up, choose exercises that match your fitness level, focus on correct form and finish with a cool-down."
    elif any(word in message for word in ["water", "hydration"]):
        reply = "Keep water nearby and drink regularly. Your needs can vary with activity, climate and health."
    elif any(word in message for word in ["beginner", "start", "new"]):
        reply = "Start with short, comfortable sessions such as walking and basic bodyweight movements. Increase activity gradually."
    else:
        reply = "I can help with general workout, food and healthy-routine ideas. Ask me about diet, exercise, hydration or getting started."
    return jsonify({"reply": reply})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
