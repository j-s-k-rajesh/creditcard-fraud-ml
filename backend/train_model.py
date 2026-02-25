import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Load dataset
data = pd.read_csv("creditcard.csv")

# Stratified split
data['class_cat'] = pd.cut(data["Class"],
                           bins=[-0.1,0.9,np.inf],
                           labels=[0,1])

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_index, test_index in split.split(data, data['class_cat']):
    train_set = data.loc[train_index].drop("class_cat", axis=1)

train_labels = train_set["Class"]
train_features = train_set.drop("Class", axis=1)

# Pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

X_train_prepared = pipeline.fit_transform(train_features)

model = XGBClassifier(
    scale_pos_weight=500,  # important for imbalance
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    n_jobs=-1
)

model.fit(X_train_prepared, train_labels)

# Save model & pipeline
joblib.dump(model, "model.pkl")
joblib.dump(pipeline, "pipeline.pkl")

print("Model and Pipeline saved successfully!")