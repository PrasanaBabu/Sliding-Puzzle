from tkinter import *
from tkinter.ttk import Entry,Button,OptionMenu
from PIL import Image,ImageTk
import random
import tkinter.filedialog
import os

class node:
      def __init__(self,name,moves,nextnode=None):
            self.name=name
            self.moves=moves
            self.nextnode=nextnode

      def getname(self):
            return self.name

      def setname(self,name):
            self.name=name

      def setmoves(self,moves):
            self.moves=moves

      def getmoves(self):
            return self.moves

      def getnextnode(self):
            return self.nextnode

      def setnextnode(self,nextnode):
            self.nextnode=nextnode

class LinkedList:
      def __init__(self,head=None):
            self.head=head
            self.tail=None
            self.size=0

      def addnodeF(self,name,moves):
            newnode=node(name,moves,self.head)
            self.head=newnode
            self.size+=1
      
class Tiles():
      def __init__(self,grid):
            self.tiles=[]
            self.grid=grid
            self.gap=None
            self.moves=0
            
            
      def add(self,tile):
            self.tiles.append(tile)

      def getTile(self,*pos):
            for tile in self.tiles:
                  if tile.pos==pos:
                        return tile                        

      def getTileAroundGap(self):
            gRow,gCol=self.gap.pos
            return self.getTile(gRow,gCol-1),self.getTile(gRow-1,gCol),self.getTile(gRow,gCol+1),self.getTile(gRow+1,gCol)

      def changeGap(self,tile):
            try:
                  gPos=self.gap.pos
                  self.gap.pos=tile.pos
                  tile.pos=gPos
                  self.moves+=1
            except:
                  pass

      def slide(self,key):
            left,top,right,down=self.getTileAroundGap()
            if key=='Up':
                  self.changeGap(down)
                  
            if key=='Down':
                  self.changeGap(top)
                  
            if key=='Left':
                  self.changeGap(right)
                 
            if key=='Right':
                  self.changeGap(left)
                  
            self.show()
                  
      def shuffle(self):
            random.shuffle(self.tiles)
            i=0
            for row in range(self.grid):
                  for col in range(self.grid):
                        self.tiles[i].pos=(row,col)
                        i+=1
      def show(self):
            for tile in self.tiles:
                  if self.gap!=tile:
                        tile.show()

      def setGap(self,index):
            self.gap=self.tiles[index]           

      def isCorrect(self):
            for tile in self.tiles:
                  if not tile.isCorrectPos():
                        return False
            return True

      
class Tile(Label):
      def __init__(self,parent,image,pos):
            Label.__init__(self,parent,image=image)

            self.image=image
            self.pos=pos
            self.curPos=pos

      def show(self):
            self.grid(row=self.pos[0],column=self.pos[1])

      def isCorrectPos(self):
            return self.pos==self.curPos


class Board(Frame):
      MAX_BOARD_SIZE=500
      def __init__(self,parent,image,grid,win,*args,**kwargs):
            Frame.__init__(self,parent,*args,**kwargs)
            self.parent=parent
            self.stack=[]
            self.grid=grid
            self.win=win
            self.image=self.openImage(image)
            self.tileSize=self.image.size[0]/self.grid
            undoButton=Button(parent,text="UNDO",command=self.undo)
            undoButton.pack()
            self.tiles=self.createTiles()
            self.tiles.shuffle()
            self.tiles.show()
            self.bindKeys()
            

      def undo(self):
            if self.stack!=[]:
                  key=self.stack.pop()
                  if key=='Up':
                        self.tiles.slide('Down')
                  if key=='Down':
                        self.tiles.slide('Up')
                  if key=='Left':
                        self.tiles.slide('Right')
                  if key=='Right':
                        self.tiles.slide('Left')                            

      def openImage(self,image):

            image=Image.open(image)
            if min(image.size)>self.MAX_BOARD_SIZE:
                  image=image.resize((self.MAX_BOARD_SIZE,self.MAX_BOARD_SIZE),Image.ANTIALIAS)
            if image.size[0]!=image.size[1]:
                  image=image.crop((0,0,image.size[0],image.size[0]))

            return image

      def bindKeys(self):

            self.bind_all('<Key-Up>',self.slide)            
            self.bind_all('<Key-Down>',self.slide)            
            self.bind_all('<Key-Left>',self.slide)
            self.bind_all('<Key-Right>',self.slide)

      def slide(self,event):
            if event.keysym=='Up':
                  self.stack.append('Up')
            if event.keysym=='Down':
                  self.stack.append('Down')
            if event.keysym=='Left':
                  self.stack.append('Left')
            if event.keysym=='Right':
                  self.stack.append('Right')
            self.tiles.slide(event.keysym)
            if self.tiles.isCorrect():
                  self.win(self.tiles.moves)
                             
      def createTiles(self):

            tiles=Tiles(self.grid)
            for row in range(self.grid):
                  for col in range(self.grid):
                        x0=col*self.tileSize
                        y0=row*self.tileSize
                        x1=x0+self.tileSize
                        y1=y0+self.tileSize
                        tileImage=ImageTk.PhotoImage(self.image.crop((x0,y0,x1,y1)))
                        tile=Tile(self,tileImage,(row,col))
                        tiles.add(tile)
            tiles.setGap(-1)
            return tiles

