import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np

def evaluate_model(model_path, X_test, y_test):
    # Load model
    model = tf.keras.models.load_model(model_path)

    # Predict probabilities
    y_pred_proba = model.predict(X_test).ravel()

    # Convert to binary labels
    y_pred = (y_pred_proba > 0.5).astype(int)

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    print("✅ Accuracy:", acc)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

    return acc
