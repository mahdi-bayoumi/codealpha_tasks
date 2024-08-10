import dlib
import cv2
import numpy as np
import os
import pickle
from imutils import paths
import imutils
from helperF import *

# Load the shape predictor and face recognition models
shape_predictor = dlib.shape_predictor(r"shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1(r"dlib_face_recognition_resnet_model_v1.dat")

# Load the pre-trained face detector
detector = dlib.get_frontal_face_detector()


def train_face_recognition(image, person_name):
    """
    Train face recognition on a single image.

    :param image: numpy array of the image (BGR format)
    :param person_name: string, name of the person in the image
    :return: tuple of (face_encoding, person_name) if a face is found, None otherwise
    """
    # Resize the image
    image = imutils.resize(image, width=600)

    # Convert to RGB (dlib uses RGB)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    rects = detector(rgb_image, 1)

    if len(rects) > 0:
        # Use the first detected face
        rect = rects[0]

        # Get facial landmarks
        shape = shape_predictor(rgb_image, rect)

        # Compute face encoding
        face_encoding = np.array(face_rec_model.compute_face_descriptor(rgb_image, shape))

        return face_encoding, person_name

    return None


def load_encodings():
    """Load existing encodings from file."""
    if os.path.exists("facial_encodings.dat"):
        with open("facial_encodings.dat", "rb") as f:
            return pickle.load(f)
    return [], []


def save_encodings(face_encodings, face_names):
    """Save encodings to file."""
    with open("facial_encodings.dat", "wb") as f:
        pickle.dump((face_encodings, face_names), f)


def train_from_directory(directory):
    """Train face recognition from a directory of images."""
    face_encodings, face_names = load_encodings()

    for image_path in paths.list_images(directory):
        image = cv2.imread(image_path)
        person_name = os.path.basename(os.path.dirname(image_path))

        result = train_face_recognition(image, person_name)
        if result:
            face_encodings.append(result[0])
            face_names.append(result[1])
            print(f"Trained on: {person_name}")

    save_encodings(face_encodings, face_names)
    speak("Training complete! Facial encodings saved to facial_encodings.dat")


# Example usage:
# Train from a directory


# Train on a single image
# image = cv2.imread("path_to_image.jpg")
# result = train_face_recognition(image, "Person's Name")
# if result:
#     face_encodings, face_names = load_encodings()
#     face_encodings.append(result[0])
#     face_names.append(result[1])
#     save_encodings(face_encodings, face_names)
#     print(f"Trained on new image for: {result[1]}")