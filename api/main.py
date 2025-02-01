from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google import generativeai as genai
from modules.weather import get_weather
from datetime import datetime
from config_loader import config


GEMINI_API_KEY = config["llm"]["api_key"]
GEMINI_MODEL_NAME = config["llm"]["model"]
#HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")

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

@app.post("/greet/")
async def greet(request: Request):
    """Calls Gemini Advanced to generate a personalized greeting."""
    if not GEMINI_API_KEY:
        return {"error": "Missing Gemini API Key"}

    try:
        data = await request.json()
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            system_instruction="You are a funny and sarcastic AI. Greet the user according to time of day and present the agenda. The output is converted to speach so don't use headers or any other markdown. Be brief and consice",
        )
        name = data.get("name", "Stranger")
        agenda = data.get("agenda", "None")
        weather = data.get("weather", "Weather unknown")
        print(f"PROMPT --- Name: {name}. Current Time: {datetime.now()} Todays agenda: {agenda}. Current weather: {weather}")
        response = model.generate_content(f"Name: {name}. Current Time: {datetime.now()} Todays agenda: {agenda}. Current weather: {weather}")
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

@app.get("/weather")
def weather():
    return {"weather": get_weather()}

