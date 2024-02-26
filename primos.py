from math import sqrt,floor,ceil
from queue import Queue
import copy
 
#es_primo calcula si un numero n es primo o no
#Tiene tiempo de O(n^1/2) pero se asume O(1)
def es_primo(n):
	primo = 0
	if n<=1:
		return False
	if(n > 1):
		for i in range(2, int(sqrt(n)) + 1):
			if (n % i == 0):
				primo = 1
				break
		if (primo == 0):
			return True
		else:
			return False
	else:
		return False

INF = float('inf')
NIL = 0

class GrafoBipartito():
	def __init__(self, m, n):
		self.n_izquierda = m-1  #numero de vertices en la izquierda
		self.n_derecha = n-1    #numero de vertices en la derecha
		self.adyacentes = [[] for _ in range(m+1)]  
		#lista de lista que representa para adyacentes[x] los vertices adyacentes a x

	#Agrega lado de u a v
	def agregar_lado(self, u, v):
		self.adyacentes[u].append(v)

	# Retorna true si hay un camino de aumento, sino false 
	def BFS(self):
		Q = Queue()
		for u in range(1, self.n_izquierda+1):
			if self.par_u[u] == NIL:
				self.distancia[u] = 0
				Q.put(u)
			else:
				self.distancia[u] = INF
		self.distancia[NIL] = INF
		while not Q.empty():
			u = Q.get()
			if self.distancia[u] < self.distancia[NIL]:
				for v in self.adyacentes[u]:
					if self.distancia[self.par_v[v]] == INF:
						self.distancia[self.par_v[v]] = self.distancia[u] + 1
						Q.put(self.par_v[v])
		return self.distancia[NIL] != INF

	# Retorna true si hay un camino de aumento que comienza con u
	def DFS(self, u):
		if u != NIL:
			for v in self.adyacentes[u]:
				if self.distancia[self.par_v[v]] == self.distancia[u] + 1:
					if self.DFS(self.par_v[v]):
						self.par_v[v] = u
						self.par_u[u] = v
						return True
			self.distancia[u] = INF
			return False
		return True

	#Implementacion del algoritmo de Hopcroft Karp
	def hopcroft_karp(self):
		self.par_u = [0 for x in range(self.n_izquierda+1)]
		self.par_v = [0 for x in range(self.n_derecha+1)]

		self.distancia = [0 for x in range(self.n_izquierda+1)]
		resultado = 0
		while self.BFS():
			for u in range(1, self.n_izquierda+1):
				if self.par_u[u] == NIL and self.DFS(u):
					resultado += 1
		return resultado

#tamanos consigue los tamanos de ambos lados del grafo bipartito
# Tiempo de ejecucion de O(n^2)
def tamanos(C):
	Z = [[]]*len(C)
	for x in range(len(C)):
		actual = []
		for y in range(len(C)):
			if C[x]==C[y]:
				continue
			else:
				if es_primo(C[x]+C[y]):
					actual.append(copy.deepcopy(C[y]))
		Z[x] = actual
	izquierda = []
	derecha = []
	for x in range(len(C)):
		actual = x+1
		if len(izquierda)==0 and len(derecha)==0:
			izquierda.append(actual)
			derecha += Z[x]
		else:
			if actual in set(izquierda):
				derecha += Z[x]
			if actual in set(derecha):
				izquierda += Z[x]

	n1 = len(set(izquierda))
	n2 = len(set(derecha))
	return [n1,n2]

def menor_cantidad_numeros(C):
	[n1,n2] = tamanos(C)  #O(n^{2})
	g = GrafoBipartito(n1, n2)
	#O(n^2)
	for x in range(len(C)):   #O(n^{2})
		for y in range(len(C)):
			if C[x]==C[y]:
				continue
			else:
				if es_primo(C[x]+C[y]):
					g.agregar_lado(C[x]%n1,C[y]%n2)
	menor = g.hopcroft_karp()  #O(n^{2}*n^{1/2})
	print("La menor cantidad de numeros a eliminar es",menor)

C = [1,2,3,4,5]  #Conjunto C a evaluar

menor_cantidad_numeros(C)

