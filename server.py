from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor
from twisted.internet import protocol
import sys


class MyServer(protocol.Protocol):

    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class MyServerFactory(protocol.Factory):
    protocol = MyServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class TwistedServerApp(App):
    label = None
    label2 = None
    users = {
        "steffen":"123",
        "horst":"123",
        "chris":"123",
        "frieda":"123"
        }
    userOnline = []


    def build(self):
        
        def applyServerQuit(instance):
            sys.exit(0)
            
        PORT = 8000
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Server wurde auf Port {} gestartet.\n".format(PORT))
        self.label2 = Label(text="Benutzer:\n", color=(0, 1, 0, 1))
        self.my_output = Label(text_size= (None,None),
                          pos_hint={'center_x': 0.5, 'center_y': .95},
                          size_hint_y=None,
                          size = (20,64),
                          height = 64,
                          halign="center",
                          valign = "middle",)
        button = Button(text='Beenden')
        button.bind(on_press=applyServerQuit)                          
        layout.add_widget(button, index=1)
        layout.add_widget(self.label, index=2)
        layout.add_widget(self.label2, index=3)
        layout.add_widget(self.my_output, index=4)
        reactor.listenTCP(PORT, MyServerFactory(self))
        self.my_output.text += "Server listening...\n"
        return layout


    def handle_message(self, clientMsg):
        cMsg = clientMsg.decode('utf-8')
        msgArray = cMsg.split(':')
        self.label.text = "Empfangen:  {}\n".format(cMsg)
        userName = msgArray[0]
        clientCmd = msgArray[1]
        if clientCmd == "Message":
            res = "Msg:"+userName
            self.my_output.text += format(userName)
            return res.encode('utf-8')
        if clientCmd == "Delete":
            self.delUser(userName)
            res = "Benutzer {} ist vom Server abgemeldet.".format(userName)
            self.label.text += "Server: {}\n".format(res)
            self.my_output.text += "Benutzer {} hat sich abgemeldet\n".format(userName)
            return res.encode('utf-8')
        if userName in self.userOnline:
            res = "Der Benutzer {} ist schon angemeldet.".format(userName)
            self.label.text += "Server: {}\n".format(res)
            return res.encode('utf-8')
        if userName in self.users:
            res = "Der Benutzer {} ist registriert.".format(userName)
            self.label.text += "Server: {}\n".format(res)
            if self.users[userName] == msgArray[1]:
                res = "Benutzername und Passwort sind korrekt."
                self.label.text += "Server: {}\n".format(res)
                self.my_output.text += "Benutzer {} hat sich angemeldet\n".format(userName)
                self.addUser(userName) 
                anzuser=len(self.userOnline)
                self.my_output.text += "Es haben sich {} Benutzer angemeldet\n".format(anzuser)
                ok = 'True'+str(anzuser)
                return ok.encode('utf-8')
            else:
                res = "Passwort ist falsch."
                self.label.text += "Server: {}\n".format(res)
                return res.encode('utf-8')
        else:
            err = "Kein Benutzer mit dem Namen {} registriert.".format(userName)
            self.label.text += "Gesendet: {}\n".format(err)
            return err.encode('utf-8')
        
    def addUser(self, usern):
        print("Add user")
        self.label2.text = "Benutzer:\n"
        self.userOnline.append(usern)
        for u in self.userOnline:
            self.label2.text += "{}\n".format(u)
        
    def delUser(self, user):
        print("Remove user")
        self.label2.text = "Benutzer:\n"
        self.userOnline.remove(user)
        for u in self.userOnline:
            self.label2.text += "{}\n".format(u)

if __name__ == '__main__':
    TwistedServerApp().run()
