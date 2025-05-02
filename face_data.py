import cv2
import numpy as np 
import os

cap = cv2.VideoCapture(0)

script_dir = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_alt.xml')
dataset_path = os.path.join(script_dir, "face_dataset")
face_cascade = cv2.CascadeClassifier(cascade_path)

skip = 0
face_data = []

file_name = input("Enter the name of person : ")

def enhance_lighting(gray_img):
    """ Apply histogram equalization to improve lighting in grayscale image """
    return cv2.equalizeHist(gray_img)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = enhance_lighting(gray_frame)  # <-- lighting correction here

    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    if len(faces) == 0:
        cv2.imshow("faces", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        continue

    faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
    skip += 1

    for face in faces[:1]:
        x, y, w, h = face
        offset = 10
        face_offset = frame[y-offset:y+h+offset, x-offset:x+w+offset]
        face_gray = cv2.cvtColor(face_offset, cv2.COLOR_BGR2GRAY)
        face_gray = enhance_lighting(face_gray)  # <-- lighting fix for saved sample
        face_selection = cv2.resize(face_gray, (100, 100))

        if skip % 2 == 0:
            face_data.append(face_selection)
            print(f"Captured sample: {len(face_data)}")

        # Show face and full frame
        cv2.imshow("face", face_selection)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Add sample counter on the main window
    cv2.putText(frame, f"Samples: {len(face_data)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("faces", frame)

    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):
        break

    if len(face_data) >= 200:
        print("100 samples collected. Exiting...")
        break

# Save dataset
face_data = np.array(face_data).reshape((len(face_data), -1))
np.save(os.path.join(dataset_path, file_name), face_data)
print(f"Dataset saved at: {dataset_path + '/' + file_name}.npy")

cap.release()
cv2.destroyAllWindows()
