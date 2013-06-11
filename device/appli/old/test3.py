from Tkinter import *


#############################################################
class Fenetre_principale(Frame):
    """Constructeur fenêtre principale"""
    def __init__(self,boss=None):
        Frame.__init__(self)


        self.c=Canvas(self.master)
        self.c.grid(row=1,column=0)

        self.vscrollbar = Scrollbar(self.c)
        self.vscrollbar.grid(row=1, column=1, sticky=N+S)

        self.canvas = Canvas(self.c,
                        yscrollcommand=self.vscrollbar.set)
        self.canvas.grid(row=1, column=0, sticky=N+S+E+W)

        self.vscrollbar.config(command=self.canvas.yview)

        self.c.grid_rowconfigure(0, weight=1)
        self.c.grid_columnconfigure(0, weight=1)

# Avec cette solution, ça marche bien
        self.truc=Canvas(self.canvas)

        for a in range(100):
            t=Button(self.truc,text=str(a)+' Blablabla')
            t.grid(sticky=E+W)


        self.canvas.create_window(0, 0, anchor=NW, window=self.truc)
        self.truc.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

if __name__=='__main__':
    
    Fenetre_principale().mainloop()

