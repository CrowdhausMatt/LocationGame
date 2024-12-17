from flask import session
from utils import calculate_distance

def handle_guess(latitude, longitude, property_index, property_data):
    # Initialize session variables if they don't exist
    if 'properties_guessed' not in session:
        session['properties_guessed'] = 0
        session['total_score'] = 0

    # Assuming property_data is a list of dictionaries with property info
    current_property = property_data[property_index]
    distance = calculate_distance(latitude, longitude, current_property['latitude'], current_property['longitude'])

    # Increment the properties guessed counter
    session['properties_guessed'] += 1
    session['total_score'] += distance  # Update total score

    # Check if the game is over
    game_over = session['properties_guessed'] >= 5

    return {
        'distance': distance,
        'game_over': game_over,
        'total_score': session['total_score']
    }
