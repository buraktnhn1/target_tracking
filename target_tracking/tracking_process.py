from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO('yolo11n.pt')
cap = cv2.VideoCapture('car_tracking_sim.avi')

kf = cv2.KalmanFilter(4 , 2)
kf.measurementMatrix =  np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
kf.transitionMatrix = np.array([[1, 0, 1, 0], 
                                [0, 1, 0, 1],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]], np.float32)
kf.processNoiseCov = np.eye(4, dtype = np.float32) * 0.03

initialized = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Video finished.")
        break

    results = model.predict(frame, classes = [2], conf = 0.1, verbose = False)

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0]) 
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        if not initialized:
            kf.statePre = np.array([[center_x], [center_y], [0], [0]], np.float32)
            initialized = True     

        kf.predict()

        measured = np.array([[np.float32(center_x)], [np.float32(center_y)]])
        estimated = kf.correct(measured)

        est_x = int(estimated[0, 0])
        est_y = int(estimated[1, 0])
        cv2.circle(frame, (est_x, est_y), 10, (255, 0, 0), 2)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if (x2 - x1) < 5 or (y2 - y1) < 5:
            cv2.putText(frame, "TARGET LOST!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Kalman and YOLO tracking', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break    

cap.release()
cv2.destroyAllWindows()