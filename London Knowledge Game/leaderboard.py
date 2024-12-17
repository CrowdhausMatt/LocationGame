import json

def get_all_scores():
    with open("leaderboard_data.json", "r") as file:
        data = json.load(file)
    # Sort by score ascending
    sorted_data = sorted(data, key=lambda x: x["score"])
    return sorted_data
