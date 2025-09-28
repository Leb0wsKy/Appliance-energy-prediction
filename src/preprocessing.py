from sklearn.preprocessing import MinMaxScaler
import numpy as np

def preprocess_data(df, target_appliance="TVE"):
    """
    Prepare input (WHE) and target (appliance).
    """
    X = df[["WHE"]].values  # Whole house consumption
    y = df[[target_appliance]].values  # Appliance load
    
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()
    
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    return X_scaled, y_scaled, scaler_X, scaler_y


def create_windows(X, y, seq_len=60):
    Xs, ys = [], []
    for i in range(len(X) - seq_len):
        Xs.append(X[i:i+seq_len])
        ys.append(y[i+seq_len])
    return np.array(Xs), np.array(ys)
