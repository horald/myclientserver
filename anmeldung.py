from __future__ import unicode_literals
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
import time 
import sys
import os

from connected import Connected


class MyClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        serverMSG = data.decode('utf-8')
        if serverMSG[:4] == 'True':
            anzuser=serverMSG[4:]
            print("*** anzuser ***")
            print(anzuser)
            self.factory.app.loginValid(anzuser)
        else:
            self.factory.app.print_message('Server MSG:> ' + serverMSG)


class MyClientFactory(protocol.ClientFactory):
    protocol = MyClientProtocol

    def __init__(self, screen):
        self.app = screen

    def startedConnecting(self, connector):
        self.app.print_message('Verbindung herstellen ...')

    def clientConnectionLost(self, connector, reason):
        self.app.print_message('Verbindung abgebrochen')

    def clientConnectionFailed(self, connector, reason):
        self.app.print_message('Verbindung fehlgeschlagen.')

    def joined(self, channel):
        self.app.print_message('Verbunden: {}'.format(channel))

# A simple kivy Screen,
class Login(Screen):
    connection = None
    currUser = ""

    def removeUser(self):
        print("disconnect User")
        if self.currUser != "" and self.connection:
            delCurrUser = self.currUser + ":" + "Delete"
            self.print_message("Den Benutzer {} am Server abmelden ...".format(self.currUser))
            msgToDel = delCurrUser.encode('utf-8')
            self.connection.write(msgToDel)
        self.resetForm()

        
    def applyLogIn(self, loginField, passwordField):
        msg=""
        if loginField == "":
            msg = "Ungültiger Benutzername."
            self.print_message(msg)
        elif passwordField == "":
            msg = "Passwortfeld hat keinen gültigen Wert."
            self.print_message(msg)
        else:
            if self.connection == None:
                self.connect_to_server()
                
            self.send_message(loginField, passwordField)

    def applyQuit(self):
        msg = "Client beendet das Programm."
        self.print_message(msg)
        sys.exit()

    def loginValid(self, anzuser):        
        self.resetForm()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'
        self.manager.get_screen('connected').SetAnzUser(anzuser)
        
    def loginFailed(self):        
        self.resetForm()
        msg = "Server MSG:> Anmeldung des Benutzers fehlgeschlagen."
        self.print_message(msg)
    
    def send_message(self, user, pw):
        self.currUser = user
        logtext = user + ":" + pw
        if logtext and self.connection:
            self.connection.write(logtext.encode('utf-8'))
            msg = "Verbindung zum Server ok."
            self.print_message(msg)
        else:
            msg = "Verbindung zum Server abgebrochen."
            self.print_message(msg)
            
    def print_message(self, msg):
        if msg != "": 
            if msg[:6] == 'Server':
                self.ids['console'].text += "{}\n".format(msg)
            else:
                self.ids['console'].text += "Login:>  {}\n".format(msg)

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""
        self.ids['console'].text = "Login:>{}\n".format("")
        
    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, MyClientFactory(self))

    def on_connection(self, connection):
        self.connection = connection
        

# A simple kivy App,
class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)
    lb_anzuser = StringProperty("(Anz User)")

    def build(self):
        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        return manager


if __name__ == '__main__':
    LoginApp().run()