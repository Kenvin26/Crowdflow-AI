import numpy as np
from filterpy.kalman import KalmanFilter
from lap import lapjv

class Track:
    def __init__(self, bbox, track_id):
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.x[:4] = bbox.reshape((4, 1))
        self.time_since_update = 0
        self.id = track_id
        self.hits = 1
        self.hit_streak = 1
        self.age = 0
        self.history = []

    def update(self, bbox):
        self.kf.update(bbox)
        self.time_since_update = 0
        self.hits += 1
        self.hit_streak += 1

    def predict(self):
        self.kf.predict()
        self.age += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        self.history.append(self.kf.x[:4])
        return self.kf.x[:4]

    def get_state(self):
        return self.kf.x[:4]

class OCSort:
    def __init__(self, max_age=30, min_hits=3, iou_threshold=0.3):
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.tracks = []
        self.next_id = 0

    def update(self, detections):
        # Predict new locations for all tracks
        for t in self.tracks:
            t.predict()

        # Associate detections to tracks
        if len(self.tracks) == 0:
            for d in detections:
                self.tracks.append(Track(d, self.next_id))
                self.next_id += 1
            return {t.id: ((t.get_state()[0]+t.get_state()[2])/2, (t.get_state()[1]+t.get_state()[3])/2) for t in self.tracks}

        track_states = np.array([t.get_state() for t in self.tracks])
        if len(detections) == 0:
            matches = np.empty((0,2), dtype=int)
            unmatched_tracks = np.arange(len(self.tracks))
            unmatched_detections = np.empty((0), dtype=int)
        else:
            iou_matrix = self._iou_batch(track_states, detections)
            row_ind, col_ind, _ = lapjv(-iou_matrix, extend_cost=True)
            matches = np.array([[r, c] for r, c in enumerate(col_ind) if c >= 0 and iou_matrix[r, c] > self.iou_threshold])
            unmatched_tracks = np.setdiff1d(np.arange(len(self.tracks)), matches[:,0]) if matches.size else np.arange(len(self.tracks))
            unmatched_detections = np.setdiff1d(np.arange(len(detections)), matches[:,1]) if matches.size else np.arange(len(detections))

        # Update matched tracks
        for t, d in matches:
            self.tracks[t].update(detections[d])

        # Create new tracks for unmatched detections
        for d in unmatched_detections:
            self.tracks.append(Track(detections[d], self.next_id))
            self.next_id += 1

        # Remove dead tracks
        self.tracks = [t for t in self.tracks if t.time_since_update <= self.max_age]

        # Return dict of id -> centroid
        return {t.id: ((t.get_state()[0]+t.get_state()[2])/2, (t.get_state()[1]+t.get_state()[3])/2) for t in self.tracks if t.hits >= self.min_hits or t.time_since_update == 0}

    def _iou_batch(self, boxes1, boxes2):
        # boxes: [N,4] (x1,y1,x2,y2)
        iou = np.zeros((len(boxes1), len(boxes2)), dtype=np.float32)
        for i, a in enumerate(boxes1):
            for j, b in enumerate(boxes2):
                iou[i, j] = self._iou(a, b)
        return iou

    def _iou(self, a, b):
        x1 = max(a[0], b[0])
        y1 = max(a[1], b[1])
        x2 = min(a[2], b[2])
        y2 = min(a[3], b[3])
        inter = max(0, x2-x1) * max(0, y2-y1)
        area_a = (a[2]-a[0]) * (a[3]-a[1])
        area_b = (b[2]-b[0]) * (b[3]-b[1])
        union = area_a + area_b - inter
        return inter / union if union > 0 else 0 