"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path


class Activity:
    """Represent a school activity and manage participant signups."""

    def __init__(self, name: str, description: str, schedule: str,
                 max_participants: int, participants=None):
        self.name = name
        self.description = description
        self.schedule = schedule
        self.max_participants = max_participants
        self.participants = participants or []

    def __len__(self):
        return len(self.participants)

    def has_participant(self, email: str) -> bool:
        return any(existing.lower() == email.lower() for existing in self.participants)

    def is_full(self) -> bool:
        return len(self.participants) >= self.max_participants

    def register(self, email: str) -> str:
        normalized_email = email.strip()

        if not normalized_email:
            raise ValueError("Email is required")

        if self.has_participant(normalized_email):
            raise ValueError(f"{normalized_email} is already signed up")

        if self.is_full():
            raise ValueError(f"{self.name} is full")

        self.participants.append(normalized_email)
        return normalized_email

    def to_dict(self):
        return {
            "description": self.description,
            "schedule": self.schedule,
            "max_participants": self.max_participants,
            "participants": self.participants,
        }


app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": Activity(
        "Chess Club",
        "Learn strategies and compete in chess tournaments",
        "Fridays, 3:30 PM - 5:00 PM",
        12,
        ["michael@mergington.edu", "daniel@mergington.edu"],
    ),
    "Programming Class": Activity(
        "Programming Class",
        "Learn programming fundamentals and build software projects",
        "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        20,
        ["emma@mergington.edu", "sophia@mergington.edu"],
    ),
    "Gym Class": Activity(
        "Gym Class",
        "Physical education and sports activities",
        "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        30,
        ["john@mergington.edu", "olivia@mergington.edu"],
    ),
    "Soccer Team": Activity(
        "Soccer Team",
        "Practice teamwork and compete in soccer matches",
        "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        18,
        ["liam@mergington.edu", "noah@mergington.edu"],
    ),
    "Basketball Club": Activity(
        "Basketball Club",
        "Improve shooting, dribbling, and game strategy",
        "Wednesdays, 3:30 PM - 5:00 PM",
        16,
        ["ava@mergington.edu", "mia@mergington.edu"],
    ),
    "Drama Club": Activity(
        "Drama Club",
        "Act, improvise, and explore stage performance",
        "Mondays, 3:30 PM - 5:00 PM",
        15,
        ["charlotte@mergington.edu", "amelia@mergington.edu"],
    ),
    "Art Workshop": Activity(
        "Art Workshop",
        "Create paintings, sketches, and mixed-media artwork",
        "Thursdays, 3:30 PM - 5:00 PM",
        14,
        ["harper@mergington.edu", "ella@mergington.edu"],
    ),
    "Math Olympiad": Activity(
        "Math Olympiad",
        "Solve advanced math problems and prepare for competitions",
        "Tuesdays, 3:30 PM - 4:45 PM",
        12,
        ["benjamin@mergington.edu", "lucas@mergington.edu"],
    ),
    "Science Club": Activity(
        "Science Club",
        "Conduct experiments and explore scientific concepts",
        "Fridays, 2:30 PM - 4:00 PM",
        20,
        ["nora@mergington.edu", "zoe@mergington.edu"],
    ),
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return {name: activity.to_dict() for name, activity in activities.items()}


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    try:
        registered_email = activity.register(email)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"message": f"Signed up {registered_email} for {activity_name}"}
