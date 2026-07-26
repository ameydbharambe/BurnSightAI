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
        self.history.append({
            "role": "user",
            "text": prompt_text
        })
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt_text],
        )
        self.history.append({
        "role": "assistant",
        "text": response.text
    })
        return response.text
    
    def chat(self, question):
        prompt_text = prompt.chat_prompt(question)
        self.history.append({
            "role": "user",
            "text": prompt_text
        })
        history_text = "\n".join(
        f"{msg['role'].capitalize()}: {msg['text']}"
        for msg in self.history
    )
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt_text],
        )
        self.history.append({
            "role": "assistant",
            "text": response.text
        })
        return response.text
    
#Test the chat interface
model = BurnClassifier()
chatbot = BurnSightChat()
prediction, confidence = model.predict("TestingData/First Degree Burn.jpg")
diagnosis = chatbot.diagnose(prediction, confidence)
print(diagnosis)
follow_up_question = input()
follow_up_response = chatbot.chat(follow_up_question)
print(follow_up_response)





