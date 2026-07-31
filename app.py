"""
app.py is entirely written by Claude minus a few changes in the UI
Talks to the FastAPI backend defined in main.py (/diagnose, /followup).

Run the backend first:   uvicorn main:app --reload --port 8000
Then run this app:       streamlit run app.py
"""

import os
from datetime import datetime
import json

import requests
import streamlit as st

# --------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------
BACKEND_URL = os.environ.get("BURNSIGHT_BACKEND_URL", "http://localhost:8000")
LOGO_PATH = os.environ.get("BURNSIGHT_LOGO_PATH", "BurnSightAI_Logo.png")
HISTORY_FILE = "history.json"
MAX_HISTORY = 15
history = []

st.set_page_config(
    page_title="BurnSight AI",
    page_icon="FrontEnd/BurnSightAI Logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# THEME — first-aid red & white
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        :root {
            --burn-red: #D32F2F;
            --burn-red-dark: #A5241F;
            --burn-red-light: #FDEAEA;
            --white: #FFFFFF;
        }

        .block-container { padding-top: 2rem; max-width: 900px; }

        h1 { margin-top: -2px; margin-bottom: 2px; }
        p  { margin-top: 0px; }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: var(--burn-red);
            border-right: 2px solid var(--burn-red);
        }
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: var(--white);
        }

        /* Buttons */
        div.stButton > button, div.stDownloadButton > button {
            background-color: var(--burn-red-dark);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }
        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background-color: var(--burn-red-dark);
            color: white;
        }

        /* Chat input */
        .stChatInput { border-color: var(--burn-red) !important; }

        /* Chat bubbles */
        div[data-testid="stChatMessage"] {
            border-radius: 12px;
            padding: 4px 8px;
        }

        /* File uploader accent */
        section[data-testid="stFileUploaderDropzone"] {
            border: 2px dashed var(--burn-red);
            background-color: var(--burn-red);
        }

        .burnsight-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 999px;
            background-color: var(--burn-red);
            color: white;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .history-card {
            border: 1px solid var(--burn-red);
            border-radius: 8px;
            padding: 8px 10px;
            margin-bottom: 8px;
            background-color: white;
        }
        .history-card .ts { font-size: 11px; color: #888; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# HISTORY HELPERS
# --------------------------------------------------------------------------

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history():
    history = st.session_state.history = st.session_state.history[:MAX_HISTORY]
    with open(HISTORY_FILE, "w") as f:
        return json.dump(history, f, indent=4)

# --------------------------------------------------------------------------
# SESSION STATE
# --------------------------------------------------------------------------
def init_state():
    defaults = {
        "messages": [],        # current conversation: [{"role", "content"}]
        "diagnosed": False,    # has the current session gotten a diagnosis yet?
        "diagnosis_info": None,  # {"prediction", "confidence"}
        "history" : load_history(),
        "viewing_past_id": None,  # if set, we're viewing read-only history
        "uploaded_image_bytes": None,
        "uploaded_image_name": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    


init_state()


# --------------------------------------------------------------------------
# BACKEND CALLS
# --------------------------------------------------------------------------
def call_diagnose(image_bytes: bytes, filename: str):
    """POST the image to /diagnose. Returns (ok, data_or_error)."""
    try:
        files = {"image": (filename, image_bytes, "application/octet-stream")}
        resp = requests.post(f"{BACKEND_URL}/diagnose", files=files, timeout=60)
        resp.raise_for_status()
        return True, resp.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)


def call_followup(question: str):
    """POST a follow-up question to /followup. Returns (ok, data_or_error)."""
    try:
        resp = requests.post(
            f"{BACKEND_URL}/followup", params={"question": question}, timeout=60
        )
        resp.raise_for_status()
        return True, resp.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)


# --------------------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------------------

    

def archive_current_session():
    """Push the current conversation into history and reset for a new one."""
    if st.session_state.messages:
        st.session_state.history.insert(
            0,
            {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
                "prediction": (st.session_state.diagnosis_info or {}).get(
                    "prediction", "Unclassified"
                ),
                "confidence": (st.session_state.diagnosis_info or {}).get(
                    "confidence"
                ),
                "messages": st.session_state.messages.copy(),
            },
        )
        st.session_state.history = st.session_state.history[:MAX_HISTORY]
        save_history()

    st.session_state.messages = []
    st.session_state.diagnosed = False
    st.session_state.diagnosis_info = None
    st.session_state.uploaded_image_bytes = None
    st.session_state.uploaded_image_name = None
    st.session_state.viewing_past_id = None


def get_viewed_session():
    if st.session_state.viewing_past_id is None:
        return None
    for session in st.session_state.history:
        if session["id"] == st.session_state.viewing_past_id:
            return session
    return None


