import tkinter as tk

class app:
    oya_dict = {0:"", 1:"Right", 2:"top", 3:"left"}
    bakaze_dict = {0:"EAST", 1:"SOUTH", 2:"WEST", 3:"NORTH"}

    def __init__(self, master):
        self.master = master
        self.master.geometry("500x500")
        self.start()
        self.score = [25000, 25000, 25000, 25000]
        self.bakaze = 0
        self.oya = 0

    def start(self):
        for i in self.master.winfo_children():
            i.pack_forget()
        self.startFrame = tk.Frame(self.master)
        self.startFrame.pack()
        tk.Label(self.startFrame, text="Mahjong Score Calculator").pack()
        self.startBtn = tk.Button(self.startFrame, text="Get Started", command=self.init_score_input)
        self.startBtn.pack()

    def init_score_input(self):
        for i in self.master.winfo_children():
            i.pack_forget()
        self.inputFrame = tk.Frame(self.master)
        self.inputFrame.pack()

        tk.Label(self.inputFrame, text="Set initial score").pack()

        default_val = tk.StringVar(value="25000") # initial value
        self.initialScore = tk.Entry(self.inputFrame, textvariable=default_val)
        self.initialScore.pack()

        # Set Oya
        tk.Label(self.inputFrame, text = "Select Oya:").pack()
        setOya = tk.IntVar()
        self.oya_rad1 = tk.Radiobutton(self.inputFrame, text = "Player", variable=setOya, value = 0)
        self.oya_rad1.pack()
        self.oya_rad2 = tk.Radiobutton(self.inputFrame, text = "Right Player", variable=setOya, value = 1)
        self.oya_rad2.pack()
        self.oya_rad3 = tk.Radiobutton(self.inputFrame, text = "Top Player", variable=setOya, value = 2)
        self.oya_rad3.pack()
        self.oya_rad4 = tk.Radiobutton(self.inputFrame, text = "Left Player", variable=setOya, value = 3)
        self.oya_rad4.pack()

        # Set Bakaze
        tk.Label(self.inputFrame, text = "Select Bakaze").pack()
        setBakaze = tk.IntVar()
        self.bakaze_rad1 = tk.Radiobutton(self.inputFrame, text = "E", variable=setBakaze, value = 0)
        self.bakaze_rad1.pack()
        self.bakaze_rad2 = tk.Radiobutton(self.inputFrame, text = "S", variable=setBakaze, value = 1)
        self.bakaze_rad2.pack()
        self.bakaze_rad3 = tk.Radiobutton(self.inputFrame, text = "W", variable=setBakaze, value = 2)
        self.bakaze_rad3.pack()
        self.bakaze_rad4 = tk.Radiobutton(self.inputFrame, text = "N", variable=setBakaze, value = 3)
        self.bakaze_rad4.pack()

        self.scoreBtn = tk.Button(self.inputFrame, text="Set", command=lambda:self.init_params([self.initialScore.get(), self.initialScore.get(), self.initialScore.get(), self.initialScore.get()], setOya, setBakaze))
        self.scoreBtn.pack()

    def init_params(self, scores, current_oya, current_bakaze):
        self.score = scores
        self.oya = current_oya.get()
        self.bakaze = current_bakaze.get()

        self.main_screen()

    
    def main_screen(self):
        # kaze: 0~3 ESWN (in order)
        # score 0~3 player->right->top->left
        # oya 0~3 player->right->top->left
        for i in self.master.winfo_children():
            i.pack_forget()
        self.mainFrame = tk.Frame(self.master)
        self.mainFrame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)

        tk.Label(self.mainFrame, text=self.oya_dict[self.oya]+" Player is Oya", fg="blue").pack()

        self.scorePanel = tk.LabelFrame(self.mainFrame, text = "Scores", width=200, height=200)
        self.scorePanel.pack(anchor=tk.N, side=tk.TOP, pady=10, fill=tk.BOTH, expand=False)
        # player at top
        self.topPlayerFrame = tk.Frame(self.scorePanel)
        self.topPlayerFrame.pack(side=tk.TOP, padx=10)
        tk.Label(self.topPlayerFrame, text="Top Player").pack()
        self.topPlayerLabel = tk.Label(self.topPlayerFrame, text=self.score[2])
        self.topPlayerLabel.pack()

        # player at bottom
        self.bottomPlayerFrame = tk.Frame(self.scorePanel)
        self.bottomPlayerFrame.pack(side=tk.BOTTOM, padx=10)
        tk.Label(self.bottomPlayerFrame, text="Player").pack()
        self.playerLabel = tk.Label(self.bottomPlayerFrame, text=self.score[0])
        self.playerLabel.pack()

        # player at right
        self.rightPlayerFrame = tk.Frame(self.scorePanel)
        self.rightPlayerFrame.pack(side=tk.RIGHT, padx=10)
        tk.Label(self.rightPlayerFrame, text="Right Player").pack()
        self.rightPlayerLabel = tk.Label(self.rightPlayerFrame, text=self.score[1])
        self.rightPlayerLabel.pack()

        # player at left
        self.leftPlayerFrame = tk.Frame(self.scorePanel)
        self.leftPlayerFrame.pack(side=tk.LEFT, padx=10)
        tk.Label(self.leftPlayerFrame, text="Left Player").pack()
        self.leftPlayerLabel = tk.Label(self.leftPlayerFrame, text=self.score[3])
        self.leftPlayerLabel.pack()

        tk.Label(self.scorePanel, text = self.bakaze_dict[self.bakaze]).pack(side=tk.TOP, pady=100)

        self.ronBtn = tk.Button(self.mainFrame, text="Ron")
        self.ronBtn.pack()
        self.tsumoBtn = tk.Button(self.mainFrame, text="Tsumo")
        self.tsumoBtn.pack()

        # def ron_score_calc(self, winner): calculate and update frame
        # def tsumo_score_calc(self, winner): 
    def result_screen(self, scoreDiff, newOya):
        for i in self.master.winfo_children():
            i.pack_forget()
        self.mainFrame = tk.Frame(self.master)
        self.mainFrame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        if newOya:
            tk.Label(self.mainFrame, text="New Oya: "+self.oya_dict[self.oya], fg="red").pack()
        else :
            tk.Label(self.mainFrame, text=self.oya_dict[self.oya]+" Player is Oya").pack()

        self.scorePanel = tk.LabelFrame(self.mainFrame, text = "Scores", width=200, height=200)
        self.scorePanel.pack(anchor=tk.N, side=tk.TOP, pady=10, fill=tk.BOTH, expand=False)
        # player at top
        self.topPlayerFrame = tk.Frame(self.scorePanel)
        self.topPlayerFrame.pack(side=tk.TOP, padx=10)
        tk.Label(self.topPlayerFrame, text="Top Player").pack()
        tk.Label(self.topPlayerFrame, text="("+ "+" if scoreDiff[2]>=0 else "-" + scoreDiff[2]+")", fg="blue").pack()
        self.topPlayerLabel = tk.Label(self.topPlayerFrame, text=self.score[2])
        self.topPlayerLabel.pack()

        # player at bottom
        self.bottomPlayerFrame = tk.Frame(self.scorePanel)
        self.bottomPlayerFrame.pack(side=tk.BOTTOM, padx=10)
        tk.Label(self.bottomPlayerFrame, text="Player").pack()
        tk.Label(self.bottomPlayerFrame, text="("+ "+" if scoreDiff[0]>=0 else "-" + scoreDiff[0]+")", fg="blue").pack()
        self.playerLabel = tk.Label(self.bottomPlayerFrame, text=self.score[0])
        self.playerLabel.pack()

        # player at right
        self.rightPlayerFrame = tk.Frame(self.scorePanel)
        self.rightPlayerFrame.pack(side=tk.RIGHT, padx=10)
        tk.Label(self.rightPlayerFrame, text="Right Player").pack()
        tk.Label(self.rightPlayerFrame, text="("+ "+" if scoreDiff[1]>=0 else "-" + scoreDiff[1]+")", fg="blue").pack()
        self.rightPlayerLabel = tk.Label(self.rightPlayerFrame, text=self.score[1])
        self.rightPlayerLabel.pack()

        # player at left
        self.leftPlayerFrame = tk.Frame(self.scorePanel)
        self.leftPlayerFrame.pack(side=tk.LEFT, padx=10)
        tk.Label(self.leftPlayerFrame, text="Left Player").pack()
        tk.Label(self.leftPlayerFrame, text="("+ "+" if scoreDiff[3]>=0 else "-" + scoreDiff[3]+")", fg="blue").pack()
        self.leftPlayerLabel = tk.Label(self.leftPlayerFrame, text=self.score[3])
        self.leftPlayerLabel.pack()

        tk.Label(self.scorePanel, text = self.bakaze_dict[self.bakaze]).pack(side=tk.TOP, pady=100)

        # return to main screen
        tk.Button(self.mainFrame, text="Confirm", self.conmmand=main_screen).pack()

root = tk.Tk()
root.title("Mahjong Score Calc")
root.resizable(width=False, height=False)
app(root)
root.mainloop()