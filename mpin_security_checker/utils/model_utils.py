import joblib
import numpy as np

# Load all models: classifier, regressor, and encoder
def load_model(
    classifier_path="mpin_security_checker/models/rf_pattern_model.pkl",
    regressor_path="mpin_security_checker/models/rf_guessability_model.pkl",
    encoder_path="mpin_security_checker/models/pattern_encoder.pkl"
):
    classifier = joblib.load(classifier_path)
    regressor = joblib.load(regressor_path)
    encoder = joblib.load(encoder_path)
    return classifier, regressor, encoder

# Predict strength label and guessability percentage
def predict_strength(classifier, regressor, encoder, mpin, pattern_type):
    mpin = str(mpin)
    length = len(mpin)
    digit_diversity = len(set(mpin))

    # One-hot encode pattern_type safely
    try:
        pattern_encoded = encoder.transform([[pattern_type]])
    except Exception:
        pattern_encoded = encoder.transform([["Random"]])

    # Create feature vector
    input_vector = np.concatenate([[length, digit_diversity], pattern_encoded[0]])

    # 1️⃣ Predict WEAK/STRONG label using classifier
    probas = classifier.predict_proba([input_vector])[0]
    if 1 in classifier.classes_:
        weak_index = list(classifier.classes_).index(1)
        guessability_prob = probas[weak_index]
    else:
        guessability_prob = 0.0
    label = int(guessability_prob > 0.5)

    # 2️⃣ Predict actual guessability % using regressor
    guessability_percent = int(regressor.predict([input_vector])[0])

    return guessability_percent, label
