import cv2
import numpy as np

colors = None


def draw_prediction(img, obj_id, name, confidence, color, x, y):
    cv2.putText(img, name, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.putText(img, percent(confidence), (x - 10, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.putText(img, "ID=" + str(obj_id), (x - 10, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def draw_box(img, color, x, y, x1, y1):
    cv2.rectangle(img, (x, y), (x1, y1), color, 2)


def percent(confidence):
    return str(np.round(confidence * 100)) + "%"


def get_box(box):
    x = round(box[0])
    y = round(box[1])
    return x, y, round(x + box[2]), round(y + box[3])


def draw_obj(image, objects, classes):
    global colors
    if colors is None:
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
    for obj in objects:
        x, y, x1, y1 = get_box(obj[3])
        obj_id = obj[0]
        obj_class = classes[obj[1]]
        class_conf = obj[2]
        obj_color = colors[obj[1]]

        draw_prediction(image, obj_id, obj_class, class_conf, obj_color, x, y)
        draw_box(image, obj_color, x, y, x1, y1)


def draw_collisions(image, objects):
    for obj in objects:
        shift = 2
        x, y, x1, y1 = get_box(obj[3])
        draw_box(image, (0, 0, 255), x - shift, y - shift, x1 + shift, y1 + shift)


def show(image, window_name='object detection'):
    cv2.imshow(window_name, image)


def close():
    cv2.destroyAllWindows()
