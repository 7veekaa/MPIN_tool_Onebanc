import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, mean_absolute_error

# Step 1: Load dataset
csv_path = "mpin_security_checker/data/common_pins.csv"
df = pd.read_csv(csv_path)

# Step 2: Clean and feature engineering
df['mpin'] = df['mpin'].astype(str)
df['length'] = df['mpin'].apply(len)
df['digit_diversity'] = df['mpin'].apply(lambda x: len(set(x)))
df['label'] = df['label'].apply(lambda x: 1 if str(x).lower() == "weak" else 0)

# Step 3: One-hot encode the pattern type
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
pattern_encoded = encoder.fit_transform(df[['pattern_type']])
pattern_df = pd.DataFrame(pattern_encoded, columns=encoder.get_feature_names_out(['pattern_type']))

# Step 4: Merge all features
features = pd.concat([df[['length', 'digit_diversity']], pattern_df], axis=1)
labels = df['label']
guessability = df['guessability_percentage']

# Step 5: Split data
X_train, X_test, y_label_train, y_label_test = train_test_split(
    features, labels, test_size=0.2, stratify=labels, random_state=42
)
_, _, y_guess_train, y_guess_test = train_test_split(
    features, guessability, test_size=0.2, random_state=42
)

# Step 6: Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_label_train)
acc = accuracy_score(y_label_test, clf.predict(X_test))
print(f"Classifier Accuracy: {acc * 100:.2f}%")

# Step 7: Train regressor
reg = RandomForestRegressor(n_estimators=100, random_state=42)
reg.fit(X_train, y_guess_train)
mae = mean_absolute_error(y_guess_test, reg.predict(X_test))
print(f"Regressor MAE: {mae:.2f}")

# Step 8: Save all models
model_dir = "mpin_security_checker/models"
os.makedirs(model_dir, exist_ok=True)
joblib.dump(clf, os.path.join(model_dir, "rf_pattern_model.pkl"))
joblib.dump(reg, os.path.join(model_dir, "rf_guessability_model.pkl"))  # ✅ NEW
joblib.dump(encoder, os.path.join(model_dir, "pattern_encoder.pkl"))

print("✅ Classifier, Regressor, and Encoder saved to mpin_security_checker/models/")
