import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from google import genai

# ---------------------
# GEMINI API
# ---------------------

API_KEY = "amit"

client = genai.Client(api_key=API_KEY)

# ---------------------
# PAGE CONFIG
# ---------------------

st.set_page_config(
    page_title="TradeMaster Pro",
    page_icon="📈",
    layout="wide"
)

st.title("📈 TradeMaster Pro")
st.subheader("Nifty | IPO | SIP | EMI | Intraday Trading Assistant")

# ---------------------
# SIDEBAR
# ---------------------

menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Nifty Dashboard",
        "Intraday Analysis",
        "Candlestick Analysis",
        "IPO Analysis",
        "SIP Calculator",
        "EMI Calculator",
        "AI Trading Chat"
    ]
)

# ---------------------
# NIFTY DASHBOARD
# ---------------------

if menu == "Nifty Dashboard":

    st.header("Nifty 50 Dashboard")

    ticker = "^NSEI"

    data = yf.download(
        ticker,
        period="1mo",
        interval="1d"
    )

    st.write(data.tail())

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"]
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    last_close = data["Close"].iloc[-1]
    prev_close = data["Close"].iloc[-2]

    if last_close > prev_close:
        st.success("Bullish Trend")
    else:
        st.error("Bearish Trend")

# ---------------------
# INTRADAY ANALYSIS
# ---------------------

elif menu == "Intraday Analysis":

    st.header("Intraday Trading Analysis")

    index_name = st.selectbox(
        "Select Index",
        [
            "NIFTY",
            "BANKNIFTY"
        ]
    )

    query = f"""
    Analyze {index_name}.

    Provide:
    1. Overall Trend
    2. Bullish or Bearish
    3. Key Support
    4. Key Resistance
    5. Intraday Strategy
    6. Risk Management
    7. Important Levels
    """

    if st.button("Generate Analysis"):

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=query
        )

        st.write(response.text)

# ---------------------
# CANDLESTICK ANALYSIS
# ---------------------

elif menu == "Candlestick Analysis":

    st.header("Candlestick Pattern Analysis")

    pattern = st.selectbox(
        "Select Pattern",
        [
            "Hammer",
            "Shooting Star",
            "Doji",
            "Bullish Engulfing",
            "Bearish Engulfing",
            "Morning Star",
            "Evening Star"
        ]
    )

    query = f"""
    Analyze candlestick pattern {pattern}

    Explain:
    Trend
    Reliability
    Entry
    Stoploss
    Target
    """

    if st.button("Analyze Pattern"):

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=query
        )

        st.write(response.text)

# ---------------------
# IPO
# ---------------------

elif menu == "IPO Analysis":

    st.header("IPO Analysis")

    ipo = st.text_input("IPO Name")

    if st.button("Analyze IPO"):

        prompt = f"""
        Analyze IPO {ipo}

        Cover:
        Company Overview
        Strengths
        Risks
        Listing Potential
        Long-Term View
        """

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        st.write(response.text)

# ---------------------
# SIP CALCULATOR
# ---------------------

elif menu == "SIP Calculator":

    st.header("SIP Calculator")

    amount = st.number_input(
        "Monthly SIP",
        value=5000
    )

    years = st.number_input(
        "Years",
        value=10
    )

    rate = st.number_input(
        "Expected Return (%)",
        value=12.0
    )

    if st.button("Calculate SIP"):

        monthly_rate = rate/12/100
        months = years*12

        corpus = amount * (
            ((1+monthly_rate)**months - 1)
            / monthly_rate
        ) * (1+monthly_rate)

        st.success(
            f"Estimated Corpus: ₹{corpus:,.2f}"
        )

# ---------------------
# EMI CALCULATOR
# ---------------------

elif menu == "EMI Calculator":

    st.header("EMI Calculator")

    principal = st.number_input(
        "Loan Amount",
        value=1000000
    )

    rate = st.number_input(
        "Interest Rate (%)",
        value=8.5
    )

    years = st.number_input(
        "Loan Tenure",
        value=20
    )

    if st.button("Calculate EMI"):

        r = rate/12/100
        n = years*12

        emi = principal * r * (1+r)**n / (
            (1+r)**n - 1
        )

        st.success(
            f"Monthly EMI: ₹{emi:,.2f}"
        )

# ---------------------
# AI CHAT
# ---------------------

elif menu == "AI Trading Chat":

    st.header("AI Trading Assistant")

    user_query = st.text_area(
        "Ask about Nifty, BankNifty, Options, IPO, SIP"
    )

    if st.button("Ask AI"):

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=user_query
        )

        st.write(response.text)