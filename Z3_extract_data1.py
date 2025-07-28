import os
import json
import requests
import base64
from Z3_1_schema_cyber import schema_cyber
from datetime import datetime


import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

Pry_Token = os.getenv('Pry_Token')


def extract_data(file):
    sample = {
        "file": file,
        "settings": {
            "pages": "1-500",
            "dpi": 300,
            "ocr": {
                "extract": True,
                "multilingual": False,
                "fields": {
                    "extract": True,
                    "filter": False,
                    "model": "engine7"
                },
                "table": {
                    "extract": True,
                    "include": True,
                    "validate": False,
                    "json": True
                },
                "paragraphs": {
                    "json": True
                },
                "localization": {
                    "translate": False,
                    "language": "english",
                    "model": "engine7"
                }
            },
            "barcode": {
                "extract": False
            },
            "signature": {
                "extract": False,
                "crop": True
            }
        },
        "schema": schema_cyber,
        "version": "3.0.0",
        "key": "0f0e453f-58fc-4c34-8ef0-901340cf46ba"
    }

    ############# To make a json file for payload ############
    # payloadPath = os.path.join(os.path.dirname(__file__),"payload.json")
    # with open(payloadPath, 'w+') as fl:
    #     json.dump(sample, fl, indent=4)

    json_data = json.dumps(sample)

    try:
        url = "https://sequel-invoice-api-1055298495325.asia-south1.run.app/api/invoice"
        headers1 = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {Pry_Token}'
        }
        response = requests.post(url, data=json_data, headers=headers1)

        # print(response,"Response generated")
        data = response.json()
        # print(data)
        return data
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the POST request:", e)
        return None
    except json.JSONDecodeError as e:
        print("An error occurred while parsing the JSON response:", e)
        return None
    except IOError as e:
        print("An error occurred while writing the JSON response to a file:", e)
        return None


def convertobase64(file):

    file_text = open(file, 'rb')
    file_read = file_text.read()
    file_encode = base64.encodebytes(file_read).decode('utf-8')

    # Determine file type and data type accordingly
    if file.lower().endswith('.pdf'):
        data_type = 'data:application/pdf;base64,'

    elif file.lower().endswith(('.png')):
        data_type = 'data:image/png;base64,'

    elif file.lower().endswith(('.jpeg')):
        data_type = 'data:image/jpeg;base64,'

    elif file.lower().endswith(('.jpg')):
        data_type = 'data:image/jpg;base64,'

    else:
        raise ValueError('Unsupported file type')

    # Add data type before base64 string
    # "file": data_type
    base64_with_data_type = data_type + file_encode

    return base64_with_data_type.replace('\n', '')


# file_path = r'C:\Users\bheem\Desktop\sequelstring_zomato\code\cyber_cell_notices\downloads_20250724_080435\unprotected.pdf'
# # file_path=r'C:\Users\bheem\Desktop\sequelstring_zomato\docs\CYBER CELL\1. Cyber Crime Notice Sample.pdf'
# base64_file = convertobase64(file_path)
# extracted_data = extract_data(base64_file)

# # with open('cyber_data.json', 'w') as f:
# #     json.dump(extracted_data, f, indent=4)
# # print('--------------',extracted_data)

# folder_name = "json_data"
# os.makedirs(folder_name, exist_ok=True)

# # Generate filename with timestamp
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"cyber_data_{timestamp}.json"
# file_path = os.path.join(folder_name, filename)

# # Save JSON
# with open(file_path, 'w') as f:
#     json.dump(extracted_data, f, indent=4)



def process_and_save_json_from_pdf(pdf_path):

    base64_file = convertobase64(pdf_path)
    extracted_data = extract_data(base64_file)
    folder_name = "json_data"
    os.makedirs(folder_name, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"cyber_data_{timestamp}.json"
    json_file_path = os.path.join(folder_name, json_filename)

    # Step 5: Save to JSON
    with open(json_file_path, 'w') as f:
        json.dump(extracted_data, f, indent=4)

    print(f"✅ Extracted data saved to: {json_file_path}")
    return json_file_path
