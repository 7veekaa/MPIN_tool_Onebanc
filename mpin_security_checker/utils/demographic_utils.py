import joblib
import numpy as np
from datetime import datetime
from itertools import permutations


model = joblib.load("mpin_security_checker/models/demographic_model.pkl")
label_encoder = joblib.load("mpin_security_checker/models/label_encoder.pkl")

def generate_jumbled_variants(date_obj, pin_length=4):
    date_str = date_obj.strftime("%Y%m%d")
    variants = set()
    for i in range(len(date_str) - pin_length + 1):
        sub = date_str[i:i+pin_length]
        for p in permutations(sub):
            variants.add(''.join(p))
    return list(variants)

def predict_demographic_strength(mpin, dob_self, dob_spouse, dob_pet, anniversary):

    if isinstance(dob_self, datetime): dob_self = dob_self.date()
    if isinstance(dob_spouse, datetime): dob_spouse = dob_spouse.date()
    if isinstance(dob_pet, datetime): dob_pet = dob_pet.date()
    if isinstance(anniversary, datetime): anniversary = anniversary.date()

    mpin = str(mpin)
    pin_length = len(mpin)
    digit_diversity = len(set(mpin))

    # Generate jumbled formats based on MPIN length
    jumbled_self = generate_jumbled_variants(dob_self, pin_length)
    jumbled_spouse = generate_jumbled_variants(dob_spouse, pin_length)
    jumbled_pet = generate_jumbled_variants(dob_pet, pin_length)
    jumbled_anniv = generate_jumbled_variants(anniversary, pin_length)

    # Feature engineering
    is_in_self = int(mpin in jumbled_self)
    is_in_spouse = int(mpin in jumbled_spouse)
    is_in_pet = int(mpin in jumbled_pet)
    is_in_anniv = int(mpin in jumbled_anniv)

    input_features = np.array([[pin_length, digit_diversity, is_in_self, is_in_spouse, is_in_pet, is_in_anniv]])
    prediction_encoded = model.predict(input_features)[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

    return prediction_label  
