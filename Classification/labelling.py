import pandas as pd
import os

# 1. Load your original CSV
file_paths = ['Electricity_I.csv','Electricity_P.csv','Electricity_Q.csv','Electricity_S.csv'] 
file_paths = ['data/'+ fp for fp in file_paths] 
for file_path in file_paths:
    df = pd.read_csv(file_path)

    # 2. Identify all machine columns (every column except timestamp)
    timestamp_col = 'UNIX_TS'
    machine_columns = [col for col in df.columns if col != timestamp_col]

    # 3. Build combined dataframe of (Timestamp, Machine, Overconsumption)
    records = []
    for machine_col in machine_columns:
        # Calculate a simple threshold for overconsumption: mean + 2*std
        threshold = df[machine_col].mean() + 2 * df[machine_col].std()

        # Flag rows above threshold
        overconsumption = (df[machine_col] > threshold).astype(int)

        # Append rows for each timestamp
        for ts, oc in zip(df[timestamp_col], overconsumption):
            records.append((ts, machine_col, oc))

    # 4. Create new dataframe
    all_df = pd.DataFrame(records, columns=['Timestamp', 'Machine', 'Overconsumption'])

    # 5. Save to CSV
    output_path_all = 'C:/Users/Admin/Desktop/IEEE/IASTAM5.0/'+file_path[:-4]+'_Overconsumption_AllMachines.csv'
    all_df.to_csv(output_path_all, index=False)

    print(f"File saved as {output_path_all}")
    print(all_df.head())
