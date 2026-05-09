import streamlit as st
import yfinance as yf

# --- Page Config ---
st.set_page_config(page_title="10-Year Stock Predictor", layout="wide")

st.title("📈 10-Year Fundamental Price Predictor")

# --- Sidebar Inputs ---
st.sidebar.header("User Inputs")
ticker_symbol = st.sidebar.text_input("Enter Ticker Symbol", value="SBIN.NS").upper()
forecast_years = st.sidebar.slider("Forecast Horizon (Years)", 1, 20, 10)

@st.cache_data
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        return stock.info
    except:
        return None

info = get_stock_data(ticker_symbol)

if info and info.get('trailingEps'):
    current_price = info.get('currentPrice', 0.0)
    current_eps = info.get('trailingEps', 0.0)
    current_pe = info.get('trailingPE', 15.0)
    
    growth_val = info.get('earningsGrowth')
    historical_growth = growth_val if growth_val else 0.10
    
    st.sidebar.subheader("Adjust Assumptions")
    growth_rate = st.sidebar.number_input("Annual Growth Rate (%)", value=float(historical_growth * 100)) / 100
    target_pe = st.sidebar.number_input("Target P/E Ratio (Exit Multiple)", value=float(current_pe))

    # Calculations
    future_eps = current_eps * ((1 + growth_rate) ** forecast_years)
    future_price = future_eps * target_pe
    
    # UI Layout
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Price", f"₹{current_price:,.2f}")
        st.metric("Current EPS", f"{current_eps:.2f}")
    with col2:
        st.metric(f"Predicted Price ({forecast_years}y)", f"₹{future_price:,.2f}")
        st.metric("Future EPS", f"{future_eps:.2f}")

    # --- MANUAL MARKDOWN TABLE (No PyArrow needed) ---
    st.subheader("Forecast Breakdown")
    markdown_table = f"""
| Metric | Current (Actual) | Future ({forecast_years}y) |
| :--- | :--- | :--- |
| **Earnings Per Share** | {current_eps:.2f} | {future_eps:.2f} |
| **P/E Multiple** | {current_pe:.2f} | {target_pe:.2f} |
| **Share Price** | ₹{current_price:,.2f} | **₹{future_price:,.2f}** |
"""
    st.markdown(markdown_table)

    st.info(f"💡 Based on {growth_rate:.2%} growth, the stock reaches ₹{future_price:.2f} in {forecast_years} years.")

else:
    st.error("Could not fetch data. Please check the ticker symbol.")
