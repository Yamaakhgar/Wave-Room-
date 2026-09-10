
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

rooms = [
    {"id": 1, "name": "Tech Talk", "topic": "AI, apps, coding & startups", "listeners": 245, "host": "Alex"},
    {"id": 2, "name": "Late Night", "topic": "Relaxed conversations after dark", "listeners": 198, "host": "Emma"},
    {"id": 3, "name": "Music Vibes", "topic": "Music, artists and good energy", "listeners": 156, "host": "John"},
]

messages = [
    {"user": "Emma", "text": "This is so interesting! 🔥", "time": "Now"},
    {"user": "John", "text": "Amazing conversation!", "time": "Now"},
]

@app.route("/")
def home():
    return render_template("index.html", rooms=rooms)

@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    return jsonify(rooms)

@app.route("/api/rooms", methods=["POST"])
def create_room():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    topic = (data.get("topic") or "").strip() or "General conversation"

    if not name:
        return jsonify({"error": "Room name is required"}), 400

    new_room = {
        "id": max([r["id"] for r in rooms], default=0) + 1,
        "name": name,
        "topic": topic,
        "listeners": 1,
        "host": "You",
    }
    rooms.insert(0, new_room)
    return jsonify(new_room), 201

@app.route("/api/rooms/<int:room_id>/join", methods=["POST"])
def join_room(room_id):
    room = next((r for r in rooms if r["id"] == room_id), None)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    room["listeners"] += 1
    return jsonify({
        "message": f"You joined {room['name']}",
        "room": room
    })

@app.route("/api/messages", methods=["GET"])
def get_messages():
    return jsonify(messages)

@app.route("/api/messages", methods=["POST"])
def send_message():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Message cannot be empty"}), 400

    msg = {
        "user": "You",
        "text": text,
        "time": datetime.now().strftime("%I:%M %p")
    }
    messages.append(msg)
    return jsonify(msg), 201

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
