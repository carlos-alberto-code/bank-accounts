import pandas as pd
import random

# Provided file path
file_path = 'data/.accounts.csv'

# Load the existing CSV file
df = pd.read_csv(file_path)

# List of common names in Mexico
paternal_surnames = ["García", "Martínez", "López", "González", "Pérez", "Rodríguez", "Sánchez", "Ramírez", "Cruz", "Flores"]
maternal_surnames = ["Hernández", "Gutiérrez", "Jiménez", "Mendoza", "Vázquez", "Castillo", "Ortega", "Ramos", "Reyes", "Morales"]
names = ["Juan", "Carlos", "José", "Luis", "Miguel", "Antonio", "Jorge", "Pedro", "Ricardo", "Fernando", 
         "María", "Guadalupe", "Verónica", "Ana", "Martha", "Patricia", "Laura", "Gabriela", "Sandra", "Rosa"]

# Generate unique account numbers
existing_account_numbers = set(df['Numero de Cuenta'].astype(str))
new_account_numbers = set()
while len(new_account_numbers) < 100:
    account_number = ''.join(random.choices('0123456789', k=10))
    if account_number not in existing_account_numbers:
        new_account_numbers.add(account_number)

# Create new accounts
new_accounts = []
for account_number in new_account_numbers:
    new_accounts.append({
        'Apellido Paterno': random.choice(paternal_surnames),
        'Apellido Materno': random.choice(maternal_surnames),
        'Nombres': random.choice(names),
        'Numero de Cuenta': account_number
    })

# Convert new accounts to DataFrame
new_accounts_df = pd.DataFrame(new_accounts)

# Append new accounts to the existing DataFrame
df = pd.concat([df, new_accounts_df], ignore_index=True)

# Save the updated DataFrame to a new CSV file
output_file_path = 'data/accounts.csv'
df.to_csv(output_file_path, index=False)