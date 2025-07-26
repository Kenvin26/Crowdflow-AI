import pandas as pd
import yaml
import time

# Placeholder for Telegram bot integration
def send_telegram_alert(message, token, chat_id):
    # You can use python-telegram-bot or requests to send messages
    print(f"[TELEGRAM ALERT] {message}")
    # Example: requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": message})


def check_alerts(df, cfg, telegram_cfg=None):
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    alerts = []
    if last["active"] > cfg["alerts"]["crowd_threshold"]:
        alerts.append("HIGH_CROWD")
    growth = (last["active"] - prev["active"]) / max(prev["active"], 1)
    if growth > cfg["alerts"]["growth_rate_threshold"]:
        alerts.append("SURGE")
    # Add forecast breach, etc.
    if alerts and telegram_cfg:
        for alert in alerts:
            send_telegram_alert(f"Alert: {alert} at {last['timestamp']}", telegram_cfg["token"], telegram_cfg["chat_id"])
    return alerts

# Example usage:
# df = pd.read_csv("data/outputs/metrics.csv")
# cfg = yaml.safe_load(open("src/config.yaml"))
# telegram_cfg = {"token": "<bot_token>", "chat_id": "<chat_id>"}
# check_alerts(df, cfg, telegram_cfg) 