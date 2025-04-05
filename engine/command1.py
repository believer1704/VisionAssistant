import pyttsx3
import speech_recognition as sr
import eel
import time  # Import time for sleep functionality

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')  # Send message to front-end
        time.sleep(0.1)  # Add a short delay to ensure the front-end updates
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')  # Send message to front-end
        time.sleep(0.1)  # Add a short delay to ensure the front-end updates
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(f'You said: {query}')  # Send recognized text to front-end
        time.sleep(2)
        
    except Exception as e:
        print("Sorry, I didn't catch that. Could you please repeat?")
        eel.DisplayMessage("Sorry, I didn't catch that. Could you please repeat?")  # Handle errors
        print(f"Error: {e}")
        return ""

    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        
    else:
        query = message
        
    try:
         
        if "open" in query:
            from engine.features1 import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features1 import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features1 import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)    
        
        else:
            from engine.features1 import chatBot
            chatBot(query)
        
    except:    
            print("error")
    
    eel.Showhood()    



