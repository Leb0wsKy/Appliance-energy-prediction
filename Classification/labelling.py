import pandas as pd
import glob
import os

def add_overconsumption_label(df, s_col="S", dpf_col="DPF", k=1.5):
    median_S = df[s_col].median()
    std_S = df[s_col].std()

    df["overconsumption"] = (
        (df[s_col] > median_S + k*std_S) |
        ((df[dpf_col] < 0.8) & (df[s_col] > median_S))
    ).astype(int)
    
    return df

'''
machines=['BME','CWE','DWE','EQE','FRE','HPE','OFE','UTE','WOE','B2E','CDE','DNE','EBE','FGE','HTE','OUE','TVE']
for machine in machines:
    df = pd.read_csv("Classification/data/Electricity_"+machine+".csv")
    df = add_overconsumption_label(df)
    df.to_csv("Classification/data/Electricity_"+machine+".csv", index=False)
    print(df[["S", "DPF", "overconsumption"]].head(15))
'''


def merge_machines_data(df_list):
    machines=['B1E','GRE','BME','RSE','WHE','CWE','DWE','EQE','FRE','HPE','OFE','UTE','WOE','B2E','CDE','DNE','EBE','FGE','HTE','OUE','TVE']
    for machine in machines:
        # Read CSV
        df = pd.read_csv("Classification/data/Electricity_"+machine+".csv")
        
        # Add machine name column
        df["machine_name"] = machine
        
        df_list.append(df)

    # Concatenate all
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df


def read_first_100k_lines(csv_path):
    df = pd.read_csv(csv_path)
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df_shuffled.head(100000)

df=read_first_100k_lines("Classification/data/combined_machines_data.csv")
df.to_csv("Classification/data/combined_machines_data_100k.csv", index=False)