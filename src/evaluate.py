import matplotlib.pyplot as plt
import numpy as np
from .config import PLOTS_DIR

def evaluate_and_plot(model, X, y, scaler_X, scaler_y, target_appliance="TVE"):
    y_pred = model.predict(X)
    
    # Inverse scaling
    y_true = scaler_y.inverse_transform(y)
    y_pred_rescaled = scaler_y.inverse_transform(y_pred)
    
    plt.figure(figsize=(12,5))
    plt.plot(y_true[:500], label="True")
    plt.plot(y_pred_rescaled[:500], label="Predicted")
    plt.title(f"Disaggregation for {target_appliance}")
    plt.xlabel("Time Steps")
    plt.ylabel("Power (W)")
    plt.legend()
    
    plt.savefig(f"{PLOTS_DIR}/{target_appliance}_plot.png")
    plt.show()
