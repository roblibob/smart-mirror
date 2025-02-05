import cv2
import time
from modules.database import init_db, update_last_seen, get_last_seen
from modules.face_detect import load_known_faces, detect_faces
from modules.api_client import get_greeting, update_recognized_face
from modules.tts import speak_text
from modules.calendar_client import get_today_events
from modules.weather import get_weather
from config_loader import config

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
        agenda = get_today_events(name)
        weather_data = get_weather()
        weather = f"{weather_data['current_condition'][0]['weatherDesc'][0]['value']} and {weather_data['current_condition'][0]['temp_C']}°C"
        print(weather)
        greeting = get_greeting(name, agenda, weather)

        #if last_seen:
        #    greeting += f" Welcome back! You last visited on {last_seen}."
        
        update_recognized_face(name, greeting)
        print(greeting)
        speak_text(greeting)

    time.sleep(1)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
conn.close()