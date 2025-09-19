import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Import our custom modules
from data_fetch import get_price_data, get_historical_prices, CoinGeckoAPI
from analysis import (calculate_moving_averages, calculate_volatility, 
                     calculate_correlation_matrix)
from plots import (create_price_chart, create_volatility_chart, 
                  create_correlation_heatmap)
from sentiment import generate_mock_sentiment_data, get_sentiment_signal

# Page configuration
st.set_page_config(
    page_title="Crypto Market Dashboard",
    page_icon="â‚¿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #00d4aa, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00d4aa;
    }
    .positive {
        color: #00ff88;
    }
    .negative {
        color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

def main():
    # Header
    st.markdown('<h1 class="main-header">â‚¿ Crypto Market Dashboard</h1>', unsafe_allow_html=True)

    # Sidebar controls
    st.sidebar.title("Dashboard Controls")

    # Cryptocurrency selection
    crypto_options = {
        "Bitcoin": "bitcoin",
        "Ethereum": "ethereum", 
        "Dogecoin": "dogecoin",
        "Cardano": "cardano",
        "Solana": "solana",
        "Polkadot": "polkadot",
        "Chainlink": "chainlink",
        "Litecoin": "litecoin",
        "Polygon": "polygon",
        "Avalanche": "avalanche-2"
    }

    selected_cryptos = st.sidebar.multiselect(
        "Select Cryptocurrencies",
        options=list(crypto_options.keys()),
        default=["Bitcoin", "Ethereum", "Dogecoin"]
    )

    # Date range selection
    date_range = st.sidebar.select_slider(
        "Historical Data Range",
        options=[7, 14, 30, 60, 90],
        value=30,
        format_func=lambda x: f"{x} days"
    )

    # Analysis options
    st.sidebar.subheader("Analysis Options")
    show_ma = st.sidebar.checkbox("Show Moving Averages", True)
    show_volatility = st.sidebar.checkbox("Show Volatility Analysis", True)
    show_correlation = st.sidebar.checkbox("Show Correlation Matrix", True)
    show_sentiment = st.sidebar.checkbox("Show Sentiment Analysis", False)

    # Refresh button
    if st.sidebar.button("Refresh Data"):
        st.session_state.last_update = datetime.now()
        st.rerun()

    # Last update time
    st.sidebar.write(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

    if not selected_cryptos:
        st.warning("Please select at least one cryptocurrency to display data.")
        return

    # Convert selection to API IDs
    selected_ids = [crypto_options[crypto] for crypto in selected_cryptos]

    # Fetch current market data
    with st.spinner("Loading market data..."):
        try:
            market_df = get_price_data(selected_ids)

            if market_df.empty:
                st.error("Unable to fetch market data. Please try again later.")
                return

        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return

    # Display current prices
    st.subheader("Current Market Prices")

    cols = st.columns(min(len(selected_cryptos), 3))
    for i, (_, row) in enumerate(market_df.head(3).iterrows()):
        col = cols[i % 3]

        change_class = "positive" if row['price_change_percentage_24h'] > 0 else "negative"
        change_symbol = "â†—" if row['price_change_percentage_24h'] > 0 else "â†˜"

        with col:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{row['name']} ({row['symbol'].upper()})</h3>
                <h2>${row['current_price']:,.2f}</h2>
                <p class="{change_class}">
                    {change_symbol} {row['price_change_percentage_24h']:.2f}% (24h)
                </p>
                <p>Market Cap: ${row['market_cap']/1e9:.2f}B</p>
                <p>Volume: ${row['total_volume']/1e6:.1f}M</p>
            </div>
            """, unsafe_allow_html=True)

    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["Price Trends", "Volatility Analysis", "Correlation Matrix", "Market Summary"])

    with tab1:
        st.subheader("Price Trends and Moving Averages")

        # Fetch historical data for price trends
        historical_data = {}
        for crypto_id in selected_ids:
            hist_df = get_historical_prices(crypto_id, date_range)
            if not hist_df.empty:
                if show_ma:
                    hist_df = calculate_moving_averages(hist_df)
                historical_data[crypto_id] = hist_df

        if historical_data:
            # Individual charts
            for crypto_id, hist_df in historical_data.items():
                crypto_name = market_df[market_df['id'] == crypto_id]['name'].iloc[0]
                fig = create_price_chart(hist_df, crypto_name, show_ma)
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if show_volatility:
            st.subheader("Volatility Analysis")

            for crypto_id in selected_ids:
                hist_df = get_historical_prices(crypto_id, date_range)
                if not hist_df.empty:
                    hist_df = calculate_volatility(hist_df)
                    crypto_name = market_df[market_df['id'] == crypto_id]['name'].iloc[0]

                    fig_vol = create_volatility_chart(hist_df, crypto_name)
                    st.plotly_chart(fig_vol, use_container_width=True)

                    # Display volatility statistics
                    if 'volatility' in hist_df.columns:
                        avg_vol = hist_df['volatility'].mean()
                        current_vol = hist_df['volatility'].iloc[-1]
                        st.write(f"**{crypto_name} Volatility Stats:**")
                        st.write(f"- Current 30-day volatility: {current_vol:.4f}")
                        st.write(f"- Average volatility: {avg_vol:.4f}")

    with tab3:
        if show_correlation and len(selected_ids) > 1:
            st.subheader("Price Correlation Matrix")

            # Fetch price data for correlation analysis
            price_data = {}
            for crypto_id in selected_ids:
                hist_df = get_historical_prices(crypto_id, date_range)
                if not hist_df.empty:
                    price_data[crypto_id] = hist_df

            if len(price_data) > 1:
                corr_matrix = calculate_correlation_matrix(price_data)
                if not corr_matrix.empty:
                    fig_corr = create_correlation_heatmap(corr_matrix)
                    st.plotly_chart(fig_corr, use_container_width=True)

                    st.write("**Correlation Insights:**")
                    st.write("- Values close to 1 indicate strong positive correlation")
                    st.write("- Values close to -1 indicate strong negative correlation") 
                    st.write("- Values close to 0 indicate no correlation")

    with tab4:
        st.subheader("Market Summary")

        # Summary statistics table
        summary_data = []
        for _, row in market_df.iterrows():
            summary_data.append({
                "Cryptocurrency": f"{row['name']} ({row['symbol'].upper()})",
                "Current Price": f"${row['current_price']:,.2f}",
                "24h Change": f"{row['price_change_percentage_24h']:+.2f}%",
                "Market Cap": f"${row['market_cap']/1e9:.2f}B",
                "Volume (24h)": f"${row['total_volume']/1e6:.1f}M",
                "Market Rank": int(row['market_cap_rank'])
            })

        summary_df = pd.DataFrame(summary_data)
        st.table(summary_df)

        # Sentiment analysis (mock data)
        if show_sentiment:
            st.subheader("Sentiment Analysis")
            st.info("Note: This is a demonstration using mock sentiment data. "
                   "Real implementation requires Twitter API credentials.")

            sentiment_cols = st.columns(len(selected_cryptos))
            for i, crypto_id in enumerate(selected_ids):
                crypto_name = market_df[market_df['id'] == crypto_id]['name'].iloc[0]
                sentiment_data = generate_mock_sentiment_data(crypto_name)
                signal_data = get_sentiment_signal(sentiment_data)

                with sentiment_cols[i % len(sentiment_cols)]:
                    st.write(f"**{crypto_name} Sentiment**")
                    st.write(f"ðŸ“Š Tweets analyzed: {sentiment_data['total_tweets']}")
                    st.write(f"ðŸ˜Š Positive: {sentiment_data['positive_percentage']:.1f}%")
                    st.write(f"ðŸ˜ Neutral: {sentiment_data['neutral_percentage']:.1f}%") 
                    st.write(f"ðŸ˜Ÿ Negative: {sentiment_data['negative_percentage']:.1f}%")
                    st.write(f"ðŸ“ˆ Signal: {signal_data['signal'].upper()}")
                    st.write(f"ðŸŽ¯ Confidence: {signal_data['confidence']:.1%}")

if __name__ == "__main__":
    main()