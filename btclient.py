# BtEchoClient.py

from btpycom import *  # Standard-Python (PC, Raspi, ...)

def onStateChanged(state, msg):
    global reply
    if state == "CONNECTING":
        print("Connecting", msg)
    elif state == "CONNECTION_FAILED":
        print("Connection failed", msg)
    elif state == "CONNECTED":
        print("Connected", msg)
    elif state == "DISCONNECTED":
        print("Disconnected", msg)
    elif state == "MESSAGE":
        print("Message", msg)
        reply = msg
       
serviceName = "EchoServer"
print("Performing search for service name", serviceName)
client = BTClient(stateChanged = onStateChanged, isVerbose = False)
serverInfo = client.findService(serviceName, 20)
if serverInfo == None:
    print("Service search failed")
else:
    print("Got server info", serverInfo)
    if client.connect(serverInfo, 20):
        anz = input("Anzahl Zeilen? ")
        msg = ""
        for i in range(0,int(anz)):
            inpmsg = input(str(i+1)+". Mitteilung? ")
            msg = msg + inpmsg + "\n"
        print(msg)
        client.sendMessage(msg)        
        client.disconnect()  
#    if client.connect(serverInfo, 20):
#        print("Und noch eine Nachricht")
#        client.sendMessage("Und noch eine Nachricht")        
#        client.disconnect()  

