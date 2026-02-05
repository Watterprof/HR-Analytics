"""
Employee Attrition Prediction Script
=====================================
This script loads the trained model and predicts employee attrition risk.

Usage:
    python predict.py --age 35 --department Sales --monthly_income 5000 ...
    
Or use a JSON file:
    python predict.py --json_file sample_employee.json
"""

import joblib
import pandas as pd
import numpy as np
import argparse
import json
import os
import sys

# Load models
MODEL_PATH = '../models/best_model.pkl'
SCALER_PATH = '../models/scaler.pkl'
FEATURES_PATH = '../models/feature_names.pkl'

def load_models():
    """Load the trained model, scaler, and feature names"""
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        feature_names = joblib.load(FEATURES_PATH)
        return model, scaler, feature_names
    except FileNotFoundError as e:
        print(f"Error: Model files not found. Please train the model first.")
        print(f"Missing file: {e.filename}")
        sys.exit(1)

def preprocess_input(data, feature_names):
    """Preprocess input data to match training format"""
    
    # Create DataFrame
    df = pd.DataFrame([data])
    
    # Feature Engineering (same as training)
    if 'Age' in df.columns:
        df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 100], 
                               labels=['<30', '30-40', '40-50', '50+'])
    
    if 'YearsAtCompany' in df.columns:
        df['TenureGroup'] = pd.cut(df['YearsAtCompany'], bins=[0, 2, 5, 10, 50], 
                                  labels=['0-2', '2-5', '5-10', '10+'])
    
    if 'MonthlyIncome' in df.columns:
        df['IncomeLevel'] = pd.cut(df['MonthlyIncome'], bins=[0, 3000, 6000, 10000, 20000], 
                                  labels=['Low', 'Medium', 'High', 'Very High'])
    
    if 'YearsAtCompany' in df.columns and 'YearsSinceLastPromotion' in df.columns:
        df['PromotionGap'] = df['YearsAtCompany'] - df['YearsSinceLastPromotion']
    
    if all(col in df.columns for col in ['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction']):
        df['AvgSatisfaction'] = (df['JobSatisfaction'] + 
                                df['EnvironmentSatisfaction'] + 
                                df['RelationshipSatisfaction']) / 3
    
    # Encode binary variables
    if 'Gender' in df.columns:
        df['Gender'] = 1 if df['Gender'].iloc[0] == 'Male' else 0
    if 'OverTime' in df.columns:
        df['OverTime'] = 1 if df['OverTime'].iloc[0] == 'Yes' else 0
    
    # One-hot encoding
    categorical_cols = ['BusinessTravel', 'Department', 'EducationField', 'JobRole', 
                       'MaritalStatus', 'AgeGroup', 'TenureGroup', 'IncomeLevel']
    
    for col in categorical_cols:
        if col in df.columns:
            df = pd.get_dummies(df, columns=[col], drop_first=True)
    
    # Ensure all features from training are present
    for feature in feature_names:
        if feature not in df.columns:
            df[feature] = 0
    
    # Select only the features used in training
    df = df[feature_names]
    
    return df

def predict_attrition(employee_data):
    """Predict attrition for a single employee"""
    
    # Load models
    model, scaler, feature_names = load_models()
    
    # Preprocess input
    X = preprocess_input(employee_data, feature_names)
    
    # Make prediction
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    
    # Determine risk level
    attrition_prob = probability[1]
    if attrition_prob < 0.3:
        risk_level = "Low"
    elif attrition_prob < 0.6:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    return {
        'prediction': 'Will Leave' if prediction == 1 else 'Will Stay',
        'attrition_probability': float(attrition_prob),
        'retention_probability': float(probability[0]),
        'risk_level': risk_level
    }

def main():
    parser = argparse.ArgumentParser(description='Predict employee attrition')
    parser.add_argument('--json_file', type=str, help='Path to JSON file with employee data')
    parser.add_argument('--age', type=int, help='Employee age')
    parser.add_argument('--department', type=str, help='Department')
    parser.add_argument('--monthly_income', type=int, help='Monthly income')
    parser.add_argument('--overtime', type=str, help='Overtime (Yes/No)')
    parser.add_argument('--years_at_company', type=int, help='Years at company')
    
    args = parser.parse_args()
    
    if args.json_file:
        # Load from JSON file
        with open(args.json_file, 'r') as f:
            employee_data = json.load(f)
    else:
        # Use command line arguments (simplified example)
        employee_data = {
            'Age': args.age if args.age else 35,
            'Department': args.department if args.department else 'Sales',
            'MonthlyIncome': args.monthly_income if args.monthly_income else 5000,
            'OverTime': args.overtime if args.overtime else 'No',
            'YearsAtCompany': args.years_at_company if args.years_at_company else 5
        }
    
    # Make prediction
    result = predict_attrition(employee_data)
    
    # Display results
    print("\n" + "="*50)
    print("EMPLOYEE ATTRITION PREDICTION")
    print("="*50)
    print(f"\nPrediction: {result['prediction']}")
    print(f"Attrition Probability: {result['attrition_probability']:.2%}")
    print(f"Retention Probability: {result['retention_probability']:.2%}")
    print(f"Risk Level: {result['risk_level']}")
    print("\n" + "="*50)
    
    if result['risk_level'] in ['Medium', 'High']:
        print("\n⚠️  RECOMMENDATION: Consider retention interventions")
        print("   - Review compensation and benefits")
        print("   - Assess work-life balance")
        print("   - Provide career development opportunities")
        print("   - Conduct stay interview")
    
    return result

if __name__ == "__main__":
    main()
