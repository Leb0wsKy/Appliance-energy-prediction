from src.train import train
from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.evaluate import evaluate_and_plot

if __name__ == "__main__":
    target_appliance = "TVE"  # Change to CWE, DWE, etc.
    
    model, scaler_X, scaler_y = train(target_appliance)
    
    df = load_data()
    X, y, _, _ = preprocess_data(df, target_appliance)
    
    evaluate_and_plot(model, X, y, scaler_X, scaler_y, target_appliance)
