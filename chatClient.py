import socket,sys,threading

HOST='192.168.1.89'
PORT=46000


# ====== Prototype de chat dans un réseau local ======

# ****** Programme client ******

class threadReception(threading.Thread):
    """Thread gérant la réception des messages"""
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.connexion=conn  #Référence du socket de connexion
        self.event=threading.Event()  #Gestionnaire du thread en cours

    def stop(self):
        self.event.set()


    def run(self):
        while 1:
            msg_recu=self.connexion.recv(1024).decode("Utf8")  #Réception d'un message
            print(msg_recu)
            if not msg_recu or msg_recu.upper()=="FIN":
                break

        #Le thread reception s'arrete ici
        self.stop()
        print("Client arreté, connexion perdue")
        self.connexion.close()  #La fermeture du thread entraine celui de la connexion en cours

class threadEmission(threading.Thread):
    """Thread gérant l'émission des messages"""
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.connexion=conn

    def run(self):
        while 1:
            msg_emis=input( "Entrez votre message ici : \n")
            self.connexion.send(msg_emis.encode("Utf8"))

#=====Programme principale - Etablissement de la connexion =====
connexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    connexion.connect((HOST,PORT))
except socket.error as err:
    print("****** Connexion au serveur échouée ******")
    print("Erreur : %s "%err)
    sys.exit()
print("****** Connexion au serveur réussie ******")

#Dialogue avec le serveur et lancement de deux threads

th_E=threadEmission(connexion)
th_R=threadReception(connexion)
th_E.start()
th_R.start()
