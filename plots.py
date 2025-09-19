import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

def create_price_chart(df, coin_name="Cryptocurrency", show_ma=True):
    """
    Create an interactive price chart with moving averages

    Args:
        df (pd.DataFrame): Price data with timestamp index
        coin_name (str): Name of the cryptocurrency
        show_ma (bool): Whether to show moving averages

    Returns:
        plotly.graph_objects.Figure: Interactive price chart
    """
    fig = go.Figure()

    # Add price line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['price'],
        mode='lines',
        name=f'{coin_name} Price',
        line=dict(color='#00d4aa', width=2),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                     'Date: %{x}<br>' +
                     'Price: $%{y:,.2f}<extra></extra>'
    ))

    # Add moving averages if available and requested
    if show_ma:
        ma_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
        ma_columns = [col for col in df.columns if col.startswith('MA_')]

        for i, ma_col in enumerate(ma_columns):
            if i < len(ma_colors):
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[ma_col],
                    mode='lines',
                    name=f'{ma_col.replace("_", " ")}',
                    line=dict(color=ma_colors[i], width=1.5),
                    opacity=0.8,
                    hovertemplate=f'<b>{ma_col.replace("_", " ")}</b><br>' +
                                 'Date: %{x}<br>' +
                                 'Price: $%{y:,.2f}<extra></extra>'
                ))

    # Update layout
    fig.update_layout(
        title=f'{coin_name} Price Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        hovermode='x unified',
        showlegend=True,
        height=500
    )

    return fig

def create_volatility_chart(df, coin_name="Cryptocurrency"):
    """
    Create volatility chart

    Args:
        df (pd.DataFrame): Data with volatility column
        coin_name (str): Name of the cryptocurrency

    Returns:
        plotly.graph_objects.Figure: Volatility chart
    """
    fig = go.Figure()

    if 'volatility' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['volatility'],
            mode='lines',
            fill='tozeroy',
            name=f'{coin_name} Volatility',
            line=dict(color='#ff6b6b'),
            hovertemplate='<b>Volatility</b><br>' +
                         'Date: %{x}<br>' +
                         'Volatility: %{y:.4f}<extra></extra>'
        ))

    fig.update_layout(
        title=f'{coin_name} Price Volatility (30-day)',
        xaxis_title='Date',
        yaxis_title='Volatility',
        template='plotly_dark',
        height=400
    )

    return fig

def create_correlation_heatmap(correlation_matrix):
    """
    Create correlation heatmap

    Args:
        correlation_matrix (pd.DataFrame): Correlation matrix

    Returns:
        plotly.graph_objects.Figure: Correlation heatmap
    """
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdYlBu',
        zmid=0,
        text=correlation_matrix.round(3).values,
        texttemplate='%{text}',
        textfont={"size": 12},
        hovertemplate='<b>%{y} vs %{x}</b><br>' +
                     'Correlation: %{z:.3f}<extra></extra>'
    ))

    fig.update_layout(
        title='Cryptocurrency Price Correlations',
        template='plotly_dark',
        height=500,
        width=600
    )

    return fig