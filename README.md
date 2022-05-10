# info664-final-project
Assessing how frequently board game players refer to Covid-19 in their reviews on BoardGameGeeks.com, and whether there are any identifiable patterns in the games they're choosing to play.

The dataset of game data and user reviews is too large to include in github, but can be found at https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews. The relevant files used in this project are games_detailed_info.csv and bgg-19m-reviews.csv. Be forewarned that the sheer size of the data makes using Kaggle's notebook and/or Jupyter Notebook almost impossible. I found the greatest success using JupyterLab in the Google Cloud AI console, which had more processing capacity to handle the dataset (most of the time -- you should still expect some crashing, or messages indicating

    IOPub data rate exceeded.
    The Jupyter server will temporarily stop sending output
    to the client in order to avoid crashing it.
    To change this limit, set the config variable
    `--ServerApp.iopub_data_rate_limit`.

    Current values:
    ServerApp.iopub_data_rate_limit=1000000.0 (bytes/sec)
    ServerApp.rate_limit_window=3.0 (secs)

To load the dataset to Google Cloud AI directly from Kaggle, open a Kaggle notebook using the dataset and click the ellipsis at the top right of the page. Select "Open in Google Notebooks" and follow the prompts to upgrade to Google Cloud AI Platform Notebooks. The upgrade comes with $300 credit worth of use time.
