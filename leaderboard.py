import os
import time
import json
import datetime

SCORE_FILE = 'score.txt'
LEADERBOARD_FILE = 'leaderboard.txt'
MAX_LEADERBOARD_SIZE = 10

def read_scores():
    """
    Read scores from the score file and return them as a list of dictionaries.
    """
    scores = []
    try:
        with open(SCORE_FILE, 'r') as file:
            data = file.read()
            if data.strip():  # Check if data is not empty after stripping
                json_array = json.loads(data)
                for line in json_array:
                    # Convert string datetime to datetime object
                    line['datetime'] = datetime.datetime.strptime(line['datetime'], '%m-%d-%Y')
                    scores.append(line)
    except FileNotFoundError:
        print("Score file not found.")
    except Exception as e:
        print("Error reading scores:", e)
    return scores


def write_leaderboard(scores):
    """
    Write scores to the leaderboard file.
    """
    try:
        with open(LEADERBOARD_FILE, 'w') as file:
            for score in scores:
                # Convert datetime object to string
                score['datetime'] = score['datetime'].strftime('%m-%d-%Y')
                file.write(json.dumps(score) + '\n')
    except Exception as e:
        print("Error writing leaderboard:", e)



def update_leaderboard():
    """
    Sorts and verifies scores, then calls write_leaderboard() to update
    """
    scores = read_scores()
    print("Scores read:", scores)
    
    # Filter out duplicate entries based on user, score, and datetime
    unique_scores = {}
    for score in scores:
        key = (score['User'], score['Score'], score['datetime'])
        if key not in unique_scores:
            unique_scores[key] = score
    
    print("Unique scores:", unique_scores)
    
    # Sort unique scores and limit leaderboard size
    leaderboard = sorted(unique_scores.values(), key=lambda x: x['Score'], reverse=True)[:MAX_LEADERBOARD_SIZE]
    print("Leaderboard:", leaderboard)
    
    write_leaderboard(leaderboard)



if __name__ == "__main__":
    while True:
        # Check for modifications to score.txt
        try:
            score_file_modified = os.path.getmtime(SCORE_FILE)
            time.sleep(1)  # Check every second
            if os.path.getmtime(SCORE_FILE) != score_file_modified:
                update_leaderboard()
                print("Leaderboard updated.")
        except Exception as e:
            print("Error:", e)
