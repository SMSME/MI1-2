import pandas as pd
from pandas.tseries.offsets import MonthEnd

# --- STEP 1: PREPROCESS ZILLOW RENT DATA (Zip 22903) ---

# Load the raw ZORI dataset
zillow_file = 'Zip_zori_uc_sfrcondomfr_sm_month.csv'
df_zillow_raw = pd.read_csv(zillow_file)

# Filter for UVA area zip code
df_22903 = df_zillow_raw[df_zillow_raw['RegionName'] == 22903]

# Identify date columns (all columns except the initial metadata)
metadata_cols = ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName']
date_cols = [col for col in df_zillow_raw.columns if col not in metadata_cols]

# Melt from Wide to Long format (one row per date)
df_rent_long = df_22903.melt(id_vars=['RegionName'], 
                             value_vars=date_cols, 
                             var_name='ds', 
                             value_name='y')

# Data Cleaning: Convert 'ds' to datetime and interpolate missing rent values
df_rent_long['ds'] = pd.to_datetime(df_rent_long['ds'])
df_rent_long['y'] = df_rent_long['y'].interpolate(method='linear')

# Final rent formatting
df_rent_final = df_rent_long[['ds', 'y']].sort_values('ds').reset_index(drop=True)


# --- STEP 2: PREPROCESS BLS EMPLOYMENT DATA (Charlottesville MSA) ---

# Load BLS file, skipping the first 10 rows of metadata
employment_file = 'SeriesReport-20260311082221_73518f.csv'
df_emp_raw = pd.read_csv(employment_file, skiprows=10)

# Melt from wide to long format
df_emp_long = df_emp_raw.melt(id_vars=['Year'], var_name='Month', value_name='employment_count')

# Map month names to numbers
month_map = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}
df_emp_long['month_num'] = df_emp_long['Month'].map(month_map)

# Create 'ds' column and align to month-end to match Zillow format
df_emp_long['ds'] = pd.to_datetime(
    df_emp_long['Year'].astype(str) + '-' + df_emp_long['month_num'].astype(str) + '-01'
)
df_emp_long['ds'] = df_emp_long['ds'] + MonthEnd(1)

# Sort and handle reporting gaps (e.g., if October 2025 is missing)
df_emp_final = df_emp_long[['ds', 'employment_count']].sort_values('ds').set_index('ds')
full_range = pd.date_range(start=df_emp_final.index.min(), end=df_emp_final.index.max(), freq='ME')

# Re-index to ensure all months exist and use linear interpolation to fill gaps
df_emp_full = df_emp_final.reindex(full_range).interpolate(method='linear').reset_index()
df_emp_full.rename(columns={'index': 'ds'}, inplace=True)


# --- STEP 3: MERGE INTO FINAL MASTER DATASET ---

# Use an inner join to keep only months where both sources have data
df_master = pd.merge(df_rent_final, df_emp_full, on='ds', how='inner')

# Save the final robust master dataset for use in Meta Prophet
df_master.to_csv('Charlottesville_Rent_Employment_Master.csv', index=False)

print("Master dataset saved as 'Charlottesville_Rent_Employment_Master.csv'.")