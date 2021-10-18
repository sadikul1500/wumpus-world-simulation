from world import *
from tkinter import *
from logic import *

class Mygui:
	def __init__(self, master):
		self.master = master

		Label(self.master, text="Number of Wumpus ", font=5).grid(row=0, column=0)
		Label(self.master, text="Number of Arrow ", font=5).grid(row=1, column=0)
		Label(self.master, text="Number of Pit ", font=5).grid(row=2, column=0)

		# self.w = Entry(self.master, width= 15, borderwidth=3)
		
		self.w = Scale(self.master, from_=0, to=10, length=150, orient=HORIZONTAL, sliderrelief='ridge', highlightthickness=1, activebackground='gray')
		self.w.grid(row=0, column=1)
		self.w.set(3)

		# self.a = Entry(self.master, width= 15, borderwidth=3)
		# self.a.grid(row=1, column=1)
		self.a = Scale(self.master, from_=0, to=10, length=150, orient=HORIZONTAL,sliderrelief='ridge', highlightthickness=1, activebackground='gray')
		self.a.grid(row=1, column=1) #troughcolor='green',
		self.a.set(3)

		# self.p = Entry(self.master, width= 15, borderwidth=3)
		# self.p.grid(row=2, column=1)
		self.p = Scale(self.master, from_=0, to=10, length=150, orient=HORIZONTAL, sliderrelief='ridge', highlightthickness=1, activebackground='gray')
		self.p.grid(row=2, column=1)
		self.p.set(3)

		self.submit = Button(self.master, text="start", command=self.click, font=("Comic Sans Ms", 12), fg="red",
		relief="solid", borderwidth=1, padx=10, pady=3, highlightthickness=2, highlightcolor="black")
		#img = PhotoImage(file="D:/Sadi/tkinter/start.jpg")
		#submit.config(image=img)
		self.submit.grid(row=3, column=0, columnspan=2)
		self.submit.bind("<Enter>", self.on_enter)
		self.submit.bind("<Enter>", self.on_leave)


	def click(self):
		
		numberOfWumpus = int(self.w.get())
		numberOfArrow = int(self.a.get())
		numberOfPit = int(self.p.get())

		#initiate = Initiate(numberOfWumpus, numberOfArrow, numberOfPit)
		self.top = Toplevel(self.master)
		#top.geometry("800X800")
		self.top.title("wumpus world!!!")

		#global world
		self.world = World(numberOfWumpus, numberOfArrow, numberOfPit)
		

		#global game 
		self.game = Logic(self.world, self.top)
		#self.game.run()
		

		#print("done")

	def on_enter(self, e):
		self.submit['background'] = 'blue'

	def on_leave(self, e):
		self.submit['background'] = 'SystemButtonFace'

root = Tk()
root.title("Wumpus")
root.resizable(False, False)
root.iconbitmap('ai.ico')

app = Mygui(root)
root.mainloop()
