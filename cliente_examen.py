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

		with open("221A4694.txt", "a") as f:
			f.write(self.nick + ": " + msg + "\n") 
            
def mult_secuencial(A, B): # calculamos multiplicacion en secuencial
		C = [[0] * n_col_B for i in range(n_fil_A)] # C = A*B
		for i in range(n_fil_A):
			for j in range(n_col_B): 
				for k in range(n_col_A):
					C[i][j] += A[i][k] * B[k][j] 
		return C     

def mult_paralela(A, B): # distribuimos tareas para la multiplicaacion en paralelo
		n_cores = mp.cpu_count()
		size_col = math.ceil(n_col_B/n_cores) 
		size_fil = math.ceil(n_fil_A/n_cores) 
		MC = mp.RawArray('i', n_fil_A * n_col_B) 
		cores = [] 
		for core in range(n_cores):
			i_MC = min(core * size_fil, n_fil_A) 
			f_MC = min((core + 1) * size_fil, n_fil_A) 
			cores.append(mp.Process(target=par_core, args=(A, B, MC, i_MC, f_MC)))
		for core in cores:
			core.start()
		for core in cores:
			core.join()# Bloqueo llamadas hasta que terminen su trabajo los cores
		C_2D = [[0] * n_col_B for i in range(n_fil_A)]  
		for i in range(n_fil_A):
			for j in range(n_col_B):
				C_2D[i][j] = MC[i*n_col_B + j] 
		return C_2D

	def core_paral(A, B, MC, i_MC, f_MC):
		for i in range(i_MC, f_MC): 
			for j in range(len(B[0])):
				for k in range(len(A[0])): 
					MC[i*len(B[0]) + j] += A[i][k] * B[k][j]

	if __name__ == '__main__':
		A = [[random.randint(0,10) for i in range(4694)] for j in range(22)] 
		B = [[random.randint(0,10) for i in range(22)] for j in range(4694)] 
		n_fil_A = 4694  
		n_col_A = 22 
		n_fil_B = 22 
		n_col_B = 4694 
		if n_col_A != n_fil_B: raise Exception('Dimensiones no validas') # Compruebo que se puedan multiplicar
		inicioS = time.time()
		sec_mult(A, B) # Ejecuto multiplicacion secuencial
		finS = time.time()
		inicioP = time.time()
		par_mult(A, B) # Ejecuto multiplicacion paralela
		finP = time.time()
		print('\n\nMatriz  A y B se han multiplicado con exito en SECUENCIAL ha tardado ', finS-inicioS, ' y en PARALELO ', finP-inicioP)            


arrancar = Cliente()