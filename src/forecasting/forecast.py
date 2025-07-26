import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def train_and_forecast(csv_path="data/outputs/metrics.csv", horizon=6):
    """
    horizon = number of future intervals (if you log every 5 mins, 6 -> next 30 mins)
    """
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp")
    # aggregate across cameras if multiple
    agg = df.groupby("timestamp")["active"].sum().asfreq("5T").interpolate()

    model = SARIMAX(agg, order=(1,1,1), seasonal_order=(0,0,0,0))
    res = model.fit(disp=False)
    fc = res.get_forecast(steps=horizon)
    pred = fc.predicted_mean
    conf = fc.conf_int()
    return pred, conf 