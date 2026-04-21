#!/usr/bin/env python

import pandas as pd
import numpy as np
import lib.Gold 

from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report

# =========================
# 1. DATEN LADEN
# =========================

def load_data():
    data = lib.Gold.Gold().get_all_prices_with_timestamp()    
    print(data)
    return( data )


def add_returns(df):
    df["log_return"] = np.log(df["price"]).diff()
    
    df["ret_1"] = df["log_return"]
    df["ret_5"] = df["log_return"].rolling(5).sum()
    df["ret_15"] = df["log_return"].rolling(15).sum()
    df["ret_30"] = df["log_return"].rolling(30).sum()
    
    return df

def add_volatility(df):
    df["vol_5"] = df["log_return"].rolling(5).std()
    df["vol_15"] = df["log_return"].rolling(15).std()
    df["vol_30"] = df["log_return"].rolling(30).std()
    
    df["atr"] = (df["price"].rolling(5).max() - df["price"].rolling(5).min())
    
    return df

def add_trend(df):
    df["ma_5"] = df["price"].rolling(5).mean()
    df["ma_15"] = df["price"].rolling(15).mean()
    df["ma_30"] = df["price"].rolling(30).mean()
    
    df["trend_5_15"] = df["ma_5"] - df["ma_15"]
    df["trend_15_30"] = df["ma_15"] - df["ma_30"]
    
    df["momentum"] = df["price"] - df["price"].shift(5)
    
    return df


def add_mean_reversion(df):
    df["ma_15"] = df["price"].rolling(15).mean()
    df["std_15"] = df["price"].rolling(15).std()
    
    df["zscore"] = (df["price"] - df["ma_15"]) / df["std_15"]
    
    df["distance_ma"] = df["price"] / df["ma_15"] - 1
    
    return df

def add_time_features(df):
    df["hour"] = df.index.hour
    df["day_of_week"] = df.index.dayofweek
    
    # Sessions (vereinfacht)
    df["london_session"] = ((df["hour"] >= 8) & (df["hour"] <= 16)).astype(int)
    df["ny_session"] = ((df["hour"] >= 13) & (df["hour"] <= 21)).astype(int)
    df["overlap"] = ((df["hour"] >= 13) & (df["hour"] <= 16)).astype(int)
    
    return df

def add_regime(df):
    df["vol_regime"] = (
        df["vol_15"] > df["vol_15"].rolling(50).mean()
    ).astype(int)
    
    df["trend_regime"] = (
        abs(df["trend_5_15"]) > df["trend_5_15"].rolling(50).std()
    ).astype(int)
    
    return df

def build_gold_features(df):
    df = df.copy()
    
    df = add_returns(df)
    df = add_volatility(df)
    df = add_trend(df)
    df = add_mean_reversion(df)
    df = add_time_features(df)
    df = add_regime(df)
    
    df = df.dropna()
    
    return df


df = pd.DataFrame(load_data(), columns=["timestamp", "price"])
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")


# Erwartet: Spalte "price"
df = df.sort_values("timestamp")  # falls vorhanden

# =========================
# 2. RETURNS BERECHNEN
# =========================

df["log_return"] = np.log(df["price"]).diff()

# =========================
# 3. FEATURE ENGINEERING
# =========================
"""
# Lags
df["ret_1"] = df["log_return"]
df["ret_2"] = df["log_return"].shift(1)
df["ret_5"] = df["log_return"].rolling(5).sum()
df["ret_15"] = df["log_return"].rolling(15).sum()

# Volatilität
df["vol_5"] = df["log_return"].rolling(5).std()
df["vol_15"] = df["log_return"].rolling(15).std()

# Momentum / Trend
df["ma_5"] = df["price"].rolling(5).mean()
df["ma_15"] = df["price"].rolling(15).mean()
df["ma_ratio"] = df["ma_5"] / df["ma_15"]

# Z-Score (Mean Reversion Signal)
df["zscore"] = (df["price"] - df["ma_15"]) / df["price"].rolling(15).std()
"""


df = build_gold_features(df)


# =========================
# 4. TARGET DEFINIEREN
# =========================

# Richtung nächste Minute
df["target"] = (df["log_return"].shift(-1) > 0).astype(int)

# =========================
# 5. CLEANING
# =========================

df = df.dropna()

# =========================
# 6. FEATURES
# =========================

features = [
    "ret_5", "ret_15",
    "vol_5", "vol_15",
    "atr",
    "trend_5_15", "trend_15_30",
    "momentum",
    "zscore",
    "distance_ma",
    "hour", "london_session", "ny_session",
    "vol_regime", "trend_regime"
]

X = df[features]
y = df["target"]

# =========================
# 7. TRAIN / TEST SPLIT (ZEITREIHE!)
# =========================

split = int(len(df) * 0.8)

X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# =========================
# 8. MODELL
# =========================

model = LGBMClassifier(
    n_estimators=200,
    learning_rate=0.05,
    num_leaves=31
)

model.fit(X_train, y_train)

# =========================
# 9. PREDICTION
# =========================

proba = model.predict_proba(X_test)[:, 1]

df_test = df.iloc[split:].copy()
df_test["prob_up"] = proba

# =========================
# 10. SIGNAL GENERATION
# =========================

# nur handeln wenn Sicherheit hoch genug ist
df_test["signal"] = 0
df_test.loc[df_test["prob_up"] > 0.55, "signal"] = 1
df_test.loc[df_test["prob_up"] < 0.45, "signal"] = -1

# =========================
# 11. STRATEGY BACKTEST
# =========================

# nächste Minute Return
df_test["future_return"] = df_test["log_return"].shift(-1)
df_test = df_test.iloc[:-1].copy()

df_test["strategy_return"] = df_test["signal"] * df_test["future_return"]
df_test["strategy_return"] -= 0.0002 * abs(df_test["signal"]) ###TAG

df_test["cumulative_market"] = (1 + df_test["future_return"]).cumprod()
df_test["cumulative_strategy"] = (1 + df_test["strategy_return"]).cumprod()

# =========================
# 12. EVALUATION
# =========================

y_pred = (proba > 0.5).astype(int)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

print("Final Strategy Return:",
      df_test["cumulative_strategy"].iloc[-1])


print("Trades:", (df_test["signal"] != 0).sum())