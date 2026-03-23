import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import MonthEnd

# Load the dataset
df = pd.read_csv('../DATA/Charlottesville_Rent_Employment_Master.csv')
df['ds'] = pd.to_datetime(df['ds'])
df['month'] = df['ds'].dt.month

# Set plot style
sns.set_theme(style="whitegrid")

# Plot rent trend
plt.figure(figsize=(10, 5))
plt.plot(df['ds'], df['y'], color='blue', linewidth=2, label='Rent ($)')
plt.title('UVA Area Rent Prices (Zip 22903)', fontsize=13)
plt.ylabel('Monthly Rent ($)')
plt.legend()
plt.savefig('../OUTPUT/eda_1_rent_trend.png')
plt.close()

# Plot employment trend
plt.figure(figsize=(10, 5))
plt.plot(df['ds'], df['employment_count'], color='red', linewidth=2, label='Employment')
plt.title('Charlottesville Monthly Employment (2015-2025)', fontsize=13)
plt.ylabel('Number of Jobs')
plt.legend()
plt.savefig('../OUTPUT/eda_2_employment_trend.png')
plt.close()

# Plot dual axis comparison between rent and employment
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Rent ($)', color=color)
ax1.plot(df['ds'], df['y'], color=color, linewidth=2, label='Rent')
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis for the employment count
ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('Employment Count', color=color)
ax2.plot(df['ds'], df['employment_count'], color=color, alpha=0.5, linestyle='--', label='Employment')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Rent vs. Employment By Year (2015-2025)', fontsize=13)
fig.tight_layout() 
plt.savefig('../OUTPUT/eda_3_dual_axis_comparison.png')
plt.close()

# Plot scatter plot between employment and rent
plt.figure(figsize=(10, 6))
sns.regplot(x='employment_count', y='y', data=df, 
            scatter_kws={'alpha':0.3, 'color':'gray'}, 
            line_kws={'color':'darkred', 'label':'Linear Trend'})
plt.title('Employment Level vs. Rent Level', fontsize=13)
plt.xlabel('Employment Count')
plt.ylabel('Rent Price ($)')
plt.savefig('../OUTPUT/eda_4_scatter_plot.png')
plt.close()

# Plot monthly boxplot of rent
plt.figure(figsize=(10, 6))
sns.boxplot(x='month', y='y', data=df, palette='viridis')
plt.title('Rent Price Distribution By Month', fontsize=13)
plt.xticks(ticks=range(0, 12), labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
plt.ylabel('Rent ($)')
plt.savefig('../OUTPUT/eda_5_monthly_boxplot.png')
plt.close()

# Data appendix statistics and plots

# Load Raw Zillow to find original NaNs for rent
df_z_raw = pd.read_csv('../DATA/Zillow_Rent_Data.csv')
# Filter for UVA area zip code
df_22903_raw = df_z_raw[df_z_raw['RegionName'] == 22903]
date_cols = [c for c in df_z_raw.columns if '20' in c] # Identifies date columns
# Melt from wide to long format such that we get one row per date
df_rent_raw = df_22903_raw.melt(id_vars=['RegionName'], value_vars=date_cols, var_name='ds', value_name='y_raw')
df_rent_raw['ds'] = pd.to_datetime(df_rent_raw['ds'])

# Load Raw Employment to find original NaNs for employment
df_e_raw = pd.read_csv('../DATA/Charlottesville_Employment_Data.csv', skiprows=10)
# Melt from wide to long format such that we get one row per date
df_e_long = df_e_raw.melt(id_vars=['Year'], var_name='Month', value_name='emp_raw')
# Map month names to numbers for the 'ds' column
month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
             'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
df_e_long['ds'] = pd.to_datetime(df_e_long['Year'].astype(str) + '-' + df_e_long['Month'].map(month_map).astype(str) + '-01') + MonthEnd(1)

# We merge the master 'df' with the raw data to see which of our final 132 rows were originally NaN
audit = pd.merge(df[['ds']], df_rent_raw[['ds', 'y_raw']], on='ds', how='left')
audit = pd.merge(audit, df_e_long[['ds', 'emp_raw']], on='ds', how='left')

# Calculate the number of missing values for rent, employment, and dates
n = len(df)
m_y = audit['y_raw'].isna().sum()
m_emp = audit['emp_raw'].isna().sum()
m_ds = 0 # Dates are used as the index, so they are never missing by definition in the master file


# Histogram for ds
plt.figure(figsize=(10, 6))
plt.hist(df['ds'], bins=22, color='orange', edgecolor='black')
plt.title('Distribution of Observations (ds) Across Years', fontsize=13)
plt.xlabel('Date')
plt.ylabel('Frequency (Months per Bin)')
plt.savefig('../OUTPUT/eda_6_ds_histogram.png')
plt.close()

# Histogram for rent index y
plt.figure(figsize=(10, 6))
sns.histplot(df['y'], kde=True, color='blue', bins=15)
plt.title('Distribution of UVA Area Rent Index (y)', fontsize=13)
plt.xlabel('Rent Price ($)')
plt.ylabel('Frequency')
plt.savefig('../OUTPUT/eda_7_rent_histogram.png')
plt.close()

# Histogram for employment count
plt.figure(figsize=(10, 6))
sns.histplot(df['employment_count'], kde=True, color='red', bins=15)
plt.title('Distribution of Charlottesville Employment Count', fontsize=13)
plt.xlabel('Number of Jobs')
plt.ylabel('Frequency')
plt.savefig('../OUTPUT/eda_8_employment_histogram.png')
plt.close()

# Print statistics for each variable
def print_stats(var_name, data, m_val, is_date=False):
    # Describe the data and print the statistics
    stats = data.describe(percentiles=[.25, .5, .75])
    print(f"\nVariable: {var_name}")
    print(f"Status: {n}({m_val})")
    print(f"{'Statistic':<20} | {'Value':<15}")
    print("-" * 40)
    # If the variable is a date, print the statistics for the date
    if is_date:
        origin = data.min()
        days = (data - origin).dt.days
        print(f"{'Mean':<20} | {(origin + pd.to_timedelta(days.mean(), unit='D')).date()}")
        print(f"{'Std. Deviation':<20} | {days.std():.2f} days")
        print(f"{'Minimum':<20} | {data.min().date()}")
        print(f"{'25th Percentile':<20} | {data.quantile(0.25).date()}")
        print(f"{'Median (50th)':<20} | {data.quantile(0.5).date()}")
        print(f"{'75th Percentile':<20} | {data.quantile(0.75).date()}")
        print(f"{'Maximum':<20} | {data.max().date()}")
    else:
        # If the variable is not a date, print raw statistics for the variable
        print(f"{'Mean':<20} | {stats['mean']:,.2f}")
        print(f"{'Std. Deviation':<20} | {stats['std']:,.2f}")
        print(f"{'Minimum':<20} | {stats['min']:,.2f}")
        print(f"{'25th Percentile':<20} | {stats['25%']:,.2f}")
        print(f"{'Median (50th)':<20} | {stats['50%']:,.2f}")
        print(f"{'75th Percentile':<20} | {stats['75%']:,.2f}")
        print(f"{'Maximum':<20} | {stats['max']:,.2f}")

# pritnt final statistics for the variables
print_stats("Date (ds)", df['ds'], m_ds, is_date=True)
print_stats("Rent Index (y)", df['y'], m_y)
print_stats("Employment Count", df['employment_count'], m_emp)
