import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("EDIN_API_KEY")
url = "https://api.edenai.run/v2/ocr/financial_parser"
def parse_file(file_name):
#make file path user's input file 
    file_path = f"uploads/{file_name}"
    with open(file_path, 'rb') as file:
    # Set the payload with the file
        files = {'file': file}
        data = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_base_64": True,
        "show_original_response": False,
        "document_type": "invoice",
        "convert_to_pdf": False,
        "providers": ["amazon"],
        "language": "en"
    }

        headers = {
        'Authorization': f'Bearer {api_key}',
        }

    # Send the POST request with the file
        response = requests.post(url, files=files, data=data, headers=headers)

    # Check the response
        if response.status_code == 200:
            # If the request was successful, print the parsed response
            response_str = response.text
            json_data = json.loads(response_str)
            print(json_data)
            items_dict = dict()
            item_lines = json_data['amazon']['extracted_data'][0]['item_lines']
            for item in item_lines:
                item_desc = item['description'] 
                if item_desc in items_dict.keys():
                    print("DUPLICATE:" + item_desc)
                    items_dict[item_desc] = (item['amount_line'], items_dict[item_desc][1] + 1) #if duplicate (double charge)
                else:
                    items_dict[item_desc] = (item['amount_line'], 1)
            for key in items_dict.keys():
                print("Item: " + key)
            for value in items_dict.values():
                print("Amount" + str(value))
            return items_dict

        else:
            print(f"Error: {response.status_code} - {response.text}")
