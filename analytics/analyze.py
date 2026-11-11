import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


FIG = Path("analytics/figures")
FIG.mkdir(parents=True, exist_ok=True)
df = pd.read_csv("data/raw/ufa_2026.csv", parse_dates=["date"], index_col="date").sort_index()
df = df.ffill().dropna()
print(df.shape)
print(df.info())
print(df.describe())

df['temp_diff'] = df["apparent_temperature_max"] - df["temperature_2m_max"]
corr = np.corrcoef(df["temperature_2m_max"],df["wind_speed_10m_max"])[0,1]
mean_abs_diff = df["temp_diff"].abs().mean()
wet_days = (df["precipitation_sum"] > 0).mean() * 100
cold_days = (df["temperature_2m_max"] < 5).mean() * 100

df["month"] = df.index.month
full = df[df.index.month <= 10]
plt.figure(figsize=(12, 5))
plt.plot(df.index, df["temperature_2m_max"], label="max fact temp", color="red")
plt.plot(df.index, df["temperature_2m_min"], label="min fact temp", color="blue")
plt.plot(df.index, df["apparent_temperature_max"], label="max apparent temp",color="orange", linestyle="--")
plt.title("Температура воздуха в Уфе, 2026")
plt.xlabel("Дата")
plt.ylabel("Температура, °C")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig(FIG / "01_temperature.png", dpi=150)
plt.show()
plt.close()

plt.figure(figsize=(12, 5))
plt.bar(df.index, df["temp_diff"], color="blue",width=1)
plt.axhline(0, color="black", linewidth=0.8)
plt.title("Разница ощущаемой и фактической макс температуры, Уфа 2026")
plt.xlabel("Дата")
plt.ylabel("Разница, °C")
plt.grid()
plt.tight_layout()
plt.savefig(FIG / "02_temp_diff.png", dpi=150)
plt.show()
plt.close()

plt.figure(figsize=(12, 5))
sns.boxplot(data=full, x="month", y="temperature_2m_max", hue="month", palette="coolwarm", legend=False)
plt.title("Распределение фактической максимальной температуры по месяцам, Уфа 2026")
plt.xlabel("Месяц")
plt.ylabel("Температура, °C")
plt.xticks(range(10), ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт"])
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(FIG / "03_boxplot_temp.png", dpi=150)
plt.show()
plt.close()

pivot = full.pivot_table(values="temperature_2m_max", index=full.index.day, columns=full.index.month)
plt.figure(figsize=(10, 8))
sns.heatmap(pivot, cmap="coolwarm", cbar_kws={"label": "Температура, °C"})
plt.title("Макс температура по дням и месяцам, Уфа 2026")
plt.xlabel("Месяц")
plt.ylabel("День")
plt.xticks(np.arange(10) + 0.5, ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт"], rotation=0)
plt.tight_layout()
plt.savefig(FIG / "04_heatmap.png", dpi=150)
plt.show()
plt.close()

plt.figure(figsize=(10, 5))
sns.histplot(df["precipitation_sum"], bins=30, kde=True, color="green")
plt.title("Распределение осадков за сутки, Уфа 2026")
plt.xlabel("Осадки, мм")
plt.ylabel("Кол-во дней")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(FIG / "05_precip.png", dpi=150)
plt.show()
plt.close()

def wmo(code):
    if code == 0: return "Ясно"
    if code <= 3: return "Облачно"
    if code in (45, 48): return "Туман"
    if 51 <= code <= 57: return "Морось"
    if 61 <= code <= 67 or 80 <= code <= 82: return "Дождь"
    if 71 <= code <= 77 or 85 <= code <= 86: return "Снег"
    return "Гроза"

df["condition"] = df["weather_code"].apply(wmo)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="wind_speed_10m_max", y="temperature_2m_max", hue="condition", palette="tab10", alpha=0.7)
plt.title(f"Ветер и температура (r = {corr:.2f}), Уфа 2026")
plt.xlabel("Макс ветер, км/ч")
plt.ylabel("Макс температура, °C")
plt.legend(title="Погода", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.grid()
plt.tight_layout()
plt.savefig(FIG / "06_wind_scatter.png", dpi=150)
plt.show()
plt.close()

print("Сводка по погоде Уфа 2026 ===")
print("дней:", len(df))
print("средняя разница факт/ощущ:", round(mean_abs_diff, 1), "°C")
print("макс отклонение:", round(df["temp_diff"].abs().max(), 1), "°C")
print("дней с осадками:", round(wet_days), "%")
print("холодных дней:", round(cold_days), "%")
print("корреляция ветер/темп:", round(corr, 2))
print("чаще всего:", df["condition"].value_counts().idxmax())