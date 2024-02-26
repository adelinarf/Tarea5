import numpy as np
import copy
primero = "-"
segundo = "|"
vacio = " "
plus = "+"


positive_infinity = float('inf')
negative_infinity = float('-inf')


def evaluate(grid):
	for row in range(3):
		if (grid[row][0]==grid[row][1] and grid[row][1]==grid[row][2] and grid[row][2]==plus):
			return 10

	for col in range(3):
		if (grid[0][col]==grid[1][col] and grid[1][col]==grid[2][col] and grid[2][col]==plus):
			return 10

	if grid[0][0]==plus and grid[0][0] == grid[1][1] and grid[1][1]==grid[2][2]:
		return 10

	if (grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0] and grid[2][0]==plus) : 
		return 10

	for row in range(3):
		if (plus in grid[row]):
			return 5
		else:
			return -5

	for col in range(3):
		if (plus in grid[:col]):
			return 5
		else:
			return -5

	return 0

ganadores = []

def MM(w,n,alpha,beta,isMax,lastO):
	score = evaluate(w)
	if score==10:
		print(np.matrix(w))
		z = np.matrix(w)
		ganadores.append([copy.deepcopy(w),n])
		return score 
	if score==-10:
		return score 
	if (n==0):
		return evaluate(w)
	if (isMax):
		best = negative_infinity
		for i in range(3):
			for j in range(3):
				if (w[i][j]==vacio or w[i][j]=="|") and lastO[0]!=i and lastO[1]!=j:
					original = w[i][j]
					if w[i][j]=="|":
						w[i][j] = plus
					else:
						w[i][j] = primero 
					last = [i,j]
					best = max(best,MM(w,n-1,alpha,beta,not isMax,last))
					alpha = max(alpha,best)
					if beta<=alpha:
						break

					w[i][j] = original
		return best
	else:
		best = positive_infinity
		for i in range(3):
			for j in range(3):
				if (w[i][j]==vacio or w[i][j]=="-") and lastO[0]!=i and lastO[1]!=j:
					original = w[i][j]
					if w[i][j]=="-":
						w[i][j] = plus
					else:
						w[i][j] = segundo
					last = [i,j]
					best = min(best,MM(w,n-1,alpha,beta,not isMax,last))
					alpha = min(alpha,best)
					if beta<=alpha:
						break

					w[i][j] = original
		return best

n=[[vacio,vacio,vacio],[vacio,vacio,vacio],[vacio,vacio,vacio]]
alpha=negative_infinity
beta=positive_infinity
depth = 6   #cantidad de movimientos para ambos jugadores
a = MM(n,depth,alpha,beta,True,[-1,-1])
print("Para",depth,"movimientos se llega a",len(ganadores), "nodos con una configuración ganadora")
