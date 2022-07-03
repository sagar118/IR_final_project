# End-to-End Information Retrieval (IR) Project
The aim of the project was to create an end-to-end web search engine along with an analytics dashboard. The search engine used covid and vaccine twitter tweets for indexing and used the Okapi BM 25 model to retrieve relevant tweets for a given query. The backend was built in flask, as for the analytics dashboard, we used Plotly.js for innovative story telling and interactive data plots.

## The overall structure of the search is as follows:
- Technologies/frameworks used in frontend: Plotly.js, CSS and HTML.
- Technologies/frameworks used in backend: Flask, Solr, NLTK, Keras, Flair

## Dataset:
- At lease 50,000 tweets in total with not more that 15% being retweets.
  a. At least 500 tweets per POI(7,500 total for all 15 POIs). Out of the 500 tweets per POI, at least 50 related to Covid-19 and the Covie-19 vaccines.
  b. At least 32,500 tweets from the general population, and related to the Covid-19 vaccines.
  c. The rest 10,000 tweets must be replies to either point b or point a, constrained by:
    - At least 1,500 tweets from b should have 1 reply
    - At lest 10 replies or a minimum of 300 Covid-19 related tweets by the POI (Minimum 3,000 replies in total for all POI)
- At a high level, there are:
  - At least 5,000 tweets per language i.e., English, Hindi and Spanish
  - At least 5,000 tweets per country

Tweets from 5 POIs per country, where
  - 1 of the POIs is the official government health agency of the country
  - Rest of the POIs should be from the current ruling or opposition party, where 1 of them should be the president/prime minister of the country
In total, there are at least 15 POIs.

## The User Experience Flow:
Upon entering the website, the user is presented with a clean interface to enter a query. This is rendered via HTML and CSS. Upon entering the query, the query is sent to the flask server, where the following happens:
1. We perform stop word removal for all languages.
2. The cleaned query is then sent to Solr to retrieve the appropriate results.
3. Once the “all” the results are retrieved, we compute the global statistics and create a view for the search query result page. The following graphs are generated based on the query and filters:
  a. Tweet Count of POIs and General Population for the query.
  b. Language tweet count.
  c. Country-wise tweet count.
  d. Tweet count for POIs whose tweets have been retrieved.
4. We also present the following filters to the user to narrow down the tweets they are looking for:
  a. Language wise tweets.
  b. Country wise tweets.
  c. POI name wise tweets.
5. Once the graphs are generated, we then take the top 40 tweets to present to the user.
  a. If POI tweets are available, the top tweets are dominated by those, followed by the general population tweets. If we have 40 tweets by POIs, all tweets will be from POIs.
6. The following components are displayed as part of the tweet:
  a. User-name: If available, otherwise Twitter User (POI names are always available, hence POI name will always be present).
  b. If the tweet is by a POI, then a hyperlink to the tweet will be present.
  c. Whether a user is verified or not.
  d. The tweet text.
  e. The tweet sentiment and the probability of the sentiment.
  f. Best positive reply if present, best negative reply if present.

This summarizes the search page view
Moving on the Analytics dashboard (Overview Page), we have precomputed the required statistics and loaded them before serving it to the user. Here are the graphs that are presented there:

1. Overall count of tweets per country.
2. Overall count of tweets per POI.
3. Average sentiment for covid and vaccine by general population
4. Vaccine Hesitancy word cloud
5. Percentage of tweet as per Vaccine/Covid/Neither.
6. Percentage of tweet as per language.

We have precomputed the sentiment separately and uploaded to Solr. The following methods were used to do sentiment analysis for the different languages.

1. English: We use a python library called flair, which is a state-of-the-art NLP library that performs sentiment analysis for a given dataset. It handles Named Entity Recognition at the backend and gives us the sentiment probability for a given tweet.
2. Hindi: We used a keras LSTM model to predict the sentiment of a given tweet. We used a publicly available data for creating the training and testing dataset.
3. Spanish: We used an off-the shelf library called sentiment-analysis-spanish. It readily gave us the sentiments without any need for training.

Once the sentiments were computed, the dataset was transformed to fit the narrative in the analytics dashboard.
For vaccine hesitancy we tried to find keywords that indicates towards vaccine hesitancy and tried to find them in our tweets. If found, we classified those tweets as vaccine hesitancy. Some of those keywords are: 
“mybodymychoice”, “NoVaccineForMe”, “NoForcedVaccines”, “stopmandatoryvaccination”, “forcedvaccines”, “covidvaccineispoison”, “VaccinesAreNotTheAnswer”, “medicalfreedomofchoice”, etc. In total there were 55 keywords we used to find the results.

Based on the tweets that were marked true for vaccine hesitancy, we tried to clean the tweet text and create a word cloud of the words that help us understand the most frequent words used in those kinds of tweets.

Finally, we have created another dashboard for POI analysis. Here are the graphs displayed over there (Based on filter on POI names):
1. Type of tweets count (Vaccine/Covid/Neither)
2. Overall average sentiment for POI.
3. Calendar Heatmap for Date-wise number for POI.
4. Curve for new Covid cases based on country, upon which we are displaying instances of covid and vaccine tweets for POI.

## Demo
- Uploaded in the repository named `Video_demonstration.mp4`
