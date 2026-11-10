import requests, pandas as pd
from pathlib import Path

P = {"latitude":54.7388,"longitude":55.9721,"start_date":"2026-01-01","end_date":"2026-11-04","timezone":"Asia/Yekaterinburg",
     "daily":"temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,wind_speed_10m_max,weather_code"}

r = requests.get("https://archive-api.open-meteo.com/v1/archive", params=P, timeout=30)
r.raise_for_status()
df = pd.DataFrame(r.json()["daily"])
df["time"] = pd.to_datetime(df["time"])
df = df.rename(columns={"time":"date"}).set_index("date").sort_index()
out = Path("data/raw/ufa_2026.csv")
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out)
print("OK", len(df), list(df.columns))
