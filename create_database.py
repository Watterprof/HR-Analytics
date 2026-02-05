import pandas as pd
import sqlite3

# Load CSV
print("Loading employee_data.csv...")
df = pd.read_csv('employee_data.csv')

print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Create SQLite database
print("\nCreating SQLite database...")
conn = sqlite3.connect('hr_data.db')

# Save to database
df.to_sql('employees', conn, if_exists='replace', index=False)

print("✅ Database created successfully!")
print("\nDatabase file: hr_data.db")
print("Table name: employees")

# Verify
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM employees")
count = cursor.fetchone()[0]
print(f"\nVerification: {count} records in database")

conn.close()

print("\n" + "="*50)
print("NEXT STEPS:")
print("="*50)
print("1. Di Metabase, klik 'Settings' (icon gear)")
print("2. Pilih 'Admin settings' → 'Databases'")
print("3. Klik 'Add database'")
print("4. Pilih 'SQLite'")
print("5. Name: HR Database")
print("6. Filename: Browse dan pilih 'hr_data.db'")
print("7. Klik 'Save'")
print("="*50)
