import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import numpy as np
import os
from sklearn.metrics import confusion_matrix, classification_report

PLOT_DIR = "Classification/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

def plot_confusion_matrix(y_true, y_pred, labels, filename="confusion_matrix.png"):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, filename))
    plt.close()

def plot_training_history(history_path, filename="training_history.png"):
    history = joblib.load(history_path)
    plt.figure(figsize=(8,4))
    plt.plot(history['accuracy'], label='Train Accuracy')
    plt.plot(history['val_accuracy'], label='Val Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training History')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, filename))
    plt.close()

def print_classification_report(y_true, y_pred):
    print("Classification Report:")
    print(classification_report(y_true, y_pred))