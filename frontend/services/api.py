import os

import requests

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def chat(session_id: str, message: str):

    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": session_id,
            "message": message,
        },
    )

    response.raise_for_status()

    return response.json()


def triage(session_id: str):

    response = requests.post(
        f"{BASE_URL}/triage",
        json={
            "session_id": session_id,
        },
    )

    response.raise_for_status()

    return response.json()


def attention(session_id: str):

    response = requests.post(
        f"{BASE_URL}/attention",
        json={
            "session_id": session_id,
        },
    )

    response.raise_for_status()

    return response.json()
