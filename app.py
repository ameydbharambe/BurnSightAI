import streamlit as st
import requests

st.markdown("""
<style>
    .block-container {
        padding-top:3.0rem;
    }

    h1 {
        margin-top: -2px;
        margin-bottom: 2px;
    }

    p {
        margin-top: 0px;
    }
</style>
""", unsafe_allow_html=True)

#TITLE USER INTERFACE
#TODO: REDUCE SPACING BETWEEN LOGO AND TITLE
col1, col2, col3 = st.columns([1.25,1, 1.25])
with col2:
    st.image("FrontEnd/BurnSightAI Logo.png", width=700)


st.markdown(
    "<h1 style='text-align:center; color:#D32F2F;'>BurnSight AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; font-size:18px;'>
    Please begin by uploading an image of the burn.
    </p>
    """,
    unsafe_allow_html=True
)

#TODO: ADD CHAT FEATURES