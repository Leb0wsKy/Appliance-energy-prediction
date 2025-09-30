from loader import load_data
from train import train_model
from evaluate import evaluate_model
from plot import plot_confusion_matrix, plot_training_history, print_classification_report

def main():
    # 1. Load data
    X_train, X_test, y_train, y_test, scaler = load_data()

    # 2. Train model
    model, history = train_model(X_train, y_train, save_path="Classification/model/class_model.h5")

    # 3. Predict on test set
    y_pred = model.predict(X_test)
    # If binary classification, convert probabilities to class labels
    if y_pred.shape[1] == 1 or len(y_pred.shape) == 1:
        y_pred = (y_pred > 0.5).astype(int).flatten()
    else:
        y_pred = y_pred.argmax(axis=1)

    # 4. Plot results
    plot_confusion_matrix(y_test, y_pred, labels=[0,1])
    plot_training_history("Classification/model/history.pkl")
    print_classification_report(y_test, y_pred)

    # 5. Evaluate model (optional, if you want to keep this)
    evaluate_model("Classification/model/class_model.h5", X_test, y_test)

if __name__ == "__main__":
    main()