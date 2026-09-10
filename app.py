
from flask import Flask, render_template, request, jsonify

from database import add_message, add_room, join_room, list_messages, list_rooms

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", rooms=list_rooms())

@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    return jsonify(list_rooms())

@app.route("/api/rooms", methods=["POST"])
def create_room():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    topic = (data.get("topic") or "").strip() or "General conversation"

    if not name:
        return jsonify({"error": "Room name is required"}), 400

    new_room = add_room(name, topic)
    return jsonify(new_room), 201

@app.route("/api/rooms/<int:room_id>/join", methods=["POST"])
def join_room(room_id):
    room = join_room(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    room["listeners"] += 1
    return jsonify({
        "message": f"You joined {room['name']}",
        "room": room
    })

@app.route("/api/messages", methods=["GET"])
def get_messages():
    return jsonify(list_messages())

@app.route("/api/messages", methods=["POST"])
def send_message():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Message cannot be empty"}), 400

    msg = add_message(text)
    return jsonify(msg), 201

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
