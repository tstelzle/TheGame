import tkinter as tk

class Firstframe(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.winfo_toplevel().title("The Game")
        self.createWidgets()

    def createWidgets(self):
        self.playerLabel = tk.Label(self, text="Player Name")
        self.playerLabel.grid(row=0, column=1)

        self.playerOne = tk.Entry(self)
        self.playerOne.grid(row=1, column=1)

        self.gameName = tk.Entry(self)
        self.gameName.grid(row=3, column=0)

        self.createGame = tk.Button(self, text="Create Game")
        self.createGame.grid(row=4, column=0)

        self.gameID = tk.Entry(self)
        self.gameID.grid(row=3, column=2)

        self.joinGame = tk.Button(self, text="Join Game")
        self.joinGame.grid(row=4, column=2)

def main():
    root = tk.Tk()
    root.geometry("600x400")
    app = Firstframe(master=root)
    app.mainloop()