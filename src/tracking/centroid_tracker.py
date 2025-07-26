import numpy as np
from scipy.spatial.distance import cdist

class CentroidTracker:
    def __init__(self, max_disappeared=30, max_distance=80):
        self.next_id = 0
        self.tracks = {}           # id -> centroid
        self.disappeared = {}      # id -> frames missed
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance

    def update(self, boxes):
        if len(boxes) == 0:
            # mark all as disappeared
            to_delete = []
            for object_id in self.disappeared:
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    to_delete.append(object_id)
            for oid in to_delete:
                del self.tracks[oid]
                del self.disappeared[oid]
            return self.tracks

        input_centroids = np.array([( (b[0]+b[2]) / 2, (b[1]+b[3]) / 2 ) for b in boxes])

        if len(self.tracks) == 0:
            for i in range(len(input_centroids)):
                self.tracks[self.next_id] = input_centroids[i]
                self.disappeared[self.next_id] = 0
                self.next_id += 1
        else:
            object_ids = list(self.tracks.keys())
            object_centroids = np.array(list(self.tracks.values()))
            D = cdist(object_centroids, input_centroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows, used_cols = set(), set()
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                if D[row, col] > self.max_distance:
                    continue
                object_id = object_ids[row]
                self.tracks[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(D.shape[0])).difference(used_rows)
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    del self.tracks[object_id]
                    del self.disappeared[object_id]

            for col in set(range(input_centroids.shape[0])).difference(used_cols):
                self.tracks[self.next_id] = input_centroids[col]
                self.disappeared[self.next_id] = 0
                self.next_id += 1

        return self.tracks 