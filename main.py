import requests


API_Key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjRiZGE5NmItZjUzNS00MjBjLThjZDQtYjllYjYyNTE2OGQwIiwidHlwZSI6ImFwaV90b2tlbiJ9.JzTeIYcTmrEHgUdWrLHWIxnBaQRBNqfIr-TNxTRkVEw'
file_path = 'hospital bill format_2_.pdf'


with open(file_path, 'rb') as f:
    response = requests.post(
        'https://api.edenai.run/v1/pretrained/financial_document_parsing',
        headers={'Authorization': f'Bearer {API_Key}'},
        files={'file': f}
    )


data = response.json()
print(data)