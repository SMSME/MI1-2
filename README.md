# DS4002 Project 2: Timeseries Data

## Software And Platform ##
- For the software, we have used Python (v3.11.7) for all the scripts and data analysis with the following required add-on packages:
    - pandas (v3.0.1) for manipulation of .csv files into usable data frames
    - numpy (v2.4.3) for numerical operations
    - scipy (v1.17.1) for statistical tests used in the analysis
    - scikit-learn (v1.8.0) for evaluation metrics (e.g., MAE)
    - prophet (v1.3.0) for time-series modeling
    - dieboldmariano (v1.1.0) for forecast comparison (DM test)
    - pyprojroot (v0.3.0) for robust project-path handling
    - matplotlib (v3.10.8) and seaborn (v0.13.2) for data visualization and plotting

## Instructions for Reproducing Results
### Analysis
To reproduce the results for **analysis** and run through the **entire** process, first run the following command to make a virtual environment:
```bash
python -m venv .venv
```
Afterwards, activate your environment (use the command for your OS):
```bash
source .venv/bin/activate # MAC 

.venv\Scripts\activate # Windows

```

- First install requirements via `pip install -r requirements.txt`

- **Reproducing the Dataset:** We created our dataset from two input datasets present in the `DATA` folder (`DATA/Zillow_Rent_Data.csv` and `DATA/Charlottesville_Employment_Data.csv`). Upon running the script `data_extraction.py`, it will parse both datasets, join them on month-end dates, and save `DATA/Charlottesville_Rent_Employment_Master.csv`. Each row contains the columns `ds` (month-end date), `y` (rent index/value), and `employment_count` (employment/jobs count).

    - How to Reproduce the Dataset:
        - In the command line, run 'cd SCRIPTS' and make sure you are in the 'SCRIPTS' folder. All the scripts are located there and need to be run while in the folder.
        - Run data_extraction.py to parse the datasets and create the final dataset for use.
            - Command: ```
                        python3 data_extraction.py
                        ```


- **Producing Exploratory Plots:** Upon retrieving the dataset, we harnessed the produced CSV to generate exploratory data analysis plots, as well as histograms and summary statistics for the data appendix. 
    - Please run the following command from the `MI1-2/SCRIPTS` directory to create 8 plots (5 EDA, 3 histograms for data appendix) and view the summary statistics:
        - Command: ```
                        python3 eda.py
                        ```

- **Producing and Running Analysis:** All analysis and model creation was done in a jupyter notebook. To see the step by step logic and results, click the play button next to each cell in sequential order. Alternatively, at the top of the notebook you can choose `Run All` to run all the cells at once. This will take some time as the the hyperparameter tuning is a longer process.

## A Map of Documentation

```text
MI1-2/
├── DATA/
│   ├── Charlottesville_Employment_Data.csv
│   ├── Charlottesville_Rent_Employment_Master.csv
│   └── Zillow_Rent_Data.csv
│
├── OUTPUT/
│   ├── eda_1_rent_trend.png
│   ├── eda_2_employment_trend.png
│   ├── eda_3_dual_axis_comparison.png
│   ├── eda_4_scatter_plot.png
│   └── eda_5_monthly_boxplot.png
│
├── SCRIPTS/
│   ├── analysis.ipynb
│   ├── data_extraction.py
│   └── eda.py
│
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```
