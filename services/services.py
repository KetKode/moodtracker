import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from moodtracker.models.models import User, Mood

load_dotenv()

PIXELA_BASE_URL = "https://pixe.la/v1/users/"
PIXELA_TOKEN = str(os.getenv("PIXELA_TOKEN"))


def create_user(username):
    user_url = PIXELA_BASE_URL

    payload = {
        "token": PIXELA_TOKEN,
        "username": username,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
        }

    response = requests.get(user_url, json=payload)

    if response.status_code == 200:
        print(f"User '{username}' already exists")
    else:
        # If the user does not exist, attempt to create them

        create_response = requests.post(user_url, json=payload)

        if create_response.status_code == 200:
            print(f"User '{username}' created successfully")
        else:
            print(f"Failed to create user '{username}'. Status code: {create_response.status_code}")
            print(f"Response content: {create_response.content}")


def delete_user(username):
    user_url = f"{PIXELA_BASE_URL}{username}"

    headers = {
        "X-USER-TOKEN": PIXELA_TOKEN
        }

    response = requests.delete(user_url, headers=headers)

    if response.status_code == 200:
        print(f"User '{username}' deleted successfully")
    elif response.status_code == 400 and "does not exist" in response.json ().get ("message", ""):
        print(f"User '{username}' does not exist")
    else:
        print(f"Failed to delete user '{username}'. Status code: {response.status_code}")
        print(f"Response content: {response.content}")


def create_mood_graph(username):
    graph_id = f"{username}_mood"
    graph_url = f"{PIXELA_BASE_URL}{username}/graphs/{graph_id}"

    headers = {
        "X-USER-TOKEN": PIXELA_TOKEN
        }

    payload = {
        "id": graph_id,
        "name": "My Mood Journal",
        "unit": "mood",
        "type": "int",
        "color": "ajisai",  # default purple
        }

    response = requests.post(graph_url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"Graph '{graph_id}' created for user '{username}'")
    else:
        print(f"Failed to create graph '{graph_id}' for user '{username}'. Status code: {response.status_code}")

