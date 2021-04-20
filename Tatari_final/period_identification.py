#period_identification
#Description: functions and tools used to identify where periods are occurring

#imports
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timezone
from datetime import datetime, timedelta
import dateutil
import pickle


#pandas settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


## Functions applying to columns 
# function to apply the timestamp difference 
# because I do not like timestamps with offsets
def format_timestamps(csv_timestamp_w_offset):
    try:
        tzoffset = timedelta(seconds=int(str(csv_timestamp_w_offset.tzinfo)[16:-1]))
    except:
        tzoffset = timedelta(seconds=0)
    formatted_timestamp = csv_timestamp_w_offset.replace(tzinfo=None)
    formatted_timestamp += tzoffset
    return formatted_timestamp 

def is_time_between(begin_time, end_time, check_time):
    # If check time is not given, default to current UTC time
    if (begin_time < check_time) and (check_time < end_time):
        return True
    else: # crosses midnight
        return False

# function to check check whether a datapoint is in a known range
def check_cluster(df, clusters, remember_others=False):
    time_obj = df['time']
    agg_list=[] 
    out = False
    check_cluster_col = True if 'in_cluster' in df.index else False     
    for i in range(len(clusters)):       
        # for n in range(len(clusters[i])):
        #     agg_list.append(clusters[i][n])
        local_start_time = clusters[i][0]
        local_end_time = clusters[i][-1]
        check_time = is_time_between(local_start_time, local_end_time, time_obj)
        if check_time:
            out=True
        else:
            if remember_others:
                if check_cluster_col:
                    if df['in_cluster'] == True:
                        out = True
                else:
                    out=False
    return out

def round_and_fill(clusters):
    for cm in range(len(clusters)):   
            # generate the null H0 set:
            inf, sup = clusters[cm][0].replace(second=0), clusters[cm][-1].replace(second=0)
            set_length = (clusters[cm][-1] - clusters[cm][0]).total_seconds()/60
            for element in range(int(set_length)):
                time_incr = timedelta(minutes=element)
                clusters[cm].append(inf+time_incr)
    return clusters


def cluster_assignment(single_side_channel_df, cutofftime, fill=False):
    single_side_channel_df = single_side_channel_df.reset_index()
    active_periods = []
    current_period=[single_side_channel_df['time'].iloc[0]]
    for index,row in single_side_channel_df.iterrows():
        period_member = single_side_channel_df['time'].iloc[index]
        if (period_member - current_period[-1]).total_seconds() < cutofftime:
            current_period.append(period_member)

        else:
            #if len(current_period) > 2:
            active_periods.append(current_period)
            current_period = [period_member]
            #current_cluster.append(cluster_member)
        if index == len(single_side_channel_df) -1 :
            current_period.append(period_member)
            active_periods.append(current_period)
    #option for adding minutes but its time intensive
    if fill:
        active_periods = round_and_fill(active_periods)

    return active_periods



# function that will help me idientify clusters
#generatestartandstoptimes for pltaxvspan
def axvspan_start_stop_color_id(single_side_df):
    axvspairs = []
    single_side_df['cluster_id'] = [0]*len(single_side_df)
    counter = 0
    for index, row in single_side_df.iterrows():
        if index ==0:
            start = single_side_df['time'].iloc[index]
        else:
            if single_side_df['in_cluster'].iloc[index] == single_side_df['in_cluster'].iloc[index-1]:
                single_side_df['cluster_id'].iloc[index] = counter
                pass
            else:
                stop = single_side_df['time'].iloc[index-1]
                counter += 1
                single_side_df['cluster_id'].iloc[index] = counter
                axvspairs.append([single_side_df['in_cluster'].iloc[index-1], start, stop])
                start= single_side_df['time'].iloc[index-1]
    if index==len(single_side_df)-1:
        stop = single_side_df['time'].iloc[index]
        #single_side_df['cluster_id'].iloc[index] = single_side_df['cluster_id'].iloc[index-1]
        axvspairs.append([single_side_df['in_cluster'].iloc[index], start, stop])
    return axvspairs

def axvspan_plotting(list_of_axvspairs):
    for i in range(len(avspairs)):
        if avspairs[i][0]==True:
            shade='red'
        else:
            shade='green'
        plt.axvspan(avspairs[i][1], avspairs[i][2], color=shade, alpha=0.1)
