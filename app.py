from openai import OpenAI
import os

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseModel):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

class Config:
    env_file = '.env'

settings = Settings()
client = OpenAI(
  api_key = settings.OPENAI_API_KEY,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def return_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/", response_class=HTMLResponse)
def index(request: Request, animal: str= Form(...)):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content" : generate_prompt(animal)}
            ],
        temperature = 0.6,
    )
    result = response.choices[0].message.content
    return templates.TemplateResponse(request=request, name="index.html", context={"result": result})


def generate_prompt(animal):
    answer = f"""Suggest three names for an animal that is a superhero.
    Animal: Cat
    Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
    Animal: Dog
    Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
    Animal: {animal.capitalize()}
    Names:"""
    return answer

