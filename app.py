import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

load_dotenv()
client = OpenAI()
SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive'
]

app = Flask(__name__)


def get_google_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def push_to_google_slide(new_text, new_file=False):
    creds = get_google_creds()
    service = build('slides', 'v1', credentials=creds)
    requests =[
        {
            'replaceAllText': {
                'replaceText': new_text,
                #'pageObjectIds': [''],
                'containsText': {
                    'text': '<TK>',
                    'matchCase': True
                }
            }
        }
    ]
    body = {
        'requests': requests
    }
    service.presentations().batchUpdate(
        presentationId=os.environ.get('GOOGLE_SLIDES_PRESENTATION_ID'),
        body=body
    ).execute()
    service.close()


def call_assistant(message, thread):
    client.beta.threads.messages.create(thread_id=thread.id, content=message, role='user')
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=os.environ.get('ASSISTANT_ID')
    )
    while not run.status == 'completed':
        if run.status == 'requires_action' and run.required_action.type == 'submit_tool_outputs':
            tool_outputs = [{
                'tool_call_id': tool_call.id,
                'output': json.dumps(eval(tool_call.function.name)(**json.loads(tool_call.function.arguments)))
            } for tool_call in run.required_action.submit_tool_outputs.tool_calls]
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                tool_outputs=tool_outputs,
                run_id=run.id,
                thread_id=thread.id
            )
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    thread_id = request.json.get('thread_id')
    
    if not thread_id:
        thread = client.beta.threads.create(messages=[])
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)
    
    response = call_assistant(message, thread)
    return jsonify({'response': response, 'thread_id': thread_id})


if __name__ == '__main__':
    app.run(debug=True)
