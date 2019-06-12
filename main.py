import lcd_multithread
import time
import threading
import dht
str1 = "this is main, reee  "
str2 = "hello world, i want die. "
str3 = "this is the final message, good bye world. "

x = threading.Thread(target=lcd_multithread.LCDprint,args=(str1,))
x.start()
time.sleep(5)

a,b=dht.dht_GetData()
str = "Humidity : %.2f, Temperature : %.2f "%(a,b)
lcd_multithread.updateString(str)
time.sleep(5)
a,b=dht.dht_GetData()
str = "Humidity : %.2f, Temperature : %.2f "%(a,b)
lcd_multithread.updateString(str)
x.join()
