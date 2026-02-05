import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import timedelta

# Initialize Faker with Indian Locale
fake = Faker(['en_IN'])


def generate_banking_data(n_target=100000):
    data = []
    unique_identities = 75000

    print(f"Generating {unique_identities} identities with robust DOB errors...")

    for i in range(unique_identities):
        # --- Base Data Generation ---
        fn = fake.first_name()
        ln = fake.last_name()

        # Create a Python date object
        base_dob_obj = fake.date_of_birth(minimum_age=18, maximum_age=90)
        dob_str = base_dob_obj.strftime('%Y-%m-%d')

        addr = f"{fake.building_number()}, {fake.street_name()}, Mumbai, 400001"
        phone = fake.msisdn()
        email = f"{fn.lower()}.{ln.lower()}{random.randint(1, 99)}@gmail.com"
        gov_id = fake.bothify(text='????#####?')

        # 1. Add Original Account
        data.append([f"ACC_{i:07d}", fn, ln, dob_str, email, phone, addr, gov_id])

        # 2. Add 20,000 Duplicates (With Robust Error Handling)
        if i < 20000:
            error_type = random.random()
            messy_dob = dob_str

            try:
                if error_type < 0.3:  # 30% chance: Year is off by 1
                    # Using timedelta or simple replace with a safety check
                    messy_dob = (base_dob_obj + timedelta(days=365 * random.choice([-1, 1]))).strftime('%Y-%m-%d')
                elif error_type < 0.5 and base_dob_obj.day <= 12:  # 20% chance: Swap day and month
                    messy_dob = base_dob_obj.strftime('%Y-%d-%m')
            except Exception:
                # If a leap year or invalid date is created, just keep the original
                messy_dob = dob_str

            data.append([
                f"ACC_DUP_{i:07d}",
                fn.lower() if random.random() > 0.5 else f"  {fn} ",
                ln.upper(),
                messy_dob,
                email,
                phone[-10:],
                addr.replace("Mumbai", "MUM"),
                gov_id
            ])

        # 3. Add 5,000 Household members
        if i >= 70000:
            hh_dob = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
            data.append([
                f"ACC_HH_{i:07d}",
                fake.first_name(),
                ln,
                hh_dob,
                email,
                phone,
                addr,
                fake.bothify(text='????#####?')
            ])

    columns = ['ACCT_ID', 'FN', 'LN', 'DOB', 'EMAIL', 'PHONE', 'ADDR', 'GOV_ID']
    df = pd.DataFrame(data, columns=columns)
    df = df.sample(frac=1).reset_index(drop=True)
    return df


# --- Execution ---
df = generate_banking_data()
print(f"Total Rows Generated: {len(df)}")

# Save to CSV
df.to_csv('banking_data_final.csv', index=False)
print("File 'banking_data_final.csv' created successfully.")