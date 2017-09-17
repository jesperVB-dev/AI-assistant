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
from collections import defaultdict
import pygame
import os

Looper = True
NextLine = False
Score = 0
hour = 100
minute = 100
MachineLearning = defaultdict(list)
Linenumber = 0
line_num = 0
Said = False
ScoreIndexes = True
Loopme = True

#Interface = str(raw_input("Interface: "))
Interface = "Keyboard"

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

def RecordAudio(Length):
    Length = Command[13:16]
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
    
def PlayMusic(Loopme):
    root, dirs, files = next(os.walk('tracks/'))
    
    pygame.mixer.init()
    
    for name in files:
        name = 'tracks/'+str(name)
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy() and Loopme == True:
            Loopquestion = Listen(r)
            print "-" + str(Loopquestion)
            if Loopquestion == "Jarvis stop the music":
                PauseMusic()
                Loopme == False
            pygame.time.Clock().tick(5)
        Loopme = True
        return
    

def StopMusic():
    pygame.mixer.music.stop()

def PauseMusic():
    pygame.mixer.music.pause()

def ResumeMusic(Loopme):
    pygame.mixer.music.play
    while pygame.mixer.music.get_busy() and Loopme == True:
        Loopquestion = Listen(r)
        print "-" + str(Loopquestion)
        if Loopquestion == "Jarvis stop the music":
            PauseMusic()
            Loopme == False
        pygame.time.Clock().tick(5)
    Loopme = True
    return

def CheckAlarm():
    if hour == datetime.now().strftime('%H') and minute == datetime.now().strftime('%M'):
        ChangeVolume(volume, "100")
        for j in range(0,11):
            speak("alarm")

def NewCommand(Type):
    if Type == "Asked":
        print("+ Sure what will be the command and what the answer")
        speak("Sure what will be the command and what the answer")
        CommandAnswer = Listen(r)
        print CommandAnswer
        while ' with the answer ' not in CommandAnswer:
            print("+ please start the answer to the command with 'with the answer'")
            speak("please start the answer to the command with quote with the answer")
            CommandAnswer = Listen(r)
        
        Command = CommandAnswer.split(" with the answer ")[0]
        Answer = CommandAnswer.split(" with the answer ")[1]
    else:
        Command = Type
        
    print("+ Is the answer to the Command " + str(Command) + " " + str(Answer))
    speak("Is the answer to the Command " + str(Command) + " " + str(Answer))
    Comfirmation = Listen(r)

    if 'yes' in Comfirmation:
        with open("commands.txt", "a") as myfile:
            myfile.write(Command + "\n")
            myfile.write(Answer + "\n")
            myfile.write(Command[7:] + "\n")
            myfile.write("Are you talking to me if yes please say jarvis in front of the command")
        print("New command added " + str(Command) + " With the answer " + str(Answer))
        speak("New command added " + str(Command) + " With the answer " + str(Answer))
        Looper = True
    elif 'no answer' in Comfirmation:
        print("Answer has been skipped")
        speak("Answer has been skipped")
        Looper = True
    else:
        while Looper == True:
            print("Please try again")
            speak("Please try again")
            Answer = Listen(r)
            if "no answer" in Answer:
                print("Answer has been skipped")
                speak("Answer has been skipped")
                Looper = False
            else:
                print("+ Is the answer to the Command " + str(Command) + " " + str(Answer))
                speak("Is the answer to the Command " + str(Command) + " " + str(Answer))
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
                elif "no answer" in Answer:
                    print("Answer has been skipped")
                    speak("Answer has been skipped")
                    Looper = False

def AnswerCommand(CommandRecognised, line_num, Score, r, Command):
    CommandFile = open("commands.txt", "r")
    for line in CommandFile.readlines():
        line_num += 1
        if line.find(CommandRecognised) >= 0:
            Linenumber = line_num
            break
        
    CommandFile = open("commands.txt", "r")
    for i, line in enumerate(CommandFile):    
        if i == Linenumber:
            Answer = line
            speak(line)
            print("+ " + str(line))
            MachineLearning = defaultdict(list)
    
    if len(Command.split(" "))/2 > Score:
        print("+ Is this answer correct")
        speak("Is this answer correct")
        Comfirmmation = Listen(r)
        if "yes" in Comfirmmation:
            with open("commands.txt", "a") as myfile:
                myfile.write(CommandRecognised + "\n")
                myfile.write(Answer + "\n")
                myfile.write(CommandRecognised[7:] + "\n")
                myfile.write("Are you talking to me if yes please say jarvis in front of the command")
            print("New command added " + str(Command) + " With the answer " + str(Answer))
            speak("New command added " + str(Command) + " With the answer " + str(Answer))
        else:
            print("+ Do you want me to make a new command of it")
            speak("Do you want me to make a new command of it")
            Comfirmmation = Listen(r)
            if "yes" in Comfirmmation:
                NewCommand(Command)
            else:
                print("+ Well i am not always correct")
                speak("Well i am not always correct")
