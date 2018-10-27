import utils


def detect_obj_collisions(objects, collision_classes):
    pass


def detect_obj_area_collisions(objects, collision_areas):
    pass


def detect_collisions(objects, collision_classes, collision_areas):
    collisions = {}
    info = []
    obj_collisions, obj_collisions_info = detect_obj_collisions(objects, collision_classes)
    obj_area_collisions, obj_area_collisions_info = detect_obj_area_collisions(objects, collision_areas)
    collisions.update(obj_collisions)
    collisions.update(obj_area_collisions)
    info.extend(obj_collisions_info)
    info.extend(obj_area_collisions_info)
    return obj_collisions, info
