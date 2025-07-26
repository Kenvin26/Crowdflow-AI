import numpy as np
from sklearn.ensemble import IsolationForest

class BehaviorAnalyzer:
    def __init__(self):
        self.model = IsolationForest(contamination=0.01)

    def fit(self, features):
        self.model.fit(features)

    def detect_anomalies(self, features):
        return self.model.predict(features)  # -1: anomaly, 1: normal

# Feature extraction example: speed, direction change, dwell time
# features = np.array([[speed, direction_var, dwell_time], ...])
# analyzer = BehaviorAnalyzer()
# analyzer.fit(features)
# anomalies = analyzer.detect_anomalies(features) 