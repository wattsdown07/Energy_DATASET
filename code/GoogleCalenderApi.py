pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime

#Scopes for readonly access to calendar,
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

#Authenticate and build the service,
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
service = build('calendar', 'v3', credentials=creds)

#Get time window (next 60 days, for example),
now = datetime.datetime.utcnow().isoformat() + 'Z'
future = (datetime.datetime.utcnow() + datetime.timedelta(days=60)).isoformat() + 'Z'

#Read events (holidays, meetings, bookings, public holidays if calendar is subscribed),
events_result = service.events().list(
    calendarId='primary',
    timeMin=now,
    timeMax=future,
    singleEvents=True,
    orderBy='startTime'
).execute()
events = events_result.get('items', [])

#Function to determine season (basic logic),
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Fall"
    else:
        return "Unknown"

#Print useful calendar variables for energy analysis,
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
    season = get_season(dt)
    summary = event.get('summary', 'No Title')
    day_name = dt.strftime("%A")
    is_weekend = day_name in ["Saturday", "Sunday"]

    print(f"Event: {summary} | Date: {dt.date()} | Day: {day_name} | Weekend: {is_weekend} | Season: {season}")

#You can also automatically flag public holidays and school breaks