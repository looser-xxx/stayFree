import tkinter as tk
from tkinter import scrolledtext, filedialog


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.title("Text Editor with Line Numbers")
        self.backGroundCol='#1e1f22'
        self.textColor="#a3a3a3"
        self.sideNumberColor='#575757'
        self.root.background = self.backGroundCol
        # --- 1. Create the Layout ---
        # Create the canvas for the line numbers
        self.lineNumberCanvas = tk.Canvas(self.root, width=20, bg=self.backGroundCol,borderwidth=0, highlightthickness=0)
        self.lineNumberCanvas.pack(side=tk.LEFT, fill='y')
        self.root.option_add("*Menu.font",("Consolas",20,"bold"))
        self.createMenuBar()
        # Create the text area
        self.textArea = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 14),
            bg=self.backGroundCol,
            fg=self.textColor,
            insertbackground="white",
            borderwidth=0,
            highlightthickness=0
        )
        self.textArea.pack(expand=True, fill='both')

        self.textArea.tag_config("cursor", underline=True)
        self.updateLoopId = None
        self.textArea.vbar.config(borderwidth=0)
        self.setupBindings()
        self.updateLineNumbers()  # Draw the initial line number

    def updateLineNumbers(self, event=None):
        # Clear the old line numbers
        self.lineNumberCanvas.delete("all")

        # Get the number of lines in the text area
        # 'end-1c' gets the position of the last character, '.split('.')[0]' gets the line number
        lineCount = int(self.textArea.index('end-1c').split('.')[0])

        # Get the first visible line's index
        firstVisibleLineIndex = int(self.textArea.index("@0,0").split('.')[0])

        for i in range(lineCount):
            lineNumber = i + 1
            # Calculate the y-position for each line number
            # We subtract the first visible line to align scrolling
            yPosition = (i - firstVisibleLineIndex+1.6) * 22  # 20 is an estimate for line height

            # Draw the line number on the canvas
            self.lineNumberCanvas.create_text(
                10, yPosition, text=str(lineNumber), fill=self.sideNumberColor, anchor='center'
            )
        return "break"

    def setupBindings(self):
        # --- 3. Synchronize on every key press and scroll ---
        self.textArea.bind("<KeyRelease>", self.updateLineNumbers)
        self.textArea.bind("<MouseWheel>", self.updateLineNumbers)
        self.textArea.bind("<FocusIn>", self.startUpdateLoop)
        self.textArea.bind("<FocusOut>", self.stopUpdateLoop)

        # This makes the line numbers scroll along with the text area's scrollbar
        self.textArea.vbar.config(command=self.onScroll)

    def onScroll(self, *args):
        # This is called when the scrollbar is used
        self.textArea.yview(*args)
        self.updateLineNumbers()

    # (Include your other methods like startUpdateLoop, stopUpdateLoop, etc., here)
    # ...

    def updateCursor(self):
        if not self.textArea.winfo_exists(): return
        self.textArea.tag_remove("cursor", "1.0", tk.END)
        self.textArea.tag_add("cursor", tk.INSERT)
        self.updateLoopId = self.root.after(100, self.updateCursor)

    def startUpdateLoop(self, event=None):
        if self.updateLoopId is None: self.updateCursor()

    def stopUpdateLoop(self, event=None):
        if self.updateLoopId:
            self.root.after_cancel(self.updateLoopId)
            self.updateLoopId = None
        if self.textArea.winfo_exists(): self.textArea.tag_remove("cursor", "1.0", tk.END)

    def createMenuBar(self):
        mainMenu = tk.Menu(self.root)
        self.root.config(menu=mainMenu)

        # --- 2. Create the "File" Dropdown Menu ---
        # The tearoff=0 removes the dashed line at the top of the dropdown
        fileMenu = tk.Menu(mainMenu,
                           tearoff=0,
                           background = self.backGroundCol,  # Background of the dropdown
                           foreground = self.textColor,  # Text color
                           activebackground = "#8f8f8f",  # Highlight color on hover
                           activeforeground = self.backGroundCol,
                           borderwidth=0,
                           )

        # --- 4. Attach the "File" dropdown to the main bar ---
        mainMenu.add_cascade(label="File", menu=fileMenu)

        # --- 3. Add Commands to the "File" Dropdown ---
        fileMenu.add_command(label="New", command=self.newFile)
        fileMenu.add_command(label="Open...", command=self.openFile)
        fileMenu.add_command(label="Save", command=self.saveFile)
        fileMenu.add_separator()  # Adds a dividing line
        fileMenu.add_command(label="Exit", command=self.root.quit)

        # --- Create the "Edit" Dropdown Menu (example) ---
        editMenu = tk.Menu(mainMenu, tearoff=0,
                           background = self.backGroundCol,  # Background of the dropdown
                           foreground = self.textColor,  # Text color
                           activebackground="#8f8f8f",  # Highlight color on hover
                           activeforeground=self.backGroundCol,
                           borderwidth=0,
                           )
        mainMenu.add_cascade(label="Edit", menu=editMenu)

        editMenu.add_command(label="Cut", command=lambda: self.textArea.event_generate("<<Cut>>"))
        editMenu.add_command(label="Copy", command=lambda: self.textArea.event_generate("<<Copy>>"))
        editMenu.add_command(label="Paste", command=lambda: self.textArea.event_generate("<<Paste>>"))

    # --- Placeholder functions for the commands ---
    def newFile(self):
        self.textArea.delete("1.0", tk.END)
        print("New File Created")
    def openFile(self):
        filePath = filedialog.askopenfilename()
        if filePath:
            with open(filePath, "r") as file:
                self.textArea.delete("1.0", tk.END)
                self.textArea.insert("1.0", file.read())
            print(f"Opened file: {filePath}")
    def saveFile(self):
        filePath = filedialog.asksaveasfilename()
        if filePath:
            with open(filePath, "w") as file:
                file.write(self.textArea.get("1.0", tk.END))
            print(f"Saved file: {filePath}")

    def run(self):
        self.textArea.focus_set()
        self.startUpdateLoop()
        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()