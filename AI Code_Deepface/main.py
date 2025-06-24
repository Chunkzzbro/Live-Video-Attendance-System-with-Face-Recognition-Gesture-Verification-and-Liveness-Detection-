import cv2
import numpy as np
import datetime
import os
import tensorflow as tf
from deepface import DeepFace
import xlwings as xw

# Initialize variables
cap = cv2.VideoCapture(0)
running = True
students = []

# Initialize the Excel workbook
workbook = xw.Book('attendance.xlsx')

model = 'liveness.model'
model = tf.keras.models.load_model(model)

# Initialize the starting day
t0 = datetime.datetime.now().day  # Set t0 to the current day at the start
s = 2  # Row where the student details will be saved

while running:
    moment = datetime.datetime.now()
    hour = moment.hour
    minute = moment.minute
    day = moment.day
    month = moment.month
    year = moment.year

    date = f"{day}-{month}-{year}"
    time = f"{hour}:{minute}"

    # Check if the day has changed
    if day != t0:
        t0 = day
        worksheet = workbook.sheets.add(date)
        worksheet.range('A1').value = 'STUDENT'
        worksheet.range('B1').value = 'DATE'
        worksheet.range('C1').value = 'TIME'
        s = 2

    state, frame = cap.read()
    if not state:
        break

    # Perform face recognition
    res = DeepFace.find(frame, db_path='./ImagesAttendance/', enforce_detection=False, model_name='VGG-Face')

    if len(res[0]['identity']) > 0:
        # Example file path
        file_path = res[0]['identity'][0]

        # Extracting the name without the extension
        name = os.path.splitext(os.path.basename(file_path))[0]

        # Get the face coordinates
        xmin = int(res[0]['source_x'][0])
        ymin = int(res[0]['source_y'][0])
        w = res[0]['source_w'][0]
        h = res[0]['source_h'][0]
        xmax = int(xmin + w)
        ymax = int(ymin + h)

        # Liveness detection
        img = frame[ymin:ymax, xmin:xmax]
        img = cv2.resize(img, (32, 32))
        img = img.astype('float') / 255.0
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = np.expand_dims(img, axis=0)

        liveness = model.predict(img)
        liveness = liveness[0].argmax()

        if liveness == 1:
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.rectangle(frame, (xmin, ymin - 25), (xmax, ymin), (255, 255, 255), -1)
            cv2.putText(frame, name, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.putText(frame, f"Date: {date}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Time: {time}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            # Log the attendance automatically
            if name not in students:
                worksheet.range(f'A{s}').value = name
                worksheet.range(f'B{s}').value = date
                worksheet.range(f'C{s}').value = time
                students.append(name)
                s += 1

        else:
            cv2.putText(frame, "Liveness test failed", (xmin, ymin - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the frame with OpenCV
    cv2.imshow('Attendance System', frame)

    # Check for the exit condition (press 'q' to exit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()