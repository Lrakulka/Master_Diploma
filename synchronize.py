import interface

fail_synchronize_ids = {}
last_id = 0


def find_tracked(detected_obj, tracked_objects):
    e = 5000
    tracked_obj = None
    dist = float("inf")
    # Could be done in O(NlogN)
    for tracked_object in tracked_objects:
        curr_dist = (detected_obj[2][0] - tracked_object[3][0])**2 + (detected_obj[2][1] - tracked_object[3][1])**2
        if detected_obj[0] == tracked_object[1] and curr_dist < dist:
            tracked_obj = tracked_object
            dist = curr_dist
    if dist > e:
        return None
    return tracked_obj


def synchronize_objects(detected_objects, tracked_objects, fail_synchronize_threshold, frame):
    global fail_synchronize_ids, last_id
    synchronized_objects = []

    for detected_obj in detected_objects:
        tracked_object = find_tracked(detected_obj, tracked_objects)

       # if tracked_object is not None:
       #     interface.draw(frame, [[tracked_object[0], 2, detected_obj[1], detected_obj[2]], tracked_object], ['person', 'car', 'synth'], 'synch')
        #else: interface.draw(frame, [[3000, 2, detected_obj[1], detected_obj[2]]], ['person', 'car', 'synth'], 'synch')

        if tracked_object is not None:
            # Update tracked obj with detected
            detected_id = tracked_object[0]
            synchronized_objects.append([detected_id, detected_obj[0], detected_obj[1], detected_obj[2]])

            tracked_objects.remove(tracked_object)
            fail_synchronize_ids.update({detected_id: 0})
        else:
            # Add new detected obj
            last_id += 1
            synchronized_objects.append([last_id, detected_obj[0], detected_obj[1], detected_obj[2]])

    for tracked_obj in tracked_objects:
        obj_id = tracked_obj[0]
        synchronize_attempts = fail_synchronize_ids.get(obj_id, 0)
        if synchronize_attempts < fail_synchronize_threshold:
            # Add not old tracked obj
            synchronized_objects.append([obj_id, tracked_obj[1], tracked_obj[2], tracked_obj[3]])
            fail_synchronize_ids.update({obj_id: synchronize_attempts + 1})
        else:
            #interface.draw(frame, [tracked_obj], ['person', 'car', 'synth'], ' syncth fail')
            fail_synchronize_ids.pop(obj_id)

    return synchronized_objects
