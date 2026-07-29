from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from model import BurnClassifier
from chat import BurnSightChat
import os


app = FastAPI(title = "BurnSightAI",
              description = "AI powered burn injury diagnosis and treatment assistant",
              version = "0.1.0")

origins = ["http://localhost:8501", "http://192.168.254.21:8501"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

classifier = BurnClassifier()
chat = BurnSightChat()

@app.get("/home")
def home():
    return {"message": "BurnSightAI API is running"}

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