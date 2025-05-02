import random
import pandas as pd
from datetime import datetime, timedelta

# Helper to create random date
def random_date(start_year, end_year):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).date()

# Create jumbled formats from a date
def generate_jumbled_dates(date):
    date_str = date.strftime("%Y%m%d")
    return list(set([
        date_str[2:6],                 # MMDD
        date_str[4:8],                 # DDYY
        date_str[0:4],                 # YYYY
        date_str[6:8] + date_str[4:6], # DDMM reversed
        date_str[2:4] + date_str[6:8]  # MMDD only
    ]))

# Common MPINs (to simulate weak cases)
common_pins_4 = ['1234', '1111', '0000', '1212', '7777', '2580']
common_pins_6 = ['123456', '111111', '000000', '121212', '654321', '258025']

# Main function
def generate_demographic_dataset(num_users=1000, output_file="demographic_checkpoint_data.csv"):
    users = []

    for i in range(1, num_users + 1):
        user_id = f"U{str(i).zfill(4)}"
        pin_length = 4 if i <= num_users // 2 else 6
        pin_space = 9999 if pin_length == 4 else 999999

        dob_self = random_date(1970, 2003)
        dob_spouse = random_date(dob_self.year - 5, dob_self.year + 5)
        dob_pet = random_date(2010, 2024)
        anniversary_date = random_date(1995, 2023)

        jumbled_self = generate_jumbled_dates(dob_self)
        jumbled_spouse = generate_jumbled_dates(dob_spouse)
        jumbled_pet = generate_jumbled_dates(dob_pet)
        jumbled_anniv = generate_jumbled_dates(anniversary_date)

        all_jumbled = jumbled_self + jumbled_spouse + jumbled_pet + jumbled_anniv
        candidates = [j for j in all_jumbled if len(j) == pin_length]

        choice_type = random.choices(["common", "demographic", "random"], weights=[20, 40, 40])[0]

        if choice_type == "common":
            mpin = random.choice(common_pins_4 if pin_length == 4 else common_pins_6)
        elif choice_type == "demographic" and candidates:
            mpin = random.choice(candidates)
        else:
            mpin = str(random.randint(0, pin_space)).zfill(pin_length)

        # Label logic
        reasons = []
        if mpin in common_pins_4 + common_pins_6:
            reasons.append("COMMON_PATTERN")
        if mpin in jumbled_self:
            reasons.append("DEMOGRAPHIC_SELF")
        if mpin in jumbled_spouse:
            reasons.append("DEMOGRAPHIC_SPOUSE")
        if mpin in jumbled_pet:
            reasons.append("DEMOGRAPHIC_PET")
        if mpin in jumbled_anniv:
            reasons.append("DEMOGRAPHIC_ANNIVERSARY")

        label = "WEAK" if reasons else "STRONG"

        users.append({
            "user_id": user_id,
            "mpin": mpin,
            "pin_length": pin_length,
            "dob_self": dob_self,
            "dob_spouse": dob_spouse,
            "dob_pet": dob_pet,
            "anniversary_date": anniversary_date,
            "label": label,
            "reason_if_weak": ",".join(reasons),
            "jumbled_self": "|".join(jumbled_self),
            "jumbled_spouse": "|".join(jumbled_spouse),
            "jumbled_pet": "|".join(jumbled_pet),
            "jumbled_anniversary": "|".join(jumbled_anniv)
        })

    df = pd.DataFrame(users)
    df.to_csv(output_file, index=False)
    print(f"✅ CSV generated: {output_file} with {num_users} entries.")

# Run this file directly
if __name__ == "__main__":
    generate_demographic_dataset()
