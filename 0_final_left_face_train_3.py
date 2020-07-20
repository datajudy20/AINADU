import cv2
import numpy as np

model = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = 'deploy.prototxt'

cap = cv2.VideoCapture(0)   # camera device index

if not cap.isOpened():
    print('Camera open failed!')
    exit()


net = cv2.dnn.readNet(model, config)

if net.empty():
    print('Net open failed!')
    exit()


count = 1
while True:
    _, frame = cap.read()

    if frame is None:
        break

    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    detect = net.forward()

    (h, w) = frame.shape[:2]
    detect = detect[0, 0, :, :]

    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.7:
            break

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))
        face = cv2.resize(frame[y1:y2,x1:x2],(200,200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        name = 'f_images/right/kim' + str(count) + '.jpg'

        cv2.imwrite(name, face)
        count += 1

        label = 'Face: %4.3f' % confidence
        label = 'show your right face'
        cv2.putText(frame, label, (x1, y1 - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if count == 100:
        break

    # press ESC key
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
