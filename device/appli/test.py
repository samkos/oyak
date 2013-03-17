import Tkinter
import time

curtime = ''
clock = Tkinter.Label(  )
clock.pack(  )

def tick(  ):
    global curtime
    newtime = time.strftime('%H:%M:%S')
    if newtime != curtime:
        curtime = newtime
        clock.config(text=curtime)
    clock.after(200, tick)

tick(  )
clock.mainloop(  )
