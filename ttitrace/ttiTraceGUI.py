from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog as fd
import ttiTrace


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        e = StringVar()
        self.nameInput = Entry(self, textvariable=e, width=50)
        e.set('please input file path here or select a file')
        self.nameInput.pack(pady=10, ipady=5)

        e1 = StringVar()
        self.size = Entry(self, textvariable=e1, width=50)
        e1.set('please input averaging size(default is 100)')
        self.size.pack(pady=10, ipady=5)

        self.alertButton = Button(self, text='select file', width=15,  command=self.chooseFile)
        self.alertButton.pack(pady=10)
        self.alertButton = Button(self, text='start', width=15, command=self.start)
        self.alertButton.pack(pady=10)

    def start(self):
        name = self.nameInput.get()
        size = self.size.get()
        if name == "" or name.startswith("please"):
            messagebox.showinfo('Message', 'please input file path or select a file')
        if int(size) <= 1:
            messagebox.showinfo('Message', 'please input correct averaging size')
        if name.endswith(".txt"):
            ttiTrace.readAndShow(name)
        elif name.endswith(".csv"):
            ttiTrace.analyseCsv(name, size)
            ttiTrace.readAndShow(name.replace(".csv", "_" + size + ".txt"))


    def chooseFile(self):
        self.nameInput.delete(0, END)
        self.size.delete(0, END)
        self.size.insert(0, "100")
        fileName = fd.askopenfilename()
        self.nameInput.insert(0, fileName)


app = Application()
app.master.geometry("450x250")
# 设置窗口标题:
app.master.title('ttiTrace')
# 主消息循环:
app.mainloop()



