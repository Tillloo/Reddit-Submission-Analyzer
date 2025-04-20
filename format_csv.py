import pandas as pd
import sys
#take all raw data and clean it here
input_dir = sys.argv[1]
output_dir = sys.argv[2]
include_body = sys.argv[3]

data = pd.read_csv(input_dir)
#data = pd.read_csv('data_files/story.csv')
#news = pd.read_csv('data_files/news.csv')

#do a bit more cleaning since data is extremely right skewed due to volume of low upvote posts
data = data.drop(data[data['score'] > 5000].index)
data = data.drop(data[data['score'] < 10].index) #good range i think...
data = data.drop(data[data['num_comments'] < 1].index)


if include_body == '1':
    # get relevant cols
    data = data[['subreddit', 'created_utc', 'month', 'score', 'num_comments', 'title', 'selftext']]
    # drop rows where relevant fields are empty
    data.dropna(subset=['title', 'selftext'], inplace=True)
    # filter deleted/no content posts
    data.drop(data[data['title'] == '[deleted by user]'].index, inplace=True)
    data.drop(data[data['selftext'] == '[removed]'].index, inplace=True)
    data.drop(data[data['selftext'] == '[deleted]'].index, inplace=True)
    # get length of relevant text body
    data['length'] = data['selftext'].apply(lambda x: len(str(x)))
else:
    # get relevant cols
    data = data[['subreddit', 'created_utc', 'month', 'score', 'num_comments', 'title']]
    # drop rows where relevant fields are empty
    data.dropna(subset=['title'], inplace=True)
    # filter deleted/no content posts
    data.drop(data[data['title'] == '[deleted by user]'].index, inplace=True)
    # get length of relevant text body
    data['length'] = data['title'].apply(lambda x: len(str(x)))


#filter duplicates/spam posters
data.drop_duplicates(subset=['title'], inplace= True)

#convert utc to time of posting
#data['datetime'] = data['created_utc'].apply(lambda x: pd.to_datetime(x, unit='s'))
#data.drop(columns=['created_utc'], inplace=True)
#get hour of posting time
data['hour'] = data['datetime'].apply(lambda x: int(str(x)[11:13]))


#filter megathreads (more common in story subreddits)
data.drop(data[data['title'].str.contains("megathread|Megathread|MEGATHREAD")].index, inplace=True)

#write to csv
data.to_csv(output_dir, index=False)