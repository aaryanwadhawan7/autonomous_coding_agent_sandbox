import streamlit as st
import requests

st.set_page_config(
    page_title="Coding Agent",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Hide Streamlit chrome */
header[data-testid="stHeader"] { display: none; }
#MainMenu { display: none; }
footer { display: none; }
.stDeployButton { display: none; }

/* Root */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 680px;
}

/* Theme toggle */
.theme-row {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 2rem;
}

/* Typography */
.page-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 8px;
}

.page-title {
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
    color: inherit;
}

.page-desc {
    font-size: 14px;
    color: #888;
    margin-bottom: 32px;
    font-weight: 400;
}

/* Constraint pill row */
.pill-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 28px;
}

.pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 4px;
    border: 1px solid #e5e5e5;
    color: #555;
    background: #fafafa;
}

.pill.no {
    border-color: #ffd5d5;
    color: #c00;
    background: #fff5f5;
}

/* Input label */
.stTextArea label {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #666 !important;
    letter-spacing: 0.5px !important;
}

/* Button */
.stButton > button {
    background: #111 !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 24px !important;
    letter-spacing: 0.2px !important;
    transition: opacity 0.15s !important;
}

.stButton > button:hover {
    opacity: 0.75 !important;
}

/* Divider */
.divider {
    height: 1px;
    background: #f0f0f0;
    margin: 28px 0;
}

/* Output block */
.output-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.output-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #999;
}

.iter-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #999;
    background: #f5f5f5;
    border: 1px solid #eee;
    padding: 3px 10px;
    border-radius: 4px;
}

.status-ok {
    font-size: 12px;
    font-weight: 500;
    color: #2d7a2d;
    margin-bottom: 16px;
}

.status-fail {
    font-size: 12px;
    font-weight: 500;
    color: #c00;
    margin-bottom: 16px;
}

/* Dark mode overrides */
[data-theme="dark"] .pill {
    border-color: #2a2a2a;
    color: #888;
    background: #1a1a1a;
}

[data-theme="dark"] .pill.no {
    border-color: #3a1a1a;
    color: #ff6b6b;
    background: #1a0a0a;
}

[data-theme="dark"] .divider {
    background: #1e1e1e;
}

[data-theme="dark"] .iter-tag {
    background: #1a1a1a;
    border-color: #2a2a2a;
    color: #666;
}

[data-theme="dark"] .stButton > button {
    background: #f0f0f0 !important;
    color: #111 !important;
}
</style>
""", unsafe_allow_html=True)

# Session state
if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None
if "dark" not in st.session_state:
    st.session_state.dark = False

# Theme toggle
col1, col2 = st.columns([6, 1])
with col2:
    dark = st.toggle("Dark", value=st.session_state.dark)
    st.session_state.dark = dark

if dark:
    st.markdown("""
    <style>
    html, body, [class*="css"], .main, .block-container {
        background-color: #0d0d0d !important;
        color: #e0e0e0 !important;
    }
    textarea, .stTextArea textarea {
        background-color: #111 !important;
        color: #e0e0e0 !important;
        border-color: #2a2a2a !important;
    }
    .page-desc, .output-label, .page-label { color: #555 !important; }
    .page-title { color: #f0f0f0 !important; }
    .status-ok { color: #4caf50 !important; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<div class="page-label">AI Engineering</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Coding Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="page-desc">Writes, executes, and debugs Python code autonomously using function calling and a Docker sandbox.</div>', unsafe_allow_html=True)

# Constraints
st.markdown("""
<div class="pill-row">
    <span class="pill">✓ algorithms</span>
    <span class="pill">✓ data structures</span>
    <span class="pill">✓ math</span>
    <span class="pill">✓ standard library</span>
    <span class="pill no">✗ numpy</span>
    <span class="pill no">✗ pip installs</span>
</div>
""", unsafe_allow_html=True)

# Input
user_input = st.text_area(
    "Request",
    placeholder="e.g. write a binary search function and test edge cases",
    height=100,
    label_visibility="collapsed"
)

if st.button("Run agent"):
    st.session_state.result = None
    st.session_state.error = None
    if user_input.strip():
        with st.spinner("Running..."):
            try:
                response = requests.post(
                    "http://localhost:8000/run-agent",
                    json={"code": user_input},
                    timeout=300
                )
                st.session_state.result = response.json()
            except requests.exceptions.ConnectionError:
                # Windows drops connection — result already came, retry GET
                try:
                    fallback = requests.get(
                        "http://localhost:8000/",
                        timeout=5
                    )
                    if fallback.status_code == 200:
                        st.session_state.error = "Windows connection drop — refresh and try again"
                except:
                    pass
            except Exception as e:
                st.session_state.error = str(e)
    else:
        st.warning("Enter a request first.")
        
# Output
if st.session_state.result:
    result = st.session_state.result
    success = "Maximum iteration" not in result.get("result", "")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="output-meta">
        <span class="output-label">Output</span>
        <span class="iter-tag">{result['iterations']} iteration{"s" if result['iterations'] != 1 else ""}</span>
    </div>
    <div class="{'status-ok' if success else 'status-fail'}">
        {'Completed successfully' if success else 'Max iterations reached'}
    </div>
    """, unsafe_allow_html=True)

    st.code(result["result"], language="python")

if st.session_state.error:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.error(f"Connection error — make sure the backend is running on port 8000.")