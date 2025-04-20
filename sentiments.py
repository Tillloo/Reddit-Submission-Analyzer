import pandas as pd
import sys
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon') #download sentiment dict

# Sentiment Analysis columns calculated here
# A fair warning before running: this took from 10pm to around 8am the next day to fully complete on the
# filtered dataset, but it worked!

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

#input_dir = sys.argv[1]
#output_dir = sys.argv[2]
#include_body = sys.argv[3]

input_dir = 'output.csv'
output_dir = 'output.csv'
include_body = '1'

sia = SentimentIntensityAnalyzer()

data = pd.read_csv(input_dir)
#story = pd.read_csv('data_files/story_simplified.csv')
#news = pd.read_csv('data_files/news_simplified.csv')


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
tokenizer.model_max_length = 512
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def roberta_analyze(string):
    string = str(string)
    encoded_text = tokenizer(string, return_tensors='pt', truncation = True)
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    #return [ ['neg', scores[0]] , ['neu', scores[1]] , ['pos', scores[2]] ]
    #get highest value for string
    if abs(scores[0]) > abs(scores[1]) and abs(scores[0]) > abs(scores[2]):
        return ['neg', scores[0]]
    elif abs(scores[1]) > abs(scores[0]) and abs(scores[1]) > abs(scores[2]):
        return ['neu', scores[1]]
    elif abs(scores[2]) > abs(scores[1]) and abs(scores[2]) > abs(scores[0]):
        return ['pos', scores[2]]

def sia_analyze(string):
    string = str(string)
    scores = sia.polarity_scores(string)
    # get highest value for string
    if abs(scores['neg']) > abs(scores['neu']) and abs(scores['neg']) > abs(scores['pos']):
        return ['neg', scores['neg']]
    elif abs(scores['neu']) > abs(scores['neg']) and abs(scores['neu']) > abs(scores['pos']):
        return ['neu', scores['neu']]
    elif abs(scores['pos']) > abs(scores['neu']) and abs(scores['pos']) > abs(scores['neg']):
        return ['pos', scores['pos']]

if include_body == '1':
    data['polarity_score'] = data['selftext'].apply(lambda x: sia_analyze(x))
    data['roberta_score'] = data['selftext'].apply(lambda x: roberta_analyze(x))
else:
    data['polarity_score'] = data['title'].apply(lambda x: sia_analyze(x))
    data['roberta_score'] = data['title'].apply(lambda x: roberta_analyze(x))

data.to_csv(output_dir, index=False)
#story.to_csv('data_files/story_withsentiments.csv', index=False)
#news.to_csv('data_files/news_withsentiments.csv', index=False)