# from tkinter import *
import tkinter

class WindowManager:
    def __init__(self, title, width, height, callback):
        self.width = width
        self.height = height

        self.window = tkinter.Tk()
        self.window.title(title)

        self.searchEntry = tkinter.Entry(self.window, width=int(width/2))
        self.searchEntry.pack()

        self.search_button = tkinter.Button(self.window, text="Go", command=callback)
        self.search_button.pack()

        self.window.geometry(str(width)+"x"+str(height))

        self.labels = []

    def add_label(self, text):
        w = tkinter.Label(self.window, text=text, anchor='w')
        w.pack(fill='both')
        self.labels.append(w)

    def remove_labels(self):
        for label in self.labels:
            label.pack_forget()

    def run(self):
        self.window.mainloop()
