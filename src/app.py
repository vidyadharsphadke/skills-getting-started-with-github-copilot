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
    "Chess Club": Activity(**{
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    }),
    "Programming Class": Activity(**{
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    }),
    "Gym Class": Activity(**{
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    }),
    "Soccer Team": Activity(**{
        "name": "Soccer Team",
        "description": "Practice teamwork and compete in soccer matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
    }),
    "Basketball Club": Activity(**{
        "name": "Basketball Club",
        "description": "Improve shooting, dribbling, and game strategy",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
    }),
    "Drama Club": Activity(**{
        "name": "Drama Club",
        "description": "Act, improvise, and explore stage performance",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"],
    }),
    "Art Workshop": Activity(**{
        "name": "Art Workshop",
        "description": "Create paintings, sketches, and mixed-media artwork",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["harper@mergington.edu", "ella@mergington.edu"],
    }),
    "Math Olympiad": Activity(**{
        "name": "Math Olympiad",
        "description": "Solve advanced math problems and prepare for competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
        "max_participants": 12,
        "participants": ["benjamin@mergington.edu", "lucas@mergington.edu"],
    }),
    "Science Club": Activity(**{
        "name": "Science Club",
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 2:30 PM - 4:00 PM",
        "max_participants": 20,
        "participants": ["nora@mergington.edu", "zoe@mergington.edu"],
    }),
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
