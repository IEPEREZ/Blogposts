## description: creates QQ plots to answer wei's question on my assumption of normality ## 
## tatari interview presentation 4/08/2021 ## 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

df = pd.read_csv("by_creative_dir.csv") # this changes based on the sheet i want to import there are 4:
# [by network , email] , [by_network, direct], [by_creative, email], [by_creative, direct]
l0_df = df['l0']

df.drop('group_id', inplace=True, axis=1)
df.drop('l0', inplace=True, axis=1)

df = df.dropna(how='all')

l0_df = l0_df.dropna(how='all')

print(l0_df.head())
print(df.head())


# # performing QQ plot on l0  # # 
measurements = l0_df
stats.probplot(measurements, dist='norm', plot=plt)
plt.title("Q-Q Plot l0's for direct traffic grouped by creative_id ")
plt.show()

   # creative new QQ plot for excision of larges two values #
print(l0_df.mean())
#print(l0_df.max(), l0_df.idxmax())
l0_df = l0_df.drop(l0_df.idxmax())
l0_df = l0_df.drop(l0_df.idxmax())
#print(l0_df.max())

# print(l0_df.mean())
# measurements = l0_df
# stats.probplot(measurements, dist='norm', plot=plt)
# plt.title("Q-Q Plot l0's for direct traffic grouped by network, removing largest two values, new mean=" + "6.581 " + "visits/min")
# plt.show()

# creating QQ subplots for network code ## 
fig = plt.figure(figsize=(22, 8))
rows = 4
columns = 5
grid = plt.GridSpec(rows, columns, wspace = .50, hspace = .50)
for i in range(rows*columns):
    net_code = list(df.columns)[i]
    series_no_nan = df[net_code].dropna(how='all')
    exec (f"plt.subplot(grid{[i]})")
    stats.probplot(series_no_nan, dist='norm', plot=plt)
    plt.title(net_code)

plt.suptitle("Q-Q Plots for l1's from direct traffic grouped by network code:")
plt.show()

# creating QQ subplots for creative id ##  
fig = plt.figure(figsize=(22, 8))
rows = 2
columns = 4
grid = plt.GridSpec(rows, columns, wspace = .50, hspace = .50)
for i in range(rows*columns):
    creative_id = list(df.columns)[i]
    series_no_nan = df[creative_id].dropna(how='all')
    exec (f"plt.subplot(grid{[i]})")
    stats.probplot(series_no_nan, dist='norm', plot=plt)
    plt.title(creative_id)

plt.suptitle("Q-Q Plots for l1's from direct traffic grouped by creative_id:")
plt.show()
