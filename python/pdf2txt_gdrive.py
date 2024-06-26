#!/mnt/linuxdata/james/code/venv_python/bin/python
# Copied from https://stackoverflow.com/questions/43713924/how-to-extract-pdf-content-into-txt-file-with-google-docs
# Credit to tanaike
# Python library documentation: https://googleapis.github.io/google-api-python-client/docs/epy/index.html

# For the imports to work you must do this before running the script:
# source /home/jlownie/james/code/venv_python/bin/activate

# Credentials are stored in /etc/pdf2txt, this dir must exist

import os.path
import io
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

# Scopes are the permissions requested by the app.  If you have modified them (eg, in the Google API web console), delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# This file stores the credentials used to login.  It is created automatically.
credentials_path="/etc/pdf2txt/pdf2txt_credentials.json"

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
token_path="/etc/pdf2txt/token.json"

def main():  
  # Parse command line arguments
  args=parseArgs()
  
  # Authentication
  creds = None
  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      # First delete token.json, as it confuses it sometimes
      os.remove(token_path)
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          credentials_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_path, "w") as token:
      token.write(creds.to_json())

  service = build("drive", "v3", credentials=creds)
  
  # Prepare the parameters
  pdffile = args.pdfname # PDF file
  logmsg('Input file: ' + pdffile)
  txtfile = pdffile.removesuffix('.pdf') + '.txt' # Text file
  logmsg('Output file: ' + txtfile)
  mime = 'application/vnd.google-apps.document'
  
  # Upload the PDF file
  logmsg('Uploading file')
  fileCreateTransaction = service.files().create(
  	body={
  		'name': pdffile,
  		'mimeType': mime
  	},
  	media_body=MediaFileUpload(pdffile, mimetype=mime, resumable=True)
  )
  res = fileCreateTransaction.execute()
  logmsg("Done")
  
  # Download the txt file
  logmsg('Downloading file')
  dl = MediaIoBaseDownload(
  	io.FileIO(txtfile, 'wb'),
  	service.files().export_media(fileId=res['id'], mimeType="text/plain")
  )
  done = False
  while done is False:
  	status, done = dl.next_chunk()
  logmsg("Done")

  # Delete the file from Drive  
  logmsg("Deleting file")
  deletion_json = {'trashed': True}
  response = service.files().update(fileId=res['id'], body=deletion_json).execute()
  logmsg("Done")

def logmsg( msg ):
  print(msg)

# Parses command line parameters and returns them
def parseArgs():
  parser = argparse.ArgumentParser(
      prog='pdf2txt',
      description='Converts PDFs to TXT files')
  parser.add_argument('pdfname', help="The path to the PDF file to be converted")
  return parser.parse_args()

if __name__ == "__main__":
  main()
