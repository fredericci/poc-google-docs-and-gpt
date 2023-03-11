from __future__ import print_function

import os
import openai
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

# Create your own API KEY in https://platform.openai.com/account/api-keys
api_key = os.getenv("OPENAI_API_KEY")

# That is a test document. It's about a job description for a devops position
document_id = os.getenv("DOCUMENT_ID")

# What question would you like to ask about the document?
question = "Baseado na descrição da vaga de Engenheiro de Software Senior acima, crie 10 perguntas difíceis para entrevista dos candidatos"

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def main():

    # Get the Google Docs API credations based on credentials.json
    creds = get_credations()

    try:
        # Load the Google Docs content in plain text
        document = load_document(creds)
        
        print('----------------------------------------------------')
        print('Title of the document is: {}'.format(document.get('title')))
        print('----------------------------------------------------')
        print('Document content: ')
        print('----------------------------------------------------')
        text = get_plain_text(document)
        print(text)
        print('----------------------------------------------------')
        print('\n\n')

        # Concat the prompt
        prompt = generate_question(text) 
                
        # Send to OpenAI API         
        openai.api_key = api_key
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        print(response.choices[0].text)
        
    except HttpError as err:
        print(err)

def generate_question(text):
    return text + "\n\n" + question

def load_document(creds):
    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=document_id).execute()
    return document

def get_credations():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_plain_text(document):
    text_runs = []
    for element in document.get('body').get('content'):
        if 'paragraph' in element:
            for paragraph_element in element.get('paragraph').get('elements'):
                if 'textRun' in paragraph_element:
                    if paragraph_element.get('textRun').get('content') not in ['\n','','\\n']:
                        text_runs.append(paragraph_element.get('textRun').get('content'))
    
    return "".join(text_runs)

if __name__ == '__main__':
    main()
