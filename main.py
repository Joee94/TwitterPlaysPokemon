import pywinauto
import threading
import time
import random
import win32api
import win32con
from win32api import *
from twython import *
from pywinauto.application import Application

def doEverything(app):	#seperate function so loading only happens when the code is first loaded, although I should change it so the app is checked if it's active instead but whatever

	twitter = authorisation()	#logs me into twitter essentially
	reply = lastReply(twitter)	#gets the last reply
	#reply = debug()
	command = searchForCommand(reply)	#checks the tweet for the command, and converts it to a string
	sendToGame(command, app)	#sends the command to the game
	takeScreenshot(app)	#takes a screenshot
	createTweet(reply, twitter)

	threading.Timer(240, doEverything, args =(app,)).start()	#Calls this every 2 minutes

def loadGame():
	app = Application.start("C:\Users\Joee94\Documents\VisualBoyAdvance-1.8.0-beta3\VisualBoyAdvance.exe")	#Starting the emulator
	app.VisualBoyAdvance.MenuSelect('File->Open')	#Clicking open

	window = pywinauto.timings.WaitUntilPasses(10, 0.5, lambda: app.window_(title=u'Select ROM'))	#Waiting until the correct window is open
	ctrl = window['ComboBox2']
	ctrl.ClickInput()
	ctrl.TypeKeys("PokemonRed.gb")
	ctrl = window['&Open']
	ctrl.Click()	#bleh bleh the last few lines are just opening the file big whoop
	return app

def authorisation():	#put your keys here
	apikey		= ''
	apisecret	= ''
	oauthtoken	= ''
	oauthsecret	= ''

	twitter = Twython(apikey, apisecret, oauthtoken, oauthsecret)
	return twitter

def lastReply(twitter):	
	user_tweets = twitter.get_mentions_timeline(count = 1)	#just finding one
	
	for tweet in user_tweets:	#can't figure out how to do this without a for loop because im a bad programmer
		username = tweet['user']['screen_name'].encode('utf-8')	#getting the username, encoding it
		body = tweet['text'].encode('utf-8')	#getting the actual tweet
	bodyChars = list(body)

	fullTweet = 'RT @' + username + ' "' + body + '" #twitterplayspokemon'	#piecing it together for later
	tweetLen = len(fullTweet)

	if(tweetLen > 115):
		for i in range(0, len(bodyChars)):
			if i > 66 and i < 70:
				bodyChars[i] = "."
			elif i > 69:
				bodyChars[i] = ""

	body = ''.join(bodyChars)
	fullTweet = 'RT @' + username + ' "' + body + '" #twitterplayspokemon'	#body changed so I'm updating it, bleh its bad but it should work
	return fullTweet

def debug():
	command = raw_input()
	return command

def searchForCommand(lastReply):
	replyFile = open('reply.txt', 'r')	#just checking if no ones replied since the last tweet 
	if(lastReply in replyFile):
		return "Contained"

	lastReply = lastReply.lower()	#converting the tweet to lower case

	print lastReply

	if ' up' in lastReply:	#there are no case statements in python I know there is another way but bleh this'll do who cares
		return 'w'
	elif ' down' in lastReply:
		return 's'
	elif ' left' in lastReply:
		return 'a'
	elif ' right' in lastReply:
		return 'd'
	elif ' a ' in lastReply or 'a"' in lastReply or '"a"' in lastReply or "'a'" in lastReply:
		return 'z'
	elif ' b ' in lastReply or 'b"' in lastReply or '"b"' in lastReply or "'b'" in lastReply:
		return 'x'
	elif ' start' in lastReply:
		return 'n'
	elif ' select' in lastReply:
		return 'm'
	else:
		return "No Command"

def sendToGame(command, app):	#just sending the input to the game
	time.sleep(3)	#wait a sec incase it's all flashy and weird yknow
	command = str(command)
	app.VisualBoyAdvance.SetFocus()
	if command == "Contained":
		pass
	elif command == "No Command":
		pass
	else:
		press(command)
		press('F1')

	print command

def takeScreenshot(app):
	time.sleep(3)	#wait a sec incase it's all flashy and weird yknow
	counterFile = open ('counter.txt', 'r')	#opening the counter and reading what it is
	counterStr = str(counterFile.read())
	counterInt = int(counterStr)
	print counterStr, " ", counterInt	#bit of debugging info here 
	saveLocation = "^a C:\Users\Joee94\Documents\Uni\Summer\TwitterPlaysPokemon\TwitterPlaysPokemon\Screenshots\\" + counterStr	#Put your Screenshot folder here

	time.sleep(3)	#wait a sec incase it's all flashy and weird yknow
	app.VisualBoyAdvance.MenuItem(u'&File').Click()
	app.VisualBoyAdvance.MenuItem(u'&File->S&creen capture...').Click()	#clicking the save screenshot button

	window = pywinauto.timings.WaitUntilPasses(10, 0.5, lambda: app.window_(title=u'Select screen capture name'))	#Waiting until the correct window is open
	ctrl = window['ComboBox2']
	ctrl.ClickInput()
	ctrl.TypeKeys(saveLocation)
	ctrl = window['&Save']
	ctrl.Click()	#saving it and whatever

def createTweet(reply, twitter):	#tweeting it
	counterFile = open ('counter.txt', 'r')	#checking which image to tweet 
	counterStr = str(counterFile.read())
	counterInt = int(counterStr)

	screenshotLocation = "C:\Users\Joee94\Documents\Uni\Summer\TwitterPlaysPokemon\TwitterPlaysPokemon\Screenshots\\" + counterStr + ".png"	#Your screenshot folder again

	screenshot = open(screenshotLocation, 'rb')
	twitter.update_status_with_media(status= reply, media= screenshot)	#updating the status

	counterInt += 1	#incrementing the counter
	counterFile = open ('counter.txt', 'w')
	counterFile = counterFile.write(str(counterInt))	#saving it
	
	replyFile = open('reply.txt', 'w')	#saving the tweet to file for later
	replyFile.write(reply)

VK_CODE = {
'a':0x41,
'd':0x44,
'm':0x4D,
'n':0x4E,
's':0x53,
'w':0x57,
'x':0x58,
'z':0x5A,
'left_shift':0xA0,
'F1':0x70,
}

def press(*args):
	'''
	press, release
	eg press('x', 'y', 'z')
	'''
	print args
	for i in args:
		win32api.keybd_event(VK_CODE[i], 0, 0, 0)
		time.sleep(0.2)
		win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
		print VK_CODE[i]

def main():
	app = loadGame()	#Do a check before loading this tho
	doEverything(app)

if __name__ == "__main__":
	main()
