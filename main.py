import pandas as pd
import analysis
import plsa_with_prior
import plsa_without_prior

# Normalize stock data that has been pre-downloaded and stored in a folder called 'stock_data'.
# Output: dictionary with month as key and dataframe containing month's stock data as value.
df_collection = {}

dfs_may = pd.read_html('stock_data/May_2000.htm', header=0)
df_collection['May'] = pd.DataFrame(dfs_may[0])
dfs_june = pd.read_html('stock_data/June_2000.htm', header=0)
df_collection['June'] = dfs_june[0]
dfs_july = pd.read_html('stock_data/July_2000.htm', header=0)
df_collection['July'] = dfs_july[0]
dfs_august = pd.read_html('stock_data/August_2000.htm', header=0)
df_collection['Aug'] = dfs_august[0]
dfs_sept = pd.read_html('stock_data/Sept_2000.htm', header=0)
df_collection['Sept'] = dfs_sept[0]
dfs_oct = pd.read_html('stock_data/Oct_2000.htm', header=0)
df_collection['Oct'] = dfs_oct[0]

# This is where normalization occurs.
# Formula from paper: (Dem Price /(Dem Price + Rep Price))
# Normalized values added as new column to each month's dataframe.
for key in df_collection:
    df = df_collection[key]
    df_collection[key] = df_collection[key][df_collection[key].Contract != 'Reform']
    df_collection[key] = df_collection[key].drop(['Units', '$Volume', 'LowPrice', 'HighPrice', 'LastPrice'], axis=1)
    df_collection[key] = df_collection[key].dropna()
    df_collection[key]['NormalizedPrice'] = 0

    for index, row in df_collection[key].iterrows():
        if row['Contract'] == 'Dem':
            demPrice = float(row['AvgPrice'])
            # print(demPrice)
            repPrice = df_collection[key].loc[df_collection[key]['Date'] == row['Date']]
            repPrice = repPrice[repPrice.Contract != 'Dem']
            repPrice.reset_index(drop=True, inplace=True)
            if (repPrice.empty):
                df_collection[key].loc[index, 'NormalizedPrice'] = -1
            else:
                repPrice = repPrice.iloc[0]['AvgPrice']
                repPrice = float(repPrice)
                df_collection[key].loc[index, 'NormalizedPrice'] = demPrice / (demPrice + repPrice)
        if row['Contract'] == 'Rep':
            repPrice = float(row['AvgPrice'])
            # print(demPrice)
            demPrice = df_collection[key].loc[df_collection[key]['Date'] == row['Date']]
            demPrice = demPrice[demPrice.Contract != 'Rep']
            demPrice.reset_index(drop=True, inplace=True)
            if (demPrice.empty):
                df_collection[key].loc[index, 'NormalizedPrice'] = -1
            else:
                demPrice = demPrice.loc[0, 'AvgPrice']
                demPrice = float(demPrice)
                df_collection[key].loc[index, 'NormalizedPrice'] = repPrice / (demPrice + repPrice)

# We want to create a master dataframe with the stock data for all months.
# This master dataframe is called df_all_normalized.
frames = []
for key in df_collection:
    frames.append(df_collection[key])

df_all_normalized = pd.concat(frames)
df_all_normalized = df_all_normalized[df_all_normalized.NormalizedPrice != -1]

# We input the list of topics for each day and its respective probability which is retrieved by the PLSA algorithm below.
# df_plsa is a new dataframe containing the data we would like
plsa_without_prior.plsa_without_prior_run()
min_probability = analysis.granger_run('plsa_without_prior.csv', df_all_normalized)

# We run PLSA with priors until all topics have confidence of 95%+.
while min_probability < 0.95:
    plsa_with_prior.plsa_with_prior_run()
    min_probability = analysis.granger_run('plsa_with_prior.csv', df_all_normalized)
