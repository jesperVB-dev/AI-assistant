import pyttsx
import speech_recognition as sr
from urllib2 import Request, urlopen, URLError
import json
from datetime import datetime
from random import randint
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google import google

hour = 100
minute = 100

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
   IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
speech_engine = pyttsx.init('sapi5') # see http://pyttsx.readthedocs.org/en/latest/engine.html#pyttsx.init
speech_engine.setProperty('rate', 150)

def speak(text):
	speech_engine.say(text)
	speech_engine.runAndWait()
 
# get audio from the microphone                                                                       
r = sr.Recognizer()

def Listen(r):
    with sr.Microphone() as source:                                                                                 
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            Listen(r)

def Getweather():
    request = Request('http://api.wunderground.com/api/60eb52589081d5c1/conditions/q/BE/ninove.json')

    try:
	response = urlopen(request)
	kittens = response.read()
	resp_dict = json.loads(kittens)
	return resp_dict['current_observation']['temp_c']
    except URLError, e:
        print 'No kittez. Got an error code:', e

def Gettime():
    Hours = datetime.now().strftime('%H')
    Hours = int(Hours) % 12
    Minutes = datetime.now().strftime('%M')
    Seconds = datetime.now().strftime('%S')
    
    return "It is " + str(Minutes) + " over " + str(Hours) + " and " + str(Seconds) + " seconds"

def ChangeVolume(volume, Volume):
    if Volume == "100":
        volume.SetMasterVolumeLevel(-0.0, None)
    elif Volume == "75":
        volume.SetMasterVolumeLevel(-5.0, None)
    elif Volume == "50":
        volume.SetMasterVolumeLevel(-10.0, None)
    elif Volume == "25":
        volume.SetMasterVolumeLevel(-25.0, None)
    elif Volume == "0":
        volume.SetMasterVolumeLevel(-60.0, None)

def Googlesomething(Query):
    num_page = 1
    Result = []
    search_results = google.search(Query, 1)
    for result in search_results:
        Result.append(result.name)

    return Result[0]

def Calculate(Query):
    return eval(Query)
        
while True:
    if hour == datetime.now().strftime('%H') and minute == datetime.now().strftime('%M'):
        ChangeVolume(volume, "100")
        speak("your alarm is going of")
    Command = Listen(r)
    print Command
    
    if Command == "Lola how hot is it outside":
        speak("It is " + str(Getweather()) + " degrees outside")
    elif Command == "Lola what is the time":
        speak(Gettime())
    elif Command == "Lola who is Jasper":
        speak("Jesper is the most cool and beautiful person in this universe")
    elif Command == "Lola who is Lisa":
        speak("She is the sister of Jesper nobody cares about her")
    elif Command == "Lola what is 9 + 10":
        speak("21")
    elif Command == "Lola will robots destroy the world":
        speak("I have not acquired enough information about the human race to answer that question")
    elif Command == "Lola what is a meme":
        speak("One of the best things ever created")
    elif Command == "Lola enumerate something":
        speak("Sure what do you want me to calculate")
        Calculation = Listen(r)
        Result = Calculate(Calculation)
        speak("The result of " + str(Calculation) + " is equal to " + str(Result))
    elif Command == "Lola Google something":
        speak("Sure what do you want me to google")
        Query = Listen(r)
        Result = Googlesomething(Query)
        speak("the answer to the question " + str(Query) + " is " + str(Result))
    elif Command == "Lola how are you":
        speak("I am fine thank you for asking")
    elif Command == "Lola change the volume":
        speak("What should be the volume")
        NewVolume = Listen(r)
        ChangeVolume(volume, NewVolume)
        speak("the volume has been set to " + str(NewVolume))
    elif Command == "Lola set an alarm":
        speak("What will be the hour")
        hour = Listen(r)
        speak("the hour set is " + str(hour))
        speak("What will be the minute")
        minute = Listen(r)
        speak("the minute set is " + str(minute))
        speak("Alarm has been set at " + str(hour) + " " + str(minute))
    elif Command == "Lola give me a compliment":
        if randint(0, 10) < 5:
            speak("You have beautiful eyes")
        else:
            speak("You are looking good")
    elif Command != None:
        if "Lola" in Command:
            speak("I do not know the command " + str(Command[4:]))
