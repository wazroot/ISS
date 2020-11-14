import requests
import urllib.request
from datetime import datetime, timezone, date
import datetime
import json
import pytz


people_in_space = 'http://api.open-notify.org/astros.json'
ISS_now = 'http://api.open-notify.org/iss-now.json'


# Coordinates for checking when and how many times ISS will pass given location
lat = input('Latitude?: ')
lon = input('Longitude?: ')
n = input('Number of ISS passes used to calculate passes before midnight(e.x 1,2,3): ')

# Automated year, month and day for the midnight section
today = datetime.datetime.now()
y = today.year
m = today.month
d = today.day
print('===============================================')
# How many people in space and their names
response = urllib.request.urlopen(people_in_space)
result = json.loads(response.read())

print('People in space:', result['number'], 'people')
print('===============================================')
people = result['people']
for i in people:
    print(i['name'], 'in', i['craft'])
print('================================================')
# ISS current location
response1 = urllib.request.urlopen(ISS_now)
result1 = json.loads(response1.read())
print('ISS current location:','latitude:', result1['iss_position']['latitude'],'&' ,'longitude:', result1['iss_position']['longitude'])
print('===================================================')

# Number of passes until midnight
ISS_passess = 'http://api.open-notify.org/iss-pass.json?' + 'lat=' + str(lat) + '&' + 'lon=' + str(lon) + '&n=' + str(n)
response2 = urllib.request.urlopen(ISS_passess)
result2 = json.loads(response2.read())


# Midnight time in unixms
midn_time_unixms = datetime.datetime(y, m, d, 23, 59, 59).timestamp()
parsed_mind_unixms = str(midn_time_unixms)[:-2]
parsed_mind_unixms_int = int(parsed_mind_unixms)
#print(parsed_mind_unixms_int) 


parameters = {
    'lat' : float(lat),
    'lon' : float(lon),
    'n' : float(n)
}

response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
#print(response.json())

pass_times = response.json()['response']
#print(pass_times)
# Pass times till midnight
risetimes = []
durations = []
for d in pass_times:
    if d['risetime'] < parsed_mind_unixms_int:
        time = d['risetime']
        risetimes.append(time)
        dur = d['duration']
        durations.append(dur)
#print(risetimes)
#print(durations)

times = []
for rt in risetimes:
    time = datetime.datetime.fromtimestamp(int(rt)).isoformat()
    times.append(time)
    print('ISS pass times before midnight: ' + str(time))
print('===========================================================')
durations1 = []
for dr in durations:
    dur_sec = str(dr) + ' seconds'
    durations1.append(dur_sec)
    print('ISS pass durations: ' + dur_sec)
print('==============================================================')
# How many times ISS will pass given location before midnight
print('Number of ISS passes before midnight: ',len(risetimes))

