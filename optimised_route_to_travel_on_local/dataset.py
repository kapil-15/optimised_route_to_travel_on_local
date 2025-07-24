import camelot.io as camelot
import pandas as pd
import numpy as np


def convert_pdf_timetable(pdf_path, store_data_path ):


    tables = camelot.read_pdf(
        pdf_path,
        flavor='stream',
        pages="all",
        #_______________________________
        row_tol=2,               # Tighten row detection
        edge_tol=750,
        #_______________________________
        table_areas=["50,800,800,0"]               #["50,700,550,100"] ## Left, Top, Right, Bottom
    )
    merged_df = pd.DataFrame()
    count = 0
    for i in tables:
        print(i)
        count += 1
        df = i.df
        num=df.index[df.iloc[:, 0] == "CSMT"][0] #Get the index of "CSMT"
        header_rows = df.loc[1:num-1]
        new_header = header_rows.apply(lambda x: '_'.join(x.astype(str)), axis=0)
        df.columns = new_header
        df = df.iloc[num:]
        df.rename(columns={df.columns[0]: 'Station_Name'}, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(f"../data/raw/extracted_csv_file/Central_Line_{count}.csv")
        melted_df = pd.melt(df, id_vars=df.columns[0], var_name="Train_ID", value_name="Arrival_Time")
        melted_df.replace(['',"…","`"], np.nan, inplace=True)
        melted_df.dropna(inplace=True)
        melted_df["Arrival_Time"] =pd.to_datetime(melted_df["Arrival_Time"], format="%H:%M").dt.time
        melted_df["Station_Order"]=melted_df.groupby("Train_ID").cumcount() + 1  # creating station sequence
        melted_df.to_csv(f"../data/processed/cleaned_csv_file/Central_Line_{count}.csv")
        #--------------
        merged_df = pd.concat([merged_df,melted_df], ignore_index=True)
        
    merged_df.to_csv(store_data_path, index=False)
