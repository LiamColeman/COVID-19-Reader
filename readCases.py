# Made by Liam Coleman
# All data from https://covidtracking.com/
import os
import tempfile
import requests
from gtts import gTTS
import time
from playsound import playsound

previousPositiveCases = 0


def readStats(text):
    tts = gTTS(text=text, lang='en')
    f = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    tts.write_to_fp(f)
    f.close()
    playsound(f.name)
    # print(f.name)
    os.remove(f.name)


while True:
    response = requests.get('https://covidtracking.com/api/us')
    if response.status_code == 200:
        print('Success!')
        print(response.text)
        response = response.json()
        positiveCases = response[0]["positive"]
        if positiveCases != previousPositiveCases:
            print(positiveCases)
            readStats(f"There are currently {positiveCases} known cases of covid19 in the US")
            previousPositiveCases = response[0]["positive"]
        else:
            print("No change")



    else:
        print(f'Unexpected Result {response.status_code}')

    time.sleep(5*60);
