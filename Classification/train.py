from model import build_model
import joblib
import os

def train_model(X_train, y_train, save_path="Classification/model/class_model.h5"):
    # Build model
    model = build_model(input_dim=X_train.shape[1])

    # Train
    history = model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=30,
        batch_size=32,
        verbose=1
    )

    # Save model
    model.save(save_path)
    print(f"✅ Deep learning model saved to {save_path}")

    # Save training history
    model_dir = os.path.dirname(save_path)
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(history.history, os.path.join(model_dir, "history.pkl"))

    return model, history
