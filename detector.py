import cv2
import numpy as np
import utils


def get_result_layer(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def detect(image, conf_threshold, classes, frame_id, video_path, nms_threshold=0.4):
    weight_path = "./yolo/yolov3.weights"
    config_path = "./yolo/yolov3.cfg"
    class_path = "./yolo/yolov3.txt"
    scale = 0.00392
    frame_width = image.shape[1]
    frame_height = image.shape[0]

    net = cv2.dnn.readNet(weight_path, config_path)
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_result_layer(net))

    class_ids = []
    confidences = []
    boxes = []

    # Read detectable classes
    with open(class_path, 'r') as f:
        detectable_classes = [line.strip() for line in f.readlines()]

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > conf_threshold:
                class_index = utils.get_index(classes, detectable_classes[class_id])
                if class_index is not None:
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    w = int(detection[2] * frame_width)
                    h = int(detection[3] * frame_height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(int(class_index))
                    confidences.append(float(confidence))
                    boxes.append((x, y, w, h))

    # Very expensive time consuming method
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    result = []
    for i in indexes:
        index = i[0]
        #                   class           confidence       current box
        result.append([class_ids[index], confidences[index], boxes[index]])
    return result
