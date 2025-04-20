import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy import stats
import seaborn as sns

#output_folder = sys.argv[1]
output_folder = 'stats_results'
news = pd.read_csv('data_files/news_final.csv')
story = pd.read_csv('data_files/story_final.csv')

#do a bit of sentiment column processing bc I forgot to do it in sentiments.py oops

news.dropna(subset=['polarity_score'], inplace = True)
story.dropna(subset=['polarity_score'], inplace = True)
news.dropna(subset=['roberta_score'], inplace = True)
story.dropna(subset=['roberta_score'], inplace = True)

def get_time_of_day(x):
    if 5 <= x < 12: #5am to 12pm
        return "morning"
    elif 12 <= x < 20:
        return "day"
    else: #10pm to 4am
        return "night"


def simplify_sentiment(pol_sent, pol_score, rob_sent, rob_score):
    #if results are equal, take the highest score, otherwise, assignment highest scoring result to text
    if pol_sent == rob_sent:
        if pol_score > rob_score:
            return pol_sent, pol_score
        else:
            return pol_sent, rob_score
    elif pol_sent != rob_sent:
        if pol_score > rob_score:
            return pol_sent, pol_score
        else:
            return rob_sent, rob_score

def get_sentiment(text):
    text = str(text)
    return text[2:5]

def get_score(text):
    text = str(text)
    return float(text[8:-1])

def get_numpy_score(text):
    text = str(text)
    return float(text[19:-2])

news['polarity_sentiment'] = news['polarity_score'].apply(lambda x: get_sentiment(x))
news['polarity_score'] = news['polarity_score'].apply(lambda x: get_score(x))
news['roberta_sentiment'] = news['roberta_score'].apply(lambda x: get_sentiment(x))
news['roberta_score'] = news['roberta_score'].apply(lambda x: get_numpy_score(x))

story['polarity_sentiment'] = story['polarity_score'].apply(lambda x: get_sentiment(x))
story['polarity_score'] = story['polarity_score'].apply(lambda x: get_score(x))
story['roberta_sentiment'] = story['roberta_score'].apply(lambda x: get_sentiment(x))
story['roberta_score'] = story['roberta_score'].apply(lambda x: get_numpy_score(x))

story[['sentiment', 'sent_score']] = story.apply(lambda x: simplify_sentiment(x['polarity_sentiment'],
                                                                       x['polarity_score'],
                                                                       x['roberta_sentiment'],
                                                                       x['roberta_score']),
                                                                       axis='columns', result_type='expand')
story = story.drop(columns = ['polarity_sentiment', 'polarity_score', 'roberta_sentiment', 'roberta_score'])

news[['sentiment', 'sent_score']] = news.apply(lambda x: simplify_sentiment(x['polarity_sentiment'],
                                                                       x['polarity_score'],
                                                                       x['roberta_sentiment'],
                                                                       x['roberta_score']),
                                                                       axis='columns', result_type='expand')
news = news.drop(columns = ['polarity_sentiment', 'polarity_score', 'roberta_sentiment', 'roberta_score'])

#do a bit more cleaning since data is extremely right skewed due to volume of low upvote posts
news = news.drop(news[news['score'] > 5000].index)
news = news.drop(news[news['score'] < 10].index) #good range i think...
news = news.drop(news[news['num_comments'] < 1].index)

story = story.drop(story[story['score'] > 5000].index)
story = story.drop(story[story['score'] < 10].index) #good range i think...
story = story.drop(story[story['num_comments'] < 1].index)

#transform skewed values:
#news['score'] = news['score'].apply(lambda x: np.log2(np.sqrt(x)))
#story['score'] = story['score'].apply(lambda x: np.log2(np.sqrt(x)))
#news['num_comments'] = news['num_comments'].apply(lambda x: np.log2(np.sqrt(x)))
#story['num_comments'] = story['num_comments'].apply(lambda x: np.log2(np.sqrt(x)))

#create some useful subsets/categories:
#get hour of posting time
news['hour'] = news['datetime'].apply(lambda x: int(x[11:13]))
story['hour'] = story['datetime'].apply(lambda x: int(x[11:13]))

#categoricals
#posted in the morning/night
story['time_posted'] = story['hour'].apply(get_time_of_day)
news['time_posted'] = news['hour'].apply(get_time_of_day)
news_morning = news[news['time_posted'] == 'morning']
news_night = news[news['time_posted'] == 'night']
story_morning = story[story['time_posted'] == 'morning']
story_night = story[story['time_posted'] == 'night']

