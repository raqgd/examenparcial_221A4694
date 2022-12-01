import socket
import threading
import sys
import pickle
import os

class Servidor():

	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
		self.clientes = [] #array que almacena los clientes
		print('\nSu IP actual es : ',socket.gethostbyname(host))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket()
		self.s.bind((str(host), int(port)))
		self.s.listen(30)
		self.s.setblocking(False)

		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		while True:
			msg = input('\n << SALIR = 1 >> \n')
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				with open("nicknameList.txt", "w") as f:
					f.write(" ")
				self.s.close()
				sys.exit()
			else: pass

	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except: pass
        
	def leerNick(self):
		with open("nicknameList.txt", "r") as f:
			print("Clientes conectados actualmente {\n" + f.read() + "--------------------------")

	def procesarC(self):
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(128)
						if data: self.broadcast(data,c)
						self.listaNicks()  # Imprimir nicknames
						matriz = pickle.loads(data) #Añado datos matrices
						print(matriz) # Imprime el mensaje
						matrizFinal = matriz.split(',')
						print(matrizFinal)
						self.multiplicacionMatrices(matrizFinal[0], matrizFinal[1], matrizFinal[2], matrizFinal[3])
						# Mandar mensaje a los demas clientes
							self.broadcast(data, c)
						except:  
					except: pass

def historial(self, n):  # Guardamos el historial de mensajes
		with open("221A4694.txt", 'a') as f:
			f.write("Historial " + str(n) + ":\n") 
            
		# Imprimimos lista de usuarios conectados
	def listaNicks(self):
		print("Lista de Nicknames:")
		with open("221A4694nicknames.txt", 'r') as f:
			print(f.read())
            
	def mult_secuencial(A, B): 
	C = [[0] * n_col_B for i in range(n_fil_A)] C = A*B
	for i in range(n_fil_A):
		for j in range(n_col_B): 
			for k in range(n_col_A): 
				C[i][j] += A[i][k] * B[k][j] 
	return C

arrancar = Servidor()