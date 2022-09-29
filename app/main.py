from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

	clean_text  = re.sub(r"[^a-zA-Z0-9_]", " ", text)

    response = requests.put('https://API_ADDRESS/predictions/MODEL_NAME', data=clean_text)

    # post-process of response

    topic  = result.json()["label"]

	return templates.TemplateResponse("output.html", {"request": request, 
                                                      "text": text,
                                                      "topic": topic})
                                                    
if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8080)