from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from model import BurnClassifier
import prompt

load_dotenv()

class BurnSightChat:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.config = types.GenerateContentConfig(temperature=0.1, tools=[types.Tool(google_search=types.GoogleSearch())])
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
        if self.used_google_search(response):
            return "I used Google Search to find the answer. Here is the information I found: \n " + response.text 

        return response.text

    





