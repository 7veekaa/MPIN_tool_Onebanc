import random
import pandas as pd
from utils.pattern_checker import get_pattern_type
from utils.model_utils import predict_strength


COMMON_PINS_PATH = "mpin_security_checker/data/common_pins.csv"
common_pins_df = pd.read_csv(COMMON_PINS_PATH)


common_pins_set = set(common_pins_df["mpin"].astype(str).tolist())



def generate_medium():
    
    digits = random.sample(range(10), 4)
    return ''.join(str(d) for d in digits)

def generate_hard():

    return ''.join(str(random.randint(0, 9)) for _ in range(6))



def generate_secure_mpin(level, classifier, regressor, encoder, avoid_set=None):
    """
    Generate a secure MPIN based on memory level, avoiding:
    - Common pins (from common_pins.csv)
    - Demographic-based pins (from avoid_set)
    - Weak predictions from your trained model
    """
    if avoid_set is None:
        avoid_set = set()

    for _ in range(100):
        candidate = generate_medium() if level == "Medium" else generate_hard()

        if candidate in avoid_set or candidate in common_pins_set:
            continue

        pattern = get_pattern_type(candidate)
        _, label = predict_strength(classifier, regressor, encoder, candidate, pattern)

        if label == 0:
            return candidate, pattern

    return None, None
