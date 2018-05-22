# -*- encoding: UTF-8 -*-
# Fonction qui gère la machine à états, elle est appelée à chaque fois qu'un mot est reconnu
import time
from main import *
RedBall = None

def StateManager(AudioRecognition):
	global RedBall
	MotReconnu = AudioRecognition.mot
	tts = AudioRecognition.tts
	Redball = None
	motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)

	if AudioRecognition.Redballactif == False:
		RedBall = RedBallRecognitionModule("RedBall")
		AudioRecognition.Redballactif = True



	if (MotReconnu == "说你好Nao"):
		tts.say("你好")
		print "Current State :"
		print AudioRecognition.cs

	if (MotReconnu == "跟着球走"):
		if (AudioRecognition.cs == 0):
			tts.say("我听从你的命令")
			AudioRecognition.cs = 1
			RedBall.connect(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 1):
			tts.say("我是一个白痴!")
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 2):
			tts.say("好吧，我不再试着抓住他了。")
			AudioRecognition.cs = 1
			RedBall.disconnect(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return

	if (MotReconnu == "圈套"):
		if ( AudioRecognition.cs == 1):
			tts.say("D'accord je vais essayer de l'attraper好吧，我试着抓住他。")
			AudioRecognition.cs = 2
			RedBall.grabTarget(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 2):
			tts.say("J'essaye déjà de l'attraper mongol我已经试着去抓蒙古了。")
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 0):
			tts.say("Fais moi d'abord suivre la balle先让我跟着球。")
			print "Current State :"
			print AudioRecognition.cs
			return


	if (MotReconnu == "我们不再玩了"):
			motionProxy.setStiffnesses("Body",0)
			tts.say("一切正常")
			AudioRecognition.cs = 0
			RedBall.disconnect(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return


	if AudioRecognition.cs == 0:

		RedBall.disconnect(RedBall)
