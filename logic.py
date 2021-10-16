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
			self.homeComing(r-1, c)
		elif c-1>=0 and self.world.board[r][c-1].visited == True: #self.world.board[r][c-1].pitValue <= 0 and self.world.board[r][c-1].wumpusValue <= 0:
			self.updateCell( r, c-1, True)
			self.homeComing(r, c-1)
		elif r+1<10 and self.world.board[r+1][c].visited == True: #self.world.board[r+1][c].pitValue <= 0 and self.world.board[r+1][c].wumpusValue <= 0:
			self.updateCell( r+1, c, True)
			self.homeComing(r+1, c)
		elif c+1<10 and self.world.board[r][c+1].visited == True: #self.world.board[r][c+1].pitValue <= 0 and self.world.board[r][c+1].wumpusValue <= 0:
			self.updateCell(r, c+1, True)
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
			self.board[r][c].weight += 1
		else:
			self.updateBoardForBreeze(r, c, -100)
			self.board[r][c].weight -= 1

		if self.world.board[r][c].stench:
			self.updateBoardForStench(r, c, 1)
			self.board[r][c].weight += 1
		else:
			self.updateBoardForStench(r, c, -100)
			self.board[r][c].weight -= 1
		
		if self.world.board[r][c].wumpus == True: #self.world.board[r][c].wumpusValue >= 2 or
			# if self.world.numberOfArrow > 0:
			# 	self.world.numberOfArrow -= 1
			# 	self.world.numberOfWumpus -= 1
			# 	self.world.board[r][c].wumpusValue = -100
			# 	self.score -= 10
				 
			# 	print("killed WUMPUS!!!!")
			# 	#playsound('kill.mp3')
				
			# 	self.world.board[r][c].wumpus = False
			# 	self.updateBoardForStench(r, c, -1)
			# 	self.removeStench(r, c)

			# else:
			# 	print("wumpus killed agent")
			# 	self.score -= 1000
			# 	return True
			print("killed by wumpus")
		else:
			self.world.board[r][c].wumpusValue = -100
		
		if self.world.board[r][c].pit == True:
			print("fell in trap")
			self.score -= 1000
			messagebox.showinfo("Died", "Agent has fell in trap")
			return True
		else:
			self.world.board[r][c].pitValue = -100

		return False





	def updateBoardForBreeze(self, r, c, val):
		if r + 1 < self.world.row:
			self.world.board[r+1][c].pitValue += val
		if r - 1 >= 0 and c != 0:
			self.world.board[r-1][c].pitValue += val
		if c + 1 < self.world.col:
			self.world.board[r][c+1].pitValue += val
		if c - 1 >= 0 and r != 0:
			self.world.board[r][c-1].pitValue += val





	def updateBoardForStench(self, r, c, val):
		if r + 1 < self.world.row:
			self.world.board[r + 1][c].wumpusValue += val
            
		if r - 1 >= 0 and c != 0:
			self.world.board[r - 1][c].wumpusValue += val
		
		if c + 1 < self.world.col:
			self.world.board[r][c + 1].wumpusValue += val
            
		if c - 1 >= 0 and r != 0:
			self.world.board[r][c - 1].wumpusValue += val
           





	def checkAdjacentCell(self,r,c):
		stack1 = [] #no wupus
		stack2 = [] #shoot with arrow

		if c+1<self.world.col and self.world.board[r][c+1].pitValue <= 0 and self.world.board[r][c+1].wumpusValue <= 0 and self.world.board[r][c+1].visitedValue < 7:
			stack1.append([r, c+1]) #right

		elif c+1<self.world.col and self.world.board[r][c+1].pitValue <= 0 and self.world.numberOfArrow > 0 and self.world.board[r][c+1].visitedValue < 7:
			stack2.append([r, c+1]) #stack1

		if r-1 >= 0 and self.world.board[r-1][c].pitValue <= 0 and self.world.board[r-1][c].wumpusValue <= 0 and self.world.board[r-1][c].visitedValue < 7:
			stack1.append([r-1, c])

		elif r-1>= 0 and self.world.board[r-1][c].pitValue <= 0 and self.world.numberOfArrow > 0 and self.world.board[r-1][c].visitedValue < 7:
			stack2.append([r-1, c])

		if c-1 >= 0 and self.world.board[r][c-1].pitValue <= 0 and self.world.board[r][c-1].wumpusValue <= 0 and self.world.board[r][c-1].visitedValue < 7:
			stack1.append([r, c-1])

		elif c-1 >= 0 and self.world.board[r][c-1].pitValue <= 0 and self.world.numberOfArrow > 0 and self.world.board[r][c-1].visitedValue < 7:
			stack2.append([r, c-1])

		if r+1 < self.world.row and self.world.board[r+1][c].pitValue <= 0 and self.world.board[r+1][c].wumpusValue <= 0 and self.world.board[r+1][c].visitedValue < 7:
			stack1.append([r+1, c])

		elif r+1 < self.world.row and self.world.board[r+1][c].pitValue <= 0 and self.world.numberOfArrow > 0 and self.world.board[r+1][c].visitedValue < 7:
			stack2.append([r+1, c])

		return stack1, stack2



	def priority(self, i, j):
		if self.world.board[i][j].visitedValue == 0:
			return -2
		# if self.world.board[i][j].wumpusValue <= 0:
		# 	return 0
		else:
			return 1 #-2


	
	def selectCell2(self, stack): #kill wumpus from outside wumpus cell
		if not stack:
			return []
		stack.sort(key=lambda x : x.wumpusValue, reverse=True)
		
		#path = []
		#for st in stack:
		if self.world.numberOfArrow > 0:
			self.world.numberOfArrow -= 1
			print("shooooooot")
			if self.world.board[stack[0][0]][stack[0][1]].wumpus == True:
				print("wumpus killed")
			else:
				print("no wumpus in that cell. Arrow wasted by agent")

			self.world.board[stack[0][0]][stack[0][1]].wumpus = False
			self.world.board[stack[0][0]][stack[0][1]].wumpusValue -= 100

			self.updateCells(stack[0])#path = st

			return st

		print("no arrow. Take a risk.")
		return stack[-1]






	def selectCell(self, stack):
		
		
		mini = self.world.board[stack[0][0]][stack[0][1]].weight + self.priority(stack[0][0], stack[0][1]) # avoid infinity loop
		rv = [stack[0][0], stack[0][1]] #,self.world.board[][stack[0][1]]
		for elem in stack:
			temp = self.world.board[elem[0]][elem[1]].weight + self.priority(elem[0], elem[1])
			if temp < mini:
			    rv = elem
			    mini = temp
			elif temp == mini:
				if self.world.board[elem[0]][elem[1]].move == self.world.board[rv[0]][rv[1]].move and self.world.board[elem[0]][elem[1]].visitedValue == 0: #to avoid repetation
					rv = elem
				elif self.world.board[elem[0]][elem[1]].move > self.world.board[rv[0]][rv[1]].move + 1:
					rv = elem


		return rv





	def choosePath(self, stack1, stack2): #1, stack2
		
		path = []
		if len(stack1) > 0:
			path = self.selectCell(stack1)
		else:
			path = self.selectCell2(stack2)

		return path        #empty path - no cell to move or stack2 path

  



	def updateWeight(self, current): #, previous
		r = current[0]
		c = current[1]
		
		# if previous:
		# 	p_r = previous[0]
		# 	p_c = previous[1]
		# 	self.world.board[p_r][p_c].weight = 1

		# if r-1 >= 0:
		#	self.world.board[r][c].weight += self.world.board[r-1][c].visitedValue > 0 #self.world.board[r-1][c].weight  #max(0, min(2, self.world.board[r-1][c].visitedValue))
		# if r+1 <10:
		# 	self.world.board[r][c].weight += self.world.board[r+1][c].visitedValue > 0
		# if c-1 >= 0:
		# 	self.world.board[r][c].weight += self.world.board[r][c-1].visitedValue > 0  #self.world.board[r][c].visitedValue += self.world.board[r][c-1].visitedValue > 0
		# if c+1 < 10:
		# 	self.world.board[r][c].weight += self.world.board[r][c+1].visitedValue > 0

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
			stack1, stack2 = self.checkAdjacentCell(self.c_loc[0], self.c_loc[1]) #, stack2
			path = self.choosePath(stack1, stack2) #, stack2

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







