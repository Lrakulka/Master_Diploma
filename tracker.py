import cv2

trackers = {}

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[7]


def get_tracker():
    track = None
    if int(minor_ver) < 3:
        track = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            track = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            track = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            track = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            track = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            track = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            track = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            track = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            track = cv2.TrackerCSRT_create()
    return track


def set_tracked(frame, objects):
    global trackers
    trackers.clear()
    for obj in objects:
        obj_id = obj[0]
        tracker = get_tracker()
        try:
            tracker.init(frame, obj[3])
            trackers.update({obj_id: [obj, tracker]})
        except:
            print(obj)


def get_tracked(frame):
    tracked_obj = []
    remove_obj = []
    for obj_id, value in trackers.items():
        tracker = value[1]
        # Update tracker
        ok, bbox = tracker.update(frame)

        if ok:
            # Tracking success
            #                    ID      class      confidence  current  prev box
            tracked_obj.append([obj_id, value[0][1], value[0][2], bbox, value[0][3]])
        else:
            # Tracking failure
            remove_obj.append(obj_id)
    for obj_id in remove_obj:
        trackers.pop(obj_id, None)

    return tracked_obj
