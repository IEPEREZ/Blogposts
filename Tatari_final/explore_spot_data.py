import pandas as pd
import matplotlib.pyplot as plt
from datetime import timezone
from datetime import datetime, timedelta
import dateutil
import pickle
import period_identification

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
df_web = pd.read_csv('assignment-analyst-1-traffic-data.csv', parse_dates=["time"])
#import the data using our csv reader in pandas 
df = pd.read_csv('assignment-analyst-1-spot-data.csv', parse_dates = ["time"])
#bool splitting has a hard time if program has nans 
df['program'] = df['program'].fillna('')
df = df.sort_values(by='time', ascending=True)
# split into the east and west feeds
df_east = df[df['feed'] == 1]
df_west = df[df['feed'] == 2]

# group our data by the network code or channel
by_netw = df_east.groupby("network_code")
network_codes = df.network_code.unique()
#testcase fxx
for i in range(len(network_codes)):
    plot_df = by_netw.get_group(network_codes[0])
    clusters = period_identification.cluster_assignment(plot_df, 21600)
    df_east['in_cluster'] = df_east.apply(lambda x: period_identification.check_cluster(x, clusters), axis=1)

df_east = df_east.reset_index()

df_east_fxx = df_east[df_east['in_cluster'] == True]


#generatestartandstoptimes for pltaxvspan
avspairs = period_identification.axvspan_start_stop_color_id(df_east)

for i in range(len(avspairs)):
    print(avspairs[i])
    if avspairs[i][0]==True:
        print("red")
        shade='red'
    else:
        print("green")
        shade='green'
    plt.axvspan(avspairs[i][1], avspairs[i][2], color=shade, alpha=0.1)

# print(len(clusters))
plt.scatter(x=plot_df['time'], y=[10]*len(plot_df))
plt.scatter(x=df_east['time'], y=[1]*len(df_east))
plt.show()


#for i in range(len(clusters)):
#    plt.scatter(x=clusters[i], y=[(i+1)*10]*len(clusters[i]))

#plt.show()
#df_east_live.to_pickle("./df_east_live.pkl")
#df_west_live.to_pickle("./df_west_live.pkl")

# df = df.groupby("network_code")
# for i in range(len(df)):


# task find the duration of each creative


#def logical_duration_fill()
#questions 
#for some the duration is missing..
#was it because the ad was played and not recorded or... was it remnant ad time?
#my guess it didnot get shown because ... its during nfl and sports games

# revolt is an online tv channel shows no show or duration
# I would guess they just don't feel like sharing this info?

# 
"""
print(df.traffic_source.unique())
#print(df.value.unique())

# df = df.resample("5T").sum()
# print(df.head())

# questions ?
# the visits in the minute are negative/ partial should be integers
# hwile individual visits could have happened at timestamps and then aggregated
# not sure 

df_dir = df[df['traffic_source'] == 'direct']
df_eml = df[df['traffic_source'] == 'email']

print(len(df_eml))

#print(df.value.unique())

plt.scatter(x=df_dir['time'], y=df_dir['value'],s=1)
plt.scatter(x=df_eml['time'], y=df_eml['value'],s=1)
plt.show()
"""
#print(test_east_live['time'])
#plt.scatter(x=test_east_live['time'], y=[10]*len(test_east_live), s=1)
#plt.show()

# if __name__ == "__main__":
#     pass
