import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

train_df = pd.read_csv("Dataset\\archive\\train.txt", sep=";", names=["text", "emotion"])
val_df = pd.read_csv("Dataset\\archive\\val.txt", sep=";", names=["text", "emotion"])
test_df = pd.read_csv("Dataset\\archive\\test.txt", sep=";", names=["text", "emotion"])

def cleaningText(data):
    data['text'] = data['text'].str.lower()
    data['text'] = data['text'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    data['text'] = data['text'].apply(lambda x: " ".join([
        lemmatizer.lemmatize(word)
        for word in x.split()
        if word not in stop_words
    ]))
    data.drop_duplicates(inplace=True)
    data.dropna(inplace=True)
    data['text'] = data['text'].str.replace(r"\bim\b", "i am", regex=True)
    return data

# Cleaning the data
train_df = cleaningText(train_df)
val_df = cleaningText(val_df)
test_df = cleaningText(test_df)

# Combine training + validation data for optimal
combined_df = pd.concat([train_df, val_df])
X_train = combined_df['text']
y_train = combined_df['emotion']

X_test = test_df['text']
y_test = test_df['emotion']

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# # Prediction based on the test data
y_pred = model.predict(X_test_vec)

def predict_mood(text):
    # Clean the input text using the same cleaning function
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    clean_text = re.sub(r"\bim\b", "i am", clean_text)

    # Transform the input using the trained vectorizer
    text_vec = vectorizer.transform([clean_text])

    # Predict the mood
    predicted_emotion = model.predict(text_vec)[0]
    return predicted_emotion

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

if __name__ == "__main__":
    print("Welcome to MoodTune - Emotion Based Music Recommender!")
    user_input = input("How are you feeling today? Describe your mood: ")
    mood = predict_mood(user_input)
    print(f"\n Based on your description, your mood is: {mood.capitalize()}")