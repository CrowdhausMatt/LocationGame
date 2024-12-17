import random
import json
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, jsonify, redirect, url_for
from utils import read_json, calculate_distance
from leaderboard import get_all_scores

app = Flask(__name__)

@app.before_request
def enforce_https():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return redirect(request.url.replace('http://', 'https://', 1))

properties = read_json("multiple_property_data.json")
NUM_PROPERTIES_PER_GAME = 5  # Change this if you want more or fewer properties per game

@app.route("/")
def index():
    property_index = int(request.args.get("property_index", 0))
    total_score = float(request.args.get("total_score", 0.0))
    selected_indices_str = request.args.get("selected_indices")

    # If starting a new game with no selected indices, pick random properties
    if property_index == 0 and total_score == 0.0 and selected_indices_str is None:
        all_indices = list(range(len(properties)))
        chosen_indices = random.sample(all_indices, NUM_PROPERTIES_PER_GAME)
        selected_indices_str = ",".join(map(str, chosen_indices))

    # Parse the selected indices from the URL parameter
    if selected_indices_str is not None:
        selected_indices = list(map(int, selected_indices_str.split(",")))
    else:
        # Fallback if none provided
        selected_indices = list(range(NUM_PROPERTIES_PER_GAME))

    # Check if game is over
    if property_index >= NUM_PROPERTIES_PER_GAME:
        return render_template("game_over.html", total_score=total_score)

    # Get the current property from the selected indices
    current_property_id = selected_indices[property_index]

    return render_template(
        "game.html", 
        property_index=property_index, 
        properties=properties, 
        total_score=total_score,
        current_property_id=current_property_id,
        selected_indices_str=selected_indices_str
    )

@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    property_index = data["property_index"]
    guessed_lat = data["latitude"]
    guessed_lng = data["longitude"]

    selected_indices_str = request.args.get("selected_indices")
    if selected_indices_str is None:
        return jsonify({"error": "No selected indices provided"}), 400

    selected_indices = list(map(int, selected_indices_str.split(",")))

    if property_index >= len(selected_indices):
        return jsonify({"error": "Invalid property index"}), 400

    actual_property_index = selected_indices[property_index]
    actual_lat = properties[actual_property_index]["latitude"]
    actual_lng = properties[actual_property_index]["longitude"]

    distance = calculate_distance(actual_lat, actual_lng, guessed_lat, guessed_lng)
    return jsonify({"distance": distance})

@app.route("/leaderboard_data")
def leaderboard_data():
    scores = get_all_scores()
    return jsonify(scores)

@app.route("/submit_score", methods=["POST"])
def submit_score():
    name = request.form.get("name")
    agency = request.form.get("agency")
    email = request.form.get("email")
    score = float(request.form.get("score", 0.0))

    # Append new entry to leaderboard_data.json
    with open("leaderboard_data.json", "r") as file:
        data = json.load(file)
    data.append({
        "player_name": name,
        "agency": agency,
        "score": score
    })
    with open("leaderboard_data.json", "w") as file:
        json.dump(data, file, indent=4)

    # Send email notification
    subject = "New Score Submitted"
    body = f"Name: {name}\nAgency: {agency}\nEmail: {email}\nScore: {score:.1f} km"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "matt@knokknok.social"  # Replace with your Gmail
    msg["To"] = "matt@knokknok.social"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("matt@knokknok.social", "escpmzznqlizapmd")  # Replace with your App Password
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
