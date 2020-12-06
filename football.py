from __future__ import print_function
import pickle
import os.path
import cv2
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of the spreadsheet
SPREADSHEET_ID = '13FKqzuFu-A9_JSsTugiw17dOjlVf-_Zn52caU65qWnk'

# Get credentials to log in to google spreadsheets api
# First time log in is necessary, then saved in token.pickle
# Returns credentials object to connect to spreadsheet
def getCredentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Update players value in cell to P/L depending on time
def updateValue(player_id):
    # Get the correct cell for player + date
    row = int(player_id) + 2
    range_ = getDateColumn() + str(row)
    inputvalue = {}
    
    # Zaterdag of woensdag
    if datetime.today().weekday() == 5:
        # Present of late
        if datetime.time(datetime.now()) < datetime.time(datetime.strptime("10:00", "%H:%M")):
            inputvalue['values'] = [['P']]
        else:
            inputvalue['values'] = [['L']]
    else:
        if datetime.time(datetime.now()) < datetime.time(datetime.strptime("19:30", "%H:%M")):
            inputvalue['values'] = [['P']]
        else:
            inputvalue['values'] = [['L']]
    inputvalue['majorDimension'] = "ROWS"
    inputvalue['range'] = range_
    # Update the changes on the sheet
    updateSheet(inputvalue, range_)

# Update the sheet
# inputvalue = new value for the cell
# range_ = the cell range
def updateSheet(inputvalue, range_):
    service = build('sheets', 'v4', credentials=getCredentials())

    # Call the Sheets API
    sheet = service.spreadsheets()
    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption='RAW', body=inputvalue)
    response = request.execute()

# Get the correct column of the sheet based on todays date
def getDateColumn():
    range_ = 'G2:AK2' # Date values
    # Connect to the sheet
    service = build('sheets', 'v4', credentials=getCredentials())
    sheet = service.spreadsheets()
    # Get all dates from the sheet
    dates = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()
    values = dates.get('values', [])
    datestr = datetime.now().strftime("%d/%m")
    # Find todays date in the list
    idx = values[0].index(datestr)
    return colnum_string(idx + 7)

# Convert from an integer to a column string in sheet
def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def getId():
    result = -1
    #windows
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    #mac
    #cap = cv2.VideoCapture(0)
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        # detect and decode
        data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if bbox is not None:
            # display the image with lines
            for i in range(len(bbox)):
                # draw all lines
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            if data:
                result = data
                vinkje = cv2.imread("vinkje.jpg")
                cv2.imshow("vink", vinkje)
                cv2.waitKey(0)
                time.sleep(1)
                break
        # display the result
        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("q"):
            quit = True
            break
    cap.release()
    cv2.destroyAllWindows()
    if quit:
        return -1
    return result

if __name__ == '__main__':
    while True:
        value = getId()
        if value == -1:
            break
        else:
            updateValue(value)
