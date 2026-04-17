#!/usr/bin/env python3
"""
Test script to validate the time series notebooks and identify issues
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

def test_time_series_basics():
    print("=== Testing Time Series Basics ===")
    
    # Step 1: Create sample time series data
    print("1. Creating sample time series data...")
    try:
        # Generate synthetic time series data
        np.random.seed(42)
        dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
        n = len(dates)
        
        # Create a time series with trend, seasonality, and noise
        trend = np.linspace(100, 200, n)
        seasonal = 10 * np.sin(2 * np.pi * np.arange(n) / 365.25)  # Annual seasonality
        noise = np.random.normal(0, 5, n)
        
        ts_data = trend + seasonal + noise
        ts = pd.Series(ts_data, index=dates, name='value')
        
        print(f"✓ Sample time series created: {len(ts)} observations from {ts.index[0]} to {ts.index[-1]}")
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        return False
    
    # Step 2: Basic time series analysis
    print("2. Performing basic time series analysis...")
    try:
        # Basic statistics
        print(f"  - Mean: {ts.mean():.2f}")
        print(f"  - Std: {ts.std():.2f}")
        print(f"  - Min: {ts.min():.2f}")
        print(f"  - Max: {ts.max():.2f}")
        print("✓ Basic analysis completed")
    except Exception as e:
        print(f"✗ Error in basic analysis: {e}")
        return False
    
    # Step 3: Stationarity test
    print("3. Testing stationarity...")
    try:
        result = adfuller(ts.dropna())
        print(f"  - ADF Statistic: {result[0]:.4f}")
        print(f"  - p-value: {result[1]:.4f}")
        print(f"  - Critical Values: {result[4]}")
        
        if result[1] < 0.05:
            print("✓ Series is stationary (p < 0.05)")
        else:
            print("✓ Series is non-stationary (p >= 0.05) - differencing may be needed")
    except Exception as e:
        print(f"✗ Error in stationarity test: {e}")
        return False
    
    # Step 4: Time series decomposition
    print("4. Decomposing time series...")
    try:
        # Use statsmodels for decomposition
        decomposition = sm.tsa.seasonal_decompose(ts, model='additive', period=365)
        
        # Check if decomposition was successful
        if hasattr(decomposition, 'trend'):
            print("✓ Time series decomposition completed")
            print(f"  - Trend component shape: {decomposition.trend.dropna().shape}")
            print(f"  - Seasonal component shape: {decomposition.seasonal.dropna().shape}")
            print(f"  - Residual component shape: {decomposition.resid.dropna().shape}")
        else:
            print("✗ Decomposition failed")
            return False
    except Exception as e:
        print(f"✗ Error in decomposition: {e}")
        return False
    
    return True

def test_arima_modeling():
    print("\n=== Testing ARIMA Modeling ===")
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=365, freq='D')
    ts_data = np.cumsum(np.random.normal(0, 1, 365)) + 100  # Random walk
    ts = pd.Series(ts_data, index=dates, name='value')
    
    # Step 1: Train-test split (temporal)
    print("1. Creating temporal train-test split...")
    try:
        train_size = int(len(ts) * 0.8)
        train = ts[:train_size]
        test = ts[train_size:]
        
        print(f"✓ Train set: {len(train)} observations")
        print(f"✓ Test set: {len(test)} observations")
    except Exception as e:
        print(f"✗ Error in train-test split: {e}")
        return False
    
    # Step 2: ARIMA model fitting
    print("2. Fitting ARIMA model...")
    try:
        # Use simple ARIMA(1,1,1) for testing
        model = ARIMA(train, order=(1,1,1))
        fitted_model = model.fit()
        
        print(f"✓ ARIMA model fitted successfully")
        print(f"  - AIC: {fitted_model.aic:.2f}")
        print(f"  - BIC: {fitted_model.bic:.2f}")
    except Exception as e:
        print(f"✗ Error fitting ARIMA model: {e}")
        return False
    
    # Step 3: Making predictions
    print("3. Making predictions...")
    try:
        # Forecast
        forecast = fitted_model.forecast(steps=len(test))
        forecast_ci = fitted_model.get_forecast(steps=len(test)).conf_int()
        
        print(f"✓ Forecast generated for {len(forecast)} steps")
        print(f"  - Forecast mean: {forecast.mean():.2f}")
        print(f"  - Forecast std: {forecast.std():.2f}")
    except Exception as e:
        print(f"✗ Error in forecasting: {e}")
        return False
    
    # Step 4: Model evaluation
    print("4. Evaluating model performance...")
    try:
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(mean_squared_error(test, forecast))
        mape = np.mean(np.abs((test - forecast) / test)) * 100
        
        print(f"✓ Model evaluation completed")
        print(f"  - MAE: {mae:.4f}")
        print(f"  - RMSE: {rmse:.4f}")
        print(f"  - MAPE: {mape:.2f}%")
    except Exception as e:
        print(f"✗ Error in model evaluation: {e}")
        return False
    
    return True

def test_machine_learning_approach():
    print("\n=== Testing Machine Learning Approach ===")
    
    # Create sample data with features
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=365, freq='D')
    n = len(dates)
    
    # Target variable
    target = np.cumsum(np.random.normal(0, 1, n)) + 100
    
    # Features: lag values, date-based features
    df = pd.DataFrame({
        'date': dates,
        'value': target,
        'lag_1': np.roll(target, 1),
        'lag_7': np.roll(target, 7),
        'day_of_week': dates.dayofweek,
        'month': dates.month,
        'quarter': dates.quarter
    }).dropna()
    
    df.set_index('date', inplace=True)
    
    # Step 1: Feature engineering
    print("1. Creating time series features...")
    try:
        # Create rolling statistics
        df['rolling_mean_7'] = df['value'].rolling(window=7).mean()
        df['rolling_std_7'] = df['value'].rolling(window=7).std()
        df['rolling_mean_30'] = df['value'].rolling(window=30).mean()
        
        # Drop NaN values
        df = df.dropna()
        
        print(f"✓ Features created: {df.shape}")
        print(f"  - Features: {list(df.columns)}")
    except Exception as e:
        print(f"✗ Error in feature engineering: {e}")
        return False
    
    # Step 2: Temporal train-test split
    print("2. Creating temporal train-test split...")
    try:
        train_size = int(len(df) * 0.8)
        train = df[:train_size]
        test = df[train_size:]
        
        X_train = train.drop('value', axis=1)
        y_train = train['value']
        X_test = test.drop('value', axis=1)
        y_test = test['value']
        
        print(f"✓ Train set: {X_train.shape}")
        print(f"✓ Test set: {X_test.shape}")
    except Exception as e:
        print(f"✗ Error in train-test split: {e}")
        return False
    
    # Step 3: Feature scaling
    print("3. Scaling features...")
    try:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print("✓ Features scaled successfully")
    except Exception as e:
        print(f"✗ Error in feature scaling: {e}")
        return False
    
    # Step 4: Model training
    print("4. Training ML model...")
    try:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        print("✓ Random Forest model trained")
        print(f"  - Feature importance: {dict(zip(X_train.columns, model.feature_importances_))}")
    except Exception as e:
        print(f"✗ Error in model training: {e}")
        return False
    
    # Step 5: Prediction and evaluation
    print("5. Making predictions and evaluating...")
    try:
        y_pred = model.predict(X_test_scaled)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"✓ Predictions evaluated")
        print(f"  - MAE: {mae:.4f}")
        print(f"  - RMSE: {rmse:.4f}")
        print(f"  - Mean actual: {y_test.mean():.4f}")
        print(f"  - Mean predicted: {y_pred.mean():.4f}")
    except Exception as e:
        print(f"✗ Error in prediction/evaluation: {e}")
        return False
    
    return True

def test_ttm_availability():
    print("\n=== Testing TinyTimeMixer Availability ===")
    
    try:
        import tsfm_public
        print("✓ TinyTimeMixer (tsfm_public) package is available")
        
        # Try to import key components
        from tsfm_public.toolkit.time_series_forecasting import (
            TimeSeriesForecastingPipeline,
            get_model
        )
        print("✓ TTM forecasting components imported successfully")
        
        return True
    except ImportError as e:
        print(f"⚠ TinyTimeMixer not available: {e}")
        print("  Install with: pip install tsfm-public")
        return False
    except Exception as e:
        print(f"✗ Error testing TTM: {e}")
        return False

def test_visualization():
    print("\n=== Testing Time Series Visualization ===")
    
    try:
        # Create sample data
        np.random.seed(42)
        dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
        ts_data = np.cumsum(np.random.normal(0, 1, 100)) + 100
        ts = pd.Series(ts_data, index=dates, name='value')
        
        # Test basic plotting
        plt.figure(figsize=(12, 6))
        plt.plot(ts.index, ts.values)
        plt.title('Sample Time Series')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.grid(True)
        plt.close()
        
        print("✓ Basic time series plotting works")
        
        # Test decomposition plot
        decomposition = sm.tsa.seasonal_decompose(ts, model='additive', period=30)
        fig = decomposition.plot()
        plt.close()
        
        print("✓ Decomposition plotting works")
        
        return True
    except Exception as e:
        print(f"✗ Error in visualization: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Time Series Notebook Tests\n")
    
    tests = [
        ("Basic Time Series Analysis", test_time_series_basics),
        ("ARIMA Modeling", test_arima_modeling),
        ("Machine Learning Approach", test_machine_learning_approach),
        ("TinyTimeMixer Availability", test_ttm_availability),
        ("Visualization", test_visualization)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The time series notebooks should work correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above and fix dependencies or code issues.")
    
    print("\n💡 Next steps:")
    print("1. Run the notebooks to verify they work with real data")
    print("2. Test with your own time series datasets")
    print("3. Experiment with different model parameters")
    print("4. Try TinyTimeMixer if tsfm-public is installed")
