import numpy as np
import cv2

class HomographyCalibrator:
    def __init__(self, image_points=None, world_points=None):
        self.image_points = image_points  # List of (x, y) in image
        self.world_points = world_points  # List of (X, Y) in meters
        self.H = None
        if image_points is not None and world_points is not None:
            self.compute_homography()

    def compute_homography(self):
        if self.image_points is not None and self.world_points is not None:
            self.H, _ = cv2.findHomography(np.array(self.image_points), np.array(self.world_points))
        return self.H

    def image_to_world(self, pts):
        # pts: Nx2 array of image points
        pts = np.array(pts, dtype=np.float32)
        pts = np.concatenate([pts, np.ones((pts.shape[0], 1))], axis=1)
        mapped = (self.H @ pts.T).T
        mapped = mapped[:, :2] / mapped[:, 2:]
        return mapped

    def world_to_image(self, pts):
        # pts: Nx2 array of world points
        H_inv = np.linalg.inv(self.H)
        pts = np.array(pts, dtype=np.float32)
        pts = np.concatenate([pts, np.ones((pts.shape[0], 1))], axis=1)
        mapped = (H_inv @ pts.T).T
        mapped = mapped[:, :2] / mapped[:, 2:]
        return mapped

# Example usage:
# image_pts = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
# world_pts = [(X1, Y1), (X2, Y2), (X3, Y3), (X4, Y4)]
# calibrator = HomographyCalibrator(image_pts, world_pts)
# ground_pts = calibrator.image_to_world([(x, y)]) 