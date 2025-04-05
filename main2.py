import os
import eel

# Import functions from features and command modules
from engine.features1 import playAssistantSound
from engine.command1 import *  # Make sure to specify the functions or classes you're using from this module

def start():


    eel.init("www")


    playAssistantSound()


    os.system('start msedge.exe --app="http://localhost:8000/index2.html"')

    
    eel.start('index2.html', mode=None, host='localhost', block=True)


