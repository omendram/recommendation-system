'''
Integrates all files
'''
import tkinter
from tkinter import ttk
 
class RS(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()
 
    def init_gui(self):
        """Builds GUI."""
        self.root.title('Recommender System')
        self.grid(column=0, row=0, sticky='nsew')

        self.p = ttk.LabelFrame(self, height=300)
        self.p.grid(column=0,row=0,columnspan=5, sticky='news')
        
        self.f = ttk.LabelFrame(self, text='A', height=100)
        self.f.grid(column=0, row=10, columnspan=5, sticky='news')
        
        self.l = ttk.Label(self.f, text='')
        self.l.grid(column=0, row=0)

        self.b = ttk.Button(self.f, text='Upload')
        self.b.grid(column=0, row=0, rowspan=3)

        self.e = ttk.Entry(self.f, width=30)
        self.e.grid(column=1,row=0, sticky='ew')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
 
if __name__ == '__main__':
    root = tkinter.Tk()
    RS(root)
    root.mainloop()