class Main():
      def __init__(self,parent):
            self.parent=parent
            self.highscores=[]
            self.image=StringVar()
            self.winText=StringVar()
            self.grid=IntVar()
            self.A=LinkedList()
            self.createWidgets()

      def createWidgets(self):
            self.mainFrame=Frame(self.parent)
            Label(self.mainFrame,text='Sliding Puzzle',font=('',50)).pack(padx=10,pady=10)
            frame=Frame(self.mainFrame)
            Label(frame,text='Image').grid(sticky=W)
            Entry(frame,textvariable=self.image,width=50).grid(row=0,column=1,padx=10,pady=10)
            Button(frame,text='Browse',command=self.browse).grid(row=0,column=2,pady=10,padx=10)
            Label(frame,text='Grid').grid(sticky=W)
            OptionMenu(frame,self.grid,*[2,3,4,5,6,7,8,9,10]).grid(row=1,column=1,padx=10,pady=10,sticky=W)
            frame.pack(padx=10,pady=10)
            Label(frame,text='Enter your name :').grid(row=2,column=0,padx=10,pady=10)
            self.Name=StringVar()
            NameEntry=Entry(frame,textvariable=self.Name)
            NameEntry.grid(row=2,column=1,padx=10,pady=10)
            Button(self.mainFrame,text='Start',command=self.start).pack(padx=10,pady=10)            
            Button(self.mainFrame,text='Scores',command=self.scores).pack(padx=10,pady=10)
            self.mainFrame.pack()
            self.board=Frame(self.parent)
            self.winFrame=Frame(self.parent)
            Label(self.winFrame,textvariable=self.winText,font=('',50)).pack(padx=10,pady=10)
            
            Button(self.winFrame,text="Play Again",command=self.playAgain).pack(padx=10,pady=10)

      def scores(self):
          c=self.A.head
          while c :
                print((c.getname(),c.getmoves()))
                c=c.getnextnode()
            
      def start(self):
            self.name=str(self.Name.get())
            image=self.image.get()
            grid=self.grid.get()
            if os.path.exists(image):
                  self.board=Board(self.parent,image,grid,self.win)
                  self.mainFrame.pack_forget()
                  self.board.pack()
                  
      def browse(self):
            self.image.set(tkinter.filedialog.askopenfilename(title='Select Image',filetype=(("png File","*png"),("jpg File","*jpg"))))

      def addscore(self,moves):
            self.A=LinkedList()
            self.A.addnodeF(self.name,moves)
            

      def win(self,moves):
            self.board.pack_forget()
            self.addscore(moves)
            self.winText.set("Congrats {0} You win with {1} moves".format(self.name,moves))
            self.winFrame.pack()

      def playAgain(self):
            self.winFrame.pack_forget()
            self.mainFrame.pack()
           
if __name__ =="__main__":
      root=Tk()
      Main(root)                                                                 
      root.mainloop()
