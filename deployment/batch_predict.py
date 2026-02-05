"""
Batch Prediction Script for Employee Attrition
Predicts attrition risk for all employees and generates action report
"""

import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load model and preprocessing objects
print("Loading model and preprocessing objects...")
model = joblib.load('../models/best_model.pkl')
scaler = joblib.load('../models/scaler.pkl')
feature_names = joblib.load('../models/feature_names.pkl')

print("✅ Model loaded successfully!\n")

# Load employee data
print("Loading employee data...")
df = pd.read_csv('../employee_data.csv')
print(f"Loaded {len(df)} employees\n")

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

# Preprocess data
print("Preprocessing data...")
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
print("Making predictions...\n")
predictions = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)[:, 1]

# Add predictions to dataframe
df['AttritionPrediction'] = predictions
df['AttritionProbability'] = probabilities * 100

# Categorize risk
def categorize_risk(prob):
    if prob < 30:
        return 'Low'
    elif prob < 60:
        return 'Medium'
    else:
        return 'High'

df['RiskLevel'] = df['AttritionProbability'].apply(categorize_risk)

# Generate recommendations
def generate_recommendation(row):
    recommendations = []
    
    if row['OverTime'] == 'Yes':
        recommendations.append("Reduce overtime")
    if row['MonthlyIncome'] < 3000:
        recommendations.append("Review compensation")
    if row['WorkLifeBalance'] < 3:
        recommendations.append("Improve work-life balance")
    if row['JobSatisfaction'] < 3:
        recommendations.append("Address job satisfaction")
    if row['YearsSinceLastPromotion'] > 3:
        recommendations.append("Consider promotion/career development")
    if row['YearsAtCompany'] < 2:
        recommendations.append("Enhanced onboarding & mentorship")
    
    return '; '.join(recommendations) if recommendations else 'Monitor regularly'

df['Recommendations'] = df.apply(generate_recommendation, axis=1)

# ============================================
# GENERATE REPORTS
# ============================================

print("="*60)
print("EMPLOYEE ATTRITION RISK REPORT")
print("="*60)

# Overall statistics
print(f"\n📊 OVERALL STATISTICS:")
print(f"Total Employees: {len(df)}")
print(f"High Risk: {len(df[df['RiskLevel'] == 'High'])} ({len(df[df['RiskLevel'] == 'High'])/len(df)*100:.1f}%)")
print(f"Medium Risk: {len(df[df['RiskLevel'] == 'Medium'])} ({len(df[df['RiskLevel'] == 'Medium'])/len(df)*100:.1f}%)")
print(f"Low Risk: {len(df[df['RiskLevel'] == 'Low'])} ({len(df[df['RiskLevel'] == 'Low'])/len(df)*100:.1f}%)")

# High risk employees
high_risk = df[df['RiskLevel'] == 'High'].sort_values('AttritionProbability', ascending=False)

print(f"\n🚨 HIGH RISK EMPLOYEES (Top 10):")
print("-" * 60)
for idx, row in high_risk.head(10).iterrows():
    print(f"\nEmployee ID: {row['EmployeeId']}")
    print(f"  Department: {row['Department']}")
    print(f"  Job Role: {row['JobRole']}")
    print(f"  Attrition Risk: {row['AttritionProbability']:.1f}%")
    print(f"  Recommendations: {row['Recommendations']}")

# Department-level analysis
print(f"\n📈 RISK BY DEPARTMENT:")
print("-" * 60)
dept_risk = df.groupby('Department').agg({
    'AttritionProbability': 'mean',
    'EmployeeId': 'count'
}).round(2)
dept_risk.columns = ['Avg Risk %', 'Employee Count']
print(dept_risk.sort_values('Avg Risk %', ascending=False))

# Save detailed report
output_file = 'attrition_risk_report.csv'
report_columns = ['EmployeeId', 'Department', 'JobRole', 'Age', 'YearsAtCompany', 
                 'MonthlyIncome', 'OverTime', 'WorkLifeBalance', 'JobSatisfaction',
                 'AttritionProbability', 'RiskLevel', 'Recommendations']

df[report_columns].sort_values('AttritionProbability', ascending=False).to_csv(output_file, index=False)

print(f"\n✅ Detailed report saved to: {output_file}")

# Generate action plan for HR
print("\n" + "="*60)
print("🎯 IMMEDIATE ACTION PLAN FOR HR")
print("="*60)

print("\n1. PRIORITY INTERVENTIONS (High Risk Employees):")
print(f"   - Schedule 1-on-1 meetings with {len(high_risk)} high-risk employees")
print(f"   - Conduct stay interviews")
print(f"   - Review compensation packages")

print("\n2. DEPARTMENT-SPECIFIC ACTIONS:")
for dept in df['Department'].unique():
    dept_data = df[df['Department'] == dept]
    high_risk_count = len(dept_data[dept_data['RiskLevel'] == 'High'])
    avg_risk = dept_data['AttritionProbability'].mean()
    
    if high_risk_count > 0:
        print(f"   - {dept}: {high_risk_count} high-risk employees (Avg: {avg_risk:.1f}%)")
        print(f"     Action: Review workload, overtime, and satisfaction")

print("\n3. SYSTEMIC IMPROVEMENTS:")
overtime_high_risk = df[(df['OverTime'] == 'Yes') & (df['RiskLevel'] == 'High')]
if len(overtime_high_risk) > 0:
    print(f"   - Reduce overtime for {len(overtime_high_risk)} employees")

low_income_high_risk = df[(df['MonthlyIncome'] < 3000) & (df['RiskLevel'] == 'High')]
if len(low_income_high_risk) > 0:
    print(f"   - Review compensation for {len(low_income_high_risk)} low-income employees")

print("\n4. MONITORING:")
print(f"   - Re-run this analysis monthly")
print(f"   - Track attrition rate changes")
print(f"   - Measure intervention effectiveness")

print("\n" + "="*60)
print("Report generation complete!")
print("="*60)
