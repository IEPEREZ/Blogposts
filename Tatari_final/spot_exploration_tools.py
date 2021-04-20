import pandas as pd
import matplotlib.pyplot as plt
from datetime import timezone
from datetime import datetime, timedelta
import dateutil
import pickle
import period_identification

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

df = pd.read_csv('assignment-analyst-1-spot-data.csv', parse_dates = ["time"])
df['program'] = df['program'].fillna('')
#df = df[:int(len(df)*0.5)]
df_east = df[df['feed'] == 1]
df_west = df[df['feed'] == 2]


print(df.head())
print(df.creative_id.unique())
print(df.duration.unique())
print(df.network_code.unique())
print(df.program.unique())
print(df.rotation_days.unique())
print(df.is_dual_feed.unique())


live_shows = [
        "NBA CHAMPIONS", "Monday Night Football" , 'NBA GAMETIME',  
        "Thursday Night Football", "UFC FIGHT NIGHT", "NBA BASKETBALL", 
        'NHL Tonight Pre-Game Skate <Live> 6P', 'NHL Tonight <Live>', 
        'NHL Tonight With Bonus Coverage <Live>', 'NHL Tonight <Live>',
        'Regular Season Hockey on NHL Network <Live Game>', 
    ]


live_shows = "|".join(live_shows)

df_east_live = df_east[df_east['program'].str.contains(live_shows)]
df_west_live = df_west[df_west['program'].str.contains(live_shows)]

df_east_live['time'] = df_east_live['time'].apply(lambda x: period_identification.format_timestamps(x))
df_west_live['time'] = df_west_live['time'].apply(lambda x: period_identification.format_timestamps(x))

print(df_east_live[:5])
print(df_west_live[:5])


