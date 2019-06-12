import RPi.GPIO as GPIO

ledPin = 12
sensorPin =11

ispassing = False

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin,GPIO.OUT)
    GPIO.setup(sensorPin, GPIO.IN)

def loop():
    while True:
        if GPIO.input(sensorPin)==GPIO.HIGH:
            GPIO.output(ledPin,GPIO.HIGH)
            ispassing = True
        else:
            GPIO.output(ledPin,GPIO.LOW)
            ispassing = False


def destroy():
    GPIO.cleanup()


if __name__== '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
