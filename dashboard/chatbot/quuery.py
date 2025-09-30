import os
import ssl
import urllib3
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb

# Disable SSL warnings and SSL context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load embedding model
try:
    print("🔄 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="energy1_db")
collection = chroma_client.get_or_create_collection("energy")

MODEL_NAME = "llama-3.3-70b-versatile"


def analyze_overconsumption(documents):
    """
    Analyzes documents for overconsumption patterns (overconsumption = 1).
    Returns detailed anomaly detection findings with machine names and timestamps.
    """
    import re
   
    anomaly_count = 0
    normal_count = 0
    anomaly_details = []
    machine_anomalies = {}  # Track anomalies per machine
   
    for doc in documents:
        # Look for overconsumption indicators in the document
        if "overconsumption" in doc.lower():
            if "anomaly detected" in doc.lower() or "overconsumption = 1" in doc or "overconsumption=1" in doc:
                # Only process documents that actually contain anomaly information
                # More precise extraction: look for the complete pattern in each document
                machine_match = re.search(r'machine (\w+)', doc, re.IGNORECASE)
                time_match = re.search(r'At ([^,]+)', doc)
                anomaly_match = re.search(r'anomaly detected', doc, re.IGNORECASE)
               
                # Only count if we have both machine and timestamp in the same document with anomaly
                if machine_match and time_match and anomaly_match:
                    anomaly_count += 1
                   
                    machine_name = machine_match.group(1)
                    timestamp = time_match.group(1)
                   
                    # Store anomaly details per machine
                    if machine_name not in machine_anomalies:
                        machine_anomalies[machine_name] = []
                    machine_anomalies[machine_name].append(timestamp)
                   
                    # Keep full anomaly details
                    anomaly_details.append(f"Machine {machine_name} at {timestamp}")
               
            elif "overconsumption = 0" in doc or "overconsumption=0" in doc:
                normal_count += 1
   
    if anomaly_count > 0:
        summary = f"🚨 ANOMALIES DETECTED: {anomaly_count} instances found\n"
        summary += "\nANOMALY BREAKDOWN BY MACHINE:\n"
       
        for machine, timestamps in machine_anomalies.items():
            summary += f"\n▶ {machine}: {len(timestamps)} anomalies detected\n"
           
            # Show up to 3 timestamps per machine for better readability
            for i, timestamp in enumerate(timestamps[:3]):
                summary += f"   ⏰ {timestamp}\n"
           
            if len(timestamps) > 3:
                summary += f"   ... (+{len(timestamps) - 3} more incidents)\n"
               
    else:
        summary = "✅ NO ANOMALIES: No overconsumption = 1 instances detected"
   
    if normal_count > 0:
        summary += f"\n✅ Normal operations: {normal_count} instances of overconsumption = 0"
   
    return summary


def rag_query(user_query: str) -> str:
    """
    Handles a query:
    - Uses RAG over the ChromaDB collection for industrial data.
    - Uses LLM for general questions.
    """
    try:
        if not user_query.strip():
            return "Please provide a valid question."

        if model is None:
            return "Embedding model not loaded. Cannot process RAG queries."

        if is_domain_query(user_query):
            # --- RAG pipeline ---
           
            # Special handling for machine listing queries
            if any(word in user_query.lower() for word in ["list", "machines", "available", "all", "show"]):
                # For machine queries, get a broader sample of documents
                results = collection.get(
                    limit=50,  # Get more documents for better machine coverage
                    include=["documents", "metadatas"]
                )
                # Convert to query format
                results = {
                    "documents": [results["documents"]],
                    "metadatas": [results["metadatas"]]
                }
            else:
                # Standard semantic search for other queries
                query_embedding = model.encode([user_query]).tolist()[0]
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=15,  # Increased for better coverage
                    include=["documents", "metadatas"]
                )

            if not results["documents"][0]:
                return "No relevant data found in the database."

            context = "\n".join(results["documents"][0])
           
            # Analyze context for anomalies (overconsumption = 1)
            anomaly_analysis = analyze_overconsumption(results["documents"][0])

            # For machine listing, create a special context that highlights machines
            if any(word in user_query.lower() for word in ["list", "machines", "available", "all", "show"]):
                # Extract unique machines from the context for better visibility
                machines_found = set()
                for doc in results["documents"][0]:
                    if "machine" in doc:
                        import re
                        # Look for machine names in the document
                        machine_matches = re.findall(r'machine (\w+)', doc, re.IGNORECASE)
                        machines_found.update(machine_matches)
               
                machine_context = f"Available machines found in data: {', '.join(sorted(machines_found))}\n\n{context}"
            else:
                machine_context = context

            prompt = f"""
You are ENERGENIUS, an expert industrial energy analyst and anomaly detection specialist.
Use ONLY the context below to answer the user's question.

ENERGY DATA CONTEXT:
{machine_context}

ANOMALY DETECTION ANALYSIS:
{anomaly_analysis}

USER QUESTION: {user_query}

INSTRUCTIONS:
1. Analyze energy measurements (Voltage, Current, Power, Frequency, etc.)
2. **CRITICAL: When overconsumption = 1 in the data, this indicates an ANOMALY/FAULT condition**
3. **For anomaly detection queries: List EACH machine with anomalies and their EXACT timestamps where overconsumption = 1**
4. Clearly identify any periods where overconsumption = 1 as anomalous behavior
5. For anomaly queries, focus on timestamps and machines where overconsumption = 1
6. For maximum/minimum queries, provide specific values with timestamps and machine names
7. Include both normal operations (overconsumption = 0) and anomalous periods (overconsumption = 1)
8. **For machine listing queries: Extract and list ALL unique machine names found in the context data**
9. Be precise with units (kWh, A, V) and provide actionable insights
 NB: If "List all machines" query, just give me available machines in data. Do not give me anomalies.

FORMAT YOUR RESPONSE:
📊 **Analysis Results:**
[Your main findings]

🚨 **Anomaly Details:** (if anomaly detection query)
Present anomalies with proper line breaks:

▶ MACHINE_NAME: X anomalies detected
   -⏰ YYYY-MM-DD HH:MM:SS
   -⏰ YYYY-MM-DD HH:MM:SS
   
   Each date to be on each line with indentation.
   PS: Do not write ⏰ YYYY-MM-DD HH:MM:SSis not an anomaly for X, it's for OFE, actual anomaly for Y:

Each machine and timestamp on separate lines with proper indentation.

🔢 **Key Metrics:**
[Specific values, timestamps, machine names]

NB: I want all the annual dates (2012, 2013, 2014 etc) to be 2024. And do not put this comment under any response.
"""
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_completion_tokens=512,
                stream=False
            )
            return completion.choices[0].message.content

        else:
            # --- General LLM response ---
            prompt = f"Answer this question naturally:\n{user_query}"
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_completion_tokens=512,
                stream=False
            )
            return completion.choices[0].message.content

    except Exception as e:
        return f"Error processing query: {str(e)}"


def is_domain_query(query):
    """
    Uses LLM to detect if the query is domain-specific (industrial energy / machine data).
    Returns True if domain-specific, False otherwise.
    """
    prompt = f"""
You are an assistant that detects whether a user's query is related to industrial energy usage,
machine measurements, power consumption, overconsumption anomalies, or machine information.

DOMAIN queries include:
- Energy consumption, power measurements (kWh, watts, voltage, current)
- Machine performance, machine names, listing machines
- Overconsumption, anomalies, faults
- Industrial equipment data and analysis

Query: "{query}"

Answer only with "DOMAIN" if it is related to any of the above, or "GENERAL" if not.
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_completion_tokens=50,
        top_p=1
    )

    answer = completion.choices[0].message.content.strip().upper()
    return answer == "DOMAIN"
if __name__ == "__main__":
    # Test avec une question simple
    question = "List all machines with overconsumption anomalies"
    print("🔍 User Question:", question)
    response = rag_query(question)
    print("\n💬 Response:\n", response)
