import streamlit as st
import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np
import mysql.connector
import json
import pandas as pd
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use('ggplot')
with open("config.json", "r") as f:
   config = json.load(f)

cnx = mysql.connector.connect(
    host="localhost",
    user=config["username"],
    password=config["password"],
    database=config["database"]
)
# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comment TEXT NOT NULL,
    rough_score INT NOT NULL,
    evaluated_score DECIMAL(8, 7) NOT NULL
)
"""
cursor.execute(create_table_query)


def preprocess_sentence(tweet):

     # Contractions
    tweet = re.sub(r"he's", "he is", tweet)
    tweet = re.sub(r"there's", "there is", tweet)
    tweet = re.sub(r"We're", "We are", tweet)
    tweet = re.sub(r"That's", "That is", tweet)
    tweet = re.sub(r"won't", "will not", tweet)
    tweet = re.sub(r"they're", "they are", tweet)
    tweet = re.sub(r"Can't", "Cannot", tweet)
    tweet = re.sub(r"wasn't", "was not", tweet)
    tweet = re.sub(r"don\x89Ûªt", "do not", tweet)
    tweet = re.sub(r"aren't", "are not", tweet)
    tweet = re.sub(r"isn't", "is not", tweet)
    tweet = re.sub(r"What's", "What is", tweet)
    tweet = re.sub(r"haven't", "have not", tweet)
    tweet = re.sub(r"hasn't", "has not", tweet)
    tweet = re.sub(r"There's", "There is", tweet)
    tweet = re.sub(r"He's", "He is", tweet)
    tweet = re.sub(r"It's", "It is", tweet)
    tweet = re.sub(r"You're", "You are", tweet)
    tweet = re.sub(r"I'M", "I am", tweet)
    tweet = re.sub(r"shouldn't", "should not", tweet)
    tweet = re.sub(r"wouldn't", "would not", tweet)
    tweet = re.sub(r"i'm", "I am", tweet)
    tweet = re.sub(r"I\x89Ûªm", "I am", tweet)
    tweet = re.sub(r"I'm", "I am", tweet)
    tweet = re.sub(r"Isn't", "is not", tweet)
    tweet = re.sub(r"Here's", "Here is", tweet)
    tweet = re.sub(r"you've", "you have", tweet)
    tweet = re.sub(r"you\x89Ûªve", "you have", tweet)
    tweet = re.sub(r"we're", "we are", tweet)
    tweet = re.sub(r"what's", "what is", tweet)
    tweet = re.sub(r"couldn't", "could not", tweet)
    tweet = re.sub(r"we've", "we have", tweet)
    tweet = re.sub(r"it\x89Ûªs", "it is", tweet)
    tweet = re.sub(r"doesn\x89Ûªt", "does not", tweet)
    tweet = re.sub(r"It\x89Ûªs", "It is", tweet)
    tweet = re.sub(r"Here\x89Ûªs", "Here is", tweet)
    tweet = re.sub(r"who's", "who is", tweet)
    tweet = re.sub(r"I\x89Ûªve", "I have", tweet)
    tweet = re.sub(r"y'all", "you all", tweet)
    tweet = re.sub(r"can\x89Ûªt", "cannot", tweet)
    tweet = re.sub(r"would've", "would have", tweet)
    tweet = re.sub(r"it'll", "it will", tweet)
    tweet = re.sub(r"we'll", "we will", tweet)
    tweet = re.sub(r"wouldn\x89Ûªt", "would not", tweet)
    tweet = re.sub(r"We've", "We have", tweet)
    tweet = re.sub(r"he'll", "he will", tweet)
    tweet = re.sub(r"Y'all", "You all", tweet)
    tweet = re.sub(r"Weren't", "Were not", tweet)
    tweet = re.sub(r"Didn't", "Did not", tweet)
    tweet = re.sub(r"they'll", "they will", tweet)
    tweet = re.sub(r"they'd", "they would", tweet)
    tweet = re.sub(r"DON'T", "DO NOT", tweet)
    tweet = re.sub(r"That\x89Ûªs", "That is", tweet)
    tweet = re.sub(r"they've", "they have", tweet)
    tweet = re.sub(r"i'd", "I would", tweet)
    tweet = re.sub(r"should've", "should have", tweet)
    tweet = re.sub(r"You\x89Ûªre", "You are", tweet)
    tweet = re.sub(r"where's", "where is", tweet)
    tweet = re.sub(r"Don\x89Ûªt", "Do not", tweet)
    tweet = re.sub(r"we'd", "we would", tweet)
    tweet = re.sub(r"i'll", "I will", tweet)
    tweet = re.sub(r"weren't", "were not", tweet)
    tweet = re.sub(r"They're", "They are", tweet)
    tweet = re.sub(r"Can\x89Ûªt", "Cannot", tweet)
    tweet = re.sub(r"you\x89Ûªll", "you will", tweet)
    tweet = re.sub(r"I\x89Ûªd", "I would", tweet)
    tweet = re.sub(r"let's", "let us", tweet)
    tweet = re.sub(r"it's", "it is", tweet)
    tweet = re.sub(r"can't", "cannot", tweet)
    tweet = re.sub(r"don't", "do not", tweet)
    tweet = re.sub(r"you're", "you are", tweet)
    tweet = re.sub(r"i've", "I have", tweet)
    tweet = re.sub(r"that's", "that is", tweet)
    tweet = re.sub(r"i'll", "I will", tweet)
    tweet = re.sub(r"doesn't", "does not", tweet)
    tweet = re.sub(r"i'd", "I would", tweet)
    tweet = re.sub(r"didn't", "did not", tweet)
    tweet = re.sub(r"ain't", "am not", tweet)
    tweet = re.sub(r"you'll", "you will", tweet)
    tweet = re.sub(r"I've", "I have", tweet)
    tweet = re.sub(r"Don't", "do not", tweet)
    tweet = re.sub(r"I'll", "I will", tweet)
    tweet = re.sub(r"I'd", "I would", tweet)
    tweet = re.sub(r"Let's", "Let us", tweet)
    tweet = re.sub(r"you'd", "You would", tweet)
    tweet = re.sub(r"It's", "It is", tweet)
    tweet = re.sub(r"Ain't", "am not", tweet)
    tweet = re.sub(r"Haven't", "Have not", tweet)
    tweet = re.sub(r"Could've", "Could have", tweet)
    tweet = re.sub(r"youve", "you have", tweet)
    tweet = re.sub(r"donå«t", "do not", tweet)

    # Remove non-punctuation special characters excluding '!', '?'
    tweet = re.sub(r'[^\w\s#@:;]|_', '', tweet)

    # Remove escape characters
    tweet = tweet.encode().decode('unicode_escape')

    # Remove extra white spaces
    tweet = re.sub(r'\s+', ' ', tweet)

    # Remove newline characters
    tweet = tweet.replace('\n', ' ')

    # Remove extra white spaces
    tweet = re.sub(r'\s+', ' ', tweet)

    return tweet


def get_severity_score(proba):
   severity_out_of_5 = np.argmax(proba)
   severity_score = 0
   for i in range(6):
      severity_score += i*proba[i]

   return severity_out_of_5, severity_score


def insert_entry(comment, rough_score, evaluated_score):
    # Insert a new entry into the table
    insert_query = "INSERT INTO entries (comment, rough_score, evaluated_score) VALUES (%s, %s, %s)"
    data = (comment, rough_score, evaluated_score)
    cursor.execute(insert_query, data)
    cnx.commit()
    print("Entry added successfully.")


def view_entries(order_by):
    # Fetch entries from the table
    select_query = f"SELECT * FROM entries ORDER BY evaluated_score {order_by}"
    cursor.execute(select_query)
    entries = cursor.fetchall()

    # Create a DataFrame from the entries
    columns = ["ID", "Comment", "Rough Score", "Evaluated Score"]
    df = pd.DataFrame(entries, columns=columns)

    # Display the DataFrame
    return df


with open('model_pickle', 'rb') as f:
  model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
  vec = pickle.load(f)


st.write("# Jigsaw Comments Severity Rating")
st.write(" ML model capable of rating comments based on the Jigsaw-Rate Severity of Toxic Comments Kaggle competition dataset. This project harnesses the power of machine learning to tackle the critical issue of toxic comments, enabling effective comment rating and content moderation.")
rad = st.sidebar.radio("Navigation", ["Make Entry", "Get Analytics"])
if rad == "Make Entry":
    comment = st.text_area(
        "Enter the comment here for calculating its severity:")
    if comment:
        preprocessed_comment = preprocess_sentence(comment)
        vectorized_comment = vec.transform([preprocessed_comment])
        proba = model.predict_proba(vectorized_comment)
        rough_severity_score, total_score = get_severity_score(proba[0])
        st.write("## The rough severity score out of 5 is:")
        st.write(rough_severity_score)
        st.write("## Total Score:")
        st.write(total_score)
        if st.button("Make Entry to Database?"):
            insert_entry(comment, int(rough_severity_score),
                         float(total_score))
            df = view_entries("ASC")
            plt.hist(df["Evaluated Score"], bins=10, alpha=0.7)
            plt.xlabel("Evaluated Score")
            plt.ylabel("Frequency")
            plt.title("Histogram of Evaluated Scores")
            plt.axvline(x=total_score, color="red",
                        linestyle="--", label="Most Recent Entry")
            plt.legend()
            st.pyplot()
            plt.hist(df["Rough Score"], orientation="horizontal")
            plt.xlabel("Frequency")
            plt.ylabel("Score out of 5")
            plt.title("Histogram of Scores out of 5")
            plt.axhline(y=rough_severity_score, color="purple",
                        linestyle="--", label="Most Recent")
            plt.legend()
            st.pyplot()
if rad == "Get Analytics":
   choice = st.radio("View comments in: ", [
                     "Ascending", "Descending"], index=1)
   if choice == "Descending":
      df = view_entries("DESC")
   elif choice == "Ascending":
      df = view_entries("ASC")
   st.write("# Displaying Entries")
   seeall = st.button("Click to see all entries")
   if(seeall):
      st.table(df)
   else:
      st.table(df.head())

    
   plt.hist(df["Evaluated Score"], bins=10, alpha=0.7)
   plt.xlabel("Evaluated Score")
   plt.ylabel("Frequency")
   plt.title("Histogram of Evaluated Scores")
   st.pyplot()
   plt.hist(df["Rough Score"], orientation="horizontal")
   plt.xlabel("Frequency")
   plt.ylabel("Score out of 5")
   plt.title("Histogram of Scores out of 5")
   st.pyplot()

   plt.pie(df["Rough Score"].value_counts(),labels=[i for i in range(max(df["Rough Score"])+1)],autopct="%6.2f")
   plt.title("% Of records having a particular rough score")
   st.pyplot()






