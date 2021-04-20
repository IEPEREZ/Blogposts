import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import time
from period_identification import format_timestamps
from period_identification import cluster_assignment
from period_identification import check_cluster
from period_identification import axvspan_start_stop_color_id

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

df = pd.read_csv('assignment-analyst-1-web-traffic-data.csv', parse_dates = ["time"])
df_east_live = pd.read_pickle("./df_east_live.pkl")
df_west_live = pd.read_pickle("./df_west_live.pkl")

print(df_east_live.head())
df_spot = pd.read_csv('assignment-analyst-1-spot-data.csv', parse_dates=["time"])
df_spot = df_spot.sort_values(by='time', ascending=True)
df_spot['time'] = df_spot['time'].apply(lambda x: format_timestamps(x))
df_spot = df_spot[df_spot['feed']==1.0]
#df_spot = df_spot[:100]

print(type(df['time'].iloc[0].tzinfo))
df = df.sort_values(by='time', ascending=True)
df['time'] = df['time'].apply(lambda x: format_timestamps(x))
#df_spot['program'] = df_spot['program'].fillna('')
#df_live = df_spot[df_spot['program'].str.contains('Live')]

#df_live_east = df_live[df_live['feed'] == 1.0]
#df_list_west = df_live[df_live['feed'] == 2.0]

#print(df.head())
#print(df.traffic_source.unique())


df_dir = df[df['traffic_source'] == 'direct']
df_eml = df[df['traffic_source'] == 'email']

df_eml = df_eml.reset_index()
df_dir = df_dir.reset_index()
#.set_index('time')#.resample("5T").sum()
#df_dir['time'] = df_dir['time'].resample("5T").sum()

#print(type(df_eml['time'].iloc[0]))
def get_rate(df):
    #print(df.head())
    arrivals = df['value'].sum()
    period_length = (max(df['time']) - min(df['time'])).total_seconds() / 60
    return (arrivals/period_length)

def pd_excel_save(title, save_df):
    title +=".xlsx"    
    writer = pd.ExcelWriter(title, engine='xlsxwriter')
    save_df.to_excel(writer, sheet_name='Sheet1')
    writer.save()


#ref_dt = 
#df_eml['time'] = df_eml['time'].dt.tz_localize("Europe/Berlin")
#print(time.utctime(df_east_live['time'].iloc[0]))

#print(type(df_eml['time'].iloc[0]))
#df_east_l['time'] = df_live_east['time'].apply(lambda x: x.timestamp())
#print(type(df_live_east['time'].iloc[0]))
#df_live_east['time'] = (df_live_east['time'] - df_eml['time'].iloc[0])# /np.timedelta64(1, 's')
#df_eml['time'] = (df_eml['time'] - df_eml['time'].iloc[0]) / np.timedelta64(1, 's')
#df_live_east['time'] = (df_live_east['time'] - df_eml['time'].iloc[0])# /np.timedelta64(1, 's')

#/np.timedelta64(1, 's')#pd.to_timedelta(df_eml['time'])

#plt.hist(df_dir['value'], bins=100)

#query = max(df_eml['value'])
#entry_max = df_eml.query('value == %d' %query)
#plt.hist(df_eml['value'], bins=20)

#print(entry_max)
#df_dir = df_dir[:1000]
#df_eml = df_eml[:10000]
#print(df.value.unique())
print(df_eml['time'].iloc[2800:2840])

#plt.scatter(x=df_dir['time'], y=df_dir['value'],s=1)
#plt.scatter(x=df_eml['time'], y=df_eml['value'],s=1)
#plt.scatter(x=df_east_live['time'], y=[25]*len(df_east_live), s=2)
#plt.scatter(x=df_west_live['time'], y=[12]*len(df_west_live), s=2, color="red")
#plt.xlim(df_eml['time'].iloc[2800], df_eml['time'].iloc[2840])

by_netw = df_spot.groupby("network_code")

unique_networks = df_spot["network_code"].unique()

# def group(df):
#     group_id = 

