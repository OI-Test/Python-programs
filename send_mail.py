#!/usr/bin/env python

# import httplib2
import os

# from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file

try:
    import argparse

    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Mails'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    
    """
    home_dir = os.path.expanduser('.')
    credential_dir = os.path.join(home_dir, '')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'API_Token.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
        """
    
    credential_dir = '.'
    credential_path = os.path.join(credential_dir,'API_Token.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    return credentials


import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from httplib2 import Http

from apiclient import errors
# import apiclient
from apiclient.discovery import build

credentials = get_credentials()
service = build('gmail', 'v1', http=credentials.authorize(Http()))


def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def CreateMessage(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64 encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.b64encode(message.as_string().encode()).decode()}


# testMessage = CreateMessage('EMAIL ADDRESS', 'EMAIL ADDRESS', 'subject', 'YOUR MESSAGE')

# testSend = SendMessage(service, 'me', testMessage)

"""
parser = argparse.ArgumentParser()

parser.add_argument("--sender", "-s", help="sender email")
parser.add_argument("--receiver", "-r", help="Rec email")
parser.add_argument("--subject", "-t", help="Subject")
parser.add_argument("--body", "-b", help="Body")
args = parser.parse_args()
"""


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--sender", "-s", help="sender email", action="store", dest="sender", required=True)
    parser.add_argument("--receiver", "-r", help="Rec email", action="store", required=True)
    parser.add_argument("--subject", "-t", help="Subject", action="store", required=True)
    parser.add_argument("--body", "-b", help="Body", action="store", required=True)
    args = parser.parse_args()
    # print(args)
    # if args.sender and args.receiver and args.subject and args.body:
    testMessage = CreateMessage(args.sender, args.receiver, args.subject, args.body)
    SendMessage(service, 'me', testMessage)


if __name__ == '__main__':
    main()
