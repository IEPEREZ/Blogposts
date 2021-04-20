import pandas as pd
import matplotlib.pyplot as plt
from period_identification import format_timestamps
from period_identification import cluster_assignment
from period_identification import check_cluster
from period_identification import axvspan_start_stop_color_id
import numpy as np
# fig 1 simple description of webtraffic data

df = pd.read_csv('assignment-analyst-1-web-traffic-data.csv', parse_dates = ["time"])
#print(df.columns)
df = df.sort_values(by='time', ascending=True)
df['time'] = df['time'].apply(lambda x: format_timestamps(x))

df_dir = df[df['traffic_source']=='direct']
df_eml = df[df['traffic_source']=='email']

df_dir = df_dir.reset_index()
df_eml = df_eml.reset_index()

df_spot = pd.read_csv('assignment-analyst-1-spot-data.csv', parse_dates=['time'])
#bool splitting has a hard time if program has nans 
df_spot['program'] = df_spot['program'].fillna('')
df_spot = df_spot.sort_values(by='time', ascending=True)
df_spot['time'] = df_spot['time'].apply(lambda x: format_timestamps(x))

# split into the east and west feeds
df_east = df_spot[df_spot['feed'] == 1]
df_west = df_spot[df_spot['feed'] == 2]


def figure_1(df_dir, df_eml, cuttoff):
    fig, ax = plt.subplots(2,sharex=True)
    fig.suptitle("Rate of arrival per minute to company-XYZ's site over 24h")
    ax[0].scatter(x=df_dir['time'], y=df_dir['value'], s=1, label="direct traffic")
    ax[0].set_ylim(min(df_dir['value'][:cuttoff]), max(df_dir['value'][:cuttoff]+10))
    ax[1].scatter(x=df_eml['time'], y=df_eml['value'], s=1, label="email traffic", color='orange')
    ax[1].set_ylim(min(df_eml['value'][:cuttoff]), max(df_eml['value'][:cuttoff]))
    plt.xlim(df['time'].iloc[0], df['time'].iloc[cuttoff])
    ax[0].set_ylabel("direct arrivals to site")
    ax[1].set_ylabel("email arrivals to site")
    ax[0].set_xlabel("date/time UTC datetime")
    ax[1].set_xlabel("date/time UTC datetime")
    plt.show()

def figure_2_categorical(df_spot, grouping_col_name):
    grouped = df_spot.groupby(grouping_col_name)
    print(len(grouped))
    unique_subgroups = df_spot[grouping_col_name].unique()
    #unique_subgroups = unique_subgroups[~np.isnan(unique_subgroups)]
    #print(type(unique_subgroups))
    #unique_subgroups = [member if member > 0 else  for member in range(len(unique_subgroups))]

    print(unique_subgroups)

    for i in range(len(unique_subgroups)):
        group_code = unique_subgroups[i]
        print(group_code)
        title = str(group_code)+" @ level:"+str((i+1)*10)
        plot_df = grouped.get_group(group_code)
        print(len(plot_df))
    
        plt.scatter(x=plot_df['time'], y=[(i+1)*10]*len(plot_df), s=2,label=title)
    plt.legend()
    plt.ylabel("arbitrary group level")
    plt.xlabel("time spot aired (datetime UTC)")
    plt.title("Airing of Spots by " + grouping_col_name)
    plt.show()

#figure_2_4(df_east, 'network_code')

#figure_2_4(df_east, 'duration')

def figure_2_numeric(df_spot, grouping_col_name):
    grouped = df_spot.groupby(grouping_col_name)
    print(len(grouped))
    unique_subgroups = df_spot[grouping_col_name].unique()
    unique_subgroups = unique_subgroups[~np.isnan(unique_subgroups)]
    print(type(unique_subgroups))
    #unique_subgroups = [member if member > 0 else  for member in range(len(unique_subgroups))]

    print(unique_subgroups)

    for i in range(len(unique_subgroups)):
        group_code = unique_subgroups[i]
        print(group_code)
        title = str(group_code)+" @ level:"+str((i+1)*10)
        plot_df = grouped.get_group(group_code)
        print(len(plot_df))
    
        plt.scatter(x=plot_df['time'], y=[unique_subgroups[i]]*len(plot_df), s=2,label=title)
    plt.legend()
    plt.ylabel("Numeric Group level units")
    plt.xlabel("time spot aired (datetime UTC)")
    plt.title("Airing of Spots by " + grouping_col_name)
    plt.show()

