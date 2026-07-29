import streamlit as st
import requests

#DEFAULT FONT = ROBOTO TODO: POTENTIAL CHANGE TO OPEN SANS

st.markdown("""
<style>

/* Change font for entire application */
html, body, [class*="css"], [data-testid="stAppViewContainer"] * {
    font-family: "Comic Sans MS" !important;
}

</style>
""", unsafe_allow_html=True)

#TITLE & SUBHEADER
st.markdown( """ <h1 style="text-align:center; color:#D32F2F;">BurnSight AI</h1>""",unsafe_allow_html=True)
st.write("Welcome to BurnSightAI! To begin your diagnosis please upload an image of the burn injury. Once the diagnosis is made, you can ask follow-up questions related to immediate treatment for the injury.")
