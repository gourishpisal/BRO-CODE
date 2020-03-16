from gtts import gTTS
import speech_recognition as sr
import re
import time
import webbrowser
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import requests
from pygame import mixer
import urllib.request
import urllib.parse
import bs4


def talk(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
#         audio.splitlines(): splitline() is a string method. 
#         The splitlines() method splits the string at line breaks and returns a list of lines in the string.

        text_to_speech = gTTS(text=audio, lang='en-uk')
#         gTTS is the function from gtts library. Which is used for converting text to speech. 
#         gTTS: Here two arguments are are given to gTTS function i.e. text = Which is a text to be converted in 
#         speech. and lang = The reference language provided.
#         https://gtts.readthedocs.io/en/latest/module.html

        text_to_speech.save('audio.mp3')
#         Here we are saving the converted audio as MP3 file.

        mixer.init()
#         https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.init
#         This is a function imported from library pygame.
#         This function is used for initializing the mixer module for Sound loading and playback.

        mixer.music.load("audio.mp3")
#         This will load a music filename/file object and prepare it for playback.
#         If a music stream is already playing it will be stopped.
#         This does not start the music playing.

        mixer.music.play()
#         This will play the loaded music stream.
#         If the music is already playing it will be restarted.
#         https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.play

def myCommand():
    "listens for commands"
    #Initialize the recognizer
    #The primary purpose of a Recognizer instance is, of course, to recognize speech.
    
    r = sr.Recognizer()
#     Here we are creating Recognition instance for speech recogniton with named variable "r"
#     This Recognizer is the class from SpeechRecognition API Library. 
#     It is library for performing speech recognition, with support for several engines and APIs,online and offline.
#     (https://pypi.org/project/SpeechRecognition/)
#     All of the magic in SpeechRecognition happens with the Recognizer class.
#     The primary purpose of a Recognizer instance is to recognize speech. 
#     (https://realpython.com/python-speech-recognition/#the-recognizer-class)

    with sr.Microphone() as source:
        Here we are creating microphone instance to listen from.
        And we are using the default microphone as the audio source.
        We have started default microphone as source
        print('Bro is Ready...')
        r.pause_threshold = 1
#         This is a method of Recognizer class to give a pause
#         wait for a second to let the recognizer adjust the
#         energy threshold based on the surrounding noise level

        r.adjust_for_ambient_noise(source, duration=1)
#         Adjusts the energy threshold dynamically using audio from source 
#         (an AudioSource instance) to account for ambient noise.
#         Intended to calibrate the energy threshold with the ambient energy level. 
#         Should be used on periods of audio without speech - will stop early if any speech is detected.
#         The duration parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning. 
#         This value should be at least 0.5 in order to get a representative sample of the ambient noise.
        
        audio = r.listen(source)
#         listens for the user's input
#         https://pypi.org/project/SpeechRecognition/1.3.0/
        print('analyzing...')

    try:
        command = r.recognize_google(audio).lower()
#         recognize_google() is method from Recognizer class which takes and provides an audio input to google speech API
#         Here we are giving "audio" which is we already recorded in r.listen(source) and also we are providing lower threshold
        print('You said: ' + command + '\n')
        time.sleep(2)
#         It will take pause for 2 seconds

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
#         sr.UnknownValueError is the error when audio we provided is not understandable, that it can not understand it
        print('Your last command couldn\'t be heard')
        command = myCommand();
#         Here we used recursion, that it is giving error when audio is not understandable it wiil run this function

    return command
#     Returning given audio input as text

# This function takes input "command" which is generated/returned from myCommand() function
def BRO(command):
    errors=[
        "I didnot get you",
        "sorry i am not supose to do this",
        "can you repeat it",
        "",
    ]
#     This is list of errors which will get if we have given wrong audio input

    "if statements for executing commands"
    # Search on Google
    if 'open google and search' in command:
        reg_ex = re.search('open google and search (.*)', command)
#         re.search will search for the pattern defined, this is regular expression function.
        
        search_for = command.split("search",1)[1]
#         if we got the given pattern in command provided then it will be splitted to search.
#         eg. "open google and search abcd" then ["open google and", "abcd"]
        
        print(search_for)
        url = 'https://www.google.co.in/search?q=' + search_for
#         here we are joining the url link and search term provided by user
        if reg_ex:
            subgoogle = reg_ex.group(1)
#             here group 1 means the 1st index element of list ["open google and", "abcd"] that is "abcd"
            url = url + 'r/' + subgoogle
    
        talk('Okay!')
#         This (talk) function we defined earlier. Here we are giving input to it.
#         That function will convert text to speech

        webbrowser.open('https://www.google.co.in/search?q=' + search_for)
#         open is the function from webbrowser library that opens default web browser for us with url given

        driver.get('https://www.google.com')
#         gets given url link to browser with selenium. SEARCH AND READ ABOUT SELENIUM
#         https://selenium-python.readthedocs.io/getting-started.html
#         function from selenium.
#         Selenium is a portable framework for testing web applications. Selenium provides a
#         playback tool for authoring functional tests without the need to learn a test scripting language.

        search = driver.find_element_by_name('q')
#         We are creating a "search" variable to getting search "q" that is "q" stands for querry in google search URL.
#         Used to locating the element

        search.send_keys(str(search_for))
#         We are sending keys, this is similar to entering keys using your keyboard.
#         Special keys can be sent using Keys class imported from selenium.

        search.send_keys(Keys.RETURN)
#         Hit return after you enterarch text

# Send Email
    elif 'email' in command:
        talk('What is the subject?')
#         It will speak for 'What is the subject?' and argument given to talk function

        time.sleep(3)
#         Wait for 3 seconds
        
        subject = myCommand()
#         After waiting we can give audio command as a subject for email

        talk('What should I say?')
        message = myCommand()
        content = 'Subject: {}\n\n{}'.format(subject, message)
#         I am not explaining this because it is general topic which can be asked anywhere
#         Please read about string formatting methods

        #init gmail SMTP
        mail = smtplib.SMTP('smtp.gmail.com', 587)
#         Search for what is SMTP protocol. and other protocols used for sending email communication
#         Also search and read little bit about TCP, HTTP, HTTPS protocols
#         https://docs.python.org/3/library/smtplib.html

        mail.ehlo()
#         identify to server
#         That is connecting to server as you are getting to server of gmail.com i.e. 'smtp.gmail.com'

        mail.starttls()
#         encrypt session
#         Put the SMTP connection in TLS (Transport Layer Security) mode.
#         All SMTP commands that follow will be encrypted. 

        mail.login('your_mail', 'your_mail_password')
#         Log in on an SMTP server that requires authentication.
#         The arguments are the username and the password to authenticate with.
#         If there has been no previous EHLO or HELO command this session, this method tries ESMTP EHLO first.

        mail.sendmail('FROM', 'TO', content)
#         This function is used to send mail to Recipient with Your address
#         This creates mail as an envelop and send it to SMTP server with given address

        mail.close()
#         This function close the connection with SMTP server, that means you will be logged out after it.
#         If it gives error then try for mail.quit

        talk('Email sent.')
#         This will tell us that mail is sent to given address

# THIS PART WORK JUST AS WE SEARCHED GOOGLE IN FIRST PART OF FUNCTION
# search in wikipedia (e.g. Can you search in wikipedia apples)
    elif 'wikipedia' in command:
        reg_ex = re.search('wikipedia (.+)', command)
        if reg_ex:
            query = command.split("wikipedia",1)[1]
            response = requests.get("https://en.wikipedia.org/wiki/" + query)
            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')
                title = html.select("#firstHeading")[0].text
                paragraphs = html.select("p")
                for para in paragraphs:
                    print (para.text)
                intro = '\n'.join([ para.text for para in paragraphs[0:3]])
                print (intro)
                mp3name = 'speech.mp3'
                language = 'en'
                myobj = gTTS(text=intro, lang=language, slow=False)
                myobj.save(mp3name)
                mixer.init()
                mixer.music.load("speech.mp3")
                mixer.music.play()
    elif 'stop' in command:
        mixer.music.stop()

# Search videos on Youtube and play (e.g. Search in youtube believer)
    elif 'youtube' in command:
        talk('Ok!')
        reg_ex = re.search('youtube (.+)', command)
        if reg_ex:
            domain = command.split("youtube",1)[1]
#             Here we will get what we want to search by splitting string and getting 1st element of the list
            
            query_string = urllib.parse.urlencode({"search_query" : domain})
#             This will encode i.e. convert the string to ASCII text string.
#             Which will used for search
            
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
#             This will join the search term with youtube url and open in address bar of browser
            
            
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
#             Checking the results URL if there is the given term is available or not.
#             If it is available then it will split it to given pattern then it will proceed
            
            
            #print("http://www.youtube.com/watch?v=" + search_results[0])
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
#             It is as we opened the browser in last part
            
            pass

# This will go to next part if we are not provided right term command
    elif 'hello' in command:
        talk('hi its bro how can i help you')
        time.sleep(3)
    elif "what can you do for me" in command:
        talk('i can do anything u ask  me for')
        time.sleep(3)
    elif 'how is weather today' in command:
        talk('its hot because of you ')
        time.sleep(3)
    elif 'I love you' in command:
        talk('sorry i have a boyfriend')
        time.sleep(3)
    else:
        error = random.choice(errors)
#         Random is the library with which we can select random element from given list or any sequence

        talk(error)
        time.sleep(3)
