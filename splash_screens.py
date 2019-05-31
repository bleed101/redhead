from tkinter import *
#root=Tk()
#root.title('CREATOR')
#root.geometry("700x400+250+167")
#img1=PhotoImage(file='C:/Users/nephilim/Desktop/game/me.gif')
#def me(e):
    #root.destroy()
root3=Tk()
root3.title('DVOLT')
root3.geometry("700x400+250+167")
img=PhotoImage(file='C:/Users/nephilim/Desktop/game/splash.gif')

def fun():
        root3.destroy()
        root1=Tk()
        root1.title('Instruction')
        root1.geometry("700x400+250+167")
        img2=PhotoImage(file='C:/Users/nephilim/Desktop/game/instruction.gif')
        def ins():
            root1.destroy()
        i=Label(root1,image=img2)
       # i.bind('<Motion>',ins)
        i.after(5000,ins)
        i.pack()
        root1.mainloop()
s=Label(root3,image=img)
    #s.bind('<Motion>',fun)
s.after(2500,fun)
s.pack()

  #  root3.mainloop()
m=Label(root3,image=img)
m.bind('<Motion>',fun)
m.pack()
root3.mainloop()
import link_DBA
