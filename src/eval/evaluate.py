import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_counts(gt_csv, pred_csv):
    gt = pd.read_csv(gt_csv, parse_dates=["timestamp"])
    pred = pd.read_csv(pred_csv, parse_dates=["timestamp"])
    merged = pd.merge(gt, pred, on="timestamp", suffixes=("_gt", "_pred"))
    mae = mean_absolute_error(merged["active_gt"], merged["active_pred"])
    rmse = mean_squared_error(merged["active_gt"], merged["active_pred"] , squared=False)
    return {"MAE": mae, "RMSE": rmse}

# For MOTA, IDF1, ID switches, you need per-frame ID assignments (not just counts)
# Placeholder for future implementation

def evaluate_tracking(gt_ids, pred_ids):
    # gt_ids, pred_ids: list of sets of IDs per frame
    # Compute MOTA, IDF1, ID switches (requires Hungarian matching)
    pass

if __name__ == "__main__":
    # Example usage
    print(evaluate_counts("ground_truth.csv", "predictions.csv")) 