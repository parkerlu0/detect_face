import tkinter as tk

class Score(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.score = 0
        self.scoredis = tk.Label(master, height=5, width=10, textvariable="")
        self.scoredis.config(text="0")
        self.scoredis.pack()
        #self.start_button = tk.Button(master,text="Count", width=8, height=4, command=self.addScore)
        #self.start_button.pack()

    def getScore(self):
        return score
        print(score)
    
    def addScore(self):
        self.score +=100
        self.scoredis.config(text="%d" % self.score)

#root = tk.Tk()
#cd = Score(root)
#cd.mainloop()