import os
import base64
import mimetypes
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# If modifying the SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Authenticate and create a service
def authenticate_gmail():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('./credentials/ash.temp.new@gmail.com-token.json'):
        creds = Credentials.from_authorized_user_file('./credentials/ash.temp.new@gmail.com-token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./credentials/ash.temp.new@gmail.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('./credentials/ash.temp.new@gmail.com-token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

# Function to create the email message
def create_message(sender, to, subject, body, image_path):
    # Create the root message
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Add the body of the email
    msg = MIMEText(body, 'html')
    message.attach(msg)

    # Add the image as Base64 encoding
    content_type, encoding = mimetypes.guess_type(image_path)
    content_type = content_type or 'application/octet-stream'
    with open(image_path, 'rb') as image_file:
        img_data = image_file.read()
        encoded_img = base64.b64encode(img_data).decode('utf-8')
        #encoded_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/9lD1+gAAAAASUVORK5CYII="
    
    image = MIMEImage(img_data, _subtype='png')
    image.add_header('Content-ID', '<image1>')
    message.attach(image)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')}

# Send the email
def send_message(service, sender, to, subject, body, image_path):
    try:
        message = create_message(sender, to, subject, body, image_path)
        message_sent = service.users().messages().send(userId="me", body=message).execute()
        print('Message Id: %s' % message_sent['id'])
        return message_sent
    except Exception as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    sender = "ash.temp.new@gmail"  # Replace with your Gmail address
    to = "ash.temp.new@gmail.com"  # Replace with recipient's email
    subject = "Test Email with Base64 Image"
    body = '''
    <h1>Welcome to My Email!</h1>
    <p>This is an example of an email with an embedded Base64 image:</p>
    <img src="cid:image1">
    '''
    image_path = "./test.png"  # Replace with the path to your image

    # Authenticate and send the message
    service = authenticate_gmail()
    send_message(service, sender, to, subject, body, image_path)