# --------------------------------------------------------------------------
# SIDEBAR — past history
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## BurnSight AI")
    st.sidebar.html("<span class='burnsight-badge' style='margin-top: -50px; display: inline-block;'>PAST INTERACTIONS</span>")
    st.markdown("---")

    if st.button("➕ New Diagnosis", use_container_width=True):
        archive_current_session()
        st.rerun()

    st.markdown("")

    if not st.session_state.history:
        st.caption("No past sessions yet. Upload a burn image to get started.")
    else:
        for session in st.session_state.history:
            with st.container():
                st.markdown(
                    f"""
                    <div class="history-card">
                        <b>{session['prediction']}</b><br>
                        <span class="ts">{session['timestamp']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("View", key=f"view_{session['id']}", use_container_width=True):
                    st.session_state.viewing_past_id = session["id"]
                    st.rerun()

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=180)
    else:
        st.markdown(
            "<div style='text-align:center; font-size:60px;'></div>",
            unsafe_allow_html=True,
        )

st.markdown(
    "<h1 style='text-align:center; color:#D32F2F;'>BurnSight AI</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style='text-align:center; font-size:16px; color:#555;'>
    AI-powered burn classification and first-aid guidance
    </p>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

# --------------------------------------------------------------------------
# MAIN AREA — either read-only history view, or the live chat
# --------------------------------------------------------------------------
viewed_session = get_viewed_session()

if viewed_session is not None:
    st.info(f"Viewing past session from {viewed_session['timestamp']} (read-only)")
    if viewed_session.get("thumbnail"):
        st.image(viewed_session["thumbnail"], width=220)

    for msg in viewed_session["messages"]:
        with st.chat_message(msg["role"], avatar="FrontEnd/BurnSightAI Logo.png" if msg["role"] == "assistant" else "🧑"):
            st.markdown(msg["content"])

    if st.button("⬅ Back to current session"):
        st.session_state.viewing_past_id = None
        st.rerun()

else:
    # Render existing conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="FrontEnd/BurnSightAI Logo.png" if msg["role"] == "assistant" else "🧑"):
            if msg.get("image"):
                st.image(msg["image"], width=220)
            st.markdown(msg["content"])

    # Step 1: no diagnosis yet — show uploader
    if not st.session_state.diagnosed:
        st.markdown(
            "<p style='text-align:center; font-size:18px;'>"
            "Please begin by uploading an image of the burn.</p>",
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload burn image", type=["png", "jpg", "jpeg"], label_visibility="collapsed"
        )

        if uploaded_file is not None:
            image_bytes = uploaded_file.getvalue()

            st.session_state.uploaded_image_bytes = image_bytes
            st.session_state.uploaded_image_name = uploaded_file.name

            st.session_state.messages.append(
                {"role": "user", "content": "Uploaded a burn image for diagnosis."}
            )

            with st.chat_message("user", avatar="🧑"):
                st.image(image_bytes, width=220)
                st.markdown("Uploaded a burn image for diagnosis.")

            with st.chat_message("assistant", avatar="FrontEnd/BurnSightAI Logo.png"):
                with st.spinner("Analyzing image..."):
                    ok, data = call_diagnose(image_bytes, uploaded_file.name)

                if ok:
                    prediction = data.get("prediction", "Unknown")
                    confidence = data.get("confidence", 0)
                    diagnosis_text = data.get("diagnosis", "")

                    try:
                        confidence_pct = f"{float(confidence) * 100:.1f}%"
                    except (TypeError, ValueError):
                        confidence_pct = str(confidence)

                    reply = (
                        f"**Classification:** {prediction}  \n"
                        f"**Confidence:** {confidence_pct}\n\n"
                        f"{diagnosis_text}"
                    )
                    st.markdown(reply)

                    st.session_state.diagnosis_info = {
                        "prediction": prediction,
                        "confidence": confidence,
                    }
                    st.session_state.diagnosed = True
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    error_reply = (
                        "⚠️ I couldn't reach the diagnosis service. "
                        f"Please make sure the backend is running.\n\n`{data}`"
                    )
                    st.markdown(error_reply)
                    st.session_state.messages.append({"role": "assistant", "content": error_reply})

            st.rerun()

    # Step 2: diagnosed — allow follow-up chat
    else:
        question = st.chat_input("Ask a follow-up question about your diagnosis...")
        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user", avatar="🧑"):
                st.markdown(question)

            with st.chat_message("assistant", avatar="FrontEnd/BurnSightAI Logo.png"):
                with st.spinner("Thinking..."):
                    ok, data = call_followup(question)

                if ok:
                    reply = data.get("response", "")
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    error_reply = f"⚠️ I couldn't reach the chat service.\n\n`{data}`"
                    st.markdown(error_reply)
                    st.session_state.messages.append({"role": "assistant", "content": error_reply})

        st.caption(
            "Note: BurnSight AI provides general guidance and is not a substitute "
            "for professional medical care. Seek emergency help for severe burns."
        )