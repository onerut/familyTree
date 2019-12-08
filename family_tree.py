import tkinter as tk
import tkinter.filedialog

import os.path

from html_parser import parser
from tree import node

from resources.strings import Strings
from resources.errors import ExtensionError

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.top = tk.Frame(self)
        self.bottom = tk.Frame(self)
        self.top.pack(side="top")
        self.bottom.pack(side="bottom", fill=tk.X)


        self.canvas = tk.Canvas(self,width = self.master.winfo_width()/2, height = self.master.winfo_height() - 100)
        self.canvas.pack(in_= self.top,side="left", expand=True)

        self.display_frame = tk.Frame(self,width = self.master.winfo_width()/2, height = self.master.winfo_height() - 100)
        self.display_frame.pack(in_= self.top,side="right", expand=True)

        self.selected_file_path = tk.Entry(self)
        self.selected_file_path.insert(tk.INSERT, Strings.get("selectedFilePlaceholder"))
        self.selected_file_path.pack(in_= self.bottom,side="top", fill=tk.X)

        self.select_file_button = tk.Button(self)
        self.select_file_button["text"] = Strings.get("selectFileButton")
        self.select_file_button["command"] = self.select_file
        self.select_file_button.pack(in_= self.bottom,side="top", fill=tk.X)

        self.tree_visualizer_button = tk.Button(self)
        self.tree_visualizer_button["text"] = Strings.get("visualizeButton")
        self.tree_visualizer_button["command"] = self.visualize_tree
        self.tree_visualizer_button.pack(in_= self.bottom,side="top", fill=tk.X)

        self.quit = tk.Button(self, text="QUIT", fg="white", bg="red",
                              command=self.master.destroy)
        self.quit.pack(in_= self.bottom,side="bottom", fill=tk.X)

    def visualize_tree(self):
        print("Starting Treeification...")

        #Parse the selected file
        p = parser(self.open_file())
        family_members = p.parse()

        print("Parsing Completed.")

        #Treeify the List
        tree_root = self.treeify(family_members)

        print("Treeification Completed.")

        #Visualize the Tree
        self.visualize(tree_root)

        print("Visualization Completed.")

    def select_file(self):
        print("Waiting for File Selection...")
        source_file_path = tk.filedialog.askopenfilename(parent = root, title = Strings.get("selectFileTitle"),filetypes = (("Hmtl Files","*.html"),("All Files","*.*")))
        self.selected_file_path.delete(0, tk.END)
        self.selected_file_path.insert(tk.INSERT, source_file_path)
        print("File Selected.")

    def open_file(self):
        source_file_path = self.selected_file_path.get()

        try:
            sf = open(source_file_path, encoding="utf8").read()
            extension = os.path.splitext(source_file_path)[1]
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
        return sf

    def treeify(self, family_members):
        family_members.reverse() #Reversing since the relation level decreases going through the list in the original order.
        family_root = node(family_members[0])
        for member in family_members:
            family_root.insert(member) 
        family_root.print_tree() #Inorder print to console
        return family_root

    def visualize(self, tree_root):
        self.master.update_idletasks()
        self.canvas.config(width = self.master.winfo_width()/2, height = self.master.winfo_height() - 100)
        self.display_frame.config(width = self.master.winfo_width()/2, height = self.master.winfo_height() - 100)
        self.display_frame.update_idletasks()
        self.canvas.update_idletasks()
        self.canvas.delete("all")
        tree_root.visualize_tree(self.canvas)

root = tk.Tk()
root.update()
app = Application(master=root)
app.mainloop()