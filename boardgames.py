#to parse numerical data
import numpy as np

#to parse tabular data
import pandas as pd

#to plot out the data
import matplotlib.pyplot as plt

#to make some basic visualizations
import seaborn as sns

#to make visualizations that flag where data is missing
import missingno as msno

#to search for matching strings in the dataset
import re

#ignore warnings in Python (for simplicity's sake)
import warnings
warnings.filterwarnings("ignore")

#Check out the game details dataset column headers -- this has to be done in chunks, the dataset is too big otherwise.
games_chunk = pd.read_csv("../input/boardgamegeek-reviews/games_detailed_info.csv", index_col=0, delimiter=',', decimal=",", chunksize=5000)
games_df = pd.concat(games_chunk)
print(games_df.columns.values.tolist())

#Create a dataframe of user reviews -- this has to be done in chunks, the dataset is too big otherwise.
reviews_chunk = pd.read_csv('../input/boardgamegeek-reviews/bgg-19m-reviews.csv', delimiter=',', decimal=",", chunksize=5000, index_col=0)
reviews_df = pd.concat(reviews_chunk)
print(reviews_df.columns.values.tolist())

#Remove empty comments (to make the dataframe smaller)
reviews_df = reviews_df.dropna(subset=['comment'])

#Create a subset dataframe of the user reviews, retaining only the columns of interest
reviews_sub_df = reviews_df[['user', 'comment', 'ID', 'name']]

#Create a subset dataframe of the game details, retaining only the columns of interest
games_sub_df = games_df[['id', 'yearpublished', 'boardgamecategory', 'usersrated', 'average', 'Board Game Rank']]

#Create a single merged dataframe, using the BoardGameGeeks game IDs to match up the two datasets.
joined_df = games_sub_df.merge(reviews_sub_df, left_on='id', right_on='ID', how='left')
joined_df.head(20)

#Check for missing values -- a summary of how many missing values are contained within the dataframe. Columns with 0 have no missing data, the remaining columns are missing the number of values listed.
joined_df.isna().sum()

#Check for duplicates in the data (just as a sense-check)
joined_df.duplicated().sum()

#Remove empty IDs. If we can't ID the games across the board, we can't use that row of data.
joined_df = joined_df.dropna(subset=['ID'])

#Remove empty game names. If we don't know what game we're looking at, we can't use that row of data.
joined_df = joined_df.dropna(subset=['name'])

#Remove empty comments. If users didn't leave written reviews of the game, their ranking isn't relevant to our Covid-related investigation.
joined_df = joined_df.dropna(subset=['comment'])

#Get info about the merged dataset (and check if everything looks good)
joined_df.info()

#Years when the games were published, rendered as a histogram
sns.histplot(data=joined_df, x='yearpublished')

cat_heatmap = sns.heatmap(np.asarray[joined_df['boardgamecategory']])
loc, labels = plt.xticks()
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=45)
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=45) # reversed order for y
plt.title("Category Data")

#Visual Missing values rendered as a matrix graph. This will display a sample of 5000 rows of data rather than the entire dataset and only shows the 10 bottom columns that are missing the most values.
msno.matrix(joined_df.sample(5000), labels=True, filter='bottom', n=10, color=(0.1, 0.2, 0.5))

#Show how many games each user has reviewed (because we dropped the rows of ratings without reviews). Displaying only users who have rated >1000 games.
from collections import Counter
input =  joined_df.user
c = Counter( input )
cf = c.most_common
listToStr = ' '.join([str(elem) for elem in cf()])
listToStr_over1k = listToStr[0:3046]
print("Username and number of reviews:", listToStr_over1k)

#Show most common words and phrases from the user reviews. Displaying only the first 1000 characters, due to memory.
input =  joined_df.comment
c2 = Counter( input )
cf2 = c2.most_common
listToStr = ' '.join([str(elem) for elem in cf2()])
listToStr_1250 = listToStr[0:1250]
print(listToStr_1250)

#Break out all the game category values (subgenres, as determined by the site users) and de-dupe
category_df = joined_df['boardgamecategory']
category_df.drop_duplicates(keep='first')

#Print the game category values
print(category_df.values)

#Break out all the game mechanics values and de-dupe
mechanics_df = joined_df['boardgamemechanic']
mechanics_df.drop_duplicates(keep='first')

#Print the game mechanics values
print(mechanics_df.values)

#Create a subset dataframe consisting only of game names and game reviews
reviews_df = joined_df[['comment','name']]

#Use Regex to search the game reviews for variations on "coronavirus" or "covid"
search = re.compile(r'([ck][ao0]?r[ao0]n[ao]|c[o0]vid).{0,80}?(v[ai]i?r[aou]s|flu)|(v[ai]i?r[aou]s|flu).{0,80}?([ck][ao0]?r[ao0]n[ao]|c[o0]vid)')
output = []

for eachReview in reviews_df.comment:
    if search.search(eachReview):
        output.append(eachReview)

print(output)

#Count number of game review results
output_count = tuple(output)
len(output_count)

#List the game names associated with each user review that matched the previous Regex
output_names = []

for eachReview in reviews_df.comment:
    if search.search(eachReview):
        output_names.append(reviews_df.name)

print(output_names)

#Count number of game name results
outputnames_count = tuple(output_names)
len(outputnames_count)

#De-dupe the list of game name results
from collections import Counter
input =  tuple(output_names)
c2 = Counter( input )
cf2 = c2.most_common
listToStr_gameNames = ' '.join([str(elem) for elem in cf2()])
print(listToStr_gameNames)

#Another way to try de-duping the list of game name results
gamename_count = pd.Series(output_name).value_counts(ascending=True)
print(gamename_count)

#One last way to try to de-dupe the list of game names
sortedTup = [tuple(sorted(val)) for val in tupList]
tupListWoDup = list(set(sortedTup))
# Printing the list of tuples 
print("After removing duplicates : " + str(tupListWoDup))