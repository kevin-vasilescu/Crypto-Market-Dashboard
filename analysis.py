import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_moving_averages(df, windows=[7, 30, 50]):
    """
    Calculate simple moving averages for price data

    Args:
        df (pd.DataFrame): Price data with 'price' column
        windows (list): List of window sizes for moving averages

    Returns:
        pd.DataFrame: DataFrame with moving averages added
    """
    df_ma = df.copy()

    for window in windows:
        df_ma[f'MA_{window}'] = df_ma['price'].rolling(window=window, min_periods=1).mean()

    return df_ma

def calculate_volatility(df, window=30):
    """
    Calculate rolling volatility (standard deviation of returns)

    Args:
        df (pd.DataFrame): Price data with 'price' column
        window (int): Window size for volatility calculation

    Returns:
        pd.DataFrame: DataFrame with volatility added
    """
    df_vol = df.copy()

    # Calculate returns
    df_vol['returns'] = df_vol['price'].pct_change()

    # Calculate rolling volatility
    df_vol['volatility'] = df_vol['returns'].rolling(window=window, min_periods=1).std()

    # Annualized volatility (assuming daily data)
    df_vol['volatility_annualized'] = df_vol['volatility'] * np.sqrt(365)

    return df_vol

def calculate_correlation_matrix(price_data_dict):
    """
    Calculate correlation matrix between different cryptocurrencies

    Args:
        price_data_dict (dict): Dictionary with coin_id as keys and price DataFrames as values

    Returns:
        pd.DataFrame: Correlation matrix
    """
    # Combine all price data
    combined_df = pd.DataFrame()

    for coin_id, df in price_data_dict.items():
        if not df.empty and 'price' in df.columns:
            combined_df[coin_id] = df['price']

    if combined_df.empty:
        return pd.DataFrame()

    # Calculate correlation matrix
    correlation_matrix = combined_df.corr()

    return correlation_matrix