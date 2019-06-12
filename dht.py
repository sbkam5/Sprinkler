
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
DHTPin = 38     #define the pin of DHT11
GPIO.setwarnings(False)
def loop():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    sumCnt = 0              #number of reading times
    while(True):
        sumCnt += 1         #counting number of reading times
        chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        print ("The sumCnt is : %d, \t chk    : %d"%(sumCnt,chk))
        if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            print("DHT11,OK!")
        elif(chk is dht.DHTLIB_ERROR_CHECKSUM): #data check has errors
            print("DHTLIB_ERROR_CHECKSUM!!")
        elif(chk is dht.DHTLIB_ERROR_TIMEOUT):  #reading DHT times out
            print("DHTLIB_ERROR_TIMEOUT!")
        else:               #other errors
            print("Other error!")

        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
        time.sleep(2)

def dht_GetData():
    dht = DHT.DHT(DHTPin)
    cond = True
    while(cond):
        chk =dht.readDHT11()
        if(chk is dht.DHTLIB_OK):
            print("DHT11, OK!")
            print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
            return dht.humidity,dht.temperature;
            cond = False
        else:
            print("error, Getting data again...")
            time.sleep(2)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
