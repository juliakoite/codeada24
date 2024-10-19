import requests


API_Key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjRiZGE5NmItZjUzNS00MjBjLThjZDQtYjllYjYyNTE2OGQwIiwidHlwZSI6ImFwaV90b2tlbiJ9.JzTeIYcTmrEHgUdWrLHWIxnBaQRBNqfIr-TNxTRkVEw'

def parse_file(file_name):
#make file path user's input file 
    file = "uplaods/{file_name}"

    with open(file, 'rb') as f:
        response = requests.post(
            'https://api.edenai.run/v1/pretrained/financial_document_parsing',
            headers={'Authorization': f'Bearer {API_Key}'},
            files={'file': f}
        )


    data = response.text
    print(data)