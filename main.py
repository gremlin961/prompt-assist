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
from pkg import EnrichPrompt, ComparePrompt, RunPrompt
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
      context = ' '

   #compare_data = prompt.GetData('prompt-enrichment', prompt)
   enrich_data = EnrichPrompt.GetData('prompt-enrichment', prompt)

   compare_data = ComparePrompt.GetData('prompt-compare', prompt, enrich_data)

   results = {"prompt": prompt, "context": context}

   return templates.TemplateResponse("results.html", {"request": request, "results": results, "enrich_data": enrich_data, "compare_data": compare_data})


# Compare the output of both prompts
@app.post("/output", response_class=HTMLResponse)
async def form_post(request: Request, context: str = Form(...), prompt: str = Form(...), enrich_data: str = Form(...), model_type: str = Form(...)):
   if context is None:
      context = ' '

   response1 = RunPrompt.GetData('empty-prompt', model_type, prompt, context)
   response2 = RunPrompt.GetData('empty-prompt', model_type, enrich_data, context)

   #compare_response = ComparePrompt.GetData('prompt-compare', response1, response2)

   results = {"context": context, "prompt1": prompt, "prompt2": enrich_data, 'response1': response1, 'response2': response2, "model_type": model_type}
   #results = {"context": context, "prompt1": prompt, "prompt2": enrich_data, "model_type": model_type}


   #return templates.TemplateResponse("compare.html", {"request": request, "results": results, "compare_response": compare_response})   
   return templates.TemplateResponse("compare.html", {"request": request, "results": results})  

