import tensorflow as tf
from keras import layers, models

def build_lstm_model(seq_len=30, features=1):
    model = models.Sequential([
        layers.Input(shape=(seq_len, features)),
        layers.LSTM(128, return_sequences=False),
        layers.Dense(64, activation="relu"),
        layers.Dense(1, activation="linear")
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model
