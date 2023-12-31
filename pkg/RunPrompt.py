import vertexai
from vertexai.language_models import TextGenerationModel
from pkg import SecurePrompt 
import json
# Add support for Gemini models
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Image, Content, Part, Tool, FunctionDeclaration, GenerationConfig, HarmCategory, HarmBlockThreshold



def GetData(SECRET, MODEL, PROMPT, CONTEXT=''):

    # Define the needed parameters provided in the parameters.json file. 
    # --YOU WILL NEED TO UPDATE THE parameters.json TEMPLATE FILE WITH YOUR OWN PROJECT ID AND SECRET ID NAMES--
    #project_id = PARAMETERS['project_id']
    #location = PARAMETERS['location']
    #model = PARAMETERS['model']
    #secret_id = PARAMETERS['secret_id']
    #secret_ver = PARAMETERS['secret_ver']
    project_id = 'rkiles-demo-host-vpc'
    location = 'us-central1'
    model_type = MODEL
    secret_id = SECRET
    secret_ver = 'latest'
    prompt = PROMPT
    context = CONTEXT
    
    # Pull the prompt data and parameters from GCP Secret Manager. This data is stored in the same json format as the my-prompts library in the Vertex Language console.
    data = SecurePrompt.GetValue(project_id, secret_id, secret_ver)
    values = json.loads(data)
    
    # Define the parameters from the returned data
    c_count = values['parameters']['candidateCount']
    max_output = values['parameters']['tokenLimits']
    temp = values['parameters']['temperature']
    top_p = values['parameters']['topP']
    top_k = values['parameters']['topK']
    #context = values['context']
    #prompt = values['testData'][0]['inputs'][0]


    # Initialize the vertex AI text-bison model with values set from the previous step
    # The context and prompt are provided in the parameters file. The template and data are provided in the template and data files.
    vertexai.init(project=project_id, location=location)
    parameters = {
        "candidate_count": c_count,
        "max_output_tokens": max_output,
        "temperature": temp,
        "top_p": top_p,
        "top_k": top_k
    }
    if model_type == 'gemini-pro':
        model = GenerativeModel("gemini-pro")
        response = model.generate_content(
            '"'+context+'"'+'"'+prompt+'"',
            generation_config=GenerationConfig(
                temperature=temp,
                top_p=top_p,
                top_k=top_k,
                candidate_count=c_count,
                max_output_tokens=max_output,
                stop_sequences=["STOP!"],
            )
        )
    else:
        model = TextGenerationModel.from_pretrained(model_type)
        response = model.predict(
            """"""+context+""""""
            """ input: """+prompt+
            """ output:
            """,
                **parameters
        )
    # Return the response from the model to main.py
    return response.text

