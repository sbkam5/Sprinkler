import RPi.GPIO as GPIO
import time

relayPin = 40    # define the relayPin
buttonPin = 12    # define the buttonPin
debounceTime = 50

def setup():
	print ('Program is starting...')
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(relayPin, GPIO.OUT)   # Set relayPin's mode is output
#	GPIO.setup(buttonPin, GPIO.IN)

def loop():
	relayState = False
	lastChangeTime = round(time.time()*1000)
	buttonState = GPIO.HIGH
	lastButtonState = GPIO.HIGH
	reading = GPIO.HIGH
	while True:
		reading = GPIO.input(buttonPin)
		if reading != lastButtonState :
			lastChangeTime = round(time.time()*1000)
		if ((round(time.time()*1000) - lastChangeTime) > debounceTime):
			if reading != buttonState :
				buttonState = reading;
				if buttonState == GPIO.LOW:
					print("Button is pressed!")
					relayState = not relayState
					if relayState:
						print("Turn on relay ...")
					else :
						print("Turn off relay ... ")
				else :
					print("Button is released!")
		GPIO.output(relayPin,relayState)
		lastButtonState = reading

def test():
	GPIO.output(relayPin,GPIO.HIGH)
	time.sleep(10)
	GPIO.output(relayPin,GPIO.LOW)
	time.sleep(10)
	GPIO.output(relayPin,GPIO.HIGH)
	time.sleep(5)
	GPIO.output(relayPin,GPIO.LOW)
	time.sleep(5)
	destroy()

def on():
	GPIO.output(relayPin, GPIO.LOW)

def off():
	GPIO.output(relayPin, GPIO.HIGH)

def destroy():
	GPIO.output(relayPin, GPIO.LOW)     # relay off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		test()
	except KeyboardInterrupt:
		destroy()
