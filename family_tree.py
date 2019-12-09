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
        self.details = None

        self.tree_root = None

    def create_widgets(self):
        self.top = tk.Frame(self)
        self.bottom = tk.Frame(self)
        self.top.bind("<Button-1>", self.click_on_node)
        self.top.pack(side="top")
        self.bottom.pack(side="bottom", fill=tk.X)

        self.canvas = tk.Canvas(self,width = self.master.winfo_width()*3/4, height = self.master.winfo_height() - 100)
        self.canvas.pack(in_= self.top,side="left")

        self.display_frame = tk.Frame(self,width = self.master.winfo_width()/4, height = self.master.winfo_height() - 100)
        self.display_frame.pack(in_= self.top,side="right")

        self.selected_file_path = tk.Entry(self)
        self.selected_file_path.insert(tk.INSERT, Strings.get("selected_file_placeholder"))
        self.selected_file_path.pack(in_= self.bottom,side="top", fill=tk.X)

        self.select_file_button = tk.Button(self)
        self.select_file_button["text"] = Strings.get("select_file_button")
        self.select_file_button["command"] = self.select_file
        self.select_file_button.pack(in_= self.bottom,side="top", fill=tk.X)

        self.tree_visualizer_button = tk.Button(self)
        self.tree_visualizer_button["text"] = Strings.get("visualize_button")
        self.tree_visualizer_button["command"] = self.visualize_tree
        self.tree_visualizer_button.pack(in_= self.bottom,side="top", fill=tk.X)

        self.quit = tk.Button(self, text="QUIT", fg="white", bg="red",
                              command=self.master.destroy)
        self.quit.pack(in_= self.bottom,side="bottom", fill=tk.X)

    def create_details_widgets(self, frame, attributes=None):
        if self.details is not None:
            return True
        else:
            self.details = dict()
        for attribute in attributes:
            label = tk.Label(self, text=attribute+": \t"+Strings.get("select_a_node_placeholder"), anchor=tk.W)
            label.pack(in_= frame, side="top", fill=tk.BOTH)
            self.details[attribute] = label
        return True

    def visualize_tree(self):
        print("Starting Treeification...")

        #Parse the selected file
        p = parser(self.open_file())
        family_members = p.parse()
        attributes = p.get_attributes()

        print("Parsing Completed.")

        #Treeify the List
        tree_root = self.treeify(family_members)
        self.tree_root = tree_root

        print("Treeification Completed.")

        #Visualize the Tree
        self.visualize(tree_root) #Draw the tree
        self.create_details_widgets(self.display_frame, attributes) #Create the details frame
        
        #Bind mouse click to enable node selection
        self.master.bind("<Button-1>", self.click_on_node)

        print("Visualization Completed.")

    def select_file(self):
        print("Waiting for File Selection...")
        source_file_path = tk.filedialog.askopenfilename(parent = root, title = Strings.get("select_file_title"),filetypes = (("Hmtl Files","*.html"),("All Files","*.*")))
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
        self.canvas.config(width = self.master.winfo_width()*3/4, height = self.master.winfo_height() - 100)
        self.display_frame.config(width = self.master.winfo_width()/4, height = self.master.winfo_height() - 100)
        self.canvas.delete("all")
        tree_root.visualize_tree(self.canvas)

    def click_on_node(self, event):
        current = self.canvas.find_withtag(tk.CURRENT)
        if current:
            tags = self.canvas.gettags(current)
            if "text" in tags:
                previous = self.canvas.find_withtag("selected")
                if previous:
                    self.canvas.dtag(previous, "selected")
                    self.canvas.itemconfig(previous, fill="black")
                self.canvas.itemconfig(current, fill="blue")
                self.canvas.addtag_withtag("selected", current)

                for data in self.tree_root.search(tags[1]):
                    for attribute in data:
                        self.details[attribute].config(text=attribute+": \t"+data[attribute])
                

root = tk.Tk()
root.update()
app = Application(master=root)
app.mainloop()