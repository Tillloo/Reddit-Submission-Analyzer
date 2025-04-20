# Reddit-Submission-Analyzer

For this project, we chose to look at reddit submissions to see if we could analyze what makes a good/popular submission. We decided to look at two subsets of the Reddit Comment Corpus: news-related subreddits and long form story-related subreddits. The best environment to run this project on is Linux.
## Packages needed for data preprocessing:
- textstat
- nltk / nltk.sentiment
- torch (pytorch)
- scipy
## Packages needed in general:
- pandas
- numpy
- matplotlib

## Data Preprocessing Pipeline:

0.1: reddit.py: Using the given code snippet from the course page, we extracted specifically submissions from 10 subreddits.\
0.2: gzip_to_csv: Convert the gzip partitions to pandas-workable csv files.

---

(Note: The above two steps are not technically part of the pipeline. They're more like steps needed to get the ball rolling.)\
Two sample set of our data have also been provided for testing purposes (news_sample.csv and story_sample.csv).

---
#### 1: format_csv:
The first step in cleaning, basically strips any outliers/unwanted data such as:\
-Filtering to only relevant columns (subreddit, title, score, etc.)\
-Dropping NA/NaN values in text fields, as well as posts that have been [deleted] or [removed] and Megathread posts\
-Reformatting unix time into readable datetime

-As input, provide an input csv, output file name, and either a 1 or 0 (providing a 1 for this field includes post body text, while providing a 0 does not)\
Examples:\
`python3 format_csv.py story.csv filtered_story.csv 1`\
`python3 format_csv.py news.csv filtered_news.csv 0`

#### 2: readability_scores.py: 
Used to compute various NLP features of each submission. We decided to analyze:\
-Flesch Reading Ease: An estimate of the ease of readability of the text (either title text or body text)

| Score  | Ease Of Reading  |
|--------|------------------|
| 90-100 | Very Easy        |
| 80-89  | Easy             |
| 70-79  | Fairly Easy      |
| 60-69  | Standard         |
| 50-59  | Fairly Difficult |
| 30-49  | Difficult        |
| <30    | Very Confusing   |

-Average grade level required to understand the text\
-Average time to read the text

Example: (Providing a 1 here analyzes readability of body text, and a 0 analyzes title text.)\
`python3 readability_scores.py filtered_story.csv readability_story.csv 1`\
`python3 readability_scores.py filtered_news.csv readability_news.csv 0`

#### 3: sentiments.py: 
Used to perform sentiment analysis on text. We use two models to achieve this:\
-NLTK's Sentiment Intensity Analyzer (SIA) using the vader-lexicon sentiment dictionary. This approach looks at scores for individual words and aggregates them to a final score.\
-Hugging Face/CardiffNLP's twitter-roBERTa, a machine learning model based on ~58M tweets from Twitter designed to analyze sentiment of an entire text block (taking into account things like context)

Example: (Providing a 1 here analyzes sentiments of body text, and a 0 analyzes title text.)\
`python3 sentiments.py readability_story.csv final_story.csv 1`\
`python3 sentiments.py readability_news.csv final_news.csv 0`

#### 4: statistics.py: 
Where all the analysis takes place (there is also a bit of data transformation happening here, done as needed to improve accuracy of statistical results). Running the code will output a csv corresponding to 1/0 passed for use in visualizations.py.

Example: (Providing a 1 here analyzes sentiments of body text, and a 0 analyzes title text.)\
`python3 statistics.py final_story.csv 1`\
`python3 statistics.py final_news.csv 0`

#### 5. visualizations.py
Where all the graphing takes place. The file creates graphs based on the final csv files and puts them in a folder named 'output', so no input is required.

Example: \
`python3 visualizations.py`
