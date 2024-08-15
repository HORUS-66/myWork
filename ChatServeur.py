import socket,sys,threading

HOST='192.168.1.89'
PORT=46000


# ====== Prototype de chat dans un réseau local ======

# ****** Programme serveur ******
class threasServeur(threading.Thread):
    """Classe gérant les requetes de connexion provenant des clients"""
    def __init__(self,conn,nomClient):
        threading.Thread.__init__(self,name=nomClient)
        self.connexion=conn

    def run(self):
        #Dialoguer avec le client en cours
        while 1:
            msgClient=self.connexion.recv(1024).decode("Utf8")
            #Sorti de la boucle si l'une des conditions est vraie
            if not msgClient or msgClient.upper()=="FIN":
                break
            message="%s > %s "%(self.name,msgClient)
            print(message)
            for cle in conn_client:  #Parcous de chaque thead en cours
                if cle != self.name:      #Ne pas renvoyer le message à l'emeteur
                    conn_client[cle].send(message.encode("Utf8"))

        #Fermeture de la connexion
        self.connexion.close()   #Couper la connexion coté serveur
        del conn_client[nom]  #Supprimer sa référence dans le dictionnaire de connexion client
        print("client %s déconnecté "%self.name)

# Initialisation du serveur et mise en place du socket
mySocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Liaison avec la machine physique
try:
    mySocket.bind((HOST,PORT))
except socket.error as err:
    print("****** La liaison du socket a échouée ******")
    print("Erreur : %s "%err)
    sys.exit()
print("****** Liaison au socket réussie ******")

mySocket.listen(5)  #Il peut gérer 5 threads

#Attente et prise en charge des connexions demandés par des clients

conn_client={}
while 1:
    connexion,adresse = mySocket.accept()  #Attente des requetes de connexion
    #Demande du nom du client
    msgSer="Veuillez entrer votre nom : "
    connexion.send(msgSer.encode("Utf8"))  #Envoie du message au client
    nom=connexion.recv(1024).decode("Utf8")

    th=threasServeur(connexion,nom)  #Création d'un nouvel objet thread pour gérer la connexion
    th.start()
    #Mémoriser la connexion dans le dictionnaire
    id=th.name
    conn_client[id]=connexion
    print("Client %s connecté : adresse IP = %s , port = %s "%(id,adresse[0],adresse[1]))
    #Dialogue avec le client
    msg="Vous etes connectés, vous pouvez envoyer vos messages"
    connexion.send(msg.encode("Utf8"))