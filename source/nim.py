#!/usr/bin/python3
# Nim Game by Dean Ang

from tkinter import *
from random import *
from itertools import *
#from PIL import ImageTk, Image

#Define root window with title
root = Tk()
root.wm_title('Game of Nim')
root.wm_geometry('300x640+10+10')
root.lift()

v = StringVar()
clickedrow = "None"
nselected = 0
heaps = [1,3,5,7]

def hs(lst):
    return lst[0]^lst[1]^lst[2]^lst[3]

def countzero(lst):
    return sum([1 if x==0 else 0 for x in lst])

nsum = hs(heaps)


#matchstick = ImageTk.PhotoImage(Image.open("matchstick.jpeg"))
#blank = ImageTk.PhotoImage(Image.open("blank.jpeg"))
matchstick = PhotoImage(file="matchstick.gif")
blank = PhotoImage(file="blank.gif")

#A class for the matchstick or blank object
class GameObject(Label):
    global heaps
    #Initialise the object
    def __init__(self, parent, i, j):
        #Inherit the tkinter label object and initialise 
        Label.__init__(self, parent)
        #Decide if image is matchstick or blank based on row number (i) and column number (j) 
        if j < heaps[i]:
            self.config(image = matchstick)
        else:
            self.config(image = blank)
        self.pack(side = LEFT)

        # Callback function when matchstick is clicked
        def callback(event):
            global clickedrow, heaps, nselected
            if j < heaps[i]:
                if clickedrow == "None":
                    clickedrow = i
                if clickedrow == i:
                    self.config(image = blank)
                    nselected += 1
                else:
                    clickedrow = i
                    nselected = 1
                    redraw()
                    self.config(image = blank)

        def commitmove(event):
            heaps[clickedrow] -= nselected
            clickedrow = None
            nselected = 0
        self.bind('<Button-1>', callback)
        self.pack(side = RIGHT)
            
#Draw 4 rows of canvases
rows = [Canvas(root) for i in range(len(heaps))]

#Create title label and instruction text
title = Label(root, background = 'light green', justify = CENTER, wraplength = 285, text='Game of Nim: By Dean Ang', font = ('Courier', 18, 'bold'))
instruction = Label(root, justify = LEFT, wraplength = 285, text='Player who pick the last matchstick loses.\nWhen it\'s one\'s turn to play, a player can remove up to as many matchsticks available in a one row.', anchor = NW)
status = Label(root, background = 'light yellow', justify = LEFT, wraplength = 285, text='Status: Choose who to go first!')
comradio = Radiobutton(root, text = "Computer go first!", variable = v, value="Hello")
title.pack(expand=1, fill=X)
instruction.pack()
comradio.pack()

'''
def comstartfirst(event):
    global heaps
    row = randint(1,4)
    n = randint(1, heaps[row-1])
    heaps[row-1] -= n
    status.config(text = 'I will start first. I haved moved ' + str(n) + ' matchstick(s) from row ' + str(row)+". Your turn now.")
    redraw()
    comradio.config(state="disabled")
'''            
status.pack(expand=1, fill=X)

#For each canvas, create a lst of Labels
labels = [[GameObject(rows[i], i, j)  for j in range(7)]  for i in range(len(heaps))]
for i in range(4):
    rows[i].pack()

#A function to draw the matchsticks based on nsum
def redraw():
    global labels, heaps
    for i in range(len(heaps)):
        for j in range(heaps[i]):
            labels[i][j].config(image = matchstick)
        for j in range(heaps[i], 7):
            labels[i][j].config(image = blank)


            
#Function to commit move to change nsum
def confirmmove(event):
    global heaps, clickedrow, nselected
    if clickedrow == "None":
        status.config(text = 'Please remove at least 1 matchstick!')
    else:
        heaps[clickedrow] -= nselected
        print("After my move, heaps is {} and nsum is {}".format(heaps, hs(heaps)))
        if heaps == [0, 0, 0, 1] or heaps == [0, 0, 1, 0] or heaps == [0, 1, 0, 0] or heaps == [1, 0, 0, 0]:
            heaps = [0, 0, 0, 0]
            redraw()
            status.config(text = 'You win! Press R to restart or Q to quit.')
        else:
            clickedrow = "None"
            nselected = 0
            status.config(text = '')
            redraw()
            button.config(state="disabled")
            cmove()
            
#Create confirm move button
button = Button(root, text = 'Confirm Move')
button.bind('<Button-1>', confirmmove)
button.pack()

#Define Keypress event to reset or quit game
def key_press(event):
    global heaps
    if event.char == 'R' or event.char == 'r':
        heaps = [1, 3, 5, 7]
        comradio.config(state="normal")
        status.config(text = 'Player to move!')
        button.config(state="normal")
        redraw()
    if event.char == 'Q' or event.char == 'q':
        root.destroy()
    
root.bind('<KeyPress>', key_press)
root.bind('<Return>', confirmmove)

#Computer to move
def cmove(*event):
    global heaps
    status.config(text = 'Computer to move')
    if hs(heaps) == 0:
        row = randint(1,4)
        while(heaps[row-1] == 0):
            row = randint(1,4)
        n = randint(1, heaps[row-1])              
        heaps[row-1] -= n
        print("After computer move: heaps is {} and nsum is {}. i is {}!".format(heaps, hs(heaps),str(row)))
        status.config(text = 'I haved moved ' + str(n) + ' matchstick(s) from row ' + str(row)+". Your turn now.")
        redraw()
        comradio.config(state="disabled")
        button.config(state="normal")
    
    elif heaps == [0, 0, 0, 1] or heaps == [0, 0, 1, 0] or heaps == [0, 1, 0, 0] or heaps == [1, 0, 0, 0]:
        heaps = [0, 0, 0, 0]
        redraw()
        status.config(text = 'You win! Press R to restart or Q to quit.')

    elif heaps in [list(x) for x in permutations([1,2,0,0])]:
        heaps[heaps.index(2)] = 0
        redraw()
        status.config(text = 'I win! Press R to restart or Q to quit.')

    elif countzero(heaps) == 3:
        indx = sum([ i if x != 0 else 0 for i,x in enumerate(heaps)])
        heaps[indx] = 1
        redraw()
        status.config(text = 'I win! Press R to restart or Q to quit.') 
        
    else:
        comradio.config(state="disabled")
        nsum = hs(heaps)
        for i in range(4):
            test = heaps[i] - (nsum^heaps[i])
            temp = [ x if j != i else x - test for j,x in enumerate(heaps)]
            if test > 0:
                heaps[i] -= test
                print("After computer move: heaps is {} and nsum is {}. i is {}!".format(heaps, hs(heaps),str(i)))
                status.config(text = 'My turn. I haved moved ' + str(nsum) + ' matchstick(s) from row ' + str(i+1))
                redraw()
                button.config(state="normal")
                break

comradio.bind('<Button-1>', cmove)

root.mainloop()


