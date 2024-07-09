# Emotion Recognition Project

This project uses a pre-trained deep learning model to recognize and classify human emotions from real-time video input. The recognized emotions are saved into a CSV file with the time duration and probability of each detected emotion.

## Requirements

- Python 3.x
- Keras
- OpenCV
- Imutils
- Numpy

## Installation

1. Install the required libraries:

    ```bash
    pip install keras opencv-python imutils numpy
    ```

2. Ensure you have the required pre-trained models:

    - Haarcascade for face detection: `haarcascade_frontalface_default.xml`
    - Pre-trained emotion classification model: `_mini_XCEPTION.102-0.66.hdf5`

3. Ensure you have the `abcde.py` script in the same directory for running music recognition (if applicable).

## Usage

1. Run the script:

    ```bash
    python emotion_recognition.py
    ```

2. The program will activate your webcam and start detecting emotions in real-time. It will display two windows:
   - `facial_recognition`: Shows the video feed with detected faces and emotion labels.
   - `Probabilities`: Displays a bar graph with the probability of each emotion.

3. To stop the program, press `q`.

## File Descriptions

- `emotion_recognition.py`: Main script for real-time emotion recognition and CSV logging.
- `haarcascade_frontalface_default.xml`: Haarcascade model for face detection.
- `_mini_XCEPTION.102-0.66.hdf5`: Pre-trained model for emotion classification.
- `emotionsave.csv`: CSV file where the emotions detected are logged.
- `abcde.py`: Script for music recognition (optional).

## How It Works

1. **Face Detection**: The script uses Haarcascade to detect faces in the video feed.
2. **Emotion Classification**: Detected faces are preprocessed and passed through the pre-trained `_mini_XCEPTION` model to predict the emotion.
3. **Logging**: Detected emotions are saved to a CSV file with the start time, end time, emotion label, and probability.
4. **Display**: The video feed with detected faces and emotions is displayed in real-time, along with a probability bar graph.

## CSV Logging

The emotions detected are logged into a CSV file (`emotionsave.csv`) with the following columns:
- `Start Time`: The start time of the detected emotion.
- `End Time`: The end time of the detected emotion.
- `Emotion`: The detected emotion.
- `Probability`: The probability of the detected emotion.

## Customization

- **Emotion Model Path**: You can change the path of the emotion model by modifying the `emotion_model_path` variable.
- **CSV File Path**: You can change the path of the CSV file by modifying the `csv_file_path` variable.

## Note

Ensure your webcam is properly connected and accessible by OpenCV. If you encounter any issues, check the webcam permissions on your device.

## License

This project is licensed under the MIT License. Feel free to modify and distribute as needed.

---

Feel free to reach out if you have any questions or need further assistance.

Happy coding!
