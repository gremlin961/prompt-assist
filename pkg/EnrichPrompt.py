import vertexai
from vertexai.language_models import TextGenerationModel
from pkg import SecurePrompt 
import json



def GetData(SECRET, SOURCE_PROMPT, SOURCE_CONTEXT=''):

    # Define the needed parameters provided in the parameters.json file. 
    # --YOU WILL NEED TO UPDATE THE parameters.json TEMPLATE FILE WITH YOUR OWN PROJECT ID AND SECRET ID NAMES--
    #project_id = PARAMETERS['project_id']
    #location = PARAMETERS['location']
    #model = PARAMETERS['model']
    #secret_id = PARAMETERS['secret_id']
    #secret_ver = PARAMETERS['secret_ver']
    project_id = 'rkiles-demo-host-vpc'
    location = 'us-central1'
    model = 'text-bison'
    secret_id = SECRET
    secret_ver = 'latest'
    source_prompt = SOURCE_PROMPT
    source_context = SOURCE_CONTEXT
    
    # Pull the prompt data and parameters from GCP Secret Manager. This data is stored in the same json format as the my-prompts library in the Vertex Language console.
    data = SecurePrompt.GetValue(project_id, secret_id, secret_ver)
    values = json.loads(data)
    
    # Define the parameters from the returned data
    c_count = values['parameters']['candidateCount']
    max_output = values['parameters']['tokenLimits']
    temp = values['parameters']['temperature']
    top_p = values['parameters']['topP']
    top_k = values['parameters']['topK']
    context = values['context']
    prompt = values['testData'][0]['inputs'][0]


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
    model = TextGenerationModel.from_pretrained(model)
    response = model.predict(
        """"""+context+""""""
        """ input: """+prompt+
        """ """+source_context+""" """+source_prompt+
        """output:
        """,
            **parameters
    )
    # Return the response from the model to main.py
    return response.text