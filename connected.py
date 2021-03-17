from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

class Connected(Screen):
    def logOff(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        # Gibt das Screen-Widget-Objekt zurück, das dem Namen zugeordnet ist, oder 
        # löst eine ScreenManagerException aus, wenn es nicht gefunden wurde.
        # Über das Screen-Widget-Objekt kann eine Methode des Objekts aufgerufen werden
        self.manager.get_screen('login').removeUser()

    def SendMsg(self):
        msg=self.ids['nachricht'].text
        print(msg)
        self.manager.get_screen('login').SendMsg(msg)
        
    def SetAnzUser(self, anzuser):
        stranzuser="Anzahl User:"+format(anzuser)
        self.ids['anzuser'].text=stranzuser        
