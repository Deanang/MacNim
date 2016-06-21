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
root.attributes("-topmost", True)

v = StringVar()
clickedrow = None
nselected = 0
heaps = [1,3,5,7]

def hs(lst):
    return lst[0]^lst[1]^lst[2]^lst[3]

# return True if lst1, which is shorter, is a sublist of lst2; else return False 
def contains(lst1, lst2):
    return True if sorted(lst1) == sorted(lst2)[:len(lst1)] else False

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
            self.photo = matchstick
        else:
            self.config(image = blank)
            self.photo = blank
        self.pack(side = LEFT)
        self.clicked = 0

                
        # Callback function when matchstick is clicked
        def callback(event):

            global clickedrow, heaps, nselected

            if j < heaps[i]:

                if clickedrow == "None":

                    clickedrow = i

                if clickedrow == i:
                    if self.clicked == 0:
                        self.config(image = blank)

                        nselected += 1
                        self.clicked = 1                       
                else:

                    clickedrow = i

                    nselected = 1

                    redraw()

                    self.config(image = blank)                   
                    
        def commitmove(event):
            heaps[clickedrow] -= nselected
            nselected = 0
            clickedrow = None
        self.bind('<Button-1>', callback)
        self.pack(side = LEFT)
            
#Draw 4 rows of canvases
rows = [Canvas(root) for i in range(len(heaps))]

#Create title label and instruction text
title = Label(root, background = 'light green', justify = CENTER, wraplength = 285, text='Game of Nim: By Dean Ang', font = ('Courier', 18, 'bold'))
instruction = Label(root, justify = LEFT, wraplength = 285, text='Player who pick the last matchstick loses.\nWhen it\'s one\'s turn to play, a player can remove up to as many matchsticks available in a one row.', anchor = NW)
status = Label(root, background = 'light yellow', justify = LEFT, wraplength = 285, text='Status: Choose who to go first!')
comradio = Radiobutton(root, text = "Computer go first!", variable = v, value="Hello")
title.pack(expand=1, fill=X)
instruction.pack()
status.pack(expand=1, fill=X)
comradio.pack()

           


#For each canvas, create a lst of Labels
labels = [[GameObject(rows[i], i, j)  for j in range(7)]  for i in range(len(heaps))]
for i in range(4):
    rows[i].pack()

#A function to draw the matchsticks based on nsumr
def redraw():
    global labels, heaps, clickedrow
    for i in range(len(heaps)):
        for j in range(heaps[i]):
            labels[i][j].config(image = matchstick)
            labels[i][j].clicked = 0 
        for j in range(heaps[i], 7):
            labels[i][j].config(image = blank)
            labels[i][j].clicked = 0


            
#Function to commit move to change nsum
def confirmmove(event):
    global heaps, clickedrow, nselected
    if clickedrow == "None":
        status.config(text = 'Please remove at least 1 matchstick!')
    else:
        heaps[clickedrow] -= nselected
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
    # If player made the "correct" move, computer will randomly make the next move.
    if hs(heaps) == 0:
        row = randint(1,4)
        while(heaps[row-1] == 0):
            row = randint(1,4)
        n = randint(1, heaps[row-1])
        heaps[row-1] -= n
        #print("After computer move: heaps is {} and nsum is {}. i is {}!".format(heaps, hs(heaps),str(row)))
        status.config(text = 'I haved moved ' + str(n) + ' matchstick(s) from row ' + str(row)+". Your turn now.")
        redraw()
        comradio.config(state="disabled")
        button.config(state="normal")
    
    # If player left computer the last matchstick:
    elif contains([0,0,0,1], heaps):
        heaps = [0, 0, 0, 0]
        status.config(text = 'You win! Press R to restart or Q to quit.')
        redraw()

    #If only a row of matchsticks left, i.e 3 empty rows:
    elif heaps.count(0) == 3:
        n = sum([ i if x != 0 else 0 for i,x in enumerate(heaps)])
        temp, heaps[n-1] = heaps[n-1], 1
        status.config(text = 'I have removed {} matchsticks from row {}. I win! Press R to restart or Q to quit.'.format(temp-1, n))
        redraw()

    # If heaps contains 2 empty rows and 1 row with only 1 matchstick left:
    elif contains([0,0,1], heaps) or contains([1,1,1], heaps):
        n = sum([ i if not (x == 0 or x == 1) else 0 for i,x in enumerate(heaps)])
        temp, heaps[n] = heaps[n], 0
        status.config(text = 'I have removed {} matchsticks from row {}.'.format(temp, n+1))
        button.config(state="normal")
        redraw()

    #If heaps contains 1 empty row and 2 rows of 1 matchsticks:
    elif contains([0,1,1], heaps):
        n = sum([ i if not (x == 0 or x == 1) else 0 for i,x in enumerate(heaps)])
        temp, heaps[n] = heaps[n], 1
        button.config(state="normal")
        status.config(text = 'I haved moved {} matchstick(s) from row {}. Your turn now.'.format(temp-1, n+1))
        redraw()

    # Algorithm for non-trivial cases not listed above
    else:
        comradio.config(state="disabled")
        nsum = hs(heaps)
        for i in range(4):
            test = heaps[i] - (nsum^heaps[i])
            temp = [ x if j != i else x - test for j,x in enumerate(heaps)]
            if test > 0:
                heaps[i] -= test
                #print("After computer move: heaps is {} and nsum is {}. i is {}!".format(heaps, hs(heaps),str(i)))
                status.config(text = 'My turn. I haved moved ' + str(test) + ' matchstick(s) from row ' + str(i+1))
                redraw()
                button.config(state="normal")
                break
    if contains([0,0,0,1], heaps):
        status.config(text = 'I win! Press R to restart or Q to quit.')
        button.config(state="disabled")
    if heaps == [0, 0, 0, 0]:
        status.config(text = 'You win! Press R to restart or Q to quit.')
        button.config(state="disabled")
        

comradio.bind('<Button-1>', cmove)

root.mainloop()


