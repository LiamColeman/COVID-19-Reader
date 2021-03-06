# Made by Liam Coleman
# All data from https://covidtracking.com/
import configparser
import os
import tempfile
import requests
from gtts import gTTS
import time
import datetime
from playsound import playsound


previousPositiveCases = 0
previousDeaths = 0
options = configparser.ConfigParser()

def getOptions():
    try:
        global airhornStatus
        global timerTime
        options.read('options.ini')
        airhornStatus = options.get('options', 'airhorn')
        timerTime = options.get('options', 'time')
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        options['options'] = {'airhorn': 'off', 'time': 15}
        with open('options.ini', 'w') as configfile:
            options.write(configfile)
        timerTime = 15
        airhornStatus = "off"

def doAirhorn():
    if airhornStatus == "on":
        playsound('airhorn.mp3')
    else:
        print("Airhorn is off")

def readStats(text):
    doAirhorn()
    tts = gTTS(text=text, lang='en')
    f = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    tts.write_to_fp(f)
    f.close()
    playsound(f.name)
    # print(f.name)
    os.remove(f.name)

def getData():
    # response = requests.get('https://covidtracking.com/api/us', headers=headers)
    response = requests.get('https://covidtracking.com/api/v1/us/current.json', headers=headers)

    global previousPositiveCases
    global previousDeaths
    if response.status_code == 200:
        print('Success!')
        print(response.text)
        response = response.json()
        positiveCases = response[0]["positive"]
        deaths = response[0]["death"]
        if positiveCases != previousPositiveCases or deaths != previousDeaths:
            print(positiveCases)
            print(deaths)
            readStats(f"There are currently {positiveCases} known cases and {deaths} deaths due to covid19 in the US")
            previousPositiveCases = response[0]["positive"]
            previousDeaths = response[0]["death"]
            log = open("log.txt", "a")
            log.write(f"As of {datetime.datetime.now().__str__()} {positiveCases} cases and {deaths} deaths \n")
            log.close()
        # elif deaths != previousDeaths:
        #     print(positiveCases)
        #     print(deaths)
        #     readStats(f"There are currently {positiveCases} known cases and {deaths} deaths  of covid19 in the US")
        #     previousDeaths = response[0]["death"]
        #     log = open("log.txt", "a")
        #     log.write(f"{deaths} covid deaths as of {datetime.datetime.now().__str__()} \n")
        #     log.close()
        else:
            print("No change")
    else:
        print(f'Unexpected Result {response.status_code}')

headers = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

getOptions()

while True:
    getData()
    time.sleep(float(timerTime)*60)