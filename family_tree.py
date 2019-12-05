import tkinter as tk
import tkinter.filedialog

import os.path

from html_parser import htmlParser
from resources.strings import Strings
from resources.errors import ExtensionError

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.selectedFilePath = tk.Text(self)
        self.selectedFilePath.insert(tk.INSERT, Strings.get("selectedFilePlaceholder"))
        self.selectedFilePath.pack(side="top", fill=tk.BOTH, expand=True)

        self.selectFileButton = tk.Button(self)
        self.selectFileButton["text"] = Strings.get("selectFileButton")
        self.selectFileButton["command"] = self.selectFile
        self.selectFileButton.pack(side="top", fill=tk.BOTH, expand=True)

        self.treeVisualizer = tk.Button(self)
        self.treeVisualizer["text"] = Strings.get("visualizeButton")
        self.treeVisualizer["command"] = self.visualizeTree
        self.treeVisualizer.pack(side="top", fill=tk.BOTH, expand=True)

        self.quit = tk.Button(self, text="QUIT", fg="white", bg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom", fill=tk.BOTH, expand=True)

    def visualizeTree(self):
        print("Starting Treeification...")
        sourceFilePath = self.selectedFilePath.get(1.0, "end-1c")

        try:
            sf = open(sourceFilePath, encoding="utf8").read()
            extension = os.path.splitext(sourceFilePath)[1]
            print(extension)
            if extension != ".html":
                raise ExtensionError
        except ExtensionError:
            print("Not an HTML file")
            print("Treefication Aborted.")
            return
        except:
            print("Can't open file")
            print("Treefication Aborted.")
            return

        parser = htmlParser(sf)
        parser.parse()

        print("Treefication Completed...")

    def selectFile(self):
        print("Waiting for File Selection...")
        sourceFilePath = tk.filedialog.askopenfilename(parent = root, title = Strings.get("selectFileTitle"),filetypes = (("Hmtl Files","*.html"),("All Files","*.*")))
        self.selectedFilePath.delete(1.0, tk.END)
        self.selectedFilePath.insert(tk.INSERT, sourceFilePath)
        print("File Selected.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()