def TryToRecognise(NextLine, ScoreIndexes, Score, Command):
    CommandFile = open("commands.txt", "r")
    for line in CommandFile:
        line = line.rstrip()
        if NextLine == True:
            print("+ " + str(line))
            speak(line)
            NextLine = False
            ScoreIndexes = False
            break
        if line == Command:
            NextLine = True
                    
    if ScoreIndexes == True:
        CommandFile = open("commands.txt", "r")
        for lines in CommandFile:
            for lines in CommandFile:
                lines = lines.rstrip()
                CommandParts = lines.split(" ")
                CommandParts.append(lines)
                for i in CommandParts:
                    if i in Command:
                        Score += 1
                    MachineLearning[Score].append(CommandParts)
                Score = 0
        for i in range(len(Command)+1,0,-1):
            if MachineLearning.get(i) != None:
                Commands = MachineLearning.get(i)
                Commands = Commands[0]
                CommandRecognised = Commands[-1]
                if "Jarvis" in Command and "Jarvis" in CommandRecognised:
                    print "+ I think you said " + str(CommandRecognised)
                    AnswerCommand(CommandRecognised, line_num, i, r, Command)
                    break
            
    else:
        ScoreIndexes = True
        
def KnownCommands(Command, r, NextLine, ScoreIndexes, Score):
    if Command != None:
        if 'Jarvis' in Command and 'how' in Command and 'hot' in Command and 'is' in Command and 'it' in Command and 'outside' in Command:
            print("+ It is " + str(Getweather()) + " degrees outside")
            speak("It is " + str(Getweather()) + " degrees outside")
        elif 'Jarvis' in Command and 'play' in Command and 'some' in Command and 'music' in Command:
            print("+ Playing Music")
            speak("Playing Music")
            PlayMusic(Loopme)
        elif 'Jarvis' in Command and 'pause' in Command and 'the' in Command and 'music' in Command:
            print("+ Pausing Music")
            speak("Pausing Music")
            PauseMusic()
        elif 'Jarvis' in Command and 'resume' in Command and 'the' in Command and 'music' in Command:
            print("+ resuming Music")
            speak("resuming Music")
            ResumeMusic()
        elif 'Jarvis' in Command and 'what' in Command and 'is' in Command and 'the' in Command and 'time' in Command:
            print("+ " + str(Gettime()))
            speak(Gettime())
        elif 'Jarvis' in Command and 'calculate' in Command:
            print("+ The result of " + str(Command[17:]) + " is equal to " + str(eval(Command[17:])))
            speak("The result of " + str(Command[17:]) + " is equal to " + str(eval(Command[17:])))
        elif 'Jarvis' in Command and 'record' in Command and 'seconds' in Command and 'of' in Command and 'audio' in Command:
            Length = Command[13:16]
            RecordAudio(Length)
        elif 'Jarvis' in Command and ('google' in Command or 'Google' in Command):
            Result = Googlesomething(Command[12:])
            print("+ the answer to the question " + str(Command[12:]) + " is " + str(Result))
            speak("the answer to the question " + str(Command[12:]) + " is " + str(Result))
        elif 'Jarvis' in Command and 'change' in Command and 'the' in Command and 'volume' in Command and 'to' in Command:
            NewVolume = Command[28:]
            ChangeVolume(volume, NewVolume)
            print("+ the volume has been set to " + str(NewVolume))
            speak("the volume has been set to " + str(NewVolume))
        elif 'Jarvis' in Command and 'new' in Command and 'commands' in Command:
            NewCommand("Asked")             
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
            TryToRecognise(NextLine, ScoreIndexes, Score, Command)

def main():
    print("+ Ready for action sir")
    speak("Ready for action sir")


    while True:
        MachineLearning = defaultdict(list)
        CheckAlarm()
        
        if Interface == "Voice":
            Command = Listen(r)
            print "- " + str(Command)
            KnownCommands(Command, r, NextLine, ScoreIndexes, Score)    
        else:
            Command = str(raw_input("Command: "))
            KnownCommands(Command, r, NextLine, ScoreIndexes, Score)

if __name__ == "__main__":
    main()
        
        
    
                        
                
                    
                
        