#figure_2_4_categorical(df_east, 'program')

def figure_3_categorical(df_spot, df_eml, df_dir, grouping_col_name, sup_title, wait_time):
    grouped = df_spot.groupby(grouping_col_name)
    unique_subgroups = df_spot[grouping_col_name].unique()

    fig, ax = plt.subplots(5, sharex=True)
    fig.suptitle(sup_title)
    for i in range(5):
        code = unique_subgroups[i]
        title = code+" "+str((i+1)*10)
        plot_df = grouped.get_group(code)
        clusters = cluster_assignment(plot_df, wait_time)
        df_eml['in_cluster'] = df_eml.apply(lambda x: check_cluster(x, clusters, remember_others=True), axis=1)
        avspairs = axvspan_start_stop_color_id(df_eml)
        for n in range(len(avspairs)):
            if avspairs[n][0]==True:
                shade='red'
            else:
                shade='green'
            if len(avspairs[n]) == 3:
                ax[i].axvspan(avspairs[n][1], avspairs[n][2], color=shade, alpha=0.1)
        ax[i].scatter(x=plot_df['time'], y=[(i+1)*10]*len(plot_df), s=2,label=title[:5])
        ax[i].set_ylabel(code[:5])
        if i == len(unique_subgroups)-2:
            ax[i].scatter(x=df_dir['time'], y=df_dir['value'],s=1, label="direct traffic")
            ax[i].set_ylabel(code[:5] + " direct traffic")
        if i == len(unique_subgroups)-1:
            ax[i].scatter(x=df_eml['time'], y=df_eml['value'],s=1, label="email traffic")
            ax[i].set_ylabel(code[:5] +" email traffic")

    fig.text(0.5, 0.04, 'Date/Time (UTC datetime)', ha='center')
    fig.text(0.04, 0.5, 'individual '+grouping_col_name+'; number of site arrivals', va='center', rotation='vertical')

    plt.show()

fig_4_sup_title = "Sample Active Period contribution by the 8 creatives, deadline between spots 10h"
fig_5_sup_title = "Sample Active Period contribution by the 5 channels, deadline between spots 10h"
#figure_3_categorical(df_spot, df_eml, df_dir, "creative_id", fig_4_sup_title, 36000)

# needs fix
#figure_3_categorical(df_spot, df_eml, df_dir, "network_code", fig_5_sup_title, 36000)

# figure that just shows both fully selected by creative ?## done
# under the figure excise a mean lambda_0 TODO

# figure that just shows both fully selected by channel ## done
# under figure mean lambda_0 TODO

# figure that shows just single selections by channel DONE 
# under the figure print 5 sample mean lambda_n's TODO 

# figure that shows just single selections by creative done
# under the figure print the set of creative lambdas  todo 


# getting spend by channel and spend by creative
def spend_across_netw(df_spot):
    by_netw = df_spot.groupby("network_code")
    unique_netw = df_spot.network_code.unique()
    spends=[]
    for i in range(len(unique_netw)):
        netw_df = by_netw.get_group(unique_netw[i])
        spend = netw_df['spend'].sum()
        print(spend, unique_netw[i])
        spends.append(spend)
    plt.bar(unique_netw, spends)
    plt.ylabel("Total Effective Spend at Network (USD)")
    plt.xlabel("Network code")
    plt.title("Spend Across Networks on East Coast Spots")
    plt.show()

#def spend_across_creative(df_spot):#
spend_across_netw(df_spot)

def spend_across_creative(df_spot):
    by_creative = df_spot.groupby("creative_id")
    unique_creative = df_spot.creative_id.unique()
    spends=[]
    for i in range(len(unique_creative)):
        creative_df = by_creative.get_group(unique_creative[i])
        spend = creative_df['spend'].sum()
        print(spend, unique_creative[i])
        spends.append(spend)
    unique_creative =  [unique_creative[name][:5] for name in range(len(unique_creative))]
    plt.bar(unique_creative, spends)
    plt.ylabel("Total Effective Spend by Creative (USD)")
    plt.xlabel("first 5 letters of creative_id")
    plt.title("Spend Across Creatives on East Coast Spots")
    plt.show()

spend_across_creative(df_spot)

