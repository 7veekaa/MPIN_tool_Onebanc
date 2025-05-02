import pandas as pd
import random
import os

# Fixed guessability per pattern type
fixed_guessability = {
    "Sequential": 90,
    "Repeated Digits": 95,
    "Keypad Patterns": 85,
    "Mirror/Symmetry": 75,
    "Alternating": 73,
    "Doublets": 70,
    "Special/Other": 65,
    "Random": 10  # Strong pins
}

# Weak patterns - 4 digit
weak_patterns_4 = [
    ("Sequential",       ["1234", "2345", "3456", "4321"],        "Straight sequences"),
    ("Repeated Digits",  ["1111", "2222", "9999", "0000"],        "All digits same"),
    ("Keypad Patterns",  ["2580", "1478", "1593"],                "Keypad memory patterns"),
    ("Mirror/Symmetry",  ["1221", "3443", "2112"],                "Mirror symmetry"),
    ("Alternating",      ["1212", "1313", "2323"],                "Alternating digits"),
    ("Doublets",         ["1122", "5566", "7788"],                "Double pairs"),
    ("Special/Other",    ["2020", "1004", "1515"],                "Famous dates or symbols")
]

# Weak patterns - 6 digit
weak_patterns_6 = [
    ("Sequential",       ["123456", "654321"],                    "Straight sequences"),
    ("Repeated Digits",  ["000000", "999999", "111111"],          "All digits same"),
    ("Keypad Patterns",  ["258025", "147852"],                    "Keypad memory patterns"),
    ("Mirror/Symmetry",  ["123321", "456654"],                    "Mirror symmetry"),
    ("Alternating",      ["121212", "343434"],                    "Alternating digits"),
    ("Doublets",         ["112233", "445566"],                    "Double pairs"),
    ("Special/Other",    ["202020", "151515", "131313"],          "Special dates")
]

def expand_pattern_data(patterns, user_prefix, start_idx, replication=72):
    data = []
    counter = start_idx
    for pattern_type, base_list, comment in patterns:
        for _ in range(replication):
            mpin = random.choice(base_list)
            data.append({
                "user_id": f"{user_prefix}_{str(counter).zfill(4)}",
                "mpin": mpin,
                "pattern_type": pattern_type,
                "label": "Weak",
                "guessability_percentage": fixed_guessability[pattern_type],
                "comment": comment
            })
            counter += 1
    return data, counter

# Generate strong MPINs
def generate_strong_mpin(length=4):
    while True:
        pin = ''.join(random.choices("0123456789", k=length))
        if len(set(pin)) == length:
            return pin

def generate_strong_data(count, user_prefix, start_idx):
    data = []
    for i in range(count):
        length = 4 if i < count // 2 else 6
        mpin = generate_strong_mpin(length)
        data.append({
            "user_id": f"{user_prefix}_{str(start_idx + i).zfill(4)}",
            "mpin": mpin,
            "pattern_type": "Random",
            "label": "Strong",
            "guessability_percentage": fixed_guessability["Random"],
            "comment": "No known pattern"
        })
    return data

# 📦 Build and export
weak4, idx = expand_pattern_data(weak_patterns_4, "C4", 1, replication=72)
weak6, idx = expand_pattern_data(weak_patterns_6, "C6", idx, replication=71)
strong = generate_strong_data(1000, "S", 1)

# Combine and shuffle
all_data = weak4 + weak6 + strong
random.shuffle(all_data)

# Export
df = pd.DataFrame(all_data)
os.makedirs("mpin_security_checker/data", exist_ok=True)
df.to_csv("mpin_security_checker/data/common_pins.csv", index=False)
print("✅ Regenerated: 2000 balanced MPIN records saved to common_pins.csv")
