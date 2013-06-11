#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
from Tkinter import *
 
class scrollCanvas:
    def __init__(self,root):
        frame = Frame(root)
        frame.grid()        
        self.xScrollbar = Scrollbar(frame, orient=HORIZONTAL)
        self.xScrollbar.grid(row=1, column=0, sticky=E+W)
        self.yScrollbar = Scrollbar(frame)
        self.yScrollbar.grid(row=0, column=1, sticky=N+S)
        self.myCanvas = Canvas(frame, bd=0,width=300,height=300,
                        scrollregion=(0,0,1000,1000),
                        xscrollcommand=self.xScrollbar.set,
                        yscrollcommand=self.yScrollbar.set)
        self.myCanvas.grid(row=0, column=0)
        self.myCanvas.create_line(0,0,100,250)
        frame.pack()
        self.xScrollbar.config(command=self.myxScroll)
        self.yScrollbar.config(command=self.myCanvas.yview)
        
    def myxScroll(self,move,x=0,page=None):
        '''move peut prendre 2 valeurs : 'moveto' et 'scroll'
        Dans le cas de moveto, val est compris entre 0.0 et 1.0, page
        =None.
        Dans le cas de scroll,page vaut pages, et x = 1
        '''
        self.myCanvas.xview(move,x,page)
        if page:
            y=x
        else:
            y=float(x)/2
        self.myCanvas.yview(move,y,page)
        
if __name__=='__main__':
    root=Tk()
    app=scrollCanvas(root)
    root.mainloop()
    
