from openai import OpenAI
import requests

import os
import json

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def ask_ai(charge):
    example_json = {
    "charges": [
        {
        "procedure": "ARTERIAL PUNCTURE",
        "description": "Arterial puncture is a medical procedure in which a needle is inserted into an artery to collect blood for testing or to measure blood gases and acidity. This procedure is typically performed to evaluate oxygen and carbon dioxide levels in the blood.",
        "validity": "This charge is valid if the procedure was performed and you were billed for the service according to your health care provider's billing practices."
        } ]
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant trained to provide explanations to users who are confused about charges on their medical bills. Explain to them the procedure that the charge is for and whether or not the charge is valid. Provide output in valid JSON. The data schema should be like this: " + json.dumps(example_json)},
            {
                "role": "user",
                "content": "Can you explain these medical charges on my medical bill:" + str(charge)
            }
        ]
    )
    response_json = json.loads(response.choices[0].message.content)
    print(response_json)
    descriptions = []
    return_json = {"charges" : []}
    for charge in response_json['charges']:
        return_json['charges'].append({
            'Procedure' : charge['procedure'],
            'Description': charge['description'],
            'Validity': charge['validity']
        })
        #print("Description: " + charge['description'])
        #descriptions.append(charge['description'])
    return return_json