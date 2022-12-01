import threading
import sys
import socket
import threading
import sys
import socket
import pickle
import os

class Cliente():

	def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  ")), nick = ""):
		self.s = socket.socket()
		while (nick == ""):
			nick = input ("Introduce tu nombre de usuario: ")
		self.nick = nick
		with open("nickname.txt", "a") as f:
			f.write(self.nick + "\n")
		self.s.connect((host, int(port)))
        
        
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		threading.Thread(target=self.recibir, daemon=True).start()

		while True:
			msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
			if msg != '1' : self.enviar(msg)
			else:
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.deleteNick(nick)
				self.s.close()
				sys.exit()
                
	def borrarNick(self, nick):
		lines = []
		with open("nickname.txt" , "r") as f:
			nicknames = f.readlines()
			for n in nickname:
				if (nick not in n):
					lines.append(n)
                
			with open("nicknames.txt", "w") as f:
				for n in lines:
					f.write(n)

				nick = input("Ingrese su nickname")
				msg = input("Escriba el mensaje")
				f.write("\n" + nick + "~" + msg)

	def recibir(self):
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			try:
				data = self.s.recv(128)
				if data: print(pickle.loads(data))
			except: pass
        
	def enviar(self, msg):
		self.s.send(pickle.dumps(self.nick + ": " + msg))

		with open("22164964.txt", "a") as f:
			f.write(self.nick + ": " + msg + "\n") 

arrancar = Cliente()