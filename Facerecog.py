import numpy as np
import dlib
import cv2
import imutils
import pickle
from helperF import *
import facerecogn.modeltrainer as mt


def run_face_recognition():

    # Load the pre-trained model data (facial encodings and names)
    try:
        face_encodings, face_names = mt.load_encodings()
        speak(f"Loaded {len(face_encodings)} face encodings from the trained model.")
    except FileNotFoundError:
        speak("No pre-trained model found. Starting with an empty model.")
        face_encodings = []
        face_names = []
    name = "Unknown"
    is_new_user = False  # Initialize new user flag
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)
    num_shots = 5
    shot_count = 0

    shot_folder_name = "Captured_Faces"
    os.makedirs(shot_folder_name, exist_ok=True)

    # Add these variables
    unmatched_count = 0
    running = True

    while running:

        ret, frame = cam.read()
        if not ret:
            speak("Failed to capture image")
            break

        frame = imutils.resize(frame, width=400)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        try:
            rects = mt.detector(gray_frame, 1)

        except Exception as e:
            speak(f"Error during face detection: {e}")
            break

        for rect in rects:
            x = rect.left()
            y = rect.top()
            w = rect.width()
            h = rect.height()

            face_shape = mt.shape_predictor(frame, rect)
            face_encoding = np.array(mt.face_rec_model.compute_face_descriptor(frame, face_shape))

            matches = []
            for i, known_encoding in enumerate(face_encodings):
                dist = np.linalg.norm(known_encoding - face_encoding)
                match = dist < 0.6  # Adjust this threshold if needed
                matches.append(match)

            if True in matches:
                first_match_index = matches.index(True)
                name = face_names[first_match_index]
                speak(f'identity confirmed, welcome {name}')
                unmatched_count = 0  # Reset unmatched count
                running = False

            else:
                unmatched_count += 1

                if unmatched_count == 3:
                    speak(f'new face detected, hello sir what is your name?')
                    new_name = takeCommand()
                    face_encodings.append(face_encoding)
                    face_names.append(new_name)

                    # Save updated encodings
                    mt.save_encodings(face_encodings, face_names)
                    speak(f"Updated facial encodings saved for {new_name}.")

                    name = new_name  # Update name for display
                    is_new_user = True
                    unmatched_count = 0  # Reset count
                    print(f"New face added: {new_name}")
                    print(f"Current face_names: {face_names}")

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, name, (x + 6, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if shot_count < num_shots and name != "Unknown":
                shot_filename = os.path.join(shot_folder_name, f"{name}_{shot_count}.jpg")
                cv2.imwrite(shot_filename, frame)
                shot_count += 1

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    # Return the name and new user flag
    return name, is_new_user
