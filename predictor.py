import joblib
import pandas as pd 
from features import generate_features
import sys
import os 

def resource_path(filename):
    base_path = getattr(
        sys,
        "_MEIPASS",
        os.path.dirname(os.path.abspath(__file__))
    )

    return os.path.join(base_path, filename)

# loading model, scaler, and training columsn from file
model = joblib.load(resource_path("model.pkl"))
scaler = joblib.load(resource_path("scaler.pkl")) 
training_columns = joblib.load(resource_path("training_columns.pkl"))

def predict_questions(a, b, operation, correct_answer): 
    features = generate_features(a, b, operation, correct_answer) 
    df = pd.DataFrame([features])
    df = pd.get_dummies(df, columns=["operation"])
    # finds missing columns and sets them to 0 
    df = df.reindex(columns=training_columns, fill_value=0) 
    scaled_features = scaler.transform(df) 
    probability = model.predict_proba(scaled_features)[0][1]
    return probability

if __name__ == "__main__": 
    pass
    print(f"{predict_questions(22, 0, 'Squares', 484):.2%}")
    print(f"{predict_questions(98, 0, 'Squares', 9604):.2%}")
    print(f"{predict_questions(76, 0, 'Squares', 5776):.2%}")
    print(f"{predict_questions(51, 0, 'Squares', 2601):.2%}")
    print(f"{predict_questions(41, 0, 'Squares', 1681):.2%}")