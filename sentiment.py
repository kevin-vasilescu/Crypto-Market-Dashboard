import pandas as pd
from datetime import datetime
import random

def generate_mock_sentiment_data(coin_name):
    """
    Generate mock sentiment data for demonstration

    Args:
        coin_name (str): Cryptocurrency name

    Returns:
        dict: Mock sentiment summary
    """
    # Generate random but realistic sentiment scores
    positive_bias = random.uniform(0.1, 0.4)  # Slight positive bias for crypto

    return {
        'coin_name': coin_name,
        'total_tweets': random.randint(50, 200),
        'avg_compound_score': random.uniform(-0.2, 0.4),
        'positive_percentage': random.uniform(30, 60),
        'negative_percentage': random.uniform(15, 35),
        'neutral_percentage': random.uniform(20, 40),
        'avg_polarity': random.uniform(-0.1, 0.3),
        'avg_subjectivity': random.uniform(0.4, 0.8),
        'sentiment_trend': random.choice(['bullish', 'bearish', 'neutral']),
        'timestamp': datetime.now()
    }

def get_sentiment_signal(sentiment_summary):
    """
    Generate trading signal based on sentiment analysis

    Args:
        sentiment_summary (dict): Sentiment analysis results

    Returns:
        dict: Trading signal and confidence
    """
    if 'avg_compound_score' not in sentiment_summary:
        return {'signal': 'hold', 'confidence': 0}

    compound_score = sentiment_summary['avg_compound_score']
    positive_pct = sentiment_summary.get('positive_percentage', 0)

    # Simple signal generation logic
    if compound_score > 0.1 and positive_pct > 50:
        signal = 'buy'
        confidence = min(0.8, compound_score + (positive_pct - 50) / 100)
    elif compound_score < -0.1 and positive_pct < 30:
        signal = 'sell'
        confidence = min(0.8, abs(compound_score) + (50 - positive_pct) / 100)
    else:
        signal = 'hold'
        confidence = 0.3

    return {
        'signal': signal,
        'confidence': confidence,
        'reasoning': f"Compound score: {compound_score:.3f}, Positive tweets: {positive_pct:.1f}%"
    }