#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
from Tkinter import *
 
class keyboard:
    def __init__(self,root):
        frame = Frame(root)
        i=0
        for c in "AZERTYUIOP" :
            print c
            labelKey=Button(frame,text="X")
            labelKey.pack()
            i=i+1
        frame.pack()

if __name__=='__main__':
    root=Tk()
    app=keyboard(root)
    root.mainloop()
    
