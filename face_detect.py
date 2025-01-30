import face_recognition
import cv2
import numpy as np
import sqlite3
import requests
import os
import time
from datetime import datetime
import pyttsx3
import subprocess  # For macOS `say` command
import requests

# API endpoint for Gemini greeting
API_GREET_URL = "http://127.0.0.1:8000/greet/"
API_UPDATE_URL = "http://127.0.0.1:8000/recognized_faces/"

# Database setup
DB_PATH = "visits.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Create visits table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        name TEXT PRIMARY KEY,
        last_seen TEXT
    )
""")
conn.commit()

# Load known faces
KNOWN_FACES_DIR = "faces"
known_face_encodings = []
known_face_names = []

# Initialize TTS engine
engine = pyttsx3.init()

for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)

        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])  # Filename as name

print(f"Loaded known faces: {known_face_names}")

# Cooldown dictionary to track last greeting time
cooldown_tracker = {}

# Set cooldown time (in seconds)
COOLDOWN_TIME = 100  # Adjust cooldown duration

# Initialize camera
camera = cv2.VideoCapture(0)

def speak_text(text):
    """Speaks the given text using macOS 'say' or pyttsx3."""
    if os.name == "posixx":  # macOS/Linux
        subprocess.run(["say", text])  # Use macOS built-in TTS
    else:
        engine.say(text)
        engine.runAndWait()

def update_api(name, greeting):
    """Sends recognized face data to the API."""
    data = {"name": name, "greeting": greeting}
    try:
        requests.post(API_UPDATE_URL, json=data, timeout=2)
    except requests.exceptions.RequestException:
        print("Failed to update API")

while True:
    ret, frame = camera.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Stranger"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

            # Get current time
            now = time.time()

            # Check if this person was recently greeted
            if name in cooldown_tracker and (now - cooldown_tracker[name] < COOLDOWN_TIME):
                print(f"Skipping greeting for {name}, still in cooldown.")
                continue  # Skip greeting if in cooldown

            # Update cooldown tracker
            cooldown_tracker[name] = now

            # Check last visit
            cursor.execute("SELECT last_seen FROM visits WHERE name=?", (name,))
            row = cursor.fetchone()
            last_seen = row[0] if row else None

            # Update database with new visit time
            visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO visits (name, last_seen) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET last_seen=?", 
                           (name, visit_time, visit_time))
            conn.commit()

            # Send name to Gemini API for greeting
            response = requests.get(API_GREET_URL + name)
            greeting = response.json().get("message", "Hello!")

            update_api(name, greeting)
            print(greeting)
            speak_text(greeting)

        else:
            print("Stranger detected! Registering new face...")
            
            # Capture face region
            top, right, bottom, left = face_location
            face_image = frame[top:bottom, left:right]

            # Show the face and prompt for a name
            cv2.imshow("New Face", face_image)
            name = input("Enter name for this person: ").strip()

            if name:
                # Save the new face image
                face_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
                cv2.imwrite(face_path, face_image)
                print(f"Saved new face as {face_path}")

                # Encode the new face
                new_image = face_recognition.load_image_file(face_path)
                new_encoding = face_recognition.face_encodings(new_image)

                if new_encoding:
                    known_face_encodings.append(new_encoding[0])
                    known_face_names.append(name)
                    print(f"Added {name} to known faces.")

            cv2.destroyWindow("New Face")  # Close the face preview window

    # Small delay to reduce CPU usage
    time.sleep(1)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
conn.close()