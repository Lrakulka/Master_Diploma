import cv2
import numpy as np
from random import randint
import pickle
import os


def get_output_layers(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


if __name__ == '__main__':
    videos = ['bike_strike']
    videosPath = './video/'
    classPath = 'yolo/yolov3.txt'
    weightPath = './yolo/yolov3.weights'
    configPath = './yolo/yolov3.cfg'
    mockPath = 'E:/test_diploma/'

    conf_threshold = 0.5
    nms_threshold = 0.4

    for video in videos:
        directory = 'E:/test_diploma/' + video
        if not os.path.exists(directory):
            os.makedirs(directory)

        cap = cv2.VideoCapture(videosPath + video + '.mp4')
        t = 0
        p = str(randint(0, 100))

        while True:
            r, image = cap.read()
            if image is None:
                break

            Width = image.shape[1]
            Height = image.shape[0]
            scale = 0.00392

            classes = None

            with open(classPath, 'r') as f:
                classes = [line.strip() for line in f.readlines()]

            COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

            net = cv2.dnn.readNet(weightPath, configPath)

            blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

            net.setInput(blob)

            outs = net.forward(get_output_layers(net))

            class_ids = []
            confidences = []
            boxes = []

            t = t + 1
            f = open(mockPath + video + '/demofile' + str(t), 'wb')
            serial_grades = pickle.dumps(outs)
            f.write(serial_grades)
            f.close()

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > conf_threshold:
                        center_x = int(detection[0] * Width)
                        center_y = int(detection[1] * Height)
                        w = int(detection[2] * Width)
                        h = int(detection[3] * Height)
                        x = center_x - w / 2
                        y = center_y - h / 2
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])

            indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

            for i in indices:
                i = i[0]
                box = boxes[i]
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
                draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

            cv2.imshow(video + ' detection', image)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
