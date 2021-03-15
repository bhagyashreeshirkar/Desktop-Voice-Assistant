import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import pywhatkit
import wikipedia
from translate import Translator
import smtplib
from datetime import datetime
import pyjokes
from pygame import mixer
import os
import winshell

engine = pyttsx3.init()  # initialize pyttsx3 function
voices = engine.getProperty('voices')  # gets the current value
engine.setProperty('voice', voices[1].id)  # It sets the property of female voice from python voices[0=male, 1=female]
engine.setProperty('rate', 180)  # It'll speak 180 words in 1 minute


def talk(audio):
    engine.say(audio)  # It will make a voice assistant speak
    engine.runAndWait()


def wish_me():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        talk("Good Morning!")
    elif 12 <= hour < 18:
        talk("Good Afternoon!")
    else:
        talk("Good Evening!")

    talk('I am your digital assistant! what can I do for you?')


def take_command():
    r = sr.Recognizer()  # r is an object used to recognize your voice
    with sr.Microphone() as speech:  # the microphone module is used for listening the commands
        print('Listening...')
        r.adjust_for_ambient_noise(speech)  # It removes ambient noise
        r.pause_threshold = 1  # seconds of non-speaking audio before a phrase is considered complete
        r.energy_threshold = 400  # the threshold value removes extreme background noises
        voice = r.listen(speech)
    try:
        print('Recognizing...')
        command = r.recognize_google(voice)
        print(f'User said: {command}\n')
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        time.sleep(10)
        command = take_command().lower()
    return command


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Extended HELO(EHLO) is an Extended Simple Mail Transfer Protocol (ESMTP) command sent by an email server to
    # identify itself when connecting to another email server to start the process of sending an email.
    server.ehlo()
    # StartTLS is a protocol command used to inform the email server that the
    # email client wants to upgrade from an insecure connection to a secure one using TLS or SSL.
    server.starttls()
    talk('tell me your email id')
    your_id = input()
    talk('tell me the password')
    password = input()
    server.login(your_id, password)
    server.sendmail(your_id, to, content)
    server.close()


def run():
    command = take_command().lower()  # taking the command from user

    if 'pause' in command or 'wait' in command:
        talk('No problem! How many seconds shall I wait?')
        command = take_command().lower()
        talk('waiting')
        time.sleep(int(command))

    elif 'google' in command:
        talk('Opening google')
        webbrowser.open_new_tab('www.google.com')
        time.sleep(5)

    elif 'where is' in command:
        location = command.replace('where is', '')
        location_url = "https://www.google.com/maps/place/" + location + ''
        talk('Hold on, I will show you where' + location + 'is.')
        webbrowser.open(location_url)  # It'll show the location of a particular place
        time.sleep(5)

    elif 'play' in command:
        song = command.replace('play', '')
        talk('Playing' + song)
        pywhatkit.playonyt(song)  # It'll play the song on the youtube, playonyt = play on youtube
        time.sleep(5)

    elif 'news' in command:
        talk('Here are some headlines from the Times of India, Happy reading!')
        # It'll fetch top headline news from Time of India by using the web browser function
        webbrowser.open_new_tab('https://timesofindia.indiatimes.com/home/headlines')
        time.sleep(5)

    elif 'wikipedia' in command:
        talk('Searching Wikipedia')
        source = command.replace('wikipedia', '')
        get_info = wikipedia.summary(source, sentences=4)
        talk('According to wikipedia')
        print(get_info)
        talk(get_info)  # It'll' speak information from Wikipedia

    elif 'translate' in command:
        talk('To which language you want to translate?')
        command = take_command().lower()
        translator = Translator(from_lang="english", to_lang=command)
        talk('Say the text')
        sentences = take_command().lower()
        translation = translator.translate(sentences)
        talk('Your translation is displayed.')
        print(translation)
        time.sleep(5)  # It'll translate the statements and print translation

    elif 'send a mail' in command or 'email' in command:
        try:
            talk('What should I say?')
            content = take_command()
            talk('To whom I send?')
            to = input()
            send_email(to, content)
            talk('Email has been sent!')
        except Exception as e:
            print(e)
            talk('Sorry, I am not able to send this Email')

    elif 'time' in command:
        current_time = datetime.now().strftime("%I %M %p")  # 12-hour format and %p is for pm or am
        talk('Current time is ' + current_time)

    elif 'date' in command:
        current_date = datetime.now().strftime("%B %d, %Y")  # textual month, day and year format
        talk('Current date is' + current_date)

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)  # It'll speak random inbuilt python jokes

    elif 'music' in command:
        # first, it opened the music directory and then listed all the songs present in the directory.
        # then asks for the song name and plays that song
        music_dir = "C:\\Users\\Rsc\\Music"
        songs = os.listdir(music_dir)
        print(songs)
        time.sleep(5)
        talk('Which song do you want to hear?')
        command = take_command().lower()
        if 'song' in command:
            mixer.init()
            song_name = command.replace('song ', '')
            talk('Playing song' + song_name)
            name = song_name.capitalize() + '.mp3'
            print(name)
            mixer.music.load('C:\\Users\\Rsc\\Music\\' + name)
            mixer.music.play()
        else:
            talk('sorry! This song is not there on your personal computer.')

    elif 'documents' in command or 'files' in command:
        ide_path = 'C:\\Users\\Rsc\\Documents'
        os.startfile(ide_path)  # It'll open a document folder from your personal computer
        time.sleep(5)

    elif 'create folder on desktop' in command:
        talk('Creating a folder')
        talk('Which name should I give to the folder?')
        command = take_command().lower()
        new_path = 'C:\\Users\\Rsc\\Desktop\\' + command
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        talk('Folder has been created!')

    elif 'empty recycle bin' in command:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        talk('Recycle Bin Recycled')

    elif 'shutdown system' in command:
        talk("Hold On a Sec ! Your system is on its way to shut down")
        os.system('shutdown /s')

    elif 'restart system' in command:
        talk("Hold On a Sec ! Your system is on its way to restart")
        os.system('shutdown /r')

    elif 'sleep' in command or 'hibernate' in command:
        talk('Hibernating')
        os.system('shutdown /h')

    elif 'exit' in command or 'turn off' in command or 'stop' in command:
        talk('Thanks for giving me your time! Have a good day.')
        exit()  # It'll exit the program

    else:
        temp = command.replace('', '')
        g_url = 'https://www.google.com/search?q='
        talk("Sorry, I can't understand, but I can search on the internet to give you an answer.")
        talk("Do you want me to google that for you?")
        command = take_command().lower()
        if 'yes' in command:
            talk('Right away,Created new window in existing browser session.')
            webbrowser.open_new_tab(g_url + temp)
        else:
            talk('How can i help you?')


if __name__ == '__main__':
    wish_me()
    while True:
        run()
