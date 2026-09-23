import streamlit as st
from google import genai
import yfinance as yf

# =========================
# API KEY
# =========================

API_KEY = "PASTE API KEY"

client = genai.Client(api_key=API_KEY)

# =========================
# PAGE
# =========================

st.set_page_config(
    page_title="Indian Stock Market AI",
    layout="wide"
)

st.title("📈 Indian Stock Market AI Assistant")

# =========================
# SIDEBAR
# =========================

option = st.sidebar.selectbox(
    "Select Feature",
    [
        "Market Chat",
        "Nifty 50",
        "Bank Nifty",
        "IPO Analysis",
        "SIP Calculator",
        "EMI Calculator"
    ]
)

# =========================
# NIFTY
# =========================

if option == "Nifty 50":

    st.header("Nifty 50")

    data = yf.download("^NSEI", period="1mo")

    st.line_chart(data["Close"])

    if st.button("Analyze Nifty"):

        prompt = """
        Analyze Nifty 50.

        Give:
        1. Trend
        2. Support
        3. Resistance
        4. Intraday View
        5. Risk Management
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.write(response.text)

# =========================
# BANK NIFTY
# =========================

elif option == "Bank Nifty":

    st.header("Bank Nifty")

    data = yf.download("^NSEBANK", period="1mo")

    st.line_chart(data["Close"])

    if st.button("Analyze Bank Nifty"):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="""
            Analyze Bank Nifty.
            Give trading opportunities.
            Explain trend and risk.
            """
        )

        st.write(response.text)

# =========================
# IPO
# =========================

elif option == "IPO Analysis":

    ipo = st.text_input("IPO Name")

    if st.button("Analyze IPO"):

        prompt = f"""
        Analyze IPO {ipo}

        Include:

        Company Overview
        Strengths
        Risks
        Listing Potential
        Long-Term View
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.write(response.text)

# =========================
# SIP
# =========================

elif option == "SIP Calculator":

    amount = st.number_input("Monthly SIP", 500, 1000000, 5000)

    years = st.number_input("Years", 1, 40, 10)

    rate = st.number_input("Expected Return %", 1.0, 30.0, 12.0)

    if st.button("Calculate SIP"):

        monthly_rate = rate / 12 / 100
        months = years * 12

        corpus = amount * (
            ((1 + monthly_rate) ** months - 1)
            / monthly_rate
        ) * (1 + monthly_rate)

        st.success(f"Estimated Value = ₹{corpus:,.2f}")

# =========================
# EMI
# =========================

elif option == "EMI Calculator":

    principal = st.number_input(
        "Loan Amount",
        value=1000000
    )

    rate = st.number_input(
        "Interest Rate %",
        value=9.0
    )

    years = st.number_input(
        "Years",
        value=20
    )

    if st.button("Calculate EMI"):

        r = rate / 12 / 100
        n = years * 12

        emi = principal * r * (1+r)**n / (
            (1+r)**n - 1
        )

        st.success(
            f"Monthly EMI = ₹{emi:,.2f}"
        )

# =========================
# CHATBOT
# =========================

else:

    question = st.text_area(
        "Ask about Stocks, IPO, SIP, Trading, Options"
    )

    if st.button("Ask AI"):

        system_prompt = """
        You are an Indian Stock Market Expert.

        Expertise:
        - Nifty 50
        - Bank Nifty
        - FinNifty
        - Sensex
        - IPO
        - SIP
        - Mutual Funds
        - Options Trading
        - Technical Analysis
        - Candlestick Patterns

        Never promise profits.
        Always explain risks.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\n\n{question}"
        )

        st.write(response.text)
