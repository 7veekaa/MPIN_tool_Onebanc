import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from datetime import datetime
import joblib
import os

# Generate jumbled date variants
def generate_jumbled_variants(date_obj):
    date_str = date_obj.strftime("%Y%m%d")
    return list(set([
        date_str[2:6],                 # MMDD
        date_str[4:8],                 # DDYY
        date_str[0:4],                 # YYYY
        date_str[6:8] + date_str[4:6], # DDMM reversed
        date_str[2:4] + date_str[6:8]  # MMDD only
    ]))

# Load dataset
df = pd.read_csv("mpin_security_checker/data/demographic_checkpoint_data.csv")

features = []
labels = []

for index, row in df.iterrows():
    mpin = str(row['mpin'])
    pin_length = len(mpin)
    digit_diversity = len(set(mpin))

    dob_self = pd.to_datetime(row['dob_self']).date()
    dob_spouse = pd.to_datetime(row['dob_spouse']).date()
    dob_pet = pd.to_datetime(row['dob_pet']).date()
    anniversary = pd.to_datetime(row['anniversary_date']).date()

    # Jumbled matches
    jumbled_self = generate_jumbled_variants(dob_self)
    jumbled_spouse = generate_jumbled_variants(dob_spouse)
    jumbled_pet = generate_jumbled_variants(dob_pet)
    jumbled_anniv = generate_jumbled_variants(anniversary)

    is_in_self = int(mpin in jumbled_self)
    is_in_spouse = int(mpin in jumbled_spouse)
    is_in_pet = int(mpin in jumbled_pet)
    is_in_anniv = int(mpin in jumbled_anniv)

    features.append([pin_length, digit_diversity, is_in_self, is_in_spouse, is_in_pet, is_in_anniv])
    labels.append(row['label'])

# Prepare data
X = np.array(features)
y = np.array(labels)

# Encode labels
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("📊 Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save model + encoder
os.makedirs("mpin_security_checker/models", exist_ok=True)
joblib.dump(model, "mpin_security_checker/models/demographic_model.pkl")
joblib.dump(label_encoder, "mpin_security_checker/models/label_encoder.pkl")

print("✅ Model saved to mpin_security_checker/models/")
