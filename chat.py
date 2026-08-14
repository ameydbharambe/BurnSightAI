from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from model import BurnClassifier
import prompt
import streamlit as st

load_dotenv()

class BurnSightChat:
    def __init__(self):
        self.client = genai.Client(st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY"))
        self.config = types.GenerateContentConfig(temperature=0.1)
        self.chat = None
    # ---------------------------------------------------------------------------
    #           Pipeline Interfaces: Image Diagnosis & Follow-up Chat
    # ---------------------------------------------------------------------------
    
    def diagnose(self, prediction, confidence):
        prompt_text = prompt.diagnosis_prompt(prediction, confidence)
        self.chat = self.client.chats.create( model="gemini-2.5-flash", config=self.config)
        response = self.chat.send_message(prompt_text)      
        return response.text
    
    def used_google_search(self, response):
        candidate = response.candidates[0]

        metadata = candidate.grounding_metadata
        return (
            metadata is not None and
            metadata.web_search_queries is not None
        )
    
    def followUp(self, question):
        prompt_text = prompt.chat_prompt(question)
        if self.chat is None:
            return "Chat cannot be initiated till diagnosis is made. Please upload an image and get a diagnosis first."
        response = self.chat.send_message(question)

        return response.text

    





