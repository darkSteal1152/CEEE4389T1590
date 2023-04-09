from easy_comms import Easy_comms
from time import sleep

com1 = Easy_comms(uart_id=0, baud_rate=9600)
com1.start()

com2 = Easy_comms(uart_id=1, baud_rate=9600)
com2.start()

while True:
    message = ""
    message = com1.read()
    
    mess2 = ""
    mess2 = com2.read()
    
    if message is not None:
        print(f"message received: {message.strip('\n')}")
        print(int(message[-1]))
    sleep(1)
    
    if mess2 is not None:
        print(f"message received: {mess2.strip('\n')}")
        print(int(mess2[-1]))
