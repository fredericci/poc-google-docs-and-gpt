# Google Docs + OpenAI

I'm curious about the new OpenAI APIs and their capability to understand documents like contracts, technical documentation, Q&A, how-to guides, and so on.

This proof of concept basically reads a Google Doc document and sends its plain text content to OpenAI. Then, you can ask questions about it.

In my tests, I took a job description and asked the AI to create 10 questions to interview a candidate.

## Install libs

```bash
$ pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

## Dependency install 

```bash
$ pip install -r requirements.txt
```

## Create your own OpenAI API Key and change the .env file
https://platform.openai.com/account/api-keys

## Create your own Google Docs Credentials
https://console.cloud.google.com/apis/credentials

It is only using document readonly scope. 
/auth/documents.readonly

## Choose your google doc file and set its ID on .env file
DOCUMENT_ID=<YOUR DOCUMENT ID>

You can find the document id opening the file 
https://docs.google.com/document/d/<DOCUMENT_ID>/edit

## Execution 

```bash
$ python poc.py
```

In the first time you have to authorize the Google Aplication