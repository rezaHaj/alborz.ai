import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt


def make_data(num_events=2500):
    start_date = datetime.now() - timedelta(days=90)  # about 3 months ago
    end_date = datetime.now()
    
    event_ids = range(1, num_events + 1)
    user_ids = [random.randint(1, 300) for _ in range(num_events)]
    

    timestamps = [
        start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        for _ in range(num_events)
    ]
    timestamps = [t.strftime("%Y-%m-%d %H:%M:%S") for t in timestamps]
    

    platforms = [random.choice(['web', 'ios', 'android']) for _ in range(num_events)]
    

    event_types = random.choices(
        ['login', 'play video', 'like', 'comment', 'logout'],
        weights=[0.15, 0.4, 0.25, 0.15, 0.05],
        k=num_events
    )
    
    video_ids = [
        random.randint(1000, 2000) if et in ['play video', 'like', 'comment'] else None
        for et in event_types
    ]
    
    video_durations = [
        random.randint(30, 600) if et == 'play video' else None
        for et in event_types
    ]
    watch_times = [
        random.randint(5, vd) if vd else None
        for vd in video_durations
    ]
    
    df = pd.DataFrame({
        'event_id': event_ids,
        'user_id': user_ids,
        'timestamp': timestamps,
        'platform': platforms,
        'event_type': event_types,
        'video_id': video_ids,
        'watch_time_sec': watch_times,
        'video_duration_sec': video_durations
    })
    return df

data_df = make_data(3000)

data_df['timestamp'] = pd.to_datetime(data_df['timestamp'])

score_map = {
    'comment': 5,
    'like': 3,
    'play video': 1,
    'login': 0,
    'logout': 0
}
data_df['engagement_score'] = data_df['event_type'].map(score_map)


print("Sample rows from the dataset:")
print(data_df.head())


data_df['date'] = data_df['timestamp'].dt.date
daily_scores = data_df.groupby(['date', 'platform'])['engagement_score'].sum().reset_index()


heatmap_table = daily_scores.pivot(index='date', columns='platform', values='engagement_score').fillna(0)

print("\nSample of daily pivot table for Heatmap:")
print(heatmap_table.head())


plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_table, cmap='YlOrRd')
plt.title('Daily User Engagement Score by Platform')
plt.xlabel('Platform')
plt.ylabel('Date')
plt.tight_layout()

plt.savefig("heatmap_engagement.png")
plt.show()
# khaste nbashid ostad. :)