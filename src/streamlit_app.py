import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# Set page config 
st.set_page_config(page_title="📈 Cryptoto ", layout="wide")

# Layout
st.title("📈 Cryptoto Trading Dashboard 📈")

# Select Time Window 
col1, col2, col3 = st.columns(3)
with col1: 
    time_period = st.selectbox("Select a time period:", ["Validation (Jan - Feb) 📋", "Testing (March) 🔎"])

# Metrics - Update if changed 
m_testing = {'Annualised Return': -5.4, 'Sharpe': 0.19,
             'Max Drawdown': -10.56, 'Win Rate': 40.00, 
             'Annual Volatility': 65.86, 'Drawdown Patterns': 3,
             'Number of Trades': 18, 'Average Holding Period': 8.13,
             'Profit per trade': -203.83}

m_validation = {'Annualised Return': 12.7, 'Sharpe': 0.35,
             'Max Drawdown': -12.73, 'Win Rate': 55.56, 
             'Annual Volatility': 56.78, 'Drawdown Patterns': 11,
             'Number of Trades': 45, 'Average Holding Period': 6.42,
             'Profit per trade': 520.37}

# Load data  
if time_period == "Validation (Jan - Feb) 📋":
    trade_log = pd.read_csv("../data/misc/trade_log_validation.csv")
    daily_portfolio = pd.read_csv("../data/misc/daily_portfolio_value_validation.csv").set_index("date")
    metrics = m_validation
else:
    trade_log = pd.read_csv("../data/misc/trade_log.csv")
    daily_portfolio = pd.read_csv("../data/misc/daily_portfolio_value.csv").set_index("date")
    metrics = m_testing

trade_log['date'] = pd.to_datetime(trade_log['date'])
daily_portfolio.index = pd.to_datetime(daily_portfolio.index)

strategy_map = pd.read_csv("../data/experiments/asset_strategies_2_months_with_tpsl.csv")
idx= strategy_map.groupby("Asset")["Sharpe Ratio"].idxmax()
best = strategy_map.loc[idx]
asset_strategies = best[["Asset", "Weight", "Strategy"]]
asset_strategies = asset_strategies.set_index("Asset")

# Graph plotting functions
def plot_portfolio_value(portfolio_value: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=portfolio_value.index,
        y=portfolio_value['portfolio_value'],
        mode='lines',
        name='Portfolio Value'
    ))
    fig.update_layout(
        title=f'Portfolio Value Over Time - {time_period}',
        xaxis_title='Date',
        yaxis_title='Portfolio Value',
        template='plotly_white'
    )
    fig.update_xaxes(nticks = 15)
    st.plotly_chart(fig, use_container_width=True)

def plot_candlestick(asset_name: str, trades: pd.DataFrame):
    if time_period == "Validation (Jan - Feb) 📋":
        df = yf.Ticker(asset_name).history(start="2025-01-01", end="2025-03-01", actions=False)
    else:
        df = yf.Ticker(asset_name).history(start="2025-03-01", end="2025-04-01", actions=False)
    # Create figure 
    fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name=asset_name
        )])  
    for _, trade in trades.iterrows():
        trade_date = trade['date']
        action = trade['action']

        # Add vertical line
        fig.add_vline(
            x=trade_date, 
            line=dict(color="blue", width=2, dash="dash"),  # blue dashed line
            name=f"{action} on {trade_date.strftime('%Y-%m-%d')}"
        )
    # Add annotation for the action
        fig.add_annotation(
            x=trade_date,
            y=df['Low'].min() - 5,  
            text=action,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            ax=0,
            ay=-40,
            font=dict(color="white")
        )        
    # Layout settings
    fig.update_layout(
        title=f"Candlestick Chart for {asset_name} - {time_period}",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,  # Hide the default range slider
        template="plotly_white"
    )
     # Display the interactive chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2, border = True)

# Metrics Panel
with col1:
    st.subheader("Key Metrics")
    col11, col12, col13 = st.columns([1, 1, 1])
    with col11: 
        st.metric(label="Annualised Return [%]", value=f"{metrics['Annualised Return']}")
    with col12:
        st.metric(label="Sharpe Ratio", value=f"{metrics['Sharpe']}")
    with col13: 
        st.metric(label="Max Drawdown [%]", value=f"{metrics['Max Drawdown']}")
    col21, col22, col23 = st.columns([1, 1, 1])
    with col21: 
        st.metric(label="Win Rate [%]", value=f"{metrics['Win Rate']}")
    with col22:
        st.metric(label="Annual Volatility [%]", value=f"{metrics['Annual Volatility']}")
    with col23: 
        st.metric(label="Drawdown Patterns", value=f"{metrics['Drawdown Patterns']}")
    col31, col32, col33 = st.columns([1, 1, 1])
    with col21: 
        st.metric(label="Number of Trades", value=f"{metrics['Number of Trades']}")
    with col22:
        st.metric(label="Average Holding Period", value=f"{metrics['Average Holding Period']}")
    with col23: 
        st.metric(label="Profit per trade", value=f"{metrics['Profit per trade']}")

# Trade Log
with col2:
    st.subheader("Trade Log")
    st.dataframe(trade_log.style.set_table_styles(
        [{"selector": "thead", "props": "background-color: #222222; color: white;"}],
    ), use_container_width=True, height=300)

# Portfolio Value
with st.container():
    plot_portfolio_value(daily_portfolio)

col1, col2, col3 = st.columns(3)
with col1: 
    #unique_assets = trade_log['asset'].unique()
    unique_assets = asset_strategies.index
    asset_name = st.selectbox("Select an asset:", unique_assets, index=14)
    asset_strat = asset_strategies.loc[asset_name, "Strategy"]
    st.write(f"{asset_name} uses strategy {asset_strat}")

with st.container():
    relevant_trades = trade_log[trade_log["asset"] == asset_name]
    plot_candlestick(asset_name, relevant_trades)