#!/usr/bin/env python3
"""
Test script to validate the notebook code and identify issues
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import kagglehub

def test_notebook_workflow():
    print("=== Testing Notebook Workflow ===")
    
    # Step 1: Load dataset
    print("1. Loading dataset...")
    try:
        path = kagglehub.dataset_download("blastchar/telco-customer-churn")
        df = pd.read_csv(path + "/WA_Fn-UseC_-Telco-Customer-Churn.csv")
        print(f"✓ Dataset loaded: {df.shape}")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        return False
    
    # Step 2: Data preprocessing
    print("2. Preprocessing data...")
    try:
        # Drop customerID
        df = df.drop('customerID', axis=1)
        
        # Map Churn to binary
        df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
        
        # Fix TotalCharges - convert to numeric and handle missing values
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].fillna(0)  # Fill missing values
        
        # Convert categorical variables to dummies
        df = pd.get_dummies(df, drop_first=True)
        print(f"✓ Data preprocessed: {df.shape}")
    except Exception as e:
        print(f"✗ Error preprocessing data: {e}")
        return False
    
    # Step 3: Split data
    print("3. Splitting data...")
    try:
        X = df.drop('Churn', axis=1)
        y = df['Churn']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(f"✓ Data split: Train={X_train.shape}, Test={X_test.shape}")
    except Exception as e:
        print(f"✗ Error splitting data: {e}")
        return False
    
    # Step 4: Scale features
    print("4. Scaling features...")
    try:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        print("✓ Features scaled")
    except Exception as e:
        print(f"✗ Error scaling features: {e}")
        return False
    
    # Step 5: Train model
    print("5. Training model...")
    try:
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        print("✓ Model trained")
    except Exception as e:
        print(f"✗ Error training model: {e}")
        return False
    
    # Step 6: Evaluate model
    print("6. Evaluating model...")
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"✓ Model evaluated. Accuracy: {accuracy:.4f}")
        
        # Additional metrics
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return True
    except Exception as e:
        print(f"✗ Error evaluating model: {e}")
        return False

if __name__ == "__main__":
    success = test_notebook_workflow()
    if success:
        print("\n🎉 All tests passed! The notebook workflow is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
