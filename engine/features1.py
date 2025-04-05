import os
from shlex import quote
import sqlite3
import struct
import subprocess
import webbrowser
from playsound import playsound
import eel
import pyautogui
from engine.command1 import *
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import re
from engine.helper import extract_yt_term
import pvporcupine
import pyaudio

from hugchat import hugchat


conn = sqlite3.connect('vision2.db')
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    # Use absolute path for testing
    music_dir = r"C:\Users\aditya\OneDrive\Desktop\vision2\www\assets\audio\the-sound-that-siri-iphone-makes-when-she-listens.mp3"
    
    # Check if file exists
    if not os.path.isfile(music_dir):
        print(f"File not found: {music_dir}")
        return

    print(f"Attempting to play sound from: {music_dir}")
    try:
        playsound(music_dir)
    except Exception as e:
        print(f"Error playing sound: {e}")


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()
    
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")



def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term) 


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



    # Whatsapp Message Sending
def findContact(query):
    # Define the words to remove
    words_to_remove = ['ASSISTANT_NAME', 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    
    # Remove specified words from the query
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
            ('%' + query + '%', query + '%')
        )
        results = cursor.fetchall()

        if results:
            print(results[0][1])
            mobile_number_str = str(results[0][1])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, query
        else:
            speak('Not found in contacts')
            return 0, 0
    except Exception as e:
        print(f"Error: {e}")
        speak('An error occurred while finding the contact')
        return 0, 0

# Helper function to remove words
def remove_words(query, words_to_remove):
    for word in words_to_remove:
        query = query.replace(word, '').strip()
    return query


def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

#chat bot
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
