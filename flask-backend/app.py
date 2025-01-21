import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime  # Import datetime for date handling

app = Flask(__name__)

# Firebase setup
firebase_cert_path = "C:/Users/wadia/mt05-terminal/flask-backend/firebase_config/firebase-admin-sdk.json"
if not os.path.exists(firebase_cert_path):
    print(f"File not found at path: {firebase_cert_path}")
else:
    cred = credentials.Certificate(firebase_cert_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()  # Use Firebase Admin SDK's Firestore client

# ----------------------- GET
# ---- GET MILEAGE
@app.route("/mileages", methods=["GET"])
def get_mileages():
    mileages_ref = db.collection("mileages")
    docs = mileages_ref.stream()
    mileages = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    return jsonify({"mileages": mileages})

# ---- GET Washing Logs
@app.route("/washing_logs", methods=["GET"])
def get_washing_logs():
    washing_logs_ref = db.collection("washing_logs")
    docs = washing_logs_ref.stream()
    washing_logs = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    return jsonify({"washing_logs": washing_logs})

# ---- GET Oil Changes
@app.route("/oil_changes", methods=["GET"])
def get_oil_changes():
    oil_changes_ref = db.collection("oil_changes")
    docs = oil_changes_ref.stream()
    oil_changes = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    return jsonify({"oil_changes": oil_changes})

# ---- GET Trips
@app.route("/trips", methods=["GET"])
def get_trips():
    trips_ref = db.collection("trips")
    docs = trips_ref.stream()
    trips = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    return jsonify({"trips": trips})

# ------------------ POST
# ---- ADD MILEAGE
@app.route("/mileages", methods=["POST"])
def add_mileage():
    data = request.get_json()
    if not data or "date" not in data or "distance" not in data:
        return jsonify({"error": "Invalid data. 'date' and 'distance' are required."}), 400

    try:
        # Convert the date string to a datetime object
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'."}), 400

    try:
        # Add the mileage data to Firestore
        doc_ref = db.collection("mileages").document()  # Create a new document reference
        doc_ref.set(data)  # Set the data for the document

        # Format the date to include accurate clock time
        formatted_date = data["date"].strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Return the response with the document ID and formatted date
        return jsonify({
            "message": "Mileage added!",
            "data": {
                "date": formatted_date,  # Use the formatted date
                "distance": data["distance"]
            },
            "id": doc_ref.id
        }), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ---- ADD Washing Log
@app.route("/washing_logs", methods=["POST"])
def add_washing_log():
    data = request.get_json()
    if not data or "date" not in data:
        return jsonify({"error": "Invalid data. 'date' is required."}), 400

    try:
        # Convert the date string to a datetime object
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'."}), 400

    try:
        # Add the washing log data to Firestore
        doc_ref = db.collection("washing_logs").document()  # Create a new document reference
        doc_ref.set(data)  # Set the data for the document

        # Format the date to include accurate clock time
        formatted_date = data["date"].strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Return the response with the document ID and formatted date
        return jsonify({
            "message": "Washing log added!",
            "data": {
                "date": formatted_date,  # Use the formatted date
                **data  # Include other fields from the request
            },
            "id": doc_ref.id
        }), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ---- ADD Oil Change
@app.route("/oil_changes", methods=["POST"])
def add_oil_change():
    data = request.get_json()
    if not data or "date" not in data or "mileage" not in data:
        return jsonify({"error": "Invalid data. 'date' and 'mileage' are required."}), 400

    try:
        # Convert the date string to a datetime object
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'."}), 400

    try:
        # Add the oil change data to Firestore
        doc_ref = db.collection("oil_changes").document()  # Create a new document reference
        doc_ref.set(data)  # Set the data for the document

        # Format the date to include accurate clock time
        formatted_date = data["date"].strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Return the response with the document ID and formatted date
        return jsonify({
            "message": "Oil change added!",
            "data": {
                "date": formatted_date,  # Use the formatted date
                "mileage": data["mileage"]
            },
            "id": doc_ref.id
        }), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ---- ADD Trip
@app.route("/trips", methods=["POST"])
def add_trip():
    data = request.get_json()
    if not data or "date" not in data or "distance" not in data or "destination" not in data:
        return jsonify({"error": "Invalid data. 'date', 'distance', and 'destination' are required."}), 400

    try:
        # Convert the date string to a datetime object
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'."}), 400

    try:
        # Add the trip data to Firestore
        doc_ref = db.collection("trips").document()  # Create a new document reference
        doc_ref.set(data)  # Set the data for the document

        # Format the date to include accurate clock time
        formatted_date = data["date"].strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Return the response with the document ID and formatted date
        return jsonify({
            "message": "Trip added!",
            "data": {
                "date": formatted_date,  # Use the formatted date
                "distance": data["distance"],
                "destination": data["destination"]
            },
            "id": doc_ref.id
        }), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)