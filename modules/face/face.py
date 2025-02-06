from core.base_module import BaseModule
import face_recognition
import cv2
import os
import numpy as np
import time

class Module(BaseModule):
    def __init__(self, config, event_bus):
        super().__init__(config, event_bus, update_interval=5)
        self.config = config
        self.event_bus = event_bus  # Store reference to the event bus
        self.dir = config.get("dir", "faces")
        self.camera = cv2.VideoCapture(0)
        self.cooldown_tracker = {}
        self.cooldown_time = config.get("cooldown", 100)

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        self.known_face_encodings, self.known_face_names = self.load_known_faces()
    
    def load_known_faces(self):
        """Loads known faces from the directory."""
        known_face_encodings = []
        known_face_names = []

        for filename in os.listdir(self.dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                img_path = os.path.join(self.dir, filename)
                image = face_recognition.load_image_file(img_path)
                encoding = face_recognition.face_encodings(image)

                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(os.path.splitext(filename)[0])

        print(f"🔍 Loaded known faces: {known_face_names}")
        return known_face_encodings, known_face_names

    def detect_faces(self, frame):
        """Detects faces and returns recognized names."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        recognized_faces = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Stranger"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            recognized_faces.append(name)

        return recognized_faces

    def update(self):
        print("📸 Running face detection...", flush=True)
        """Runs face detection and emits an event when a face is recognized."""
        ret, frame = self.camera.read()
        if not ret:
            return
        
        recognized_faces = self.detect_faces(frame)

        for name in recognized_faces:
            now = time.time()
            if name in self.cooldown_tracker and (now - self.cooldown_tracker[name] < self.cooldown_time):
                print(f"Skipping greeting for {name}, still in cooldown.")
                continue

            self.cooldown_tracker[name] = now

            # Emit an event to notify that a face was detected
            self.event_bus.emit("face_detected", {"name": name})
            print(f"👤 Detected face: {name}")

    def cleanup(self):
        """Releases resources."""
        self.camera.release()
        cv2.destroyAllWindows()