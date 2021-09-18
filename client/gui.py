import tkinter as tk

SERVER_IP = None
SERVER_PORT = None
GAME_ID = None

import requests


class Firstframe(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.winfo_toplevel().title("The Game - Join")
        self.create_widgets()

    def create_widgets(self):
        self.server_ip = tk.Entry(self, textvariable=tk.StringVar(self, "localhost"))
        self.server_ip.grid(row=0, column=0)

        self.server_port = tk.Entry(self, textvariable=tk.StringVar(self, "5050"))
        self.server_port.grid(row=1, column=0)

        connect = tk.Button(self, text="Connect", command=self.connect)
        connect.grid(row=2, column=0)

    def connect(self):
        global SERVER_IP
        global SERVER_PORT
        SERVER_IP = self.server_ip.get()
        SERVER_PORT = self.server_port.get()

        self.change(Secondframe)

    def change(self, frame):
        frame_list = self.grid_slaves()
        for item in frame_list:
            item.destroy()
        frame(self)


class Secondframe(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.winfo_toplevel().title("The Game - Server")
        self.createWidgets()

    def createWidgets(self):
        self.playerLabel = tk.Label(self, text="Player Name")
        self.playerLabel.grid(row=0, column=1)

        self.playerOne = tk.Entry(self)
        self.playerOne.grid(row=1, column=1)

        self.gameName = tk.Entry(self)
        self.gameName.grid(row=3, column=0)

        createGame = tk.Button(self, text="Create Game", command=self.create_game)
        createGame.grid(row=4, column=0)

        # TODO Make new frame when button is pressed -> Reload if Call fails

        print(GAME_ID)
        game_id_label = tk.Label(self, text=GAME_ID)
        game_id_label.grid(row=5, column=0)

        self.gameID = tk.Entry(self)
        self.gameID.grid(row=3, column=2)

        joinGame = tk.Button(self, text="Join Game", command=self.join_game)
        joinGame.grid(row=4, column=2)

    def create_game(self):
        global GAME_ID
        game_name = self.gameName.get()
        response = requests.post("http://" + SERVER_IP + ":" + SERVER_PORT + "/game/" + game_name)

        GAME_ID = response.content.decode()


    def join_game(self):
        game_id = self.gameID.get()
        response = requests.get("http://" + SERVER_IP + ":" + SERVER_PORT + "/game/" + game_id)

        print(response)

def main():
    root = tk.Tk()
    root.geometry("600x400")
    app = Firstframe(master=root)
    app.mainloop()
