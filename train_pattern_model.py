import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, mean_absolute_error


csv_path = "mpin_security_checker/data/common_pins.csv"
df = pd.read_csv(csv_path)


df['mpin'] = df['mpin'].astype(str)
df['length'] = df['mpin'].apply(len)
df['digit_diversity'] = df['mpin'].apply(lambda x: len(set(x)))
df['label'] = df['label'].apply(lambda x: 1 if str(x).lower() == "weak" else 0)

encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
pattern_encoded = encoder.fit_transform(df[['pattern_type']])
pattern_df = pd.DataFrame(pattern_encoded, columns=encoder.get_feature_names_out(['pattern_type']))


features = pd.concat([df[['length', 'digit_diversity']], pattern_df], axis=1)
labels = df['label']
guessability = df['guessability_percentage']


X_train, X_test, y_label_train, y_label_test = train_test_split(
    features, labels, test_size=0.2, stratify=labels, random_state=42
)
_, _, y_guess_train, y_guess_test = train_test_split(
    features, guessability, test_size=0.2, random_state=42
)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_label_train)
acc = accuracy_score(y_label_test, clf.predict(X_test))
print(f"Classifier Accuracy: {acc * 100:.2f}%")


reg = RandomForestRegressor(n_estimators=100, random_state=42)
reg.fit(X_train, y_guess_train)
mae = mean_absolute_error(y_guess_test, reg.predict(X_test))
print(f"Regressor MAE: {mae:.2f}")


model_dir = "mpin_security_checker/models"
os.makedirs(model_dir, exist_ok=True)
joblib.dump(clf, os.path.join(model_dir, "rf_pattern_model.pkl"))
joblib.dump(reg, os.path.join(model_dir, "rf_guessability_model.pkl"))  # ✅ NEW
joblib.dump(encoder, os.path.join(model_dir, "pattern_encoder.pkl"))

print(" Classifier, Regressor, and Encoder saved to mpin_security_checker/models/")
