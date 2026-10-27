import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
from features import generate_features
import os 

# APP_DIR = os.path.join(
#     os.environ["LOCALAPPDATA"],
#     "Advanced Flash App"
# )

# os.makedirs(APP_DIR, exist_ok=True)

CSV_FILE = "attempts.csv"


def create_attempts_file():
    pd.DataFrame(columns=[
        "user",
        "a",
        "b",
        "operation",
        "correct",
        "response_time",
        "correct_answer",
        "user_answer",
        "timestamp"
    ]).to_csv(CSV_FILE, index=False)


def load_attempts():
    if not os.path.exists(CSV_FILE):
        create_attempts_file()

    return pd.read_csv(CSV_FILE)

data = load_attempts()

print(data.head()) 


feature_rows = []
# Applying features generation to the csv file 
for _, row in data.iterrows(): 
    features = generate_features(int(row["a"]), int(row["b"]), row["operation"], int(row["correct_answer"]))
    features["correct"] = int(row["correct"])

    feature_rows.append(features) 

features_df = pd.DataFrame(feature_rows)

features_df = features_df.fillna(0)

if features_df.empty:
    raise ValueError("Training data is empty. Check attempts.csv.")

x = features_df.drop(columns=["correct"])
y = features_df["correct"]

# makes a table of 0s and 1s because the computer doesn't understand the word "Multiplication"
x = pd.get_dummies(x, columns=["operation"])

# Save the feature column order for later prediction 
training_columns = x.columns.tolist()


# 20% used to test, 80% training
# random state is the seed value for the computer's random number generator
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

for column in x_train.columns:
    for value in x_train[column]:
        if isinstance(value, tuple):
            print("TUPLE FOUND")
            print("Column:", column)
            print("Value:", value)
            break

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train) 
x_test = scaler.transform(x_test) 

# Logistic Regression is a ML algorithm that predics a binary outcome (question right or wrong)
model = LogisticRegression(max_iter=5000) 
# Training on data
model.fit(x_train, y_train)

# Making prediction
predictions = model.predict(x_test)
probabilities = model.predict_proba(x_test) 

accuracy = accuracy_score(y_test, predictions) 

print("Accuracy:", accuracy)

joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(training_columns, "training_columns.pkl")
# print(features_df["correct"].mean())
# print(features_df.groupby("answer_digits")["correct"].mean())
# print(features_df.groupby("answer_digit_sum")["correct"].mean())