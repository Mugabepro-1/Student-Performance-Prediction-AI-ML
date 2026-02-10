import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import os

def train():
    csv_file = os.path.join(os.path.dirname(__file__), 'dataset.csv')
    df = pd.read_csv(csv_file)

    df['Extracurricular Activities'] = LabelEncoder().fit_transform(
    df['Extracurricular Activities']
    )
    X = df.drop('Performance Index', axis=1)
    y = df['Performance Index']
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, 'performance/model.pkl')
    print("Model trained and saved")