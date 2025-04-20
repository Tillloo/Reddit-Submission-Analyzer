import pandas as pd
import textstat
import re
import sys

# Sample DataFrame

#flesch reading ease:
#90-100 very easy
#80-89 easy
#70-79 fairly easy
#60=69 standard
#50-59 fairly difficult
#30-49 difficult
#less than 30 very confusing

#calculate grade level is the equivalent reading level of that grade (ie: a nth grader would be expected to read text at that level)



# Function to calculate readability score
def calculate_readability_flesch(text):
    return textstat.flesch_reading_ease(text)

#def calculate_readability_coleman(text):
 #   return textstat.coleman_liau_index(text)

#def calculate_readability_automated(text):
 #   return textstat.automated_readability_index(text)

def calculate_grade_level(text):
    return textstat.text_standard(text, float_output = True)

def calculate_reading_time(text):
    return textstat.reading_time(text)

# Function to check if a title contains only alphabet characters and spaces
def is_alphabetic(title):
    if isinstance(title, str):  # Only apply regex if title is a string
        return bool(re.match(r'^[a-zA-Z\s.,!?&%\[\]]+$', title))
    return False  # Return False for non-string values (e.g., NaN, numbers)

input = sys.argv[1]
output = sys.argv[2]
include_body = sys.argv[3]

data = pd.read_csv(input)

# Filter the DataFrame to include only titles with alphabetic characters and spaces
data = data[data['title'].apply(is_alphabetic)] 


# There are still almost 90000 rows in the filtered dataframe
#print(df_filtered.shape[0])

# Calculate readability scores for the filtered DataFrame
if include_body == 1:
    data['reading_ease'] = data['selftext'].apply(calculate_readability_flesch)
    data['reading_time'] = data['selftext'].apply(calculate_reading_time)
    data['grade_level'] = data['selftext'].apply(calculate_grade_level)
else:
    data['reading_ease'] = data['title'].apply(calculate_readability_flesch)
    data['reading_time'] = data['title'].apply(calculate_reading_time)
    data['grade_level'] = data['title'].apply(calculate_grade_level)

data = data[data['grade_level'] < 15]

data.to_csv(output, index = False)
#story.to_csv('data_files/story_final.csv', index=False)
#news.to_csv('data_files/news_final.csv', index=False)