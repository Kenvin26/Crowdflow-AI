import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Optionally, use xgboost or lightgbm if available
try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False


def create_features(df, lags=6):
    df = df.copy()
    df['hour'] = df['timestamp'].dt.hour
    df['weekday'] = df['timestamp'].dt.weekday
    for i in range(1, lags+1):
        df[f'lag_{i}'] = df['active'].shift(i)
    df = df.dropna()
    return df

def train_and_forecast_ml(csv_path="data/outputs/metrics.csv", horizon=6, lags=6):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp")
    df = create_features(df, lags=lags)
    X = df.drop(["timestamp", "active"], axis=1)
    y = df["active"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    if XGB_AVAILABLE:
        model = xgb.XGBRegressor(objective="reg:squarederror")
    else:
        model = GradientBoostingRegressor()
    model.fit(X_train, y_train)

    # Forecast next horizon steps
    last_row = X.iloc[[-1]].copy()
    preds = []
    for _ in range(horizon):
        pred = model.predict(last_row)[0]
        preds.append(pred)
        # roll lags
        for i in range(lags, 1, -1):
            last_row[f'lag_{i}'] = last_row[f'lag_{i-1}']
        last_row['lag_1'] = pred
        # Optionally update hour/weekday
        last_row['hour'] = (last_row['hour'] + 1) % 24
        last_row['weekday'] = (last_row['weekday'] + (last_row['hour'] == 0)) % 7

    # Probabilistic: use model's std dev or quantiles if available (placeholder)
    pred_arr = np.array(preds)
    conf_int = np.vstack([pred_arr - pred_arr.std(), pred_arr + pred_arr.std()]).T
    return preds, conf_int 