import numpy as np
from shapely.geometry import Point, Polygon

class FlowCounter:
    def __init__(self, roi_polygon):
        self.roi = Polygon(roi_polygon)  # [(x,y), ...]
        self.prev_positions = {}         # id -> (x,y)
        self.in_count = 0
        self.out_count = 0

    def update(self, tracked_points):
        # tracked_points = {id: (x,y)}
        for oid, pt in tracked_points.items():
            p = Point(pt[0], pt[1])
            prev = self.prev_positions.get(oid)
            self.prev_positions[oid] = pt
            if prev is None:
                continue
            prev_inside = self.roi.contains(Point(prev[0], prev[1]))
            now_inside  = self.roi.contains(p)
            if prev_inside and not now_inside:
                self.out_count += 1
            elif not prev_inside and now_inside:
                self.in_count += 1

        return self.in_count, self.out_count 