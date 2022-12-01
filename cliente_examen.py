import threading
import sys
import socket
import pickle
import os


class Cliente():

    def __init__(self, host=input("Introduce la direccion ip del servidor: "), port=input("Introduce el puerto deseado: ")):
        nick = self.pedirNick() #Llamamos a la función que pide el nickname y guardamos su valor en una variable
        self.sock = socket.socket() # Inicializa el socket
        self.sock.connect((str(host), int(port))) # Se conecta al socket con la ip y puerto dados
        threading.Thread(target=self.recibir, daemon = True).start() # Crea un hilo, lo convierte en demonio y lo inicia
        
        print('Hilo con PID',os.getpid()) # Imprime el ID del proceso
        print('Hilos activos', threading.active_count()) # Imprime la cantidad de hilos activos(cada cliente es un hilo)
        
        
        while True: # Creamos un bucle para que el cliente pueda escribir mientras el programa este activo
            msg = input('\nEscriba texto ? ** Enviar = ENTER ** Abandonar Chat = Q \n') # Le pedimos al cliente que introduzca un mensaje y se guarde en la variable
            if msg != 'Q' : # Si no introduce el cáracter Q envia el mensaje
                self.enviar(nick, msg)
                self.historial(nick, msg)
            else: # Si lo introduce el hilo se cierra, borra el nick y se acaba el programa
                self.deleteNick(nick)
                print(" **** TALOGOOO  ****")
                self.sock.close() # Cierra el socket
                sys.exit() # Cierra el programa

    def recibir(self): # Función para recibir mensajes del servidor
        while True: # Bucle while para que se ejecute mientras el programa esta activo
            try: # Gestionamos con un try/except los errores
                data = self.sock.recv(64) # Recibimos el mensaje del servidor y lo guardamos en la variable data
                if data: # Si data no está vacio imprime el mensaje
                    print(pickle.loads(data))
            except:
                pass

            
    def enviar(self, nick, msg): # Función para enviar el mensaje al servidor
        self.sock.send(pickle.dumps(msg)) # El hilo manda a través del socket el msg al servidor
        
    def nickname(self, nick): # Función para guardar el nickname y mostrarlo en el servidor
        with open("u22132785nicknames.txt", 'r') as f: # Abre en modo lectura el documento nicknames.txt
            if(nick in f.read()): # Comprueba si el nick está ya en uso y si esta exige otro nick
                print("Error. Introduce otro nickname")
                self.pedirNick()
            else: # Si no esta en uso lo añade al documento
                with open("u22132785nicknames.txt", 'a') as f: # Manejamos un documento externo para que guarde el nick
                    f.write(nick+"\n") # Escribimos en el documento el valor de la variable
        
    def historial(self, nick, msg): # Función para crear el historial del chat
        with open("ue22132785A1.txt", 'a') as f: # Manejamos un documento externo para que guarde el nick y el mensaje que envia
            f.write(nick+": "+ msg+ "\n") # Escribimos en el documento el valor de las variables
            
    def pedirNick(self): # Función que solicita el nickname
        nick=input("Introduce tu nickname: ") # Le pedimos al cliente su nickname y lo guardamos en una variable
        self.nickname(nick) # Guardamos la variable en el txt sino esta en uso ya
        return nick
    
    def deleteNick(self, nick): # Función para borrar el nickname de nicknames activos
        lineas = [] # Inicializamos la lista lineas
        with open("u22132785nicknames.txt", 'r') as f:
                    nicknames = f.readlines() # Guardamos en una lista todas las lineas del txt
                    for n in nicknames: # Recorremos la lista
                        if (nick not in n): # Si el nick no esta en el elemento de la lista guardamos el elemento en la lista lineas
                            lineas.append(n)
        with open("u22132785nicknames.txt", 'w') as f: # Borramos lo que habia en el txt y le insertamos los elementos de la lista lineas
            for n in lineas:
                f.write(n)

c = Cliente()