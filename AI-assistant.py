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
MachineLearning = {}

#Interface = str(raw_input("Interface: "))
Interface = "Voice"

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

def CheckAlarm():
    if hour == datetime.now().strftime('%H') and minute == datetime.now().strftime('%M'):
        ChangeVolume(volume, "100")
        for j in range(0,11):
            speak("alarm")
            
print("Ready for action sir")
speak("Ready for action sir")

Linenumber = 0
line_num = 0
Said = False

while True:
    CheckAlarm()
    
    if Interface == "Voice":
        Command = Listen(r)
        print "- " + str(Command)
    else:
        Command = str(raw_input("Command: "))
        
    if Command != None:
        if 'Jarvis' in Command and 'how' in Command and 'hot' in Command and 'is' in Command and 'it' in Command and 'outside' in Command:
            print("+ It is " + str(Getweather()) + " degrees outside")
            speak("It is " + str(Getweather()) + " degrees outside")
        elif 'Jarvis' in Command and 'what' in Command and 'is' in Command and 'the' in Command and 'time' in Command:
            print("+ " + str(Gettime()))
            speak(Gettime())
        elif 'Jarvis' in Command and 'calculate' in Command:
            print("+ The result of " + str(Command[17:]) + " is equal to " + str(eval(Command[17:])))
            speak("The result of " + str(Command[17:]) + " is equal to " + str(eval(Command[17:])))
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
        elif 'Jarvis' in Command and 'google' in Command:
            Result = Googlesomething(Command[12:])
            print("+ the answer to the question " + str(Command[12:]) + " is " + str(Result))
            speak("the answer to the question " + str(Command[12:]) + " is " + str(Result))
        elif 'Jarvis' in Command and 'change' in Command and 'the' in Command and 'volume' in Command and 'to' in Command:
            NewVolume = Command[28:]
            ChangeVolume(volume, NewVolume)
            print("+ the volume has been set to " + str(NewVolume))
            speak("the volume has been set to " + str(NewVolume))
        elif 'Jarvis' in Command and 'set' in Command and 'an' in Command and 'alarm' in Command and 'at' in Command:
            hour = Command[23:25]
            minute = Command[26:]
            print("+ Alarm has been set at " + str(hour) + " " + str(minute))
            speak("Alarm has been set at " + str(hour) + " " + str(minute))
        elif 'Jarvis' in Command and 'give' in Command and 'me' in Command and 'a' in Command and 'compliment' in Command:
            if randint(0, 10) < 5:
                print("+ You have beautiful eyes")
                speak("You have beautiful eyes")
            else:
                print("+ You are looking good")
                speak("You are looking good")
        else:
            CommandFile = open("commands.txt", "r")
            for line in CommandFile: 
                CommandPartsArray = line.split(" ")
                for i in range(0,len(CommandPartsArray)):
                    CommandPartsArray[i] = CommandPartsArray[i].rstrip()
                for CommandPart in CommandPartsArray:
                    if CommandPart in Command:
                        Score += 1
                        MachineLearning[line] = Score
                Score = 0

            for value, key in MachineLearning.iteritems():
                if key == len(Command.split(" ")):
                    CommandFile = open("commands.txt", "r")
                    for line in CommandFile.readlines():
                        line_num += 1
                        if line.find(value) >= 0:
                            Linenumber = line_num
                            break
                    CommandFile = open("commands.txt", "r")
                    for i, line in enumerate(CommandFile):    
                        if i == Linenumber:
                            speak(line)
                            print(line)
                            Said = True
            
            if Said != True:
                if "Jarvis" in Command:
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
                            with open("commands.txt", "a") as myfile:
                                myfile.write("\n" + Command + "\n")
                                myfile.write(Answer + "\n")
                                myfile.write(Command[7:] + "\n")
                                myfile.write("Are you talking to me if yes please say jarvis in front of the command")
                            print("New command added " + str(Command) + " With the answer " + str(Answer))
                            speak("New command added " + str(Command) + " With the answer " + str(Answer))
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
                                        with open("commands.txt", "a") as myfile:
                                            myfile.write(Command + "\n")
                                            myfile.write(Answer + "\n")
                                            myfile.write(Command[7:] + "\n")
                                            myfile.write("Are you talking to me if yes please say jarvis in front of the command")
                                        print("New command added " + str(Command) + " With the answer " + str(Answer))
                                        speak("New command added " + str(Command) + " With the answer " + str(Answer))
                                        Looper = False
                    else:
                        print("Answer has been skipped")
                        speak("Answer has been skipped")
                Looper = True
            else:
                Said = False
                    
                
        
