from world import *
from tkinter import *
import time
from tkinter import messagebox
from playsound import playsound




class Logic:
	def __init__(self, world, window):
		self.window = window #for UI
		self.world = world
		self.p_loc = []
		self.c_loc = [0, 0]
		#self.move = 0
		self.world.board[0][0].visited = True
		self.world.board[0][0].visitedValue += 1
		self.world.board[0][0].move = 0
		self.updateBoardForBreeze(0, 0, -1)
		self.updateBoardForStench(0, 0, -1)
		self.dir = "right"
		self.score = 0
		self.result = None
		self.label = [ [None]*10 for i in range(10) ] #for UI
		
		self.run() 


	


	def getTxt(self, i, j):
		#global world
		txt = ''

		if self.world.board[i][j].pit == True:
			txt += "P "
		if self.world.board[i][j].wumpus == True:
			txt += "W "
		if self.world.board[i][j].stench > 0 :
			txt += "S "
		if self.world.board[i][j].breeze == True:
			txt += "B "
		if self.world.board[i][j].glitter == True:
			txt += "G "

		return txt



	def buildCell(self):
		for i in range(10):
			for j in range(10):
				txt = self.getTxt(i, j)

				if self.world.board[i][j].visited == True:
					rlf = "sunken"
				else:
					rlf = "groove"
				
				if "G" in txt:
					self.label[i][j] = Label(self.window, text=txt, height=3, width=11,
				 		borderwidth=2, relief="raised",  bg="#d4af37" )
				elif "P" in txt:
					self.label[i][j] = Label(self.window, text=txt, height=3, width=11,
				 		borderwidth=2, relief=rlf, bg="gray" )
				elif "W" in txt:
					self.label[i][j] = Label(self.window, text=txt, height=3, width=11,
				 		borderwidth=2, relief=rlf, bg="#ff8c00" ) #ffcccb #ff9900 #cc5500
				else:
					self.label[i][j] = Label(self.window, text=txt, height=3, width=11,
				 		borderwidth=2, relief=rlf )


				self.label[i][j].grid(row=i, column=j)




	def homeComing(self, r, c): #after finding gold return home - 0,0
		if r+c == 0:
			self.updateCell( r, c, True)
			messagebox.showinfo("climed out of the cave")
			return
		if r-1>=0 and self.world.board[r-1][c].visited == True: #self.world.board[r-1][c].pitValue <= 0 and self.world.board[r-1][c].wumpusValue <= 0:
			self.updateCell( r-1, c, True)
			self.world.board[r-1][c].visited == False #avoid repitation
			self.homeComing(r-1, c)
		elif c-1>=0 and self.world.board[r][c-1].visited == True: #self.world.board[r][c-1].pitValue <= 0 and self.world.board[r][c-1].wumpusValue <= 0:
			self.updateCell( r, c-1, True)
			self.world.board[r][c-1].visited == False
			self.homeComing(r, c-1)
		elif r+1<10 and self.world.board[r+1][c].visited == True: #self.world.board[r+1][c].pitValue <= 0 and self.world.board[r+1][c].wumpusValue <= 0:
			self.updateCell( r+1, c, True)
			self.world.board[r+1][c].visited == False
			self.homeComing(r+1, c)
		elif c+1<10 and self.world.board[r][c+1].visited == True: #self.world.board[r][c+1].pitValue <= 0 and self.world.board[r][c+1].wumpusValue <= 0:
			self.updateCell(r, c+1, True)
			self.world.board[r][c+1].visited == False
			self.homeComing(r, c+1)







	def removeStench(self, row, col):
		if row - 1 >= 0:
			self.world.board[row - 1][col].stench -= 1 
		if row + 1 < 10:
			self.world.board[row + 1][col].stench -= 1 
		if col - 1 >= 0:
			self.world.board[row][col - 1].stench -= 1 
		if col + 1 < 10:
			self.world.board[row][col + 1].stench -= 1 




	def currentLocation(self, r, c):
		if self.world.board[r][c].glitter:
			self.result = "Won"
			self.score += 1000
			print(self.result, self.score)
			#exit()
			#self.printPrevPath()
			return True
		
		elif self.world.board[r][c].breeze:
			self.updateBoardForBreeze(r, c, 1)
			self.world.board[r][c].weight += 1
		else:
			self.updateBoardForBreeze(r, c, -100)
			self.world.board[r][c].weight -= 1

		if self.world.board[r][c].stench:
			self.updateBoardForStench(r, c, 1)
			self.world.board[r][c].weight += 1
		else:
			self.updateBoardForStench(r, c, -100)
			self.world.board[r][c].weight -= 1
		
		if self.world.board[r][c].wumpus == True: #self.world.board[r][c].wumpusValue >= 2 or
			
			print("agent was killed by wumpus")
		else:
			self.world.board[r][c].wumpusValue = -100
			self.updateWumpusValue([r,c])
		
		if self.world.board[r][c].pit == True:
			print("fell in trap")
			self.score -= 1000
			messagebox.showinfo("Died", "Agent has fell in trap")
			return True
		else:
			self.world.board[r][c].pitValue = -100
			self.updatePitValue([r,c])

		return False




	def updatePitValue(self, arr):
		r = arr[0]
		c = arr[1]

		if r-1>=0 and c-1>=0 and self.world.board[r-1][c-1].pitValue > 0:
			self.world.board[r-1][c-1].pitValue += 1
		
		if r+1<10 and c-1>=0 and self.world.board[r+1][c-1].pitValue > 0:
			self.world.board[r+1][c-1].pitValue += 1
		
		if r-1>=0 and c+1<10 and self.world.board[r-1][c+1].pitValue > 0:
			self.world.board[r-1][c+1].pitValue += 1
		
		if r+1<10 and c+1<10 and self.world.board[r+1][c+1].pitValue > 0:
			self.world.board[r+1][c+1].pitValue += 1


	def updateBoardForBreeze(self, r, c, val):
		x, y, m, n = 0, 0, 0, 0 #x out of y
		#m,n sure about wumpus cell        #total y 
		if r + 1 < self.world.row:
			self.world.board[r + 1][c].pitValue += val
			y += 1
			if self.world.board[r + 1][c].pitValue < 0:
				x += 1
			else:
				m, n = r+1 , c
        
		if r - 1 >= 0 and c != 0:
			self.world.board[r - 1][c].pitValue += val
			y += 1
			if self.world.board[r - 1][c].pitValue < 0:
				x += 1
			else:
				m, n = r-1 , c
		
		if c + 1 < self.world.col:
			self.world.board[r][c + 1].pitValue += val
			y += 1
			if self.world.board[r][c + 1].pitValue < 0:
				x += 1
			else:
				m, n = r , c+1
            
		if c - 1 >= 0 and r != 0:
			self.world.board[r][c - 1].pitValue += val
			y += 1
			if self.world.board[r][c - 1].pitValue < 0:
				x += 1
			else:
				m, n = r , c-1

		if x == y-1:
			self.world.board[m][n].pitValue += 10 #sure about pit
			





	def updateBoardForStench(self, r, c, val):
		#if val > 0:
		x, y, m, n = 0, 0, 0, 0 #x out of y
		#m,n sure about wumpus cell        #total y 
		if r + 1 < self.world.row:
			self.world.board[r + 1][c].wumpusValue += val
			y += 1
			if self.world.board[r + 1][c].wumpusValue < 0:
				x += 1
			else:
				m, n = r+1 , c
        
		if r - 1 >= 0 and c != 0:
			self.world.board[r - 1][c].wumpusValue += val
			y += 1
			if self.world.board[r - 1][c].wumpusValue < 0:
				x += 1
			else:
				m, n = r-1 , c
		
		if c + 1 < self.world.col:
			self.world.board[r][c + 1].wumpusValue += val
			y += 1
			if self.world.board[r][c + 1].wumpusValue < 0:
				x += 1
			else:
				m, n = r , c+1
            
		if c - 1 >= 0 and r != 0:
			self.world.board[r][c - 1].wumpusValue += val
			y += 1
			if self.world.board[r][c - 1].wumpusValue < 0:
				x += 1
			else:
				m, n = r , c-1

		if x == y-1:
			self.world.board[m][n].wumpusValue += 10 #sure about wumpus
			if self.world.numberOfArrow > 0: #adjacent
				print("shoooot at ", m, n)
				messagebox.showinfo("Winner", "shooooooot at " +str(m) +", " +str(n))
				self.world.numberOfArrow -= 1
				self.world.board[m][n].wumpus = False
				self.removeStench(m, n)
				self.updateCells([m, n])




		
           





	def checkAdjacentCell(self,r,c):
		stack1 = [] #no wupus
		stack2 = [] #shoot with arrow
		stack3 = [] #take risk for pit

		if c+1 < 10 and self.world.board[r][c+1].pitValue <= 0 and self.world.board[r][c+1].wumpusValue <= 0 and self.world.board[r][c+1].visitedValue < 3:
			stack1.append([r, c+1]) #right
			# if self.world.board[r][c+1].move - 1 == self.world.board[r][c].move:
			# 	self.world.board[r][c+1].weight += 2


		elif c+1 < 10 and self.world.board[r][c+1].pitValue <= 0 and self.world.board[r][c+1].wumpusValue > 0 and self.world.board[r][c+1].visitedValue < 7:
			stack2.append([r, c+1]) #stack1

		elif c+1 < 10 and self.world.board[r][c+1].pitValue > 0 and self.world.board[r][c+1].visitedValue < 7:
			stack3.append([r, c+1]) #stack1

		
		if r-1 >= 0 and self.world.board[r-1][c].pitValue <= 0 and self.world.board[r-1][c].wumpusValue <= 0 and self.world.board[r-1][c].visitedValue < 3:
			stack1.append([r-1, c])

		elif r-1 >= 0 and self.world.board[r-1][c].pitValue <= 0 and self.world.board[r][c+1].wumpusValue > 0 and self.world.board[r-1][c].visitedValue < 7:
			stack2.append([r-1, c])

		elif r-1 >= 0 and self.world.board[r-1][c].pitValue > 0 and self.world.board[r-1][c].visitedValue < 7:
			stack3.append([r-1, c]) #stack1


		if c-1 >= 0 and self.world.board[r][c-1].pitValue <= 0 and self.world.board[r][c-1].wumpusValue <= 0 and self.world.board[r][c-1].visitedValue < 3:
			stack1.append([r, c-1])

		elif c-1 >= 0 and self.world.board[r][c-1].pitValue <= 0 and self.world.board[r][c-1].wumpusValue > 0 and self.world.board[r][c-1].visitedValue < 7:
			stack2.append([r, c-1])

		elif c-1 >= 0 and self.world.board[r][c-1].pitValue > 0 and self.world.board[r][c-1].visitedValue < 7:
			stack3.append([r, c-1])

		if r+1 < 10 and self.world.board[r+1][c].pitValue <= 0 and self.world.board[r+1][c].wumpusValue <= 0 and self.world.board[r+1][c].visitedValue < 3:
			stack1.append([r+1, c])

		elif r+1 < 10 and self.world.board[r+1][c].pitValue <= 0 and self.world.board[r][c+1].wumpusValue > 0 and self.world.board[r+1][c].visitedValue < 7:
			stack2.append([r+1, c])

		elif r+1 < 10 and self.world.board[r+1][c].pitValue > 0 and self.world.board[r+1][c].visitedValue < 7:
			stack3.append([r+1, c])

		return stack1, stack2, stack3



	def priority(self, i, j, moveNo):
		if self.world.board[i][j].visitedValue == 0:
			return -2 #high priority
		# if self.world.board[i][j].wumpusValue <= 0:
		# 	return 0
		elif self.world.board[i][j].move == moveNo-1:
			return 3
		else:
			return 1 #-2

	
	def updateWumpusValue(self, arr):
		r = arr[0]
		c = arr[1]

		if r-1>=0 and c-1>=0 and self.world.board[r-1][c-1].wumpusValue > 0:
			self.world.board[r-1][c-1].wumpusValue += 1
		
		if r+1<10 and c-1>=0 and self.world.board[r+1][c-1].wumpusValue > 0:
			self.world.board[r+1][c-1].wumpusValue += 1
		
		if r-1>=0 and c+1<10 and self.world.board[r-1][c+1].wumpusValue > 0:
			self.world.board[r-1][c+1].wumpusValue += 1
		
		if r+1<10 and c+1<10 and self.world.board[r+1][c+1].wumpusValue > 0:
			self.world.board[r+1][c+1].wumpusValue += 1




	
	def selectCell2(self, stack): #kill wumpus from outside wumpus cell
		if not stack:
			return []
		
		if self.world.numberOfArrow > 0:
			
			rv = []
			maxi = -2000
			for st in stack:
				if self.world.board[st[0]][st[1]].wumpusValue > maxi:
					maxi = self.world.board[st[0]][st[1]].wumpusValue
					rv = st
			
			print("shooooooot at ", rv[0], rv[1])
			messagebox.showinfo("Winner", "shooooooot at " +str(rv[0]) +", " + str(rv[1]))

			self.world.numberOfArrow -= 1
			if self.world.board[rv[0]][rv[1]].wumpus == True:
				print("wumpus was killed!!!!!!")
				self.world.board[rv[0]][rv[1]].wumpusValue -= 100
				self.world.board[rv[0]][rv[1]].wumpus = False
				self.removeStench(rv[0], rv[1])
				self.updateCells([rv[0], rv[1]])
			else:
				print("no wumpus. arrow missed")
				self.updateWumpusValue([rv[0], rv[1]])
			return rv
		else:
			mini = 200
			print("no arrow. Take a risk.")
			for st in stack:
				if self.world.board[st[0]][st[1]].wumpusValue < mini:
					mini = self.world.board[st[0]][st[1]].wumpusValue
					rv = st
			return rv



		
		#return stack[-1]


	def selectCell3(self, stack): #take risk for cell
		if not stack:
			return []
		#stack.sort(key=lambda x : x.pitValue) #, reverse=True

		print("agent is taking a risk.")
		mini = 200
		#print("no arrow. Take a risk.")
		for st in stack:
			if self.world.board[st[0]][st[1]].pitValue < mini:
				mini = self.world.board[st[0]][st[1]].pitValue
				rv = st
		return rv
		#return stack[0]








	def selectCell(self, stack, moveNo):
		
		
		mini = self.world.board[stack[0][0]][stack[0][1]].weight + self.priority(stack[0][0], stack[0][1], moveNo) # avoid infinity loop
		rv = [stack[0][0], stack[0][1]] #,self.world.board[][stack[0][1]]
		for elem in stack:
			temp = self.world.board[elem[0]][elem[1]].weight + self.priority(elem[0], elem[1], moveNo)
			if temp < mini:
			    rv = elem
			    mini = temp
			elif temp == mini:
				if self.world.board[elem[0]][elem[1]].move == self.world.board[rv[0]][rv[1]].move and self.world.board[elem[0]][elem[1]].visitedValue == 0: #to avoid repetation
					rv = elem
				elif self.world.board[elem[0]][elem[1]].move > self.world.board[rv[0]][rv[1]].move + 1:
					rv = elem


		return rv





	def choosePath(self, stack1, stack2, stack3, moveNo): #1, stack2
		
		path = []
		if len(stack1) > 0:
			path = self.selectCell(stack1, moveNo)
		if not path:
			path = self.selectCell2(stack2)
		if not path:
			path = self.selectCell3(stack3)

		
		return path        #empty path - no cell to move or stack2 path


  



	def updateWeight(self, current): #, previous
		r = current[0]
		c = current[1]
		
		

		if r-1 >= 0:
			self.world.board[r-1][c].weight += self.world.board[r-1][c].visitedValue #self.world.board[r-1][c].weight  #max(0, min(2, self.world.board[r-1][c].visitedValue))
		if r+1 <10:
		 	self.world.board[r+1][c].weight += self.world.board[r+1][c].visitedValue
		if c-1 >= 0:
		 	self.world.board[r][c-1].weight += self.world.board[r][c-1].visitedValue  #self.world.board[r][c].visitedValue += self.world.board[r][c-1].visitedValue > 0
		if c+1 < 10:
		 	self.world.board[r][c+1].weight += self.world.board[r][c+1].visitedValue # > 0

		self.world.board[r][c].weight += 1 #self.world.board[r][c].visitedValue
		


	



	def animate(self, txt, i, j):
		if "G" in txt:
			self.label[i][j].config(bg="#2eb92e", relief="raised") #text=""
			self.world.board[i][j].glitter = False
			messagebox.showinfo("Winner", "Agent has found gold") #show a win message
			self.homeComing(i, j)
		elif "P" in txt:
			self.label[i][j].config(bg="gray")
		elif "W" in txt:
			self.label[i][j].config(bg="#ff8c00")
		else:
			self.label[i][j].config(bg="#bfff80")





	def updateCell(self, i, j, anim=False):
		txt = self.getTxt(i, j)
		

		if anim:
			pretxt = self.label[i][j].cget("text")
			#rlf = "sunken"
			if "G" in pretxt:
				self.label[i][j].config(bg="#d4d4d4", relief="sunken", text=txt)
			elif "P" in pretxt:
				self.label[i][j].config(bg="#d4d4d4", relief="sunken", text=txt)
			elif "W" in pretxt:
				self.label[i][j].config(bg="red", relief="sunken", text=txt)
			else:
				self.label[i][j].config(bg="#d4d4d4", relief="sunken", text=txt)

			#self.window.after(5000, lambda: self.updateCell(i, j))
			self.window.update()
			time.sleep(1)
			self.animate(txt, i, j)


		else:
			#rlf = "groove"
			self.label[i][j].config(text=txt)
			
		




	def updateCells(self, arr):
		i = arr[0]
		j = arr[1]
		self.updateCell(i, j, True)
		#self.window.update()

		if i - 1 >= 0:
			self.updateCell(i-1, j, False)
		if i + 1 < 10:
			self.updateCell(i+1, j, False)
		if j - 1 >= 0:
			self.updateCell(i, j-1, False)
		if j + 1 < 10:
			self.updateCell(i, j+1, False)

		self.window.update()





	def run(self):
		self.buildCell()
		self.window.update()

		for i in range(0, 1000):  #while(True):
			gameOff = self.currentLocation(self.c_loc[0], self.c_loc[1])
			self.updateWeight(self.c_loc) #self.p_loc
			self.updateCells(self.c_loc)

			if gameOff == True:
				break
			stack1, stack2, stack3 = self.checkAdjacentCell(self.c_loc[0], self.c_loc[1]) #, stack2
			path = self.choosePath(stack1, stack2, stack3, i) #, stack2 #move number

			if not path:
				print("can't move")
				messagebox.showinfo("stopped", "Agent can't move")
				break

			
			self.world.board[path[0]][path[1]].move = i+1
			self.world.board[path[0]][path[1]].visited = True
			self.world.board[path[0]][path[1]].visitedValue += 1
			
			
			
			print("moving Forward to", path, "from", self.c_loc)
			self.p_loc = self.c_loc
			self.c_loc = path
			self.score -= 1
			#time.sleep(2)
			#self.showBoard()
			#self.window.mainloop()