print(df.head())
by_creative=df_spot.groupby("creative_id")
unique_creatives= df_spot.creative_id.unique()
unique_creatives= unique_creatives
# print(df.duration.unique())
# print(df.network_code.unique())
# print(df.program.unique())
# print(df.rotation_days.unique())
# print(df.is_dual_feed.unique())
fig, ax = plt.subplots(2, sharex=True)
fig.suptitle("Cummulative Active Period contribution from creatives, deadline time between spots = 10 hours")
for i in range(len(unique_creatives)):#len(by_netw)):
    netcode = unique_creatives[i]
    title = netcode+" "+str((i+1)*10)#+"for l0"
    plot_df = by_creative.get_group(netcode)
    clusters = cluster_assignment(plot_df,36000)
    df_eml['in_cluster'] = df_eml.apply(lambda x: check_cluster(x, clusters, remember_others=False), axis=1)
    df_dir['in_cluster'] = df_dir.apply(lambda x: check_cluster(x, clusters, remember_others=False), axis=1)
    avspairs_eml = axvspan_start_stop_color_id(df_eml)
    avspairs_dir = axvspan_start_stop_color_id(df_dir)
    by_cluster_id_eml = df_eml.groupby("cluster_id")
    by_cluster_id_dir = df_dir.groupby("cluster_id")
    dict_to_save = []
    for uc in range(len(by_cluster_id_eml)):
        print(uc)
        input_df_eml = by_cluster_id_eml.get_group(uc)
        input_df_dir = by_cluster_id_dir.get_group(uc)
        rate_eml = get_rate(input_df_eml)
        rate_dir = get_rate(input_df_dir)
        dict_to_save.append({ 'group_id': uc, 'rate eml':rate_eml, 'rate dir':rate_dir})
        print(rate_dir)

    dict_to_df = pd.DataFrame(dict_to_save)

    pd_excel_save(title, dict_to_df)

    # for n in range(len(avspairs)):
    #     #print(avspairs[n])
    #     if avspairs[n][0]==True:
    #         #print("red")
    #         shade='red'
    #     else:
    #         #print("green")
    #         shade='green'
    #     if len(avspairs[n]) == 3:
    #         ax[i].axvspan(avspairs[n][1], avspairs[n][2], color=shade, alpha=0.1)
    #ax[i].scatter(x=plot_df['time'], y=[(i+1)*10]*len(plot_df), s=2,label=title[:5])
    #ax[i].set_ylabel(netcode[:5])#"creative_id "+netcode[:5]+" "+"spot appearances")
    #if i == len(unique_creatives)-2:
    #    ax[i].scatter(x=df_dir['time'], y=df_dir['value'],s=1, label="direct traffic")
    #    ax[i].set_ylabel(netcode[:5] + " direct traffic")
#     if i == len(unique_creatives)-1:
#         for n in range(len(avspairs_)):
#         #print(avspairs[n])
#             if avspairs[n][0]==True:
#             #print("red")
#                 shade='red'
#             else:
#             #print("green")
#                 shade='green'
#         # if len(avspairs[n]) == 3:
#         #     ax[i].axvspan(avspairs[n][1], avspairs[n][2], color=shade, alpha=0.1)
#             ax[0].axvspan(avspairs[n][1], avspairs[n][2], color=shade, alpha=0.1)
#             ax[1].axvspan(avspairs[n][1], avspairs[n][2], color=shade, alpha=0.1)
#         #ax[1].scatter(x=df_eml['time'], y=df_eml['value'],s=1, label="email traffic")
#         #ax[i].set_ylabel(netcode[:5] +" email traffic")

# ax[0].scatter(x=df_dir['time'], y=df_dir['value'], s=1, label="direct traffic")
# ax[1].scatter(x=df_eml['time'], y=df_eml['value'], s=1, label="email traffic")

# ax[0].set_ylabel("direct traffic arrivals")
# ax[1].set_ylabel(" email traffic arrivals")

# fig.text(0.5, 0.04, 'Date/Time (UTC datetime)', ha='center')
# fig.text(0.04, 0.5, 'individual creatives, number of site arrivals', va='center', rotation='vertical')

# #plt.legend()
# plt.show()

print(df_eml.head())






print(df_eml.index[0])