from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
mileages = []
washing_logs = []
oil_changes = []
trips = []

# ----------------------- GET
# ---- GET MILEAGE
@app.route("/mileages", methods=["GET"])
def get_mileages():
    return jsonify({"mileages": mileages})

# ---- GET Washing Logs
@app.route("/washing_logs", methods=["GET"])
def get_washing_logs():
    return jsonify({"washing_logs": washing_logs})

# ---- GET Oil Changes
@app.route("/oil_changes", methods=["GET"])
def get_oil_changes():
    return jsonify({"oil_changes": oil_changes})

# ---- GET Trips
@app.route("/trips", methods=["GET"])
def get_trips():
    return jsonify({"trips": trips})

# ------------------ POST
# ---- ADD MILEAGE
@app.route("/mileages", methods=["POST"])
def add_mileage():
    data = request.get_json()
    if not data or "date" not in data or "distance" not in data:
        return jsonify({"error": "Invalid data. 'date' and 'distance' are required."}), 400
    mileages.append(data)
    return jsonify({"message": "Mileage added!", "data": data}), 201

# ---- ADD Washing Log
@app.route("/washing_logs", methods=["POST"])
def add_washing_log():
    data = request.get_json()
    if not data or "date" not in data:
        return jsonify({"error": "Invalid data. 'date' is required."}), 400
    washing_logs.append(data)
    return jsonify({"message": "Washing log added!", "data": data}), 201

# ---- ADD Oil Change
@app.route("/oil_changes", methods=["POST"])
def add_oil_change():
    data = request.get_json()
    if not data or "date" not in data or "mileage" not in data:
        return jsonify({"error": "Invalid data. 'date' and 'mileage' are required."}), 400
    oil_changes.append(data)
    return jsonify({"message": "Oil change added!", "data": data}), 201

# ---- ADD Trip
@app.route("/trips", methods=["POST"])
def add_trip():
    data = request.get_json()
    if not data or "date" not in data or "distance" not in data or "destination" not in data:
        return jsonify({"error": "Invalid data. 'date', 'distance', and 'destination' are required."}), 400
    trips.append(data)
    return jsonify({"message": "Trip added!", "data": data}), 201

if __name__ == "__main__":
    app.run(debug=True)
