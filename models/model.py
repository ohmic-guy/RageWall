import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib


df = pd.read_csv("../data/traffic_data_labeled.csv")
print("Loaded labeled data from traffic_data_labeled.csv")


features_to_drop = ['src_ip', 'dst_ip']
df = df.drop(columns=features_to_drop)
print("Dropped non-numeric columns:", features_to_drop)


df['length_log'] = np.log1p(df['length'])
df['ttl_bins'] = pd.qcut(df['ttl'], q=5, labels=False, duplicates='drop')


X = df.drop("label", axis=1)
y = df["label"]


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)


X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)


param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'class_weight': ['balanced']
}
print("Starting GridSearchCV for Random Forest...")
grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    n_jobs=-1,
    scoring='f1',
    verbose=1
)
grid.fit(X_train, y_train)
clf = grid.best_estimator_
print(f"Best parameters: {grid.best_params_}")


y_pred = clf.predict(X_test)
print("Classification Report:\n")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))


artifacts = {
    'model': clf,
    'scaler': scaler,
    'feature_columns': X.columns.tolist()
}
joblib.dump(artifacts, "ragewall_model.pkl")
print("Model and artifacts saved as ragewall_model.pkl")
