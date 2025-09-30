import pandas as pd
import chromadb
import ssl
import urllib3
from sentence_transformers import SentenceTransformer
import time
from uuid import uuid4

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# CSV file
csv_file = "chatbot/combined_machines_data_100k.csv"

# Load embedding model
print("🔄 Loading embedding model...")
start_time = time.time()
model = SentenceTransformer("all-MiniLM-L6-v2")
print(f"✅ Model loaded in {time.time() - start_time:.2f} seconds")

# Initialize ChromaDB
print("🔄 Initializing ChromaDB...")
client = chromadb.PersistentClient(path="energy1_db")
collection = client.get_or_create_collection("energy")

# Clear existing data
if collection.count() > 0:
    print(f"🔄 Clearing {collection.count()} existing documents...")
    existing_data = collection.get()
    if existing_data['ids']:
        collection.delete(ids=existing_data['ids'])

# Load CSV
try:
    df = pd.read_csv(csv_file, on_bad_lines="skip")
    print(f"✅ Loaded {len(df)} rows from {csv_file}")
   
    # Show distribution of overconsumption values
    print("📊 Overconsumption distribution:")
    print(df['overconsumption'].value_counts())
   
    # Use a reasonable sample that includes anomalies - take every 10th row
    df = df.iloc[::10]  # Sample every 10th row to get ~10,000 rows
    print(f"✅ Sampled {len(df)} rows (every 10th row)")
    print("📊 Sample overconsumption distribution:")
    print(df['overconsumption'].value_counts())
except Exception as e:
    raise RuntimeError(f"❌ Error loading {csv_file}: {e}")

# Convert UNIX timestamp to datetime
df["timestamp"] = pd.to_datetime(df["unix_ts"], unit="s")

# Column explanations mapping
column_explanations = {
    "V": "Voltage (V)",
    "I": "Current (A)",
    "f": "Frequency (Hz)",
    "DPF": "Displacement Power Factor",
    "APF": "Apparent Power Factor",
    "P": "Real Power (W)",
    "Pt": "Total Real Power (W)",
    "Q": "Reactive Power (VAR)",
    "Qt": "Total Reactive Power (VAR)",
    "S": "Apparent Power (VA)",
    "St": "Total Apparent Power (VA)",
}

# Function to convert row to descriptive text
def row_to_text(row):
    energy_text = ", ".join([
        f"{col}={row[col]} ({column_explanations[col]})" for col in column_explanations
    ])
    anomaly_text = "⚠️ Overconsumption anomaly detected" if row["overconsumption"] == 1 else "Normal operation"
    return (f"At {row['timestamp']}, machine {row['machine_name']} - "
            f"{energy_text}. Status: {anomaly_text}.")

# Convert all rows to text
documents = df.apply(row_to_text, axis=1).tolist()

# Create embeddings
print(f"🔄 Creating embeddings for {len(documents)} documents...")
embeddings = model.encode(documents, batch_size=32, show_progress_bar=True).tolist()
print(f"✅ Embeddings created in {time.time() - start_time:.2f} seconds")

# Generate unique IDs and metadata
ids = [f"doc_{i}_{uuid4()}" for i in range(len(documents))]
metadatas = [{"machine": row["machine_name"]} for _, row in df.iterrows()]

# Store in ChromaDB in batches
print(f"\n🔄 Storing {len(documents)} documents in ChromaDB...")
batch_size = 100
for i in range(0, len(documents), batch_size):
    collection.add(
        documents=documents[i:i+batch_size],
        embeddings=embeddings[i:i+batch_size],
        ids=ids[i:i+batch_size],
        metadatas=metadatas[i:i+batch_size],
    )
    print(f"   ✅ Batch {(i // batch_size) + 1}/{(len(documents)+batch_size-1)//batch_size} completed")

print(f"\n🎉 Successfully indexed {collection.count()} documents into ChromaDB!")
print(f"⏱️ Total processing time: {time.time() - start_time:.2f} seconds")