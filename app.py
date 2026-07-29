import streamlit as st
import requests

#DEFAULT FONT = ROBOTO TODO: POTENTIAL CHANGE TO OPEN SANS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Roboto', sans-serif;
}
</style>
""", unsafe_allow_html=True)

#TITLE & SUBHEADER
st.markdown( """ <h1 style="text-align:center; color:#D32F2F;">BurnSight AI</h1>""",unsafe_allow_html=True)
st.write("Welcome to BurnSightAI! To begin your diagnosis please upload an image of the burn injury. Once the diagnosis is made, you can ask follow-up questions related to immediate treatment for the injury.")
