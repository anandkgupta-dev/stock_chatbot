"""
app.py - Streamlit Web Application for Stock Market Domain-Specific Chatbot
"""

import os
import streamlit as st
from dotenv import load_dotenv
from stock_agent import StockChatbot

# Page configuration
st.set_page_config(
    page_title="StockPulse AI | Stock Market Chatbot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load existing environment variables
load_dotenv()

# Custom CSS for modern Bloomberg / TradingView inspired aesthetics
st.markdown("""
<style>
    /* Dark financial theme refinements */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    
    /* Header container */
    .header-box {
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
        border: 1px solid rgba(56, 139, 253, 0.25);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    
    .badge-domain {
        display: inline-block;
        background: rgba(35, 134, 54, 0.2);
        color: #3fb950;
        border: 1px solid rgba(63, 185, 80, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    .badge-warning {
        display: inline-block;
        background: rgba(218, 54, 51, 0.15);
        color: #f85149;
        border: 1px solid rgba(248, 81, 73, 0.3);
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.78rem;
        font-weight: 500;
        margin-left: 8px;
    }

    .main-title {
        font-size: 1.85rem;
        font-weight: 700;
        color: #f0f6fc;
        margin: 0;
        padding-top: 4px;
    }
    
    .sub-title {
        color: #8b949e;
        font-size: 0.95rem;
        margin-top: 6px;
        margin-bottom: 0px;
    }

    /* Sidebar cards */
    .sidebar-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 16px;
    }

    /* Sample chips */
    .chip-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #8b949e;
        margin-bottom: 8px;
    }

    /* Disclaimer box */
    .disclaimer-card {
        background: rgba(240, 136, 62, 0.1);
        border: 1px solid rgba(240, 136, 62, 0.3);
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 0.78rem;
        color: #d29922;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    env_key = os.getenv("OPENAI_API_KEY", "").strip()
    
    # API Key Input
    user_api_key = st.text_input(
        "OpenAI API Key",
        value=st.session_state.get("api_key", env_key),
        type="password",
        placeholder="sk-proj-...",
        help="Enter your OpenAI API key here or define OPENAI_API_KEY in the .env file."
    )
    
    # Save key in session state
    if user_api_key:
        st.session_state["api_key"] = user_api_key.strip()
        st.caption("✅ API Key configured")
    else:
        st.caption("⚠️ API Key required to run queries")

    st.markdown("---")
    
    # Model Selection
    selected_model = st.selectbox(
        "LLM Model",
        options=["gpt-4o-mini", "gpt-4o"],
        index=0,
        help="gpt-4o-mini is optimized for fast, cost-effective inference. gpt-4o offers deep analytical reasoning."
    )
    
    # Temperature Slider
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="Lower values (0.1 - 0.3) provide precise, fact-based answers on financial metrics."
    )

    st.markdown("---")

    # Domain Guardrail Rules Card
    st.markdown("""
    <div class="sidebar-card">
        <strong style="color: #58a6ff;">🛡️ Domain Boundaries</strong><br>
        <span style="font-size: 0.82rem; color: #8b949e;">This AI is strictly restricted to:</span>
        <ul style="font-size: 0.8rem; color: #c9d1d9; margin-top: 6px; padding-left: 18px;">
            <li>Stocks, Shares & Equities</li>
            <li>Market Indices (S&P 500, NASDAQ, etc.)</li>
            <li>Fundamental & Technical Analysis</li>
            <li>Valuation Ratios (P/E, EPS, etc.)</li>
            <li>Trading Mechanisms & IPOs</li>
        </ul>
        <span style="font-size: 0.78rem; color: #f85149;">
            ❌ Non-stock topics (sports, cooking, weather, general code) will be rejected.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Disclaimer
    st.markdown("""
    <div class="disclaimer-card">
        ⚠️ <strong>Financial Disclaimer:</strong> For educational purposes only. Does not constitute certified financial or investment advice.
    </div>
    """, unsafe_allow_html=True)


# ----------------- MAIN INTERFACE -----------------

# Header Banner
st.markdown("""
<div class="header-box">
    <div>
        <span class="badge-domain">● DEDICATED DOMAIN</span>
        <span class="badge-warning">STOCKS ONLY</span>
    </div>
    <h1 class="main-title">📈 StockPulse AI</h1>
    <p class="sub-title">Your focused assistant for Stock Markets, Equities, Valuation Ratios, and Trading Concepts.</p>
</div>
""", unsafe_allow_html=True)

# Initialize Chatbot
active_key = st.session_state.get("api_key", env_key)
chatbot = StockChatbot(api_key=active_key, model=selected_model, temperature=temperature)

# Initialize Session Messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Welcome to **StockPulse AI**! I am specialized exclusively in the **Stock Market and Equities** domain.\n\nYou can ask me about stock valuation, financial metrics (like P/E or EPS), market indices, trading mechanics, or company fundamentals. Non-stock queries will be politely refused to keep the focus strictly on financial markets."
        }
    ]

# Display Existing Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick Prompt Suggestions (visible when chat history is brief)
if len(st.session_state.messages) <= 2:
    st.markdown("<div class='chip-label'>💡 Try these sample prompts:</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    prompt_to_send = None
    with c1:
        if st.button("📈 What is P/E Ratio?", use_container_width=True):
            prompt_to_send = "What is the P/E (Price-to-Earnings) ratio and how do investors use it to value a stock?"
    with c2:
        if st.button("⚖️ Market vs Limit Order", use_container_width=True):
            prompt_to_send = "Explain the difference between a Market Order and a Limit Order in stock trading."
    with c3:
        if st.button("📊 Bull vs Bear Market", use_container_width=True):
            prompt_to_send = "What defines a Bull Market vs a Bear Market, and how do market cycles typically behave?"
    with c4:
        if st.button("🍕 Test: Pizza Recipe", use_container_width=True, help="Test out-of-domain rejection guardrail"):
            prompt_to_send = "Can you give me a recipe for Italian pizza?"

    if prompt_to_send:
        st.session_state.messages.append({"role": "user", "content": prompt_to_send})
        st.rerun()

# User Input Box
user_prompt = st.chat_input("Ask a question about stocks, market analysis, or trading...")

if user_prompt:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        if not chatbot.is_configured:
            warning_msg = (
                "⚠️ **API Key Required**:\n\n"
                "Please enter your **OpenAI API Key** in the sidebar on the left (or add `OPENAI_API_KEY=your_key` in the `.env` file) to run the chatbot."
            )
            st.warning(warning_msg)
            st.session_state.messages.append({"role": "assistant", "content": warning_msg})
        else:
            response_stream = chatbot.get_response_stream(
                messages=st.session_state.messages,
                model=selected_model,
                temperature=temperature
            )
            full_response = st.write_stream(response_stream)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