#pos/neu/neg sentiment
news_neg = news[news['sentiment'] == 'neg']
news_pos = news[news['sentiment'] == 'pos']
news_neu = news[news['sentiment'] == 'neu']
story_neg = story[story['sentiment'] == 'neg']
story_pos = story[story['sentiment'] == 'pos']
story_neu = story[story['sentiment'] == 'neu']

#separate based on school -> elementary: <5, middle: 5 <= grade <= 8, high: 9+
news_elementary = news[news['grade_level'] < 5]
news_middle = news[(news['grade_level'] <= 8) & (news['grade_level'] >= 5)]
news_high = news[news['grade_level'] > 8]

story_elementary = story[story['grade_level'] < 5]
story_middle = story[(story['grade_level'] <= 8) & (story['grade_level'] >= 5)]
story_high = story[story['grade_level'] > 8]

#story length (only for story.csv)
short_story = story[story['reading_time'] < 8.25]
long_story = story[story['reading_time'] > 8.25]

#ease of reading (split between easy and difficult reading, the upper half of 'standard' reading ease is classified as easy)
easy_reading = story[story['reading_ease'] >= 65]
hard_reading = story[story['reading_ease'] < 65]
easy_reading_news = story[story['reading_ease'] >= 65]
hard_reading_news = story[story['reading_ease'] < 65]


news.to_csv("data_files/news_visualizations.csv")
story.to_csv("data_files/story_visualizations.csv")

#lets start with looking at the news subreddits:

#does a neg/pos sentiment score influence the number of comments?
print("news tests:")
print("neg/pos sentiment vs num_comments p-value:")
print(stats.mannwhitneyu(news_neg['num_comments'], news_pos['num_comments'], alternative='two-sided').pvalue) #significant

#does a neg/pos sentiment score influence the score?
print("neg/pos sentiment vs score p-value:")
print(stats.mannwhitneyu(news_neg['score'], news_pos['score'], alternative='two-sided').pvalue) #insignificant


print("time of day vs score:")
print(stats.mannwhitneyu(news_morning['score'], news_night['score'], alternative='two-sided').pvalue) #both significant for day/night fields given above, but no indication of which direction influences these fields
print("time of day vs comments:")
print(stats.mannwhitneyu(news_morning['num_comments'], news_night['num_comments'], alternative='two-sided').pvalue)

print("reading ease vs score p-value:")
print(stats.mannwhitneyu(easy_reading_news['score'], hard_reading_news['score'], alternative='two-sided').pvalue)
print("reading ease vs comments p-value:")
print(stats.mannwhitneyu(easy_reading_news['num_comments'], hard_reading_news['num_comments'], alternative='two-sided').pvalue)

print("grade level vs score p-value:")
print(stats.mannwhitneyu(news_elementary['score'], news_high['score'], alternative='two-sided').pvalue)
print("grade level vs comments p-value:")
print(stats.mannwhitneyu(news_elementary['num_comments'], news_high['num_comments'], alternative='two-sided').pvalue)

#now lets look at story subreddits:

print("story tests:")

print("neg/pos sentiment vs num_comments p-value:")
print(stats.mannwhitneyu(story_neg['num_comments'], story_pos['num_comments'], alternative='two-sided').pvalue)
print("neg/pos sentiment vs score p-value:")
print(stats.mannwhitneyu(story_neg['score'], story_pos['score'], alternative='two-sided').pvalue)

print("grade level vs score p-value:")
print(stats.mannwhitneyu(story_elementary['score'], story_high['score'], alternative='two-sided').pvalue)
print("grade level vs comments p-value:")
print(stats.mannwhitneyu(story_elementary['num_comments'], story_high['num_comments'], alternative='two-sided').pvalue)

print("reading time vs score p-value:")
print(stats.mannwhitneyu(short_story['score'], long_story['score'], alternative='two-sided').pvalue)
print("reading time vs comments p-value:")
print(stats.mannwhitneyu(short_story['num_comments'], long_story['num_comments'], alternative='two-sided').pvalue)

print("reading difficulty vs score p-value:")
print(stats.mannwhitneyu(easy_reading['score'], hard_reading['score'], alternative='two-sided').pvalue)
print("reading difficulty vs comments p-value:")
print(stats.mannwhitneyu(easy_reading['num_comments'], hard_reading['num_comments'], alternative='two-sided').pvalue)


