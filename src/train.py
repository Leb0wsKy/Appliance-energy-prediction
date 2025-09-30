from .data_loader import load_data
from .preprocessing import preprocess_data, create_windows
from .model import build_lstm_model
from .config import MODELS_DIR
import os



def train(target_appliance="TVE"):
    df = load_data()
    X, y, scaler_X, scaler_y = preprocess_data(df, target_appliance)
    
    # Windowed data
    Xw, yw = create_windows(X, y, seq_len=30)
    
    model = build_lstm_model(seq_len=30, features=1)
    model.fit(Xw, yw, epochs=10, batch_size=32, validation_split=0.2)
    
    return model, scaler_X, scaler_y