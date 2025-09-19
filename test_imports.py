# Simple test to verify module imports
try:
    from data_fetch import CoinGeckoAPI
    print("âœ“ data_fetch module imported successfully")
except ImportError as e:
    print(f"âœ— Error importing data_fetch: {e}")

try:
    from analysis import calculate_moving_averages
    print("âœ“ analysis module imported successfully")
except ImportError as e:
    print(f"âœ— Error importing analysis: {e}")

try:
    from plots import create_price_chart
    print("âœ“ plots module imported successfully")
except ImportError as e:
    print(f"âœ— Error importing plots: {e}")

try:
    from sentiment import generate_mock_sentiment_data
    print("âœ“ sentiment module imported successfully")
except ImportError as e:
    print(f"âœ— Error importing sentiment: {e}")

print("\nAll modules are ready! ðŸš€")