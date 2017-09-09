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
import sounddevice as sd
import time

Looper = True
Score = 0
hour = 100
minute = 100
Machine_learning = {"hi": "hello"}
Command_added = False

Interface = str(raw_input("Interface: "))

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

speak("Ready for action sir")
print("Ready for action sir")

while True:
    if hour == datetime.now().strftime('%H') and minute == datetime.now().strftime('%M'):
        ChangeVolume(volume, "100")
        for j in range(0,11):
            speak("alarm")
    if Interface == "Voice":
        Command = Listen(r)
        print "- " + str(Command)
    else:
        Command = str(raw_input("Command: "))
    if Command != None:
        if 'Jarvis' in Command and 'how' in Command and 'hot' in Command and 'is' in Command and 'it' in Command and 'outside' in Command:
            print("+ It is " + str(Getweather()) + " degrees outside")
            speak("It is " + str(Getweather()) + " degrees outside")
        elif 'how' in Command and 'hot' in Command and 'is' in Command and 'it' in Command and 'outside' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'what' in Command and 'is' in Command and 'the' in Command and 'time' in Command:
            print("+ " + str(Gettime()))
            speak(Gettime())
        elif 'what' in Command and 'is' in Command and 'the' in Command and 'time' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'who' in Command and 'is' in Command and ('Jasper' in Command or 'jesper' in Command):
            print("+ Jesper is the most cool and beautiful person in this universe")
            speak("Jesper is the most cool and beautiful person in this universe")
        elif 'who' in Command and 'is' in Command and ('Jasper' in Command or 'jesper' in Command):
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'who' in Command and 'is' in Command and 'Lisa' in Command:
            print("+ She is the sister of Jesper nobody cares about her")
            speak("She is the sister of Jesper nobody cares about her")
        elif 'who' in Command and 'is' in Command and 'Lisa' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'enable' in Command and 'security' in Command:
            print("+ Security has been enabled")
            speak("Security has been enabled")
        elif 'enable' in Command and 'security' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'what' in Command and 'is' in Command and '9' in Command and '+' in Command and '10' in Command:
            print("+ 21")
            speak("21")
        elif 'what' in Command and 'is' in Command and '9' in Command and '+' in Command and '10' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'will' in Command and 'robots' in Command and 'destroy' in Command and 'the' in Command and 'world' in Command:
            print("+ I have not acquired enough information about the human race to answer that question")
            speak("I have not acquired enough information about the human race to answer that question")
        elif 'will' in Command and 'robots' in Command and 'destroy' in Command and 'the' in Command and 'world' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'what' in Command and 'is' in Command and 'a' in Command and 'meme' in Command:
            print("+ One of the best things ever created")
            speak("One of the best things ever created")
        elif 'what' in Command and 'is' in Command and 'a' in Command and 'meme' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'tell' in Command and 'me' in Command and 'a' in Command and 'joke' in Command:
            print("+ Your life")
            speak("your lifed")
        elif 'tell' in Command and 'me' in Command and 'a' in Command and 'joke' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'turn' in Command and 'on' in Command and 'the ' in Command and 'lights' in Command:
            print("+ I am not able to do that yet")
            speak("I am not able to do that yet")
        elif 'turn' in Command and 'on' in Command and 'the ' in Command and 'lights' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'turn' in Command and 'off' in Command and 'the ' in Command and 'lights' in Command:
            speak("I am not able to do that yet")
            print("+ I am not able to do that yet")
        elif 'turn' in Command and 'off' in Command and 'the ' in Command and 'lights' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'calculate' in Command:
            print("+ The result of " + str(Command[17:]) + " is equal to " + str(eval(Command[17:])))
            speak("The result of " + str(Command[17:]) + " is equal to " + str(eval(Command[17:])))
        elif 'calculate' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'record' in Command and 'seconds' in Command and 'of' in Command and 'audio' in Command:
            Length = Command[13:15]
            fs = 44100
            print("+ Recording")
            speak("Recording")
            myrecording = sd.rec(int(int(Length) * fs), samplerate=fs, channels=2)
            time.sleep(int(Length))
            print("+ This is what i have recorded")
            speak("This is what i have recorded")
            sd.play(myrecording)
            print("*recording playing*")
            time.sleep(int(Length))
        elif 'record' in Command and 'seconds' in Command and 'of' in Command and 'audio' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'google' in Command:
            Result = Googlesomething(Command[12:])
            print("+ the answer to the question " + str(Command[12:]) + " is " + str(Result))
            speak("the answer to the question " + str(Command[12:]) + " is " + str(Result))
        elif 'google' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'how' in Command and 'are' in Command and 'you' in Command:
            print("+ I am fine thank you for asking")
            speak("I am fine thank you for asking")
        elif 'how' in Command and 'are' in Command and 'you' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'change' in Command and 'the' in Command and 'volume' in Command and 'to' in Command:
            NewVolume = Command[28:]
            ChangeVolume(volume, NewVolume)
            print("+ the volume has been set to " + str(NewVolume))
            speak("the volume has been set to " + str(NewVolume))
        elif 'change' in Command and 'the' in Command and 'volume' in Command and 'to' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'set' in Command and 'an' in Command and 'alarm' in Command and 'at' in Command:
            hour = Command[23:25]
            minute = Command[26:]
            print("+ Alarm has been set at " + str(hour) + " " + str(minute))
            speak("Alarm has been set at " + str(hour) + " " + str(minute))
        elif 'set' in Command and 'an' in Command and 'alarm' in Command and 'at' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        elif 'Jarvis' in Command and 'give' in Command and 'me' in Command and 'a' in Command and 'compliment' in Command:
            if randint(0, 10) < 5:
                print("+ You have beautiful eyes")
                speak("You have beautiful eyes")
            else:
                print("+ You are looking good")
                speak("You are looking good")
        elif 'give' in Command and 'me' in Command and 'a' in Command and 'compliment' in Command:
            print("+ are you talking to me if yes then please say jarvis in front of the command")
            speak("are you talking to me if yes then please say jarvis in front of the command")
        else:
            for Question in Machine_learning:
                if Question in Command:
                    Score += 1

            if Score > len(Command.split(" ")) / 2:
                speak(Machine_learning[Command])
                print(Machine_learning[Command])
            elif "Jarvis" in Command:
                print("+ I do not know the command " + str(Command[6:]))
                speak("I do not know the command " + str(Command[6:]))
                print("What should be the answer")
                speak("What should be the answer")
                Answer = Listen(r)
                if Answer != "no answer":
                    print("Is the answer " + str(Answer))
                    speak("Is the answer " + str(Answer))
                    Comfirmation = Listen(r)
                    if Comfirmation == "yes":
                        for i in Command.split(" "):
                            Machine_learning[i] = Answer

                            Machine_learning[Command] = Answer
                        print("New cammand added " + str(Command) + " With the answer " + str(Answer))
                        speak("New cammand added " + str(Command) + " With the answer " + str(Answer))
                    else:
                        while Looper == True:
                            print("Please try again")
                            speak("Please try again")
                            Answer = Listen(r)
                            if Answer == "no answer":
                                Looper = False
                                print("Answer has been skipped")
                                speak("Answer has been skipped")
                            else:
                                print("Is the answer " + str(Answer))
                                speak("Is the answer " + str(Answer))
                                Comfirmation = Listen(r)
                                if Comfirmation == "yes":
                                    for i in Command.split(" "):
                                        Machine_learning[i] = Answer

                                        Machine_learning[Command] = Answer
                                    print("New cammand added " + str(Command) + " With the answer " + str(Answer))
                                    speak("New cammand added " + str(Command) + " With the answer " + str(Answer))
                else:
                    print("Answer has been skipped")
                    speak("Answer has been skipped")
                
                
        
