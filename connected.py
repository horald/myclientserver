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
        
    def SetAnzUser(self):
        stranzuser="Anzahl User:"+self.manager.get_screen('login').getAnzUser()        
#        stranzuser="Anzahl User:"        
        return stranzuser 