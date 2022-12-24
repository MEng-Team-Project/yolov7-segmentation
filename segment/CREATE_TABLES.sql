/* Standard Yolo Object Detections with class (COCO idx), bbox, conf */
CREATE TABLE IF NOT EXISTS detections(
    detection_id INTEGER PRIMARY KEY,
    frame        INTEGER NOT NULL,
    class_idx    FLOAT NOT NULL,
    x1           FLOAT NOT NULL,
    y1           FLOAT NOT NULL,
    x2           FLOAT NOT NULL,
    y2           FLOAT NOT NULL,
    confidence   FLOAT NOT NULL
);

/* Current objects being tracked by ClassySORT (Kalman Filter) */
CREATE TABLE IF NOT EXISTS tracked(
    tracked_id INTEGER PRIMARY KEY,
    frame      INTEGER NOT NULL,
    bbox_x1    FLOAT NOT NULL,
    bbox_y1    FLOAT NOT NULL,
    bbox_x2    FLOAT NOT NULL,
    bbox_y2    FLOAT NOT NULL,
    label      INTEGER NOT NULL,
    anchor_x   FLOAT NOT NULL,
    anchor_y   FLOAT NOT NULL
);

/* Routes inferred from ClassySORT (Kalman Filter) for entire duration per object */
CREATE TABLE IF NOT EXISTS route(
    sub_route_id INTEGER PRIMARY KEY,
    frame        INTEGER NOT NULL,
    route_idx    INTEGER NOT NULL,
    x1           FLOAT NOT NULL,
    y1           FLOAT NOT NULL,
    x2           FLOAT NOT NULL,
    y2           FLOAT NOT NULL
);