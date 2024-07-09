from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import csv
from datetime import datetime
import subprocess

# Parameters for loading data and images
detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'

# Hyperparameters for bounding boxes shape
num_classes = 5
img_rows, img_cols = 64, 64
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

# Initialize variables for tracking the longest non-neutral emotion
longest_non_neutral_emotion = ''
longest_non_neutral_emotion_duration = 0
current_emotion_start_time = datetime.now()

# CSV file setup
csv_file_path = 'emotionsave.csv'
csv_columns = ['Start Time', 'End Time', 'Emotion', 'Probability']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    csv_writer.writeheader()

# OpenCV setup
face_detection = cv2.CascadeClassifier(detection_model_path)
cv2.namedWindow('facial_recognition')
camera = cv2.VideoCapture(0)

preds = []

while True:
    frame = camera.read()[1]
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    canvas = np.zeros((650, 650, 3), dtype="uint8")
    frameClone = frame.copy()

    # Initialize emotion_probability and label
    emotion_probability = 0
    label = 'neutral'

    if len(faces) > 0:
        faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces

        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (img_rows, img_cols))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        # Update preds inside the loop
        preds = emotion_classifier.predict(roi)[0]
        preds_np = np.array(preds)  # Convert to NumPy array
        emotion_probability = np.max(preds_np)
        label = EMOTIONS[preds_np.argmax()]

        if label != 'neutral':
            current_emotion_duration = (datetime.now() - current_emotion_start_time).total_seconds()

            if current_emotion_duration > longest_non_neutral_emotion_duration:
                longest_non_neutral_emotion = label
                current_emotion_duration = int((datetime.now() - current_emotion_start_time).total_seconds())


                with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                    csv_writer.writerow({
                        'Start Time': current_emotion_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'End Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': longest_non_neutral_emotion,
                        'Probability': emotion_probability
                    })

                current_emotion_start_time = datetime.now()

    for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
        text = "{}: {:.2f}%".format(emotion, prob * 100)
        w = int(prob * 300)
        cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
        cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        cv2.putText(frameClone, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)

    cv2.imshow('facial_recognition', frameClone)
    cv2.imshow("Probabilities", canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

music_recognition_script = 'abcde.py'  # Replace with the actual filename
subprocess.run(['python', music_recognition_script])