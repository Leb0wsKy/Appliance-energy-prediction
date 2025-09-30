import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(path="Classification/data/combined_machines_data_100k.csv", target_col="overconsumption"):
    # Load dataset
    df = pd.read_csv(path)

    # Features = all numeric except machine_name & target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train_numeric = X_train.select_dtypes(include=['number'])
    X_test_numeric = X_test.select_dtypes(include=['number'])

    # Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_numeric)
    X_test_scaled = scaler.transform(X_test_numeric)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler
