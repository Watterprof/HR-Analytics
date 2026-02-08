"""
Update HR Database with ML Predictions
Adds prediction results to the database for dashboard visualization
"""

import pandas as pd
import sqlite3
import joblib
import warnings
warnings.filterwarnings('ignore')

print("Loading ML model and data...")

# Load model and preprocessing objects
model = joblib.load('../models/best_model.pkl')
scaler = joblib.load('../models/scaler.pkl')
feature_names = joblib.load('../models/feature_names.pkl')

# Load employee data
df = pd.read_csv('../employee_data.csv')

# Feature engineering function
def engineer_features(df):
    """Apply same feature engineering as training"""
    df = df.copy()
    
    # Age groups
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 100], 
                            labels=['Young', 'Mid', 'Senior', 'Veteran'])
    
    # Tenure groups
    df['TenureGroup'] = pd.cut(df['YearsAtCompany'], bins=[0, 2, 5, 10, 100],
                               labels=['New', 'Intermediate', 'Experienced', 'Veteran'])
    
    # Income levels
    df['IncomeLevel'] = pd.cut(df['MonthlyIncome'], bins=[0, 3000, 6000, 10000, 100000],
                               labels=['Low', 'Medium', 'High', 'VeryHigh'])
    
    # Promotion gap
    df['PromotionGap'] = df['YearsSinceLastPromotion'] - df['YearsAtCompany'].apply(lambda x: max(1, x/3))
    
    # Average satisfaction
    satisfaction_cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction']
    df['AvgSatisfaction'] = df[satisfaction_cols].mean(axis=1)
    
    return df

print("Preprocessing and making predictions...")

# Preprocess data
df_processed = engineer_features(df)

# Encode categorical variables
categorical_cols = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 
                   'JobRole', 'MaritalStatus', 'OverTime', 'AgeGroup', 'TenureGroup', 'IncomeLevel']

df_encoded = pd.get_dummies(df_processed, columns=categorical_cols, drop_first=True)

# Ensure all features are present
for col in feature_names:
    if col not in df_encoded.columns:
        df_encoded[col] = 0

# Select and order features
X = df_encoded[feature_names]

# Scale features
X_scaled = scaler.transform(X)

# Make predictions
predictions = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)[:, 1]

# Add predictions to original dataframe
df['PredictedAttrition'] = predictions
df['AttritionProbability'] = (probabilities * 100).round(2)

# Categorize risk
def categorize_risk(prob):
    if prob < 30:
        return 'Low'
    elif prob < 60:
        return 'Medium'
    else:
        return 'High'

df['RiskLevel'] = df['AttritionProbability'].apply(categorize_risk)

# Connect to database
print("Updating database...")
conn = sqlite3.connect('../hr_data.db')

# Save updated data to database
df.to_sql('employees_with_predictions', conn, if_exists='replace', index=False)

# Also update the original employees table
df.to_sql('employees', conn, if_exists='replace', index=False)

print("Database updated successfully!")
print(f"\nNew columns added:")
print("  - PredictedAttrition (0/1)")
print("  - AttritionProbability (0-100%)")
print("  - RiskLevel (Low/Medium/High)")

# Verify
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM employees")
count = cursor.fetchone()[0]
print(f"\nTotal records in database: {count}")

# Show sample
print("\nSample predictions:")
sample = df[['EmployeeId', 'Department', 'JobRole', 'AttritionProbability', 'RiskLevel']].head(10)
print(sample.to_string(index=False))

conn.close()

print("\n" + "="*60)
print("NEXT STEPS:")
print("="*60)
print("1. Restart Metabase container:")
print("   docker restart metabase")
print("\n2. Wait 2-3 minutes, then open http://localhost:3000")
print("\n3. Create new dashboard with prediction visualizations:")
print("   - Risk Level Distribution (Pie Chart)")
print("   - High Risk Employees by Department (Bar Chart)")
print("   - Attrition Probability Distribution (Histogram)")
print("   - Top 10 High Risk Employees (Table)")
print("="*60)
