import cv2
import time
from database import init_db, update_last_seen, get_last_seen
from face_detect import load_known_faces, detect_faces
from api_client import get_greeting, update_recognized_face
from tts import speak_text

# Initialize components
conn, cursor = init_db()
known_face_encodings, known_face_names = load_known_faces()
camera = cv2.VideoCapture(0)
cooldown_tracker = {}
COOLDOWN_TIME = 100  # Adjust cooldown duration

while True:
    ret, frame = camera.read()
    recognized_faces, face_locations = detect_faces(frame, known_face_encodings, known_face_names)

    for name in recognized_faces:
        now = time.time()
        if name in cooldown_tracker and (now - cooldown_tracker[name] < COOLDOWN_TIME):
            print(f"Skipping greeting for {name}, still in cooldown.")
            continue

        cooldown_tracker[name] = now
        last_seen = get_last_seen(cursor, name)
        update_last_seen(cursor, name)

        greeting = get_greeting(name)
        if last_seen:
            greeting += f" Welcome back! You last visited on {last_seen}."
        
        update_recognized_face(name, greeting)
        print(greeting)
        speak_text(greeting)

    time.sleep(1)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
conn.close()