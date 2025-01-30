import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets on US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets on US Airlines")


st.markdown("A streamlit dashboard to analyze tweets🦜")
st.sidebar.markdown("A streamlit dashboard to analyze tweets🦜")


Data_url = "path to your file tweets"

@st.cache_data()
def load_data():
    data = pd.read_csv(Data_url)
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data()
st.sidebar.subheader("show random tweet")
random_tweet = st.sidebar.radio('Sentiment',('Positive','Neutral','Negative'))
# st.sidebar.markdown(data.query('airline_sentiment== @random_tweet')[["text"]].sample(n=1).iat[0,0])
random_tweet_lower = random_tweet.lower()
random_tweet = data.query("airline_sentiment == @random_tweet_lower")

if not random_tweet.empty:
    tweet_sample = random_tweet[["text"]].sample(n=1).iat[0, 0]  # Extract text value
    st.sidebar.markdown(tweet_sample)
else:
    st.sidebar.markdown("No tweets found for the selected sentiment.")

st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})
if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == 'Bar plot':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)



st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour to look at", 0, 23)

modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close Map", True, key='close_map'):
    st.markdown("### Tweet locations based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
    st.map(modified_data)

    if st.sidebar.checkbox("Show raw data", False, key='show_raw_data'):
        st.write(modified_data)

st.sidebar.subheader("Breakdown airline by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways','United','American','Southwest','Delta','Virgin America'), key=0)
if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_0 = px.histogram(
                        choice_data, x='airline', y='airline_sentiment',
                         histfunc='count', color='airline_sentiment',
                         facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'},
                          height=600, width=800)
    st.plotly_chart(fig_0)


st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
if not st.sidebar.checkbox("Close", True, key='3'):
    st.subheader('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()

st.sidebar.subheader("Total number of tweets for each airline")
each_airline = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='2')
airline_sentiment_count = data.groupby('airline')['airline_sentiment'].count().sort_values(ascending=False)
airline_sentiment_count = pd.DataFrame({'Airline':airline_sentiment_count.index, 'Tweets':airline_sentiment_count.values.flatten()})
if not st.sidebar.checkbox("Close", True, key='ok'):
    if each_airline == 'Bar plot':
        st.subheader("Total number of tweets for each airline")
        fig_1 = px.bar(airline_sentiment_count, x='Airline', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig_1)
    if each_airline == 'Pie chart':
        st.subheader("Total number of tweets for each airline")
        fig_2 = px.pie(airline_sentiment_count, values='Tweets', names='Airline')
        st.plotly_chart(fig_2)

