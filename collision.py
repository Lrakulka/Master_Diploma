collision_map = {}
MAP_CLEAN_THRESHOLD = 10


def get_trigger_points(box):
    triggers = [(box[0], box[1])]
    return triggers


def get_collision_number(key, area_time_threshold):
    value = collision_map.get(key, (0, 0))
    collision_number = value[0]
    last_update_frame = value[1]
    if area_time_threshold > last_update_frame * MAP_CLEAN_THRESHOLD:
        return 0
    return collision_number


def detect_obj_area_collisions(objects, collision_areas, frame_id):
    collisions = set()
    info = []
    for area in collision_areas:
        area_name = area[0]
        area_collision_classes = area[1]
        area_time_threshold = area[2]
        area_polygon = area[3]
        for obj in objects:
            obj_id = obj[0]
            obj_class = obj[1]
            obj_triggers = get_trigger_points(obj[3])
            for trigger in obj_triggers:
                if obj_class in area_collision_classes and is_in_polygon(area_polygon, trigger[0], trigger[1]):
                    collision_number = get_collision_number((area_name, obj_id), area_time_threshold)
                    collision_map.update({(area_name, obj_id): (collision_number + 1, frame_id)})
                    if area_time_threshold < collision_number + 1:
                        collisions.add(obj)
                        info.append('Collision ' + obj_class + ' Id=' + str(obj_id) + ' with area id=' + area_name)
    return collisions, info


def detect_collisions(objects, collision_areas, frame_id):
    collisions = set()
    info = []
    obj_area_collisions, obj_area_collisions_info = detect_obj_area_collisions(objects, collision_areas, frame_id)
    # TODO: Other collision detectors
    collisions.update(obj_area_collisions)
    info.extend(obj_area_collisions_info)
    return collisions, info


# Thank you http://alienryderflex.com/polygon/
def create_polygon(poly_corners):
    j = -1
    constant = [0] * len(poly_corners)
    multiple = [0] * len(poly_corners)
    polygon = []
    for i in range(0, len(poly_corners)):
        poly_x0 = poly_corners[i][0]
        poly_y0 = poly_corners[i][1]
        poly_x1 = poly_corners[j][0]
        poly_y1 = poly_corners[j][1]
        if poly_y1 == poly_y0:
            constant[i] = poly_x0
            multiple[i] = 0
        else:
            constant[i] = poly_x0 - (poly_y0 * poly_x1) / (poly_y1 - poly_y0) \
                          + (poly_y0 * poly_x0) / (poly_y1 - poly_y0)
            multiple[i] = (poly_x1 - poly_x0) / (poly_y1 - poly_y0)
        j = i
        polygon.append(((poly_x0, poly_y0), constant[i], multiple[i]))
    return polygon


def is_in_polygon(polygon, x, y):
    j = -1
    odd_nodes = False
    for i in range(0, len(polygon)):
        poly_x0, poly_y0 = polygon[i][0]
        poly_x1, poly_y1 = polygon[j][0]
        constant = polygon[i][1]
        multiple = polygon[i][2]
        if poly_y0 < y <= poly_y1 or poly_y1 < y <= poly_y0:
            odd_nodes ^= ((y * multiple + constant) < x)
        j = i
    return odd_nodes
