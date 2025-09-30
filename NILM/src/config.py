import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Data files
FILE_I = os.path.join(DATA_DIR, "Electricity_I.csv")
FILE_P = os.path.join(DATA_DIR, "Electricity_P.csv")
FILE_Q = os.path.join(DATA_DIR, "Electricity_Q.csv")
FILE_S = os.path.join(DATA_DIR, "Electricity_S.csv")

# Output folders
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
MODELS_DIR = os.path.join(OUTPUT_DIR, "models")

# Ensure dirs exist
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
