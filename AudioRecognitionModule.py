# -*- encoding: UTF-8 -*-
# Generalites du robot
NAO_IP = "127.0.0.1"
NAO_PORT = 64534

# Global variable to store the memory module instance
memory = None

from StateManager import *
from naoqi import ALProxy
from naoqi import ALModule
from redball import *

class AudioRecognitionModule(ALModule):

    tts = None
    mot = "Rien"
    cs = 0
    asr = None
    Redballactif = False


    def __init__(self, name):
        global Redball
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")



    def disconnect(self, *_args):
        global asr
        global memory
        if (self.asr != None):

            self.asr.unsubscribe("ALSpeech")
            self.asr = None
            memory.unsubscribeToEvent("WordRecognized","AudioRecognition")
            memory = None
            self.tts = None



    def connect(self, *_args):
        if self.asr != None:
            self.disconnect(self)





        self.tts.setLanguage("Chinese")
        self.tts.say("好吧，让派对开始吧。")


        # Connecting to the Speech recognition module
        self.asr = ALProxy("ALSpeechRecognition",NAO_IP,NAO_PORT)
        # Set the language of recognition to French
        self.asr.setLanguage("Chinese")
        # Enable to make a bip is played at the beginning of the recognition process,
        # and another bip is played at the end of the process.
        self.asr.setAudioExpression(True)

        # The words that have to be recognised by the robot
        wordList=["我们不再玩了","跟着球走","圈套","说你好Nao"]
        # We update the vocabulary list
        # Warning : will crash if the ASR engine is still running
        self.asr.setVocabulary(wordList,False)

        # Says the word that can be recognised
        self.tts.say("可以识别的行为是")
        for index in range(0,len(wordList)):
            self.tts.say(wordList[index])

        # Subscribe to the Wordrecognised event
        self.asr.subscribe("ALSpeech")

        # Subscribe to the Wordrecognised event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("WordRecognized",
            "AudioRecognition",
            "onWordRecognised")


    def onWordRecognised(self, *_args):
        """ This will be called each time a word is recognised.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("WordRecognized","AudioRecognition")

        # We access to the word recognised in the memory
        word = memory.getData("WordRecognized")

        # Debug : Print the word recognised
        print("字：")
        print(word[0])
        print("信心指数：")
        print(word[1])
        print


        # We acknoledge a word if the trust is high enough
        if (word[1] > 0.28):
            self.mot = word[0]
            #self.tts.say("Le mot reconnu est :"+self.mot)
            StateManager(self)


        # Subscribe again to the event
        memory.subscribeToEvent("WordRecognized",
            "AudioRecognition",
            "onWordRecognised")
