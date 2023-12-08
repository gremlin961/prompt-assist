# This web service uses FastAPI to accept requests to convert json files to a standard data structure
#
# The following modules are used in this service
# fastapi - Web service framework used to build the API
# uvicorn - ASGI web server implementation for Python
# json - Used to interact with json files and data passed to the web service
# typing - Primarliy using the Union function to handle optional json data passed to the API
# convert - Custom library used to submit form data to the PaLM text-bison model

from fastapi import FastAPI, File, UploadFile, Request, HTTPException, Form
import uvicorn
import shutil
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import json
#from pkg import convert
from fastapi.staticfiles import StaticFiles



app = FastAPI()

# Specify the location for the Jinja templates
templates = Jinja2Templates(directory="templates")

# Specify the location for static files
app.mount("/static", StaticFiles(directory="static"), name="static")



# Define the entry point for the service and render the UI using the "form.html" file
@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# Display the response from the user input form
@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, prompt: str = Form(...), context: str = Form(None, required=False)):
   if context is None:
      context = ''
   results = {"prompt": prompt, "context": context}
   
   return templates.TemplateResponse("results.html", {"request": request, "results": results})