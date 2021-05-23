import requests
import simplejson as json
import time
import winsound
import datetime

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
yellow = "\033[1;33m"
white = "\033[0;37m"

user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 ' \
                     'Safari/537.36'

headers = {
    'User-Agent': user_agent_desktop,
    'Accept-Language': 'hi_IN',
    'Content-Type': 'application/json'}


def find_slot(district):
    global red, blue, green, yellow, white

    global headers

    date = datetime.datetime.now() + + datetime.timedelta(days=1)  # look for the slots of tomorrow

    tomorrow = date.strftime("%d-%m-%Y")


    payload = {'district_id': district, 'date': tomorrow}

    r = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",params=payload, headers=headers)

    session = json.loads(r.text)

   # print(len(session.values()))

    for value in session.values():
        if(len(value) > 0):
            for res in value:
                if (res['available_capacity_dose1'] > 30):
                    print(green, res['date'], white, "Pincode:",red, res['pincode'], blue,"Slots:",res['available_capacity_dose1'], white, res['name'], res['address'],red,"Age:", res['min_age_limit'])
                    winsound.Beep(200, 800)
        else:
            print(blue, "No slots available")


try:
    r = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers=headers)
    states = r.json()
    states = states['states']
    for res in states:
        print(white, res['state_name'], ":", green, res['state_id'])
except Exception as e:
    print(red, e)

print(red, 'Enter state ID from list given:')
state_id = input()

dist = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + state_id, headers=headers)
districts = dist.json()
dists = districts['districts']

try:
    for dist_res in dists:
        print(white, dist_res['district_name'], ":", green, dist_res['district_id'], end="\t\n")
except Exception as e:
    print(red, e)

print(red, 'Select District:')
district = input()


i=0
while i==0:
    find_slot(district)
    time.sleep(4)  # run again after 2 secs

