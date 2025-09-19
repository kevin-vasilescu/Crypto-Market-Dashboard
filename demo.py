# Demo Script for Crypto Dashboard
# This script demonstrates the functionality of the crypto dashboard modules

from data_fetch import get_price_data, get_historical_prices
from analysis import calculate_moving_averages, calculate_volatility, calculate_correlation_matrix
from plots import create_price_chart, create_volatility_chart, create_correlation_heatmap
from sentiment import generate_mock_sentiment_data, get_sentiment_signal
import pandas as pd

def demo_data_fetching():
    """Demonstrate data fetching capabilities"""
    print("=== DATA FETCHING DEMO ===")

    # Test fetching current prices for popular cryptocurrencies
    coins = ['bitcoin', 'ethereum', 'dogecoin']
    print(f"Fetching current prices for: {coins}")

    try:
        df = get_price_data(coins)
        if not df.empty:
            print("âœ“ Successfully fetched market data")
            print(f"Columns: {list(df.columns)}")
            print(f"Number of cryptocurrencies: {len(df)}")
        else:
            print("âœ— No data returned (API might be unavailable)")
    except Exception as e:
        print(f"âœ— Error fetching data: {e}")

    # Test fetching historical data
    print("\nFetching historical data for Bitcoin...")
    try:
        hist_df = get_historical_prices('bitcoin', days=30)
        if not hist_df.empty:
            print(f"âœ“ Successfully fetched {len(hist_df)} data points")
            print(f"Date range: {hist_df.index.min()} to {hist_df.index.max()}")
        else:
            print("âœ— No historical data returned")
    except Exception as e:
        print(f"âœ— Error fetching historical data: {e}")

def demo_analysis():
    """Demonstrate analysis capabilities"""
    print("\n=== ANALYSIS DEMO ===")

    # Create sample price data for demonstration
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    sample_prices = [50000 + i*100 + (i%7)*500 for i in range(len(dates))]
    sample_df = pd.DataFrame({'price': sample_prices}, index=dates)

    print("Using sample price data for analysis...")

    # Moving averages
    ma_df = calculate_moving_averages(sample_df, [7, 14, 30])
    print(f"âœ“ Calculated moving averages: {[col for col in ma_df.columns if 'MA_' in col]}")

    # Volatility analysis
    vol_df = calculate_volatility(ma_df)
    if 'volatility' in vol_df.columns:
        print(f"âœ“ Calculated volatility - Average: {vol_df['volatility'].mean():.4f}")

    # Correlation matrix (requires multiple assets)
    sample_data = {
        'bitcoin': sample_df,
        'ethereum': pd.DataFrame({'price': [p * 0.06 for p in sample_prices]}, index=dates)
    }
    corr_matrix = calculate_correlation_matrix(sample_data)
    if not corr_matrix.empty:
        print(f"âœ“ Calculated correlation matrix: {corr_matrix.shape}")

def demo_sentiment():
    """Demonstrate sentiment analysis capabilities"""
    print("\n=== SENTIMENT ANALYSIS DEMO ===")

    coins = ['Bitcoin', 'Ethereum', 'Dogecoin']
    for coin in coins:
        sentiment_data = generate_mock_sentiment_data(coin)
        signal_data = get_sentiment_signal(sentiment_data)

        print(f"\n{coin} Sentiment:")
        print(f"  Tweets analyzed: {sentiment_data['total_tweets']}")
        print(f"  Positive sentiment: {sentiment_data['positive_percentage']:.1f}%")
        print(f"  Trading signal: {signal_data['signal'].upper()}")
        print(f"  Confidence: {signal_data['confidence']:.1%}")

def main():
    """Run all demo functions"""
    print("CRYPTO DASHBOARD DEMO")
    print("=" * 50)

    demo_data_fetching()
    demo_analysis() 
    demo_sentiment()

    print("\n" + "=" * 50)
    print("Demo completed! âœ“")
    print("\nTo run the full dashboard:")
    print("streamlit run app.py")

if __name__ == "__main__":
    main()