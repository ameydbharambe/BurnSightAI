from google import genai
from dotenv import load_dotenv
import os
from model import BurnClassifier
import prompt

load_dotenv()

class BurnSightChat:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.history = []
        
    # ---------------------------------------------------------------------------
    #           Pipeline Interfaces: Image Diagnosis & Follow-up Chat
    # ---------------------------------------------------------------------------
    
    def diagnose(self, prediction, confidence):
        prompt_text = prompt.diagnosis_prompt(prediction, confidence)
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash")
        
        response = self.chat.send_message(prompt_text)
        
        return response.text
    
    def followUp(self, question):
        prompt_text = prompt.chat_prompt(question)
        if self.chat is None:
            self.chat = self.client.chats.create(
                model="gemini-2.5-flash")
        
        response = self.chat.send_message(question)

        return response.text
    





