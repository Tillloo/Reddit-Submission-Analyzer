import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# Load the data
news = pd.read_csv("data_files/news_visualizations.csv")
story = pd.read_csv("data_files/story_visualizations.csv")

# Figures
#
#

# Scatter plots for Reading Time vs Comments (news first then story)
story = story[story['num_comments'] < 1250]

story_temp = story[story['reading_time'] < 100]
news_temp = news[news['num_comments'] < 10000]

# News Reading Times vs Comments Scatter Plot
plt.figure(figsize=(8, 6))
plt.scatter(news_temp['reading_time'], news_temp['num_comments'], alpha=0.6, color='purple')
plt.title("Reading Time vs. Comments (News)")
plt.xlabel("Reading Time (minutes)")
plt.ylabel("Comments")
plt.savefig('output/Reading Time vs. Comments (news).png')
plt.show()

# Story Reading Times vs Comments Scatter Plot
plt.figure(figsize=(8, 6))
plt.scatter(story_temp['reading_time'], story_temp['num_comments'], alpha=0.6, color='purple')
plt.title("Reading Time vs. Comments (Story)")
plt.xlabel("Reading Time (minutes)")
plt.ylabel("Comments")
plt.savefig('output/Reading Time vs. Comments (Story).png')
plt.show()



# Bar graphs of Sentiment vs Count

sentiment_counts = news['sentiment'].value_counts()

# Bar graph of Sentiment vs Count, News compared to Story
plt.figure(figsize=(10, 6))
sentiment_counts = pd.concat([
    news['sentiment'].value_counts().rename('News'),
    story['sentiment'].value_counts().rename('Story')
], axis=1)
sentiment_counts.rename(index={'neg': 'Negative', 'pos': 'Positive', 'neu': 'Neutral'}, inplace=True)
sentiment_counts.plot(kind='bar', title='Sentiment Distribution', rot=0)
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('output/Sentiment Distribution.png')
plt.show()


# Filter to only include 'neg' and 'pos'
sentiment_counts = sentiment_counts.loc[['Negative', 'Positive']]

# Bar graph of Sentiment vs Count, News compared to Story (only negative and postive sentiments)
plt.figure(figsize=(10, 6))
sentiment_counts.plot(kind='bar', title='Sentiment Distribution (Positive and Negative)', rot=0)
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('output/Sentiment Distribution (Positive and Negative).png')
plt.show()





news = news.drop(news[news['grade_level'] > 15].index)
story = story.drop(story[story['grade_level'] > 15].index)



# Create a figure with two subplots for better comparison
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Histogram of Reading Level (with custom bins to avoid gaps)
ax[0].hist(news['grade_level'], bins=16, alpha=0.7, color='purple', edgecolor='black')
ax[0].set_title("Distribution of Reading Levels")
ax[0].set_xlabel("Reading Level (e.g., Flesch Reading Ease Score)")
ax[0].set_ylabel("Frequency")

# Histogram of Score
ax[1].hist(news['score'], bins=16, alpha=0.7, color='green', edgecolor='black')
ax[1].set_title("Distribution of Scores")
ax[1].set_xlabel("Score")
ax[1].set_ylabel("Frequency")

plt.tight_layout()
plt.savefig("output/Histogram Reading Level and Score (News)")
plt.show()

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Histogram of Reading Level (with custom bins to avoid gaps)
ax[0].hist(story['grade_level'], bins=16, alpha=0.7, color='purple', edgecolor='black')
ax[0].set_title("Distribution of Reading Levels")
ax[0].set_xlabel("Reading Level (e.g., Flesch Reading Ease Score)")
ax[0].set_ylabel("Frequency")

# Histogram of Score
ax[1].hist(story['score'], bins=16, alpha=0.7, color='green', edgecolor='black')
ax[1].set_title("Distribution of Scores")
ax[1].set_xlabel("Score")
ax[1].set_ylabel("Frequency")

plt.tight_layout()
plt.savefig("output/Histogram Reading Level and Score (Story)")
plt.show()


filtered_posts_story = story[story['score'] > 1000]
filtered_posts_story = story[story['reading_time'] > 150]

# Plot the reading time for posts with score greater than 1000
plt.figure(figsize=(10, 6))
plt.hist(filtered_posts_story['reading_time'], bins=13, alpha=0.7, color='red', edgecolor='black')
plt.title("Reading Time for Posts with Score > 1000 (Story)")
plt.xlabel("Reading Time (minutes)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("output/Reading Time for Posts with Score Over 1000 (Story)")
plt.show()

filtered_posts_news = news[news['score'] > 1000]

# Plot the reading time for posts with score greater than 1000
plt.figure(figsize=(10, 6))
plt.hist(filtered_posts_news['reading_time'], bins=13, alpha=0.7, color='red', edgecolor='black')
plt.title("Reading Time for Posts with Score > 1000 (News)")
plt.xlabel("Reading Time (minutes)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("output/Reading Time for Posts with Score Over 1000 (News)")
plt.show()



plt.figure(figsize=(14, 6))


news['datetime'] = pd.to_datetime(news['datetime'])

# Extract the hour from the 'timestamp'
news['hour'] = news['datetime'].dt.hour

# Count the number of posts for each hour
hourly_activity_news = news['hour'].value_counts().sort_index()

# Plot the activity (posts) per hour
plt.subplot(1, 2, 1)
hourly_activity_news.plot(kind='bar', color='skyblue', alpha=0.7)
plt.title("Posts Activity Per Hour (news)")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Posts")
plt.xticks(rotation=0)
plt.tight_layout()


story['datetime'] = pd.to_datetime(story['datetime'])

# Extract the hour from the 'timestamp'
story['hour'] = story['datetime'].dt.hour

# Count the number of posts for each hour
hourly_activity_story = story['hour'].value_counts().sort_index()

# Plot the activity (posts) per hour
plt.subplot(1, 2, 2)
hourly_activity_story.plot(kind='bar', color='salmon', alpha=0.7)
plt.title("Posts Activity Per Hour (story)")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Posts")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("output/Posts per Hour")
plt.show()



plt.figure(figsize=(10, 6))

# Calculate the counts for morning and night posts for both news and story
news_morning_and_nights = news.drop(news[news['time_posted'] == 'day'].index)
story_morning_and_nights = story.drop(story[story['time_posted'] == 'day'].index)

news_time_counts = news_morning_and_nights['time_posted'].value_counts()
story_time_counts = story_morning_and_nights['time_posted'].value_counts()

# Create a bar plot with both categories (news and story) for morning vs night
time_counts = pd.DataFrame({
    'News': news_time_counts,
    'Story': story_time_counts
})

# Plot the bar chart
time_counts.plot(kind='bar', stacked=False, title='Number of Posts in the Morning vs Night', color=['skyblue', 'orange'])

# Add labels and title
plt.xlabel('Time of Day')
plt.ylabel('Number of Posts')
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("output/Number of Posts During the Day")
plt.show()
