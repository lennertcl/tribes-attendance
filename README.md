# tribes-attendance

An attendance tracker for teams. 

## Quickstart

### Create the spreadsheet
Create a spreadsheet with a layout like this example spreadsheet (or make a copy):
[Example sheet](https://docs.google.com/spreadsheets/d/1GHKTF-wD1uFAr05xRbIQ0OZ1T8dA0MOjeYovrxiofEg/edit?usp=drivesdk)

Give the app access to your spreadsheet. 
Follow this tutorial to make a project:
[Tutorial](https://developers.google.com/workspace/guides/create-project)
Go to Api's and services:
* You'll need to enable the Google Sheets api. 
* Configure the OAuth consent screen.
* Under test users, click add users and the sheet owner's gmail address. 
* Go to credentials and click on create credentials -> OAuth client ID.
* Select desktop app for application type and give it a name.

### Set the config variables

Install the requirements
```
pip install -r requirements.txt
```

Edit the config.py file to fit your needs.
(Weekdays monday-sunday are 0-6)

Example:
* Meeting every wednesday starting 19:30
* Meeting every saturday starting 10:00

```python
Class Config():
    SHEET_ID="Your spreadsheet ID"
    MEETINGS= {2: "19:30",
               5: "10:00"}
    SCANNER_WINDOW_TITLE="Can be anything"
    SCANOKAY_WINDOW_TITLE="Can be anything"
    SCANOKAY_IMAGE="Image file to show"
```

Run the script
```
python attendance.py
```
The first time using a new spreadsheet id you
will be taken to a Google login screen to
authorize the application. Your login data
will be stored in token.pickle file from that
point. 

### Generating QR codes
Run the script with the amount of people in your
spreadsheet as argument, e.g.
```
python qr_generator.py 20
```
The requested QR codes will be placed in the
qrcodes/ folder. They are numbered with the
same ordering as the spreadsheet. 
