from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from model import BurnClassifier
from chat import BurnSightChat
import io 
import os
import uuid
import shutil


app = FastAPI(title = "BurnSightAI",
              description = "AI powered burn injury diagnosis and treatment assistant",
              version = "0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

classifier = BurnClassifier()
chat = BurnSightChat()

@app.get("/home")
def home():
    return {"message": "BurnSightAI API is running"}

#The defined endpoint accepts an image file upload while model requires file path
@app.post("/diagnose")
async def diagnose(image: UploadFile = File(...)):

    # Create temporary file path
    file_name = f"temp_{uuid.uuid4()}.jpg"
    file_path = os.path.join("temporary", file_name)

    # Create a temporary folder and save the img to folder 
    os.makedirs("temporary", exist_ok=True)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
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
async def followup(question: str):
    response = chat.followUp(question)
    return {"response": response}