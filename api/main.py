import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/status")
def status():
    return {"status": "OK", "message": "The API is online"}

@app.get("/greet/{name}")
def greet(name: str):
    """Calls Gemini Advanced to generate a personalized greeting."""
    if not GEMINI_API_KEY:
        return {"error": "Missing Gemini API Key"}

    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(f"Greet {name}. Be funny and sarcastic")
        return {"message": response.text}
    except Exception as e:
        return {"error": str(e)}

# Store the last recognized face data
recognized_faces = {"name": "None", "greeting": "Waiting for a face..."}

@app.get("/recognized_faces")
def get_recognized_faces():
    """Returns the last recognized face and greeting."""
    return JSONResponse(content={"name": recognized_faces["name"], "greeting": recognized_faces["greeting"]})

@app.post("/recognized_faces")
async def update_recognized_faces(request: Request):
    """Updates the recognized face data from the face detection script."""
    global recognized_faces
    data = await request.json()
    recognized_faces["name"] = data.get("name", "Unknown")
    recognized_faces["greeting"] = data.get("greeting", "No greeting available.")
    return {"status": "updated"}