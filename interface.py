import cv2
import numpy as np
import collision

colors = {}


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


def draw_obj(image, objects):
    for obj in objects:
        x, y, x1, y1 = get_box(obj[3])
        obj_id = obj[0]
        obj_class = obj[1]
        class_conf = obj[2]
        obj_color = colors.get(obj[1], (0, 0, 0))

        draw_prediction(image, obj_id, obj_class, class_conf, obj_color, x, y)
        draw_box(image, obj_color, x, y, x1, y1)


def draw_collisions(image, objects):
    for obj in objects:
        shift = 2
        x, y, x1, y1 = get_box(obj[3])
        draw_box(image, (0, 0, 255), x - shift, y - shift, x1 + shift, y1 + shift)


def show(image, window_name='object detection'):
    cv2.imshow(window_name, image)


def init(classes):
    global colors
    for clazz in classes:
        colors.update({clazz: np.random.uniform(0, 255, 3)})


def close():
    cv2.destroyAllWindows()


def click_and_crop(event, x, y, flags, param):
    param[1][0] = x
    param[1][1] = y
    curr_coordinates = param[0]

    if event == cv2.EVENT_LBUTTONDOWN:
        curr_coordinates.append((x, y))
        param[1][2] = True

    if event == cv2.EVENT_RBUTTONDOWN:
        param[1][2] = False


def create_areas(frame, area_name):
    area_coordinates = []
    curr_coordinates = [0, 0, True]
    # load the image, clone it, and setup the mouse callback function
    image = frame.copy()
    window_name = "Select area " + area_name
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, click_and_crop, (area_coordinates, curr_coordinates))

    while True:
        if len(area_coordinates) > 1:
            cv2.line(image, area_coordinates[-2], area_coordinates[-1], (255, 0, 0), 5)

        image_copy = image.copy()
        if len(area_coordinates) > 0 and curr_coordinates[2]:
            cv2.line(image_copy, area_coordinates[-1], (curr_coordinates[0], curr_coordinates[1]), (255, 0, 0), 5)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        cv2.imshow(window_name, image_copy)
    cv2.destroyAllWindows()
    return [(area_name, ['person'], 1, collision.create_polygon(area_coordinates))]
