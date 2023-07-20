from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from helpers import install_nltk
from helpers.preprocess import (remove_accents, remove_equations, remove_punctuation,
								remove_website_links, stem_text, lemmatize_text,
								to_lowercase, tokenize_and_remove_stopwords, number_to_text)
import uvicorn
import re
import requests


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
@app.get('/input',response_class=HTMLResponse)
def input_page(request: Request):
	return templates.TemplateResponse("input.html", {"request": request})


@app.get("/output", response_class=HTMLResponse)
def output_page(request: Request, text : str):
	
	text = to_lowercase(text)
	text = remove_website_links(text)
	text = remove_equations(text)
	text = remove_punctuation(text)
	text = remove_accents(text)
	text = tokenize_and_remove_stopwords(text)
	text = lemmatize_text(text)
	text = number_to_text(text)
	text = stem_text(text)
	result = requests.post(url   = "http://0.0.0.0:8000/predict",
							data  = text,
							headers={'Content-Type': 'text/plain'})

	topic  = result.json()["label"]

	return templates.TemplateResponse("output.html", {"request": request, 
													  "text": text,
													  "topic": topic})

@app.get('/about',response_class=HTMLResponse)
def about_page(request: Request):

	return templates.TemplateResponse("about.html", {"request": request})


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8080)

# uvicorn --host 0.0.0.0 --port 8080 main:app --reload