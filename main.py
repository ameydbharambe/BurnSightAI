from fastapi import FastAPI, UploadFile, File
from PIL import Image
from model import BurnClassifier
from chat import BurnSightChat
import os


app = FastAPI(title = "BurnSightAI",
              description = "AI powered burn injury diagnosis and treatment assistant",
              version = "0.1.0")

classifier = BurnClassifier()
chat = BurnSightChat()

@app.get("/home")
def home():
    return {"message": "BurnSightAI API is running"}


import os
from fastapi import FastAPI
from google import genai

app = FastAPI()

@app.get("/test-gemini")
def test_gemini():
    key = os.getenv("GEMINI_API_KEY")

    print("Key exists:", key is not None)
    print("Key prefix:", key[:4] if key else "NONE")

    client = genai.Client(api_key=key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello!"
    )

    print("Gemini response:", response.text)

    return {"response": response.text}

@app.post("/diagnose")
async def diagnose(image: UploadFile = File(...)):
    
    #file_names returns just a string of name so need to create file with those contents
    file_path = image.filename 
    contents = await image.read()
    with open(file_path, "wb") as f:
        f.write(contents) 

    try:      
        prediction, confidence = classifier.predict(file_path)
        diagnosis = chat.diagnose(prediction, confidence)
        return {
            "prediction": prediction,
            "confidence": confidence,
            "diagnosis": diagnosis
        }
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/followup")
def followup(question: str):
    response = chat.followUp(question)
    return {"response": response}