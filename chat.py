from google import genai
from dotenv import load_dotenv
import os
from model import BurnClassifier

load_dotenv()

class BurnSightChat:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
    # ---------------------------------------------------------------------------
    #           Pipeline Interfaces: Image Diagnosis & Follow-up Chat
    # ---------------------------------------------------------------------------
    
    def diagnose(self, prediction, confidence):
        prompt = """You are a FIRST AID medical assistant specializing in the treatment of burn injuries (First Degree, Second Degree, Third Degree). 
        A user has uploaded an image of a burn injury, and the model has classified it 
        as"""+ prediction + """ with a confidence of""" + str(confidence) + """. If the confidence is below 0.5, please advise the user to seek professional medical attention immediately.
        Please provide a short yet detailed and informative response (200 words maximum) based on the classification and confidence level
        for treatment. Only suggest immediate diagnosis and treatment options that are easily accessible to the user at any given location and be done before calling medical assistance. 
        Avoid suggesting any treatment that requires a hospital visit or prescription medication."""
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
        )
        return response.text
    
    def chat(self, question):
        prompt = """You are a FIRST AID medical assistant specializing in treating burn injuries (First Degree, Second Degree, Third Degree)
        The user has already uploaded an image of a burn injury and received a diagnosis. The user now has the following follow up question related to burn injuries: """ + question + """ Please provide a short yet detailed and informative response (200 words maximum) based on the user's question. 
        DO NOT answer any questions that are not related to burn injuries. If the question is not related to burn injuries, please politely inform the user that you can only answer questions related to burn injuries."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
        )
        return response.text
    

