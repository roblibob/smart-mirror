import face_recognition
import cv2
import numpy as np
import os

KNOWN_FACES_DIR = "faces"

def load_known_faces():
    """Loads known faces from the 'faces' directory."""
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)

            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(os.path.splitext(filename)[0])

    print(f"Loaded known faces: {known_face_names}")
    return known_face_encodings, known_face_names

def detect_faces(frame, known_face_encodings, known_face_names):
    """Detects faces and returns recognized names."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    recognized_faces = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Stranger"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        recognized_faces.append(name)

    return recognized_faces, face_locations