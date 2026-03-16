import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the Master Dataset
df = pd.read_csv('Charlottesville_Rent_Employment_Master.csv')
df['ds'] = pd.to_datetime(df['ds'])
df['month'] = df['ds'].dt.month

# Set a professional plot style
sns.set_theme(style="whitegrid")

# --- PLOT 1: RENT TREND (The Target) ---
plt.figure(figsize=(10, 5))
plt.plot(df['ds'], df['y'], color='blue', linewidth=2, label='Rent ($)')
plt.title('UVA Area Rent Prices (Zip 22903)', fontsize=13)
plt.ylabel('Monthly Rent ($)')
plt.legend()
plt.savefig('eda_1_rent_trend.png')
plt.close()

# --- PLOT 2: EMPLOYMENT TREND (The Regressor) ---
plt.figure(figsize=(10, 5))
plt.plot(df['ds'], df['employment_count'], color='red', linewidth=2, label='Employment')
plt.title('Charlottesville Monthly Employment (2015-2025)', fontsize=13)
plt.ylabel('Number of Jobs')
plt.legend()
plt.savefig('eda_2_employment_trend.png')
plt.close()

# --- PLOT 3: DUAL-AXIS COMPARISON ---
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
plt.savefig('eda_3_dual_axis_comparison.png')
plt.close()

# --- PLOT 4: SCATTER PLOT & REGRESSION ---
plt.figure(figsize=(10, 6))
sns.regplot(x='employment_count', y='y', data=df, 
            scatter_kws={'alpha':0.3, 'color':'gray'}, 
            line_kws={'color':'darkred', 'label':'Linear Trend'})
plt.title('Employment Level vs. Rent Level', fontsize=13)
plt.xlabel('Employment Count')
plt.ylabel('Rent Price ($)')
plt.savefig('eda_4_scatter_plot.png')
plt.close()

# --- PLOT 5: SEASONAL BOXPLOTS ---
plt.figure(figsize=(10, 6))
sns.boxplot(x='month', y='y', data=df, palette='viridis')
plt.title('Rent Price Distribution By Month', fontsize=13)
plt.xticks(ticks=range(0, 12), labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
plt.ylabel('Rent ($)')
plt.savefig('eda_5_monthly_boxplot.png')
plt.close()

print("5 EDA plots successfully saved to your directory.")