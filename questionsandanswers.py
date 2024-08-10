import json
from difflib import get_close_matches


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def find_nearest_question(user_query, data):
    questions = list(data.keys())
    closest_match = get_close_matches(user_query, questions, n=1, cutoff=0.6)
    return closest_match[0] if closest_match else None


def get_answer_for_question(nearest_question, data):
    return data.get(nearest_question)
