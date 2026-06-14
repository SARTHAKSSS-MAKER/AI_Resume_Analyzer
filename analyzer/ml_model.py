import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


data = pd.read_csv("analyzer/dataset.csv")

X = data["resume_text"]
y = data["job_role"]

vectorizer = TfidfVectorizer()

X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(
    f"Model Accuracy: {accuracy * 100:.2f}%"
)


def predict_role(text):

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)

    # Get the probability of the predicted class
    probabilities = model.predict_proba(text_vector)
    confidence = probabilities.max()

    return prediction[0], round(confidence * 100, 2)