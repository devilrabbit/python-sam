import pandas as pd

df = pd.read_csv('./sample.csv', nrows=1, header=None)
df_tr = df.transpose()
print(df_tr.describe())
df_tr.plot()