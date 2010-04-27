from Tkinter import *

class AutoScrollbar(Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"

#############################################################
class Test(Canvas):
    def __init__(self,boss):
        Canvas.__init__(self,boss)

        for a in range(100):
            t=Button(self,text=str(a)+' Blablabla')
            t.grid(sticky=E+W)
        
#############################################################
class Fenetre_principale(Frame):
    """Constructeur fenêtre principale"""
    def __init__(self,boss=None):
        Frame.__init__(self)

        self.b=Label(self.master,text='Un label bien long pour qu''il puisse prendre au moins toute la largeur de la fenetre')
        self.b.grid(row=0,column=0,sticky=E+W)

        self.c=Canvas(self.master)
        self.c.grid(row=1,column=0)

        self.vscrollbar = AutoScrollbar(self.c)
        self.vscrollbar.grid(row=1, column=1, sticky=N+S)
        self.hscrollbar = AutoScrollbar(self.c, orient=HORIZONTAL)
        self.hscrollbar.grid(row=2, column=0, sticky=E+W)

        self.canvas = Canvas(self.c,
                        yscrollcommand=self.vscrollbar.set,
                        xscrollcommand=self.hscrollbar.set)
        self.canvas.grid(row=1, column=0, sticky=N+S+E+W)

        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

        self.c.grid_rowconfigure(1, weight=1)
        self.c.grid_columnconfigure(0, weight=1)

# Avec cette ligne le résultat n'est pas tel que voulu. 
        self.truc=Test(self.canvas)

# Avec cette solution, ça marche bien
#        self.truc=Canvas(self.canvas)

#        for a in range(100):
#            t=Button(self.truc,text=str(a)+' Blablabla')
#            t.grid(sticky=E+W)


        self.canvas.create_window(0, 0, anchor=NW, window=self.truc)
        self.truc.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

if __name__=='__main__':
    
    Fenetre_principale().mainloop()

