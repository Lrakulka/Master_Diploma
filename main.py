import cv2
import detector_mock as detector
import tracker
import synchronize
import collision
import interface


def main(video_path):
    # Detector configs
    per_frame = 10
    series_frame = 1
    detector_confidence_threshold = 0.5
    # Load detectable classes
    with open("./yolo/yolov3.txt", 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    classes = ['person', 'car']
    detect_time = False

    # Tracker configs
    frame_id = 0
    round_frame = 0

    # Synchronizer configs
    fail_synchronize_threshold = series_frame * 3

    interface.init(classes)
    cap = cv2.VideoCapture(video_path)
    r, frame = cap.read()
    # Create collision areas
    areas = interface.create_areas(frame)
    while True:
        # Exit if Q pressed or end of file
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q') or r is False:
            break

        # Detect series
        if round_frame > 0:
            round_frame -= 1
            detect_time = True

        if frame_id % per_frame == 0:
            round_frame = series_frame
            detect_time = True

        # Get tracked objects
        tracked_objects = tracker.get_tracked(frame)

        # Detect objects and match them with tracked one
        if detect_time is True:
            detected_objects = detector.detect(frame, detector_confidence_threshold, classes, frame_id, video_path)
            # TODO: remove frame
            synchronized_objects = synchronize\
                .synchronize_objects(detected_objects, tracked_objects, fail_synchronize_threshold, frame)
            tracker.set_tracked(frame, synchronized_objects)
            tracked_objects = synchronized_objects
            detect_time = False

        collisions_objects, info, triggers = collision.detect_collisions(tracked_objects, areas, frame_id)

        interface.draw_obj(frame, tracked_objects)
        interface.draw_collisions(frame, collisions_objects)
        interface.draw_collisions_info(frame, info)
        interface.draw_triggers(frame, triggers)
        interface.show(frame)

        r, frame = cap.read()
        frame_id += 1
    interface.close()


if __name__ == '__main__':
    main("./video/fly_away.mp4")
